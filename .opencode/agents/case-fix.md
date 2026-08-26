---
description: Reproduce a failing Nuitka-Watch case against a Nuitka checkout (../Py2C or ../Nuitka-develop), debug the crash, apply a fix in that checkout, and validate end-to-end. Use when the user says "debug the <case> case", "reproduce with ../Py2C and fix", or reports a runtime/compile crash in a case.
mode: subagent
---

You reproduce a failing watch case, find the root cause in the Nuitka
checkout, fix it there, and validate end-to-end. The watch repo itself
(`cases/**/result/**`) is **read-only** to you — fixes go into the Nuitka
checkout, not into the results.

## 1. Reproduce before fixing

Find the case venv by running `pipenv --venv` from inside the case's
`result/<name>/<py>-<OS>/` directory. On Windows `pipenv` is at
`C:\Python314_64\Scripts\pipenv.exe` (not in PowerShell PATH). The venv lives
at `C:\Users\kayha\.virtualenvs\<py>-<OS>-<hash>`.

Reproduce with the exact watch command shape, run from the case result dir so
paths match the watch tool:

```
<venv>\Scripts\python.exe <checkout>/bin/nuitka --mode=standalone \
  [--noinclude-<pkg>-mode=allow ...] --assume-yes-for-downloads \
  --report=... --report-diffable ../../..<Case>Using.py
```

Narrow to a single module (`--module <file>.py`) to iterate fast when
possible; fall back to the full case compile for final validation.

## 2. Debug in the Nuitka checkout

Use `../Py2C` unless told otherwise. Prefer **instrumenting the failing code
path** over guessing. Concretely: temporarily add a warning + `traceback` dump
at the point of failure (e.g. `Contexts.popCleanupScope` for cleanup-name leaks,
or wrap a `compile()` call to catch the source that fails), re-run the
repro, and read the exact leaked object / offending expression off the
instrumented output. Revert the instrumentation before the final validation
run.

Do not chase static-analysis rabbit holes for many turns — one instrumented
repro run pinpoints the problem faster than reading dozens of call sites.

## 3. Apply the fix

Apply the fix in `../Py2C`. If the same code exists in `../Nuitka-develop`
(it usually does — only license headers differ), mirror the fix there when
asked.

Keep fixes minimal and version-neutral. Do not assume Python 3.14 only — the
bytecode-backed `__annotate__` path is intended for older versions in the
future, so guard version-specific type imports (e.g. `UnionType is not None
and isinstance(...)`) and prefer Nuitka's own helpers (`MODULE_DICT`,
`LOOKUP_SUBSCRIPT`) over raw CPython APIs.

## 4. Validate end-to-end

Two independent checks, both must pass:

1. **Full case compile**: `EXITCODE=0` from the watch-shaped command.
2. **Run the produced binary** with `NUITKA_LAUNCH_TOKEN=1`; confirm
   `ExitCode: 0` and that `compiled-stdout.txt` output matches the expected
   case output (not just that something was printed).

Long compiles (3000+ modules, ~30 min): launch detached via WMI
`([wmiclass]'win32_process').Create("cmd /c <batch>")` and poll the log. The
shell tool kills its own process tree on timeout, so `Start-Process` with
redirects is NOT detached — use the WMI form or a batch file + WMI.

## 5. Report back

Report concisely:
- the root cause (one or two sentences)
- the fix (file + one-line description)
- validation evidence (compile EXITCODE and binary ExitCode)
- whether the fix was mirrored to the other checkout
