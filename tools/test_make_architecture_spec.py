# =============================================================================
# EH3D-DOCS - tools/test_make_architecture_spec.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""tools/make_architecture.py: the rules of the specification, the layout, the picture it draws and the check of the code it points to."""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
import xml.dom.minidom
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
SPEC = importlib.util.spec_from_file_location("eh3d_make_architecture_spec", TOOLS / "make_architecture.py")
ARCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARCH)


def real_spec() -> dict:
    return json.loads((ROOT / "docs" / "architecture.json").read_text(encoding="utf-8"))


def small_spec() -> dict:
    return {
        "repo": "EH3D-TOY", "ecosystem": "eh3d", "description": "A toy.",
        "nodes": [
            {"id": "a", "column": 0, "level": "external", "title": "Caller", "lines": ["one line"]},
            {"id": "b", "column": 1, "level": "tested", "title": "Core", "lines": [["first", "ok"], ["second", "muted"]], "code": ["src/core.py::def run"]},
            {"id": "c", "column": 1, "level": "untested", "title": "Board", "lines": ["not run"]},
            {"id": "d", "column": 2, "level": "contract", "title": "Server", "lines": ["the API"]},
        ],
        "edges": [{"from": "a", "to": "b"}, {"from": "b", "to": "d", "level": "contract"}, {"from": "b", "to": "c"}],
    }


def broken(change) -> dict:
    spec = small_spec()
    change(spec)
    return spec


class ValidateTests(unittest.TestCase):
    def test_the_small_spec_and_the_real_one_are_valid(self) -> None:
        ARCH.validate_spec(small_spec())
        ARCH.validate_spec(real_spec())

    def test_each_required_key_is_required(self) -> None:
        for key in ("repo", "ecosystem", "description", "nodes"):
            spec = small_spec()
            del spec[key]
            with self.subTest(key=key), self.assertRaisesRegex(ARCH.SpecError, key):
                ARCH.validate_spec(spec)

    def test_the_number_of_nodes_is_limited(self) -> None:
        spec = small_spec()
        spec["nodes"] = [{"id": f"n{i}", "column": 1, "title": "x"} for i in range(ARCH.MAX_NODES + 1)]
        with self.assertRaisesRegex(ARCH.SpecError, "between 1 and"):
            ARCH.validate_spec(spec)
        spec["nodes"] = []
        with self.assertRaises(ARCH.SpecError):
            ARCH.validate_spec(spec)

    def test_a_node_needs_an_id_a_column_and_a_title(self) -> None:
        for key in ("id", "column", "title"):
            spec = small_spec()
            del spec["nodes"][1][key]
            with self.subTest(key=key), self.assertRaisesRegex(ARCH.SpecError, key):
                ARCH.validate_spec(spec)

    def test_ids_are_unique(self) -> None:
        spec = broken(lambda s: s["nodes"][2].update(id="b"))
        with self.assertRaisesRegex(ARCH.SpecError, "duplicate"):
            ARCH.validate_spec(spec)

    def test_the_column_is_zero_one_or_two(self) -> None:
        spec = broken(lambda s: s["nodes"][0].update(column=3))
        with self.assertRaisesRegex(ARCH.SpecError, "column must be"):
            ARCH.validate_spec(spec)

    def test_the_level_is_one_of_the_five(self) -> None:
        self.assertEqual(ARCH.LEVELS, ("tested", "contract", "config", "untested", "external"))
        spec = broken(lambda s: s["nodes"][0].update(level="shiny"))
        with self.assertRaisesRegex(ARCH.SpecError, "level must be"):
            ARCH.validate_spec(spec)

    def test_a_tone_must_be_a_known_one(self) -> None:
        spec = broken(lambda s: s["nodes"][1].update(lines=[["text", "loud"]]))
        with self.assertRaisesRegex(ARCH.SpecError, "tone 'loud'"):
            ARCH.validate_spec(spec)

    def test_the_repository_column_cannot_be_empty(self) -> None:
        spec = broken(lambda s: [n.update(column=0) for n in s["nodes"]])
        with self.assertRaisesRegex(ARCH.SpecError, "column 1"):
            ARCH.validate_spec(spec)

    def test_an_edge_needs_two_nodes_that_exist(self) -> None:
        for end in ("from", "to"):
            spec = small_spec()
            spec["edges"][0][end] = "missing"
            with self.subTest(end=end), self.assertRaisesRegex(ARCH.SpecError, "not a node id"):
                ARCH.validate_spec(spec)

    def test_an_edge_cannot_join_the_two_outer_columns(self) -> None:
        spec = small_spec()
        spec["edges"].append({"from": "a", "to": "d"})
        with self.assertRaisesRegex(ARCH.SpecError, "outer columns"):
            ARCH.validate_spec(spec)

    def test_an_edge_level_must_be_known(self) -> None:
        spec = small_spec()
        spec["edges"][0]["level"] = "shiny"
        with self.assertRaisesRegex(ARCH.SpecError, "unknown level"):
            ARCH.validate_spec(spec)

    def test_an_unknown_ecosystem_is_refused(self) -> None:
        spec = small_spec()
        spec["ecosystem"] = "no-such-family"
        with self.assertRaises(Exception):
            ARCH.validate_spec(spec)


