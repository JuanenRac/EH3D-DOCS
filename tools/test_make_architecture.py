# =============================================================================
# EH3D-DOCS - tools/test_make_architecture.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""A malformed architecture spec ends with an ARCHITECTURE=FAIL line, not a traceback, and the code references cannot leave the repository."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("eh3d_make_architecture", TOOLS / "make_architecture.py")
ARCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARCH)


def _spec() -> dict:
    return json.loads((TOOLS.parent / "docs" / "architecture.json").read_text(encoding="utf-8"))


def _run(root: Path) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = ARCH.run(root, False, None)
    return code, out.getvalue()


class MalformedSpecTests(unittest.TestCase):
    def test_a_line_given_as_a_list_without_a_tone_is_a_fail_line(self):
        spec = _spec()
        spec["nodes"][0]["lines"] = [["only the text"]]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "docs").mkdir()
            (root / "docs" / "architecture.json").write_text(json.dumps(spec), encoding="utf-8")
            code, text = _run(root)
        self.assertEqual(code, 1)
        self.assertIn("ARCHITECTURE=FAIL", text)

    def test_a_code_reference_cannot_leave_the_repository(self):
        spec = {"nodes": [{"id": "a", "code": ["../outside.txt", "/etc/passwd::root"]}]}
        problems = ARCH.check_code_refs(spec, Path(tempfile.gettempdir()))
        self.assertEqual(len(problems), 2)
        self.assertTrue(all("inside the repository" in problem for problem in problems))

    def test_a_spec_of_the_wrong_shape_is_a_spec_error_and_not_a_crash(self):
        for node in ("text", 5, ["a"]):
            spec = _spec()
            spec["nodes"] = [node]
            with self.assertRaises(ARCH.SpecError):
                ARCH.validate_spec(spec)
        spec = _spec()
        spec["nodes"][0]["code"] = "src/a.py"
        with self.assertRaises(ARCH.SpecError):
            ARCH.validate_spec(spec)
        spec = _spec()
        spec["edges"] = ["a-b"]
        with self.assertRaises(ARCH.SpecError):
            ARCH.validate_spec(spec)

    def test_the_example_of_the_docstring_does_not_use_a_trivial_search_text(self):
        self.assertNotIn("::9", ARCH.__doc__)

    def test_a_structure_spec_of_the_wrong_shape_is_a_spec_error(self):
        spec_file = importlib.util.spec_from_file_location("eh3d_make_structure", TOOLS / "make_structure.py")
        structure = importlib.util.module_from_spec(spec_file)
        spec_file.loader.exec_module(structure)
        base = json.loads((TOOLS.parent / "docs" / "structure.json").read_text(encoding="utf-8"))
        for cards in ("text", ["card"], [{"name": "docs/", "rows": ["row"]}], [{"name": "docs/", "rows": "row"}]):
            spec = dict(base)
            spec["cards"] = cards
            with self.assertRaises(structure.SpecError):
                structure.validate_spec(spec)


if __name__ == "__main__":
    unittest.main()
