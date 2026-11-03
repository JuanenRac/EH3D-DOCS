# =============================================================================
# EH3D-DOCS - tools/test_sync_shared_tools.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The comparison of the copies of the shared tools (tools/sync_shared_tools.py)."""
from __future__ import annotations

import importlib.util
import json
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


def full_hub(root: Path) -> None:
    """EH3D-DOCS holding a canonical copy of every shared tool, as the real hub does."""
    for tool in SYNC.SHARED:
        make(root, "EH3D-DOCS", "print(1)" + chr(10), tool)


class SyncSharedToolsTests(unittest.TestCase):
    def test_a_shared_tool_without_a_canonical_copy_fails_the_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS", "print(1)" + chr(10))
            self.assertEqual(len(SYNC.missing_canonical(root)), len(SYNC.SHARED) - 1)
            SYNC.main(["--workspace", str(root), "--lock"])
            self.assertEqual(SYNC.main(["--workspace", str(root), "--check"]), 1)
            full_hub(root)
            self.assertEqual(SYNC.missing_canonical(root), [])

    def test_a_lock_that_is_not_an_object_and_a_foreign_repo_name_are_told(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            full_hub(root)
            SYNC.write_lock(root)
            SYNC.lock_path(root).write_text("[1]", encoding="utf-8")
            self.assertEqual(SYNC.lock_problems(root), ["docs/vendored.lock must hold a JSON object"])
            for bad in ("../x", "OTHER", "EH3D-X/../..", ""):
                with self.assertRaises(SystemExit):
                    SYNC.write_copy(root, "ci_validate.py", bad)

    def test_the_name_in_the_header_is_not_a_difference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            full_hub(root)
            make(root, "EH3D-ISOCAM", "print(1)\n")
            self.assertEqual(SYNC.differing(root), {})
            self.assertEqual(SYNC.main(["--workspace", str(root), "--lock"]), 0)
            self.assertEqual(SYNC.main(["--workspace", str(root), "--check"]), 0)

    def test_a_copy_that_was_changed_is_told_and_fails_the_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS", "print(1)\n")
            make(root, "EH3D-ISOCAM", "print(1)\n")
            make(root, "EH3D-SERVER", "print(2)\n")
            SYNC.main(["--workspace", str(root), "--lock"])
            self.assertEqual(SYNC.differing(root), {"ci_validate.py": ["EH3D-SERVER"]})
            self.assertEqual(len(SYNC.report(root)["ci_validate.py"]), 2)
            self.assertEqual(SYNC.main(["--workspace", str(root)]), 0)  # the report alone never fails
            self.assertEqual(SYNC.main(["--workspace", str(root), "--check"]), 1)

    def test_a_copy_is_written_with_its_own_header_and_only_when_it_is_asked_for_by_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS", "print(1)\n")
            other = make(root, "EH3D-SERVER", "print(2)\n")
            self.assertEqual(SYNC.main(["--workspace", str(root), "--write"]), 64)
            self.assertEqual(SYNC.main(["--workspace", str(root), "--write", "--only", "ci_validate.py", "--repo", "EH3D-SERVER"]), 0)
            text = other.read_text(encoding="utf-8")
            self.assertIn("# EH3D-SERVER - tools/ci_validate.py", text)
            self.assertTrue(text.endswith("print(1)\n"))
            self.assertEqual(SYNC.differing(root), {})

    def test_the_canonical_line_of_the_header_goes_with_the_code_and_a_stale_one_is_told(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = make(root, "EH3D-DOCS", "print(1)\n")
            docs.write_text(docs.read_text(encoding="utf-8").replace("# ====\nprint", "# ====\n# canonical: EH3D-DOCS tools 4\nprint"), encoding="utf-8")
            other = make(root, "EH3D-SERVER", "print(2)\n")
            self.assertEqual(len(SYNC.canonical_problems(root)), 1)
            SYNC.write_copy(root, "ci_validate.py", "EH3D-SERVER")
            text = other.read_text(encoding="utf-8")
            self.assertEqual(text.count("# canonical:"), 1)
            self.assertIn("# canonical: EH3D-DOCS tools 4\nprint(1)", text)
            self.assertEqual(SYNC.canonical_problems(root), [])
            # raising the version in EH3D-DOCS replaces the line, it does not add another
            docs.write_text(docs.read_text(encoding="utf-8").replace("tools 4", "tools 5"), encoding="utf-8")
            self.assertEqual(len(SYNC.canonical_problems(root)), 1)
            SYNC.write_copy(root, "ci_validate.py", "EH3D-SERVER")
            self.assertEqual(other.read_text(encoding="utf-8").count("# canonical:"), 1)
            self.assertEqual(SYNC.canonical_problems(root), [])

    def test_the_lock_names_the_origin_and_notices_a_tool_changed_after_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            full_hub(root)
            docs = root / "EH3D-DOCS" / "tools" / "ci_validate.py"
            self.assertEqual(len(SYNC.lock_problems(root)), 1)  # no lock yet
            SYNC.write_lock(root)
            self.assertEqual(SYNC.lock_problems(root), [])
            self.assertEqual(json.loads(SYNC.lock_path(root).read_text(encoding="utf-8"))["origin"], "EH3D-DOCS")
            docs.write_text(docs.read_text(encoding="utf-8").replace("print(1)", "print(3)"), encoding="utf-8")
            self.assertEqual(len(SYNC.lock_problems(root)), 1)
            self.assertEqual(SYNC.main(["--workspace", str(root), "--check"]), 1)
            SYNC.write_lock(root)
            self.assertEqual(SYNC.main(["--workspace", str(root), "--check"]), 0)

    def test_a_header_change_alone_does_not_make_the_lock_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = make(root, "EH3D-DOCS", "print(1)\n")
            SYNC.write_lock(root)
            docs.write_text(docs.read_text(encoding="utf-8").replace("# GPL", "# GPL-3.0-or-later"), encoding="utf-8")
            self.assertEqual(SYNC.lock_problems(root), [])

    def test_a_broken_lock_is_told(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS", "print(1)\n")
            SYNC.write_lock(root)
            SYNC.lock_path(root).write_text("{", encoding="utf-8")
            self.assertEqual(SYNC.lock_problems(root), ["docs/vendored.lock is not valid JSON"])

    def test_folders_that_are_not_of_the_suite_are_left_alone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            make(root, "EH3D-DOCS", "print(1)\n")
            make(root, "ARMOR-STUDIO", "print(9)\n")
            self.assertEqual(list(SYNC.report(root)["ci_validate.py"].values()), [["EH3D-DOCS"]])


class OwnCopyTests(unittest.TestCase):
    def test_a_copy_a_repository_keeps_on_purpose_is_not_a_difference_and_is_never_written(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            full_hub(root)
            make(root, "ELECTRO-HOBBY-3D-UPDATER", "print('its own checks')")
            self.assertEqual(SYNC.differing(root), {})
            self.assertEqual(SYNC.canonical_problems(root), [])
            with self.assertRaises(SystemExit):
                SYNC.write_copy(root, "ci_validate.py", "ELECTRO-HOBBY-3D-UPDATER")


if __name__ == "__main__":
    unittest.main()
