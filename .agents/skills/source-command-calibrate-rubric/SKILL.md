---
name: "source-command-calibrate-rubric"
description: "Build or refresh references/top_journal_calibration.json \u2014 the held-out anchor that gates \"Top Generalist Candidate\" labels in /brainstorm and /idea"
---

# source-command-calibrate-rubric

Use this compatibility skill when the user asks for `/calibrate-rubric`,
`calibrate-rubric`, or a top-journal calibration refresh.

## Command Template

Run the `calibrate-rubric` skill. Use any target journals, recency window, or
topic coverage constraints from the user's prompt.

Steps:
1. Pull recent top-3 acceptances (last 24 months) via `top_cited_articles` and `search_papers` filtered to JF, JFE, RFS.
2. Pull stalled analogs (2–4 years old, low citations, not placed at top-3) matched to the acceptance topic areas.
3. Extract per-paper fields (question, contribution claim, mechanism, identification style, generating lens, displacement target, closest papers at time of writing).
4. Write `references/top_journal_calibration.json`.
5. Sanity-check coverage (≥15 accepted, ≥10 stalled, ≥6 lenses covered, stalled papers should mostly have weak displacement targets).
6. Append to `notes/lab_notebook.md` and `output/search_log.md`.
