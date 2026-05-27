---
description: Bootstrap the AFA 2027 submission package — captures the initial prompt, model config, and data access plan into submission/
---

Run the `init-submission` skill.

Inputs from the user, if not yet provided:

$ARGUMENTS

Steps:
1. Confirm this project is intended for the AFA 2027 Special Session.
2. Validate the initial prompt date is on or after 2026-06-01.
3. Populate `submission/initial_prompt.md`, `submission/model_config.md`, and `submission/data_access.md`.
4. Add the first row to `submission/human_time_log.md` covering prompt issuance.
5. If a first AI response is available, chain into `/log-conversation` to capture it.
6. Append a dated entry to `notes/lab_notebook.md`.
