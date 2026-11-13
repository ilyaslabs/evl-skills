#!/usr/bin/env python3
"""EVL skills evals (EVL-SKL-010..012).

  run.py --lint                      check scenario files offline
  run.py --baseline                  apply each setup and run the checks with no agent:
                                     every scenario must fail at least one check (else it tests nothing)
  run.py [--runs 3] [--only 04]      run Claude Code headless with the skills, then the checks

Environment: EVL_LIB  path to an evl-lib checkout (fixtures and payments-sdk library)
             EVL_CLI  command for the CLI, e.g. "java -jar evl-cli-1.0.0-all.jar" (default: evl)
             CLAUDE   command for Claude Code (default: claude)
"""
import argparse
import fnmatch
import json
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
SCENARIOS = HERE / "scenarios"
CHECK_KEYS = {"baselinePasses", "validate", "elements", "minKinds", "maxNewElements", "diffContains", "allowedPaths", "noSecrets"}
SETUP_KEYS = {"stripEvl", "delete", "write", "commit", "replace", "replaceAll", "move"}
SECRET = re.compile(r"(-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|sk_live_[0-9a-zA-Z]{16,}|"
                    r"(?i:password|secret|api[-_]?key)\s*[:=]\s*[\"']?[A-Za-z0-9/+_\-]{12,})")
PASS_RATE = 0.9


def load(only=None):
    out = []
    for p in sorted(SCENARIOS.glob("*.yaml")):
        if only and not p.name.startswith(only):
            continue
        out.append((p, yaml.safe_load(p.read_text())))
    return out


def lint(lib):
    errors = []
    skills = {p.parent.name for p in (REPO / "skills").glob("*/SKILL.md")}
    for p, s in load():
        for key in ("name", "fixture", "prompt", "checks"):
            if key not in s:
                errors.append(f"{p.name}: missing {key}")
        unknown = set(s.get("checks", {})) - CHECK_KEYS
        if unknown:
            errors.append(f"{p.name}: unknown checks {sorted(unknown)}")
        unknown = set(s.get("setup", {}) or {}) - SETUP_KEYS
        if unknown:
            errors.append(f"{p.name}: unknown setup {sorted(unknown)}")
        for sk in s.get("skills", []):
            if sk not in skills:
                errors.append(f"{p.name}: unknown skill {sk}")
        if lib and not (lib / "examples" / s.get("fixture", "?")).is_dir():
            errors.append(f"{p.name}: fixture {s.get('fixture')} not in {lib}/examples")
    return errors


def sh(cmd, cwd, env=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"{cmd} failed: {r.stdout}{r.stderr}")
    return r


def strip_evl(text):
    """Remove @EVL.* annotations (with balanced parentheses) and the EVL import."""
    text = re.sub(r"^import io\.github\.ilyaslabs\.evl\.EVL;\n", "", text, flags=re.M)
    out, i = [], 0
    for m in re.finditer(r"@EVL\.[A-Za-z.]+", text):
        if m.start() < i:
            continue
        out.append(text[i:m.start()])
        j = m.end()
        if j < len(text) and text[j] == "(":
            depth, in_str = 0, False
            while j < len(text):
                c = text[j]
                if in_str:
                    if c == "\\":
                        j += 1
                    elif c == '"':
                        in_str = False
                elif c == '"':
                    in_str = True
                elif c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
        while j < len(text) and text[j] in " \t":
            j += 1
        if j < len(text) and text[j] == "\n" and (not out[-1] or out[-1].endswith(("\n", " "))):
            out[-1] = out[-1].rstrip(" \t")
            j += 1
        i = j
    out.append(text[i:])
    return "".join(out)


def apply_setup(work, setup):
    setup = setup or {}
    if setup.get("stripEvl"):
        for f in work.rglob("*.java"):
            f.write_text(strip_evl(f.read_text()))
    for d in setup.get("delete", []):
        t = work / d
        shutil.rmtree(t) if t.is_dir() else t.unlink(missing_ok=True)
    for path, content in (setup.get("write") or {}).items():
        t = work / path
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(content)
    if setup.get("commit"):
        commit(work, "setup part 1")
    for r in setup.get("replace", []):
        f = work / r["file"]
        text = f.read_text()
        if r["old"] not in text:
            raise RuntimeError(f"setup: '{r['old']}' not in {r['file']}")
        f.write_text(text.replace(r["old"], r["new"], 1))
    for m in setup.get("move", []):
        (work / m["to"]).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(work / m["from"], work / m["to"])
    for r in setup.get("replaceAll", []):
        for f in work.glob(r["glob"]):
            f.write_text(f.read_text().replace(r["old"], r["new"]))


def commit(work, msg):
    sh(["git", "add", "-A"], work)
    sh(["git", "-c", "user.name=eval", "-c", "user.email=eval@example.invalid", "commit", "-qm", msg, "--allow-empty"], work)


def evl(cli, args, cwd):
    return subprocess.run(shlex.split(cli) + args, cwd=cwd, capture_output=True, text=True)


def index(cli, work, libdir):
    r = evl(cli, ["index", ".", "--classpath", str(libdir)], work)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"elements": []}


