#!/usr/bin/env python3
"""Generate skills/*/references/*.md from evl-lib/spec (EVL-PRD-005).

Usage: generate_references.py <path-to-evl-lib>   (writes into this repo)
       generate_references.py <path-to-evl-lib> --check   (exit 1 if out of date)
"""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Which reference files each skill gets.
SKILLS = {
    "evl-fundamentals": ["language.md", "documents.md", "agent-interface.md", "evidence.md"],
    "evl-document": ["language.md", "annotations.md", "documents.md", "rules.md"],
    "evl-workflows": ["workflows.md", "documents.md", "rules.md"],
    "evl-maintain": ["language.md", "annotations.md", "agent-interface.md", "rules.md"],
    "evl-validate": ["rules.md", "agent-interface.md", "language.md"],
}
COPIED = ["language.md", "annotations.md", "documents.md", "workflows.md", "agent-interface.md", "evidence.md"]


def lock():
    return yaml.safe_load((ROOT / "spec.lock").read_text())


def header(ref):
    return f"<!-- Generated from ilyaslabs/evl-lib spec at {ref[:12]} by tools/generate_references.py. Do not edit. -->\n\n"


def rules_md(spec):
    data = yaml.safe_load((spec / "rules.yaml").read_text())
    out = ["# EVL validation rules\n",
           "Every diagnostic `evl validate` can report. `configurable: no` means the level cannot be changed in `evl.yaml` `rules:`.\n",
           "| Code | Level | Title | Meaning | Configurable |", "|---|---|---|---|---|"]
    for r in data["rules"]:
        desc = r["description"].replace("|", "\\|")
        out.append(f"| `{r['code']}` | {r['level']} | {r['title']} | {desc} | {'yes' if r['configurable'] else 'no'} |")
    return "\n".join(out) + "\n"


def relink(text, present):
    """Point links to spec pages this skill does not carry at the spec on GitHub."""
    def fix(m):
        page = m.group(1)
        if page in present:
            return m.group(0)
        return f"](https://github.com/ilyaslabs/evl-lib/blob/main/spec/{page}"
    return re.sub(r"\]\(([a-z-]+\.md)", fix, text)


def render(spec, ref):
    files = {name: (spec / name).read_text() for name in COPIED}
    # Links between spec pages stay relative; links to other chapters go to the docs site already.
    files["rules.md"] = rules_md(spec)
    result = {}
    for skill, names in SKILLS.items():
        for n in names:
            result[ROOT / "skills" / skill / "references" / n] = header(ref) + relink(files[n], names)
        # Each skill is installable on its own, so it carries its own copy of the CLI bootstrap scripts.
        for script in ("ensure-evl.sh", "ensure-evl.ps1"):
            result[ROOT / "skills" / skill / "scripts" / script] = (ROOT / "scripts" / script).read_text()
    # Codex loads skills from codex/skills/<name>/; keep an exact copy.
    for path, text in list(result.items()):
        result[ROOT / "codex" / path.relative_to(ROOT)] = text
    for skill in SKILLS:
        result[ROOT / "codex" / "skills" / skill / "SKILL.md"] = (ROOT / "skills" / skill / "SKILL.md").read_text()
    return result


def main():
    lib = pathlib.Path(sys.argv[1])
    check = "--check" in sys.argv
    ref = lock()["ref"]
    stale = []
    for path, text in render(lib / "spec", ref).items():
        if check:
            if not path.exists() or path.read_text() != text:
                stale.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            if path.suffix == ".sh":
                path.chmod(0o755)
    if stale:
        print("Out of date (run tools/generate_references.py):", *stale, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
