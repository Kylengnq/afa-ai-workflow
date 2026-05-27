---
name: research-idea-generator
description: "Generate novel research ideas in finance and real estate using structured heuristic lenses, then gate top-tier labels against a held-out calibration set, displacement targets, lens-source discipline, archetype benchmarking, and an adversarial two-editor desk-reject simulation. Produces a curated Idea Menu of survivors, not a brainstorming list."
---

# Research Idea Generator

Generate a broad set of candidate research ideas, kill the weak ones internally, and present only the survivors. This skill is a generator with a built-in filter calibrated against actual top-3 finance journal outcomes. The user sees 10 ranked ideas; the model generates 25-30 and discards the rest.

## The vector-space principle

A good research idea is an arrow from the current literature toward reality. The larger the gap between what economists assume and how the world actually works, the more impactful the idea.

Three idea-source strategies, ranked by effectiveness:

1. **Starting from practitioner reality** (strongest): Real-world observations reveal where reality diverges from what economists assume. These observations mark where reality is, letting you draw the arrow from literature to reality.

2. **Starting from a cool dataset** (risky): A dataset generates many possible directions but no "hook" connecting to a specific literature-reality gap. Without a question, tinkering with data is unproductive. A dataset is a tool, not an idea.

3. **Starting from the literature** (weakest for generation): Reading papers and looking for extensions typically produces marginal additions. Literature knowledge is essential for positioning an idea, but is a poor source of ideas.

## Calibration anchor

Before scoring any candidate, read `references/top_journal_calibration.json` if it exists. This file is built by the `calibrate-rubric` skill and contains ~20 recent JF/JFE/RFS acceptances and ~20 stalled working-paper analogs, with each anchored by its question, mechanism, identification style, generating lens, and displacement target.

The calibration set is the external anchor for the "Top Generalist Go" label. Without it, the skill falls back to internal scoring only and cannot issue Top Generalist labels — it caps at Strong Field Go and warns the user.

If the file is missing, before continuing, suggest running `/calibrate-rubric` to build it. If the user declines, proceed under the cap.

## Phase 0: Collect user constraints

Before generating anything, collect and record these as **hard filters** on ranking. An idea that violates a hard constraint cannot rank in the top 5 regardless of its intellectual appeal.

| Constraint | Question to ask | How it binds |
|---|---|---|
| Data access | What databases, proprietary data, or institutional access do you have? | Ideas requiring unavailable data are capped at Medium feasibility |
| Methods comfort | What empirical methods are you comfortable executing? (DiD, RDD, structural, NLP, etc.) | Ideas requiring unfamiliar methods are downranked unless a coauthor fills the gap |
| Field comfort | What literatures do you know well enough to position a paper? | Ideas in unfamiliar fields require more literature work |
| Journal ambition | Are you targeting a top generalist journal, a strong field journal, or any good outlet? | Determines contribution bar |
| Coauthor skills | What complementary skills does a coauthor bring? | Relaxes method or field constraints |
| Timeline | How soon do you need a working paper? | Long-horizon structural projects vs. quick empirical exercises |

If the user provides a topic and constraints in their initial message, proceed without asking. Fill defaults for anything not specified (assume broad data access, standard empirical methods, strong field-journal ambition, solo researcher, 12-month timeline).

## Phase 1: Map the landscape

**Check for existing data first:** If `output/paper_set.json` exists, read it. If it contains papers relevant to the user's topic, use them as the starting point and supplement with targeted searches for gaps. This avoids redundant searching when the user has already run `/lit-review` or `/lit-search`.

Always open with the two-search pattern, then supplement:

1. **Architecture search**: `search_papers` (broad topic, `sortBy: "citedByCount"`, `matchCount: 15`) — immediately see which papers define this field and its citation hierarchy.
2. **Frontier search**: `search_papers` (same topic, `minYear: 2020`, `matchCount: 15`) — what's happening now, who is active, what's the edge.
3. **Survey search**: `search_papers` (topic + "survey" or "review", `matchCount: 10`) — find survey papers that map open questions.

