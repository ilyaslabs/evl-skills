---
name: evl-validate
description: Validate EVL documentation and fix EVL diagnostics (EVL-Exxx errors, EVL-Wxxx warnings). Use after editing any @EVL annotation, evl.yaml or .evl.yaml file, or when asked to fix EVL validation errors or a failing evlValidate build task.
metadata:
  evl-spec: "1.0"
---

# Validate EVL documentation

## Procedure

1. Run `evl validate --format json` from the application root (where `evl.yaml` is). In Gradle projects `./gradlew evlValidate` does the same with the compiled classpath, which gives more precise source checks.
2. Parse the JSON (schema in [references/agent-interface.md](references/agent-interface.md)): `summary` counts and `diagnostics[]` with `code`, `level`, `message`, `location.file/line/column`, `element`.
3. Fix every `ERROR`. Then fix `WARNING`s that your change introduced. Leave existing warnings you did not cause unless asked.
4. For each code, look it up in [references/rules.md](references/rules.md). `evl inspect <element>` shows the element, its origins and a "Did you mean" suggestion for unresolved references.
5. Re-run until the exit code is `0`. Exit code `2` is a tool failure (bad path, unreadable file): fix the invocation, not the docs.

## Common fixes

| Code | Fix |
|---|---|
| `EVL-E001` | `evl.yaml` needs `evl: "1.0"`, `id`, `name` |
| `EVL-E010` | Two elements share an id: rename the newer one |
| `EVL-E025` | Unresolved reference: use the id `evl inspect` suggests, or the `library:id` form for library elements |
| `EVL-E022` | Library not on the classpath: add the dependency, or run through the Gradle/Maven plugin |
| `EVL-E030`/`E031` | `source:` does not match code or matches several overloads: correct the type or member, add parameter types |
| `EVL-E021`/`E023` | Reference prefix or target kind is wrong for this field |
| `EVL-E061` | Duplicate step id in a flow |
| `EVL-E070` | Sensitive config property has a `defaultValue`: remove it |
| `EVL-E071` | A secret value in docs: remove it, mark the property `sensitive: true` |
| `EVL-E102`/`E103`/`E106`/`E107` | Unknown field, wrong type, missing required field, invalid enum value: check the kind's fields in documents.md. Extension fields need an `x-` prefix |

Never silence an error by lowering its level in `evl.yaml` `rules:` unless the user asks for that. Locked rules cannot be lowered.

## SARIF

`evl validate --format sarif > evl.sarif` produces SARIF 2.1.0 for GitHub code scanning.

## Running the CLI

All commands use the `evl` CLI (Java 17+). If `evl` is not on `PATH`, run `scripts/ensure-evl.sh` (or `scripts/ensure-evl.ps1` on Windows) from this skill folder. It prints what it will download, puts the CLI jar of the matching version in `~/.evl/`, and prints the command to use (`java -jar ~/.evl/evl-cli-<version>-all.jar`).

Exit codes: `0` no errors, `1` errors found, `2` tool failure.
