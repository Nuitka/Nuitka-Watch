# Nuitka-Watch Agent Instructions

This repository drives verification of Nuitka against a large set of PyPI packages. Work here falls
into three modes. Identify which one the user is asking for before acting.

## Sister checkouts

Nuitka source lives in sibling repositories, not inside this repo:

- `../Nuitka-develop` -- the public `develop` branch; the binary the watch cases are compiled
  **with** (`--nuitka-binary`).
- `../Py2C` -- Kay Hayen's private fork; used as the `nuitka-watch` driver and as a scratch checkout
  for reproducing/fixing issues. The watch tool itself runs from here (`../Py2C/bin/nuitka-watch`).
- `../Nuitka-factory` -- the factory branch; used by CI as the watch driver when Py2C is not
  present.

Treat `../Py2C` and `../Nuitka-develop` as **editable worktrees for fixing Nuitka bugs** found via
the watch cases. Fixes discovered while reproducing a case must be applied there and validated
end-to-end before reporting back. Identical bugs usually exist in both; mirror fixes when asked.

## Repository layout

- `cases/<Case>/case.yml` -- case definitions (requirements, OS list, `python_version_req`,
  `version`).
- `cases/<Case>/<Case>Using.py` -- the program compiled by a case.
- `cases/<Case>/result/<result-name>/<python-version>-<OS>/` -- watch outputs:
  `compilation-report.xml`, `compiled-stdout.txt`, `compiled-stderr.txt`, `Pipfile`, `Pipfile.lock`.
- `nuitka-release.sh` / `pypi-update.sh` / `run-watch.sh` / `auto-stage.sh` -- driver scripts.
  `nuitka-release.sh` adds `--no-pipenv-update`; `pypi-update.sh` allows package updates.
- `RELEASE_REVIEW_WORKFLOW.md` -- the canonical diff-review workflow. Follow it for release review
  tasks.

## Mode 1: Release / hotfix review

Trigger: "check the diff", "review the new run", "is this release OK" -- or the slash command
`/review-diff`.

Follow `RELEASE_REVIEW_WORKFLOW.md` as the single source of truth. The `release-review` subagent
(`.opencode/agents/release-review.md`) implements it; do not duplicate its steps here.

Key invariants the primary agent must still enforce when handling Mode 1 directly: every changed
`compilation-report.xml` must have `completion="yes"` (line 2); `nuitka_version` must be uniform;
`compiled-stdout.txt` loss is a regression even if `OK` is printed; build junk (`result/result/`,
`.build/`, `.dist/`, `Pipfile`-only dirs) is flagged not silently fixed.

Do not commit. The user stages results themselves (see `auto-stage.sh`).

## Mode 2: Reproduce and fix a failing case

Trigger: "debug the <case> <py> case", "reproduce with ../Py2C and fix".

1. Find the case venv: `pipenv --venv` run from inside the case's `result/<name>/<py>-<OS>/`
   directory. On Windows `pipenv` is at `%LOCALAPPDATA%/Programs/Python/...` or
   `C:\Python314_64\Scripts\pipenv.exe` (not in PowerShell PATH -- use Git Bash). The venv lives at
   `%USERPROFILE%\.virtualenvs\<py>-<OS>-<hash>` (e.g. `C:\Users\kayha\.virtualenvs\...`).
2. Reproduce the crash **before fixing**, using the exact watch command shape:
   ```
   <venv>\Scripts\python.exe <checkout>/bin/nuitka --mode=standalone \
     [--noinclude-<pkg>-mode=allow ...] --assume-yes-for-downloads \
     --report=... --report-diffable ../../..<Case>Using.py
   ```
   Run from the case result dir so paths match the watch tool.
3. Narrow the repro to a single module (`--module <file>.py`) when possible to iterate fast; fall
   back to the full case compile for final validation.
4. Debug in the Nuitka checkout (`../Py2C` unless told otherwise). Prefer instrumenting the failing
   code path (e.g. add a warning+traceback in `Contexts.popCleanupScope`) over guessing -- the
   instrumentation run reveals the exact leaked object / failing expression.
5. Apply the fix in the checkout. Mirror to `../Nuitka-develop` if the same code exists there (it
   usually does -- only license headers differ).
6. Validate end-to-end: full case compile (`EXITCODE=0`) **and** run the produced `.dist\<Case>.exe`
   with `NUITKA_LAUNCH_TOKEN=1`; confirm `ExitCode: 0` and the expected `compiled-stdout.txt`
   output.
7. Long compiles (3000+ modules, ~30 min): launch detached so the shell tool does not kill the
   compile on timeout. Preferred:
   `Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine="cmd /c <batch>"}`
   (WMIC/`wmiclass` was removed in Win11 24H2). Fallback `Start-Process -NoNewWindow` with log
   polling. Poll the log file until completion.

## Mode 3: Case maintenance

Trigger: "remove 3.14 from the <case> case", "bump the case version" -- or the slash command
`/bump-case`.

Delegated to the `case-maintenance` subagent (`.opencode/agents/case-maintenance.md`) when invoked
via slash command; primary agent may handle directly for trivial edits.

- `python_version_req` syntax (see `cases/Pandas/pyarrow-example/case.yml`):
  `"python_version < 0x3E0"` excludes 3.14+. `0x3E0` = 3.14, `0x3D0` = 3.13.
- Bump `case.yml` `version:` only when the **case program** changes (invalidates old results). A
  `python_version_req` change alone does not invalidate existing results.
- Removing a result dir the case no longer runs: `git rm -r <path>` (it is usually already
  committed). Check all OSes -- Linux/macOS 3.14 dirs may be pulled in later by the user.
- Never commit build artifacts (`.build/`, `.dist/`) into `result/`. If a compile ran from the wrong
  cwd and dumped a nested `result/result/` tree, delete it.

## Watch run mechanics

- `run-watch.sh` hardcodes `--nuitka-binary=../Nuitka-develop/bin/nuitka`. To test against `../Py2C`
  instead, either symlink or invoke `nuitka-watch` directly with
  `--nuitka-binary=../Py2C/bin/nuitka`.
- On Windows, the watch runs under Git Bash (MSYS). `pipenv` is at
  `%LOCALAPPDATA%/Programs/Python/...` or `C:\Python314_64\Scripts\pipenv.exe` (mixed across
  machines, not in PowerShell's PATH -- use Git Bash).
- Python versions per OS (from `run-watch.sh`): Windows 3.10/3.12/3.13/3.14, Linux 3.10-3.14, macOS
  3.10-3.14.
- `cases/*/result/*` files larger than 50 MB should be checked with `git diff --stat` before
  staging; prefer per-case `auto-stage.sh` review.