Use `get_paper_details_batch` on the top 5-10 results from the architecture search to read abstracts and understand what has been established.

Produce a 3-4 sentence internal landscape summary: what is settled, what is actively debated, where the frontier is moving. Use relative citation tiering (top 10% = foundational, next 30% = established, bottom 60% = emerging).

**Save to shared files:** Write all collected papers to `output/paper_set.json` (merge if exists). Append search queries to `output/search_log.md`.

## Phase 2: Generate candidates (internal, not shown to user)

Apply all eleven lenses to the topic area. Generate 2-3 rough candidates per lens. Target 25-30 total candidates. Most will be discarded.

### Stage A: Generative lenses (reality-first)

These lenses produce the raw material. Apply these first. **For top-tier labeling, these lenses are weighted heavier — see Phase 7.**

**Lens 1: Practitioner-reality gap**

Start from how real actors behave, and ask whether this conflicts with what economists assume. Use these specific elicitation prompts:

- What do practitioners optimize that theory says they should not?
- What variable do practitioners obsess over that papers ignore?
- What decision rule do people use in practice that would look irrational in a model?
- What do industry participants know that academics have not documented?

Search with `search_papers` for "[topic] survey evidence" or "[topic] practitioner" to find papers documenting real-world behavior. If the user provided anecdotes, use those as the starting point.

The test: can you name a specific assumption in the literature that conflicts with observed behavior? If yes, the idea is well-formed. If not, the observation is interesting but not yet an idea.

**Lens 2: Cross-pollination**

Borrow a well-established concept, method, or finding from a neighboring field (labor, IO, macro, behavioral, urban, computer science) and apply it where it has not been used. The imported concept must generate a genuinely different economic prediction in the new setting, not just "X but in field Y."

**Lens 3: First principles / economic logic**

Start from a fundamental friction (information asymmetry, moral hazard, search costs, limited attention, regulatory distortion, market segmentation) and derive a testable prediction. Then check whether anyone has tested it. The best first-principles ideas feel obvious in retrospect.

**Lens 4: Unification**

Multiple individually documented findings are manifestations of the same underlying economic force. The synthesis is the paper. List 3-5 well-known findings and ask: is there a single mechanism that explains all of them? The unification must generate a new testable prediction.

**Lens 5: Policy / regulatory shock**

A recent policy change creates a natural experiment. The policy is the instrument, not the contribution. The question must be bigger than the policy. Search for recent (past 3-5 years) shocks relevant to the topic.

### Stage B: Refinement lenses (literature-positioned)

These lenses sharpen, reframe, or find angles on existing knowledge. Apply these second, using the landscape from Phase 1.

**Lens 6: Literature gap**

Find questions that survey papers flag as open. The gap must be economically meaningful, not just "nobody has run this regression." Caution: literature-driven ideas tend to produce marginal extensions. This lens should sharpen, not source.

**Lens 7: Conflicting findings**

Two credible papers reach opposite conclusions. The reconciliation is the idea. The moderating variable or identification flaw that explains the conflict becomes the contribution.

**Lens 8: Mechanism decomposition**

Take an established result and ask: what is the economic channel? Can you distinguish competing mechanisms? Many highly cited papers document effects without pinning down why. Include the measurement-error angle: does a canonical variable mismeasure the intended concept in a systematic way that changes interpretation? (Example: the literature thinks it measures financial constraint, but the proxy is contaminated by firm quality.)

**Lens 9: Boundary conditions and equilibrium displacement**

When does a canonical finding break down? The failure must map to a theory. Include the equilibrium-displacement angle: if agents adapt to the original finding, who absorbs the incidence or where does the effect move? In household finance, asset pricing, and real estate, strategic adjustment often produces deeper questions than simple treatment-effect framing.

**Lens 10: New data x old question**

Pair a recently available data source with a classic question. The data must enable a genuinely better answer through new identification, new measurement, or a new population, not just a new time period or higher frequency.

