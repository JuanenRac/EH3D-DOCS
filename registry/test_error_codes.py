"""Coherence of the registry of container codes (EH3D-PKG.md).

The registry must list the codes 001..N without gaps or repeats, every row must be complete, and,
when the container crate is checked out next to this repository, the titles must be the ones the
crate reports.
"""

import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "EH3D-PKG.md"
CODES_RS = HERE.parent.parent / "EH3D-COMMON" / "crates" / "container" / "src" / "codes.rs"
ROW = re.compile(r"^\| (EH3D-PKG-(\d{3})) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$")


def rows():
    found = []
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        if line.startswith("| EH3D-PKG-"):
            match = ROW.match(line)
            if not match:
                raise AssertionError(f"malformed row: {line}")
            found.append(match.groups())
    return found


class RegistryTests(unittest.TestCase):
    def test_codes_are_numbered_without_gaps_or_repeats(self):
        numbers = [int(r[1]) for r in rows()]
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))
        self.assertEqual(len(numbers), 14)

    def test_every_row_is_complete(self):
        for code, _number, title, rule, raised_by in rows():
            for text in (title, rule, raised_by):
                self.assertTrue(text.strip(), code)
            self.assertTrue(rule.strip().endswith("."), f"{code}: the rule is a sentence")

    def test_titles_are_unique(self):
        titles = [r[2].strip() for r in rows()]
        self.assertEqual(len(titles), len(set(titles)))

    @unittest.skipUnless(CODES_RS.exists(), "EH3D-COMMON is not checked out next to this repository")
    def test_titles_match_the_container_crate(self):
        source = CODES_RS.read_text(encoding="utf-8")
        crate_titles = dict(re.findall(r'PkgCode::(\w+) => "([^"]+)"', source))
        self.assertEqual(len(crate_titles), 14)
        self.assertEqual(sorted(crate_titles.values()), sorted(r[2].strip() for r in rows()))


if __name__ == "__main__":
    unittest.main()
