#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/verify_release.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Checks the packages of a release against their sum and their signature (docs/RELEASE_KEY.md).

    python tools/verify_release.py --dir DOWNLOADS --signers allowed_signers      # every package in a folder
    python tools/verify_release.py --repo EH3D-AUTOLEVEL --signers allowed_signers  # download the newest release of one repository and check it
    python tools/verify_release.py --all --signers allowed_signers                # the same for the desktop programs of the suite

A package is every file that has a `.sha256` next to it. The sum must match; the `.sig` must be a good signature of the namespace `eh3d-release` made by a signer
of the file given with --signers. A package without a `.sig` is a failure (nothing signed it).

The record of a release, `eh3d-release.json` (repository, version, and the name, architecture, size and SHA-256 of every file), is signed the same way. It is demanded for
every version later than the last one of the repository published without it (`LAST_WITHOUT_RECORD`; a repository that is not listed never published without one) and by
any release that publishes the record or its signature. When it is there it must be signed, and every package must be listed in it with its sum, of its repository and
version. An earlier release that publishes neither is judged by the `.sig` of each package, as before. An `.apk` has no `.sig` of its own: the record is what signs it.

The version is checked too: with --repo and --all the files and the record must be of the tag of the release; with --version (any mode) they must be of that version.
The repository and the version of a file are read from its name. Exit code: 0 when every package is good, 1 when any is not, 64 for a wrong use.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

NAMESPACE = "eh3d-release"
OWNER = "JuanenRac"
RECORD = "eh3d-release.json"
APK_REPO = "EH3D-ANDROID-CONTROL"
# the last version of each repository that was published without a record; every later one has it
LAST_WITHOUT_RECORD = {
    "EH3D-ANDROID-CONTROL": "0.1.7",
    "EH3D-AUTOLEVEL": "0.1.2",
    "EH3D-BUNGARD-GUI": "0.3.0",
    "EH3D-CAM-DEBUGGER": "0.0.8",
    "EH3D-DRILLPRO": "0.2.2",
    "EH3D-GERBERVIEWER": "0.1.0",
    "EH3D-ISOCAM": "0.1.7",
    "EH3D-NODE-BUNGARD": "0.0.8",
    "EH3D-NODE-BUNGARD-AUX": "0.1.1",
    "EH3D-NODE-BUNGARD-HMI": "0.1.2",
    "EH3D-NODE-HMI-GUI": "0.1.2",
    "EH3D-PHOENIX-3DP": "0.0.8",
    "EH3D-PHOENIX-CAD": "0.1.4",
    "EH3D-PHOENIX-CNC": "0.2.3",
    "EH3D-PHOENIX-LASER": "0.1.6",
    "EH3D-PHOENIX-PCB": "0.1.6",
    "EH3D-PHOENIX-PNP": "0.1.4",
    "EH3D-ROUTEPRO": "0.1.9",
    "EH3D-SERVER": "0.2.5",
    "EH3D-STENCILCAM": "0.1.3",
    "EH3D-STUDIO": "0.2.0",
    "EH3D-SUITE-LAUNCHER": "0.0.7",
    "EH3D-TOOL-MANAGER": "0.1.2",
    "EH3D-VISION-STUDIO": "0.1.4",
}
# the desktop programs of the suite whose releases carry binaries
DESKTOP_TOOLS = (
    "EH3D-AUTOLEVEL",
    "EH3D-CAM-DEBUGGER",
    "EH3D-DRILLPRO",
    "EH3D-GERBERVIEWER",
    "EH3D-ISOCAM",
    "EH3D-PHOENIX-CNC",
    "EH3D-PHOENIX-LASER",
    "EH3D-ROUTEPRO",
    "EH3D-STENCILCAM",
    "EH3D-SUITE-LAUNCHER",
    "EH3D-TOOL-MANAGER",
    "EH3D-VISION-STUDIO",
)


def sum_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def expected_sum(sha_file: Path) -> str:
    """The hash that a `.sha256` file holds (the first word of its first line)."""
    words = sha_file.read_text(encoding="utf-8", errors="replace").split()
    return words[0].lower() if words else ""


