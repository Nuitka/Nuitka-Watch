# Nuitka Release Review Workflow

Use this workflow when reviewing `Nuitka-Watch` result changes for a new
Nuitka release against the upstream changelog.

## Goal

Summarize local result changes by kind, decide which changes are expected
from the Nuitka release notes, and call out anything that looks like
fixture drift, dependency bloat, or a possible regression. For bundle
growth findings, identify the exact trigger module and import chain, not
just the final DLLs.

## Inputs

- Local git worktree changes in this repository
- The Nuitka release version under review, e.g. `4.1rc11`
- The relevant upstream changelog excerpt or release notes
- Run provenance:
  - standard and commercial binary checkouts and their reported versions
  - `NUITKA_EXTRA_OPTIONS` and `--nuitka-update-mode`
  - whether `fake-x11-display.sh` was sourced for GUI cases
  - whether the run was partial or resumed

  The report `<command_line>` and `<user-data>` entries are the authoritative record; the
  `nuitka_version` string alone does not identify the build.

## Scope

- Prefer reviewing tracked result files under `cases/**/result/**`
- Staged changes are mostly what `auto-stage.sh` identified and the user accepted. They are
  generally more informative, but are supposed to be harmless for the review. Still check them,
  but treat unstaged and untracked changes as the primary review target.
- Treat broad auto-generated report refreshes differently from
  hand-curated case changes
- Do not review report schema compatibility itself; schema shape may
  change freely between releases

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

1b. Establish run provenance and completeness.

   Read the report `<command_line>` and `<user-data>` entries. Confirm:

   - standard/commercial binary versions and flavor
   - `NUITKA_EXTRA_OPTIONS` and `--nuitka-update-mode`
   - whether GUI cases had a usable X display (`fake-x11-display.sh`)
   - whether the run is partial: `compiled-exit.txt`, non-empty stderr, short or empty stdout, or
     later cases that were never refreshed

   The `nuitka_version` string alone does not identify the build; two runs can report the same
   version and differ by commit or options.

2. Split the diff into buckets.

   Classify changes into:

   - staged changes: mostly `auto-stage.sh` output accepted by the user; generally more informative
     but expected to be harmless for review
   - unstaged tracked result refreshes: the primary review target
   - untracked result trees for new cases or results not yet staged: the primary review target
   - non-result changes, if any

3. Check whether staged XML changes are only version-header or optimization-time updates.

   Staged changes are expected to be harmless. If they contain payload, plugin, or runtime-output
   changes, treat that as a finding rather than assuming `auto-stage.sh` was correct.

   Typical command:

   ```powershell
   git diff --cached --unified=0 -- <path-to-report.xml>
   ```

4. Sample representative changed reports and compare semantics, not just
   raw line counts.

   Look for:

   - plugin inventory changes
   - added or removed modules
   - added or removed DLLs, extensions, and data files
   - changed reasons on modules and included payloads
   - new package namespaces appearing in `source_path` values

   Typical commands:

   ```powershell
   git diff --unified=0 -- <path-to-report.xml>
   rg -n "<module name=|<included_extension|<included_dll|reason=" <path-to-report.xml>
   ```

4b. Check for version- or OS-specific command-line options.

   Some command-line options are only injected for certain Python versions
   or OSes by the watch tool. Their presence or absence across reports in
   the same diff is **expected** — it does not indicate a mixed run. But
   it should be documented so that the reviewer does not mistake them for
   version inconsistency.

   Known version/OS-specific options:

   | Option                                     | Applies to     | Reason                                                                                                                                          |
   |--------------------------------------------|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
   | `--devel-no-bytecode-to-compiled-fallback` | Python >= 3.14 | Disables the bytecode-to-compiled fallback for `__annotate__` functions; injected automatically by the watch tool for `python_version >= 0x3E0` |

   When reviewing, note any new entries that should be added to this table.

   Typical command:

   ```powershell
   git diff --unified=0 -- <path-to-report.xml> | Select-String "option value"
   ```