def local(elements):
    return [e for e in elements if ":" not in e["key"] or e["key"].startswith("application:")]


def run_checks(s, work, cli, libdir, before):
    c = s["checks"]
    failures = []
    if c.get("validate"):
        r = evl(cli, ["validate", ".", "--classpath", str(libdir)], work)
        if r.returncode != 0:
            failures.append("validate: " + " | ".join(l for l in r.stdout.splitlines() if " error " in l)[:500])
    idx = index(cli, work, libdir)
    elements = local(idx.get("elements", []))
    ids = {e["id"] for e in elements} | {e["key"] for e in elements}
    for want in c.get("elements", []):
        if want not in ids:
            failures.append(f"missing element {want}")
    counts = {}
    for e in elements:
        counts[e["kind"]] = counts.get(e["kind"], 0) + 1
    for kind, n in (c.get("minKinds") or {}).items():
        if counts.get(kind, 0) < n:
            failures.append(f"expected at least {n} {kind}, found {counts.get(kind, 0)}")
    if "maxNewElements" in c:
        added = {e["key"] for e in elements} - before
        if len(added) > c["maxNewElements"]:
            failures.append(f"{len(added)} new elements (max {c['maxNewElements']}): {sorted(added)[:10]}")
    sh(["git", "add", "-A"], work)
    names = sh(["git", "diff", "--cached", "--name-only", "HEAD"], work).stdout.split()
    patch = sh(["git", "diff", "--cached", "HEAD"], work).stdout
    added_lines = "\n".join(l[1:] for l in patch.splitlines() if l.startswith("+") and not l.startswith("+++"))
    for pattern in c.get("diffContains", []):
        if not re.search(pattern, added_lines):
            failures.append(f"diff lacks /{pattern}/")
    allowed = c.get("allowedPaths")
    if allowed:
        bad = [n for n in names if not any(fnmatch.fnmatch(n, g) for g in allowed)]
        if bad:
            failures.append(f"changed files outside scope: {bad}")
    if c.get("noSecrets") and SECRET.search(added_lines):
        failures.append("diff adds something that looks like a secret")
    return failures


def prepare(s, lib, tmp):
    work = tmp / "work"
    shutil.copytree(lib / "examples" / s["fixture"], work)
    sh(["git", "init", "-q"], work)
    commit(work, "fixture")
    apply_setup(work, s.get("setup"))
    commit(work, "setup")
    return work


def agent(s, work, claude, cli):
    bin_dir = work.parent / "bin"
    bin_dir.mkdir(exist_ok=True)
    shim = bin_dir / "evl"
    shim.write_text(f"#!/bin/sh\nexec {cli} \"$@\"\n")
    shim.chmod(0o755)
    env = dict(os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    cmd = shlex.split(claude) + ["-p", s["prompt"], "--plugin-dir", str(REPO), "--permission-mode",
                                 "bypassPermissions", "--max-turns", "60", "--output-format", "json"]
    return subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, timeout=1800)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint", action="store_true")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--only")
    ap.add_argument("--report", default="eval-report.json")
    a = ap.parse_args()
    lib = pathlib.Path(os.environ["EVL_LIB"]).resolve() if os.environ.get("EVL_LIB") else None
    errors = lint(lib)
    if errors or a.lint:
        print("\n".join(errors) or f"{len(load())} scenarios OK")
        sys.exit(1 if errors else 0)
    if lib is None:
        sys.exit("EVL_LIB must point to an evl-lib checkout")
    cli = os.environ.get("EVL_CLI", "evl")
    claude = os.environ.get("CLAUDE", "claude")
    results = []
    with tempfile.TemporaryDirectory() as t:
        libdir = pathlib.Path(t) / "payments-lib"
        r = evl(cli, ["package", str(lib / "examples" / "payments-sdk"), "--out", str(libdir)], t)
        if r.returncode != 0:
            sys.exit("evl package failed: " + r.stdout + r.stderr)
        for p, s in load(a.only):
            for run in range(1 if a.baseline else a.runs):
                tmp = pathlib.Path(tempfile.mkdtemp(dir=t))
                work = prepare(s, lib, tmp)
                before = {e["key"] for e in local(index(cli, work, libdir).get("elements", []))}
                if not a.baseline:
                    agent(s, work, claude, cli)
                failures = run_checks(s, work, cli, libdir, before)
                ok = (bool(failures) or s.get("baselinePasses", False)) if a.baseline else not failures
                results.append({"scenario": p.stem, "run": run + 1, "passed": ok, "failures": failures})
                print(f"{'PASS' if ok else 'FAIL'} {p.stem} #{run + 1}" + ("" if ok and not a.baseline else
                      "".join(f"\n    {f}" for f in failures)))
    rate = sum(r["passed"] for r in results) / max(len(results), 1)
    pathlib.Path(a.report).write_text(json.dumps({"passRate": rate, "results": results}, indent=2))
    print(f"pass rate {rate:.0%}")
    if a.baseline:
        sys.exit(0 if rate == 1 else 1)
    sys.exit(0 if rate >= PASS_RATE else 1)


if __name__ == "__main__":
    main()