def verify_signature(package: Path, signature: Path, signers: Path) -> bool:
    with package.open("rb") as stream:
        done = subprocess.run(
            ["ssh-keygen", "-Y", "verify", "-f", str(signers), "-I", NAMESPACE, "-n", NAMESPACE, "-s", str(signature)],
            stdin=stream, capture_output=True, text=True, timeout=60,
        )
    return done.returncode == 0 and "Good" in done.stdout


def release_of(name: str) -> tuple[str | None, str | None]:
    """The repository and the version a file of a release is named for (`eh3d-server-0.2.6-linux-x86_64.tar.gz`: EH3D-SERVER, 0.2.6); None for what the name does not say."""
    if name.startswith(APK_REPO) and name.endswith(".apk"):
        return APK_REPO, None
    found = re.match(r"(?P<program>[A-Za-z0-9-]+?)-(?P<version>\d+(?:\.\d+){2,3})(?=[-.])", name)
    if not found:
        return None, None
    program = found.group("program").lower().removeprefix("eh3d-")
    return "EH3D-" + program.upper(), found.group("version")


def numbers(version: str) -> tuple[int, ...]:
    parts = [int(part) for part in version.split(".")]
    return tuple(parts + [0] * (4 - len(parts)))


def needs_record(repo: str, version: str) -> bool:
    """Whether that version of that repository was published with a record: every one later than the last published without."""
    floor = LAST_WITHOUT_RECORD.get(repo)
    if floor is None or not re.fullmatch(r"\d+(\.\d+){0,3}", version):
        return True
    return numbers(version) > numbers(floor)


def read_record(folder: Path, signers: Path) -> tuple[dict | None, list[str]]:
    """The record in a folder, once its signature and its form are good: (record, []). (None, []) when the folder has neither the record nor its signature."""
    record, signature = folder / RECORD, folder / (RECORD + ".sig")
    if not record.is_file() and not signature.is_file():
        return None, []
    if not record.is_file():
        return None, [f"{RECORD}.sig is here and {RECORD} is not"]
    if not signature.is_file():
        return None, [f"{RECORD}: no .sig next to it (nobody signed it)"]
    if not verify_signature(record, signature, signers):
        return None, [f"{RECORD}: the signature is not a good one of the release key"]
    try:
        document = json.loads(record.read_text(encoding="utf-8"))
        if (document["format"], document["format_version"]) != ("eh3d-release", 1):
            raise ValueError
        files = {entry["name"]: (entry["sha256"], entry["arch"]) for entry in document["files"]}
        if len(files) != len(document["files"]) or not all(isinstance(document[key], str) for key in ("repository", "version")):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        return None, [f"{RECORD} is not a record of a release"]
    return {"repository": document["repository"], "version": document["version"], "files": files}, []


def verify_folder(folder: Path, signers: Path, repo: str | None = None, version: str | None = None) -> list[str]:
    """The problems of the packages in a folder (empty: every package is good). Without a package at all it is a problem too. `repo` and `version` are what the release
    is expected to be, when that is known."""
    problems: list[str] = []
    packages = sorted(p for p in folder.iterdir() if p.is_file() and p.with_name(p.name + ".sha256").is_file())
    if not packages:
        return [f"{folder.name}: no package with a .sha256 in it"]
    record, problems = None, []
    record_read = False
    for package in packages:
        if sum_of(package) != expected_sum(package.with_name(package.name + ".sha256")):
            problems.append(f"{package.name}: the sum does not match its .sha256")
            continue
        if not record_read:
            record, found = read_record(folder, signers)
            record_read = True
            problems.extend(found)
            if record is not None:
                if repo and record["repository"] != f"{OWNER}/{repo}":
                    problems.append(f"{RECORD} is the record of {record['repository']}, not of {OWNER}/{repo}")
                if version and record["version"] != version:
                    problems.append(f"{RECORD} is the record of the version {record['version']}, not of {version}")
        signature = package.with_name(package.name + ".sig")
        if signature.is_file():
            if not verify_signature(package, signature, signers):
                problems.append(f"{package.name}: the signature is not a good one of the release key")
                continue
        elif not (package.suffix == ".apk" and record is not None):
            problems.append(f"{package.name}: no .sig next to it (nobody signed it)")
            continue
        problems.extend(check_release(package, record, repo, version))
    return problems


