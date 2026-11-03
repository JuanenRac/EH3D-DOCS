# =============================================================================
# EH3D-DOCS - tools/version_places.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Every place where an EH3D repository keeps its version, the odometer that says which version comes next, and the
check that all the places agree with the manifest (eh3d.project.json).

The places: the manifest, Cargo.toml and Cargo.lock, package.json and package-lock.json, pyproject.toml and the
`__version__` mirror, the Gradle files of an Android app (versionName), project.yml of an iOS app (MARKETING_VERSION),
the file the manifest names in native_version, the badge and the "Version" row of the eight README files, and the newest
section of CHANGELOG.md. Used by bump_version.py and prerelease_check.py. Standard library only."""
from __future__ import annotations

import fnmatch
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import changelog_tools

MANIFEST = "eh3d.project.json"
# The manifest of the updater of the whole family has its own name: it belongs to no ecosystem, so it keeps its own file.
MANIFESTS = (MANIFEST, "electro-hobby-3d.project.json")
READMES = ("README.md", "README_spa.md", "README_deu.md", "README_fra.md", "README_ita.md", "README_jpn.md", "README_zho.md", "README_por.md")
SKIP_DIRS = {".git", "target", "node_modules", "build", "dist", ".gradle", ".venv", "venv", "__pycache__", ".cxx", ".idea", ".compile", "managed_components"}
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(\.\d+)?$")


class VersionError(Exception):
    """A version string or a file cannot be handled."""


# --------------------------------------------------------------------------- the odometer
def manifest_name(root: Path | str) -> str:
    """The file name of the manifest of the repository in `root`: eh3d.project.json, or electro-hobby-3d.project.json for the updater of the family."""
    for name in MANIFESTS:
        if (Path(root) / name).is_file():
            return name
    return MANIFEST


def parse(version: str) -> tuple[int, ...]:
    if not VERSION_RE.match(version):
        raise VersionError(f"'{version}' is not a version of three or four numbers")
    return tuple(int(part) for part in version.split("."))


def compare(a: str, b: str) -> int:
    """-1, 0 or 1; a version of four components is greater than the one of three with the same first three (zeros fill on the right)."""
    x, y = list(parse(a)), list(parse(b))
    size = max(len(x), len(y))
    x += [0] * (size - len(x))
    y += [0] * (size - len(y))
    return (x > y) - (x < y)


def next_version(version: str) -> str:
    """The odometer: the last number goes up; past 9 it returns to 0 and carries to the one before (0.0.9 -> 0.1.0, never 0.0.10).

    Three components reach 0.7.9 and then become four (0.7.9 -> 0.8.0.0); 0.9.9.9 -> 1.0.0.0."""
    numbers = list(parse(version))
    if any(n > 9 for n in numbers):
        raise VersionError(f"{version} has a number above 9: it is not an odometer version, so pass the new version with --explicit")
    index = len(numbers) - 1
    while index >= 0:
        numbers[index] += 1
        if numbers[index] <= 9:
            break
        numbers[index] = 0
        index -= 1
    else:
        raise VersionError(f"{version} cannot go up: the odometer is full")
    if len(numbers) == 3 and tuple(numbers) >= (0, 8, 0):
        numbers.append(0)
    return ".".join(str(n) for n in numbers)


def check_digits(version: str) -> None:
    if any(n > 9 for n in parse(version)):
        raise VersionError(f"{version} has a number above 9: the odometer never writes two digits")


# --------------------------------------------------------------------------- files with their line ends
class Repo:
    """A repository folder read through an overlay: writes stay in memory until commit(), and every read sees them."""

    def __init__(self, root: Path | str):
        self.root = Path(root)
        self.manifest = manifest_name(self.root)
        self.overlay: dict[str, str] = {}
        self._crlf: dict[str, bool] = {}
        self._disk: dict[str, str] = {}

    def exists(self, rel: str) -> bool:
        return rel in self.overlay or (self.root / rel).is_file()

    def original(self, rel: str) -> str | None:
        if rel not in self._disk:
            path = self.root / rel
            if not path.is_file():
                return None
            raw = path.read_bytes().decode("utf-8")
            self._crlf[rel] = "\r\n" in raw
            self._disk[rel] = raw.replace("\r\n", "\n")
        return self._disk[rel]

    def read(self, rel: str) -> str | None:
        return self.overlay[rel] if rel in self.overlay else self.original(rel)

    def write(self, rel: str, text: str) -> None:
        self.original(rel)
        if text != self.original(rel):
            self.overlay[rel] = text
        else:
            self.overlay.pop(rel, None)

    def changed(self) -> list[str]:
        return sorted(self.overlay)

    def commit(self) -> None:
        staged: list[tuple[Path, Path]] = []
        try:
            for rel, text in self.overlay.items():
                data = text.replace("\n", "\r\n") if self._crlf.get(rel) else text
                target = self.root / rel
                temp = target.with_name(target.name + ".bump-tmp")
                temp.write_bytes(data.encode("utf-8"))
                staged.append((temp, target))
        except OSError:
            for temp, _ in staged:
                temp.unlink(missing_ok=True)
            raise
        for temp, target in staged:  # every file is complete before the first one replaces its old copy
            os.replace(temp, target)

    def files(self, name: str) -> list[str]:
        """The relative paths of the files called `name` below the root, outside build and tool folders."""
        out = []
        for folder, dirs, names in os.walk(self.root):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)  # build and tool folders are never entered
            for found in fnmatch.filter(names, name):
                out.append((Path(folder) / found).relative_to(self.root).as_posix())
        return sorted(out)


# --------------------------------------------------------------------------- scanning
@dataclass
class Found:
    file: str
    label: str
    value: str
    start: int
    end: int
    soft: bool = False  # replaced when it holds the old version, never reported when it holds another one
    index: int | None = None  # the place holds one number of the version (0 major, 1 minor, 2 patch, 3 build), not the whole of it


@dataclass
class Scan:
    found: list[Found] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    expect_codes: list[tuple[str, str]] = field(default_factory=list)  # (file, kind) that carry a build number to raise


def _add(scan: Scan, rel: str, label: str, text: str, pattern: str, flags: int = 0, limit: int | None = None, soft: bool = False, required: bool = True) -> int:
    count = 0
    for match in re.finditer(pattern, text, flags):
        scan.found.append(Found(rel, label, match.group("v"), match.start("v"), match.end("v"), soft))
        count += 1
        if limit is not None and count >= limit:
            break
    if count == 0 and required:
        scan.missing.append(f"{rel} has no {label}")
    return count


def _cargo(scan: Scan, repo: Repo, rel: str, text: str) -> list[str]:
    """The `version` of [package] and [workspace.package]; returns the package name when [package] has one."""
    section, names = "", []
    offset = 0
    versions = 0
    inherits = False
    for line in text.split("\n"):
        header = re.match(r"\s*\[([^\]]+)\]\s*$", line)
        if header:
            section = header.group(1).strip()
        elif section in ("package", "workspace.package"):
            m = re.match(r'(\s*version\s*=\s*")(?P<v>[^"]+)"', line)
            if m:
                scan.found.append(Found(rel, "version", m.group("v"), offset + m.start("v"), offset + m.end("v"), soft=(rel != "Cargo.toml")))
                versions += 1
            n = re.match(r'\s*name\s*=\s*"(?P<n>[^"]+)"', line)
            if n and section == "package":
                names.append(n.group("n"))
            if section == "package" and re.match(r"\s*version(\.workspace\s*=\s*true|\s*=\s*\{\s*workspace\s*=\s*true)", line):
                inherits = True
        offset += len(line) + 1
    if rel == "Cargo.toml" and versions == 0 and not re.search(r"(?m)^version\.workspace\s*=\s*true", text) and re.search(r"(?m)^\[(package|workspace\.package)\]", text):
        scan.missing.append("Cargo.toml has no version in [package]")
    return names if (versions or inherits) else []


_DEPENDENCY = re.compile(r'(?m)^[ \t]*(?P<name>[A-Za-z0-9_-]+)[ \t]*=[ \t]*\{[^}\n]*\bversion[ \t]*=[ \t]*"[ \t]*(?:>=|\^|=|~)?[ \t]*(?P<v>\d+(?:\.\d+)+)"')


def _internal_dependencies(scan: Scan, rel: str, text: str, own: set[str]) -> None:
    """A dependency on a package of this same repository that asks for a minimum version (`version = ">=0.1.0"`): it follows the version when it holds the old one.

    The sign (`>=`, `^`, `=`, `~`) stays; a dependency on another repository, or one that already asks for something older, is left alone."""
    for match in _DEPENDENCY.finditer(text):
        if match.group("name") in own:
            scan.found.append(Found(rel, f"dependency on {match.group('name')}", match.group("v"), match.start("v"), match.end("v"), soft=True))


def scan(repo: Repo) -> Scan:
    """Every place that holds the version in the repository; `missing` lists the places that should exist and do not."""
    out = Scan()
    name = repo.manifest
    manifest = repo.read(name)
    if manifest is None:
        raise VersionError(f"{name} is missing")
    _add(out, name, "version", manifest, r'(?m)^[ \t]{0,4}"version"[ \t]*:[ \t]*"(?P<v>[^"]*)"', limit=1)
    _add(out, name, "version in notes", manifest, r'"notes"\s*:\s*"[A-Za-z]+ v(?P<v>\d+(?:\.\d+)+):', soft=True, required=False)
    handled = {name}

    names: list[tuple[str, bool]] = []  # (package name, is the root package)
    for rel in repo.files("Cargo.toml"):
        text = repo.read(rel) or ""
        names += [(name, rel == "Cargo.toml") for name in _cargo(out, repo, rel, text)]
        handled.add(rel)
    own = {name for name, _ in names}
    for rel in repo.files("Cargo.toml"):
        _internal_dependencies(out, rel, repo.read(rel) or "", own)
    lock = repo.read("Cargo.lock")
    if lock is not None and names:
        handled.add("Cargo.lock")
        for name, is_root in names:
            _add(out, "Cargo.lock", f"entry of the package {name}", lock, r'name = "%s"\nversion = "(?P<v>[^"]+)"' % re.escape(name), limit=1, soft=not is_root, required=is_root)

    pkg = repo.read("package.json")
    if pkg is not None:
        handled.add("package.json")
        _add(out, "package.json", "version", pkg, r'(?m)^[ \t]{0,4}"version"[ \t]*:[ \t]*"(?P<v>[^"]*)"', limit=1)
    plock = repo.read("package-lock.json")
    if plock is not None:
        handled.add("package-lock.json")
        _add(out, "package-lock.json", "version", plock, r'(?m)^  "version"[ \t]*:[ \t]*"(?P<v>[^"]*)"', limit=1)
        if '"packages"' in plock:
            _add(out, "package-lock.json", 'version of the package ""', plock, r'"packages"\s*:\s*\{\s*""\s*:\s*\{[^{}]*?"version"\s*:\s*"(?P<v>[^"]*)"', re.S, limit=1)

    py = repo.read("pyproject.toml")
    if py is not None:
        handled.add("pyproject.toml")
        dynamic = re.search(r'dynamic\s*=\s*\[[^\]]*"version"', py)
        _add(out, "pyproject.toml", "version", py, r'(?m)^version\s*=\s*"(?P<v>[^"]+)"', limit=1, required=not dynamic)
    for pattern in ("src/*/__init__.py", "*/__init__.py"):
        for path in sorted(repo.root.glob(pattern)):
            rel = path.relative_to(repo.root).as_posix()
            if rel in handled or SKIP_DIRS & set(Path(rel).parts):
                continue
            text = repo.read(rel) or ""
            if _add(out, rel, "__version__", text, r'(?m)^__version__\s*=\s*"(?P<v>[^"]*)"', limit=1, required=False):
                handled.add(rel)

    for name in ("build.gradle.kts", "build.gradle"):
        for rel in repo.files(name):
            text = repo.read(rel) or ""
            if _add(out, rel, "versionName", text, r'versionName\s*=?\s*"(?P<v>[^"]+)"', limit=1, required=False):
                out.expect_codes.append((rel, "gradle"))
                handled.add(rel)
    yml = repo.read("project.yml")
    if yml is not None and "MARKETING_VERSION" in yml:
        handled.add("project.yml")
        _add(out, "project.yml", "MARKETING_VERSION", yml, r'MARKETING_VERSION:\s*"(?P<v>[^"]+)"')
        out.expect_codes.append(("project.yml", "yml"))

    loaded = json.loads(manifest) if _valid_json(manifest) else None
    native = loaded.get("native_version") if isinstance(loaded, dict) else None
    if isinstance(native, dict) and native.get("file") and native["file"] not in handled and repo.read(native["file"]) is not None:
        _native(out, repo, native)

    for rel in READMES:
        text = repo.read(rel)
        if text is None:
            out.missing.append(f"{rel} is missing")
            continue
        _add(out, rel, "version badge", text, r"img\.shields\.io/badge/Version-(?P<v>\d[\d.]*)-", limit=1, required=False)
        _add(out, rel, 'version in the "Version" row of the table', text, r"(?m)^\|[^|\n`]*\|\s*`(?P<v>\d+\.\d+\.\d+(?:\.\d+)?)`\s*\|\s*$", limit=1)
    return out


def _valid_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


def _native(out: Scan, repo: Repo, native: dict) -> None:
    """The file named by native_version, when it is not one of the usual ones: the number the pattern points at, in full."""
    rel = native["file"]
    text = repo.read(rel) or ""
    pattern = native.get("pattern", r"(\d+\.\d+\.\d+)")
    if isinstance(pattern, dict):  # one regex per number: major, minor, patch and (optionally) build
        _native_parts(out, rel, text, pattern)
        return
    try:
        match = re.search(pattern, text, re.M)
    except re.error as error:
        out.missing.append(f"native_version pattern of the manifest is not a regular expression: {error}")
        return
    if not match or not match.groups():
        out.missing.append(f"{rel} (native_version) has no version that its pattern finds")
        return
    start = match.start(1)
    number = re.match(r"\d+(?:\.\d+)*", text[start:])
    if not number:
        out.missing.append(f"{rel} (native_version) does not hold a number at its pattern")
        return
    out.found.append(Found(rel, "native version", number.group(0), start, start + len(number.group(0))))


def _native_parts(out: Scan, rel: str, text: str, pattern: dict) -> None:
    """A native version given as one regex per number: every number is a place of its own (`index`) that follows the matching number of the version."""
    for index, key in enumerate(("major", "minor", "patch", "build")):
        if key not in pattern:
            continue
        try:
            match = re.search(str(pattern[key]), text, re.M)
        except re.error as error:
            out.missing.append(f"native_version {key} pattern of the manifest is not a regular expression: {error}")
            continue
        if not match or not match.groups():
            if key != "build":
                out.missing.append(f"{rel} (native_version) has no {key} number that its pattern finds")
            continue
        out.found.append(Found(rel, f"native version {key}", match.group(1), match.start(1), match.end(1), index=index))


def _part(version: str, index: int | None) -> str | None:
    """The whole version, or its number number `index` (None when the version has no such number)."""
    if index is None:
        return version
    parts = version.split(".")
    return parts[index] if index < len(parts) else None


# --------------------------------------------------------------------------- the check of coherence
def manifest_version(repo: Repo) -> str:
    text = repo.read(repo.manifest)
    if text is None:
        raise VersionError(f"{repo.manifest} is missing")
    try:
        return json.loads(text)["version"]
    except (ValueError, KeyError) as error:
        raise VersionError(f"{repo.manifest} has no readable version: {error}") from error


def check(repo: Repo, expected: str | None = None) -> list[str]:
    """What disagrees with `expected` (the version of the manifest by default): places that hold another version,
    places that should exist and do not, JSON files that do not parse, and the newest CHANGELOG section."""
    problems: list[str] = []
    expected = expected or manifest_version(repo)
    scanned = scan(repo)
    problems.extend(scanned.missing)
    for item in scanned.found:
        if not item.soft and item.value != _part(expected, item.index) and not (item.index == 3 and _part(expected, 3) is None):
            problems.append(f"{item.file}: {item.label} is {item.value}, the version is {expected}")
    for rel in (repo.manifest, "package.json", "package-lock.json"):
        text = repo.read(rel)
        if text is not None and not _valid_json(text):
            problems.append(f"{rel} is not valid JSON")
    changelog = repo.read("CHANGELOG.md")
    if changelog is None:
        problems.append("CHANGELOG.md is missing")
    else:
        newest = changelog_tools.newest_release(changelog)
        if newest is None or newest.version != expected:
            problems.append(f"CHANGELOG.md: the newest section is {newest.version if newest else 'none'}, the version is {expected}")
    return problems


# --------------------------------------------------------------------------- setting the version
def apply(repo: Repo, old: str, new: str, fix_drift: bool = False) -> tuple[list[str], list[str]]:
    """Write `new` in every place that holds `old` (or, with fix_drift, any version); also raises versionCode and
    CURRENT_PROJECT_VERSION by one. Returns (problems found before writing, files changed). Nothing is written when there are problems."""
    scanned = scan(repo)
    problems = list(scanned.missing)
    for item in scanned.found:
        if not item.soft and item.value != _part(old, item.index) and not fix_drift and not (item.index == 3 and _part(old, 3) is None):
            problems.append(f"{item.file}: {item.label} is {item.value}, not {old} (the version of the manifest): fix it first or use --fix-drift")
    if problems:
        return problems, []
    by_file: dict[str, list[Found]] = {}
    for item in scanned.found:
        if item.value == _part(old, item.index) or (fix_drift and not item.soft):
            by_file.setdefault(item.file, []).append(item)
    for rel, items in by_file.items():
        text = repo.read(rel) or ""
        for item in sorted(items, key=lambda i: i.start, reverse=True):
            replacement = _part(new, item.index)
            if replacement is not None:
                text = text[:item.start] + replacement + text[item.end:]
        repo.write(rel, text)
    for rel, kind in scanned.expect_codes:
        text = repo.read(rel) or ""
        pattern = r"(versionCode\s*=?\s*)(\d+)" if kind == "gradle" else r'(CURRENT_PROJECT_VERSION:\s*")(\d+)(")'
        text, count = re.subn(pattern, lambda m: m.group(1) + str(int(m.group(2)) + 1) + (m.group(3) if m.lastindex == 3 else ""), text, count=1)
        if count:
            repo.write(rel, text)
    return [], repo.changed()
