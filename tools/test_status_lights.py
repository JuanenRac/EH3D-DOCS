# =============================================================================
# EH3D-DOCS - tools/test_status_lights.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/status_lights.py: the ceiling of every light, the reading of the table, the check of the eight READMEs and what --apply rewrites."""
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import status_lights as sl

TABLE = (
    "# Toy\n\n## \U0001F6A6 Project status\n\nlegend\n\n| Area | State | What it means here |\n|---|---|---|\n"
    "| Hardware | {h} | on a board |\n| Integration | {i} | with the rest |\n| Software | {s} | the code |\n| Tests | {t} | the suite |\n| Documentation | {d} | the docs |\n\n"
    "## Next\n\ntext\n"
)
LANGS = ("README.md", "README_spa.md", "README_fra.md", "README_ita.md", "README_deu.md", "README_zho.md", "README_jpn.md", "README_por.md")


def table(h=sl.ORANGE, i=sl.ORANGE, s=sl.YELLOW, t=sl.YELLOW, d=sl.YELLOW) -> str:
    return TABLE.format(h=h, i=i, s=s, t=t, d=d)


def make_repo(root: Path, manifest: dict | None = None, text: str | None = None, tests: bool = True, ci: bool = True) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    body = {"name": root.name, "maturity": "functional", "evidence": "host-test"}
    body.update(manifest or {})
    (root / "toy.project.json").write_text(json.dumps(body), encoding="utf-8")
    for name in LANGS:
        (root / name).write_bytes((text if text is not None else table()).encode("utf-8"))
    if tests:
        (root / "tests").mkdir(exist_ok=True)
        (root / "tests" / "test_toy.py").write_text("def test_x():\n    pass\n", encoding="utf-8")
    if ci:
        (root / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
        (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
    return root


def run_main(*argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = sl.main(list(argv))
        except SystemExit as stop:
            code = stop.code if isinstance(stop.code, int) else 1
    return code, out.getvalue(), err.getvalue()


class KindTests(unittest.TestCase):
    def test_labels_are_sorted_into_kinds(self) -> None:
        cases = {
            "Hardware": "hardware", "Firmware on the board": "hardware", "Board": "hardware", "Integration": "integration",
            "Hardware integration": "integration", "Tests": "tests", "Test coverage": "tests", "Documentation": "docs", "Docs": "docs",
            "Software": "software", "Something else": "other", "  software  ": "software",
        }
        for label, kind in cases.items():
            with self.subTest(label=label):
                self.assertEqual(sl.kind_of(label), kind)

    def test_the_order_runs_from_the_worst_light_to_the_best(self) -> None:
        self.assertEqual(sl.ORDER, (sl.RED, sl.ORANGE, sl.YELLOW, sl.GREEN))
        self.assertEqual({v: k for k, v in sl.NAMES.items()}, sl.WORDS)

    def test_the_eight_readme_names_are_the_eight_languages(self) -> None:
        self.assertEqual(len(sl.LANGUAGE_FILES), 8)
        self.assertIn("README_por.md", sl.LANGUAGE_FILES)


class CeilingTests(unittest.TestCase):
    def test_the_evidence_limits_hardware_and_integration(self) -> None:
        for evidence, top in (("none", sl.ORANGE), ("host-test", sl.ORANGE), ("simulator", sl.ORANGE), ("bench", sl.YELLOW), ("field", sl.GREEN)):
            for kind in ("hardware", "integration"):
                with self.subTest(evidence=evidence, kind=kind):
                    self.assertEqual(sl.ceiling(kind, {"evidence": evidence}, True, True, "unknown")[0], top)

    def test_an_unknown_evidence_is_the_lowest_ceiling_not_a_free_pass(self) -> None:
        self.assertEqual(sl.ceiling("hardware", {"evidence": "wishful"}, True, True, "unknown")[0], sl.ORANGE)

    def test_a_missing_evidence_counts_as_none(self) -> None:
        self.assertEqual(sl.ceiling("hardware", {}, True, True, "unknown")[0], sl.ORANGE)

    def test_a_repository_without_hardware_is_not_limited_by_the_evidence(self) -> None:
        top, why = sl.ceiling("hardware", {"evidence": "none", "hardware_bound": False}, True, True, "unknown")
        self.assertEqual(top, sl.GREEN)
        self.assertEqual(why, "no limit")

    def test_software_tests_and_docs_need_tests_and_a_workflow_for_green(self) -> None:
        for kind in ("software", "tests", "docs"):
            with self.subTest(kind=kind):
                self.assertEqual(sl.ceiling(kind, {}, True, True, "unknown"), (sl.GREEN, "no limit"))
                self.assertEqual(sl.ceiling(kind, {}, False, True, "unknown"), (sl.YELLOW, "no tests in the repository"))
                self.assertEqual(sl.ceiling(kind, {}, True, False, "unknown"), (sl.YELLOW, "no CI workflow"))

    def test_a_red_default_branch_lowers_the_software_rows_only(self) -> None:
        self.assertEqual(sl.ceiling("software", {}, True, True, "red")[0], sl.YELLOW)
        self.assertEqual(sl.ceiling("software", {}, True, True, "green")[0], sl.GREEN)
        self.assertEqual(sl.ceiling("other", {}, True, True, "red")[0], sl.GREEN)

    def test_a_low_maturity_lowers_every_row_to_yellow(self) -> None:
        for maturity in sorted(sl.LOW_MATURITY):
            with self.subTest(maturity=maturity):
                top, why = sl.ceiling("other", {"maturity": maturity.upper()}, True, True, "unknown")
                self.assertEqual(top, sl.YELLOW)
                self.assertIn("maturity", why)

    def test_the_lowest_ceiling_wins_and_the_reason_is_the_one_that_set_it(self) -> None:
        top, why = sl.ceiling("hardware", {"maturity": "alpha", "evidence": "none"}, True, True, "unknown")
        self.assertEqual(top, sl.ORANGE)
        self.assertEqual(why, "evidence none")


class TableTests(unittest.TestCase):
    def test_the_table_is_read_after_the_status_heading(self) -> None:
        first, rows = sl.read_table(table())
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0][0], "Hardware")
        self.assertEqual(sl.lights_of(rows), [sl.ORANGE, sl.ORANGE, sl.YELLOW, sl.YELLOW, sl.YELLOW])
        self.assertEqual(table().split("\n")[first].split("|")[1].strip(), "Hardware")

    def test_a_text_without_the_heading_has_no_table(self) -> None:
        self.assertIsNone(sl.read_table("# Toy\n\n## Other\n\n| a | b |\n|---|---|\n| 1 | 2 |\n"))

    def test_a_heading_without_rows_has_no_table(self) -> None:
        self.assertIsNone(sl.read_table("## \U0001F6A6 Project status\n\njust words\n\n## Next\n"))

    def test_a_table_inside_a_code_block_is_not_read(self) -> None:
        text = "```\n## \U0001F6A6 Project status\n| A | B |\n|---|---|\n| x | y |\n```\n"
        self.assertIsNone(sl.read_table(text))

    def test_an_escaped_bar_stays_inside_its_cell(self) -> None:
        text = "## \U0001F6A6 Project status\n\n| Area | State | Note |\n|---|---|---|\n| Soft\\|ware | \U0001F7E1 | a |\n"
        _, rows = sl.read_table(text)
        self.assertEqual(rows[0][0], "Soft\\|ware")
        self.assertEqual(rows[0][1], sl.YELLOW)

    def test_the_lights_are_replaced_row_by_row_and_nothing_else_changes(self) -> None:
        new = sl.replace_lights(table(), [sl.RED, sl.YELLOW, sl.GREEN, sl.ORANGE, sl.RED])
        _, rows = sl.read_table(new)
        self.assertEqual(sl.lights_of(rows), [sl.RED, sl.YELLOW, sl.GREEN, sl.ORANGE, sl.RED])
        self.assertEqual([r[0] for r in rows], ["Hardware", "Integration", "Software", "Tests", "Documentation"])
        self.assertEqual([r[2] for r in rows][0], "on a board")
        self.assertTrue(new.endswith("## Next\n\ntext\n"))

    def test_replacing_with_the_same_lights_changes_nothing(self) -> None:
        text = table()
        _, rows = sl.read_table(text)
        self.assertEqual(sl.replace_lights(text, sl.lights_of(rows)), text)

    def test_a_short_row_has_an_empty_light(self) -> None:
        self.assertEqual(sl.lights_of([["only"], ["a", "b"]]), ["", "b"])


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)

    def test_tests_are_found_by_name_or_by_folder(self) -> None:
        for name in ("test_a.py", "b_test.go", "c.test.ts", "d.spec.js", "ThingTest.kt", "x_test.rs"):
            with self.subTest(name=name):
                root = self.base / name.replace(".", "_")
                root.mkdir()
                (root / name).write_text("x", encoding="utf-8")
                self.assertTrue(sl.has_tests(root))
        folder = self.base / "folder"
        (folder / "tests").mkdir(parents=True)
        (folder / "tests" / "data.txt").write_text("x", encoding="utf-8")
        self.assertTrue(sl.has_tests(folder))

    def test_an_empty_tests_folder_and_skipped_folders_do_not_count(self) -> None:
        root = self.base / "empty"
        (root / "tests").mkdir(parents=True)
        (root / "node_modules" / "pkg").mkdir(parents=True)
        (root / "node_modules" / "pkg" / "test_x.py").write_text("x", encoding="utf-8")
        (root / "src").mkdir()
        (root / "src" / "main.py").write_text("x", encoding="utf-8")
        self.assertFalse(sl.has_tests(root))

    def test_a_workflow_file_is_a_ci(self) -> None:
        root = self.base / "ci"
        self.assertFalse(sl.has_ci(root))
        (root / ".github" / "workflows").mkdir(parents=True)
        self.assertFalse(sl.has_ci(root))
        (root / ".github" / "workflows" / "x.yaml").write_text("n: 1", encoding="utf-8")
        self.assertTrue(sl.has_ci(root))

    def test_the_manifest_is_the_first_project_json(self) -> None:
        root = make_repo(self.base / "m", {"evidence": "bench"})
        self.assertEqual(sl.manifest_of(root)["evidence"], "bench")

    def test_no_manifest_stops_the_tool(self) -> None:
        root = self.base / "none"
        root.mkdir()
        with contextlib.redirect_stderr(io.StringIO()) as err, self.assertRaises(SystemExit):
            sl.manifest_of(root)
        self.assertIn("STATUS_LIGHTS=FAIL", err.getvalue())

    def test_a_manifest_that_is_not_json_stops_the_tool(self) -> None:
        root = self.base / "bad"
        root.mkdir()
        (root / "x.project.json").write_text("{not json", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            sl.manifest_of(root)

    def test_evaluate_gives_every_row_its_kind_and_ceiling(self) -> None:
        root = make_repo(self.base / "e")
        state = sl.evaluate(root, "off")
        self.assertEqual([i["kind"] for i in state["items"]], ["hardware", "integration", "software", "tests", "docs"])
        self.assertEqual([i["ceiling"] for i in state["items"]], [sl.ORANGE, sl.ORANGE, sl.GREEN, sl.GREEN, sl.GREEN])
        self.assertEqual(state["ci"], "unknown")

    def test_evaluate_stops_without_a_readme_or_without_the_table(self) -> None:
        root = make_repo(self.base / "r")
        (root / "README.md").unlink()
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            sl.evaluate(root, "off")
        (root / "README.md").write_text("# nothing\n", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            sl.evaluate(root, "off")


class CheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)

    def test_lights_within_their_ceiling_pass(self) -> None:
        root = make_repo(self.base / "ok")
        self.assertEqual(sl.run_in_ci(root), [])
        code, out, _ = run_main("--check", "--repo", str(root))
        self.assertEqual(code, 0)
        self.assertIn("STATUS_LIGHTS=PASS", out)

    def test_a_light_above_its_ceiling_fails_with_the_reason(self) -> None:
        root = make_repo(self.base / "high", text=table(h=sl.GREEN))
        problems = sl.run_in_ci(root)
        self.assertEqual(len(problems), 1)   # only README.md is judged against the ceiling; the translations agree with it
        state = sl.evaluate(root, "off")
        found = sl.problems_of(root, state)
        self.assertEqual(len(found), 1)
        self.assertIn("is green but the ceiling is orange", found[0])
        self.assertIn("evidence host-test", found[0])

    def test_a_missing_evidence_is_a_problem(self) -> None:
        root = make_repo(self.base / "noev")
        manifest = json.loads((root / "toy.project.json").read_text(encoding="utf-8"))
        del manifest["evidence"]
        (root / "toy.project.json").write_text(json.dumps(manifest), encoding="utf-8")
        found = sl.problems_of(root, sl.evaluate(root, "off"))
        self.assertTrue(any("has no 'evidence'" in line for line in found))

    def test_an_evidence_outside_the_list_is_a_problem(self) -> None:
        root = make_repo(self.base / "badev", {"evidence": "wishful"})
        found = sl.problems_of(root, sl.evaluate(root, "off"))
        self.assertTrue(any("'wishful' is not one of" in line for line in found))

    def test_a_cell_that_is_not_a_light_is_a_problem(self) -> None:
        root = make_repo(self.base / "nolight", text=table(s="ok"))
        found = sl.problems_of(root, sl.evaluate(root, "off"))
        self.assertTrue(any("not a light" in line for line in found))

    def test_a_translation_with_other_lights_is_a_problem(self) -> None:
        root = make_repo(self.base / "drift")
        (root / "README_por.md").write_bytes(table(s=sl.RED).encode("utf-8"))
        found = sl.problems_of(root, sl.evaluate(root, "off"))
        self.assertEqual(found, ["drift/README_por.md: the lights differ from README.md"])

    def test_a_translation_without_the_table_is_a_problem(self) -> None:
        root = make_repo(self.base / "notable")
        (root / "README_deu.md").write_text("# nothing\n", encoding="utf-8")
        found = sl.problems_of(root, sl.evaluate(root, "off"))
        self.assertEqual(found, ["notable/README_deu.md: no Project status table"])

    def test_a_missing_translation_is_left_to_the_readme_checks(self) -> None:
        root = make_repo(self.base / "missing")
        (root / "README_jpn.md").unlink()
        self.assertEqual(sl.problems_of(root, sl.evaluate(root, "off")), [])

    def test_the_ci_gate_is_quiet_when_there_is_no_table_to_judge(self) -> None:
        root = make_repo(self.base / "quiet", text="# nothing\n")
        self.assertEqual(sl.run_in_ci(root), [])

    def test_the_ci_gate_reports_an_unreadable_manifest_instead_of_raising(self) -> None:
        root = make_repo(self.base / "unreadable")
        (root / "toy.project.json").write_text("{", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            found = sl.run_in_ci(root)
        self.assertEqual(len(found), 1)
        self.assertIn("cannot be read", found[0])

    def test_check_exits_one_and_names_the_count(self) -> None:
        root = make_repo(self.base / "failing", text=table(h=sl.GREEN))
        code, _, err = run_main("--check", "--repo", str(root))
        self.assertEqual(code, 1)
        self.assertIn("STATUS_LIGHTS=FAIL", err)


class HydraTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)

    def glance(self, hardware: str) -> None:
        folder = self.base / "HYDRA-UMC-DOCS" / "data"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "glance.json").write_text(json.dumps({"repos": {"HYDRA-UMC-TOY": {"hardware": hardware}}}), encoding="utf-8")

    def test_only_the_hydra_repositories_are_hydra(self) -> None:
        self.assertTrue(sl.is_hydra(Path("HYDRA-UMC")))
        self.assertTrue(sl.is_hydra(Path("HYDRA-UMC-SERVER")))
        self.assertFalse(sl.is_hydra(Path("HYDRA-OTHER")))
        self.assertFalse(sl.is_hydra(Path("EH3D-DOCS")))

    def test_without_the_glance_file_nothing_is_compared(self) -> None:
        root = self.base / "HYDRA-UMC-TOY"
        root.mkdir()
        self.assertIsNone(sl.hydra_entry(root))
        self.assertEqual(sl.hydra_problems(root, {"evidence": "bench"}), [])

    def test_the_manifest_has_to_agree_with_the_glance_file(self) -> None:
        root = self.base / "HYDRA-UMC-TOY"
        root.mkdir()
        for hardware, good, bad in (("not_run", "none", "bench"), ("simulated", "simulator", "field"), ("bench", "bench", "none"), ("in_use", "field", "simulator")):
            self.glance(hardware)
            with self.subTest(hardware=hardware):
                self.assertEqual(sl.hydra_problems(root, {"evidence": good}), [])
                self.assertEqual(len(sl.hydra_problems(root, {"evidence": bad})), 1)

    def test_not_run_accepts_both_none_and_host_test(self) -> None:
        root = self.base / "HYDRA-UMC-TOY"
        root.mkdir()
        self.glance("not_run")
        self.assertEqual(sl.hydra_problems(root, {"evidence": "host-test"}), [])

    def test_not_applicable_needs_a_manifest_without_hardware(self) -> None:
        root = self.base / "HYDRA-UMC-TOY"
        root.mkdir()
        self.glance("not_applicable")
        self.assertEqual(sl.hydra_problems(root, {"evidence": "none", "hardware_bound": False}), [])
        self.assertEqual(len(sl.hydra_problems(root, {"evidence": "none"})), 1)

    def test_a_manifest_without_hardware_cannot_hold_a_hardware_statement(self) -> None:
        root = self.base / "HYDRA-UMC-TOY"
        root.mkdir()
        self.glance("bench")
        found = sl.hydra_problems(root, {"evidence": "bench", "hardware_bound": False})
        self.assertEqual(len(found), 1)
        self.assertIn("hardware_bound false", found[0])

    def test_a_glance_file_that_is_not_json_is_ignored(self) -> None:
        root = self.base / "HYDRA-UMC-TOY"
        root.mkdir()
        folder = self.base / "HYDRA-UMC-DOCS" / "data"
        folder.mkdir(parents=True)
        (folder / "glance.json").write_text("{", encoding="utf-8")
        self.assertIsNone(sl.hydra_entry(root))

    def test_apply_writes_nothing_in_a_hydra_repository(self) -> None:
        root = make_repo(self.base / "HYDRA-UMC-TOY", text=table(h=sl.GREEN))
        before = (root / "README.md").read_bytes()
        code, out, _ = run_main("--apply", "--repo", str(root), "--ci", "off")
        self.assertEqual(code, 0)
        self.assertIn("generated by HYDRA-UMC-DOCS", out)
        self.assertEqual((root / "README.md").read_bytes(), before)


class ApplyTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)

    def lights(self, root: Path, name: str = "README.md") -> list[str]:
        return sl.lights_of(sl.read_table((root / name).read_bytes().decode("utf-8"))[1])

    def test_apply_lowers_a_light_above_its_ceiling_in_the_eight_files(self) -> None:
        root = make_repo(self.base / "lower", text=table(h=sl.GREEN))
        code, out, _ = run_main("--apply", "--repo", str(root), "--ci", "off")
        self.assertEqual(code, 0)
        self.assertIn("8 README file(s) written", out)
        self.assertIn("green -> orange", out)
        for name in LANGS:
            with self.subTest(name=name):
                self.assertEqual(self.lights(root, name)[0], sl.ORANGE)

    def test_apply_does_not_raise_a_light_unless_asked(self) -> None:
        root = make_repo(self.base / "keep", {"evidence": "bench"})
        run_main("--apply", "--repo", str(root), "--ci", "off")
        self.assertEqual(self.lights(root)[0], sl.ORANGE)

    def test_apply_with_raise_moves_a_hardware_light_up_one_step_when_the_evidence_allows(self) -> None:
        root = make_repo(self.base / "raise", {"evidence": "bench"})
        run_main("--apply", "--raise", "--repo", str(root), "--ci", "off")
        self.assertEqual(self.lights(root)[0], sl.YELLOW)
        self.assertEqual(self.lights(root)[2], sl.YELLOW)   # a software light is never raised by this switch

    def test_apply_on_a_repository_that_is_right_writes_nothing(self) -> None:
        root = make_repo(self.base / "same")
        code, out, _ = run_main("--apply", "--repo", str(root), "--ci", "off")
        self.assertEqual(code, 0)
        self.assertIn("0 README file(s) written", out)

    def test_apply_stops_when_a_translation_has_other_rows(self) -> None:
        root = make_repo(self.base / "rows", text=table(h=sl.GREEN))
        (root / "README_fra.md").write_bytes(b"## \xf0\x9f\x9a\xa6 Project status\n\n| A | B |\n|---|---|\n| x | \xf0\x9f\x9f\xa1 |\n")
        with contextlib.redirect_stderr(io.StringIO()):
            code, _, _ = run_main("--apply", "--repo", str(root), "--ci", "off")
        self.assertEqual(code, 1)

    def test_suggest_lists_what_could_be_better_and_what_is_too_high(self) -> None:
        root = make_repo(self.base / "suggest", {"evidence": "bench"}, text=table(h=sl.ORANGE, s=sl.YELLOW, t=sl.GREEN))
        code, out, _ = run_main("--suggest", "--repo", str(root), "--ci", "off")
        self.assertEqual(code, 0)
        self.assertIn("Hardware: orange could reach yellow", out)
        self.assertIn("Software: yellow could reach green", out)
        root2 = make_repo(self.base / "suggest2", text=table(h=sl.GREEN))
        _, out2, _ = run_main("--suggest", "--repo", str(root2), "--ci", "off")
        self.assertIn("is ABOVE its ceiling", out2)

    def test_one_mode_is_required(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            code, _, _ = run_main("--repo", str(self.base))
        self.assertEqual(code, 2)


class MaturityTests(unittest.TestCase):
    def test_a_badge_or_row_that_disagrees_with_the_manifest_is_a_problem(self) -> None:
        badge = '<img src="https://img.shields.io/badge/Maturity-{m}-FFB020.svg" alt="Maturity">\n'
        with tempfile.TemporaryDirectory() as raw:
            root = make_repo(Path(raw) / "Toy", {"maturity": "functional"})
            self.assertEqual(sl.maturity_problems(root, {"maturity": "functional"}), [])
            (root / "README_deu.md").write_bytes((badge.format(m="scaffolding") + table()).encode("utf-8"))
            (root / "README.md").write_bytes((badge.format(m="functional") + "| Maturity | Scaffolding |\n" + table()).encode("utf-8"))
            found = sl.maturity_problems(root, {"maturity": "functional"})
            self.assertEqual(len(found), 2)
            self.assertTrue(any("README_deu.md" in line and "scaffolding" in line for line in found))
            self.assertTrue(any("README.md" in line and "row" in line for line in found))
            self.assertEqual(sl.maturity_problems(root, {}), [])


if __name__ == "__main__":
    unittest.main()
