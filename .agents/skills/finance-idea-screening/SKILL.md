---
name: finance-idea-screening
description: "Screen and refine research ideas in corporate finance, investments, asset pricing, and real estate against a held-out top-3 calibration set. Enforces a displacement-target gate, archetype benchmarking against recent JF/JFE/RFS acceptances and stalled analogs, and an adversarial two-editor desk-reject simulation before issuing a Go / Revise / Kill verdict."
---

# Finance Idea Screening

Turn rough topics into credible paper ideas or kill weak ideas early. Calibrated against actual top-3 journal outcomes, not the model's internal prior.

## Calibration anchor

Before scoring any candidate, read `references/top_journal_calibration.json` if it exists. This file is built by the `calibrate-rubric` skill and contains ~20 recent JF/JFE/RFS acceptances and ~20 stalled working-paper analogs.

The calibration set is the external anchor for the "Top Generalist Go" verdict. Without it, the skill caps at "Strong Field Go" and warns the user.

If the file is missing, suggest running `/calibrate-rubric` first. If the user declines, proceed under the cap.

## Stage 0: Desk-editor screen

Before running the full literature search and scoring workflow, answer four questions in 1-2 sentences each:

1. **Prior-changing:** What broad finance prior would change if this paper is right?
2. **Zero-result value:** Why would the paper still matter if the main estimate is zero or the sign flips?
3. **Question over method:** Is the question more important than the shock, instrument, or dataset?
4. **Desk read:** Could this clear a top generalist journal's desk read today?

If two or more answers are weak, return **Revise** or **Kill** before investing in the full search chain.

**Framing rule:** If the one-sentence summary starts with "Using a novel dataset..." or "Exploiting a policy shock...", force a rewrite until it starts with the finance question. The question must come first; the data or design is the tool, not the contribution.

## Stage 1: Displacement target (hard gate)

Before any scoring, the candidate idea must name in one sentence what it would displace: a specific paper (author, year), a specific model claim (e.g., "the Diamond-Dybvig assumption that all withdrawals are equally informative"), or a specific empirical regularity (e.g., "the documented Monday effect").

Use the prompt:

> "If this paper is accepted, what gets struck out of next year's PhD finance reading list, or which claim in a canonical model becomes wrong?"

**Hard gate:** If the candidate cannot name a concrete displacement target, the verdict is capped at **Strong Field Go** at best. Vague claims ("it would change how we think about X") do not count. The skill shows the user the median displacement target from the calibration set's accepted papers in this topic area as a benchmark, and asks the user to either match that bar or accept the cap.

Record the displacement target on the Idea Card.

## What counts as a strong idea

A strong idea scores well on six dimensions:

1. **Sharp question** — Can you state the research question in one sentence without hedging? Is there a clear dependent variable and a testable prediction?
2. **First-order importance** — Would the answer change priors in a broad finance literature or on a materially important market, policy, or contracting problem? Would a generalist finance editor care even if the estimated effect is zero?
3. **Verified contribution** — Relative to the 3-5 closest papers, is the novelty real and nontrivial? Novelty must be in mechanism, question, identification, measurement, or implication, not just in setting, time period, or data access. "X but in country Y" or "X but with newer data" is not a contribution unless the setting variation generates a genuinely different economic prediction.
4. **Economic mechanism** — Is there a friction, incentive, or equilibrium force that generates a testable prediction? Can you name the channel and distinguish it from obvious alternatives?
5. **Convincing theory-to-evidence bridge** — Is there a persuasive inferential bridge from idea to evidence? This can be a quasi-experiment, field experiment, theory model, structural estimation, validated measurement exercise, sufficient-statistic approach, or out-of-sample asset-pricing test. Judge whether the bridge matches the question, not whether it looks like a standard causal design.
6. **Data, measurement, and replication feasibility** — Three sub-checks:
   - **Access:** Can the data realistically be obtained in time?
   - **Construct validity:** Does the empirical measure actually map to the mechanism? Would a skeptic accept it as a reasonable proxy?
   - **Replication feasibility:** Could the core result be documented and replicated under current top-journal data and code sharing policies?

## Scoring rubric

Rate each of the six dimensions 1-5:
- 5: Publication-grade strength — among the best you could imagine for this dimension
- 4: Strong — needs only minor refinement, no fundamental concern
- 3: Promising — needs significant work but a clear path exists
- 2: Weak — major gap that may or may not be fixable
- 1: Fatal — unlikely to be resolved

