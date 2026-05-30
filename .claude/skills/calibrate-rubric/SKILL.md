---
name: calibrate-rubric
description: "Build the held-out calibration set that anchors /brainstorm and /idea scoring against actual top-3 journal outcomes. Pulls ~40 recent JF/JFE/RFS acceptances and ~40 stalled working-paper analogs via Corbis, tags each with question, mechanism, identification style, displacement target, failure modes, field tags, and calibration confidence, and writes references/top_journal_calibration.json."
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
| Target acceptances per area | No | 8 (≈40 total) |
| Target stalled per area | No | 8 (≈40 total) |

## Steps

### Phase 1: Pull recent top-3 acceptances

For each target journal:

1. `top_cited_articles` with `journalNames: ["<journal>"]`, `minYear: <today - 24mo>`, `matchCount: 25`.
2. `search_papers` with `journalNames: ["<journal>"]`, `minYear: <today - 24mo>`, `sortBy: "citedByCount"`, `matchCount: 25`. (Catches papers not yet highly cited.)

Deduplicate by `id`. Filter to recent (post-acceptance, not just SSRN-posted).
Sample to roughly equal coverage across the topic areas listed in the inputs.
Target ~40 papers total.

### Phase 2: Pull stalled analogs

For each topic area covered by the acceptances:

1. Pick the 2–3 main accepted papers in that area.
2. `search_papers` with their question phrased as a research query, `minYear: <today - 48mo>`, `maxYear: <today - 24mo>`, `matchCount: 20`. The age window selects papers that were drafted 2+ years ago and would have had time to land at a top-3 by now.
3. Filter to papers with `citedByCount < 30` and no `journal` field set to JF/JFE/RFS — i.e., still working papers or placed at field journals.
4. Pick ~8 per area as stalled analogs (~40 total).

This is heuristic, not exact — the goal is a contrast set, not a clean
ground truth. Note when the classification is uncertain.

### Phase 3: Extract per-paper fields

For all ~80 papers, run `get_paper_details_batch` (in groups of 25) and
extract for each:

| Field | Source | Notes |
|---|---|---|
| `id` | Corbis ID | |
| `title` | abstract | |
| `authors` | abstract | |
| `year`, `journal` | abstract | |
| `cited_by_count` | Corbis | |
| `outcome` | manual | `accepted`, `stalled`, or `uncertain` |
| `topic_area` | manual | one of `corporate`, `asset_pricing`, `household`, `intermediaries`, `real_estate`, `other` |
| `field_tags` | manual | array of finer-grained subfield labels (e.g., `governance`, `cross_section`, `banking`, `mortgages`, `entrepreneurial_finance`, `behavioral`). A paper can carry multiple tags — many recent JF papers sit across two fields. |
| `question` | one sentence | derived from abstract, question-first phrasing |
| `contribution_claim` | one sentence | the paper's stated novelty |
| `mechanism` | one phrase | the economic friction or force |
| `identification_style` | label | one of `quasi-experiment`, `structural`, `measurement`, `theory`, `descriptive`, `cross-sectional`, `asset_pricing_test` |
| `generating_lens` | label | best-guess Lens 1–11 from the research-idea-generator taxonomy |
| `displacement_target` | one sentence | what model, paper, or empirical regularity this displaces (best-guess if not stated explicitly) |
| `displacement_category` | label | which of the four categories the target fits: `paper`, `model_claim`, `empirical_regularity`, `assumption_convention_or_belief` |
| `closest_papers_at_writing` | array of IDs | 3–5 closest works cited in the abstract or known from the area |
| `failure_modes` | array (stalled only) | up to 2 tags from the failure-mode taxonomy below; first tag is the *dominant* cause. Empty for accepted. |
| `calibration_confidence` | int 1-5 | how confident this entry is correctly classified (5 = clear top-3 acceptance, displacement target obvious; 1 = uncertain inclusion, may be misread) |
| `selection_bias_note` | one sentence | a one-line note on what could be wrong about including this paper (e.g., "field-cycle peak — area was hot during the acceptance window," "small-sample stalled — may simply be too recent for top-3 timing") |

**Failure-mode taxonomy** (use for stalled papers; up to 2 tags, first is dominant):

| Tag | Meaning |
|---|---|
| `setting_variation_only` | The contribution is "X but in country/industry/period Y" without new economics |
| `unclear_mechanism` | Empirical result documented; underlying economic channel not identified or distinguished |
| `weak_identification` | The design cannot support the causal claim made; pre-trends, weak first-stage, etc. |
| `no_displacement_target` | The paper does not name a specific belief, model, or paper it displaces |
| `incremental_data_extension` | New data on an old question without changing identification or measurement in a first-order way |
| `hard_to_interpret_null` | The paper's value depends on a particular sign; a null teaches nothing |
| `insufficient_external_validity` | Results are local to a narrow population that doesn't generalize |
| `execution_too_complex` | Design is so elaborate that referees can't audit it; or data construction is unreplicable |

For accepted papers, derive `displacement_target` and `displacement_category`
from the abstract's "we show that..." or "contrary to..." statements. For
stalled papers, derive it the same way and note if it's weak — the absence of
a sharp displacement target is often *why* the paper stalled, in which case
`no_displacement_target` should be the dominant failure tag.

