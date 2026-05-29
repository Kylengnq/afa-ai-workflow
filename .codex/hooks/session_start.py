#!/usr/bin/env python3
"""Codex SessionStart hook for AFA 2027 submission logging."""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


AFA_CUTOFF = datetime(2026, 6, 1, tzinfo=timezone.utc).date()


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


def main() -> None:
    data = load_input()
    project_dir = project_root(data.get("cwd"))
    if not initialized(project_dir):
        return

    session_id = str(data.get("session_id", "unknown"))
    sentinel = project_dir / "submission" / f".session-{session_id[:8]}.start"
    sentinel.parent.mkdir(parents=True, exist_ok=True)

    git_head = "none"
    try:
        git_head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=project_dir,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        pass

    sentinel.write_text(
        f"session_id={session_id}\n"
        f"start_ts={datetime.now(timezone.utc).isoformat()}\n"
        f"git_head={git_head}\n"
        "client=codex\n"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
