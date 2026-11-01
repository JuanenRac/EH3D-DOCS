#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/sync_shared_tools.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Tells which repositories of the suite have a copy of a shared tool that is not the one of EH3D-DOCS.

The checkers and the drawers of the pictures are copied into every repository (each one has to run alone in its own CI), so a change made in one copy stays in that one
unless somebody carries it to the others. This tool compares the copies, ignoring the comment block at the top of each file (it has the name of the repository), and
says how many different versions there are and who holds which.

    python tools/sync_shared_tools.py                  # the report: for each tool, the repositories that differ from the one of EH3D-DOCS
    python tools/sync_shared_tools.py --check          # the same, and exit 1 when any copy differs
    python tools/sync_shared_tools.py --write --only ci_validate.py --repo EH3D-ISOCAM
                                                       # puts the canonical copy in that repository (its own header stays); never done without --repo
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANONICAL = "EH3D-DOCS"
SHARED = (
    "ci_validate.py",
    "status_lights.py",
    "make_structure.py",
    "make_architecture.py",
    "_readme_svg.py",
    "universal_readme_check.py",
    "pretty_run.py",
    "_manifest_contract.py",
)


def split_header(text: str) -> tuple[str, str]:
    """The text of a file as (header, body): the header is the block of comment lines at the top (after a `#!` line), which names the repository."""
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines) and (lines[i].startswith("#")):
        i += 1
    return "\n".join(lines[:i]), "\n".join(lines[i:])


def digest(path: Path) -> str:
    return hashlib.sha256(split_header(path.read_text(encoding="utf-8"))[1].encode("utf-8")).hexdigest()[:10]


def repos(workspace: Path) -> list[Path]:
    return sorted(p for p in workspace.iterdir() if p.is_dir() and (p.name.startswith("EH3D-") or p.name == "ELECTRO-HOBBY-3D-UPDATER") and (p / "tools").is_dir())


def report(workspace: Path, only: str | None = None) -> dict[str, dict[str, list[str]]]:
    """For each shared tool: the variants (digest of the body) and the repositories that hold each one."""
    out: dict[str, dict[str, list[str]]] = {}
    for tool in SHARED:
        if only and tool != only:
            continue
        variants: dict[str, list[str]] = {}
        for repo in repos(workspace):
            f = repo / "tools" / tool
            if f.is_file():
                variants.setdefault(digest(f), []).append(repo.name)
        if variants:
            out[tool] = variants
    return out


def differing(workspace: Path, only: str | None = None) -> dict[str, list[str]]:
    """For each tool: the repositories whose copy is not the one of EH3D-DOCS (a repository that has none is not listed)."""
    result: dict[str, list[str]] = {}
    for tool, variants in report(workspace, only).items():
        canon = next((d for d, names in variants.items() if CANONICAL in names), None)
        if canon is None:
            continue
        others = sorted(n for d, names in variants.items() if d != canon for n in names)
        if others:
            result[tool] = others
    return result


CANONICAL_LINE = "# canonical: "


def canonical_line(head: str) -> str | None:
    """The `# canonical: EH3D-DOCS tools N` line of a header, or None."""
    return next((line for line in head.replace("\r\n", "\n").split("\n") if line.startswith(CANONICAL_LINE)), None)


def with_canonical_line(head: str, line: str | None) -> str:
    """The header with its `# canonical:` line replaced by `line` (added at the end of the header when it had none); unchanged when `line` is None."""
    if line is None:
        return head
    lines = [item for item in head.replace("\r\n", "\n").split("\n") if not item.startswith(CANONICAL_LINE)]
    return "\n".join(lines + [line])


def canonical_problems(workspace: Path) -> list[str]:
    """The copies of ci_validate.py whose header does not state the tools version of EH3D-DOCS (a repository that has not been synchronised yet)."""
    wanted = canonical_line(split_header((workspace / CANONICAL / "tools" / "ci_validate.py").read_text(encoding="utf-8"))[0])
    out = []
    for repo in repos(workspace):
        path = repo / "tools" / "ci_validate.py"
        if path.is_file() and repo.name != CANONICAL:
            stated = canonical_line(split_header(path.read_text(encoding="utf-8"))[0])
            if stated != wanted:
                out.append(f"{repo.name}: ci_validate.py declares {stated.split('tools ')[-1] if stated else 'no canonical version'}, the suite is at {wanted.split('tools ')[-1] if wanted else '?'}")
    return out


def write_copy(workspace: Path, tool: str, repo: str) -> None:
    """Puts the body of the canonical copy in the file of a repository, whose header (its own name) stays."""
    src = workspace / CANONICAL / "tools" / tool
    dst = workspace / repo / "tools" / tool
    if not src.is_file() or not dst.is_file():
        raise SystemExit(f"{tool}: there is no copy to write in {repo} or no canonical one")
    raw = dst.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    head, _ = split_header(raw)
    src_head, body = split_header(src.read_text(encoding="utf-8"))
    head = with_canonical_line(head, canonical_line(src_head))
    text = head + "\n" + body
    dst.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Compares the copies of the shared tools of the repositories.")
    p.add_argument("--workspace", type=Path, default=HERE.parents[1], help="the folder that holds the repositories (default: the one that holds this one)")
    p.add_argument("--only", choices=SHARED, help="one tool")
    p.add_argument("--check", action="store_true", help="exit 1 when any copy differs from the one of EH3D-DOCS")
    p.add_argument("--write", action="store_true", help="put the canonical copy in the repository given with --repo")
    p.add_argument("--repo", help="with --write: the repository to write")
    a = p.parse_args(argv)
    if a.write:
        if not (a.only and a.repo):
            print("--write needs --only TOOL and --repo REPOSITORY: it never rewrites the whole suite at once", file=sys.stderr)
            return 2
        write_copy(a.workspace, a.only, a.repo)
        print(f"{a.only}: written in {a.repo}")
        return 0
    diff = differing(a.workspace, a.only)
    for tool, variants in report(a.workspace, a.only).items():
        print(f"{tool}: {len(variants)} version(s) in {sum(len(v) for v in variants.values())} repositories")
        for names in sorted(variants.values(), key=len, reverse=True):
            mark = "canonical" if CANONICAL in names else "same" if len(variants) == 1 else "differs"
            shown = ", ".join(names[:6]) + (f" (+{len(names) - 6})" if len(names) > 6 else "")
            print(f"    {mark:<9} {shown}")
    total = sum(len(v) for v in diff.values())
    print(f"SHARED_TOOLS={'FAIL' if diff and a.check else 'REPORT'} tools={len(report(a.workspace, a.only))} differing_copies={total}")
    return 1 if diff and a.check else 0


if __name__ == "__main__":
    sys.exit(main())
