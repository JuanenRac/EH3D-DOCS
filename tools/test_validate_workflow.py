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
        default = re.search(r"default:[ \t]*([^\n]*)", item.group(2))
        value = default.group(1).strip() if default else ""
        if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[item.group(1)] = value
    return out


class ReusableWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")
        self.guide = GUIDE.read_text(encoding="utf-8")

    def test_it_is_a_reusable_workflow_that_only_reads(self) -> None:
        self.assertIn("workflow_call:", self.text)
        self.assertNotIn("secrets:", self.text)
        self.assertRegex(self.text, r"(?m)^permissions:\n  contents: read$")

    def test_the_inputs_are_those_the_guide_documents_with_the_same_defaults(self) -> None:
        declared = inputs(self.text)
        self.assertEqual(
            declared,
            {
                "python-version": "3.12",
                "check-pictures": "true",
                "check-links": "false",
                "run-tool-tests": "false",
                "isolated": "true",
                "os": '["ubuntu-latest"]',
                "timeout-minutes": "15",
            },
        )
        for name, default in declared.items():
            row = re.search(r"(?m)^\| `%s` \|[^\n]*" % re.escape(name), self.guide)
            self.assertIsNotNone(row, f"{name} is not in the table of the guide")
            self.assertIn(default, row.group(0), name)

    def test_every_input_is_used_by_a_step(self) -> None:
        for name in inputs(self.text):
            self.assertIn(f"inputs.{name}", self.text, name)

    def test_the_guide_shows_how_to_call_it_with_a_tag(self) -> None:
        self.assertIn("uses: JuanenRac/EH3D-DOCS/.github/workflows/validate.yml@<tag>", self.guide)

    def test_the_steps_are_those_of_the_ci_of_this_repository(self) -> None:
        ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        for command in ("python -I tools/ci_validate.py", "python -I tools/make_architecture.py --check", "python -I tools/make_structure.py --check --readmes",
                        "python -I tools/check_links.py", 'python -I -m unittest discover -s tools -p "test_*.py"'):
            self.assertIn(command, ci)
            # the workflow writes the isolation flag as a variable, so that a repository can turn it off
            self.assertIn(command.replace("python -I", "python $PYFLAGS"), self.text)

    def test_the_new_inputs_keep_the_behaviour_of_a_call_that_names_none(self) -> None:
        # isolated by default: the flag is -I unless the input says otherwise
        self.assertIn("PYFLAGS: ${{ inputs.isolated && '-I' || '' }}", self.text)
        # one runner by default, and the name of the check is the one the callers already wait for
        self.assertIn("os: ${{ fromJSON(inputs.os) }}", self.text)
        self.assertIn("runs-on: ${{ matrix.os }}", self.text)
        self.assertIn("|| 'Validate the repository' }}", self.text)
        self.assertIn("timeout-minutes: ${{ inputs.timeout-minutes }}", self.text)
        self.assertNotIn("python -I", self.text.split("\njobs:\n", 1)[1])

    def test_the_inputs_of_a_call_are_tried_on_github_by_a_workflow_of_this_repository(self) -> None:
        trial = (ROOT / ".github" / "workflows" / "test-validate-inputs.yml").read_text(encoding="utf-8")
        self.assertIn("uses: ./.github/workflows/validate.yml", trial)
        for name in ("isolated", "os", "timeout-minutes"):
            self.assertIn(f"{name}:", trial)


if __name__ == "__main__":
    unittest.main()
