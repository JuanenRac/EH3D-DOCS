# =============================================================================
# EH3D-DOCS - tools/test_check_links.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The link check: titles, query strings, %20, root-relative links, exact case and non-UTF-8 files."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("eh3d_check_links", TOOLS / "check_links.py")
LINKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINKS)


def check(files: dict[str, bytes]) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        for name, data in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_bytes(data)
        old = LINKS.ROOT
        LINKS.ROOT = root
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = LINKS.main()
        finally:
            LINKS.ROOT = old
    return code, out.getvalue()


class LinkTests(unittest.TestCase):
    def test_good_links_with_a_title_a_query_a_space_and_a_root_path_pass(self):
        text = '[a](other.md "title") [b](other.md?x=1#top) [c](my%20file.md) [d](/docs/x.md) [e](<my file.md>)'
        code, out = check({"README.md": text.encode(), "other.md": b"x", "my file.md": b"x", "docs/x.md": b"x"})
        self.assertEqual((code, "LINKS=PASS" in out), (0, True), out)

    def test_a_link_to_a_missing_file_or_to_the_wrong_case_fails(self):
        code, out = check({"README.md": b"[a](missing.md) [b](Other.md)", "other.md": b"x"})
        self.assertEqual(code, 1)
        self.assertIn("missing.md", out)
        self.assertIn("Other.md", out)

    def test_a_tilde_fence_and_build_folders_are_skipped_and_bad_bytes_do_not_crash(self):
        files = {"README.md": b"~~~\n[a](nope.md)\n~~~\n", "node_modules/p/README.md": b"[a](nope.md)", "latin.md": b"caf\xe9 [a](README.md)"}
        code, out = check(files)
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
