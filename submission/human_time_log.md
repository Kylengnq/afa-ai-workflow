# Human Time Log

A running record of every human work session on this project. The AFA call
requires "a time log of human activity"; this is that log.

Append a row for each session using `/log-human-time`, or edit this file
directly. Keep entries in chronological order. Do not log project work before
2026-06-01.

## Sessions

| Date | Start | End | Duration | Author | Stage | Activity | Deliverable touched |
|---|---|---|---|---|---|---|---|

## Running totals

| Author | Total hours | Sessions |
|---|---|---|

## Conventions

- **Stage**: one of `idea`, `literature`, `design`, `data`, `analysis`,
  `robustness`, `writing`, `revision`, `submission-prep`, `meta`.
- **Activity**: short verb phrase ("ran regression by hand," "reviewed agent
  output," "wrote intro paragraph 3").
- **Deliverable touched**: file path relative to repo root.
- If a session interleaves AI prompting and direct human work, log only the
  human-clock-time and note the interleave in **Activity**.
- Example session row: `| 2026-06-01 | 09:00 | 09:30 | 0h 30m | Author Name | idea | drafted initial prompt | submission/initial_prompt.md |`
