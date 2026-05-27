---
description: Regenerate submission/contribution_report.md with line-count tallies of human vs AI contributions
---

Run the `contribution-report` skill.

Inputs (committer pattern, human authors, globs) from the user:

$ARGUMENTS

Steps:
1. Confirm the initial-prompt date in `submission/initial_prompt.md` is on or after 2026-06-01.
2. Refuse if `git status --porcelain` reports uncommitted changes.
3. For code, writing, and documentation: walk git history and `git blame` files matching the configured globs, classifying lines as human or AI by committer.
4. Cross-check against transcripts in `submission/conversations/`.
5. Update the headline table, method, and edge-cases sections of `submission/contribution_report.md`.
6. Append a dated entry to `notes/lab_notebook.md`.
