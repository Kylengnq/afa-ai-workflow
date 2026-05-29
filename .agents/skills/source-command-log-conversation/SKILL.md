---
name: "source-command-log-conversation"
description: "Capture an AI conversation transcript into submission/conversations/ and update the index"
---

# source-command-log-conversation

Use this compatibility skill when the user asks for `/log-conversation`,
`log-conversation`, or transcript backfill.

## Command Template

Run the `log-conversation` skill. Use the transcript source and metadata from
the user's prompt; ask for any missing required metadata.

Steps:
1. Resolve the transcript (pasted text, file path, or CLI session log).
2. Collect model/agent, project stage, goal, start and end timestamps, issuing author.
3. Write `submission/conversations/YYYY-MM-DD_HHMM_<slug>.md` with the verbatim transcript, outputs produced, and any mid-stream human interventions.
4. Append a row to the index in `submission/conversations/README.md`.
5. Append a dated entry to `notes/lab_notebook.md`.
