---
name: calibrate-rubric
description: "Build the held-out calibration set that anchors /brainstorm and /idea scoring against actual top-3 journal outcomes. Pulls ~20 recent JF/JFE/RFS acceptances and ~20 stalled working-paper analogs via Corbis, extracts question, contribution, displacement target, and lens classification, and writes references/top_journal_calibration.json."
---

# Calibrate Rubric

Build the external anchor that `/brainstorm` and `/idea` use to gate "Top
Generalist Go" labels. Without this file, those skills cannot do archetype
benchmarking and will fall back to internal scoring only.

## When to use

- First time running the skills in this repo (initial build).
- Periodic refresh (recommended every 6 months — top-journal frontier moves).
- When the user notices the rubric calling too many ideas "top generalist"
  (under-calibrated) or too few (over-calibrated).

## Inputs to collect

| Input | Required? | Default |
|---|---|---|
| Target journals | No | `["Journal of Finance", "Journal of Financial Economics", "Review of Financial Studies"]` |
| Acceptance window | No | Last 24 months from today |
| Stalled-paper age threshold | No | 24+ months on SSRN with no top-3 placement |
| Topic areas to cover | No | All of corporate finance, asset pricing, household finance, intermediaries, real estate |
| Target acceptances per area | No | 4 (≈20 total) |
| Target stalled per area | No | 4 (≈20 total) |

## Steps

### Phase 1: Pull recent top-3 acceptances

For each target journal:

1. `top_cited_articles` with `journalNames: ["<journal>"]`, `minYear: <today - 24mo>`, `matchCount: 25`.
2. `search_papers` with `journalNames: ["<journal>"]`, `minYear: <today - 24mo>`, `sortBy: "citedByCount"`, `matchCount: 25`. (Catches papers not yet highly cited.)

Deduplicate by `id`. Filter to recent (post-acceptance, not just SSRN-posted).
Sample to roughly equal coverage across the topic areas listed in the inputs.
Target ~20 papers total.

### Phase 2: Pull stalled analogs

For each topic area covered by the acceptances:

1. Pick the 2–3 main accepted papers in that area.
2. `search_papers` with their question phrased as a research query, `minYear: <today - 48mo>`, `maxYear: <today - 24mo>`, `matchCount: 20`. The age window selects papers that were drafted 2+ years ago and would have had time to land at a top-3 by now.
3. Filter to papers with `citedByCount < 30` and no `journal` field set to JF/JFE/RFS — i.e., still working papers or placed at field journals.
4. Pick ~4 per area as stalled analogs (~20 total).

This is heuristic, not exact — the goal is a contrast set, not a clean
ground truth. Note when the classification is uncertain.

### Phase 3: Extract per-paper fields

For all ~40 papers, run `get_paper_details_batch` (in groups of 25) and
extract for each:

| Field | Source | Notes |
|---|---|---|
| `id` | Corbis ID | |
| `title` | abstract | |
| `authors` | abstract | |
| `year`, `journal` | abstract | |
| `cited_by_count` | Corbis | |
| `outcome` | manual | `accepted` or `stalled` |
| `topic_area` | manual | one of `corporate`, `asset_pricing`, `household`, `intermediaries`, `real_estate`, `other` |
| `question` | one sentence | derived from abstract, question-first phrasing |
| `contribution_claim` | one sentence | the paper's stated novelty |
| `mechanism` | one phrase | the economic friction or force |
| `identification_style` | label | one of `quasi-experiment`, `structural`, `measurement`, `theory`, `descriptive`, `cross-sectional`, `asset_pricing_test` |
| `generating_lens` | label | best-guess Lens 1–11 from the research-idea-generator taxonomy |
| `displacement_target` | one sentence | what model, paper, or empirical regularity this displaces (best-guess if not stated explicitly) |
| `closest_papers_at_writing` | array of IDs | 3–5 closest works cited in the abstract or known from the area |

For accepted papers, derive `displacement_target` from the abstract's "we
show that..." or "contrary to..." statements. For stalled papers, derive it
the same way and note if it's weak — the absence of a sharp displacement
target is often *why* the paper stalled.

### Phase 4: Write the calibration file with prebuilt indexes

Write `references/top_journal_calibration.json` with this schema. The three index fields at the end let `/brainstorm` and `/idea` look up archetype anchors in O(1) without scanning the `papers` array.

