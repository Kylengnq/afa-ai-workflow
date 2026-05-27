# AFA 2027 Submission Package

This directory holds the artifacts the AFA 2027 Special Session on AI-Generated
Finance Research requires authors to submit alongside the paper.

## What the call requires

From the AFA 2027 call for papers (Goldstein, Jiang, Novy-Marx, Mann):

1. **An initial prompt** to an LLM or AI agent, issued **on or after 2026-06-01**.
2. **Full text of every conversation** with AI conducted in the course of the project.
3. **A time log** of human activity on the project.
4. **A report on the fraction of project lines** (code, writing, documentation) contributed by humans versus AI.
5. **Documentation of model configuration, data access, and the full workflow.**
6. **Documentation of any direct human contributions** made outside of prompts.

Submission deadline: **2026-08-31**. Each author can be listed on at most three
submissions and can submit only one paper as a lead author. No humans other than
named authors may perform work on the project.

## Artifacts in this directory

| File | Purpose | Populated by |
|---|---|---|
| `initial_prompt.md` | The seed prompt, target model, attached materials, scope | `/init-submission` |
| `model_config.md` | Model IDs, settings, system prompts, MCP servers, agents | `/init-submission` |
| `data_access.md` | Data sources accessed, credentials scope, access dates | `/init-submission` |
| `workflow.md` | Narrative of how AI was used at each stage of the project | manually, updated as the project progresses |
| `conversations/` | One Markdown file per AI conversation (full transcript) | `/log-conversation` |
| `human_time_log.md` | Running table of human work sessions | `/log-human-time` |
| `contribution_report.md` | Final tally of human vs AI lines (code, writing, docs) | `/contribution-report` |

## Submission checklist

Before submitting on 2026-08-31:

- [ ] `initial_prompt.md` populated, date is on or after 2026-06-01
- [ ] `model_config.md` lists every model, agent, and MCP used
- [ ] `data_access.md` lists every data source and access window
- [ ] `workflow.md` describes the AI/human split at each stage
- [ ] `conversations/` contains a transcript file for every AI conversation
- [ ] `human_time_log.md` covers every human work session
- [ ] `contribution_report.md` has been regenerated against the final state of the repo
- [ ] LaTeX appendix sections A through D in the paper match the artifacts here
- [ ] Author count and per-author submission count comply with the call rules
