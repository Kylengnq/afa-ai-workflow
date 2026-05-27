# Conversations

One file per AI conversation, capturing the full transcript. The AFA call asks
for "a text of all conversations with AI"; this directory satisfies that
requirement.

Log the initial prompt conversation, research conversations, coding sessions,
analysis sessions, writing sessions, review sessions, failed attempts, and
autonomous runs. Do not omit a conversation because it produced no final
artifact.

## File naming

```
YYYY-MM-DD_HHMM_<short-slug>.md
```

Examples:
- `2026-06-01_0900_initial-prompt.md`
- `2026-06-12_1430_literature-positioning.md`
- `2026-07-03_2200_overnight-autonomous-run.md`

## File contents

Each conversation file should include:

1. **Frontmatter** with model, agent, stage, started, ended.
2. **Goal** — one or two sentences on what the conversation was trying to accomplish.
3. **Full transcript** — every user turn and every assistant turn, verbatim.
   Tool calls and tool results should be included or summarized in a
   collapsible block. If the conversation came from Claude Code or a similar
   CLI, paste the session log directly.
4. **Outputs produced** — paths to files written or modified by the conversation.
5. **Human interventions** — anywhere the human typed text directly into the
   tool stream or steered the agent mid-conversation.

## Index

Append a row for each conversation (newest at the bottom). `/log-conversation`
maintains this table automatically.

| File | Date | Stage | Model / agent | Goal |
|---|---|---|---|---|

## Privacy note

Per the call: organizers will not use non-public information from the
submission for their own research. Even so, scrub any credentials, personal
identifiers, or confidential data from transcripts before submission.
