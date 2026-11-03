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


if __name__ == "__main__":
    unittest.main()
