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
- Submission opens through the AFA website in early June, and there is no
  submission fee.
- Papers can be on any topic appropriate to a top journal in finance.
- Projects must be entirely new.
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

Reviewers will apply standard academic criteria, including the novelty and
importance of the question, the incremental contribution to the literature, and
execution quality. The session also evaluates the design and effectiveness of
the AI workflow. Human discussants will assess scientific merit and the nature
of human labor embodied in the paper.

The organizers state that they will not use non-public information from the
submission and review process for their own research. The local call summary
and compliance map live at [`submission/call_requirements.md`](submission/call_requirements.md).

This repo is one author's working template for that submission: a structured
place to hold the documentation, plus the research skills the project actually
runs on.

## What's in the Box

| Surface | Purpose |
|---|---|
| `submission/` | The AFA submission package — call requirements, initial prompt, model config, data access, workflow narrative, conversations/, human time log, contribution report |
| AFA skills (`/init-submission`, `/log-conversation`, `/log-human-time`, `/contribution-report`) | Maintain the submission package as the project runs |
| Calibration skill (`/calibrate-rubric`) | Build the held-out top-3 journal anchor that gates "Top Generalist Go" labels in idea screening |
| Research skills (`/lit-review`, `/lit-search`, `/brainstorm`, `/idea`, `/verify-citations`, `/lit-landscape`) | Do the actual research; the call permits and expects AI-driven research |
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

### 4. First run — in this order

The skills depend on a small amount of setup. For a real AFA project, run them
in this order on or after 2026-06-01:

```text
/init-submission        # captures the initial prompt, validates 2026-06-01+, populates submission/
/calibrate-rubric       # builds references/top_journal_calibration.json from recent JF/JFE/RFS
/brainstorm <topic>     # generates 10 ranked ideas; requires the calibration set to issue Top Generalist labels
/idea <best candidate>  # screens the chosen idea end-to-end and returns Go / Revise / Kill
```

`/calibrate-rubric` is the step most people miss. Without it, `/brainstorm` and `/idea` cap their verdict at "Strong Field Go" — they still run, but they can't certify an idea against the top-3 journal frontier. It takes ~5-10 minutes and only needs to run once every ~6 months.

### 5. Keep the documentation current as you work

| Workflow trigger | Skill |
|---|---|
| You finished an AI conversation | `/log-conversation` |
| You finished a block of direct human work | `/log-human-time` |
| You did research that benefits from a literature scan | `/lit-review`, `/lit-search`, `/brainstorm`, `/idea`, `/lit-landscape` |
| The frontier moved (every ~6 months) | `/calibrate-rubric` |
| You polished citations in your `.bib` | `/verify-citations` |
| You are preparing the final submission | `/contribution-report` |

## Workflows

### AFA submission skills

| Workflow | What it does |
|---|---|
| `/init-submission` | Capture the initial prompt, model configuration, and data access plan |
| `/log-conversation` | Append a verbatim AI transcript to `submission/conversations/` |
| `/log-human-time` | Append a human work session to `submission/human_time_log.md` |
| `/contribution-report` | Recompute the human-vs-AI line tally in `submission/contribution_report.md` |

### Calibration

| Workflow | What it does |
|---|---|
| `/calibrate-rubric` | Build (or refresh) `references/top_journal_calibration.json` — the held-out anchor of ~20 recent JF/JFE/RFS acceptances and ~20 stalled analogs that gates "Top Generalist Go" labels in `/brainstorm` and `/idea`. Run once every ~6 months. |

### Research skills

| Workflow | What it does |
|---|---|
| `/lit-review` | Structured literature review on any topic |
| `/lit-search` | Closest papers to your idea, contribution sharpening |
| `/brainstorm` | Ranked research ideas with novelty rejection, calibrated against the top-3 frontier |
| `/idea` | Stress-test a specific research idea against the calibration set |
| `/verify-citations` | Audit a `.bib` file against the literature |
| `/lit-landscape` | Trend, gap, method, and landmark-paper figures |

Plus a **paper-reader subagent prompt** for assistants that support repo-defined
agents.

### Key concepts you'll see in the output

`/brainstorm` and `/idea` use a few terms that aren't standard finance vocabulary. Quick definitions:

- **Displacement target.** The specific paper, model claim, or empirical regularity an idea would render wrong if it's right. Ideas without a concrete displacement target are capped at Strong Field — they may be good projects but they aren't top-3 ambitious. Example: *"This would displace Krishnamurthy & Vissing-Jørgensen's (2012) claim that liquidity premia are driven only by collateral demand."*
- **Calibration set.** The held-out reference file at `references/top_journal_calibration.json`, built by `/calibrate-rubric`. Contains ~20 recent JF/JFE/RFS acceptances and ~20 stalled SSRN analogs with their question, mechanism, identification style, and displacement target. Acts as the external anchor for tier labels.
- **Archetype parity.** For each top-tier candidate, the skill picks 3 accepted and 2 stalled analogs from the calibration set sharing the candidate's mechanism. If the candidate is below parity on breadth/cleanness/surprise against all three accepted analogs, it gets downgraded. If it can't differentiate itself from at least one stalled analog, also downgraded.
- **Two-editor desk-reject.** Before issuing a Top Generalist label, the skill simulates desk-reject letters from two editor archetypes (empirical corporate vs. asset pricing/theory). Both convincing → tier downgrade.
- **Lens-source discipline.** Ideas come from one of 11 generative lenses. The skill enforces that ≥2 of the top 3 ranked ideas come from Lens 1 (practitioner gap), Lens 3 (first principles), or Lens 4 (unification). Lens 10 (new data × old question) is hard-capped at Strong Field — historically most "new data" papers don't reach top-3.
- **Three tiers.** *Top Generalist Go* (JF/JFE/RFS plausible — all gates cleared), *Strong Field Go* (solid paper at a strong field journal — one or more gates failed), *Workshop* (feasible but narrow scope).

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
- [ ] `submission/initial_prompt.md` confirms a new project, named authors only, and author submission caps
- [ ] `submission/model_config.md` lists every model, agent, and MCP used
- [ ] `submission/data_access.md` lists every data source and access window
- [ ] `submission/workflow.md` describes the AI/human split at each stage
- [ ] `submission/workflow.md` demonstrates AI work across multiple stages, not only modular tasks
- [ ] Every meaningful AI conversation is logged under `submission/conversations/`
- [ ] `submission/human_time_log.md` covers every human work session
- [ ] `submission/contribution_report.md` regenerated against the final repo
- [ ] `submission/call_requirements.md` final checklist is complete
- [ ] LaTeX appendix sections A through D in the paper match the artifacts above
- [ ] Author count and per-author submission count comply with the call rules

## Project Structure

```text
submission/                  AFA submission package
  call_requirements.md         Call summary and compliance mapping
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

Installs the eleven skills, eleven slash commands, paper-reader subagent, and Corbis
MCP server in one step. A parallel Codex manifest is at
`.codex-plugin/plugin.json`. Set `CORBIS_MCP_API_KEY` before use.

## Documentation

| File | What it covers |
|---|---|
| [`submission/call_requirements.md`](submission/call_requirements.md) | AFA call summary, ground rules, organizer list, and compliance mapping |
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
