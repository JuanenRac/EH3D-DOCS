# =============================================================================
# EH3D-DOCS - tools/changelog_tools.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Reading and promoting the sections of a CHANGELOG.md ("## [Unreleased]" and "## [X.Y.Z] - Title").

Used by bump_version.py (promote the unreleased entries to the new version), release_notes.py (the notes of a
release) and prerelease_check.py. Standard library only. Texts are handled with LF line ends."""
from __future__ import annotations

import re
from dataclasses import dataclass

HEADING = re.compile(r"(?m)^## \[(?P<version>[^\]\n]+)\](?P<rest>[^\n]*)$")
ENTRY = re.compile(r"(?m)^[-*] ")


class ChangelogError(Exception):
    """The changelog cannot be read or promoted as asked."""


@dataclass
class Section:
    version: str
    title: str  # the text after " - " of the heading, empty when there is none
    heading_start: int
    body_start: int  # just after the heading line, newline included
    end: int  # start of the next heading, or the end of the text

    @property
    def is_unreleased(self) -> bool:
        return self.version.lower() == "unreleased"


def sections(text: str) -> list[Section]:
    found = list(HEADING.finditer(text))
    out = []
    for index, match in enumerate(found):
        end = found[index + 1].start() if index + 1 < len(found) else len(text)
        body_start = min(match.end() + 1, len(text))
        title = match.group("rest").strip()
        if title.startswith("-"):
            title = title[1:].strip()
        out.append(Section(match.group("version").strip(), title, match.start(), body_start, end))
    return out


def find(text: str, version: str) -> Section | None:
    return next((s for s in sections(text) if s.version == version), None)


def body(text: str, section: Section) -> str:
    return text[section.body_start:section.end].strip("\n")


def unreleased_body(text: str) -> str | None:
    """The unreleased entries (stripped), or None when the changelog has no [Unreleased] heading."""
    section = next((s for s in sections(text) if s.is_unreleased), None)
    return None if section is None else body(text, section).strip()


def count_entries(section_body: str) -> int:
    """The number of top-level bullets of a section."""
    return len(ENTRY.findall(section_body))


def newest_release(text: str) -> Section | None:
    return next((s for s in sections(text) if not s.is_unreleased), None)


def promote(text: str, version: str, title: str) -> str:
    """Move the entries of [Unreleased] under a new heading "## [version] - title"; [Unreleased] is left empty.

    Raises ChangelogError when there is no [Unreleased] heading, nothing to promote or the version already has a section."""
    if "\n" in title or not title.strip():
        raise ChangelogError("the title of the version must be one non-empty line")
    unreleased = next((s for s in sections(text) if s.is_unreleased), None)
    if unreleased is None:
        raise ChangelogError("CHANGELOG.md has no '## [Unreleased]' heading")
    if find(text, version) is not None:
        raise ChangelogError(f"CHANGELOG.md already has a section for {version}")
    entries = body(text, unreleased)
    if not entries.strip():
        raise ChangelogError("'## [Unreleased]' of CHANGELOG.md has no entries to promote")
    rest = text[unreleased.end:]
    head = text[:unreleased.body_start]
    if not head.endswith("\n"):
        head += "\n"
    return head + f"\n## [{version}] - {title.strip()}\n\n{entries}\n" + ("\n" + rest if rest else "")
