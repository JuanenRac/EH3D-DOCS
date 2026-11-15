# =============================================================================
# EH3D-DOCS - tools/test_pretty_run.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/pretty_run.py: how it counts the tests of every runner, the steps of a panel, the wrapping of a script and the exit code it gives back."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

import pretty_run as pr


def quiet(function, *args, **kwargs):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        result = function(*args, **kwargs)
    return result, out.getvalue()


class CountTests(unittest.TestCase):
    def test_unittest(self) -> None:
        self.assertEqual(pr.count_tests("Ran 12 tests in 0.1s\n\nOK\n"), (12, 0))
        self.assertEqual(pr.count_tests("Ran 1 test in 0.1s\n\nOK\n"), (1, 0))

    def test_unittest_with_failures_and_errors(self) -> None:
        self.assertEqual(pr.count_tests("Ran 10 tests in 1s\n\nFAILED (failures=2, errors=1)\n"), (7, 3))
        self.assertEqual(pr.count_tests("Ran 5 tests in 1s\n\nFAILED (errors=2)\n"), (3, 2))

    def test_pytest(self) -> None:
        self.assertEqual(pr.count_tests("=== 8 passed in 0.3s ==="), (8, 0))
        self.assertEqual(pr.count_tests("=== 2 failed, 6 passed in 0.3s ==="), (6, 2))

    def test_vitest(self) -> None:
        self.assertEqual(pr.count_tests(" Tests  120 passed (120)\n"), (120, 0))
        self.assertEqual(pr.count_tests(" Tests  3 failed | 117 passed (120)\n"), (117, 3))

    def test_node(self) -> None:
        self.assertEqual(pr.count_tests("ℹ pass 9\nℹ fail 1\n"), (9, 1))

    def test_ctest(self) -> None:
        self.assertEqual(pr.count_tests("90% tests passed, 1 tests failed out of 10"), (9, 1))
        self.assertEqual(pr.count_tests("100% tests passed, 0 tests failed out of 4"), (4, 0))

    def test_cargo_adds_every_binary(self) -> None:
        text = "test result: ok. 20 passed; 0 failed; 0 ignored\ntest result: FAILED. 3 passed; 2 failed; 0 ignored\n"
        self.assertEqual(pr.count_tests(text), (23, 2))

    def test_an_output_without_a_count_is_zero(self) -> None:
        self.assertEqual(pr.count_tests(""), (0, 0))
        self.assertEqual(pr.count_tests("compiling...\nfinished"), (0, 0))

    def test_the_public_names(self) -> None:
        self.assertEqual(set(pr.__all__), {"Panel", "count_tests"})


class FormatTests(unittest.TestCase):
    def test_seconds_below_a_minute_have_one_decimal(self) -> None:
        self.assertEqual(pr._seconds(0.04), "0.0 s")
        self.assertEqual(pr._seconds(12.34), "12.3 s")

    def test_a_minute_or_more_is_written_in_minutes(self) -> None:
        self.assertEqual(pr._seconds(60), "1 min 00 s")
        self.assertEqual(pr._seconds(125.9), "2 min 05 s")
        self.assertEqual(pr._seconds(3600), "60 min 00 s")

    def test_without_a_terminal_the_colour_codes_are_not_written(self) -> None:
        if not pr._TTY:
            self.assertEqual(pr._c("31", "text"), "text")


