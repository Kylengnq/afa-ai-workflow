# AFA 2027 AI Workflow Submission Template

This repository is set up as a working template for the **AFA 2027 Annual Meeting
Special Session on Papers Written with Generative AI Workflows**. The call
requires authors to submit, alongside the paper, full text of every AI
conversation, a time log of human activity, a contribution report, and
documentation of the workflow and model configuration. This file (the Codex
counterpart to `CLAUDE.md`) tells you how to keep that documentation in good
shape as the project runs.

## AFA Submission Mode

**Hard rules from the call (Goldstein, Jiang, Novy-Marx, Mann):**

- Investigation begins **on or after 2026-06-01** with an initial prompt to an
  LLM or AI agent.
- Submission deadline is **2026-08-31**.
- Submission opens through the AFA website in early June, with no submission
  fee.
- The project must be entirely new and can be on any topic appropriate to a top
  finance journal.
- AI plays a systematic role across multiple stages, not just modular tool use.
- No humans outside the named authors may perform work on the project.
- Each author can submit only one lead-author paper and be listed on at most
  three submissions total.
- The ideal is highest possible research quality per unit of human expertise
  and effort, not minimum human involvement.
- Organizers state they will not use non-public submission and review
  information for their own research.

**What this repo expects of the assistant:**

1. Every meaningful AI conversation in this repo must be captured in
   `submission/conversations/` as a verbatim transcript (`log-conversation`
   skill).
2. Every block of direct human work must be logged in
   `submission/human_time_log.md` (`log-human-time`).
3. The initial prompt, model configuration, and data access plan live in
   `submission/initial_prompt.md`, `submission/model_config.md`, and
   `submission/data_access.md`. Use `init-submission` on day one.
4. The call summary and compliance map live in
   `submission/call_requirements.md`.
5. Before submission, run `contribution-report` to regenerate the
   human-vs-AI line tally.
6. The LaTeX template (`latex_template/academic_paper_template.tex`)
   includes Appendix A-D placeholders that mirror these artifacts.

## Automatic logging via hooks

Three Claude Code hooks at `.claude/hooks/` automate routine logging:
`session-start.py`, `log-turn.py` (renders the transcript to
`submission/conversations/` after every turn), and `session-end.py` (appends
to `submission/human_time_log.md`). Hooks skip if today is before 2026-06-01,
if `.no-afa-logging` exists, or if `submission/initial_prompt.md` is still the
unedited template. See `submission/HOOKS.md`.

Codex does not run these hooks; for Codex sessions use `log-conversation`
manually. When working in Claude Code with hooks active, do not re-log the
current session via `log-conversation` — it would duplicate the file.

## Skill routing

Before responding to any research-related prompt, check whether a skill applies.

| User is asking about... | Use skill |
|---|---|
| Set up the AFA submission package | `init-submission` |
| Build or refresh the top-3 journal calibration anchor | `calibrate-rubric` |
| Capture an AI conversation transcript | `log-conversation` |
| Log a block of human work | `log-human-time` |
| Regenerate the human-vs-AI contribution tally | `contribution-report` |
| Survey a topic, write a literature review | `literature-review` |
| Position a paper, find closest work, contribution | `literature-positioning-map` |
| Brainstorm research ideas from a topic area | `research-idea-generator` |
| Screen or score a specific research idea | `finance-idea-screening` |
| Verify citations in a .bib file | `verify-citations` |
| Visualize literature trends, gaps, methods | `literature-landscape` |

**First-time setup ordering:** `init-submission` → `calibrate-rubric` → `research-idea-generator` or `finance-idea-screening`. The calibration set at `references/top_journal_calibration.json` is required for the idea skills to issue "Top Generalist Go" verdicts; without it they cap at Strong Field Go.

## Corbis tool usage

**Always search before asserting.** Do not guess about novelty, literature, or
data availability when you can check.

