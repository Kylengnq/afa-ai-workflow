---
description: Capture an AI conversation transcript into submission/conversations/ and update the index
---

Run the `log-conversation` skill.

Conversation source and metadata from the user:

$ARGUMENTS

Steps:
1. Resolve the transcript (pasted text, file path, or CLI session log).
2. Collect model/agent, project stage, goal, start and end timestamps, issuing author.
3. Write `submission/conversations/YYYY-MM-DD_HHMM_<slug>.md` with the verbatim transcript, outputs produced, and any mid-stream human interventions.
4. Append a row to the index in `submission/conversations/README.md`.
5. Append a dated entry to `notes/lab_notebook.md`.
