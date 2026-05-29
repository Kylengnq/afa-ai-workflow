---
name: "source-command-contribution-report"
description: "Regenerate submission/contribution_report.md with line-count tallies of human vs AI contributions"
---

# source-command-contribution-report

Use this compatibility skill when the user asks for `/contribution-report`,
`contribution-report`, or a refreshed human-vs-AI contribution tally.

## Command Template

Run the `contribution-report` skill. Use any committer pattern, human-author
list, or file globs from the user's prompt.

Steps:
1. Confirm the initial-prompt date in `submission/initial_prompt.md` is on or after 2026-06-01.
2. Refuse if `git status --porcelain` reports uncommitted changes.
3. For code, writing, and documentation: walk git history and `git blame` files matching the configured globs, classifying lines as human or AI by committer.
4. Cross-check against transcripts in `submission/conversations/`.
5. Update the headline table, method, and edge-cases sections of `submission/contribution_report.md`.
6. Append a dated entry to `notes/lab_notebook.md`.
