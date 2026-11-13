# EVL™ Skills

Agent skills for [EVL](https://github.com/ilyaslabs/evl-lib), the Engineering Visualization Language for JVM architecture and workflow documentation. They work without the IntelliJ plugin; they need the `evl` CLI (Java 17+), which `scripts/ensure-evl.sh` installs on demand.

Targets spec **1.0** and CLI **1.0.0+** (see [`spec.lock`](spec.lock)).

## Install

**Claude Code**

```
/plugin marketplace add ilyaslabs/evl-skills
/plugin install evl@evl-skills
```

**Codex and other agents:** copy `codex/skills/*` into your agent's skills folder, or point the agent at [`AGENTS.md`](AGENTS.md).

**Any Agent Skills-compatible tool:** each folder in [`skills/`](skills/) is a self-contained skill (`SKILL.md`, `references/`, `scripts/`).

## Skills

| Skill | Purpose |
|---|---|
| `evl-fundamentals` | Understand EVL and read a project's architecture before changing code |
| `evl-document` | Document modules, components, dependencies, APIs, data, events, config, decisions, requirements |
| `evl-workflows` | Document business and technical flows |
| `evl-maintain` | Keep docs correct after code changes |
| `evl-validate` | Run validation and fix diagnostics |

## Development

- `references/` and `codex/` are generated: `python3 tools/generate_references.py <path-to-evl-lib>` (checkout of the `ref` in `spec.lock`). CI fails when they are stale.
- `python3 tools/lint.py` checks frontmatter, line limits and links.
- `evals/` holds scenario tests; `python3 evals/run.py --lint` checks them offline, `python3 evals/run.py --runs 3` runs them with Claude Code headless (needs `ANTHROPIC_API_KEY` and the `evl` CLI). Release requires ≥ 90% pass rate.

## License

Apache License 2.0. "EVL" is a trademark, see [TRADEMARKS.md](TRADEMARKS.md).
