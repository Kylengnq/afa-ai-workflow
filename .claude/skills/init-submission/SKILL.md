---
name: init-submission
description: "Bootstrap the AFA 2027 submission package. Captures the initial prompt, model configuration, and data-access plan into submission/ artifacts and validates the start date against the call's 2026-06-01 floor."
---

# Init Submission

Bootstraps the `submission/` directory for an AFA 2027 special-session entry. Run
this once, on the day the project starts.

## When to use

- The user is starting a new project intended for the AFA 2027 special session.
- The user wants to backfill the `submission/` artifacts on an in-flight project.
- The user asks to "set up the submission template," "initialize the AFA
  package," or "capture the seed prompt."

## Inputs to collect

| Input | Required? | Notes |
|---|---|---|
| Initial prompt text | Yes | Verbatim; paste, do not paraphrase |
| Date and time the prompt was issued | Yes | Must be on or after 2026-06-01 |
| Target model and version | Yes | e.g., claude-opus-4-7 |
| Interface or CLI used | Yes | e.g., Claude Code, Codex CLI, ChatGPT web |
| Issuing author | Yes | Name as it will appear on the paper |
| Attached materials | No | Files, links, datasets given to the agent |
| MCP servers planned | No | List the servers in `.mcp.json` |
| Planned data sources | No | Corbis, WRDS, FRED, etc. |
| Subagents or skills planned | No | Custom or stock skills the project will use |

## Steps

1. Confirm the project is genuinely intended for the AFA 2027 special session.
   If unclear, ask.
2. Validate the issuance date: must be on or after 2026-06-01. If earlier,
   refuse to proceed and explain the call's rule.
3. Populate `submission/initial_prompt.md`:
   - Fill the metadata table with the inputs.
   - Paste the prompt text verbatim under "Prompt text."
   - Ask the user for the one-or-two sentence "Why this question" rationale.
4. Populate `submission/model_config.md` with the model, version, settings,
   MCP servers, planned agents, and instruction files (`CLAUDE.md`,
   `AGENTS.md`).
5. Populate `submission/data_access.md` with the planned data sources,
   credential scope, and access method.
6. If `submission/human_time_log.md` is empty (only the header), add a first
   entry covering the time the human spent issuing the initial prompt.
7. If the first AI response exists, immediately invoke the `log-conversation`
   skill so `submission/conversations/` has its first transcript.
8. Append a dated entry to `notes/lab_notebook.md`:
   `## YYYY-MM-DD — init-submission` followed by a one-line summary.

## Outputs

- `submission/initial_prompt.md` (populated)
- `submission/model_config.md` (populated)
- `submission/data_access.md` (populated)
- `submission/human_time_log.md` (first row added)
- Optional: first transcript file in `submission/conversations/`
- Entry in `notes/lab_notebook.md`

## Validation

- Reject any issuance date earlier than 2026-06-01.
- Warn if the user lists more than three projects they intend to submit (the
  call caps each author at three submissions).
- Warn if any non-author humans are listed as contributors (the call requires
  that no humans outside the named authors perform work on the project).
