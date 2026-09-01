---
description: Review the current Nuitka-Watch result diff for a release, hotfix, or PyPI update. Classifies changes, flags regressions and build junk, and matches to the changelog.
agent: release-review
---

Review the current git diff of this Nuitka-Watch repository per `RELEASE_REVIEW_WORKFLOW.md`.

Arguments (all optional, passed as `$ARGUMENTS` below):

- `<version>` e.g. `4.2rc7`, `4.2.1` -- expected `nuitka_version` in reports
- pasted Nuitka changelog excerpt -- use to classify expected vs bloat
- if no version/changelog given, infer from `git diff` `nuitka_version` and report drift

$ARGUMENTS
