---
description: Maintain a Nuitka-Watch case (bump case.yml version, edit python_version_req, remove stale result dirs). Use when updating case definitions.
agent: case-maintenance
---

Maintain the case described below per `.opencode/agents/case-maintenance.md`.

Arguments (passed as `$ARGUMENTS` below):
- `<Case>` name e.g. `Dulwich`, `Pandas/pyarrow-example`
- action: `bump version`, `python_version_req < 0x3E0`, `remove 3.14`, `remove result dir <path>`
- if bumping version, state whether `*Using.py` or `requirements` changed (invalidates old results)

$ARGUMENTS
