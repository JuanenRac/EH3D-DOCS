#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/release_notes.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The notes and the title of a release, taken from the CHANGELOG of a repository.

    python tools/release_notes.py REPOSITORY [VERSION] [--workspace FOLDER] [--title | --notes] [--check [--allow-short]]

VERSION is the one of the manifest when it is not given. Without options it prints the title ("REPOSITORY X.Y.Z - Title")
and then the notes (the section of that version of CHANGELOG.md), which is what `gh release create --notes-file` takes.
--check publishes nothing and prints nothing but the verdict: it fails (exit 1) when the CHANGELOG has no section for the
version of the manifest or when [Unreleased] still holds entries that were not promoted; a section with fewer than
3 entries is only a warning (exit 2), and --allow-short accepts it (exit 0)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import changelog_tools  # noqa: E402
import version_places as vp  # noqa: E402

MIN_ENTRIES = 3
HUB = Path(__file__).resolve().parents[1]


def release_text(root: Path, version: str | None = None) -> tuple[str, str, str, str]:
    """(repository name, version, title, notes) of the release; raises changelog_tools.ChangelogError without a section."""
    repo = vp.Repo(root)
    version = version or vp.manifest_version(repo)
    text = repo.read("CHANGELOG.md")
    if text is None:
        raise changelog_tools.ChangelogError("CHANGELOG.md is missing")
    section = changelog_tools.find(text, version)
    if section is None:
        raise changelog_tools.ChangelogError(f"CHANGELOG.md has no section for {version}")
    notes = changelog_tools.body(text, section).strip()
    if not notes:
        raise changelog_tools.ChangelogError(f"the section {version} of CHANGELOG.md is empty")
    return root.name, version, section.title, notes + "\n"


def check(root: Path) -> tuple[int, list[str]]:
    """The verdict for the version of the manifest: (0 fine | 1 error | 2 only a warning, lines)."""
    repo = vp.Repo(root)
    version = vp.manifest_version(repo)
    text = repo.read("CHANGELOG.md")
    if text is None:
        return 1, ["FAIL CHANGELOG.md is missing"]
    lines: list[str] = []
    section = changelog_tools.find(text, version)
    if section is None:
        return 1, [f"FAIL CHANGELOG.md has no section for the version {version} of the manifest"]
    pending = changelog_tools.unreleased_body(text)
    if pending is None:
        lines.append("FAIL CHANGELOG.md has no '## [Unreleased]' heading")
    elif pending:
        lines.append(f"FAIL '## [Unreleased]' still holds {changelog_tools.count_entries(pending) or 'some'} entries that are not in {version}: promote them (bump_version.py) or move them out")
    count = changelog_tools.count_entries(changelog_tools.body(text, section))
    if lines:
        return 1, lines
    if count < MIN_ENTRIES:
        return 2, [f"WARN the section {version} has {count} entries, fewer than {MIN_ENTRIES}: a release is meant to be complete (--allow-short accepts it)"]
    return 0, [f"OK the section {version} has {count} entries and [Unreleased] is empty"]


class UsageParser(argparse.ArgumentParser):
    """An argument parser that ends a wrong use with exit code 64, as docs/CONVENTIONS.md says for the command-line tools of the suite (argparse alone uses 2)."""

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = UsageParser(description="The notes and the title of a release from the CHANGELOG.")
    parser.add_argument("repository")
    parser.add_argument("version", nargs="?")
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--title", action="store_true", help="print only the title")
    parser.add_argument("--notes", action="store_true", help="print only the notes")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--allow-short", action="store_true", help="with --check: fewer than 3 entries is accepted")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    from bump_version import resolve

    root = resolve(args.repository, args.workspace)
    try:
        if args.check:
            code, lines = check(root)
            for line in lines:
                print(line)
            return 0 if code == 2 and args.allow_short else code
        name, version, title, notes = release_text(root, args.version)
    except (vp.VersionError, changelog_tools.ChangelogError) as error:
        print(f"FAIL {error}")
        return 1
    heading = f"{name} {version}" + (f" - {title}" if title else "")
    if args.title:
        print(heading)
    elif args.notes:
        sys.stdout.write(notes)
    else:
        print(heading)
        print()
        sys.stdout.write(notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
