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
    python tools/sync_shared_tools.py --lock           # writes docs/vendored.lock: the origin and the digest of every shared tool, as this hub holds them
    python tools/sync_shared_tools.py --check          # also fails when docs/vendored.lock does not describe the canonical copies
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
    "banner_check.py",
    "changelog_pr_check.py",
    "pretty_run.py",
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
            if f.is_file() and (repo.name, tool) not in OWN_COPIES:
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


#: Copies a repository keeps on purpose (its own lineage, with checks of its own): they are neither compared nor written.
OWN_COPIES = {("ELECTRO-HOBBY-3D-UPDATER", "ci_validate.py")}

LOCK_NAME = "vendored.lock"


def lock_path(workspace: Path) -> Path:
    return workspace / CANONICAL / "docs" / LOCK_NAME


def lock_data(workspace: Path) -> dict:
    """What docs/vendored.lock must say: where the shared tools come from and the digest of the body of each canonical copy."""
    tools = {}
    for tool in SHARED:
        f = workspace / CANONICAL / "tools" / tool
        if f.is_file():
            tools[tool] = digest(f)
    return {"origin": CANONICAL, "tools": tools}


def lock_problems(workspace: Path) -> list[str]:
    """The reasons the lock does not describe the canonical copies: missing, unreadable, another origin, or a tool changed without writing the lock again."""
    path = lock_path(workspace)
    if not path.is_file():
        return [f"docs/{LOCK_NAME} is missing: run tools/sync_shared_tools.py --lock"]
    try:
        stored = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return [f"docs/{LOCK_NAME} is not valid JSON"]
    if not isinstance(stored, dict):
        return [f"docs/{LOCK_NAME} must hold a JSON object"]
    wanted = lock_data(workspace)
    out = []
    if stored.get("origin") != wanted["origin"]:
        out.append(f"docs/{LOCK_NAME} names the origin {stored.get('origin')!r}, the origin is {wanted['origin']!r}")
    have = stored.get("tools", {})
    if not isinstance(have, dict):
        return [f"docs/{LOCK_NAME}: 'tools' must be an object"]
    for tool, value in wanted["tools"].items():
        if have.get(tool) != value:
            out.append(f"{tool} changed since docs/{LOCK_NAME} was written: run tools/sync_shared_tools.py --lock")
    for tool in have:
        if tool not in wanted["tools"]:
            out.append(f"docs/{LOCK_NAME} lists {tool}, which this hub does not hold")
    return out


def missing_canonical(workspace: Path) -> list[str]:
    """The shared tools of which this hub holds no canonical copy: a drift that nothing could ever detect."""
    return [f"{tool} is listed as shared but {CANONICAL} holds no canonical copy of it" for tool in SHARED if not (workspace / CANONICAL / "tools" / tool).is_file()]


def write_lock(workspace: Path) -> None:
    lock_path(workspace).parent.mkdir(parents=True, exist_ok=True)
    lock_path(workspace).write_text(json.dumps(lock_data(workspace), indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
        if path.is_file() and repo.name != CANONICAL and (repo.name, "ci_validate.py") not in OWN_COPIES:
            stated = canonical_line(split_header(path.read_text(encoding="utf-8"))[0])
            if stated != wanted:
                out.append(f"{repo.name}: ci_validate.py declares {stated.split('tools ')[-1] if stated else 'no canonical version'}, the suite is at {wanted.split('tools ')[-1] if wanted else '?'}")
    return out


def write_copy(workspace: Path, tool: str, repo: str) -> None:
    """Puts the body of the canonical copy in the file of a repository, whose header (its own name) stays."""
    src = workspace / CANONICAL / "tools" / tool
    dst = workspace / repo / "tools" / tool
    if repo != Path(repo).name or repo in ("", ".", "..") or not (repo.startswith("EH3D-") or repo == "ELECTRO-HOBBY-3D-UPDATER"):
        raise SystemExit(f"{repo}: not the name of a repository of the suite")
    if (repo, tool) in OWN_COPIES:
        raise SystemExit(f"{tool} in {repo} is a copy that the repository keeps on purpose")
    if not src.is_file() or not dst.is_file():
        raise SystemExit(f"{tool}: there is no copy to write in {repo} or no canonical one")
    raw = dst.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    head, _ = split_header(raw)
    src_head, body = split_header(src.read_text(encoding="utf-8"))
    head = with_canonical_line(head, canonical_line(src_head))
    text = head + "\n" + body
    dst.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


class UsageParser(argparse.ArgumentParser):
    """An argument parser that ends a wrong use with exit code 64, as docs/CONVENTIONS.md says for the command-line tools of the suite (argparse alone uses 2)."""

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    p = UsageParser(description="Compares the copies of the shared tools of the repositories.")
    p.add_argument("--workspace", type=Path, default=HERE.parents[1], help="the folder that holds the repositories (default: the one that holds this one)")
    p.add_argument("--only", choices=SHARED, help="one tool")
    p.add_argument("--check", action="store_true", help="exit 1 when any copy differs from the one of EH3D-DOCS")
    p.add_argument("--write", action="store_true", help="put the canonical copy in the repository given with --repo")
    p.add_argument("--lock", action="store_true", help="write docs/vendored.lock from the canonical copies")
    p.add_argument("--repo", help="with --write: the repository to write")
    a = p.parse_args(argv)
    if a.write:
        if not (a.only and a.repo):
            print("--write needs --only TOOL and --repo REPOSITORY: it never rewrites the whole suite at once", file=sys.stderr)
            return 64
        write_copy(a.workspace, a.only, a.repo)
        print(f"{a.only}: written in {a.repo}")
        return 0
    if a.lock:
        write_lock(a.workspace)
        print(f"docs/{LOCK_NAME}: written")
        return 0
    diff = differing(a.workspace, a.only)
    lock = (lock_problems(a.workspace) + missing_canonical(a.workspace)) if not a.only else []
    for line in lock:
        print("  LOCK", line)
    for tool, variants in report(a.workspace, a.only).items():
        print(f"{tool}: {len(variants)} version(s) in {sum(len(v) for v in variants.values())} repositories")
        for names in sorted(variants.values(), key=len, reverse=True):
            mark = "canonical" if CANONICAL in names else "same" if len(variants) == 1 else "differs"
            shown = ", ".join(names[:6]) + (f" (+{len(names) - 6})" if len(names) > 6 else "")
            print(f"    {mark:<9} {shown}")
    total = sum(len(v) for v in diff.values())
    failing = bool(diff or lock) and a.check
    print(f"SHARED_TOOLS={'FAIL' if failing else 'REPORT'} tools={len(report(a.workspace, a.only))} differing_copies={total} lock={'STALE' if lock else 'OK'}")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
