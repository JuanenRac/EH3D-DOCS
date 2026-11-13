# =============================================================================
# EH3D-DOCS - tools/test_validate_workflow.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The reusable workflow .github/workflows/validate.yml and its guide agree (no YAML library: the text is read)."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"
GUIDE = ROOT / "docs" / "REUSABLE_VALIDATION.md"


def inputs(text: str) -> dict[str, str]:
    """{name: default} of the inputs declared under `workflow_call`."""
    block = re.search(r"(?ms)^on:\s*\n  workflow_call:\s*\n    inputs:\s*\n(.*?)^(?=\S)", text)
    if not block:
        return {}
    out = {}
    for item in re.finditer(r"(?ms)^      ([a-z-]+):\s*\n(.*?)(?=^      [a-z-]+:|\Z)", block.group(1)):
        default = re.search(r'default:\s*"?([^"\n]+)"?', item.group(2))
        out[item.group(1)] = default.group(1) if default else ""
    return out


class ReusableWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")
        self.guide = GUIDE.read_text(encoding="utf-8")

    def test_it_is_a_reusable_workflow_that_only_reads(self) -> None:
        self.assertIn("workflow_call:", self.text)
        self.assertNotIn("secrets:", self.text)
        self.assertRegex(self.text, r"(?m)^permissions:\n  contents: read$")

    def test_the_inputs_are_the_four_the_guide_documents_with_the_same_defaults(self) -> None:
        declared = inputs(self.text)
        self.assertEqual(declared, {"python-version": "3.12", "check-pictures": "true", "check-links": "false", "run-tool-tests": "false"})
        for name, default in declared.items():
            row = re.search(r"(?m)^\| `%s` \|[^\n]*" % re.escape(name), self.guide)
            self.assertIsNotNone(row, f"{name} is not in the table of the guide")
            self.assertIn(default, row.group(0), name)

    def test_every_input_is_used_by_a_step(self) -> None:
        for name in inputs(self.text):
            self.assertIn(f"inputs.{name}", self.text, name)

    def test_the_guide_shows_how_to_call_it_with_a_tag(self) -> None:
        self.assertIn("uses: JuanenRac/EH3D-DOCS/.github/workflows/validate.yml@<tag>", self.guide)

    def test_the_ci_of_this_repository_calls_the_reusable_workflow_with_all_its_checks(self) -> None:
        ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("uses: ./.github/workflows/validate.yml", ci)
        for option in ("check-pictures: true", "check-links: true", "run-tool-tests: true"):
            self.assertIn(option, ci)
        for command in ("python -I tools/ci_validate.py", "python -I tools/make_architecture.py --check", "python -I tools/make_structure.py --check --readmes",
                        "python -I tools/check_links.py", 'python -I -m unittest discover -s tools -p "test_*.py"'):
            self.assertIn(command, self.text)


if __name__ == "__main__":
    unittest.main()
