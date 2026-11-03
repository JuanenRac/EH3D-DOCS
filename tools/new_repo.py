#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/new_repo.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Makes the folder of a new repository of the suite with the base every repository has.

    python -I tools/new_repo.py EH3D-NEW-THING --dest ..                  # creates ../EH3D-NEW-THING
    python -I tools/new_repo.py EH3D-NEW-THING --dest .. --role library --stack rust --description "What it is for"

What is made, from the template in docs/templates/new_repo/ and from the files of this repository:

    eh3d.project.json, VERSION, CHANGELOG.md          the manifest (scaffolding), the version file and a first changelog entry
    README.md and the seven translations              the universal layout, in the eight languages, with the project status in honest lights
    LICENSE, CODE_OF_CONDUCT.md, CONTRIBUTING.md, SECURITY.md, SUPPORT.md, .gitignore, .gitattributes
    .github/                                          the CI workflow, the dashboard notice, the issue forms and the pull-request template
    tools/                                            the shared tools of this hub (the same code as here) and a test of the base
    docs/architecture.json, docs/structure.json       the data of the two pictures, which are drawn into images/ together with a banner

When it has finished it runs the repository check (`tools/ci_validate.py`) and the two picture checks in the new folder and tells the result. It does not run git, so the
folder is not a repository yet: `git init`, a first commit and the creation of the repository on GitHub are yours. It refuses to write into a folder that exists.
Exit codes (docs/CONVENTIONS.md): 0 made and the checks pass, 1 made but a check fails, or it could not be made, 64 wrong use.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TEMPLATE = ROOT / "docs" / "templates" / "new_repo"
NAME = re.compile(r"^EH3D-[A-Z0-9]+(-[A-Z0-9]+)*$")
ROLES = ("api", "ui", "cli", "firmware", "library", "service", "tool", "node", "docs")
VERSION = re.compile(r"^\d+\.\d+\.\d+$")
#: README file, language code and the way the language is shown in the language bar.
LANGUAGES = (
    ("en", "README.md", "🇺🇸", "English"),
    ("es", "README_spa.md", "🇪🇸", "Español"),
    ("fr", "README_fra.md", "🇫🇷", "Français"),
    ("it", "README_ita.md", "🇮🇹", "Italiano"),
    ("de", "README_deu.md", "🇩🇪", "Deutsch"),
    ("zh", "README_zho.md", "🇨🇳", "中文"),
    ("ja", "README_jpn.md", "🇯🇵", "日本語"),
    ("pt", "README_por.md", "🇵🇹", "Português"),
)
#: The sections of the "Jump to" line.
JUMP_SECTIONS = ("h_overview", "h_architecture", "h_quickstart", "h_testing", "h_structure", "h_related")
#: Files of this repository that are copied into the new one as they are.
COPIED = ("LICENSE", "CODE_OF_CONDUCT.md", ".gitignore", ".gitattributes", ".github/PULL_REQUEST_TEMPLATE.md", ".github/workflows/dashboard-dispatch.yml")
COPIED_FOLDERS = (".github/ISSUE_TEMPLATE",)


class UsageParser(argparse.ArgumentParser):
    """An argument parser that ends a wrong use with exit code 64, as docs/CONVENTIONS.md says."""

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")


class NewRepoError(Exception):
    """The folder cannot be made."""