Available tools:
- `search_papers`, `get_paper_details`, `get_paper_details_batch`, `top_cited_articles` — literature search
- `export_citations`, `format_citation` — citation management
- `search_datasets` — data discovery (for idea screening)
- `fred_search`, `fred_series_batch` — macro data context
- `get_market_data`, `compare_markets`, `search_markets`, `get_market_trends` — CRE market intelligence

Key principles:
- Use `search_papers` before claiming any idea is novel
- Use `compact: true` on `search_papers` when you only need titles and metadata (saves ~80% payload)
- Use `sortBy: "citedByCount"` to find the most influential papers on a topic
- Use `get_paper_details_batch` (up to 25 IDs) instead of repeated `get_paper_details` calls
- Use `top_cited_articles` with the `query` parameter to find highly cited papers on a specific topic within journals
- Use `export_citations` (format: `bibtex`) to generate bibliography entries

See `CORBIS_MCP_TOOL_REFERENCE.md` for full tool documentation.
See `CORBIS_MCP_GUIDE.md` for MCP server architecture and authentication.
See `CORBIS_MCP_CODEX_GUIDE.md` for Codex setup.
See `CORBIS_MCP_CLAUDE_CODE_GUIDE.md` for Claude Code setup.

## Writing quality

When producing literature reviews or research prose:
- Read `references/writing-norms.md` and `references/banned-words.md`
- Synthesize by theme, do not enumerate paper by paper
- No filler intensifiers ("crucially," "importantly," "interestingly")
- No em dashes. Use commas, parentheses, colons, or separate sentences
- No promotional language ("novel," "groundbreaking")
- Cite to support claims, not to name-drop

## Project structure

```
submission/      AFA 2027 submission package (initial prompt, conversations, human time log, contribution report)
notes/           Lab notebook, reading lists, idea menus
output/          Literature reviews, positioning memos, idea cards, paper_set.json
paper/           LaTeX manuscript (copy latex_template/ to start)
latex_template/  Article template with AFA appendix sections A-D
references/      Writing norms, citation formatting
```

## Shared data files

Skills produce composable outputs that later skills can reuse. This avoids
redundant searches.

### `output/paper_set.json`

Canonical paper dataset. Every skill that searches for papers writes results
here. Every skill that needs papers reads this first before running new
searches.

Format: JSON array of paper objects:
```json
[
  {
    "id": "W2002030205",
    "title": "...",
    "authors": ["..."],
    "year": 2001,
    "journal": "...",
    "citedByCount": 2962,
    "abstract": "...",
    "fullText": "...",
    "doi": "...",
    "source_queries": ["query1", "query2"],
    "tier": "foundational"
  }
]
```

Rules:
- If `output/paper_set.json` exists when a skill starts, read it and merge new results (deduplicate by `id`). Do not overwrite.
- The `fullText` field is included when available from `get_paper_details`. Use it for deeper analysis when present.
- The `source_queries` field tracks which search queries surfaced this paper.
- The `tier` field is assigned after collection using relative tiering.

### `output/search_log.md`

Search transparency log. Every skill appends its searches here.

### Relative citation tiering

Top 10% by `citedByCount` are **Foundational** (named, discussed). Next 30% are
**Established** (synthesized). Bottom 60% are **Emerging** (grouped). A paper
appearing in 3+ search queries is promoted one tier.

## Lab notebook

Every skill that produces a deliverable appends a dated entry to
`notes/lab_notebook.md`. If the file does not exist, create it with a header:
`# Lab Notebook`.

## Paper-reader agent

The paper-reader agent (`.claude/agents/paper-reader.md`) can read and summarize
academic PDFs. After a literature search identifies the top 3-5 most central
papers, recommend that the user run the paper-reader on those papers for
deeper understanding before writing synthesis claims.

## Defaults

- **Output format**: Save literature reviews and memos to `output/` as
  Markdown. Save BibTeX to `.bib` files. Write LaTeX directly into `.tex`
  files.
- **Citations**: Use `\citet{}` and `\citep{}` (natbib). Bibliography style:
  `plainnat`.
