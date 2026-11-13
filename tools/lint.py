#!/usr/bin/env python3
"""Lint skills: frontmatter, spec version, size limit, local links."""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_LINES = 300


def main():
    spec = yaml.safe_load((ROOT / "spec.lock").read_text())["spec"]
    errors = []
    skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("no skills found")
    for path in skills:
        rel = path.relative_to(ROOT)
        text = path.read_text()
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        fm = yaml.safe_load(m.group(1))
        if fm.get("name") != path.parent.name:
            errors.append(f"{rel}: name must be '{path.parent.name}'")
        desc = fm.get("description") or ""
        if not 20 <= len(desc) <= 1024:
            errors.append(f"{rel}: description must be 20-1024 characters")
        if str((fm.get("metadata") or {}).get("evl-spec")) != spec:
            errors.append(f"{rel}: metadata.evl-spec must be \"{spec}\" (spec.lock)")
        if text.count("\n") > MAX_LINES:
            errors.append(f"{rel}: more than {MAX_LINES} lines")
        for link in re.findall(r"\]\(([^)#]+?)(?:#[^)]*)?\)", text):
            if "://" in link:
                continue
            if not (path.parent / link).exists():
                errors.append(f"{rel}: broken link {link}")
        for script in ("scripts/ensure-evl.sh", "scripts/ensure-evl.ps1"):
            if not (path.parent / script).exists():
                errors.append(f"{rel}: missing {script}")
    for e in errors:
        print(e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
