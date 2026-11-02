#!/usr/bin/env python3
# =============================================================================
# EH3D-DOCS - tools/exit_conventions.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""Checks the command-line scripts of tools/ against the exit-code convention of the suite (docs/CONVENTIONS.md).

    python -I tools/exit_conventions.py             # the report; exit 1 when a script differs and is not a known difference
    python -I tools/exit_conventions.py --list      # only the convention

The convention: 0 done and nothing to say, 1 failed (a check found an error, a file could not be read), 2 done but with warnings, 10 done and there is something
to do (the updater's `check`: updates are available), 64 wrong use (an option or argument that does not exist or does not make sense).

For every script of tools/ that is a command (it has a `__main__` guard; the tests and the modules that are only imported are left out) this reads the code and
reports a literal exit code that is not in the convention, and, for a script that uses argparse, runs `--help` (it must end with 0) and an option that does not
exist (it must end with 64). The scripts that are copied into every repository of the suite (the shared tools) are not changed here, so their differences are
listed in KNOWN_DIFFERENCES and are reported as "known"; a new difference is an error.
"""
from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent

#: The exit codes of the command-line tools of the suite.
CODES = {
    0: "done, nothing to say",
    1: "failed: a check found an error, or something could not be read or written",
    2: "done, with warnings (an option such as --strict can turn them into 1)",
    10: "done, and there is something to do (for example updates are available)",
    64: "wrong use: an option or an argument that does not exist or does not make sense",
}

#: The scripts that every repository carries a copy of: they are changed only with a new tools version, so their differences are known, not new.
KNOWN_DIFFERENCES = {
    "make_architecture.py": "a wrong option ends with 2 (argparse), not 64",
    "make_structure.py": "a wrong option ends with 2 (argparse), not 64",
    "status_lights.py": "a wrong option ends with 2 (argparse), not 64",
    "universal_readme_check.py": "a wrong option ends with 2 (argparse), not 64",
}


class UsageParser(argparse.ArgumentParser):
    """An argument parser that ends a wrong use with 64 (argparse alone uses 2)."""

    def error(self, message: str):
        self.print_usage(sys.stderr)
        self.exit(64, f"{self.prog}: error: {message}\n")


def command_scripts(tools_dir: Path) -> list[Path]:
    """The scripts of the folder that are commands: not a test, not a module for importing only."""
    out = []
    for path in sorted(tools_dir.glob("*.py")):
        if path.name.startswith(("test_", "_")) or path.name == Path(__file__).name:
            continue
        if '__name__ == "__main__"' in path.read_text(encoding="utf-8", errors="replace"):
            out.append(path)
    return out


def literal_exit_codes(source: str) -> set[int]:
    """The integer literals the script ends with: what `main` returns and what `sys.exit(...)` or `raise SystemExit(...)` is given."""
    codes: set[int] = set()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            for inner in ast.walk(node):
                if isinstance(inner, ast.Return) and isinstance(inner.value, ast.Constant) and isinstance(inner.value.value, int) and not isinstance(inner.value.value, bool):
                    codes.add(inner.value.value)
        if isinstance(node, ast.Call):
            name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
            if name in ("exit", "SystemExit") and len(node.args) == 1 and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, int):
                codes.add(node.args[0].value)
    return codes


def uses_argparse(source: str) -> bool:
    return "argparse" in source


def run_script(path: Path, *args: str) -> int:
    return subprocess.run([sys.executable, "-I", str(path), *args], capture_output=True, text=True, timeout=120, check=False).returncode


def check_script(path: Path, run: Callable[..., int] = run_script) -> list[str]:
    """What differs from the convention in one script (an empty list when it follows it)."""
    source = path.read_text(encoding="utf-8", errors="replace")
    problems = [f"ends with the code {code}, which the convention does not have" for code in sorted(literal_exit_codes(source) - set(CODES))]
    if uses_argparse(source):
        if (code := run(path, "--help")) != 0:
            problems.append(f"--help ends with {code}, not 0")
        if (code := run(path, "--no-such-option-for-the-check")) != 64:
            problems.append(f"a wrong option ends with {code}, not 64")
    return problems


def check_all(tools_dir: Path = HERE, run: Callable[..., int] = run_script) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """(new differences, known differences) by script name."""
    new: dict[str, list[str]] = {}
    known: dict[str, list[str]] = {}
    for path in command_scripts(tools_dir):
        problems = check_script(path, run)
        if not problems:
            continue
        if path.name in KNOWN_DIFFERENCES and all(p.startswith("a wrong option ends with") for p in problems):
            known[path.name] = problems
        else:
            new[path.name] = problems
    return new, known


def main(argv: list[str] | None = None) -> int:
    parser = UsageParser(description="Checks the scripts of tools/ against the exit-code convention of the suite.")
    parser.add_argument("--list", action="store_true", help="only print the convention")
    parser.add_argument("--tools", type=Path, default=HERE, help="the folder of scripts to check (default: this one)")
    args = parser.parse_args(argv)
    for code, meaning in CODES.items():
        print(f"{code:>3}  {meaning}")
    if args.list:
        return 0
    new, known = check_all(args.tools)
    for name, problems in sorted(known.items()):
        for problem in problems:
            print(f"KNOWN {name}: {problem}")
    for name, problems in sorted(new.items()):
        for problem in problems:
            print(f"DIFFERS {name}: {problem}")
    print(f"EXIT_CONVENTIONS={'FAIL' if new else 'PASS'} scripts={len(command_scripts(args.tools))} differs={len(new)} known={len(known)}")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
