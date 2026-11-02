#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/bump_version.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Raise the version of a repository of the suite in every place that holds it.

    python tools/bump_version.py REPOSITORY NEW "Title of the version" [--workspace FOLDER] [--dry-run] [--explicit] [--fix-drift]

REPOSITORY is a folder name next to this repository (or a path). NEW is the version the odometer gives (0.0.9 -> 0.1.0,
0.7.9 -> 0.8.0.0; every number goes from 0 to 9 and carries to the one before) or the word `next`; any other version needs
--explicit. The places: the manifest, Cargo.toml and Cargo.lock, package.json and package-lock.json, pyproject.toml and the
`__version__` mirror, versionName (and versionCode + 1) of the Android Gradle files, MARKETING_VERSION (and
CURRENT_PROJECT_VERSION + 1) of project.yml, the file named by native_version, the badge and the table of the eight README
files, and CHANGELOG.md, whose [Unreleased] entries become the section of the new version.

Nothing is written unless every place can be changed; at the end the script reads the files again and fails if any place
differs from the manifest. --dry-run writes nothing and shows what would change. The line ends (CRLF or LF) of each file are kept."""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import changelog_tools  # noqa: E402
import version_places as vp  # noqa: E402

HUB = Path(__file__).resolve().parents[1]


def resolve(repository: str, workspace: Path | None) -> Path:
    candidate = Path(repository)
    if (candidate / vp.MANIFEST).is_file():
        return candidate.resolve()
    base = workspace or HUB.parent
    return (base / repository).resolve()


def bump(root: Path, new: str, title: str, explicit: bool = False, dry_run: bool = False, fix_drift: bool = False) -> tuple[int, list[str]]:
    """Returns (exit code, the lines to print)."""
    out: list[str] = []
    repo = vp.Repo(root)
    try:
        old = vp.manifest_version(repo)
        new = vp.next_version(old) if new == "next" else new
        vp.check_digits(new)
        if vp.compare(new, old) <= 0:
            return 1, [f"FAIL {new} is not greater than the version {old} of the manifest"]
        if not explicit:
            expected = vp.next_version(old)
            if new != expected:
                return 1, [f"FAIL the odometer gives {expected} after {old}, not {new} (use --explicit to jump)"]
        problems, _ = vp.apply(repo, old, new, fix_drift)
        if problems:
            return 1, [f"FAIL {p}" for p in problems]
        changelog = repo.read("CHANGELOG.md")
        if changelog is None:
            return 1, ["FAIL CHANGELOG.md is missing"]
        repo.write("CHANGELOG.md", changelog_tools.promote(changelog, new, title))
        problems = vp.check(repo, new)
    except (vp.VersionError, changelog_tools.ChangelogError) as error:
        return 1, [f"FAIL {error}"]
    if problems:
        return 1, [f"FAIL after the change: {p}" for p in problems]
    changed = repo.changed()
    if dry_run:
        for rel in changed:
            before = (repo.original(rel) or "").splitlines()
            after = (repo.read(rel) or "").splitlines()
            out.extend(line.rstrip("\n") for line in difflib.unified_diff(before, after, f"a/{rel}", f"b/{rel}", n=0, lineterm=""))
        out.append(f"DRY-RUN {root.name} {old} -> {new}: {len(changed)} files would change, nothing written")
        return 0, out
    repo.commit()
    problems = vp.check(vp.Repo(root), new)  # the last word: read everything again from the disk
    if problems:
        return 1, [f"FAIL after writing: {p}" for p in problems]
    out.extend(f"  changed {rel}" for rel in changed)
    out.append(f"BUMP=PASS {root.name} {old} -> {new}: {len(changed)} files, every place agrees with the manifest")
    return 0, out


class UsageParser(argparse.ArgumentParser):
    """An argument parser that ends a wrong use with exit code 64, as docs/CONVENTIONS.md says for the command-line tools of the suite (argparse alone uses 2)."""

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = UsageParser(description="Raise the version of a repository in every place that holds it.")
    parser.add_argument("repository")
    parser.add_argument("new", help="the new version, or `next` for the one the odometer gives")
    parser.add_argument("title", help="the title of the version, for the CHANGELOG heading")
    parser.add_argument("--workspace", type=Path, help="the folder that holds the repositories (default: the parent of this repository)")
    parser.add_argument("--dry-run", action="store_true", help="write nothing, show what would change")
    parser.add_argument("--explicit", action="store_true", help="accept a version that is not the one of the odometer")
    parser.add_argument("--fix-drift", action="store_true", help="also overwrite places that held another version than the manifest")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = resolve(args.repository, args.workspace)
    if not (root / vp.MANIFEST).is_file():
        print(f"FAIL {root} has no {vp.MANIFEST}")
        return 1
    code, lines = bump(root, args.new, args.title, args.explicit, args.dry_run, args.fix_drift)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
