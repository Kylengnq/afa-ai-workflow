---
description: Build or refresh references/top_journal_calibration.json — the held-out anchor that gates "Top Generalist Go" labels in /brainstorm and /idea
---

Run the `calibrate-rubric` skill.

Optional inputs (target journals, recency window, topic coverage):

$ARGUMENTS

Steps:
1. Pull recent top-3 acceptances (last 24 months) via `top_cited_articles` and `search_papers` filtered to JF, JFE, RFS.
2. Pull stalled analogs (2–4 years old, low citations, not placed at top-3) matched to the acceptance topic areas.
3. Extract per-paper fields (question, contribution claim, mechanism, identification style, generating lens, displacement target, closest papers at time of writing).
4. Write `references/top_journal_calibration.json`.
5. Sanity-check coverage (≥15 accepted, ≥10 stalled, ≥6 lenses covered, stalled papers should mostly have weak displacement targets).
6. Append to `notes/lab_notebook.md` and `output/search_log.md`.
