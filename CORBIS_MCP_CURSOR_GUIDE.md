# Corbis MCP and Cursor Setup

Use this guide when you clone the [AFA 2027 AI Workflow
template](https://github.com/Agentic-Assets/afa-ai-workflow) and work in
**Cursor**.

---

## 1. Clone and wire Cursor assets

```bash
git clone https://github.com/Agentic-Assets/afa-ai-workflow.git my-afa-project
cd my-afa-project
bash scripts/setup-cursor.sh
```

`setup-cursor.sh` creates symlinks from `.cursor/skills/` to `.agents/skills/`
so Cursor discovers all eleven workflows plus slash-command alias skills. On
Windows, run the script in Git Bash or WSL if symlinks fail after clone.

---

## 2. Corbis API key

1. Open [Corbis](https://www.corbis.ai) → **Settings → API Keys**
2. Create a key (`corbis_mcp_...`)
3. Export it in the shell that launches Cursor:

```bash
export CORBIS_MCP_API_KEY="corbis_mcp_..."
```

Add the same line to `~/.zshrc` or `~/.bashrc` if you want it persistent.

---

## 3. MCP server

This repo ships project MCP config at `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "corbis": {
      "type": "http",
      "url": "https://www.corbis.ai/api/mcp/universal?apikey=${CORBIS_MCP_API_KEY}"
    }
  }
}
```

1. Ensure `CORBIS_MCP_API_KEY` is set in your environment.
2. Open **Cursor Settings → MCP** and confirm the `corbis` server loads (or merge this JSON into your user MCP config).
3. Reload MCP servers after changing the key.

If env substitution does not work in your Cursor build, paste the key into the
URL once for local testing only (do not commit that file).

Architecture and auth options: [`CORBIS_MCP_GUIDE.md`](CORBIS_MCP_GUIDE.md). Tool
reference: [`CORBIS_MCP_TOOL_REFERENCE.md`](CORBIS_MCP_TOOL_REFERENCE.md).

---

## 4. Skills and slash-style prompts

Cursor reads:

- `AGENTS.md` — project instructions (skill routing, Corbis rules, shared files)
- `.cursor/rules/afa-workflow.mdc` — always-on routing and slash aliases
- `.cursor/skills/*/SKILL.md` — per-workflow instructions (symlinked from `.agents/skills/`)

Cursor does not use Claude Code’s `.claude/commands/` folder. Instead, type prompts like:

```text
Run /init-submission for my AFA project. Authors: ...
```

```text
/brainstorm political connections and firm value
```

```text
/idea [paste your one-paragraph idea]
```

The agent should load the matching skill from `.cursor/skills/`. See
[`SKILLS_USE_GUIDE.md`](SKILLS_USE_GUIDE.md) for when to use each workflow.

---

## 5. First session checklist (on or after 2026-06-01)

```text
1. /init-submission     → submission/ package
2. /calibrate-rubric    → references/top_journal_calibration.json
3. /brainstorm <topic>  or  /idea <question>
```

Log AI work with `/log-conversation` and human work with `/log-human-time`
throughout the project. Hooks in this repo target Claude Code and Codex only;
see [`submission/HOOKS.md`](submission/HOOKS.md).

---

## 6. Verify Corbis is connected

In Cursor chat:

```text
Search papers on mortgage prepayment, sort by citations, compact true, 5 results
```

You should see `search_papers` (or related Corbis tools) invoked. If tools are
missing, recheck MCP status and `CORBIS_MCP_API_KEY`.

---

## Related docs

| File | Purpose |
|------|---------|
| [`README.md`](README.md) | Template overview and all clients |
| [`SKILLS_USE_GUIDE.md`](SKILLS_USE_GUIDE.md) | Skill chaining and gate vocabulary |
| [`TEMPLATES.md`](TEMPLATES.md) | LaTeX and skill output templates |
| [`CORBIS_MCP_CLAUDE_CODE_GUIDE.md`](CORBIS_MCP_CLAUDE_CODE_GUIDE.md) | Claude Code plugin install |
| [`CORBIS_MCP_CODEX_GUIDE.md`](CORBIS_MCP_CODEX_GUIDE.md) | Codex `config.toml` setup |
