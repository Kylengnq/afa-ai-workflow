# Model Configuration

Document every model, agent, and tool the project used. Reviewers will use this
to judge how much of the workflow was AI-driven.

## Primary models

| Model ID | Role | Version / date | Temperature / thinking | Context window |
|---|---|---|---|---|
| e.g., claude-opus-4-7 | main research agent | 2026-06 | thinking on, default temp | 1M |
|  |  |  |  |  |

## Agents and roles

If the workflow used named subagents (e.g., paper-reader, code-reviewer,
data-engineer), list each one, what it was responsible for, and the model it
ran on.

| Agent | Responsibility | Backing model |
|---|---|---|
|  |  |  |

## System prompts and instruction files

List every file that shaped agent behavior (e.g., `CLAUDE.md`, `AGENTS.md`,
custom system prompts) and a one-line summary of what it instructed the agent
to do. Paste the contents under a fenced block or link to the file in this repo.

## MCP servers and tools

| MCP server | URL / endpoint | Tools used |
|---|---|---|
| corbis | https://www.corbis.ai/api/mcp/universal | search_papers, get_paper_details, ... |
|  |  |  |

## Plugins and skills

Workflow skills invoked during the project (literature-review,
research-idea-generator, init-submission, etc.). Note any custom skills built
specifically for this project.

## Settings and budgets

Any rate limits, budget caps, or autonomy ceilings imposed on the agent.

## Reproducibility notes

Anything a reviewer would need to reproduce the workflow: pinned model
versions, environment files (`requirements.txt`, lockfiles), seeds, time of
last successful run.
