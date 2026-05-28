---
description: Bootstrap the AFA 2027 submission package — captures the initial prompt, model config, and data access plan into submission/
---

Run the `init-submission` skill.

Inputs from the user, if not yet provided:

$ARGUMENTS

Steps:
1. Confirm this project is intended for the AFA 2027 Special Session.
2. Validate the initial prompt date is on or after 2026-06-01.
3. Validate this is an entirely new project, only named authors will perform work, and author submission caps are satisfied.
4. Populate `submission/initial_prompt.md`, `submission/model_config.md`, and `submission/data_access.md`.
5. Confirm `submission/call_requirements.md` exists and matches the populated artifacts.
6. Add the first row to `submission/human_time_log.md` covering prompt issuance.
7. If a first AI response is available, chain into `/log-conversation` to capture it.
8. Append a dated entry to `notes/lab_notebook.md`.