**Calibration guidance:**
- Default to 2 or 3 unless there is a strong, specific case for higher.
- Use 5 sparingly. A 5 means this dimension would survive the toughest referee in the field.
- Never rate an idea as top-3 Go if the only clear strength is data access or a clever shock.
- A paper that is 3 across the board is a plausible working paper or field-journal candidate, not a top generalist journal paper.

## Hierarchical gates (replaces the old decision rules)

After scoring, apply the gates in order. Each gate caps the verdict.

### Gate A — Displacement target

If Stage 1 found no concrete displacement target, maximum verdict is **Strong Field Go** regardless of all other scores.

### Gate B — Importance ≥ 4

Required for Top Generalist Go. If Importance < 4, maximum verdict is Strong Field Go.

### Gate C — Contribution ≥ 4 and Bridge ≥ 4

Required for Top Generalist Go. Either gate failing pulls the verdict down.

### Gate D — Archetype parity (see Stage 3 below)

If the candidate is below parity on all three accepted archetypes on all dimensions of breadth/cleanness/surprise, maximum verdict is Strong Field Go.

### Gate E — Desk-reject survival (see Stage 4 below)

If both Editor A and Editor B desk-reject letters are convincing, downgrade one tier from whatever the above gates allow.

### Verdicts (after all gates)

| Verdict | Gates required |
|---|---|
| **Top Generalist Go** | All gates A-E cleared |
| **Strong Field Go** | All dimensions ≥ 3, total ≥ 18, but one or more gates A-D failed |
| **Revise** | Total 15-20 with a clear path on the weak dimensions, or 1 gate failed with a fixable cause |
| **Kill / Pivot** | Importance < 3, contribution is mostly setting variation, the bridge cannot distinguish mechanisms, more than 3 essential hurdles, total ≤ 14, or any dimension = 1 |

### Revision-feasibility rule

After scoring, list the essential hurdles a referee would raise. Apply this filter:

- If more than **three essential hurdles** are needed to make the paper publishable, default to **Kill** or **Pivot** unless Importance = 5 and Contribution ≥ 4.
- Ask whether a plausible path to publication exists within **one R&R round, or at most two**. If not, the idea is not ready.

## Imaginary abstract test

Before running the full scoring workflow, write a 5-part imaginary abstract for the idea:

1. **Motivation/Tension:** What is the gap between what economists assume and what the world actually looks like? What prior would change?
2. **Empirical Setting and Data:** What is the ideal experiment or setting? What data would you use?
3. **Results:** What would you expect to find? Be specific about magnitudes if possible.
4. **Implications:** What does this mean for theory, practice, or policy?
5. **Conclusion:** One-sentence takeaway.

**Purpose:** The imaginary abstract forces coherence. If you cannot write a plausible 5-part abstract, the idea is not ready. Ideas that sound exciting as a sentence but collapse when spelled out are Type I errors waiting to happen.

**If the abstract feels impossible to write**, that is diagnostic: the idea lacks a clear question, a plausible test, or a meaningful result. Kill or revise.

## Stage 2: Closest-paper novelty test (existing four quick stress tests)

Apply these after scoring. Each should be answerable in one sentence.

1. **Null-result value test:** State the *specific finding, model, or claim* the null result would kill. Generic "we learn that X doesn't matter" answers fail this test.
2. **Simultaneous-discovery test:** If a similar working paper appeared on SSRN tomorrow, would this paper still deserve publication because it gives the cleanest, most credible, or most important answer? If not, speed-to-market is the only edge, which is fragile.
3. **Syllabus test:** Name one sentence in a *specific* PhD finance course (with course name and textbook chapter) that would have to change if the paper is right. If you cannot, the paper may not be first-order.
4. **Necessary-conditions test:** Name the one critical first-stage condition that must hold for the project to work. Can you check this condition with a few hours of work before committing months? Treat research like drug development: lab test before clinical trial.

## Stage 3: Archetype benchmarking

