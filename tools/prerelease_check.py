#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/prerelease_check.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""What has to be up to date before a release of a repository is published. It publishes nothing and changes nothing.

    python tools/prerelease_check.py REPOSITORY [--workspace FOLDER] [--no-ci] [--allow-short]

It checks, and prints one OK / WARN / SKIP / FAIL line for each:
  versions   the same version in every file that carries it (the manifest, Cargo, npm, Python, Gradle, project.yml, the eight
             README files) and in the newest section of the CHANGELOG
  changelog  a section for that version, nothing left in [Unreleased], at least 3 entries (a warning; --allow-short accepts it)
  readmes    the eight README files have the "Project status" table and show the same lights
  git        a clean working tree and no commit that is not on the remote
  validate   the repository's own tools/ci_validate.py ends in PASS
  ci         every GitHub Actions run of the commit that is checked out has finished and is green (needs `gh`; it is skipped,
             and says so, when `gh` is not installed or not logged in)
The last line is PRERELEASE=PASS or PRERELEASE=FAIL; the exit code is 1 on FAIL."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))

import release_notes  # noqa: E402
import version_places as vp  # noqa: E402

Runner = Callable[[list[str], Path], tuple[int, str]]
Result = tuple[str, str, str]  # (OK | WARN | SKIP | FAIL, check, detail)


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    try:
        done = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=600, encoding="utf-8", errors="replace")
    except (OSError, subprocess.TimeoutExpired) as error:
        return 127, str(error)
    return done.returncode, done.stdout + done.stderr


def check_versions(root: Path) -> list[Result]:
    try:
        problems = vp.check(vp.Repo(root))
    except vp.VersionError as error:
        return [("FAIL", "versions", str(error))]
    if problems:
        return [("FAIL", "versions", problem) for problem in problems]
    return [("OK", "versions", f"every place holds {vp.manifest_version(vp.Repo(root))}")]


def check_changelog(root: Path, allow_short: bool) -> list[Result]:
    try:
        code, lines = release_notes.check(root)
    except vp.VersionError as error:
        return [("FAIL", "changelog", str(error))]
    status = {0: "OK", 1: "FAIL", 2: "OK" if allow_short else "WARN"}[code]
    return [(status, "changelog", line.split(" ", 1)[1]) for line in lines]


def check_readmes(root: Path) -> list[Result]:
    import ci_validate

    lights, results = {}, []
    for name in vp.READMES:
        path = root / name
        if not path.is_file():
            results.append(("FAIL", "readmes", f"{name} is missing"))
            continue
        found = ci_validate.status_lights(path.read_text(encoding="utf-8"))
        if found is None:
            results.append(("FAIL", "readmes", f"{name} has no valid 'Project status' table"))
        lights[name] = found
    english = lights.get("README.md")
    for name, found in lights.items():
        if found is not None and english is not None and found != english:
            results.append(("FAIL", "readmes", f"{name} shows other lights than README.md"))
    return results or [("OK", "readmes", "eight README files with the same status lights")]


def check_git(root: Path, runner: Runner) -> list[Result]:
    code, out = runner(["git", "status", "--porcelain"], root)
    if code != 0:
        return [("FAIL", "git", f"git status failed: {out.strip()[:120]}")]
    results: list[Result] = []
    if out.strip():
        results.append(("FAIL", "git", f"the working tree is not clean ({len(out.strip().splitlines())} paths)"))
    code, out = runner(["git", "rev-list", "--count", "@{upstream}..HEAD"], root)
    if code != 0:
        results.append(("FAIL", "git", "the branch has no remote branch to compare with"))
    elif out.strip() != "0":
        results.append(("FAIL", "git", f"{out.strip()} commits are not on the remote"))
    return results or [("OK", "git", "clean tree, nothing left to push")]