class LoadTests(unittest.TestCase):
    def test_a_missing_file_is_named(self) -> None:
        with tempfile.TemporaryDirectory() as folder, self.assertRaisesRegex(ARCH.SpecError, "does not exist"):
            ARCH.load_spec(Path(folder) / "none.json")

    def test_a_file_that_is_not_json_is_named(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "a.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaisesRegex(ARCH.SpecError, "not valid JSON"):
                ARCH.load_spec(path)

    def test_a_good_file_is_loaded_and_validated(self) -> None:
        self.assertEqual(ARCH.load_spec(ROOT / "docs" / "architecture.json")["repo"], "EH3D-DOCS")

    def test_the_digest_follows_the_content_and_not_the_order_of_keys(self) -> None:
        a = small_spec()
        b = dict(reversed(list(small_spec().items())))
        self.assertEqual(ARCH.spec_digest(a), ARCH.spec_digest(b))
        b["description"] = "other"
        self.assertNotEqual(ARCH.spec_digest(a), ARCH.spec_digest(b))
        self.assertEqual(len(ARCH.spec_digest(a)), 16)


class NodeTests(unittest.TestCase):
    def test_the_first_plain_line_is_primary_and_the_rest_are_muted(self) -> None:
        self.assertEqual(ARCH.node_lines({"lines": ["a", "b", "c"]}), [("a", "primary"), ("b", "muted"), ("c", "muted")])

    def test_a_line_with_a_tone_keeps_it(self) -> None:
        self.assertEqual(ARCH.node_lines({"lines": [["a", "warn"], "b"]}), [("a", "warn"), ("b", "muted")])

    def test_a_node_without_lines_has_none(self) -> None:
        self.assertEqual(ARCH.node_lines({}), [])

    def test_a_box_grows_with_its_lines_and_an_untested_one_is_taller(self) -> None:
        one = ARCH.node_height({"lines": ["a"]})
        three = ARCH.node_height({"lines": ["a", "b", "c"]})
        self.assertEqual(three - one, 36)
        self.assertEqual(ARCH.node_height({}), one)
        self.assertEqual(ARCH.node_height({"lines": ["a"], "level": "untested"}) - one, 12)

    def test_every_level_has_a_style_and_every_tone_a_colour(self) -> None:
        pal = ARCH.K.palette("eh3d")
        for level in ARCH.LEVELS:
            with self.subTest(level=level):
                style = ARCH.level_style(level, pal)
                self.assertEqual(set(style), {"stroke", "title", "sw", "dash"})
        for tone in ARCH.TONES:
            with self.subTest(tone=tone):
                self.assertRegex(ARCH.tone_color(tone, pal), r"^#[0-9A-Fa-f]{6}$")

    def test_a_configuration_level_is_dashed_and_a_contract_is_thicker(self) -> None:
        pal = ARCH.K.palette("eh3d")
        self.assertIsNotNone(ARCH.level_style("config", pal)["dash"])
        self.assertIsNone(ARCH.level_style("tested", pal)["dash"])
        self.assertGreater(ARCH.level_style("contract", pal)["sw"], ARCH.level_style("tested", pal)["sw"])

    def test_the_default_legend_names_every_level(self) -> None:
        self.assertEqual(set(ARCH.DEFAULT_LEGEND), set(ARCH.LEVELS))
        self.assertEqual(len(ARCH.DEFAULT_COLUMNS), 3)


class LayoutTests(unittest.TestCase):
    def test_every_node_gets_a_box_inside_the_picture(self) -> None:
        for spec in (small_spec(), real_spec()):
            lay = ARCH.layout(spec)
            self.assertEqual(set(lay["boxes"]), {n["id"] for n in spec["nodes"]})
            for name, box in lay["boxes"].items():
                with self.subTest(name=name):
                    self.assertGreaterEqual(box["x"], 0)
                    self.assertLessEqual(box["x"] + box["w"], ARCH.W)
                    self.assertGreaterEqual(box["y"], ARCH.TOP)
                    self.assertGreater(box["h"], 0)

    def test_the_outer_columns_are_only_made_when_a_node_is_in_them(self) -> None:
        spec = small_spec()
        spec["nodes"] = [n for n in spec["nodes"] if n["column"] == 1]
        spec["edges"] = [{"from": "b", "to": "c"}]
        lay = ARCH.layout(spec)
        self.assertEqual(lay["present"], set())
        self.assertEqual(lay["container"]["x"], ARCH.MARGIN)
        full = ARCH.layout(small_spec())
        self.assertEqual(full["present"], {0, 2})
        self.assertGreater(full["container"]["x"], ARCH.MARGIN)

    def test_the_repository_cards_use_more_columns_as_they_grow(self) -> None:
        def cards(n: int) -> set[float]:
            spec = {"repo": "R", "ecosystem": "eh3d", "description": "d", "nodes": [{"id": f"n{i}", "column": 1, "title": "t"} for i in range(n)]}
            return {round(b["x"]) for b in ARCH.layout(spec)["boxes"].values()}
        self.assertEqual(len(cards(3)), 1)
        self.assertEqual(len(cards(6)), 2)
        self.assertEqual(len(cards(10)), 3)

    def test_a_column_that_is_too_tall_is_refused(self) -> None:
        spec = small_spec()
        spec["nodes"] = [{"id": f"s{i}", "column": 0, "title": "t", "lines": ["a", "b", "c", "d", "e"]} for i in range(6)] + [{"id": "m", "column": 1, "title": "m"}]
        spec["edges"] = []
        with self.assertRaisesRegex(ARCH.SpecError, "too tall"):
            ARCH.layout(spec)

    def test_edges_get_a_path_for_each_one(self) -> None:
        spec = small_spec()
        geometry = ARCH.edge_geometry(spec, ARCH.layout(spec))
        self.assertEqual(len(geometry), len(spec["edges"]))
        for item in geometry:
            self.assertIsInstance(item, dict)


class DrawingTests(unittest.TestCase):
    def test_the_picture_is_well_formed_xml_with_every_title(self) -> None:
        spec = small_spec()
        svg = ARCH.build_svg(spec)
        xml.dom.minidom.parseString(svg.encode("utf-8"))
        for node in spec["nodes"]:
            self.assertIn(node["title"], svg)
        self.assertTrue(svg.lstrip().startswith("<svg"))

    def test_the_same_spec_draws_the_same_picture(self) -> None:
        self.assertEqual(ARCH.build_svg(small_spec()), ARCH.build_svg(small_spec()))

    def test_a_change_in_a_title_changes_the_picture(self) -> None:
        other = copy.deepcopy(small_spec())
        other["nodes"][1]["title"] = "Another"
        self.assertNotEqual(ARCH.build_svg(small_spec()), ARCH.build_svg(other))

    def test_the_picture_of_the_real_spec_is_what_is_in_the_repository(self) -> None:
        drawn = ARCH.build_svg(real_spec())
        stored = (ROOT / "images" / "architecture.svg").read_text(encoding="utf-8")
        self.assertEqual(ARCH.K.normalise(stored), drawn)

    def test_special_characters_in_a_text_are_escaped(self) -> None:
        spec = small_spec()
        spec["nodes"][1]["title"] = "A & B <c>"
        svg = ARCH.build_svg(spec)
        xml.dom.minidom.parseString(svg.encode("utf-8"))
        self.assertNotIn("A & B <c>", svg)


class CodeReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        (self.root / "src").mkdir()
        (self.root / "src" / "core.py").write_text("def run():\n    pass\n", encoding="utf-8")

    def refs(self, *code: str) -> list[str]:
        return ARCH.check_code_refs({"nodes": [{"id": "n", "code": list(code)}]}, self.root)

    def test_a_file_that_exists_is_fine(self) -> None:
        self.assertEqual(self.refs("src/core.py"), [])

    def test_a_text_that_is_in_the_file_is_fine(self) -> None:
        self.assertEqual(self.refs("src/core.py::def run"), [])

    def test_a_text_that_is_gone_is_named(self) -> None:
        self.assertEqual(self.refs("src/core.py::def stop"), ["node 'n': src/core.py no longer contains 'def stop'"])

    def test_a_missing_file_is_named(self) -> None:
        self.assertIn("does not exist", self.refs("src/none.py")[0])

    def test_a_folder_cannot_contain_a_text(self) -> None:
        self.assertIn("is a folder", self.refs("src::def run")[0])
        self.assertEqual(self.refs("src"), [])

    def test_paths_that_leave_the_repository_are_refused(self) -> None:
        found = self.refs("../x", "/etc/passwd", "a/../../x", chr(92) + "windows")
        self.assertEqual(len(found), 4)
        self.assertTrue(all("inside the repository" in line for line in found))


class RunTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        (self.root / "docs").mkdir()
        (self.root / "src").mkdir()
        (self.root / "src" / "core.py").write_text("def run():\n    pass\n", encoding="utf-8")
        (self.root / "docs" / "architecture.json").write_text(json.dumps(small_spec()), encoding="utf-8")

    def go(self, check: bool) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = ARCH.run(self.root, check, None)
        return code, out.getvalue()

    def test_write_then_check_passes(self) -> None:
        code, out = self.go(False)
        self.assertEqual((code, "ARCHITECTURE=WRITTEN" in out), (0, True))
        code, out = self.go(True)
        self.assertEqual(code, 0)
        self.assertIn("ARCHITECTURE=PASS EH3D-TOY (4 boxes)", out)

    def test_check_without_a_picture_fails_and_says_to_run_the_tool(self) -> None:
        code, out = self.go(True)
        self.assertEqual(code, 1)
        self.assertIn("does not exist (run tools/make_architecture.py)", out)

    def test_check_fails_when_the_picture_is_stale(self) -> None:
        self.go(False)
        spec = small_spec()
        spec["nodes"][1]["title"] = "Renamed"
        (self.root / "docs" / "architecture.json").write_text(json.dumps(spec), encoding="utf-8")
        code, out = self.go(True)
        self.assertEqual(code, 1)
        self.assertIn("does not match docs/architecture.json", out)

    def test_check_fails_when_the_code_it_points_to_changed(self) -> None:
        self.go(False)
        (self.root / "src" / "core.py").write_text("pass\n", encoding="utf-8")
        code, out = self.go(True)
        self.assertEqual(code, 1)
        self.assertIn("no longer contains", out)

    def test_a_malformed_spec_is_one_fail_line(self) -> None:
        (self.root / "docs" / "architecture.json").write_text("{}", encoding="utf-8")
        code, out = self.go(False)
        self.assertEqual(code, 1)
        self.assertTrue(out.startswith("ARCHITECTURE=FAIL the spec is malformed"))

    def test_main_checks_the_repository_it_is_given(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(ARCH.main(["--root", str(ROOT), "--check"]), 0)
        self.assertIn("ARCHITECTURE=PASS EH3D-DOCS", out.getvalue())


if __name__ == "__main__":
    unittest.main()
