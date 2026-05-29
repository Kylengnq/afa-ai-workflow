# AFA 2027 Call Requirements

This file summarizes the AFA 2027 Special Session call and maps each requirement
to the artifact this template maintains. It is a checklist for authors before
they submit the paper and the accompanying workflow package.

## Session

**Name:** AFA 2027 Special Session of Papers Written with Generative AI
Workflows

**Organizers:**

- Itay Goldstein, Wharton School
- Wei Jiang, Goizueta Business School, Session Chair
- Robert Novy-Marx, Simon Graduate School of Business
- William Mann, Goizueta Business School

**Purpose:** Showcase and evaluate finance research projects where generative
AI systems play a systematic role across the research process, then use that
evidence to inform norms for responsible AI use and the distinct nature of
human scholarly contribution.

## Dates and Scope

| Rule | Template artifact |
|---|---|
| Investigation begins on or after 2026-06-01. | `submission/initial_prompt.md`, validated by `init-submission` |
| The first project act is an initial prompt to an LLM or AI agent. | `submission/initial_prompt.md` and first transcript in `submission/conversations/` |
| Submission deadline is 2026-08-31. | `README.md`, `submission/README.md`, final checklist |
| Submission opens through the AFA website in early June. | Final submission checklist |
| There is no submission fee. | This call summary |
| The paper can be on any topic appropriate to a top finance journal. | Research workflow and paper template |
| The project must be entirely new. | Eligibility table in `submission/initial_prompt.md` |

## Authorship and Human Labor

| Rule | Template artifact |
|---|---|
| No humans outside the named authors may perform work on the project. | Eligibility table in `submission/initial_prompt.md`; workflow notes in `submission/workflow.md` |
| Each author can submit only one lead-author paper. | Eligibility table in `submission/initial_prompt.md` |
| Each author can be listed on at most three submissions total. | Eligibility table in `submission/initial_prompt.md` |
| Direct human contributions outside prompts are allowed but must be documented. | `submission/human_time_log.md` and `submission/workflow.md` |
| The target is high research quality per unit of human expertise and effort, not zero human involvement. | `submission/workflow.md` and `submission/contribution_report.md` |

## Required Documentation

| Required item | Template artifact |
|---|---|
| Full text of every AI conversation, including the initial prompt. | `submission/conversations/` and `submission/conversations/README.md` |
| Time log of human activity. | `submission/human_time_log.md` |
| Report on the fraction of project lines contributed by humans versus AI. | `submission/contribution_report.md` |
| Initial inputs. | `submission/initial_prompt.md` |
| Data access. | `submission/data_access.md` |
| Model configuration. | `submission/model_config.md` |
| Full workflow. | `submission/workflow.md` |

## How the template strictly enforces the rules

| Rule | Enforcement mechanism |
|---|---|
| Investigation begins on or after 2026-06-01. | `/init-submission` refuses to populate `initial_prompt.md` with an earlier date. All three Claude Code hooks (`session-start.py`, `log-turn.py`, `session-end.py`) and both Codex hooks skip silently before that date. `/log-human-time` refuses sessions before 2026-06-01. |
| Entirely new project. | `/init-submission` requires explicit confirmation in the eligibility gate of `initial_prompt.md`. |
| First project act is the initial prompt. | Eligibility gate in `initial_prompt.md`. |
| No non-author humans perform project work. | Eligibility gate in `initial_prompt.md`. `workflow.md` compliance summary is the audit exhibit. |
| Each author on ≤ 3 submissions, ≤ 1 lead-author paper. | Eligibility gate in `initial_prompt.md`. `/init-submission` refuses if the gate is unconfirmed. |
| All AI conversations documented. | Hooks at `.claude/hooks/` and `.codex/hooks/` auto-capture every Claude Code / Codex session as Markdown under `conversations/`, with credential scrubbing. `/log-conversation` for non-hooked sessions. |
| Time log of human activity. | `/log-human-time` for manual entries; the `SessionEnd` hook appends `auto-review` rows that the human reclassifies before submission. |
| Contribution report. | `/contribution-report` regenerates from `git blame` and cross-references against `conversations/`. Refuses to run with uncommitted changes. |
| Direct human contributions documented. | `workflow.md` has a dedicated "Direct human contributions outside of prompts" table. The contribution report's edge-cases section captures ghost-written / paste-of-AI categories. |
| AI plays a systematic role across multiple stages. | `model_config.md` has an "AI role by stage" table covering eight project stages; the LaTeX paper template has matching Appendix A-D placeholders. |

## Fail-closed behavior

The template is built so that nothing creating a falsified compliance record can run before the AFA rules permit it:

- All hooks skip if today is before 2026-06-01.
- All hooks skip if `submission/initial_prompt.md` still contains the unedited template placeholder text.
- A `.no-afa-logging` file at the repo root disables hooks for sessions the author does not want included in the submission record (e.g., exploratory work that is not part of the project).
- `/init-submission`, `/log-human-time`, and `/log-conversation` refuse to write entries dated before 2026-06-01.

## Evaluation Emphasis

Human reviewers will use standard academic criteria: novelty and importance of
the research question, incremental contribution to the literature, and quality
of execution. The special session also emphasizes how much of the research
process was carried out by AI systems, with limited human intervention.

Discussants are expected to assess both scientific merit and the nature of
human labor embodied in the paper. They will also discuss what AI-generated
finance research lacks relative to current standards of originality and
excellence.

## Privacy Note

The call states that organizers will not use non-public information from the
submission and review process for their own research. Authors should still
remove credentials, private identifiers, and confidential data from transcript
files before submission.

## Final Author Checklist

- [ ] The project investigation began on or after 2026-06-01.
- [ ] The first project act was an initial prompt to an AI system.
- [ ] The paper is an entirely new project.
- [ ] All named authors satisfy the lead-author and total-submission caps.
- [ ] No non-author human performed project work.
- [ ] AI contributed across multiple research stages, not only modular tasks.
- [ ] Every AI conversation transcript is present under `submission/conversations/`.
- [ ] Every block of direct human work is present in `submission/human_time_log.md`.
- [ ] `submission/contribution_report.md` has been regenerated from the final repo.
- [ ] The paper appendices match the submission artifacts.
- [ ] Submission is made through the AFA website by 2026-08-31.
