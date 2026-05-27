---
description: Append a human work session to submission/human_time_log.md and recompute running totals
---

Run the `log-human-time` skill.

Session details from the user:

$ARGUMENTS

Steps:
1. Parse date, start, end, author, stage, activity, and deliverable touched.
2. Compute duration and append a new row to `submission/human_time_log.md`.
3. Recompute the running totals table.
4. Validate (date on or after 2026-06-01, end > start, length sanity).
