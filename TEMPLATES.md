# Templates Index

Quick map of scaffolds in this repo. Copy or let skills fill them in; do not
edit the originals in place.

## Paper and submission

| Template | Path | Use |
|----------|------|-----|
| LaTeX article + AFA appendices A–D | `latex_template/academic_paper_template.tex` | Copy to `paper/` with `latex_template/template_references.bib` |
| Submission call checklist | `submission/call_requirements.md` | Compliance map (fill during `/init-submission`) |
| Initial prompt, model config, data access | `submission/initial_prompt.md`, `model_config.md`, `data_access.md` | Populated by `init-submission` |
| Conversation index | `submission/conversations/README.md` | One transcript per AI session |

## Skill output scaffolds

| Template | Path | Produced by |
|----------|------|-------------|
| Idea menu | `.agents/skills/research-idea-generator/assets/idea-menu-template.md` | `/brainstorm` (`research-idea-generator`) |
| Idea card + gates | `.agents/skills/finance-idea-screening/assets/idea-card-template.md` | `/idea` (`finance-idea-screening`) |
| Literature positioning matrix | `.agents/skills/literature-positioning-map/assets/literature-matrix-template.md` | `/lit-search` |
| Reading list | `.agents/skills/literature-review/assets/reading-list-template.md` | `/lit-review` |

Claude Code uses duplicate copies under `.claude/skills/.../assets/`; Codex and
Cursor use `.agents/skills/.../assets/` as canonical.

## Shared data (created by skills, not shipped empty)

| File | Role |
|------|------|
| `output/paper_set.json` | Deduplicated Corbis paper cache across skills |
| `output/search_log.md` | Transparency log of every search query |
| `references/top_journal_calibration.json` | Held-out JF/JFE/RFS anchor from `/calibrate-rubric` |
| `ideas/<date>_<slug>/` | Per-idea lineage from `/idea` |

## Cursor / Codex discovery

- **Cursor:** run `bash scripts/setup-cursor.sh` then open the repo; skills appear under `.cursor/skills/`.
- **Codex:** skills at `.agents/skills/` via `.codex-plugin/plugin.json`.
- **Claude Code:** `/plugin install ./` or `.claude/skills/` + `.claude/commands/`.
