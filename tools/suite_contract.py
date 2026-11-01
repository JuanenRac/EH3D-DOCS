#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/suite_contract.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Checks that the repositories of the suite fit each other: the relations that no repository can check by itself.

    python -I tools/suite_contract.py --workspace ..            every check on the repositories next to this one
    python -I tools/suite_contract.py --workspace .. --only paths   a single check
    python -I tools/suite_contract.py --workspace .. --strict      a finding that is only a warning also fails

The checks:

    manifests   every eh3d.project.json is JSON with a name that is the folder and a version of dotted numbers
    paths       a dependency of a Cargo.toml on a sibling by path says which version of it the program needs (`version = ">=0.0.1", path = "../EH3D-X"`)
    versions    the version that SUITE_MAP.md gives for a repository is the one in its manifest
    ports       the screens and the server agree on the port of the server

A finding is an ERROR (the relation is broken) or a WARNING (it is drifting). The last line is SUITE_CONTRACT=PASS or SUITE_CONTRACT=FAIL; a repository that is not
next to this one is skipped, so the check runs on whatever is there. The known exceptions are in docs/suite_contract_allow.txt, one `check repository` per line.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION = re.compile(r"^\d+(\.\d+){2,3}$")


class Finding:
    def __init__(self, check: str, repo: str, level: str, text: str) -> None:
        self.check, self.repo, self.level, self.text = check, repo, level, text

    def __str__(self) -> str:
        return f"{self.level} [{self.check}] {self.repo}: {self.text}"


def repos(workspace: Path) -> list[Path]:
    return sorted(p for p in workspace.glob("EH3D-*") if p.is_dir() and (p / "eh3d.project.json").is_file())


def manifest_of(repo: Path) -> dict | None:
    try:
        data = json.loads((repo / "eh3d.project.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def check_manifests(workspace: Path) -> list[Finding]:
    out: list[Finding] = []
    for repo in repos(workspace):
        m = manifest_of(repo)
        if m is None:
            out.append(Finding("manifests", repo.name, "ERROR", "eh3d.project.json is not a JSON object"))
            continue
        name, version = m.get("name"), m.get("version")
        if name != repo.name:
            out.append(Finding("manifests", repo.name, "ERROR", f"the name in the manifest is {name!r}"))
        if not isinstance(version, str) or not VERSION.match(version):
            out.append(Finding("manifests", repo.name, "ERROR", f"the version {version!r} is not dotted numbers"))
    return out


PATH_DEP = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*=\s*\{([^}]*)\}", re.M)


def check_paths(workspace: Path) -> list[Finding]:
    out: list[Finding] = []
    for repo in repos(workspace):
        cargo = repo / "Cargo.toml"
        if not cargo.is_file():
            continue
        for m in PATH_DEP.finditer(cargo.read_text(encoding="utf-8", errors="replace")):
            body = m.group(2)
            path = re.search(r'path\s*=\s*"(\.\./[^"]+)"', body)
            if path and "version" not in body:
                out.append(Finding("paths", repo.name, "WARNING", f"{m.group(1)} reaches {path.group(1)} with no version"))
    return out


ROW = re.compile(r"^\|\s*\[(EH3D-[A-Z0-9-]+)\]\([^)]*\)\s*\|[^|]*\|[^|]*\|\s*([^|]*?)\s*\|")


def check_versions(workspace: Path) -> list[Finding]:
    out: list[Finding] = []
    here = workspace / "EH3D-DOCS" / "docs" / "SUITE_MAP.md"
    if not here.is_file():
        return out
    for line in here.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        name, shown = m.group(1), m.group(2)
        repo = workspace / name
        manifest = manifest_of(repo) if repo.is_dir() else None
        if manifest is None or not VERSION.match(shown):
            continue
        if manifest.get("version") != shown:
            out.append(Finding("versions", name, "WARNING", f"SUITE_MAP says {shown} and the manifest says {manifest.get('version')}"))
    return out


def check_ports(workspace: Path) -> list[Finding]:
    out: list[Finding] = []
    server = workspace / "EH3D-SERVER" / "src" / "config.rs"
    if not server.is_file():
        return out
    match = re.search(r"\b(\d{4,5})\b", "\n".join(l for l in server.read_text(encoding="utf-8", errors="replace").splitlines() if "port" in l.lower()))
    port = match.group(1) if match else None
    if port is None:
        return out
    for screen in ("EH3D-NODE-BUNGARD-HMI", "EH3D-NODE-HMI-GUI"):
        cfg = workspace / screen / "core" / "hmi_config.hpp"
        if cfg.is_file():
            text = cfg.read_text(encoding="utf-8", errors="replace")
            found = re.search(r"server_port\s*=\s*(\d+)", text)
            if found and found.group(1) != port:
                out.append(Finding("ports", screen, "ERROR", f"the screen looks for the server on port {found.group(1)} and the server listens on {port}"))
    return out


CHECKS = {"manifests": check_manifests, "paths": check_paths, "versions": check_versions, "ports": check_ports}


def allowed(allow_file: Path) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    if allow_file.is_file():
        for raw in allow_file.read_text(encoding="utf-8").splitlines():
            line = raw.split("#", 1)[0].split()
            if len(line) >= 2:
                out.add((line[0], line[1]))
    return out


def run(workspace: Path, only: str | None = None, strict: bool = False, allow_file: Path | None = None) -> tuple[bool, list[Finding]]:
    skip = allowed(allow_file or HERE.parent / "docs" / "suite_contract_allow.txt")
    found: list[Finding] = []
    for name, check in CHECKS.items():
        if only and name != only:
            continue
        found += [f for f in check(workspace) if (f.check, f.repo) not in skip]
    failed = any(f.level == "ERROR" or strict for f in found)
    return not failed, found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Checks that the repositories of the suite fit each other.")
    parser.add_argument("--workspace", type=Path, default=HERE.parents[1], help="the folder that holds the repositories (default: the one that holds this one)")
    parser.add_argument("--only", choices=sorted(CHECKS), help="run a single check")
    parser.add_argument("--strict", action="store_true", help="warnings fail too")
    args = parser.parse_args(argv)
    ok, found = run(args.workspace, args.only, args.strict)
    for f in found:
        print(f)
    print(f"SUITE_CONTRACT={'PASS' if ok else 'FAIL'} repositories={len(repos(args.workspace))} findings={len(found)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
