<div align="center">

# AFA 2027 AI Workflow Submission Template

**A working template for the AFA 2027 Annual Meeting Special Session on papers
written predominantly by generative AI. Bootstraps the documentation the call
requires — initial prompt, conversation transcripts, human time log,
contribution report — alongside literature, idea, and citation skills powered
by the Corbis MCP.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Works%20with-Claude%20Code-orange)](https://docs.anthropic.com/en/docs/claude-code)
[![Codex](https://img.shields.io/badge/Works%20with-Codex-black)](./CORBIS_MCP_CODEX_GUIDE.md)
[![Cursor](https://img.shields.io/badge/Works%20with-Cursor-green)](https://cursor.sh)
[![Corbis MCP](https://img.shields.io/badge/Search%20with-Corbis-purple)](https://www.corbis.ai)

[The AFA Call](#the-afa-call) | [Quick Start](#quick-start) | [Workflows](#workflows) | [Submission Checklist](#submission-checklist) | [Project Structure](#project-structure)

</div>

---

## The AFA Call

The 2027 AFA Annual Meeting includes a **Special Session of Papers Written with
Generative AI Workflows**, organized by Itay Goldstein (Wharton), Wei Jiang
(Goizueta, session chair), Robert Novy-Marx (Simon), and William Mann
(Goizueta).

Headline rules:

- The investigation begins **on or after 2026-06-01** with an initial prompt to
  an LLM or AI agent.
- Submission deadline is **2026-08-31**.
- AI plays a systematic role **across multiple stages** of the project, not
  just modular tool use.
- Authors submit, alongside the paper, a **full text of every AI conversation**,
  a **time log of human activity**, and a **report on the fraction of project
  lines** (code, writing, documentation) contributed by humans versus AI.
- Each author can be listed on at most three submissions and can submit only
  one paper as lead. No humans outside the named authors may perform work on
  the project.
- The ideal is not zero human involvement, but **highest possible research
  quality per unit of human expertise and effort.**

This repo is one author's working template for that submission: a structured
place to hold the documentation, plus the research skills the project actually
runs on.

## What's in the Box

| Surface | Purpose |
|---|---|
| `submission/` | The AFA submission package — initial prompt, model config, data access, workflow narrative, conversations/, human time log, contribution report |
| AFA skills (`/init-submission`, `/log-conversation`, `/log-human-time`, `/contribution-report`) | Maintain the submission package as the project runs |
| Literature skills (`/lit-review`, `/lit-search`, `/brainstorm`, `/idea`, `/verify-citations`, `/lit-landscape`) | Do the actual research; the call permits and expects AI-driven research |
| Corbis MCP | Literature search across 400,000+ papers, plus FRED, market data, and dataset discovery |
| `latex_template/` | A clean article template with four AFA-specific appendix sections (workflow, initial prompt, contributions, conversation index) |
| `notes/lab_notebook.md` | Project log; every skill appends a dated entry |

## Quick Start

### 1. Use the repo as your project workspace

```bash
git clone https://github.com/Agentic-Assets/afa-ai-workflow.git my-afa-project
cd my-afa-project
```

### 2. Get a Corbis API key (for literature search)

Open the **[Corbis app](https://www.corbis.ai)**, go to **Settings > API Keys**,
and create a key starting with `corbis_mcp_`. Export it:

```bash
export CORBIS_MCP_API_KEY="corbis_mcp_..."
```

### 3. Wire up your AI assistant

<details>
<summary><b>Claude Code</b></summary>

```bash
claude mcp add corbis --transport http https://www.corbis.ai/api/mcp/universal?apikey=YOUR_KEY
claude
```

Full guide: [`CORBIS_MCP_CLAUDE_CODE_GUIDE.md`](CORBIS_MCP_CLAUDE_CODE_GUIDE.md)
</details>

<details>
<summary><b>Codex</b></summary>

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.corbis]
url = "https://www.corbis.ai/api/mcp/universal"
bearer_token_env_var = "CORBIS_MCP_API_KEY"
startup_timeout_sec = 20
tool_timeout_sec = 120
```

Full guide: [`CORBIS_MCP_CODEX_GUIDE.md`](CORBIS_MCP_CODEX_GUIDE.md)
</details>

<details>
<summary><b>Cursor</b></summary>

**Settings > MCP Servers > Add**

- Name: `corbis`
- URL: `https://www.corbis.ai/api/mcp/universal?apikey=YOUR_KEY`
</details>

<details>
<summary><b>Other MCP clients</b></summary>

Endpoint: `https://www.corbis.ai/api/mcp/universal`. Auth via
`Authorization: Bearer YOUR_KEY` or `?apikey=YOUR_KEY`.

Architecture and client notes: [`CORBIS_MCP_GUIDE.md`](CORBIS_MCP_GUIDE.md)
</details>

### 4. Bootstrap the submission package

On the first day of the project, after the initial prompt has been issued:

```text
/init-submission
```

The skill will validate that your initial-prompt date is on or after
2026-06-01, then populate `submission/initial_prompt.md`,
`submission/model_config.md`, and `submission/data_access.md`.

### 5. Keep the documentation current as you work

| Workflow trigger | Skill |
|---|---|
| You finished an AI conversation | `/log-conversation` |
| You finished a block of direct human work | `/log-human-time` |
| You did research that benefits from a literature scan | `/lit-review`, `/lit-search`, `/brainstorm`, `/idea`, `/lit-landscape` |
| You polished citations in your `.bib` | `/verify-citations` |
| You are preparing the final submission | `/contribution-report` |

## Workflows

### AFA submission skills (new)

| Workflow | What it does |
|---|---|
| `/init-submission` | Capture the initial prompt, model configuration, and data access plan |
| `/log-conversation` | Append a verbatim AI transcript to `submission/conversations/` |
| `/log-human-time` | Append a human work session to `submission/human_time_log.md` |
| `/contribution-report` | Recompute the human-vs-AI line tally in `submission/contribution_report.md` |

### Research skills (existing)

| Workflow | What it does |
|---|---|
| `/lit-review` | Structured literature review on any topic |
| `/lit-search` | Closest papers to your idea, contribution sharpening |
| `/brainstorm` | Ranked research ideas with novelty rejection |
| `/idea` | Stress-test a specific research idea |
| `/verify-citations` | Audit a `.bib` file against the literature |
| `/lit-landscape` | Trend, gap, method, and landmark-paper figures |

Plus a **paper-reader subagent prompt** for assistants that support repo-defined
agents.

### How the research skills connect

Skills share data through `output/paper_set.json`, so one workflow can hand off
to the next without repeating searches:

```text
/lit-review [topic]       -> builds the paper set
/lit-landscape [topic]    -> reads the paper set and generates figures
/brainstorm [topic]       -> tests idea novelty against the paper set
/idea [specific idea]     -> finds the closest papers from the paper set
```

Every search is also logged to `output/search_log.md`.

## Submission Checklist

Before submitting on 2026-08-31:

- [ ] `submission/initial_prompt.md` populated, date on or after 2026-06-01
- [ ] `submission/model_config.md` lists every model, agent, and MCP used
- [ ] `submission/data_access.md` lists every data source and access window
- [ ] `submission/workflow.md` describes the AI/human split at each stage
- [ ] Every meaningful AI conversation is logged under `submission/conversations/`
- [ ] `submission/human_time_log.md` covers every human work session
- [ ] `submission/contribution_report.md` regenerated against the final repo
- [ ] LaTeX appendix sections A through D in the paper match the artifacts above
- [ ] Author count and per-author submission count comply with the call rules

## Project Structure

```text
submission/                  AFA submission package
  initial_prompt.md            Seed prompt and metadata
  model_config.md              Model, agents, MCP servers
  data_access.md               Data sources and access dates
  workflow.md                  Stage-by-stage narrative
  conversations/               Verbatim AI transcripts, one per file
  human_time_log.md            Running human work log
  contribution_report.md       Human vs AI line tally
.claude-plugin/              Claude Code plugin manifest
.codex-plugin/               Codex plugin manifest
.claude/skills/              Workflow definitions (Claude Code)
.claude/commands/            Slash-command wrappers
.claude/agents/              Paper-reader subagent prompt
.agents/skills/              Workflow definitions (Codex and other MCP agents)
notes/lab_notebook.md        Project log
output/                      Reviews, memos, figures, paper_set.json
paper/                       LaTeX manuscript (copy from latex_template/)
latex_template/              Article template with AFA appendix sections
references/                  Writing norms, citation formatting
```

## Optional Extras

| Dependency | Purpose | Install |
|---|---|---|
| Python 3.10+ | `/lit-landscape` figures | `pip install -r requirements.txt` |
| LaTeX | Drafting the paper | `cp -r latex_template/ paper/` |

## Install as a Claude Code Plugin

```bash
# From a Claude Code session, pointed at a local clone of this repo:
/plugin install ./
```

Installs the ten skills, ten slash commands, paper-reader subagent, and Corbis
MCP server in one step. A parallel Codex manifest is at
`.codex-plugin/plugin.json`. Set `CORBIS_MCP_API_KEY` before use.

## Documentation

| File | What it covers |
|---|---|
| [`submission/README.md`](submission/README.md) | The submission package layout and checklist |
| [`SKILLS_USE_GUIDE.md`](SKILLS_USE_GUIDE.md) | Which workflow to use, when, and how to chain them |
| [`CORBIS_MCP_CLAUDE_CODE_GUIDE.md`](CORBIS_MCP_CLAUDE_CODE_GUIDE.md) | Claude Code setup |
| [`CORBIS_MCP_CODEX_GUIDE.md`](CORBIS_MCP_CODEX_GUIDE.md) | Codex setup |
| [`CORBIS_MCP_TOOL_REFERENCE.md`](CORBIS_MCP_TOOL_REFERENCE.md) | Tool-by-tool parameters and workflow tips |
| [`CORBIS_MCP_GUIDE.md`](CORBIS_MCP_GUIDE.md) | MCP architecture and multi-client integration |

## Acknowledgments and Scope

This template does not endorse any one position on the appropriate role of AI
in finance research; it just makes the documentation the AFA 2027 call
requires easier to produce. The literature skills bundled here are useful but
optional. Authors are free to swap them out, use different MCPs, or work
entirely outside of these workflows — what matters for the call is the
documentation in `submission/` and the paper itself.

---

<div align="center">

[Corbis MCP](https://www.corbis.ai/) | [Quick Start](#quick-start) | [Workflows](#workflows) | [Submission Checklist](#submission-checklist) | [MIT License](LICENSE)

</div>
