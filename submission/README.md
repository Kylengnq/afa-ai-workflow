# AFA 2027 Submission Package

This directory holds the artifacts the AFA 2027 Special Session of Papers
Written with Generative AI Workflows requires authors to submit alongside the
paper. `call_requirements.md` is the canonical local checklist for the call.

## What the call requires

From the AFA 2027 call for papers (Goldstein, Jiang, Novy-Marx, Mann):

1. **An initial prompt** to an LLM or AI agent, issued **on or after 2026-06-01**.
2. **Full text of every conversation** with AI conducted in the course of the project.
3. **A time log** of human activity on the project.
4. **A report on the fraction of project lines** (code, writing, documentation) contributed by humans versus AI.
5. **Documentation of model configuration, data access, and the full workflow.**
6. **Documentation of any direct human contributions** made outside of prompts.
7. **An entirely new project** where AI contributes across multiple stages, not only modular tasks.

Submission deadline: **2026-08-31**. Each author can be listed on at most three
submissions and can submit only one paper as a lead author. No humans other than
named authors may perform work on the project. There is no submission fee;
submission opens through the AFA website in early June.

## Artifacts in this directory

| File | Purpose | Populated by |
|---|---|---|
| `call_requirements.md` | Call summary, rules, organizer list, and compliance mapping | template |
| `initial_prompt.md` | The seed prompt, target model, attached materials, scope | `/init-submission` |
| `model_config.md` | Model IDs, settings, system prompts, MCP servers, agents | `/init-submission` |
| `data_access.md` | Data sources accessed, credentials scope, access dates | `/init-submission` |
| `workflow.md` | Narrative of how AI was used at each stage of the project | manually, updated as the project progresses |
| `conversations/` | One Markdown file per AI conversation (full transcript) | `/log-conversation` |
| `human_time_log.md` | Running table of human work sessions | `/log-human-time` |
| `contribution_report.md` | Final tally of human vs AI lines (code, writing, docs) | `/contribution-report` |

## How this connects to the research workflow

The artifacts here document the workflow. The actual research happens through
the repo's research skills:

- `/calibrate-rubric` (one-time, refresh every ~6 months) builds the held-out top-3 journal anchor.
- `/brainstorm <topic>` generates ranked ideas calibrated against that anchor.
- `/idea <specific idea>` screens a single candidate end-to-end.
- `/lit-review`, `/lit-search`, `/lit-landscape`, `/verify-citations` support the literature work.

## How conversation capture works

Conversation transcripts are captured two ways:

1. **Automatic capture via Claude Code hooks** (`.claude/hooks/`). When Claude
   Code runs in this repo on or after 2026-06-01, after `submission/initial_prompt.md`
   has been populated, the `Stop` hook re-renders the entire session transcript
   into `conversations/` after every assistant turn. The `SessionEnd` hook
   appends a row to `human_time_log.md` and to the conversation index. See
   `HOOKS.md` for details. Codex has equivalent hooks under `.codex/hooks/`.
2. **Manual capture for non-hooked sessions.** For conversations that happened
   outside Claude Code or Codex (web UI, phone, other CLIs), use
   `/log-conversation` to paste the transcript into the same directory.

Direct human work that does not happen inside an AI session — typing into files
in another editor, data pulled by hand, offline decisions — must be logged
manually with `/log-human-time` and described in `workflow.md`. The hooks
cannot observe this work.

See `../README.md` and `../SKILLS_USE_GUIDE.md` for the full skill catalog.

## Submission checklist

Before submitting on 2026-08-31:

- [ ] `initial_prompt.md` populated, date is on or after 2026-06-01
- [ ] `initial_prompt.md` confirms this is an entirely new project and lists named authors
- [ ] `model_config.md` lists every model, agent, and MCP used
- [ ] `data_access.md` lists every data source and access window
- [ ] `workflow.md` describes the AI/human split at each stage
- [ ] `conversations/` contains a transcript file for every AI conversation
- [ ] `human_time_log.md` covers every human work session
- [ ] `contribution_report.md` has been regenerated against the final state of the repo
- [ ] `call_requirements.md` final checklist is complete
- [ ] LaTeX appendix sections A through D in the paper match the artifacts here
- [ ] Author count and per-author submission count comply with the call rules
