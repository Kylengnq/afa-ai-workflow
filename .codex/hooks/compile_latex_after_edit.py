#!/usr/bin/env python3
"""Compile root LaTeX files touched by Codex edit hooks."""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


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


def walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        for child in value.values():
            out.extend(walk_strings(child))
        return out
    if isinstance(value, list):
        out: list[str] = []
        for child in value:
            out.extend(walk_strings(child))
        return out
    return []


def touched_tex_files(data: dict, root: Path) -> list[Path]:
    candidates: set[Path] = set()
    tool_input = data.get("tool_input", {})

    command = ""
    if isinstance(tool_input, dict):
        command = str(tool_input.get("command", ""))
    if command:
        for match in re.finditer(r"^\*\*\* (?:Add|Update) File: (.+\.tex)\s*$", command, re.M):
            candidates.add((root / match.group(1)).resolve())

    for value in walk_strings(tool_input):
        if value.endswith(".tex") and "\n" not in value:
            candidates.add((root / value).resolve())

    return sorted(path for path in candidates if path.exists() and root in path.parents)


def compile_tex(path: Path) -> None:
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return
    if "\\documentclass" not in text:
        return
    if not shutil.which("pdflatex"):
        return

    base = path.stem
    cwd = path.parent
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", base],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if shutil.which("bibtex") and (cwd / f"{base}.aux").exists():
        subprocess.run(
            ["bibtex", base],
            cwd=cwd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    for _ in range(2):
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", base],
            cwd=cwd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )


def main() -> None:
    data = load_input()
    root = project_root(data.get("cwd"))
    for path in touched_tex_files(data, root):
        compile_tex(path)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