def check_validate(root: Path, runner: Runner) -> list[Result]:
    script = root / "tools" / "ci_validate.py"
    if not script.is_file():
        return [("FAIL", "validate", "tools/ci_validate.py is missing")]
    code, out = runner([sys.executable, "-I", "tools/ci_validate.py"], root)
    if code == 0 and "CI_VALIDATION=PASS" in out:
        return [("OK", "validate", "ci_validate ends in PASS")]
    fails = [line.strip() for line in out.splitlines() if "FAIL" in line][:5]
    return [("FAIL", "validate", "; ".join(fails) or "ci_validate did not end in PASS")]


def remote_slug(root: Path, runner: Runner) -> str | None:
    code, out = runner(["git", "remote", "get-url", "origin"], root)
    found = re.search(r"github\.com[:/]([^/\s]+/[^/\s]+?)(?:\.git)?\s*$", out) if code == 0 else None
    return found.group(1) if found else None


def check_ci(root: Path, runner: Runner, have_gh: bool | None = None) -> list[Result]:
    if have_gh is None:
        have_gh = shutil.which("gh") is not None
    if not have_gh:
        return [("SKIP", "ci", "`gh` is not installed: look at the Actions page of the commit by hand")]
    slug = remote_slug(root, runner)
    code, sha = runner(["git", "rev-parse", "HEAD"], root)
    if slug is None or code != 0:
        return [("SKIP", "ci", "the remote is not a GitHub repository")]
    sha = sha.strip()
    code, out = runner(["gh", "run", "list", "-R", slug, "--commit", sha, "--limit", "30", "--json", "name,status,conclusion"], root)
    if code != 0:
        return [("SKIP", "ci", f"`gh` could not list the runs ({out.strip()[:100]})")]
    try:
        runs = json.loads(out or "[]")
    except ValueError:
        return [("SKIP", "ci", "`gh` answered something that is not JSON")]
    if not runs:
        return [("FAIL", "ci", f"no run of GitHub Actions for {sha[:10]}: push the commit and wait for the CI")]
    bad = [f"{r.get('name')}: {r.get('conclusion') or r.get('status')}" for r in runs if not (r.get("status") == "completed" and r.get("conclusion") in ("success", "skipped", "neutral"))]
    if bad:
        return [("FAIL", "ci", f"not green for {sha[:10]} - " + "; ".join(bad))]
    return [("OK", "ci", f"{len(runs)} runs of {sha[:10]} are green")]


def prerelease(root: Path, runner: Runner = run, allow_short: bool = False, with_ci: bool = True, have_gh: bool | None = None) -> tuple[int, list[str]]:
    results: list[Result] = []
    results += check_versions(root)
    results += check_changelog(root, allow_short)
    results += check_readmes(root)
    results += check_git(root, runner)
    results += check_validate(root, runner)
    if with_ci:
        results += check_ci(root, runner, have_gh)
    lines = [f"{status:4} {name}: {detail}" for status, name, detail in results]
    failed = any(status == "FAIL" for status, _, _ in results)
    lines.append(f"PRERELEASE={'FAIL' if failed else 'PASS'} {root.name}")
    return (1 if failed else 0), lines


class UsageParser(argparse.ArgumentParser):
    """An argument parser that ends a wrong use with exit code 64, as docs/CONVENTIONS.md says for the command-line tools of the suite (argparse alone uses 2)."""

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = UsageParser(description="What has to be up to date before a release is published.")
    parser.add_argument("repository")
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--no-ci", action="store_true", help="do not ask GitHub for the runs of the commit")
    parser.add_argument("--allow-short", action="store_true", help="a CHANGELOG section with fewer than 3 entries is accepted")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    from bump_version import resolve

    root = resolve(args.repository, args.workspace)
    if not (root / vp.MANIFEST).is_file():
        print(f"FAIL {root} has no {vp.MANIFEST}")
        return 1
    code, lines = prerelease(root, allow_short=args.allow_short, with_ci=not args.no_ci)
    for line in lines:
        print(line)
    return code


if __name__ == "__main__":
    sys.exit(main())
