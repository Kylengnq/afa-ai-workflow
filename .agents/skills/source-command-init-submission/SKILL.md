---
name: "source-command-init-submission"
description: "Bootstrap the AFA 2027 submission package \u2014 captures the initial prompt, model config, and data access plan into submission/"
---

# source-command-init-submission

Use this compatibility skill when the user asks for `/init-submission`,
`init-submission`, or first-day setup of the AFA submission package.

## Command Template

Run the `init-submission` skill. Use any initial prompt, model config, author
information, or data-access details supplied by the user.

Steps:
1. Confirm this project is intended for the AFA 2027 Special Session.
2. Validate the initial prompt date is on or after 2026-06-01.
3. Validate this is an entirely new project, only named authors will perform work, and author submission caps are satisfied.
4. Populate `submission/initial_prompt.md`, `submission/model_config.md`, and `submission/data_access.md`.
5. Confirm `submission/call_requirements.md` exists and matches the populated artifacts.
6. Add the first row to `submission/human_time_log.md` covering prompt issuance.
7. If a first AI response is available, use `log-conversation` to capture it.
8. Append a dated entry to `notes/lab_notebook.md`.