def _sync_module():
    spec = importlib.util.spec_from_file_location("eh3d_new_repo_sync", HERE / "sync_shared_tools.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fill(text: str, values: dict[str, str]) -> str:
    """Replaces every @@key@@ of a template."""
    for key, value in values.items():
        text = text.replace(f"@@{key}@@", value)
    return text


def anchor(title: str) -> str:
    """The link GitHub gives to a heading whose first word is an icon: `#-` and the title in lower case with hyphens."""
    slug = re.sub(r"[^\w\s-]", "", title.lower(), flags=re.UNICODE).strip().replace(" ", "-")
    return "#-" + slug


def language_bar(current: str) -> str:
    parts = []
    for code, file, flag, label in LANGUAGES:
        parts.append(f"{flag} <b>{label}</b>" if code == current else f'<a href="{file}">{flag} {label}</a>')
    return '<p align="center">' + " | ".join(parts) + "</p>"


def build_readme(lang: str, texts: dict, name: str, version: str, tests: int, tree: str, description: str | None, banner: str) -> str:
    t = {key: value.replace("{name}", name).replace("{tests}", str(tests)).replace("{version}", version) for key, value in texts.items()}
    if description and lang == "en":
        t["description"] = description
    values = dict(t)
    values["banner_file"] = banner
    values["language_bar"] = language_bar(lang)
    values["jump_links"] = " · ".join(f"[{t[key]}]({anchor(t[key])})" for key in JUMP_SECTIONS)
    values["tree"] = tree
    template = (TEMPLATE / "README.md.tpl").read_text(encoding="utf-8")
    template = template.replace("{name}", name).replace("{tests}", str(tests)).replace("{version}", version)
    return fill(template, values)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))


def copy_shared_tools(repo: Path) -> list[str]:
    """Puts the shared tools of this hub in the tools/ of the new repository: the same code, with a header that names the new repository."""
    sync = _sync_module()
    done = []
    for tool in sync.SHARED:
        source = HERE / tool
        if not source.is_file():
            continue
        head, body = sync.split_header(source.read_text(encoding="utf-8"))
        lines = [line for line in head.replace("\r\n", "\n").split("\n")]
        shebang = [lines[0]] if lines and lines[0].startswith("#!") else []
        new_head = shebang + [
            "# =============================================================================",
            f"# {repo.name} - tools/{tool}",
            "# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>",
            "# GPL-3.0-or-later - see LICENSE",
            "# =============================================================================",
        ]
        canonical = sync.canonical_line(head)
        if canonical:
            new_head.append(canonical)
        write(repo / "tools" / tool, "\n".join(new_head) + "\n" + body)
        done.append(tool)
    return done


