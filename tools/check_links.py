#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/check_links.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Every relative link of every Markdown file must point at a file that exists. Prints LINKS=PASS or FAIL with the broken ones.
Inline links, reference definitions (`[a]: x.md`) and links with a title, a query or `%20` are read; fenced blocks (``` and ~~~) and `code spans` are not."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\)")
REFERENCE = re.compile(r"^ {0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*$")
CODE_SPAN = re.compile(r"(`+)(?:(?!\1).)+?\1")
SKIP_FOLDERS = {".git", ".venv", "venv", "node_modules", "target", "build", "dist", "__pycache__"}


def exists_exactly(base: Path, target: str) -> bool:
    """The target exists with the exact case of every part (Windows would accept `readme.md`, the Linux CI would not). An absolute link (`/docs/x.md`) is read from the root of the repository."""
    clean = unquote(target.split("#")[0].split("?")[0])
    if not clean:
        return True
    start = ROOT if clean.startswith("/") else base
    current = start
    for part in [p for p in clean.replace("\\", "/").split("/") if p]:
        if part == ".":
            continue
        if part == "..":
            current = current.parent
            continue
        try:
            names = os.listdir(current)
        except OSError:
            return False
        if part not in names:
            return False
        current = current / part
    return current.exists()


def markdown_files() -> list[Path]:
    """Every Markdown file below the root; the build and tool folders are not entered at all."""
    found: list[Path] = []
    for folder, dirs, names in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_FOLDERS)
        found.extend(Path(folder) / name for name in names if name.endswith(".md"))
    return sorted(found)


def targets_in(line: str) -> list[str]:
    """The link targets of one line: the inline ones `[a](x.md)` outside a `code span`, and a reference definition `[a]: x.md`."""
    reference = REFERENCE.match(line)
    if reference:
        return [reference.group(1)]
    return LINK.findall(CODE_SPAN.sub("", line))


def main() -> int:
    broken = []
    for path in markdown_files():
        fenced = False
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith(("```", "~~~")):
                fenced = not fenced
                continue
            if fenced:
                continue
            for target in targets_in(line):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if not exists_exactly(path.parent, target):
                    broken.append(f"{path.relative_to(ROOT).as_posix()}:{number}: {target}")
    for item in broken:
        print("BROKEN", item)
    print("LINKS=" + ("FAIL" if broken else "PASS"))
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
