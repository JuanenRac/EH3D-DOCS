#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/make_release_sbom.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Writes a CycloneDX 1.5 bill of materials (JSON) that lists the files of a release with their SHA-256.

    python tools/make_release_sbom.py --name EH3D-SERVER --version 1.2.3 --out sbom.cdx.json  FILE_OR_FOLDER [...]

Every file becomes a component of type "file" (a folder is walked; the names are relative to it and use "/"). The result is the same for the same files: the components
are sorted by name, the serial number is derived from the name, the version and the hashes, and no time is written unless --timestamp is given.
Exit codes: 0 written, 1 nothing to list, 64 wrong use. Standard library only."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from pathlib import Path

BOM_FORMAT = "CycloneDX"
SPEC_VERSION = "1.5"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def collect(paths: list[Path]) -> dict[str, Path]:
    """{name in the bill: file} for the files and the folders given; two files with one name are an error."""
    found: dict[str, Path] = {}
    for item in paths:
        if item.is_dir():
            files = sorted(p for p in item.rglob("*") if p.is_file())
            names = [p.relative_to(item).as_posix() for p in files]
        elif item.is_file():
            files, names = [item], [item.name]
        else:
            raise FileNotFoundError(str(item))
        for name, file in zip(names, files, strict=True):
            if name in found:
                raise ValueError(f"two files are named {name}")
            found[name] = file
    return found


def build_bom(name: str, version: str, files: dict[str, Path], timestamp: str = "") -> dict:
    components = [
        {
            "type": "file",
            "bom-ref": f"file:{rel}",
            "name": rel,
            "hashes": [{"alg": "SHA-256", "content": sha256_of(path)}],
        }
        for rel, path in sorted(files.items())
    ]
    seed = "\n".join([name, version, *(f"{c['name']} {c['hashes'][0]['content']}" for c in components)])
    metadata: dict = {"component": {"type": "application", "bom-ref": f"release:{name}", "name": name, "version": version}}
    if timestamp:
        metadata["timestamp"] = timestamp
    return {
        "bomFormat": BOM_FORMAT,
        "specVersion": SPEC_VERSION,
        "serialNumber": f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, seed)}",
        "version": 1,
        "metadata": metadata,
        "components": components,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CycloneDX bill of materials of the files of a release")
    parser.add_argument("paths", nargs="+", type=Path, help="files or folders to list")
    parser.add_argument("--name", required=True, help="name of the release (the repository)")
    parser.add_argument("--version", required=True, help="version of the release")
    parser.add_argument("--out", required=True, type=Path, help="where to write the JSON")
    parser.add_argument("--timestamp", default="", help="ISO 8601 time to write in the metadata (omitted by default so the result is repeatable)")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    try:
        files = collect(args.paths)
    except (FileNotFoundError, ValueError) as exc:
        print(f"make_release_sbom: {exc}", file=sys.stderr)
        return 64
    files = {rel: path for rel, path in files.items() if path.resolve() != args.out.resolve()}
    if not files:
        print("make_release_sbom: no files to list", file=sys.stderr)
        return 1
    bom = build_bom(args.name, args.version, files, args.timestamp)
    args.out.write_text(json.dumps(bom, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"make_release_sbom: {len(bom['components'])} files -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