def check_release(package: Path, record: dict | None, repo: str | None, version: str | None) -> list[str]:
    """The problems of what release a signed package is: its repository, its version and, when the release has one, its entry in the record."""
    name = package.name
    named_repo, named_version = release_of(name)
    if record is not None:
        repo = repo or record["repository"].removeprefix(f"{OWNER}/")
        version = version or record["version"]
    if repo and named_repo and named_repo != repo:
        return [f"{name}: it is named for {named_repo}, not for {repo}"]
    if version and named_version and named_version != version:
        return [f"{name}: it is named for the version {named_version}, not for {version}"]
    if record is not None:
        if name not in record["files"]:
            return [f"{name}: {RECORD} does not name it"]
        if record["files"][name][0] != sum_of(package):
            return [f"{name}: it is not the file that {RECORD} names"]
        return []
    repo, version = repo or named_repo, version or named_version
    if repo is None or version is None:
        return [f"{name}: which release it is cannot be told from its name, and there is no {RECORD}"]
    if needs_record(repo, version):
        return [f"{name}: {repo} {version} is published with {RECORD}, and it is not here (download it and its .sig too)"]
    return []


def download_latest(repo: str, target: Path) -> str:
    """Downloads the newest release of a repository and gives its version (the tag without the v)."""
    slug = f"{OWNER}/{repo}"
    tag = subprocess.run(["gh", "release", "view", "--repo", slug, "--json", "tagName", "--jq", ".tagName"], check=True, capture_output=True, text=True, timeout=60).stdout.strip()
    subprocess.run(["gh", "release", "download", tag, "--repo", slug, "--dir", str(target), "--clobber"], check=True, timeout=600)
    return tag.removeprefix("v")


class UsageParser(argparse.ArgumentParser):
    """An argument parser that ends a wrong use with exit code 64, as docs/CONVENTIONS.md says for the command-line tools of the suite (argparse alone uses 2)."""

    def error(self, message: str):
        self.exit(64, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = UsageParser(description="Check the sum and the signature of the packages of a release")
    parser.add_argument("--signers", required=True, help="the allowed_signers file of docs/RELEASE_KEY.md")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dir", help="a folder with the downloaded packages")
    group.add_argument("--repo", help="download the newest release of this repository and check it")
    group.add_argument("--all", action="store_true", help="the desktop programs of the suite, one after the other")
    parser.add_argument("--version", help="the version the packages have to be (with --repo the release must also be tagged with it); not with --all")
    args = parser.parse_args(argv)
    if args.version and args.all:
        parser.error("--version is not used with --all")
    signers = Path(args.signers)
    if not signers.is_file():
        print(f"VERIFY_RELEASE=FAIL no signers file {signers}", file=sys.stderr)
        return 64
    problems: list[str] = []
    if args.dir:
        problems = verify_folder(Path(args.dir), signers, version=args.version)
    else:
        for repo in (DESKTOP_TOOLS if args.all else (args.repo,)):
            with tempfile.TemporaryDirectory() as tmp:
                try:
                    version = download_latest(repo, Path(tmp))
                except (OSError, subprocess.SubprocessError) as error:
                    problems.append(f"{repo}: the release could not be downloaded ({error})")
                    continue
                if args.version and args.version != version:
                    problems.append(f"{repo}: the newest release is {version}, not {args.version}")
                problems.extend(f"{repo}: {line}" for line in verify_folder(Path(tmp), signers, repo=repo, version=version))
    for line in problems:
        print(line)
    print("VERIFY_RELEASE=" + ("FAIL" if problems else "PASS"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
