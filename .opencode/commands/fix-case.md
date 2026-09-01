---
description: Reproduce and fix a failing Nuitka-Watch case against a Nuitka checkout (../Py2C or ../Nuitka-develop). Use when a case crashes at compile time or runtime.
agent: case-fix
---

Reproduce and fix the failing case described below. Follow `.opencode/agents/case-fix.md` exactly.

Precise arguments (passed as `$ARGUMENTS` below):

- `<Case>` name and `<python-version>-<OS>` dir e.g. `Kivy 3.14-Win32` or `Dask 3.12-Linux`
- optional checkout override: `../Py2C` (default) or `../Nuitka-develop`
- attach the relevant `compilation-report.xml` snippet / traceback / `compiled-stderr.txt` if
  available

If the case venv is missing, note it; otherwise locate it via `pipenv --venv` run from the case
result dir.

$ARGUMENTS
