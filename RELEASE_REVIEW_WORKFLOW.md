# Nuitka Release Review Workflow

Use this workflow when reviewing `Nuitka-Watch` result changes for a new
Nuitka release against the upstream changelog.

## Goal

Summarize local result changes by kind, decide which changes are expected
from the Nuitka release notes, and call out anything that looks like
fixture drift or a possible regression.

## Inputs

- Local git worktree changes in this repository
- The Nuitka release version under review, e.g. `4.1rc11`
- The relevant upstream changelog excerpt or release notes

## Scope

- Prefer reviewing tracked result files under `cases/**/result/**`
- Separate staged changes from unstaged and untracked changes
- Treat broad auto-generated report refreshes differently from
  hand-curated case changes

## Workflow

1. Inspect the worktree shape.

   Typical commands:

   ```powershell
   git status --short --branch
   git diff --stat
   git diff --cached --stat
   git diff --name-only
   git diff --cached --name-only
   ```

2. Split the diff into buckets.

   Classify changes into:

   - staged report version bumps
   - unstaged tracked result refreshes
   - new result trees for new cases
   - non-result changes, if any

3. Check whether staged XML changes are only version-header updates.

   Typical command:

   ```powershell
   git diff --cached --unified=0 -- <path-to-report.xml>
   ```

4. Sample representative changed reports and compare semantics, not just
   raw line counts.

   Look for:

   - new root metadata such as `performance-totals`
   - `scons_environment` becoming populated
   - new `python_binary` nodes
   - plugin inventory changes
   - added or removed modules
   - added or removed DLLs, extensions, and data files

5. Match observed changes to the Nuitka changelog.

   Useful categories:

   - report schema and telemetry changes
   - optimization-pass behavior
   - package support changes
   - standalone asset and DLL preservation
   - runtime-output drift from updated third-party packages

6. Review untracked result trees for new cases.

   Verify:

   - `case.yml` requests the reviewed Nuitka line
   - `compilation-report.xml` has `completion="yes"`
   - `compiled-stderr.txt` is empty unless failure is expected
   - `compiled-stdout.txt` looks plausible for the case

7. Write the review summary by kind.

   The summary should separate:

   - clearly expected changes
   - changelog-aligned package/runtime changes
   - fixture or dependency drift
   - residual risks and unverified areas

## Review Heuristics

- Large XML diffs are often report-schema churn; check for semantic node
  additions before treating them as package regressions.
- `compiled-stdout.txt` changes in `latest` cases can come from dependency
  upgrades even when the Nuitka packaging graph did not change.
- New DLL and data-file payloads in standalone reports often map directly
  to package support work in Nuitka release notes.
- Added optimization passes should be treated as expected if they align
  with upstream optimization-pass changes.

## Expected Output

Produce a concise review that answers:

- What changed by kind?
- Which changes align with the Nuitka changelog?
- Which changes are likely expected auto-generated report updates?
- Which changes need follow-up, if any?

## Optional Follow-Up

If asked to commit result changes only, stage and commit only
`cases/**/result/**` paths.

Recent commit style in this repository is:

```text
Changes for Nuitka <version> on <OS>
```