5. Do a bloat and transitive-dependency pass for changed standalone
   payloads.

   Focus on newly included runtime pieces that are not obviously needed
   by the case itself.

   Look for:

   - GUI stacks pulled into non-GUI cases, e.g. `tkinter`, Qt, X11
   - codec, media, database, or browser payloads appearing unexpectedly
   - a package support rule for one package dragging in helpers from
     another package
   - anti-bloat conditions flipping from disabled to enabled or vice
     versa
   - a new plugin reason causing extra modules to be followed

   For every suspicious addition, trace:

   - which added module or DLL is new
   - which package namespace it comes from
   - which concrete module first crosses into the unexpected namespace
   - the import chain from the case-relevant package to that module
   - which `reason=` or `module_usage` path explains why it was pulled
   - whether a plugin or control-tag condition explains why the path was
     active
   - whether the Nuitka changelog explicitly justifies the growth

   Example regression pattern:

   - a Kivy case starts bundling Pillow's `PIL._tkinter_finder`,
     `_tkinter.so`, and X11/Tk libraries even though the case does not
     exercise Tk directly
   - the concrete chain is
     `PIL.SpiderImagePlugin -> PIL.ImageTk -> tkinter -> _tkinter`

6. If a suspected bloat regression has a candidate fix, validate it with
   one real watch case.

   Prefer one representative Python version rather than refreshing every
   platform immediately.

   Validation flow:

   - preserve the current watched result first, at least
     `compilation-report.xml`, and optionally a dist-file listing
   - if helpful, do a quick direct compile first to confirm the root
     cause, but treat the real watch case as the source of truth
   - run the actual `nuitka-watch` case against the candidate compiler
     checkout, e.g. `../Py2C`, using `--no-pipenv-update` unless package
     churn is part of the question
   - compare the regenerated watch report and dist payload against the
     preserved copy
   - if the fix is gated on a plugin or control tag, verify both paths
     when practical: default mode should drop the bloat, and the enabled
     mode should still keep the feature working
   - restore the preserved result afterward unless the refreshed result
     is intentionally meant to stay in the checkout

7. Match observed changes to the Nuitka changelog.

   Useful categories:

   - optimization-pass behavior
   - package support changes
   - standalone asset and DLL preservation
   - anti-bloat or dependency-pruning changes
   - standalone dependency expansion that needs justification
   - runtime-output drift from updated third-party packages

8. Review untracked result trees for new cases.

   Verify:

   - `case.yml` requests the reviewed Nuitka line
   - `compilation-report.xml` has `completion="yes"`
   - `compiled-stderr.txt` is empty unless failure is expected
   - `compiled-stdout.txt` looks plausible for the case

9. Write the review summary by kind.

   The summary should separate:

   - clearly expected changes
   - changelog-aligned package/runtime changes
   - possible bloat regressions with the triggering package path
   - fixture or dependency drift
   - residual risks and unverified areas

## Review Heuristics

- Staged changes are mostly `auto-stage.sh` output accepted by the user. They are expected to be
  harmless, but still verify `completion="yes"`, version uniformity, and payload sets; use them as
  context while treating unstaged/untracked changes as the primary review target.
- Establish run provenance before judging a diff. Two runs can report the same `nuitka_version` and
  differ by commit or options; use the report command line, `nuitka_extra_options` user data, and
  partial-run indicators.
- Ignore report schema compatibility and field-shape churn unless the XML
  becomes malformed, loses `completion="yes"`, or no longer lets you
  inspect the packaging graph.
- `compiled-stdout.txt` changes in `latest` cases can come from dependency
  upgrades even when the Nuitka packaging graph did not change.
- New DLL and data-file payloads in standalone reports often map directly
  to package support work in Nuitka release notes.
- Added optimization passes should be treated as expected if they align
  with upstream optimization-pass changes.
- The highest-signal regression class in result refreshes is unexpected
  bundle growth: new DLLs, extensions, or package namespaces that do not
  match the case's direct imports.
- When bundle growth appears, prefer tracing the exact `reason=`,
  trigger module, and package namespace over relying on line-count size
  alone.
- An excluded `module_usage` entry can be evidence that an anti-bloat
  rule worked; only treat it as remaining bloat if the module itself or
  its runtime payload is still present.
- If a suspicious library remains after a fix, verify which module uses
  it before treating it as unresolved. A leftover X11 library can come
  from another extension module and not from the original Tk path.
- Treat package-driven transitive pull-ins separately from benign root
  metadata churn.
- For fix validation, prefer a real watch-case rebuild over an ad-hoc
  compile before concluding that the checked-in result is improved.

## Expected Output

Produce a concise review that answers:

- What is the run provenance and is the run complete?
- What changed by kind?
- Which changes align with the Nuitka changelog?
- Which changes are harmless auto-generated refresh noise?
- Which changes indicate new dependency bloat or transitive pull-ins?
- What is the exact trigger module/import chain for each bloat finding?
- Which changes need follow-up, if any?

## Optional Follow-Up

If asked to commit result changes only, stage and commit only
`cases/**/result/**` paths.

Recent commit style in this repository is:

```text
Changes for Nuitka <version> on <OS>
```
