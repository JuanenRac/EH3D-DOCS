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
of the file given with --signers. A package without a `.sig` is a failure (nothing signed it). Exit code: 0 when every package is good, 1 when any is not, 64 for a wrong use.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

NAMESPACE = "eh3d-release"
OWNER = "JuanenRac"
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


def verify_folder(folder: Path, signers: Path) -> list[str]:
    """The problems of the packages in a folder (empty: every package is good). Without a package at all it is a problem too."""
    problems: list[str] = []
    packages = sorted(p for p in folder.iterdir() if p.is_file() and p.with_name(p.name + ".sha256").is_file())
    if not packages:
        return [f"{folder.name}: no package with a .sha256 in it"]
    for package in packages:
        if sum_of(package) != expected_sum(package.with_name(package.name + ".sha256")):
            problems.append(f"{package.name}: the sum does not match its .sha256")
            continue
        signature = package.with_name(package.name + ".sig")
        if not signature.is_file():
            problems.append(f"{package.name}: no .sig next to it (nobody signed it)")
        elif not verify_signature(package, signature, signers):
            problems.append(f"{package.name}: the signature is not a good one of the release key")
    return problems


def download_latest(repo: str, target: Path) -> None:
    subprocess.run(["gh", "release", "download", "--repo", f"{OWNER}/{repo}", "--dir", str(target), "--clobber"], check=True, timeout=600)


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
    args = parser.parse_args(argv)
    signers = Path(args.signers)
    if not signers.is_file():
        print(f"VERIFY_RELEASE=FAIL no signers file {signers}", file=sys.stderr)
        return 64
    problems: list[str] = []
    if args.dir:
        problems = verify_folder(Path(args.dir), signers)
    else:
        for repo in (DESKTOP_TOOLS if args.all else (args.repo,)):
            with tempfile.TemporaryDirectory() as tmp:
                try:
                    download_latest(repo, Path(tmp))
                except (OSError, subprocess.SubprocessError) as error:
                    problems.append(f"{repo}: the release could not be downloaded ({error})")
                    continue
                problems.extend(f"{repo}: {line}" for line in verify_folder(Path(tmp), signers))
    for line in problems:
        print(line)
    print("VERIFY_RELEASE=" + ("FAIL" if problems else "PASS"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
