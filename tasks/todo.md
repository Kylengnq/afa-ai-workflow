# Task Todo

## 2026-04-15 — Add Codex Plugin Support

- [x] Inspect the repo metadata, existing MCP config, and available skill directories
- [x] Create a root Codex plugin manifest at `.codex-plugin/plugin.json`
- [x] Point the plugin at `.agents/skills/` and the existing `.mcp.json`
- [x] Validate the JSON files parse cleanly and the manifest shape matches the Codex plugin spec
- [x] Add a short review section with what changed and verification results

## Review

- Added `.codex-plugin/plugin.json` so the repository can be used as a Codex plugin with its bundled research skills.
- Wired the plugin to `./.agents/skills/` and `./.mcp.json`.
- Normalized `.mcp.json` to use the `corbis` server name and `${CORBIS_MCP_API_KEY}` placeholder, matching the repo's Codex setup guide.
- Verified both JSON files parse successfully with `python3`.

## 2026-04-15 — Codex Plugin Discovery Audit

- [x] Audit the existing Codex plugin manifest, MCP wiring, and skill inventory
- [x] Add missing discovery artifacts for marketplace-style plugin discovery without restructuring the repo
- [x] Validate every discovery JSON file and document the final discovery paths

## Review

- Kept the existing repo-root Codex plugin manifest in place for direct use from the repository root.
- Added `.agents/plugins/marketplace.json` so the repo now exposes a marketplace-style discovery index.
- Added `plugins/afa-ai-workflow-template/.codex-plugin/plugin.json` as a lightweight packaged wrapper that points back to the repo's shared `.agents/skills/` directory and `.mcp.json`.
- Verified JSON parsing for `.codex-plugin/plugin.json`, `.mcp.json`, `.agents/plugins/marketplace.json`, and `plugins/afa-ai-workflow-template/.codex-plugin/plugin.json`.
- Verified the packaged plugin resolves its `skills` path to `./.agents/skills/` and its `mcpServers` path to `./.mcp.json` successfully.

## 2026-05-27 — AFA Call Compliance Template Audit

- [x] Add a canonical AFA call requirements and compliance mapping file
- [x] Expand submission templates for eligibility, data access, model configuration, workflow autonomy, and human labor documentation
- [x] Remove example rows that could be mistaken for actual project records
- [x] Sync README, assistant instructions, LaTeX appendix prompts, skills, commands, and plugin metadata with the full call
- [x] Validate JSON metadata and scan the resulting diff

## Review

- Added `submission/call_requirements.md` with dates, organizers, ground rules, evaluation emphasis, and a final author checklist.
- Updated `submission/` templates so the start-date rule, new-project requirement, author caps, named-author labor rule, all-conversation transcript rule, human time log, and human-vs-AI line report are explicit.
- Updated README, `AGENTS.md`, `CLAUDE.md`, `SKILLS_USE_GUIDE.md`, LaTeX template notes, and plugin descriptions to match the AFA call and the current eleven-skill inventory.