**Hard constraint on this lens:** Ideas from Lens 10 are **capped at strong-field tier**. They can never rank top-generalist regardless of composite score. The only exception is when the new data fundamentally rewrites measurement (e.g., the first reliable measure of a previously unobservable quantity), in which case the idea should be re-classified under Lens 3 (first principles) or Lens 8 (measurement angle).

**Lens 11: Model meets data**

Theoretical models make quantitative predictions that have not been tested. The paper tests the prediction. What would rejection mean for the theory?

## Phase 3: Three-part novelty test (paper-set-first, then parallel)

For every candidate idea, answer three questions:

1. **Closest existing paper**: Name the single closest paper.
2. **Not relabeling**: In one sentence, state why this idea is not a relabeling of that paper. What is structurally different: mechanism, prediction, identification, or setting with different economics?
3. **New prediction**: State the one prediction or finding this paper would produce that the closest paper does not.

**Do not fire a fresh Corbis search per candidate.** Phase 1 already built `output/paper_set.json` with 30-40 papers from the topic area; that set usually resolves novelty for most candidates without new API calls. Only candidates the existing set cannot answer get a fresh search, and those run in parallel.

### Step 3a — Triage against the existing paper set (internal, no API calls)

For each candidate, scan `output/paper_set.json` and classify:

- **Bucket A — clear close match in the set.** A paper in the set directly addresses the candidate's question. Answer the three novelty questions immediately from the existing paper. No fresh search.
- **Bucket B — adjacent papers in the set, novelty unclear.** Existing papers are nearby but cannot definitively settle whether the candidate is novel. Queue for fresh search.
- **Bucket C — no nearby papers in the set.** Either Phase 1 missed this corner, or the area is genuinely under-explored. Queue for fresh search.

Typical mix: 50-70% of candidates land in Bucket A and resolve without new calls. The remainder go to Step 3b.

### Step 3b — Parallel novelty searches for queued candidates

Dispatch parallel subagents via the Agent tool, one per queued candidate, in batches of up to 10 per message. Each subagent prompt contains:

- The candidate idea phrased as a research question (one sentence).
- A summary of the paper_set context: top 5 most-cited papers in the area with one-line gloss each.
- Instructions to run `search_papers` (`matchCount: 10`, `compact: true`) on the specific candidate, then `get_paper_details_batch` on the top 3 results.
- The expected return shape (see below).

Each subagent returns a structured verdict:

```
closest_paper_id: <Corbis ID>
closest_paper_one_liner: <author, year, finding>
is_relabeling: <bool>
new_prediction: <one sentence>
keep: <bool>
reason: <one sentence>
```

Wait for all subagents in a batch to return before proceeding.

### Step 3c — Aggregate, merge paper set, log

Combine Bucket A judgments (made internally) with the subagent verdicts. Add any newly surfaced papers to `output/paper_set.json` (merge, dedupe by `id`). Append the search queries to `output/search_log.md`.

**If a candidate cannot pass all three novelty questions, it is discarded.** Do not proceed to the kill test for discarded candidates.

Expected cost under this design: 5-12 fresh Corbis searches (one per Bucket B/C candidate), not 25-30. A run with a well-populated paper_set from Phase 1 may need only 3-5 fresh searches.

## Phase 4: Internal kill test (not shown to user)

For each candidate that survives the novelty test, answer three questions:

1. **Already done?** What search result or combination of papers might already cover this? What would you find if you searched harder?
2. **Identification failure?** What is the most likely reason the causal design fails? (Endogeneity, measurement error, insufficient power, parallel trends violation, weak instrument.)
3. **Seminar indifference?** Why might a skeptical seminar audience shrug? Is the question first-order, or is it a niche exercise that only the authors care about?

**Decision rule:**
- Fails 0 of 3: strong survivor, proceed
- Fails 1 of 3: proceed with the failure noted as a risk
- Fails 2 of 3: discard
- Fails 3 of 3: discard

## Phase 5: Score, displacement gate, archetype benchmarking

For each surviving candidate (~10-15), do three things in order: name the displacement target, score the three dimensions, then benchmark against the calibration set.

