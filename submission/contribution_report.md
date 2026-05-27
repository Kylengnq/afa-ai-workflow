# Contribution Report

Final tally of human versus AI contributions across the project. Regenerate
with `/contribution-report` before submission so the numbers reflect the final
state of the repo.

## Headline numbers

| Category | Human | AI | Total | Human share |
|---|---|---|---|---|
| Code lines | 0 | 0 | 0 | 0% |
| Writing words | 0 | 0 | 0 | 0% |
| Documentation lines | 0 | 0 | 0 | 0% |

Date generated: YYYY-MM-DD

## Scope

This report should cover code, paper text, research notes, submission
documentation, and generated artifacts that remain part of the final project
record. Exclude external source data and third-party library files. If the
project copied or vendored any third-party material, list it under edge cases.

## Method

Describe how each number was computed. Suggested defaults:

- **Code**: `git blame` line counts for files matching `*.py`, `*.R`, `*.do`,
  `*.sas`, `*.sql`, `*.ipynb`. Classify each commit's author as human or AI
  based on the committer identity convention agreed at project start (e.g.,
  commits authored by `agent@*` count as AI; everything else is human, unless
  flagged in the conversation log).
- **Writing**: word count of `paper/*.tex` body sections (everything between
  `\begin{document}` and `\bibliography`). Subtract verbatim AI passages
  recorded in `conversations/` from the AI total, add anything the human typed
  directly from the human total.
- **Documentation**: line count of `README.md`, `CLAUDE.md`, `AGENTS.md`,
  files under `notes/`, and everything under `submission/` except generated
  artifacts.
- **Transcripts**: count transcript files as documentation, but classify the
  assistant turns as AI-authored and the user turns as human-authored when the
  report can distinguish them.

If a different method was used, describe it here.

## Edge cases

Document anything that the line-counting heuristic mishandles:

- Text typed by the human but originally suggested by the AI ("ghost-written").
- AI-generated tables that the human pasted into the paper unchanged.
- Refactors that touched many lines but did not change semantic content.
- Files where authorship is genuinely ambiguous.
- Pre-existing template files that were copied into the project before the
  initial prompt.
- Third-party code, data dictionaries, or quotations that should not be
  credited to either the human authors or the AI workflow.

## Notes on the human contribution

The call asks discussants to articulate what AI-generated finance research
lacks relative to current standards. Use this section to describe the human
contribution that the line counts undersell: the choice of question, the
review of agent outputs, the rejected directions, the final judgment calls.
