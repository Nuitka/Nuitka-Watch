# Nuitka-Watch Agent Instructions

This repository drives verification of Nuitka against a large set of PyPI
packages. Work here falls into three modes. Identify which one the user is
asking for before acting.

## Sister checkouts

Nuitka source lives in sibling repositories, not inside this repo:

- `../Nuitka-develop` — the public `develop` branch; the binary the watch cases
  are compiled **with** (`--nuitka-binary`).
- `../Py2C` — Kay Hayen's private fork; used as the `nuitka-watch` driver and as
  a scratch checkout for reproducing/fixing issues. The watch tool itself runs
  from here (`../Py2C/bin/nuitka-watch`).
- `../Nuitka-factory` — the factory branch; used by CI as the watch driver when
  Py2C is not present.

Treat `../Py2C` and `../Nuitka-develop` as **editable worktrees for fixing
Nuitka bugs** found via the watch cases. Fixes discovered while reproducing a
case must be applied there and validated end-to-end before reporting back.
Identical bugs usually exist in both; mirror fixes when asked.

## Repository layout

- `cases/<Case>/case.yml` — case definitions (requirements, OS list,
  `python_version_req`, `version`).
- `cases/<Case>/<Case>Using.py` — the program compiled by a case.
- `cases/<Case>/result/<result-name>/<python-version>-<OS>/` — watch outputs:
  `compilation-report.xml`, `compiled-stdout.txt`, `compiled-stderr.txt`,
  `Pipfile`, `Pipfile.lock`.
- `nuitka-release.sh` / `pypi-update.sh` / `run-watch.sh` / `auto-stage.sh` —
  driver scripts. `nuitka-release.sh` adds `--no-pipenv-update`;
  `pypi-update.sh` allows package updates.
- `RELEASE_REVIEW_WORKFLOW.md` — the canonical diff-review workflow. Follow it
  for release review tasks.

## Mode 1: Release / hotfix review

Trigger: "check the diff", "review the new run", "is this release OK".

Follow `RELEASE_REVIEW_WORKFLOW.md`. Concretely:

1. `git status --short`, `git diff --stat`, split staged vs unstaged vs
   untracked.
2. For each changed `compilation-report.xml`, check line 2:
   `completion="yes"` is required; `completion="exception"` is a hard
   regression.
3. Check `nuitka_version` consistency across the diff — a single run must use
   one version. Mixed versions (e.g. rc6 and rc7) mean a half-finished state.
4. Compare `compiled-stdout.txt` diffs — output changes that lose data or go
   empty are runtime regressions even if `OK` is still printed.
5. Flag, do not silently fix: build junk under `result/`, incomplete new
   `3.14-Win32` dirs (only a `Pipfile`), nested `result/result/` trees.
6. Match changes to the Nuitka changelog; report non-improvements by kind.

Do not commit. The user stages results themselves.

## Mode 2: Reproduce and fix a failing case

Trigger: "debug the <case> <py> case", "reproduce with ../Py2C and fix".

1. Find the case venv: `pipenv --venv` run from inside the case's
   `result/<name>/<py>-<OS>/` directory. The venv name is
   `C:\Users\kayha\.virtualenvs\<py>-<OS>-<hash>`.
2. Reproduce the crash **before fixing**, using the exact watch command shape:
   ```
   <venv>\Scripts\python.exe <checkout>/bin/nuitka --mode=standalone \
     [--noinclude-<pkg>-mode=allow ...] --assume-yes-for-downloads \
     --report=... --report-diffable ../../..<Case>Using.py
   ```
   Run from the case result dir so paths match the watch tool.
3. Narrow the repro to a single module (`--module <file>.py`) when possible to
   iterate fast; fall back to the full case compile for final validation.
4. Debug in the Nuitka checkout (`../Py2C` unless told otherwise). Prefer
   instrumenting the failing code path (e.g. add a warning+traceback in
   `Contexts.popCleanupScope`) over guessing — the instrumentation run reveals
   the exact leaked object / failing expression.
5. Apply the fix in the checkout. Mirror to `../Nuitka-develop` if the same
   code exists there (it usually does — only license headers differ).
6. Validate end-to-end: full case compile (`EXITCODE=0`) **and** run the
   produced `.dist\<Case>.exe` with `NUITKA_LAUNCH_TOKEN=1`; confirm `ExitCode: 0`
   and the expected `compiled-stdout.txt` output.
7. Long compiles (3000+ modules, ~30 min): launch detached via WMI
   (`([wmiclass]'win32_process').Create("cmd /c <batch>")`) and poll the log;
   the shell tool kills its own process tree on timeout, so `Start-Process`
   with redirects is NOT detached.

## Mode 3: Case maintenance

Trigger: "remove 3.14 from the <case> case", "bump the case version".

- `python_version_req` syntax (see `cases/Pandas/pyarrow-example/case.yml`):
  `"python_version < 0x3E0"` excludes 3.14+. `0x3E0` = 3.14, `0x3D0` = 3.13.
- Bump `case.yml` `version:` only when the **case program** changes (invalidates
  old results). A `python_version_req` change alone does not invalidate
  existing results.
- Removing a result dir the case no longer runs: `git rm -r <path>` (it is
  usually already committed). Check all OSes — Linux/macOS 3.14 dirs may be
  pulled in later by the user.
- Never commit build artifacts (`.build/`, `.dist/`) into `result/`. If a
  compile ran from the wrong cwd and dumped a nested `result/result/` tree,
  delete it.

## Watch run mechanics

- `run-watch.sh` hardcodes `--nuitka-binary=../Nuitka-develop/bin/nuitka`. To
  test against `../Py2C` instead, either symlink or invoke `nuitka-watch`
  directly with `--nuitka-binary=../Py2C/bin/nuitka`.
- On Windows, the watch runs under Git Bash (MSYS). `pipenv` is at
  `C:\Python314_64\Scripts\pipenv.exe`, not in PowerShell's PATH.
- Python versions per OS (from `run-watch.sh`): Windows 3.10/3.12/3.13/3.14,
  Linux 3.10–3.14, macOS 3.10–3.12.