### Step 5a — Displacement target (hard gate)

For each candidate, name in one sentence the specific paper, model, textbook claim, or empirical regularity this idea would displace if it is right. Use the prompt template:

> "If this paper is accepted, what gets struck out of next year's PhD finance reading list, or which claim in a canonical model becomes wrong?"

The answer must name something concrete: a paper (with author, year), a model (e.g., "the Diamond-Dybvig assumption that all withdrawals are equally informative"), or an empirical regularity (e.g., "the documented Monday effect in stock returns").

**Hard gate:** If the model cannot name a concrete displacement target, **Importance is capped at 3** for this candidate. The candidate cannot rank above Strong Field tier regardless of the other scores. Vague displacement claims ("it would change how we think about X") do not count and trigger the cap.

### Step 5b — Score on three dimensions

For each surviving candidate, score on three dimensions:

| Dimension | 1 (Low) | 3 (Medium) | 5 (High) | One-line justification required |
|---|---|---|---|---|
| **Novelty** | Close paper exists, marginal extension | Adjacent work but distinct angle | No close paper, new prediction | Yes |
| **Importance** | Niche, small audience | Active field, moderate audience | First-order question, broad audience | Yes |
| **Executability** | Data unavailable or method beyond reach | Feasible but requires significant investment | Data in hand, method familiar | Yes |

**Composite score** = Novelty + Importance + Executability (max 15). Rank by composite. Break ties in favor of reality-first lenses.

**Apply user constraints as hard filters:**
- If data access is insufficient and no workaround exists: cap Executability at 2
- If method is unfamiliar and no coauthor fills the gap: cap Executability at 3
- If journal ambition is top generalist but Importance < 4: flag as "field-journal tier"

### Step 5c — Archetype benchmarking (only for candidates with composite ≥ 12)

For each candidate scoring high enough to plausibly be top-tier, pull anchors from the prebuilt indexes in `references/top_journal_calibration.json`:

1. Use the `mechanism_index`, `topic_area_index`, and `identification_style_index` built by `/calibrate-rubric`. For the candidate, look up its mechanism, topic area, and identification style as keys. Take the union of paper IDs returned, deduplicate, then split into accepted vs stalled by each paper's `outcome` field. This is a dictionary lookup, not a filter pass — no per-candidate iteration over the whole calibration array.
2. From the unioned set, pick the 3 closest accepted analogs and 2 closest stalled analogs by mechanism overlap (read the `mechanism` and `contribution_claim` fields and judge closeness).
3. If the indexes return fewer than 3 accepted analogs, batch the candidates that need supplements and dispatch them in parallel via the Agent tool, one subagent per candidate. Each subagent runs `search_papers` filtered to JF/JFE/RFS (`minYear: <today - 24mo>`, `sortBy: "citedByCount"`, `matchCount: 10`, `compact: true`) on the candidate's mechanism + identification, returns the top 3 IDs and one-line glosses. Wait for the batch to complete before proceeding.

For each accepted analog, write one sentence on the candidate's parity:

> "Candidate is [at parity / below / above] this archetype on [breadth / cleanness / surprise] because [...]"

For each stalled analog, write one sentence on the candidate's differentiation:

> "Candidate differs from this stalled paper because [...]" — or, if the candidate does *not* clearly differ, that becomes a kill reason.

**Hard gate:** If the candidate is below parity on *all* three accepted analogs on *all* three of breadth/cleanness/surprise, **Importance is re-scored down by 1** (minimum 2). If the candidate fails to differentiate from at least one stalled analog, **the candidate is downgraded one tier** in Phase 7.

If `references/top_journal_calibration.json` is missing, skip this step but cap the verdict at Strong Field Go in Phase 7 and emit a warning.

Select the top 10 by post-gate composite for the Idea Menu.

## Phase 6: Two-editor desk-reject simulation (parallel)

For every candidate that survived Phase 5 with composite ≥ 12 *and* a named displacement target *and* archetype parity (or no calibration set), write two desk-reject letters.

### Dispatch pattern

