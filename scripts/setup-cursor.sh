#!/usr/bin/env bash
# Wire .cursor/ to the canonical .agents/skills and MCP config for this template.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="${ROOT}/.agents/skills"
SKILLS_DST="${ROOT}/.cursor/skills"

mkdir -p "${SKILLS_DST}"

if [[ ! -d "${SKILLS_SRC}" ]]; then
  echo "error: missing ${SKILLS_SRC}" >&2
  exit 1
fi

linked=0
for skill_dir in "${SKILLS_SRC}"/*/; do
  name="$(basename "${skill_dir}")"
  target="${SKILLS_DST}/${name}"
  if [[ -L "${target}" || -e "${target}" ]]; then
    continue
  fi
  ln -s "../../.agents/skills/${name}" "${target}"
  linked=$((linked + 1))
done

MCP_DST="${ROOT}/.cursor/mcp.json"
if [[ ! -f "${MCP_DST}" ]]; then
  cp "${ROOT}/.mcp.json" "${MCP_DST}"
  echo "created ${MCP_DST} from .mcp.json"
fi

echo "Cursor setup: ${linked} skill symlink(s) in .cursor/skills/"
echo "Next: export CORBIS_MCP_API_KEY and reload MCP in Cursor (see CORBIS_MCP_CURSOR_GUIDE.md)"
