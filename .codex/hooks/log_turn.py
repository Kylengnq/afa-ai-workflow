#!/usr/bin/env python3
"""Codex Stop hook for AFA 2027 transcript logging."""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


AFA_CUTOFF = datetime(2026, 6, 1, tzinfo=timezone.utc).date()
MAX_TOOL_RENDER = 2000


def load_input() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def project_root(cwd: str | None) -> Path:
    base = Path(cwd or ".").resolve()
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=base,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        return Path(root)
    except Exception:
        return base


def initialized(project_dir: Path) -> bool:
    if datetime.now(timezone.utc).date() < AFA_CUTOFF:
        return False
    if (project_dir / ".no-afa-logging").exists():
        return False

    initial = project_dir / "submission" / "initial_prompt.md"
    if not initial.exists():
        return False

    try:
        text = initial.read_text(errors="ignore")
    except Exception:
        return False
    return "Paste the exact text of the initial prompt here" not in text


def load_events(transcript_path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    try:
        with transcript_path.open() as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        return []
    return events


def extract_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return str(content.get("text") or content.get("input_text") or "")
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text") or item.get("input_text")
                if text:
                    parts.append(str(text))
            else:
                parts.append(str(item))
        return "\n\n".join(parts)
    return ""


def truncate(value: str) -> str:
    if len(value) <= MAX_TOOL_RENDER:
        return value
    return value[:MAX_TOOL_RENDER] + "\n...[truncated]"


def pretty_json_or_text(value: Any) -> str:
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return json.dumps(parsed, indent=2)
        except Exception:
            return value
    try:
        return json.dumps(value, indent=2)
    except Exception:
        return str(value)


def render_events(events: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for event in events:
        if event.get("type") != "response_item":
            continue

        payload = event.get("payload", {})
        ptype = payload.get("type")
        if ptype == "message":
            role = payload.get("role")
            if role not in {"user", "assistant"}:
                continue
            title = "User" if role == "user" else "Assistant"
            text = extract_text(payload.get("content", ""))
            if text.strip():
                lines.extend([f"## {title}", "", text, ""])
        elif ptype == "function_call":
            name = str(payload.get("name", "?"))
            args = truncate(pretty_json_or_text(payload.get("arguments", "")))
            lines.extend(
                [
                    f"<details><summary>Tool: {name}</summary>",
                    "",
                    "```json",
                    args,
                    "```",
                    "</details>",
                    "",
                ]
            )
        elif ptype == "function_call_output":
            output = truncate(str(payload.get("output", "")))
            call_id = str(payload.get("call_id", "?"))[:12]
            lines.extend(
                [
                    f"<details><summary>Tool result ({call_id})</summary>",
                    "",
                    "```text",
                    output,
                    "```",
                    "</details>",
                    "",
                ]
            )
    return lines


def first_user_slug(events: list[dict[str, Any]]) -> str:
    for event in events:
        payload = event.get("payload", {})
        if event.get("type") == "response_item" and payload.get("type") == "message":
            if payload.get("role") == "user":
                text = extract_text(payload.get("content", ""))
                candidate = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()[:40]
                if candidate:
                    return candidate
    return "session"


def session_meta(events: list[dict[str, Any]]) -> dict[str, Any]:
    for event in events:
        if event.get("type") == "session_meta":
            payload = event.get("payload", {})
            if isinstance(payload, dict):
                return payload
    return {}


def sentinel_start(project_dir: Path, session_id: str) -> str | None:
    sentinel = project_dir / "submission" / f".session-{session_id[:8]}.start"
    if not sentinel.exists():
        return None
    try:
        for line in sentinel.read_text().splitlines():
            if line.startswith("start_ts="):
                return line.split("=", 1)[1].strip()
    except Exception:
        return None
    return None


def scrub_credentials(text: str) -> str:
    text = re.sub(r"corbis_mcp_[A-Za-z0-9_-]+", "corbis_mcp_REDACTED", text)
    text = re.sub(r"\bsk-[A-Za-z0-9_\-]{20,}", "sk-REDACTED", text)
    text = re.sub(r"\bBearer\s+[A-Za-z0-9_.\-]+", "Bearer REDACTED", text)
    text = re.sub(r"\bAKIA[0-9A-Z]{16}\b", "AWS_KEY_REDACTED", text)
    return text


def main() -> None:
    data = load_input()
    project_dir = project_root(data.get("cwd"))
    if not initialized(project_dir):
        return

    transcript = data.get("transcript_path")
    if not transcript or not Path(transcript).exists():
        return

    events = load_events(Path(transcript))
    if not events:
        return

    session_id = str(data.get("session_id") or session_meta(events).get("id") or "unknown")
    start_ts = sentinel_start(project_dir, session_id)
    meta = session_meta(events)
    if not start_ts:
        start_ts = str(meta.get("timestamp") or events[0].get("timestamp") or "unknown")

    try:
        dt = datetime.fromisoformat(start_ts.replace("Z", "+00:00"))
        file_ts = dt.strftime("%Y-%m-%d_%H%M")
    except Exception:
        file_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")

    body = render_events(events)
    if not body:
        return

    conv_dir = project_dir / "submission" / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)
    slug = first_user_slug(events)
    out_path = conv_dir / f"{file_ts}_{session_id[:8]}_{slug}.md"

    model = str(data.get("model") or meta.get("model") or meta.get("model_provider") or "codex")
    lines = [
        "---",
        f"session_id: {session_id}",
        f"started: {start_ts}",
        f"last_updated: {datetime.now(timezone.utc).isoformat()}",
        f"model: {model}",
        f"transcript_source: {transcript}",
        "auto_logged: true",
        "client: codex",
        "---",
        "",
        "# Conversation transcript",
        "",
        "Auto-generated by `.codex/hooks/log_turn.py` from the Codex transcript.",
        "Review before submission. Trivial sessions can be deleted.",
        "",
    ]
    lines.extend(body)
    out_path.write_text(scrub_credentials("\n".join(lines)))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
