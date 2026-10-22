#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/check_links.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Every relative link of every Markdown file must point at a file that exists. Prints LINKS=PASS or FAIL with the broken ones."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def main() -> int:
    broken = []
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        fenced = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if fenced:
                continue
            for target in LINK.findall(line):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if not (path.parent / target.split("#")[0]).exists():
                    broken.append(f"{path.relative_to(ROOT).as_posix()}:{number}: {target}")
    for item in broken:
        print("BROKEN", item)
    print("LINKS=" + ("FAIL" if broken else "PASS"))
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
