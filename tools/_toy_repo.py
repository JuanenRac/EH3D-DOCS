# =============================================================================
# EH3D-DOCS - tools/_toy_repo.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Small repositories for the tests of the version and release tools: every place that holds a version, in a temporary folder."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

LANGS = {"README.md": "Version", "README_spa.md": "Versión", "README_deu.md": "Version", "README_fra.md": "Version",
         "README_ita.md": "Versione", "README_jpn.md": "バージョン", "README_zho.md": "版本", "README_por.md": "Versão"}


def readme(label: str, version: str) -> str:
    return (
        "# Toy\n\n"
        f'<img src="https://img.shields.io/badge/Version-{version}-0f6cbd.svg" alt="Version">\n\n'
        "## \U0001F4CB At a glance\n\n| | |\n|---|---|\n"
        f"| {label} | `{version}` |\n| Tests | 5 |\n\n"
        "## \U0001F6A6 Project status\n\n\U0001F7E2 \U0001F7E1 \U0001F7E0 \U0001F534\n\n"
        "| Part | State | Notes |\n|---|---|---|\n| a | \U0001F7E1 | x |\n| b | \U0001F7E1 | x |\n| c | \U0001F7E1 | x |\n\n"
        "## Configuration\n\n| `key` | `0.0.0.0:1` | a | b |\n"
    )


def changelog(entries: int, released: str) -> str:
    bullets = "".join(f"- **Change {i}:** something.\n\n" for i in range(entries))
    return f"# Changelog\n\n## [Unreleased]\n\n{bullets}## [{released}] - The first one\n\n- **Start:** it began.\n"


def write(root: Path, rel: str, text: str, crlf: bool = False) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def make_repo(root: Path, name: str = "EH3D-TOY", version: str = "0.0.9", crlf: bool = False, cargo: bool = False, npm: bool = False,
              python: bool = False, gradle: bool = False, ios: bool = False, entries: int = 3, native: str | None = None) -> Path:
    """Make the repository `name` below `root` and return its folder; `crlf` writes every file with Windows line ends."""
    repo = root / name
    manifest = {"schema_version": "1.0", "ecosystem": "EH3D", "name": name, "version": version, "notes": f"Scaffolding v{version}: a toy."}
    if native:
        manifest["native_version"] = {"file": native, "pattern": r"^(\d+\.\d+\.\d+(?:\.\d+)?)"}
    write(repo, "eh3d.project.json", json.dumps(manifest, indent=2) + "\n", crlf)
    if native:
        write(repo, native, version + "\n", crlf)
    for rel, label in LANGS.items():
        write(repo, rel, readme(label, version), crlf)
    write(repo, "CHANGELOG.md", changelog(entries, version), crlf)
    if cargo:
        write(repo, "Cargo.toml", f'[package]\nname = "toy"\nversion = "{version}"\nedition = "2021"\n\n[dependencies]\nserde = {{ version = "1" }}\n', crlf)
        write(repo, "Cargo.lock", f'# lock\nversion = 3\n\n[[package]]\nname = "serde"\nversion = "1.0.1"\n\n[[package]]\nname = "toy"\nversion = "{version}"\ndependencies = [\n "serde",\n]\n', crlf)
    if npm:
        write(repo, "package.json", f'{{\n  "name": "toy",\n  "version": "{version}",\n  "dependencies": {{ "left": "1.0.0" }}\n}}\n', crlf)
        write(repo, "package-lock.json", f'{{\n  "name": "toy",\n  "version": "{version}",\n  "lockfileVersion": 3,\n  "packages": {{\n    "": {{\n      "name": "toy",\n      "version": "{version}",\n      "dependencies": {{ "left": "1.0.0" }}\n    }},\n    "node_modules/left": {{\n      "version": "1.0.0"\n    }}\n  }}\n}}\n', crlf)
    if python:
        write(repo, "pyproject.toml", f'[project]\nname = "toy"\nversion = "{version}"\n', crlf)
        write(repo, "src/toy/__init__.py", f'"""Toy."""\n__version__ = "{version}"\n', crlf)
    if gradle:
        write(repo, "app/build.gradle.kts", f'android {{\n    defaultConfig {{ applicationId = "x.y"; versionCode = 7; versionName = "{version}" }}\n}}\n', crlf)
    if ios:
        write(repo, "project.yml", f'name: Toy\nsettings:\n  base:\n    MARKETING_VERSION: "{version}"\n    CURRENT_PROJECT_VERSION: "6"\n', crlf)
    return repo


def git(repo: Path, *args: str) -> str:
    env = dict(os.environ, GIT_AUTHOR_NAME="Toy", GIT_AUTHOR_EMAIL="toy@example.invalid", GIT_COMMITTER_NAME="Toy", GIT_COMMITTER_EMAIL="toy@example.invalid")
    return subprocess.run(["git", *args], cwd=repo, env=env, capture_output=True, text=True, check=True).stdout
