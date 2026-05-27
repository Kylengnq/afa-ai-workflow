# Skills Guide

How to use the ten workflows in this AFA 2027 submission template. In Claude
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

### Research skills

| I want to... | Skill / Command |
|---|---|
| Survey what a field knows about a topic | `/lit-review` |
| Find the closest papers to my idea and sharpen the contribution | `/lit-search` |
| Generate research ideas in a topic area | `/brainstorm` |
| Evaluate whether a specific idea is worth pursuing | `/idea` |
| Check that my citations are correct and complete | `/verify-citations` |
| Visualize trends, gaps, and methods in a literature | `/lit-landscape` |

## The submission workflow

A typical AFA-track project pipes through the submission skills like this:

```text
Day 1 (on or after 2026-06-01):
  /init-submission          -> captures the initial prompt, model, data plan
  /log-conversation         -> capture the opening AI exchange

Throughout the project:
  /log-conversation         -> after every meaningful AI session
  /log-human-time           -> after every block of direct human work
  /lit-review, /brainstorm, /idea, ...  -> research work, AI-driven

Before submission (by 2026-08-31):
  /contribution-report      -> regenerate the human-vs-AI tally
  Update paper/ with Appendix A-D referencing submission/*
```

## Common research workflows

**Starting from scratch:**
1. `/lit-review [your topic]` — understand the field
2. `/brainstorm [your topic]` — generate ideas from gaps you found
3. `/idea [best idea]` — screen it rigorously

**Positioning an existing idea:**
1. `/lit-search [your paper's question]` — find closest work
2. `/idea [your idea]` — score and stress-test it

**Visualizing a literature:**
1. `/lit-review [your topic]` — build the paper set
2. `/lit-landscape [your topic]` — generate trend and gap figures

**Polishing citations:**
1. `/verify-citations` — audit your `.bib` against Corbis

**Reading a paper:**

If your assistant supports repo-defined agents, use the paper-reader prompt:
> "Read and summarize the paper at ~/Downloads/fama_french_1993.pdf"

## Notes

- Literature reviews produce BibTeX citations automatically via `export_citations`.
- Results are saved to `notes/` and `output/` with lab notebook entries.
- AFA documentation is saved under `submission/`; that directory is the
  primary submission artifact.
- If your client reads `CLAUDE.md` and `.claude/` directly, it can route
  requests automatically. Otherwise, use the tables above as the manual
  workflow guide.
