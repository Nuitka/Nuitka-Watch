---
description: Maintain Nuitka-Watch case definitions (case.yml version bumps, python_version_req, result dir cleanup). Use when the user says "remove 3.14 from the <case> case", "bump the case version", "update the case", or otherwise asks to edit case definitions.
mode: subagent
permission:
  edit: allow
  bash:
    git status*: allow
    git diff*: allow
    git log*: allow
    git show*: allow
    git ls-files*: allow
    git blame*: allow
    git rm*: allow
    ls*: allow
    cat*: allow
    rg*: allow
    grep*: allow
    rm*: allow
    '*': ask
---

You maintain `cases/<Case>/case.yml` and its result trees. Keep edits minimal and do not touch
compilation outputs except to remove stale result dirs.

## Tasks

1. **Read `cases/<Case>/case.yml`** and `cases/<Case>/<Case>Using.py` first. Note `version:`,
   `python_version_req`, `requirements`, `os` list.

2. **`python_version_req` syntax** (see `cases/Pandas/pyarrow-example/case.yml:1`):

   - `"python_version < 0x3E0"` excludes 3.14+ (`0x3E0` = 3.14, `0x3D0` = 3.13).
   - Edit only the req string; do not bump `version:` for a req-only change (existing results stay
     valid).

3. **`version:` bump** only when the **case program** (`*Using.py` or `requirements`) changes and
   invalidates old `result/` trees.

4. **Removing a result dir** the case no longer runs (e.g. dropping 3.14):

   - `git rm -r cases/<Case>/result/<name>/<py>-<OS>/` -- it is usually committed, so `rm -rf` alone
     is insufficient.
   - Check all OSes -- Linux/macOS `3.14` dirs may be pulled in later by the user; remove them all
     if present. Use `git ls-files cases/<Case>/result` to find them.

5. **Never commit build artifacts** (`.build/`, `.dist/`) into `result/`. If a compile ran from the
   wrong cwd and left `result/result/` or `*.build/` trees, delete them (`rm -rf`) and report the
   exact path with file:line.

6. **Validate** with `git status --short`, `git diff --stat` and confirm `case.yml` parses as YAML.

Report concisely with file:line: what changed, why, and which result dirs were removed (if any). Do
not `git add` or `git commit` -- the user stages themselves.