The two editors are independent and the letters are short. Dispatch them in parallel via the Agent tool: one subagent for Editor A, one for Editor B, sent in the same message. Across multiple candidates, batch the dispatch — e.g., 5 candidates × 2 editors = 10 subagents in one message. Each subagent gets the candidate idea, displacement target, mechanism, identification, the editor persona below, and the expected one-paragraph return format.

Wait for all subagents in a batch to return before applying the verdict logic at the end of this phase.

### Editor A — empirical corporate / intermediaries editor

Simulate an editor whose taste runs to questions like Welch, Murphy, or Schoar:

- Cares about: first-order question, institutional realism, identification, mechanism specificity.
- Skeptical of: cute shocks, clever-but-niche datasets, designs that look more memorable than the question.
- Voice: pragmatic, "tell me why this matters for how capital flows or how firms decide."

Write one paragraph stating the single most likely desk-reject reason from Editor A's POV. State the reason plainly. If Editor A would in fact advance the paper to referees, write "advances" and one sentence on why.

### Editor B — asset pricing / theory editor

Simulate an editor whose taste runs to questions like Fama, Stambaugh, or Lewellen:

- Cares about: theoretical grounding, sign predictions, sufficient statistics, out-of-sample validation, model-empirics consistency.
- Skeptical of: empirical-only stories, mechanism claims without theory, ad hoc proxies, papers that don't restrict predictions across markets or states.
- Voice: theoretical, "what does this rule out, and against what model?"

Same format. One paragraph, or "advances" with a sentence.

### Verdict from the simulation

- **Both letters convincing**: downgrade the candidate one tier (top-generalist → strong-field). Log both letters.
- **One convincing, one weak**: flag for revision. Attach the convincing letter as a "must-address" risk. Tier holds.
- **Both weak**: candidate clears the desk-reject gate. Tier holds.

Save the letters to `output/desk_reject_letters.md` for every candidate that was simulated (not just survivors).

## Phase 7: Assign tier with hierarchical gates and lens-source discipline

For each surviving candidate, apply gates in order. Failing any gate caps the tier.

### Gate 1 — Importance ≥ 4

Required for Top Generalist. If Importance < 4 (either originally or after the archetype downgrade), maximum tier is Strong Field.

### Gate 2 — Contribution and Bridge ≥ 4

Required for Top Generalist. The candidate must score ≥ 4 on Novelty *and* have a Bridge (theory-to-evidence) the model would describe as ≥ 4. (If Bridge was not separately scored, simulate it now: "would a strong referee accept the proposed inferential bridge?" yes = 4, with hesitation = 3.)

### Gate 3 — Displacement target named

If Importance was capped at 3 in Phase 5 for lack of a displacement target, maximum tier is Strong Field.

### Gate 4 — Archetype parity

If the candidate failed Phase 5c parity (below parity on all dimensions of all accepted analogs), maximum tier is Strong Field.

### Gate 5 — Desk-reject survival

If both Editor A and Editor B desk-reject letters were convincing, downgrade one tier from whatever the above gates allow.

### Gate 6 — Lens-source discipline (applies to ranked positions, not gates)

After gating, rank candidates. Then enforce: **at least 2 of the top 3 ranked positions must come from Lens 1 (practitioner gap), Lens 3 (first principles), or Lens 4 (unification).**

If the top 3 violate this rule (e.g., all three are Lens 6 literature-gap ideas), reshuffle:

- Find the highest-ranked surviving Lens-1/3/4 candidate.
- Promote it into the top 3, displacing the lowest of the existing top 3.
- Repeat if the rule still isn't satisfied.

**Lens 10 candidates are hard-capped at Strong Field tier per Phase 2 (Stage A note).** They can rank top-10 but not top-3 under top-generalist labeling, and they cannot receive the Top Generalist tier even if all other gates are satisfied.

### Final tier definitions

