# =============================================================================
# EH3D-DOCS - tools/test_exit_conventions.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The exit-code convention of the command-line scripts of tools/ (tools/exit_conventions.py)."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("eh3d_exit_conventions", TOOLS / "exit_conventions.py")
CONVENTIONS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONVENTIONS)


class ConventionTests(unittest.TestCase):
    def test_the_codes_are_the_ones_the_conventions_document_names(self) -> None:
        self.assertEqual(sorted(CONVENTIONS.CODES), [0, 1, 2, 10, 64])
        text = (TOOLS.parent / "docs" / "CONVENTIONS.md").read_text(encoding="utf-8")
        for code in CONVENTIONS.CODES:
            self.assertIn(f"`{code}`", text, f"docs/CONVENTIONS.md does not describe the exit code {code}")

    def test_literal_codes_are_read_from_main_and_from_exit_calls(self) -> None:
        source = (
            "import sys\n"
            "def helper():\n    return 48\n"
            "def main():\n    if x:\n        return 1\n    return 0\n"
            "if __name__ == '__main__':\n    sys.exit(main())\n"
            "def other():\n    raise SystemExit(3)\n"
        )
        self.assertEqual(CONVENTIONS.literal_exit_codes(source), {0, 1, 3})

    def test_a_script_that_ends_with_a_code_outside_the_convention_differs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "tool.py"
            script.write_text("def main():\n    return 7\n", encoding="utf-8")
            problems = CONVENTIONS.check_script(script)
            self.assertEqual(len(problems), 1)
            self.assertIn("7", problems[0])

    def test_argparse_scripts_are_run_with_help_and_a_wrong_option(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "tool.py"
            script.write_text("import argparse\ndef main():\n    return 0\n", encoding="utf-8")
            calls = []

            def fake(path, *args):
                calls.append(args)
                return 0 if args == ("--help",) else 2

            problems = CONVENTIONS.check_script(script, fake)
            self.assertEqual(calls, [("--help",), ("--no-such-option-for-the-check",)])
            self.assertEqual(problems, ["a wrong option ends with 2, not 64"])

    def test_a_script_without_argparse_is_not_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "tool.py"
            script.write_text("def main():\n    return 0\n", encoding="utf-8")
            self.assertEqual(CONVENTIONS.check_script(script, lambda *a: self.fail("it must not run")), [])

    def test_tests_and_modules_are_not_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, body in (("tool.py", 'if __name__ == "__main__":\n    pass\n'), ("test_tool.py", 'if __name__ == "__main__":\n    pass\n'), ("_helper.py", 'if __name__ == "__main__":\n    pass\n'), ("lib.py", "x = 1\n")):
                (root / name).write_text(body, encoding="utf-8")
            self.assertEqual([p.name for p in CONVENTIONS.command_scripts(root)], ["tool.py"])

    def test_the_parser_of_the_convention_ends_a_wrong_use_with_64(self) -> None:
        parser = CONVENTIONS.UsageParser(prog="x")
        parser.add_argument("--ok")
        with self.assertRaises(SystemExit) as caught:
            parser.parse_args(["--nope"])
        self.assertEqual(caught.exception.code, 64)


class ScriptsOfThisRepositoryTests(unittest.TestCase):
    def test_every_script_of_tools_follows_the_convention_except_the_known_shared_ones(self) -> None:
        new, known = CONVENTIONS.check_all(TOOLS)
        self.assertEqual(new, {}, "a script of tools/ differs from the exit-code convention of docs/CONVENTIONS.md")
        self.assertLessEqual(set(known), set(CONVENTIONS.KNOWN_DIFFERENCES))


if __name__ == "__main__":
    unittest.main()
