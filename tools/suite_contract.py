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

    manifests   every eh3d.project.json is JSON with a name that is the folder and a version of dotted numbers, and the parser of EH3D-UPDATER (when it is there) accepts it
    tools       every repository holds the shared ci_validate.py of this one (same tools version in the header, same code)
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


def real_parser(workspace: Path):
    """The parse_manifest function of the updater (the one that reads the manifests in the field), or None when EH3D-UPDATER is not next to this repository."""
    path = workspace / "EH3D-UPDATER" / "src" / "eh3d_updater" / "project_manifest.py"
    if not path.is_file():
        return None
    import importlib.util

    spec = importlib.util.spec_from_file_location("eh3d_contract_project_manifest", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # the dataclasses of the module look themselves up here
    try:
        spec.loader.exec_module(module)
    except Exception:  # noqa: BLE001 - a parser that does not load is not a finding about a manifest
        return None
    finally:
        sys.modules.pop(spec.name, None)
    return getattr(module, "parse_manifest", None)


def check_manifests(workspace: Path) -> list[Finding]:
    out: list[Finding] = []
    parse = real_parser(workspace)
    for repo in repos(workspace):
        m = manifest_of(repo)
        if m is None:
            out.append(Finding("manifests", repo.name, "ERROR", "eh3d.project.json is not a JSON object"))
            continue
        if parse is not None:
            try:
                parse((repo / "eh3d.project.json").read_text(encoding="utf-8"), expected_name=repo.name)
            except ValueError as error:
                out.append(Finding("manifests", repo.name, "ERROR", f"the parser of EH3D-UPDATER rejects the manifest: {error}"))
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


# the cells of a row of the map: the repository (with its link), the kind, the state, the release and what it is for
CELLS = re.compile(r"^(\|\s*\[(EH3D-[A-Z0-9-]+)\]\([^)]*\)\s*\|[^|]*\|[^|]*\|)(\s*)([^|]*?)(\s*)(\|.*)$")


def write_map(workspace: Path, write: bool = True) -> list[str]:
    """Puts in the Release column of SUITE_MAP.md the version of the manifest of each repository that is in the workspace, and nothing else: the words of the map are a person's.
    Returns what changed, as `<repository>: <old> -> <new>`; with `write` false it changes nothing."""
    here = workspace / "EH3D-DOCS" / "docs" / "SUITE_MAP.md"
    if not here.is_file():
        return []
    raw = here.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    lines = raw.replace("\r\n", "\n").split("\n")
    changed: list[str] = []
    for i, line in enumerate(lines):
        m = CELLS.match(line)
        if not m:
            continue
        name, shown = m.group(2), m.group(4)
        repo = workspace / name
        manifest = manifest_of(repo) if repo.is_dir() else None
        version = manifest.get("version") if manifest else None
        if not isinstance(version, str) or not VERSION.match(version) or version == shown:
            continue
        lines[i] = f"{m.group(1)}{m.group(3)}{version}{m.group(5)}{m.group(6)}"
        changed.append(f"{name}: {shown} -> {version}")
    if changed and write:
        text = "\n".join(lines)
        here.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
    return changed


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


def check_tools(workspace: Path) -> list[Finding]:
    """Every repository holds the shared validator of EH3D-DOCS: the same tools version in its header and the same code. A warning, because a repository that is busy is synchronised later."""
    sync_path = HERE / "sync_shared_tools.py"
    if not (workspace / "EH3D-DOCS" / "tools" / "ci_validate.py").is_file() or not sync_path.is_file():
        return []
    import importlib.util

    spec = importlib.util.spec_from_file_location("eh3d_contract_sync", sync_path)
    sync = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sync)
    out: list[Finding] = []
    for text in sync.canonical_problems(workspace):
        repo, _, message = text.partition(": ")
        out.append(Finding("tools", repo, "WARNING", message))
    for repo in sync.differing(workspace, "ci_validate.py").get("ci_validate.py", []):
        out.append(Finding("tools", repo, "WARNING", "ci_validate.py is not the copy of EH3D-DOCS"))
    return out


CHECKS = {"manifests": check_manifests, "paths": check_paths, "versions": check_versions, "ports": check_ports, "tools": check_tools}


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
    parser.add_argument("--write-map", action="store_true", help="put the versions of the manifests in the Release column of SUITE_MAP.md and stop (nothing else of the map changes)")
    args = parser.parse_args(argv)
    if args.write_map:
        changed = write_map(args.workspace)
        for line in changed:
            print(line)
        print(f"SUITE_MAP=WRITTEN rows={len(changed)}")
        return 0
    ok, found = run(args.workspace, args.only, args.strict)
    for f in found:
        print(f)
    print(f"SUITE_CONTRACT={'PASS' if ok else 'FAIL'} repositories={len(repos(args.workspace))} findings={len(found)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
