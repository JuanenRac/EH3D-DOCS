#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/bootstrap_workspace.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Lists, and with --clone fetches, the repositories that one repository of the suite needs next to it.

    python -I tools/bootstrap_workspace.py --workspace ~/eh3d EH3D-DRILLPRO            # lists what is there and what is missing; changes nothing
    python -I tools/bootstrap_workspace.py --workspace ~/eh3d EH3D-DRILLPRO --clone    # clones the missing ones (git clone --depth 1), one level after another

A repository needs a sibling when its files reach it by a path: a `path = "../EH3D-X"` of a `Cargo.toml` (in any folder of the repository), a `file:../EH3D-X` (or
`link:` / `portal:`) of a `package.json`, or a name in `depends_on` of its manifest. There is no list of repositories in this tool: the answer comes from the files
of the repository you start from, and then, recursively, from the files of each one it needs. A repository that is not on the disk cannot be read, so without --clone
its own needs are not known; with --clone it is fetched first and then read.

Nothing is deleted or overwritten: a folder that already exists is used as it is. The last line is BOOTSTRAP=PLAN (nothing was changed) or BOOTSTRAP=DONE.
Exit codes (docs/CONVENTIONS.md): 0 done, 1 a clone failed or the workspace does not exist, 2 the repository to start from is not there (nothing to read), 64 wrong use.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

DEFAULT_URL = "https://github.com/JuanenRac/{name}.git"
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SKIP_DIRS = {".git", "target", "node_modules", ".venv", "build", "dist", "__pycache__", ".gradle"}
CARGO_PATH = re.compile(r'\bpath\s*=\s*"([^"]+)"')
NPM_PATH = re.compile(r'"(?:file|link|portal):([^"]+)"')


class UsageParser(argparse.ArgumentParser):
    """An argument parser that ends a wrong use with exit code 64, as docs/CONVENTIONS.md says."""

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")


@dataclass
class Repo:
    name: str
    #: present (it was there), missing (it is not and nothing was fetched), cloned, failed (the clone did not work)
    status: str
    needed_by: str | None = None
    via: str | None = None
    detail: str = ""


@dataclass
class Plan:
    repos: list[Repo] = field(default_factory=list)

    def count(self, status: str) -> int:
        return sum(1 for r in self.repos if r.status == status)


def _files(repo: Path, names: tuple[str, ...]) -> list[Path]:
    """Every file with one of these names in the repository, leaving out the folders of builds and dependencies."""
    out: list[Path] = []
    for path in sorted(repo.rglob("*")):
        if path.name in names and path.is_file() and not any(part in SKIP_DIRS for part in path.relative_to(repo).parts[:-1]):
            out.append(path)
    return out


def _sibling(base: Path, reference: str, repo: Path, workspace: Path) -> str | None:
    """The folder of the workspace a relative path reaches from `base`, when it leaves the repository; None for a path that stays inside or leaves the workspace."""
    target = (base / reference).resolve()
    try:
        target.relative_to(repo.resolve())
        return None
    except ValueError:
        pass
    try:
        parts = target.relative_to(workspace.resolve()).parts
    except ValueError:
        return None
    return parts[0] if parts and NAME.match(parts[0]) else None


def needs_of(repo: Path, workspace: Path) -> dict[str, str]:
    """The siblings a repository on the disk needs, as {name: where it says so}."""
    found: dict[str, str] = {}
    for cargo in _files(repo, ("Cargo.toml",)):
        for match in CARGO_PATH.finditer(cargo.read_text(encoding="utf-8", errors="replace")):
            name = _sibling(cargo.parent, match.group(1), repo, workspace)
            if name and name != repo.name:
                found.setdefault(name, "Cargo.toml")
    for package in _files(repo, ("package.json",)):
        for match in NPM_PATH.finditer(package.read_text(encoding="utf-8", errors="replace")):
            name = _sibling(package.parent, match.group(1), repo, workspace)
            if name and name != repo.name:
                found.setdefault(name, "package.json")
    manifest = repo / "eh3d.project.json"
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except ValueError:
            data = {}
        for name in (data.get("depends_on") or []) if isinstance(data, dict) else []:
            if isinstance(name, str) and NAME.match(name) and name != repo.name:
                found.setdefault(name, "eh3d.project.json")
    return found