| Tier | Description | Gates required |
|---|---|---|
| **Top Generalist** | Broad mechanism, general implications, strong identification, displaces a concrete target | All gates 1-5 cleared; not Lens 10 |
| **Strong Field** | Clean question within an active literature, solid design | At least Importance ≥ 3, Contribution ≥ 3, Bridge ≥ 3 |
| **Workshop** | Feasible and interesting but narrower scope | Falls below Strong Field gates |

Be honest. Most ideas are Strong Field tier. Labeling everything as top-generalist is the failure mode this skill exists to prevent.

## Phase 8: Produce the Idea Menu

Use `assets/idea-menu-template.md`. Present all 10 surviving ideas plus a "Graveyard" section showing 3 rejected ideas with reasons. The graveyard teaches the user how the filter works and what makes ideas fail in this topic area.

Present all 10 ideas with:
- Rank
- One-sentence question (question-first, never "Using X data...")
- Lens that generated it
- **Displacement target** (one sentence)
- Closest paper (from novelty test)
- **Accepted archetypes** (3 papers from calibration set, with parity verdict)
- **Stalled analogs** (2 papers, with differentiation claim)
- Novelty / Importance / Executability scores
- **Desk-reject summary** (Editor A and B verdicts, one line each)
- **Gates cleared** (checklist)
- Contribution tier
- Key risk (from kill test)

For the Graveyard section, list each killed idea with the gate that killed it (e.g., "killed at Gate 1: no displacement target; killed at Gate 4: below parity on all accepted analogs; killed at Gate 5: both editors desk-rejected").

## Phase 9: Expand top 3 into Idea Sketches

For the three highest-ranked ideas, provide an Idea Sketch with:

**One-sentence question**

**Seminar pitch**: "This paper shows that ___ because ___." One sentence that states the real contribution. If you cannot write this sentence, the idea is not formed.

**Displacement target** (verbatim from Phase 5a)

**Core mechanism or friction** (2-3 sentences): Name the economic force. State the testable prediction.

**Question / Mechanism / Prediction / Identification / Data / Why now**: Structure these explicitly as six labeled items. If any one is weak, acknowledge it.

**Theory-to-evidence bridge** (one paragraph): What is the test? What variation is exploited? What would the ideal table or figure show?

**Key data requirements**: Specific datasets, access, coverage.

**Archetype anchors**: Three accepted papers from the calibration set the user should read before committing. One sentence per anchor on what to learn from it.

**Stalled lessons**: Two stalled analogs and what specifically the user must do to avoid each one's fate.

**Contribution tier and gates cleared**: Top Generalist / Strong Field / Workshop, with the gate checklist.

**Editor A and B desk-reject letters**: Verbatim from Phase 6.

**Referee vulnerability**: "The hardest challenge is whether ___ is just proxying for ___." One sentence stating the toughest objection.

**Why this idea beats the other top candidates**: One sentence on why this ranks above the alternatives.

**Why this idea is not dominated by a cleaner adjacent project**: One sentence.

## Phase 10: Recommend next steps

Suggest running `/idea` on the most promising candidate for full screening. Note any ideas that would benefit from `/lit-search` to deepen positioning, or `/lit-landscape` to visualize the field structure. If the calibration set is more than 6 months old, suggest refreshing with `/calibrate-rubric`.

Append a dated entry to `notes/lab_notebook.md`: topic, number of candidates generated, number that cleared each gate, top 3 with tiers.

## Tool integration (Corbis MCP)

**Never claim an idea is novel without searching first.**

### Calibration anchor (Phase 0, before Phase 5)
- Read `references/top_journal_calibration.json`. If missing, suggest `/calibrate-rubric` before proceeding.

### Landscape mapping (Phase 1)
1. `search_papers` (broad topic, `matchCount: 15`) — current state
2. `search_papers` (topic, `minYear: 2020`, `matchCount: 15`) — frontier
3. `search_papers` (topic + "survey", `matchCount: 10`) — survey papers
4. `get_paper_details_batch` (top 5-10 paper IDs in one call) — read abstracts, get citation counts