Pull anchors from the prebuilt indexes in `references/top_journal_calibration.json`. Look up the candidate's `mechanism`, `identification_style`, and `topic_area` in the `mechanism_index`, `identification_style_index`, and `topic_area_index` fields. Take the union of returned paper IDs, deduplicate, then split into accepted vs stalled by each paper's `outcome` field. Pick the 3 closest accepted analogs and 2 closest stalled analogs by mechanism overlap (read each paper's `mechanism` and `contribution_claim` fields).

This is a dictionary lookup, not a filter pass — no full scan of the calibration array.

If the indexes return fewer than 3 accepted analogs, supplement with a single Corbis call: `search_papers` filtered to JF/JFE/RFS (`minYear: <today - 24mo>`, `sortBy: "citedByCount"`, `matchCount: 10`, `compact: true`). Only one candidate is being screened in this skill, so parallelism is unnecessary here.

For each accepted analog, write one sentence on parity:

> "Candidate is [at parity / below / above] this archetype on [breadth / cleanness / surprise] because [...]"

For each stalled analog, write one sentence on differentiation:

> "Candidate differs from this stalled paper because [...]" — or, if it does *not* clearly differ, that becomes a kill reason.

**Apply Gate D:** If the candidate is below parity across all dimensions for all three accepted analogs, Importance is re-scored down by 1 (minimum 2) and the verdict caps at Strong Field Go. If the candidate fails to differentiate from at least one stalled analog, downgrade one tier.

If `references/top_journal_calibration.json` is missing, skip this stage and cap the verdict at Strong Field Go.

## Stage 4: Two-editor desk-reject simulation (parallel)

For every candidate that survived Stages 1-3 with a non-Kill scoring trajectory, write two desk-reject letters.

### Dispatch pattern

The two editors are independent. Dispatch them in parallel via the Agent tool: one subagent for Editor A, one for Editor B, sent in the same message. Each subagent gets the candidate idea, displacement target, mechanism, identification style, and the editor persona below. Wait for both subagents to return before applying the verdict logic.

### Editor A — empirical corporate / intermediaries editor

Simulate an editor whose taste runs to Welch, Murphy, or Schoar:

- Cares about: first-order question, institutional realism, identification, mechanism specificity.
- Skeptical of: cute shocks, clever-but-niche datasets, designs that look more memorable than the question.
- Voice: pragmatic, "tell me why this matters for how capital flows or how firms decide."

Write one paragraph stating the single most likely desk-reject reason from Editor A's POV. State the reason plainly. If Editor A would advance to referees, write "advances" with one sentence on why.

### Editor B — asset pricing / theory editor

Simulate an editor whose taste runs to Fama, Stambaugh, or Lewellen:

- Cares about: theoretical grounding, sign predictions, sufficient statistics, out-of-sample validation, model-empirics consistency.
- Skeptical of: empirical-only stories, mechanism claims without theory, ad hoc proxies, papers that don't restrict predictions across markets or states.
- Voice: theoretical, "what does this rule out, and against what model?"

Same format. One paragraph, or "advances" with a sentence.

**Apply Gate E:** Both letters convincing → downgrade one tier. One convincing, one weak → keep tier, flag the convincing letter as a must-address risk. Both weak → tier holds.

Save both letters to `output/desk_reject_letters.md` regardless of outcome.

## Kill criteria

Flag the idea as weak if one or more of these dominate:

- It is a minor setting variation with no new mechanism ("X but in country Y").
- The identification is decorative rather than essential — the result does not require the proposed design.
- The data are unavailable, too small, or too noisy for the claim.
- The contribution depends on saying "first" without verification.
- The likely result would be too local or too descriptive for the intended journal.
- The idea needs multiple heroic assumptions to work.
- The question has been answered convincingly and the proposed paper cannot improve on existing answers.
- The mechanism is a just-so story with no way to distinguish it from alternatives.
- **No concrete displacement target after honest effort.**
- **No clear differentiation from at least one stalled analog.**

## Screening workflow

1. **Stage 0:** Run the desk-editor screen (four questions). If weak, stop early.
2. **Stage 1:** Name the displacement target. If none, apply the cap.
3. Restate the idea in one sentence (question-first framing).
4. Write the imaginary abstract (5 parts). If you cannot write it, flag the idea as underdeveloped.
5. Identify the mechanism or friction.
6. Name the closest 3-5 papers (use `search_papers` to verify — do not guess).
7. State what is new relative to the closest papers — be specific about whether the novelty is in mechanism, data, identification, setting, or implication.
8. Sketch the theory-to-evidence bridge (quasi-experiment, model, structural, measurement, or asset-pricing test).
9. Assess data, measurement, and replication feasibility (use `search_datasets` if needed).
10. **Necessary-conditions check:** Name the one critical first-stage condition and whether it can be tested quickly.
11. Identify the likely journal track (finance generalist, finance specialist, or real-estate/housing).
12. List the 2-3 biggest fatal risks (these become the essential hurdles).
13. Apply the six-dimension scoring rubric.
14. Run the four stress tests (sharper versions per Stage 2 above).
15. **Stage 3:** Archetype benchmarking against accepted and stalled analogs.
16. **Stage 4:** Two-editor desk-reject simulation.
17. Apply the gates A-E in order to determine the verdict.
18. Apply the revision-feasibility rule (max 3 hurdles).
19. Deliver the verdict with the expanded Idea Card, including displacement target, archetypes, desk-reject letters, and gates cleared.

## Idea generation guidance

When asked to generate ideas (not just screen them):
- Start from frictions, not topics. Ask: what market failure, information asymmetry, behavioral bias, regulatory distortion, or institutional feature creates inefficiency?
- Look for natural experiments, policy changes, or data innovations that create new identification opportunities.
- Consider what new data sources have become available (satellite imagery, web scraping, administrative records, fintech platforms, text/NLP from filings, alternative workforce data).
- Think about which classic questions have become answerable with modern methods (ML, high-frequency data, granular geographic data, LLMs for text analysis).
- Always ask: is the question more important than the data? If the data is the star, the paper is likely second-order.

For full idea generation prefer `/brainstorm` (research-idea-generator), which applies the full eleven-lens taxonomy and is calibrated to enforce lens-source discipline on the top 3.

## Tool integration (Corbis MCP)

**Never claim an idea is novel without searching first.**

### Calibration anchor
- Read `references/top_journal_calibration.json` at start. Suggest `/calibrate-rubric` if missing.

### Check existing data, then architecture and frontier
0. If `output/paper_set.json` exists, read it. Papers already collected reduce redundant searching.
1. `search_papers` (query: the core question, `sortBy: "citedByCount"`, `matchCount: 15`) — papers that define this space. High-citation close papers are the biggest contribution threats.
2. `search_papers` (query: the core question, `minYear: 2020`, `matchCount: 15`) — recent frontier. Low-citation recent papers are scooping threats.

Save results to `output/paper_set.json` and append queries to `output/search_log.md`.

### Novelty verification chain (paper-set-first)

3. **Triage against paper_set first.** After Step 2's architecture and frontier searches, `output/paper_set.json` has ~30 papers in the area. Scan it for direct competitors to the specific idea. Classify:
   - **Paper set has 3+ plausible direct competitors.** Run `get_paper_details_batch` on those IDs (one call) to confirm overlap. No fresh search.
   - **Paper set has 1-2 plausible competitors.** Fire one supplemental `search_papers` (query: the specific idea phrased as a research question, `matchCount: 10`, `compact: true`) and combine with paper_set hits before reading details.
   - **Paper set has no plausible competitors.** Fire the full search: `search_papers` (query: the idea phrased as a research question, `matchCount: 15`, `compact: true`).
4. `get_paper_details_batch` (paper IDs from top 3-5 closest, whether from paper_set or fresh search) — read abstracts to confirm whether they truly overlap or just share vocabulary.
5. `top_cited_articles` (journalNames: JF/JFE/RFS, query: specific topic) — identify seminal papers. Skip if paper_set already contains 5+ papers with `citedByCount > 500` in the area.

### Citation-aware threat assessment
- **High-citation close paper (500+)**: Contribution threat. Differentiate on mechanism, identification, or setting with different economics.
- **Medium-citation close paper (100-499)**: Active conversation. Advance beyond this work.
- **Low-citation recent paper (<100, post-2020)**: Scooping threat. A recent paper doing nearly the same thing is more dangerous than a classic paper.

### Archetype benchmarking (Stage 3)
- Filter the local calibration set first.
- Supplement: `search_papers` filtered to JF/JFE/RFS (`minYear: <today - 24mo>`, `sortBy: "citedByCount"`, `matchCount: 10`) — recent accepted analogs for this mechanism class.
- `top_cited_articles` with `journalNames: ["Journal of Finance","Journal of Financial Economics","Review of Financial Studies"]` and the candidate's topic — seminal landmarks.

### Data feasibility
- `search_datasets` (topic keywords) — discover available datasets and their coverage.
- `fred_search` (keywords like "commercial real estate" or "bank lending") — find relevant FRED macro series for context or controls.

### For real-estate ideas specifically
- `get_market_data` (metro name) — current CRE fundamentals to assess whether the phenomenon is economically relevant now.
- `search_markets` (criteria) — find markets with the characteristics needed for the natural experiment.

### After screening
- `export_citations` (format: `bibtex`) — export BibTeX for the 3-5 closest papers and the 3 accepted archetypes.
- `format_citation` — format individual references for inclusion in notes or memos.

## Preferred outputs

Produce one Idea Card using `assets/idea-card-template.md`, plus:

- **Displacement target** (one sentence)
- **Accepted archetypes** (3 papers from calibration set with parity verdict)
- **Stalled analogs** (2 papers with differentiation claim)
- **Two-editor desk-reject letters** (verbatim)
- **Gates cleared / failed** (checklist)
- A one-sentence contribution claim
- A one-sentence skepticism test from a referee's point of view
- A scoring rubric result (six dimensions)
- A Go / Revise / Kill verdict with specific reasoning
- The four stress-test answers (sharpened per Stage 2)
- The killer exhibit description

## Journal-fit logic

**Top generalist ideas** must change how the field thinks about something *and* clear the calibration-anchored gates. They require a first-order question with a convincing bridge from theory to evidence, plus parity against recent accepted archetypes and survival against both editor desk-rejects.

Strong field journals are slightly more receptive to careful empirical work on narrower or cross-disciplinary questions. The gates that fail (typically Importance or displacement target) point the user at where the idea is undersized relative to top-3 ambition.

When assessing journal fit, the accepted archetypes from the calibration set serve as the explicit comparison. If no recent archetype exists in the candidate's mechanism class, the fit may be weak — note this on the Idea Card.

## Guardrails

- Never confuse an interesting topic with a publishable question.
- Do not overpraise novelty. If the search reveals close papers, say so.
- If the user gives several ideas, rank them using the scoring rubric and apply the gates to each.
- Prefer fewer, stronger claims over many diffuse ones.
- Do not let enthusiasm for a topic substitute for identification feasibility.
- Do not let enthusiasm for a dataset or shock substitute for question importance.
- Score importance and contribution honestly. Most ideas are 2-3 on these dimensions, not 4-5.
- **No displacement target → no Top Generalist verdict.** This is the single hardest gate.
- **No calibration set → no Top Generalist verdict.** Suggest `/calibrate-rubric` and proceed under the cap.
- **Always check `output/paper_set.json` before firing a fresh `search_papers` call.** The architecture and frontier searches in Step 2 usually populate enough of the closest-paper space that the novelty verification chain in Step 3 collapses to a batch-detail call.
- **Use `compact: true` on every `search_papers` call** except when the search is explicitly for detail (then use `get_paper_details_batch` instead).

## Output format

Use the template in `assets/idea-card-template.md`. Add a section for displacement target, archetype benchmarking, and the two desk-reject letters even if the template does not yet have those slots — the skill output is authoritative.

## Next steps to suggest

At the end of the screen, explicitly tell the user what to do next based on the verdict:

1. **Top Generalist Go**: "Strong verdict. Next, run `/lit-search <idea>` to deepen the related-literature positioning before drafting the contribution paragraph. After that, consider `/data-plan` (if available in your skill set) or start the data construction. Log this screening conversation with `/log-conversation`."
2. **Strong Field Go**: "Solid verdict but capped below top-3. The gate(s) that failed tell you where to push — typically Importance or displacement target. Options: (a) tighten the framing to clear the failed gate and re-run `/idea`, (b) accept the strong-field target and run `/lit-search` to position, or (c) run `/brainstorm` in the same topic area to find a sharper variant."
3. **Revise**: "The idea has substance but at least one essential hurdle. Address the specific gate that failed (often Bridge or Contribution), then re-run `/idea`. If the failed gate is structural (e.g., no clean identification possible), pivot via `/brainstorm` rather than iterating."
4. **Kill / Pivot**: "The idea does not survive screening. Run `/brainstorm <topic area>` to generate alternatives in the same space, or `/lit-review <topic>` first if you want a deeper map before regenerating ideas."
5. **Always remind**: "Log this screening conversation with `/log-conversation` and the time spent reviewing the verdict with `/log-human-time`."

## Example prompts
- "Give me three corporate-finance ideas using private-credit data."
- "Is this housing-supply idea strong enough for a top real-estate journal?"
- "Turn this empirical asset-pricing anomaly into a better paper idea."
- "I have access to fintech lending data — what could I do with it?"