When uncertain about the outcome label (e.g., the paper may still be under
review at a top-3), mark `outcome: "uncertain"` and exclude from the
calibration archetype-parity gate downstream.

### Phase 4: Write the calibration file with prebuilt indexes

Write `references/top_journal_calibration.json` with this schema. The three index fields at the end let `/brainstorm` and `/idea` look up archetype anchors in O(1) without scanning the `papers` array.

```json
{
  "version": "2026-05",
  "built_at": "YYYY-MM-DD",
  "window_months": 24,
  "target_journals": ["Journal of Finance", "Journal of Financial Economics", "Review of Financial Studies"],
  "selection_bias_summary": "One-paragraph note on systematic biases in this build: which areas are overweight relative to recent acceptances, which journals are underrepresented, what time window was active.",
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
      "field_tags": ["governance", "intermediaries"],
      "question": "...",
      "contribution_claim": "...",
      "mechanism": "...",
      "identification_style": "quasi-experiment",
      "generating_lens": 1,
      "displacement_target": "...",
      "displacement_category": "paper",
      "closest_papers_at_writing": ["W...", "W..."],
      "failure_modes": [],
      "calibration_confidence": 5,
      "selection_bias_note": "Clear top-3 acceptance with stated displacement; no flags."
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
  "field_tag_index": {
    "governance": ["W...", "W..."],
    "cross_section": ["W..."],
    "banking": ["W..."],
    "mortgages": ["W..."],
    "entrepreneurial_finance": ["W..."],
    "behavioral": ["W..."]
  },
  "identification_style_index": {
    "quasi-experiment": ["W..."],
    "structural": ["W..."],
    "measurement": ["W..."],
    "theory": ["W..."],
    "asset_pricing_test": ["W..."]
  },
  "failure_mode_index": {
    "setting_variation_only": ["W..."],
    "unclear_mechanism": ["W..."],
    "weak_identification": ["W..."],
    "no_displacement_target": ["W..."],
    "incremental_data_extension": ["W..."],
    "hard_to_interpret_null": ["W..."],
    "insufficient_external_validity": ["W..."],
    "execution_too_complex": ["W..."]
  }
}
```

Order the `papers` array: accepted first, then stalled. Within each, group by `topic_area`.

### Phase 4.5: Build the indexes

After populating the `papers` array, derive five indexes by iterating once over the papers:

- `mechanism_index[m]` = list of paper IDs where `mechanism` is `m` (or contains `m` as a substring for compound mechanisms).
- `topic_area_index[t]` = list of paper IDs where `topic_area` is `t`.
- `field_tag_index[ft]` = list of paper IDs where `ft` appears in the paper's `field_tags` array.
- `identification_style_index[i]` = list of paper IDs where `identification_style` is `i`.
- `failure_mode_index[fm]` = list of paper IDs (stalled only) where `fm` appears in the paper's `failure_modes` array. Papers contribute to one entry per tag they carry.

Normalize keys to lowercase snake_case before indexing (e.g., "Limited Attention" → `limited_attention`). All papers (accepted, stalled, uncertain) go into the topic, field-tag, mechanism, and identification indexes — downstream skills split by `outcome` after the lookup. Only stalled papers appear in `failure_mode_index`.

### Phase 5: Sanity check

Before declaring the calibration set built, verify:

- At least 30 accepted and 20 stalled papers extracted.
- Each topic area has at least 4 accepted and 4 stalled papers.
- The 11 lens categories collectively cover at least 7 of the accepted
  papers (no single lens dominates; if Lens 5 — policy shock — accounts for
  more than 35% of acceptances, the topic coverage is biased and should be
  rebalanced).
- Stalled papers' `displacement_target` is empty or weak for at least half
  the sample. (If stalled papers all have sharp displacement targets, the
  classification probably misidentified them.)
- At least 4 of the 8 failure-mode tags appear at least twice. (A taxonomy
  collapsing to one or two tags is unhealthy — the differentiation gate
  downstream becomes useless if every stalled paper carries the same tag.)
- `selection_bias_summary` is populated and names specific overweight areas
  or time-window quirks.
- At least 70% of papers have `calibration_confidence ≥ 3`. If most entries
  are below 3, the calibration set is too speculative to anchor verdicts.

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
verdict is one of the gates for the "Top Generalist Candidate" label.

If the file does not exist, both skills warn the user and skip archetype
benchmarking, downgrading any "Top Generalist Candidate" verdict to "Strong Field
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

## Next steps to suggest

After completing this skill, explicitly tell the user what to do next:

1. **If this was the first calibration build**: "The calibration anchor is now built. Next, run `/brainstorm <your topic>` to generate ten ranked ideas calibrated against the anchor, or `/idea <your specific question>` if you already have one to screen."
2. **If this was a refresh of an older calibration set**: "The calibration set has been refreshed against the recent frontier. Any prior `/brainstorm` or `/idea` verdicts may be slightly recalibrated if you re-run them."
3. **If the calibration set failed sanity checks** (e.g., fewer than 15 accepted papers found): "Calibration coverage is thin in <area>. Re-run with broader topic coverage or wait for more recent acceptances before relying on Top Generalist labels in that area."