class PanelTests(unittest.TestCase):
    def panel(self) -> pr.Panel:
        panel = pr.Panel("TOY", "test", "1.2.3")
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        panel.log_path = Path(self._tmp.name) / "log.txt"
        return panel

    def test_the_banner_names_the_project_mode_and_version(self) -> None:
        _, out = quiet(self.panel().banner)
        self.assertIn("TOY", out)
        self.assertIn("TEST", out)
        self.assertIn("v1.2.3", out)

    def test_a_command_that_succeeds_is_an_ok_step(self) -> None:
        panel = self.panel()
        ok, out = quiet(panel.step, "Say hello", [sys.executable, "-c", "print('hello')"])
        self.assertTrue(ok)
        self.assertEqual([(s[0], s[1]) for s in panel.steps], [("Say hello", "ok")])
        self.assertIn("Say hello", out)

    def test_a_command_that_fails_is_a_failed_step_and_shows_its_output(self) -> None:
        panel = self.panel()
        ok, out = quiet(panel.step, "Break", [sys.executable, "-c", "print('the reason'); raise SystemExit(3)"])
        self.assertFalse(ok)
        self.assertEqual(panel.steps[0][1], "fail")
        self.assertIn("the reason", out)

    def test_a_missing_program_is_a_failed_step_and_not_a_crash(self) -> None:
        panel = self.panel()
        ok, out = quiet(panel.step, "Nothing", ["this-program-does-not-exist-eh3d"])
        self.assertFalse(ok)
        self.assertIn("was not found", out)

    def test_the_tests_of_a_step_are_added_up(self) -> None:
        panel = self.panel()
        quiet(panel.step, "Tests", [sys.executable, "-c", "print('Ran 12 tests in 0.1s'); print('OK')"], tests=True)
        quiet(panel.step, "More", [sys.executable, "-c", "print('Ran 3 tests in 0.1s'); print('OK')"], tests=True)
        self.assertEqual((panel.passed, panel.failed), (15, 0))
        self.assertEqual(panel.steps[0][3], "12 tests")

    def test_a_skipped_step_is_kept_with_its_reason_and_does_not_fail(self) -> None:
        panel = self.panel()
        quiet(panel.skip, "Browser", "no browser")
        self.assertEqual(panel.steps, [("Browser", "skip", 0.0, "no browser")])
        code, out = quiet(panel.finish)
        self.assertEqual(code, 0)
        self.assertIn("1 skipped", out)

    def test_a_failure_that_is_not_a_command_counts(self) -> None:
        panel = self.panel()
        quiet(panel.fail, "Tool", "it is missing")
        code, out = quiet(panel.finish)
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("failed: Tool", out)

    def test_a_clean_run_finishes_with_zero_and_writes_the_log(self) -> None:
        panel = self.panel()
        quiet(panel.step, "One", [sys.executable, "-c", "print('line of the log')"])
        code, out = quiet(panel.finish, "extra words")
        self.assertEqual(code, 0)
        self.assertIn("PASS", out)
        self.assertIn("1/1 steps", out)
        self.assertIn("extra words", out)
        self.assertIn("line of the log", panel.log_path.read_text(encoding="utf-8"))

    def test_failed_tests_alone_fail_the_run(self) -> None:
        panel = self.panel()
        panel.failed = 1
        code, _ = quiet(panel.finish)
        self.assertEqual(code, 1)

    def test_a_note_is_printed_dimmed_but_complete(self) -> None:
        _, out = quiet(self.panel().note, "careful")
        self.assertIn("careful", out)

    def test_an_unwritable_log_does_not_break_the_summary(self) -> None:
        panel = self.panel()
        panel.log_path = Path(self._tmp.name) / "no" / "such" / "folder" / "log.txt"
        code, _ = quiet(panel.finish)
        self.assertEqual(code, 0)


class WrapTests(unittest.TestCase):
    def script(self, body: str) -> Path:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        path = Path(self._tmp.name) / "run.py"
        path.write_text(body, encoding="utf-8")
        return path

    def wrap(self, body: str) -> tuple[int, str, pr.Panel]:
        path = self.script(body)
        panel = pr.Panel("TOY", "build")
        panel.log_path = Path(self._tmp.name) / "log.txt"
        code, out = quiet(panel.wrap, [sys.executable, str(path)])
        return code, out, panel

    def test_numbered_markers_make_the_steps(self) -> None:
        code, out, panel = self.wrap("print('banner')\nprint('[1/2] Compile')\nprint('Ran 4 tests in 0s')\nprint('[2/2] Package')\nprint('done')\n")
        self.assertEqual(code, 0)
        self.assertEqual([(s[0], s[1]) for s in panel.steps], [("Compile", "ok"), ("Package", "ok")])
        self.assertEqual(panel.passed, 4)
        self.assertNotIn("banner", out)

    def test_command_lines_make_the_steps_when_there_are_no_markers(self) -> None:
        _, _, panel = self.wrap("print('+ cargo build')\nprint('+ cargo test')\n")
        self.assertEqual([s[0] for s in panel.steps], ["cargo build", "cargo test"])

    def test_the_step_that_was_running_is_the_one_that_fails(self) -> None:
        code, out, panel = self.wrap("import sys\nprint('[1/2] First')\nprint('[2/2] Second')\nprint('went wrong')\nsys.exit(5)\n")
        self.assertEqual(code, 5)
        self.assertEqual([(s[0], s[1]) for s in panel.steps], [("First", "ok"), ("Second", "fail")])
        self.assertIn("went wrong", out)

    def test_a_script_without_steps_is_one_step(self) -> None:
        code, _, panel = self.wrap("print('just output')\n")
        self.assertEqual(code, 0)
        self.assertEqual([(s[0], s[1]) for s in panel.steps], [("run", "ok")])

    def test_a_script_that_fails_without_steps_still_fails(self) -> None:
        code, _, panel = self.wrap("raise SystemExit(7)\n")
        self.assertEqual(code, 7)
        self.assertTrue(any(s[1] == "fail" for s in panel.steps))

    def test_a_program_that_does_not_exist_is_a_failed_start(self) -> None:
        panel = pr.Panel("TOY", "build")
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        panel.log_path = Path(self._tmp.name) / "log.txt"
        code, _ = quiet(panel.wrap, ["no-such-program-eh3d"])
        self.assertEqual(code, 1)
        self.assertEqual(panel.steps[0][0], "Start")

    def test_the_wrapper_needs_a_command(self) -> None:
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(pr._wrap_main(["--wrap"]), 2)
        self.assertIn("usage", err.getvalue())


if __name__ == "__main__":
    unittest.main()
