---
name: "source-command-log-human-time"
description: "Append a human work session to submission/human_time_log.md and recompute running totals"
---

# source-command-log-human-time

Use this compatibility skill when the user asks for `/log-human-time`,
`log-human-time`, or human work time logging.

## Command Template

Run the `log-human-time` skill. Use the session details from the user's prompt;
ask for missing date, start, end, author, stage, activity, or deliverable.

Steps:
1. Parse date, start, end, author, stage, activity, and deliverable touched.
2. Compute duration and append a new row to `submission/human_time_log.md`.
3. Recompute the running totals table.
4. Validate (date on or after 2026-06-01, end > start, length sanity).
