#!/usr/bin/env bash
# Quick check that Cursor wiring and core paths exist (for template users / CI).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
errors=0

check() {
  if [[ -e "$1" ]]; then
    echo "ok  $1"
  else
    echo "missing  $1" >&2
    errors=$((errors + 1))
  fi
}

check "${ROOT}/.agents/skills/init-submission/SKILL.md"
check "${ROOT}/.cursor/mcp.json"
check "${ROOT}/.cursor/rules/afa-workflow.mdc"
check "${ROOT}/latex_template/academic_paper_template.tex"
check "${ROOT}/submission/call_requirements.md"

for skill in init-submission research-idea-generator finance-idea-screening; do
  link="${ROOT}/.cursor/skills/${skill}"
  if [[ -L "${link}" && -f "${link}/SKILL.md" ]]; then
    echo "ok  .cursor/skills/${skill} (symlink)"
  else
    echo "warn  run: bash scripts/setup-cursor.sh  (missing .cursor/skills/${skill})" >&2
    errors=$((errors + 1))
  fi
done

if [[ -z "${CORBIS_MCP_API_KEY:-}" ]]; then
  echo "warn  CORBIS_MCP_API_KEY is not set (MCP will not auth until you export it)"
fi

if [[ "${errors}" -gt 0 ]]; then
  exit 1
fi
echo "verify-setup: passed"
