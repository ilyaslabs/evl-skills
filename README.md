# EVL™ Skills

An agent skill for [EVL](https://github.com/ilyaslabs/evl-lib), the Engineering Visualization Language for hand-drawn flow maps from JVM code. It works without the IntelliJ plugin; it uses the `evl` CLI (Java 17+), which `scripts/ensure-evl.sh` installs on demand.

Targets spec **2.0** and CLI **2.0.0+** (see [`spec.lock`](spec.lock)).

## Install

**Claude Code**

```
/plugin marketplace add ilyaslabs/evl-skills
/plugin install evl@evl-skills
```

**Codex and other agents:** copy `codex/skills/*` into your agent's skills folder, or point the agent at [`AGENTS.md`](AGENTS.md).

**Any Agent Skills-compatible tool:** each folder in [`skills/`](skills/) is a self-contained skill (`SKILL.md`, `scripts/`).

## Commands

| Claude Code | Codex | What it does |
|---|---|---|
| `/evl:init [notes]` | `/prompts:evl-init` | Map the whole project: entry points, steps, branches, loops, errors, resources; fix CLI warnings |
| `/evl:map <module>` | `/prompts:evl-map` | Map one module or folder |
| `/evl:check [folder]` | `/prompts:evl-check` | Run the CLI, fix warnings, show the flow tree |
| `/evl:update [base]` | `/prompts:evl-update` | Re-tag only what changed in the git diff |

Codex: copy `codex/prompts/*.md` into `~/.codex/prompts/`.

## Skill

| Skill | Purpose |
|---|---|
| `evl-flows` | Tag code with `@Flow("a>b")` paths, `// @flow` markers and `@EVL.*` symbols; check with `evl <dir>` |

The 1.0 skills (YAML documents) were removed with EVL 2.0.

## Development

`python3 tools/lint.py` checks frontmatter, line limits and links. `codex/skills/` must equal `skills/`.

## License

Apache License 2.0. "EVL" is a trademark, see [TRADEMARKS.md](TRADEMARKS.md).
