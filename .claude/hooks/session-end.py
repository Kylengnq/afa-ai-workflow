#!/usr/bin/env python3
"""SessionEnd hook for AFA 2027 submission logging.

Closes out a session: reads the start sentinel, computes duration, appends a
row to submission/human_time_log.md (flagged for human review), updates the
conversation index, and removes the sentinel.

Never blocks the session: always exits 0.
"""

import json
import os
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

    sentinel = project_dir / "submission" / f".session-{session_id[:8]}.start"
    if not sentinel.exists():
        return

    start_ts: str | None = None
    for line in sentinel.read_text().splitlines():
        if line.startswith("start_ts="):
            start_ts = line.split("=", 1)[1].strip()

    if not start_ts:
        try:
            sentinel.unlink()
        except Exception:
            pass
        return

    try:
        start_dt = datetime.fromisoformat(start_ts.replace("Z", "+00:00"))
    except Exception:
        try:
            sentinel.unlink()
        except Exception:
            pass
        return

    end_dt = datetime.now(timezone.utc)
    duration_min = max(0, int((end_dt - start_dt).total_seconds() / 60))
    h, m = divmod(duration_min, 60)
    duration_str = f"{h}h {m:02d}m"

    date_str = start_dt.strftime("%Y-%m-%d")
    start_hm = start_dt.strftime("%H:%M")
    end_hm = end_dt.strftime("%H:%M")

    conv_dir = project_dir / "submission" / "conversations"
    conv_files = sorted(conv_dir.glob(f"*_{session_id[:8]}_*.md")) if conv_dir.exists() else []
    conv_rel = ""
    conv_name = ""
    if conv_files:
        conv_rel = f"submission/conversations/{conv_files[-1].name}"
        conv_name = conv_files[-1].name

    # Append to human time log, marked auto-review
    log = project_dir / "submission" / "human_time_log.md"
    if log.exists():
        row = (
            f"| {date_str} | {start_hm} | {end_hm} | {duration_str} | "
            f"auto-review | meta | session via Claude Code (auto, reclassify before submission) | "
            f"{conv_rel} |"
        )
        try:
            text = log.read_text()
            if "## Running totals" in text:
                text = text.replace(
                    "## Running totals",
                    row + "\n\n## Running totals",
                    1,
                )
            else:
                text = text.rstrip() + "\n" + row + "\n"
            log.write_text(text)
        except Exception:
            pass

    # Append to conversations index
    index = conv_dir / "README.md" if conv_dir.exists() else None
    if index and index.exists() and conv_name:
        row = f"| {conv_name} | {date_str} | meta | claude-code | (auto) session {duration_str} |"
        try:
            with open(index, "a") as f:
                f.write(row + "\n")
        except Exception:
            pass

    try:
        sentinel.unlink()
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
