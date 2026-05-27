# Skills Guide

How to use the eleven workflows in this AFA 2027 submission template. In Claude
Code, they are available as slash commands. In Codex, Cursor, and other MCP
clients, use the same workflow names and examples below as prompt templates.

## Which skill to use

### AFA submission skills

| I want to... | Skill / Command |
|---|---|
| Set up the AFA submission package on day one | `/init-submission` |
| Capture a verbatim AI conversation transcript | `/log-conversation` |
| Log a block of direct human work | `/log-human-time` |
| Recompute the human-vs-AI contribution tally | `/contribution-report` |

### Calibration

| I want to... | Skill / Command |
|---|---|
| Build the top-3 journal anchor for idea screening | `/calibrate-rubric` |
| Refresh the anchor (every ~6 months) | `/calibrate-rubric` |

### Research skills

| I want to... | Skill / Command |
|---|---|
| Survey what a field knows about a topic | `/lit-review` |
| Find the closest papers to my idea and sharpen the contribution | `/lit-search` |
| Generate research ideas in a topic area | `/brainstorm` |
| Evaluate whether a specific idea is worth pursuing | `/idea` |
| Check that my citations are correct and complete | `/verify-citations` |
| Visualize trends, gaps, and methods in a literature | `/lit-landscape` |

## First-time setup

The skills depend on each other. Run them in this order on day one:

```text
1. /init-submission         # captures the initial prompt + model config under submission/
2. /calibrate-rubric        # builds the top-3 journal calibration anchor (~5-10 min, one-time)
3. /brainstorm <topic>      # or /idea <specific question> if you already have one
```

`/calibrate-rubric` is the step most people miss. Without it, `/brainstorm` and `/idea` still run, but they cap the verdict at Strong Field Go — they cannot certify an idea against the top-3 journal frontier.

Do not run `/init-submission` for a real project before 2026-06-01. The AFA
call requires the investigation to begin on or after that date with the initial
AI prompt. The local call checklist is
`submission/call_requirements.md`.

## The submission workflow (run continuously)

These run throughout the project, not as a one-time setup:

```text
After every AI conversation     -> /log-conversation
After every block of human work -> /log-human-time
At submission time              -> /contribution-report
```

Pair them with the research skills, not in place of them.

## Common research workflows

**Starting from a vague topic:**
1. `/lit-review [your topic]` — understand the field
2. `/brainstorm [your topic]` — generate 10 ranked ideas with gate verdicts
3. `/idea [best candidate from brainstorm]` — screen the chosen idea rigorously

**Starting with a specific question:**
1. `/lit-search [your paper's question]` — find closest work
2. `/idea [your idea]` — score and stress-test it against the calibration set

**Visualizing a literature:**
1. `/lit-review [your topic]` — build the paper set
2. `/lit-landscape [your topic]` — generate trend and gap figures

**Polishing citations:**
1. `/verify-citations` — audit your `.bib` against Corbis

**Reading a paper:**

If your assistant supports repo-defined agents, use the paper-reader prompt:
> "Read and summarize the paper at ~/Downloads/fama_french_1993.pdf"

## Key concepts you'll see in the output

`/brainstorm` and `/idea` use terms that aren't standard finance vocabulary:

- **Displacement target.** The specific paper, model claim, or empirical regularity an idea would render wrong. Ideas without a concrete target cap at Strong Field. Example: *"This would displace Krishnamurthy & Vissing-Jørgensen's (2012) claim about liquidity premia."*

- **Calibration set.** `references/top_journal_calibration.json`, built by `/calibrate-rubric`. ~20 recent JF/JFE/RFS acceptances and ~20 stalled SSRN analogs, each tagged with question, mechanism, identification style, and displacement target. The external anchor for tier labels.

- **Archetype parity.** For each top-tier candidate, the skill pulls 3 accepted and 2 stalled analogs from the calibration set. Below parity on all dimensions of all three accepted → tier downgrade. Can't differentiate from a stalled analog → tier downgrade.

- **Two-editor desk-reject.** Before issuing a Top Generalist label, the skill writes desk-reject letters from two editor archetypes (empirical corporate vs. asset pricing/theory) in parallel. Both convincing → tier downgrade.

- **Lens-source discipline.** Ideas come from 11 generative lenses. ≥2 of the top 3 must come from Lens 1 (practitioner gap), Lens 3 (first principles), or Lens 4 (unification). Lens 10 (new data × old question) is hard-capped at Strong Field.

- **Hierarchical gates.** Tier labels are determined by gates passed, not by a smoothed total score. Importance ≥ 4 → Contribution ≥ 4 → Bridge ≥ 4 → displacement named → archetype parity → desk-reject survival. Failing any caps the verdict.

- **Three tiers.**
  - *Top Generalist Go* — JF/JFE/RFS plausible. All gates cleared.
  - *Strong Field Go* — solid paper, one or more gates failed.
  - *Workshop* — feasible but narrow scope, falls below Strong Field gates.

## Notes

- Literature reviews produce BibTeX citations automatically via `export_citations`.
- Results are saved to `notes/` and `output/`; lab notebook entries are appended automatically.
- AFA documentation is saved under `submission/` and is the primary submission artifact.
- `submission/call_requirements.md` maps the call rules to the files the skills maintain.
- The Corbis MCP is the literature search engine; expect 15-25 Corbis calls per `/brainstorm` run, 4-8 per `/idea` run after the efficiency upgrades.
- If your client reads `CLAUDE.md` and `.claude/` directly, it routes requests automatically. Otherwise use the tables above as the manual workflow guide.