def bootstrap(workspace: Path, start: str, *, clone: bool = False, url_template: str = DEFAULT_URL,
              run: Callable[..., subprocess.CompletedProcess] = subprocess.run) -> Plan:
    """Walks the needs of `start` level by level. With `clone`, a repository that is not on the disk is fetched (git clone --depth 1) and then read."""
    plan = Plan()
    seen: set[str] = set()
    queue: list[tuple[str, str | None, str | None]] = [(start, None, None)]
    while queue:
        name, needed_by, via = queue.pop(0)
        if name in seen:
            continue
        seen.add(name)
        folder = workspace / name
        if folder.is_dir():
            plan.repos.append(Repo(name, "present", needed_by, via))
        elif not clone:
            plan.repos.append(Repo(name, "missing", needed_by, via, "its own needs are known only after it is cloned"))
            continue
        else:
            result = run(["git", "clone", "--depth", "1", "--quiet", url_template.format(name=name), str(folder)], capture_output=True, text=True, check=False)
            if result.returncode != 0:
                lines = (result.stderr or "").strip().splitlines()
                plan.repos.append(Repo(name, "failed", needed_by, via, lines[-1] if lines else f"git ended with {result.returncode}"))
                continue
            plan.repos.append(Repo(name, "cloned", needed_by, via))
        for dependency, source in needs_of(folder, workspace).items():
            if dependency not in seen:
                queue.append((dependency, name, source))
    return plan


def describe(repo: Repo, clone: bool) -> str:
    text = f"{repo.name:<28} {repo.status:<8}"
    if repo.needed_by:
        text += f" needed by {repo.needed_by} ({repo.via})"
    if repo.status == "missing" and not clone:
        text += "; with --clone it would be fetched"
    if repo.detail:
        text += f" - {repo.detail}"
    return text


def main(argv: list[str] | None = None) -> int:
    parser = UsageParser(description="Lists, and with --clone fetches, the repositories that one repository of the suite needs next to it.")
    parser.add_argument("repository", help="the repository to start from")
    parser.add_argument("--workspace", type=Path, required=True, help="the folder that holds (or will hold) the repositories")
    parser.add_argument("--clone", action="store_true", help="fetch the missing repositories with git clone --depth 1 (without it nothing is changed)")
    parser.add_argument("--dry-run", action="store_true", help="the default: list only; it cannot be combined with --clone")
    parser.add_argument("--url-template", default=DEFAULT_URL, help="where a repository is cloned from; {name} is replaced (default: %(default)s)")
    args = parser.parse_args(argv)
    if args.clone and args.dry_run:
        parser.error("--clone and --dry-run exclude each other")
    if not NAME.match(args.repository):
        parser.error(f"{args.repository!r} is not a repository name")
    if "{name}" not in args.url_template:
        parser.error("--url-template needs {name}")
    if not args.workspace.is_dir():
        if not args.clone:
            print(f"the workspace {args.workspace} does not exist", file=sys.stderr)
            return 1
        args.workspace.mkdir(parents=True, exist_ok=True)
    plan = bootstrap(args.workspace, args.repository, clone=args.clone, url_template=args.url_template)
    for repo in plan.repos:
        print(describe(repo, args.clone))
    print(f"BOOTSTRAP={'DONE' if args.clone else 'PLAN'} repos={len(plan.repos)} present={plan.count('present')} missing={plan.count('missing')} cloned={plan.count('cloned')} failed={plan.count('failed')}")
    if plan.count("failed"):
        return 1
    if plan.repos and plan.repos[0].status == "missing":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