```json
{
  "built_at": "YYYY-MM-DD",
  "window_months": 24,
  "target_journals": ["Journal of Finance", "Journal of Financial Economics", "Review of Financial Studies"],
  "papers": [
    {
      "id": "W...",
      "title": "...",
      "authors": ["..."],
      "year": 2024,
      "journal": "Journal of Finance",
      "cited_by_count": 42,
      "outcome": "accepted",
      "topic_area": "corporate",
      "question": "...",
      "contribution_claim": "...",
      "mechanism": "...",
      "identification_style": "quasi-experiment",
      "generating_lens": 1,
      "displacement_target": "...",
      "closest_papers_at_writing": ["W...", "W..."]
    }
  ],
  "mechanism_index": {
    "limited_attention": ["W...", "W..."],
    "moral_hazard": ["W..."],
    "search_cost": ["W..."]
  },
  "topic_area_index": {
    "corporate": ["W...", "W..."],
    "asset_pricing": ["W..."],
    "household": ["W..."],
    "intermediaries": ["W..."],
    "real_estate": ["W..."]
  },
  "identification_style_index": {
    "quasi-experiment": ["W..."],
    "structural": ["W..."],
    "measurement": ["W..."],
    "theory": ["W..."],
    "asset_pricing_test": ["W..."]
  }
}
```

Order the `papers` array: accepted first, then stalled. Within each, group by `topic_area`.

### Phase 4.5: Build the indexes

After populating the `papers` array, derive the three indexes by iterating once over the papers:

- `mechanism_index[m]` = list of paper IDs where `mechanism` is `m` (or contains `m` as a substring for compound mechanisms).
- `topic_area_index[t]` = list of paper IDs where `topic_area` is `t`.
- `identification_style_index[i]` = list of paper IDs where `identification_style` is `i`.

Normalize keys to lowercase snake_case before indexing (e.g., "Limited Attention" → `limited_attention`). Both `accepted` and `stalled` papers go into the same indexes — downstream skills split by `outcome` after the lookup, which is faster and keeps the index simple.

### Phase 5: Sanity check

Before declaring the calibration set built, verify:

- At least 15 accepted and 10 stalled papers extracted.
- Each topic area has at least 2 accepted and 2 stalled papers.
- The 11 lens categories collectively cover at least 6 of the accepted
  papers (no single lens dominates; if Lens 5 — policy shock — accounts for
  more than 40% of acceptances, the topic coverage is biased and should be
  rebalanced).
- Stalled papers' `displacement_target` is empty or weak for at least half
  the sample. (If stalled papers all have sharp displacement targets, the
  classification probably misidentified them.)

### Phase 6: Log

Append a dated entry to `notes/lab_notebook.md`: build date, counts of
accepted and stalled papers, lens distribution. Append all Corbis queries
used to `output/search_log.md`.

## Outputs

- `references/top_journal_calibration.json` (new or refreshed).
- Entry in `notes/lab_notebook.md`.
- Queries logged to `output/search_log.md`.

## How downstream skills use this file

`/brainstorm` and `/idea` read `references/top_journal_calibration.json`
during their archetype benchmarking phase. For each candidate idea, they
pick 3 accepted analogs and 2 stalled analogs sharing the candidate's
`mechanism`, `identification_style`, or `topic_area`, and write a one-line
parity claim ("at parity / below / above") against each. The parity
verdict is one of the gates for the "Top Generalist Go" label.

If the file does not exist, both skills warn the user and skip archetype
benchmarking, downgrading any "Top Generalist Go" verdict to "Strong Field
Go" with a note that the calibration set is missing.

## Tool integration (Corbis MCP)

- `top_cited_articles` filtered to JF/JFE/RFS for the acceptance pull.
- `search_papers` with journal and date filters for both pulls.
- `get_paper_details_batch` (up to 25 IDs per call) for abstract extraction.

## Refresh policy

The frontier moves. Refresh the calibration set:

- Every 6 months as routine maintenance.
- After any paper in `references/top_journal_calibration.json` reaches 200+
  citations (it's no longer "recent frontier" — move it to a separate
  `accepted_landmarks` section if you want to keep the comparison).
- When `/brainstorm` or `/idea` repeatedly flags candidates as "above
  parity with every accepted analog" — that means the anchors are too old.

## Guardrails

- Do not include the user's own working papers as anchors (avoid
  contaminating the gate with self-judgment).
- Do not include papers from this repo's `output/paper_set.json` directly —
  the calibration set is a separate, journal-outcome-anchored dataset.
- When classifying `generating_lens`, prefer the more rigorous lenses
  (1, 3, 4) when ambiguous — these are the lenses the skill rewards.
- Stalled-paper classification is heuristic. Mark uncertain cases as
  `outcome: "uncertain"` rather than forcing a binary label, and exclude
  them from the gate computation.