def run_tool(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-I", "-B", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600, check=False)


def create(dest: Path, name: str, *, role: str = "tool", stack: str = "scaffold", family: str = "CNC Workflow Tools", version: str = "0.0.1", description: str | None = None) -> Path:
    """Makes `dest/name` and returns it. Raises NewRepoError when it cannot."""
    if not NAME.match(name):
        raise NewRepoError(f"{name!r} is not a repository name of the suite (EH3D- and capital letters, digits and hyphens)")
    if role not in ROLES:
        raise NewRepoError(f"the role is one of {', '.join(ROLES)}")
    if not VERSION.match(version):
        raise NewRepoError("the version is MAJOR.MINOR.PATCH")
    repo = dest / name
    if repo.exists():
        raise NewRepoError(f"{repo} exists: nothing was written")
    texts = json.loads((TEMPLATE / "readme_texts.json").read_text(encoding="utf-8"))
    tests = len(re.findall(r"(?m)^\s+def test_", (TEMPLATE / "test_repository.py").read_text(encoding="utf-8")))
    banner = name.replace("-", "_") + "_BANNER.svg"
    values = {"name": name, "version": version, "role": role, "stack": stack, "family": family}
    try:
        repo.mkdir(parents=True)
        for rel in COPIED:
            if (ROOT / rel).is_file():
                write(repo / rel, (ROOT / rel).read_text(encoding="utf-8"))
        for folder in COPIED_FOLDERS:
            for source in sorted((ROOT / folder).glob("*")):
                if source.is_file():
                    write(repo / folder / source.name, source.read_text(encoding="utf-8"))
        write(repo / ".github" / "workflows" / "ci.yml", (TEMPLATE / "ci.yml").read_text(encoding="utf-8"))
        write(repo / "VERSION", version + "\n")
        for rel in ("eh3d.project.json", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", "SUPPORT.md"):
            write(repo / rel, fill((TEMPLATE / rel).read_text(encoding="utf-8"), values))
        write(repo / "docs" / "architecture.json", fill((TEMPLATE / "architecture.json").read_text(encoding="utf-8"), values))
        write(repo / "docs" / "structure.json", fill((TEMPLATE / "structure.json").read_text(encoding="utf-8"), values))
        font = max(30, min(72, int(1040 / (len(name) * 0.62))))
        write(repo / "images" / banner, fill((TEMPLATE / "banner.svg").read_text(encoding="utf-8"), {**values, "font_size": str(font)}))
        write(repo / "tools" / "test_repository.py", fill((TEMPLATE / "test_repository.py").read_text(encoding="utf-8"), values))
        copy_shared_tools(repo)
        trees = {}
        for code, _file, _flag, _label in LANGUAGES:
            result = run_tool(repo, "tools/make_structure.py", "--tree", code)
            if result.returncode != 0:
                raise NewRepoError(f"the tree of the structure in {code} could not be drawn: {(result.stdout + result.stderr).strip()}")
            trees[code] = result.stdout.replace("\r\n", "\n").rstrip("\n")
        for code, file, _flag, _label in LANGUAGES:
            write(repo / file, build_readme(code, texts[code], name, version, tests, trees[code], description, banner))
        for script in ("tools/make_architecture.py", "tools/make_structure.py"):
            result = run_tool(repo, script)
            if result.returncode != 0:
                raise NewRepoError(f"{script} failed: {(result.stdout + result.stderr).strip()}")
    except NewRepoError:
        raise
    except OSError as error:
        raise NewRepoError(f"could not write {repo}: {error}") from error
    return repo


def check(repo: Path) -> list[str]:
    """Runs the repository check and the two picture checks in the new folder; returns the lines of what fails."""
    problems = []
    if not (repo / ".git").exists():  # the checks read what git tracks and fail when git does not answer
        subprocess.run(["git", "init", "-q"], cwd=repo, capture_output=True, check=False)
    for args in (("tools/ci_validate.py",), ("tools/make_architecture.py", "--check"), ("tools/make_structure.py", "--check", "--readmes")):
        result = run_tool(repo, *args)
        if result.returncode != 0:
            problems.append(f"{' '.join(args)}: " + " | ".join(line.strip() for line in (result.stdout + result.stderr).splitlines() if line.strip())[:600])
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = UsageParser(description="Makes the folder of a new repository of the suite with the base every repository has.")
    parser.add_argument("name", help="the name of the repository, for example EH3D-NEW-THING")
    parser.add_argument("--dest", type=Path, required=True, help="the folder that will hold the new one (the workspace)")
    parser.add_argument("--role", default="tool", help="role in the manifest (default: tool)")
    parser.add_argument("--stack", default="scaffold", help="stack in the manifest (default: scaffold)")
    parser.add_argument("--family", default="CNC Workflow Tools", help="family in the manifest (default: %(default)s)")
    parser.add_argument("--version", default="0.0.1", help="first version (default: %(default)s)")
    parser.add_argument("--description", help="the one-line description of the English README")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        if args.role not in ROLES:
            parser.error(f"the role is one of {', '.join(ROLES)}")
        if not VERSION.match(args.version):
            parser.error("the version is MAJOR.MINOR.PATCH")
        if not NAME.match(args.name):
            parser.error(f"{args.name!r} is not a repository name of the suite (EH3D- and capital letters, digits and hyphens)")
        repo = create(args.dest, args.name, role=args.role, stack=args.stack, family=args.family, version=args.version, description=args.description)
    except NewRepoError as error:
        print(f"NEW_REPO=FAIL {error}", file=sys.stderr)
        return 1
    problems = check(repo)
    for problem in problems:
        print(f"  FAIL {problem}")
    print(f"NEW_REPO={'FAIL' if problems else 'PASS'} {repo}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
