# =============================================================================
# EH3D-DOCS - tools/test_sync_shared_tools.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The comparison of the copies of the shared tools (tools/sync_shared_tools.py)."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("eh3d_sync_shared_tools", TOOLS / "sync_shared_tools.py")
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


def make(root: Path, name: str, body: str, tool: str = "ci_validate.py") -> Path:
    tools = root / name / "tools"
    tools.mkdir(parents=True, exist_ok=True)
    f = tools / tool
    f.write_text(f"# ====\n# {name} - tools/{tool}\n# GPL\n# ====\n{body}", encoding="utf-8")
    return f


class SyncSharedToolsTests(unittest.TestCase):
    def test_the_name_in_the_header_is_not_a_difference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS", "print(1)\n")
            make(root, "EH3D-ISOCAM", "print(1)\n")
            self.assertEqual(SYNC.differing(root), {})
            self.assertEqual(SYNC.main(["--workspace", str(root), "--check"]), 0)

    def test_a_copy_that_was_changed_is_told_and_fails_the_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS", "print(1)\n")
            make(root, "EH3D-ISOCAM", "print(1)\n")
            make(root, "EH3D-SERVER", "print(2)\n")
            self.assertEqual(SYNC.differing(root), {"ci_validate.py": ["EH3D-SERVER"]})
            self.assertEqual(len(SYNC.report(root)["ci_validate.py"]), 2)
            self.assertEqual(SYNC.main(["--workspace", str(root)]), 0)  # the report alone never fails
            self.assertEqual(SYNC.main(["--workspace", str(root), "--check"]), 1)

    def test_a_copy_is_written_with_its_own_header_and_only_when_it_is_asked_for_by_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS", "print(1)\n")
            other = make(root, "EH3D-SERVER", "print(2)\n")
            self.assertEqual(SYNC.main(["--workspace", str(root), "--write"]), 2)
            self.assertEqual(SYNC.main(["--workspace", str(root), "--write", "--only", "ci_validate.py", "--repo", "EH3D-SERVER"]), 0)
            text = other.read_text(encoding="utf-8")
            self.assertIn("# EH3D-SERVER - tools/ci_validate.py", text)
            self.assertTrue(text.endswith("print(1)\n"))
            self.assertEqual(SYNC.differing(root), {})

    def test_folders_that_are_not_of_the_suite_are_left_alone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS", "print(1)\n")
            make(root, "ARMOR-STUDIO", "print(9)\n")
            self.assertEqual(list(SYNC.report(root)["ci_validate.py"].values()), [["EH3D-DOCS"]])


if __name__ == "__main__":
    unittest.main()
