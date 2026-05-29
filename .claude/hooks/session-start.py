#!/usr/bin/env python3
"""SessionStart hook for AFA 2027 submission logging.

Records a session-start sentinel under submission/ so the SessionEnd hook can
compute duration. Skips silently if the AFA cutoff has not arrived, if the
opt-out file exists, or if the submission package has not been initialized.

Never blocks the session: always exits 0.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


AFA_CUTOFF = datetime(2026, 6, 1, tzinfo=timezone.utc).date()


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    session_id = str(data.get("session_id", "unknown"))
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))

    if datetime.now(timezone.utc).date() < AFA_CUTOFF:
        return

    if (project_dir / ".no-afa-logging").exists():
        return

    initial = project_dir / "submission" / "initial_prompt.md"
    if not initial.exists():
        return
    try:
        if "Paste the exact text of the initial prompt here" in initial.read_text(errors="ignore"):
            return
    except Exception:
        return

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
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