### Per-candidate novelty checks (Phase 3)
- **Default: no fresh searches.** Read `output/paper_set.json` (built in Phase 1) and triage candidates into Buckets A/B/C. Bucket A resolves internally with zero API calls.
- For Bucket B and C only: dispatch parallel subagents (Agent tool, batches of 10). Each subagent runs `search_papers` (the specific candidate idea, `matchCount: 10`, `compact: true`) and `get_paper_details_batch` on top 3 results, returning a structured verdict.
- Expected fresh-search volume: 5-12 calls per run, not 25-30.

### Archetype benchmarking (Phase 5c)
- **Default: dictionary lookup on the calibration indexes.** No API calls for candidates whose mechanism/topic/identification are already covered.
- Supplement only when fewer than 3 accepted analogs are returned. Supplements dispatch in parallel (one subagent per candidate needing one).
- Each supplement subagent: `search_papers` filtered to JF/JFE/RFS (`minYear: <today - 24mo>`, `sortBy: "citedByCount"`, `matchCount: 10`, `compact: true`).

### Data feasibility
- `search_datasets` (topic keywords) — discover available datasets
- `fred_search` (keywords) — find relevant macro series

### After generation
- `export_citations` (format: `bibtex`) — export BibTeX for closest papers identified during generation

## Guardrails

These are hard bans. Ideas that violate these rules are discarded regardless of their score.

- **No displacement target, no top tier.** Ideas without a named, concrete displacement target are capped at Strong Field. This is the single hardest gate.
- **Ban "X but in country Y"** unless the new setting generates a genuinely different economic prediction.
- **Ban context-only contributions** where the only novelty is applying a known result to a new industry, time period, or population without new economics.
- **Ban ideas whose identifying variation is more memorable than the question.** If the shock is cleverer than what it identifies, the idea is backwards.
- **Ban pure heterogeneity mining** unless tied to a theory-derived margin that generates a distinct prediction. "The effect is stronger for constrained firms" is not a paper unless you explain why and what it rules out.
- **Ban ideas that cannot be explained to a seminar audience in two sentences.** If the contribution requires a paragraph of caveats to state, it is not a contribution.
- **Do not let a clever dataset or natural experiment substitute for a question.** The question must come first; the design serves the question.
- **Do not generate more than 2 ideas from the same lens.** Breadth of attack across heuristics is the value of this skill.
- **Do not present 10 equally enthusiastic ideas.** Rank honestly. Assign tiers honestly. Some ideas are workshop-tier. Say so.
- **Do not overclaim novelty.** If the search reveals a close paper, note it and adjust or drop the idea.
- **At least 2 of the top 3 must come from Lens 1, 3, or 4.** Enforced by Gate 6.
- **Lens 10 candidates are capped at Strong Field.** No exceptions short of reclassification under Lens 3 or 8.
- **An "interesting relationship" is NOT a research idea.** The idea must have a testable tension between theory and reality, not just a correlation to document.
- **If the calibration set is missing, no Top Generalist labels.** Cap at Strong Field and tell the user.
- **Do not fire one Corbis search per candidate in Phase 3.** Always triage against `output/paper_set.json` first. Only Bucket B and C candidates get fresh searches, and those dispatch in parallel.
- **Use `compact: true` on every Phase 3 and Phase 5c supplement search.** Saves ~80% of payload bytes.

## Preferred outputs

Produce:
1. **Idea Menu** — 10 ranked survivors using `assets/idea-menu-template.md`, with the new fields (displacement target, archetypes, desk-reject summary, gates cleared)
2. **Idea Sketches** — expanded treatment of the top 3
3. **Desk-reject letter archive** — `output/desk_reject_letters.md` with both editors' letters for every simulated candidate
4. **Next-step recommendation** — which idea to screen first and why

## Example prompts

- "Brainstorm 10 ideas in behavioral asset pricing."
- "Generate research ideas about climate risk and real estate."
- "I have access to Revelio Labs workforce data — brainstorm ideas in corporate finance."
- "Help me come up with ideas at the intersection of fintech and household finance."
- "Brainstorm ideas about intermediary asset pricing and credit markets."
- "Generate ideas in empirical corporate governance using NLP/LLM methods."
