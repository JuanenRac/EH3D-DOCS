#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/readme_staleness.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Which sections of a translated README are older than the same section of the English one. Informative only.

    python tools/readme_staleness.py [REPOSITORY ...] [--workspace FOLDER] [--all] [--grace-hours N]

The eight README files have the same sections in the same order (the validator checks the structure), but a section can have
been rewritten in English and not yet in another language. For each section (a `## ` heading and what follows it) the script
asks `git blame` when its newest line was written; when the English section is newer than the same section of another
language by more than the grace (24 hours by default, so that translations committed a little later do not count), it says so.
It never fails: the exit code is 0 whatever it finds, and it prints nothing for a repository whose git history it cannot read.
Without a repository it looks at this one; --all looks at every EH3D repository next to it."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import version_places as vp  # noqa: E402

HUB = Path(__file__).resolve().parents[1]


def blame_times(root: Path, name: str) -> list[tuple[str, int]] | None:
    """[(text of the line, author time)] of a file in the order of the file, or None when git cannot blame it."""
    try:
        done = subprocess.run(["git", "blame", "--line-porcelain", "-w", "--", name], cwd=root, capture_output=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if done.returncode != 0:
        return None
    lines, current = [], int(time.time())
    for raw in done.stdout.decode("utf-8", "replace").split("\n"):
        if raw.startswith("author-time "):
            current = int(raw.split()[1])
        elif raw.startswith("\t"):
            lines.append((raw[1:], current))
    return lines


def split_sections(lines: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """[(heading, newest time)] of the part before the first `## ` (heading "") and of each `## ` section, fences respected."""
    out: list[list] = [["", 0]]
    fenced = False
    for text, stamp in lines:
        if text.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and text.startswith("## "):
            out.append([text[3:].strip(), 0])
        out[-1][1] = max(out[-1][1], stamp)
    return [(heading, stamp) for heading, stamp in out]


def staleness(root: Path, grace_seconds: int = 24 * 3600) -> tuple[list[str], list[str]]:
    """(findings, notes): one finding per section of a translation that is older than the English one."""
    english = blame_times(root, "README.md")
    if english is None:
        return [], ["no git history to read"]
    base = split_sections(english)
    findings, notes = [], []
    for name in vp.READMES[1:]:
        other = blame_times(root, name)
        if other is None:
            notes.append(f"{name}: no git history")
            continue
        sections = split_sections(other)
        if len(sections) != len(base):
            notes.append(f"{name}: {len(sections)} sections against {len(base)} in README.md, so they cannot be compared")
            continue
        for (heading, stamp_en), (_, stamp) in zip(base, sections):
            if stamp_en - stamp > grace_seconds:
                days = (stamp_en - stamp) / 86400
                findings.append(f"{name}: the section '{heading or 'top of the file'}' is {days:.0f} days older than the English one" if days >= 1 else f"{name}: the section '{heading or 'top of the file'}' is older than the English one")
    return findings, notes


def repositories(args: argparse.Namespace) -> list[Path]:
    base = args.workspace or HUB.parent
    if args.all:
        return [p for p in sorted(base.glob("EH3D-*")) if (p / vp.MANIFEST).is_file()]
    if not args.repository:
        return [HUB]
    return [Path(r) if (Path(r) / vp.MANIFEST).is_file() else base / r for r in args.repository]


class UsageParser(argparse.ArgumentParser):
    """An argument parser that ends a wrong use with exit code 64, as docs/CONVENTIONS.md says for the command-line tools of the suite (argparse alone uses 2)."""

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = UsageParser(description="Sections of the translated README files that are older than the English ones (informative).")
    parser.add_argument("repository", nargs="*")
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--all", action="store_true", help="every EH3D repository of the workspace")
    parser.add_argument("--grace-hours", type=float, default=24.0)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    total = 0
    for root in repositories(args):
        findings, notes = staleness(root, int(args.grace_hours * 3600))
        total += len(findings)
        for line in findings:
            print(f"INFO {root.name}: {line}")
        for line in notes:
            print(f"NOTE {root.name}: {line}")
    print(f"README_STALENESS sections={total} (informative: it never fails)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
