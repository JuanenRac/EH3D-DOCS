"""Light tests of workflow_hygiene.py: example workflows in temporary folders, nothing real."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

def _find_tool_folder() -> str:
    """The folder that holds the tool: beside the tests, in a sibling tools/ folder or in tools/canonical/ of a parent."""
    for up in Path(__file__).resolve().parents[:4]:
        for cand in (up, up / "tools", up / "tools" / "canonical"):
            if (cand / "workflow_hygiene.py").is_file():
                return str(cand)
    return str(Path(__file__).resolve().parent.parent)


sys.path.insert(0, _find_tool_folder())
import workflow_hygiene as wh  # noqa: E402

SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"

GOOD = f"""name: CI
on:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@{SHA} # v7
      - uses: JuanenRac/some-action@v1
      - uses: ./.github/actions/local
      - name: Run
        env:
          TOKEN: ${{{{ secrets.PUBLISH_TOKEN }}}}
        run: |
          echo "uses: not/an-action@v1 is only text here"
          echo "$TOKEN" | wc -c
"""

BAD = """name: Bad
on:
  pull_request_target:
    types: [opened]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - uses: some-org/some-action@main
      - name: Leak
        run: |
          curl -H "Authorization: ${{ secrets.API_KEY }}" https://example.org
  other:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: echo ${{ secrets.ONE_LINER }}
"""

RELEASE_NO_CONC = f"""name: Release
on:
  push:
    tags: ['v*']
permissions:
  contents: write
jobs:
  publish:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@{SHA}
      - run: gh release create "$GITHUB_REF_NAME"
"""

RELEASE_OK = RELEASE_NO_CONC.replace("jobs:", "concurrency:\n  group: release\n  cancel-in-progress: false\njobs:")

CALLER = """name: Caller
on: [push]
permissions: {}
jobs:
  call:
    uses: JuanenRac/shared/.github/workflows/x.yml@main
"""


def rules(findings):
    return sorted(f["rule"] for f in findings)


def check(text, name="w.yml"):
    return wh.check_workflow(Path(name), text)


class RuleTests(unittest.TestCase):
    def test_good_workflow_has_no_findings(self):
        self.assertEqual(check(GOOD), [])

    def test_unpinned_and_own_and_local(self):
        f = [x for x in check(BAD) if x["rule"] == "unpinned-action"]
        self.assertEqual(sorted(x["message"] for x in f), ["actions/checkout@v4", "some-org/some-action@main"])

    def test_text_inside_run_block_is_not_an_action(self):
        self.assertEqual([x for x in check(GOOD) if x["rule"] == "unpinned-action"], [])

    def test_docker_and_missing_version(self):
        text = GOOD + "      - uses: docker://alpine:3\n      - uses: owner/repo\n"
        msgs = [x["message"] for x in check(text) if x["rule"] == "unpinned-action"]
        self.assertEqual(len(msgs), 2)

    def test_timeout_per_job_and_reusable_call_exempt(self):
        f = [x for x in check(BAD) if x["rule"] == "no-timeout"]
        self.assertEqual([x["message"] for x in f], ["job 'build' without timeout-minutes"])
        self.assertEqual([x for x in check(CALLER) if x["rule"] == "no-timeout"], [])

    def test_permissions_top_level_only(self):
        self.assertIn("no-permissions", rules(check(BAD)))
        self.assertNotIn("no-permissions", rules(check(GOOD)))
        # permissions at job level does not count as top-level
        job_level = GOOD.replace("permissions:\n  contents: read\n", "").replace("    timeout-minutes: 20\n", "    timeout-minutes: 20\n    permissions:\n      contents: read\n")
        self.assertIn("no-permissions", rules(check(job_level)))

    def test_concurrency_only_for_release_workflows(self):
        self.assertIn("no-concurrency", rules(check(RELEASE_NO_CONC, "release.yml")))
        self.assertNotIn("no-concurrency", rules(check(RELEASE_OK, "release.yml")))
        self.assertNotIn("no-concurrency", rules(check(GOOD, "ci.yml")))
        self.assertTrue(check(RELEASE_NO_CONC, "something.yml"))   # detected by trigger/command, not only by name
        self.assertIn("no-concurrency", rules(check(RELEASE_NO_CONC, "something.yml")))

    def test_job_level_concurrency_counts(self):
        text = RELEASE_NO_CONC.replace("    timeout-minutes: 30\n", "    timeout-minutes: 30\n    concurrency: rel\n")
        self.assertNotIn("no-concurrency", rules(check(text, "release.yml")))

    def test_pull_request_target_checkout_of_pr(self):
        f = [x for x in check(BAD) if x["rule"] == "prt-checkout"]
        self.assertEqual(len(f), 1)
        self.assertEqual(f[0]["severity"], "high")
        safe = BAD.replace("pull_request_target", "pull_request")
        self.assertEqual([x for x in check(safe) if x["rule"] == "prt-checkout"], [])
        base = BAD.replace("${{ github.event.pull_request.head.sha }}", "main")
        self.assertEqual([x for x in check(base) if x["rule"] == "prt-checkout"], [])

    def test_secret_in_run_block_and_one_liner_but_not_in_env(self):
        f = [x for x in check(BAD) if x["rule"] == "secret-in-run"]
        self.assertEqual(len(f), 2)
        self.assertEqual([x for x in check(GOOD) if x["rule"] == "secret-in-run"], [])

    def test_secret_line_number_points_into_the_block(self):
        f = [x for x in check(BAD) if x["rule"] == "secret-in-run"][0]
        self.assertIn("API_KEY", BAD.split("\n")[f["line"] - 1])

    def test_comments_and_crlf(self):
        text = GOOD.replace("\n", "\r\n") + "      # - uses: x/y@v1\n"
        self.assertEqual(check(text), [])

    def test_triggers_forms(self):
        for src, want in (("on: push\n", {"push"}), ("on: [push, pull_request_target]\n", {"push", "pull_request_target"}),
                          ("on:\n  pull_request_target:\n  push:\n", {"pull_request_target", "push"}),
                          ("on:\n  - release\n", {"release"})):
            self.assertEqual(wh.Workflow(src).triggers(), want, src)

    def test_known_false_positive_secret_in_comment_line_of_inline_run(self):
        # documented: a one line `run: echo ${{ secrets.X }}` is reported (the secret should go through env:)
        self.assertTrue([x for x in check("on: push\njobs:\n  a:\n    timeout-minutes: 1\n    steps:\n      - run: echo ${{ secrets.X }}\n") if x["rule"] == "secret-in-run"])


class ScanTests(unittest.TestCase):
    def make_root(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        for repo, files in {"ARMOR-X": {"ci.yml": BAD}, "URTC-Y": {"ci.yml": GOOD, "release.yml": RELEASE_NO_CONC}, "HYDRA-UMC-Z": {"ci.yml": GOOD},
                            "EH3D-W": {"a.yaml": CALLER}, "otro": {"ci.yml": GOOD}, "_private": {"ci.yml": BAD}}.items():
            wf = root / repo / ".github" / "workflows"
            wf.mkdir(parents=True)
            for n, t in files.items():
                (wf / n).write_text(t, encoding="utf-8")
        (root / "sin-workflows").mkdir()
        return tmp, root

    def test_scan_summary_by_ecosystem_and_skips(self):
        tmp, root = self.make_root()
        with tmp:
            repos = wh.scan(root)
            self.assertEqual(sorted(repos), ["ARMOR-X", "EH3D-W", "HYDRA-UMC-Z", "URTC-Y", "otro"])   # folders starting with _ and folders without workflows are skipped
            s = wh.summarize(repos)
            self.assertEqual(set(s["ecosystems"]), {"ARMOR", "URTC", "HYDRA", "EH3D", "OTHER"})
            self.assertEqual(s["ecosystems"]["URTC"]["by_rule"], {"no-concurrency": 1})
            self.assertEqual(s["worst"][0]["repo"], "ARMOR-X")
            self.assertEqual(s["total_workflows"], 6)

    def test_root_may_be_a_single_repo(self):
        tmp, root = self.make_root()
        with tmp:
            self.assertEqual(list(wh.scan(root / "ARMOR-X")), ["ARMOR-X"])

    def test_filters(self):
        tmp, root = self.make_root()
        with tmp:
            repos = wh.scan(root)
            wh.filter_findings(repos, {"no-timeout"}, "low")
            self.assertEqual({f["rule"] for r in repos.values() for f in r["findings"]}, {"no-timeout"})
            repos = wh.scan(root)
            wh.filter_findings(repos, None, "high")
            self.assertEqual({f["severity"] for r in repos.values() for f in r["findings"]}, {"high"})

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = wh.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_json_and_table_and_check(self):
        tmp, root = self.make_root()
        with tmp:
            code, out, _ = self.run_main("--root", str(root), "--json")
            data = json.loads(out)
            self.assertEqual(code, 0)
            self.assertEqual(data["summary"]["total_repos"], 5)
            code, out, _ = self.run_main("--root", str(root))
            self.assertIn("BY ECOSYSTEM", out)
            self.assertIn("ARMOR-X", out)
            total = data["summary"]["total_findings"]
            self.assertEqual(self.run_main("--root", str(root), "--check", "--threshold", str(total))[0], 0)
            code, out, _ = self.run_main("--root", str(root), "--check", "--threshold", str(total - 1))
            self.assertEqual(code, 1)
            self.assertIn("WORKFLOW_HYGIENE=FAIL", out)
            self.assertEqual(self.run_main("--root", str(root), "--check")[0], 1)

    def test_unknown_rule_and_missing_root(self):
        self.assertEqual(self.run_main("--root", str(Path(tempfile.gettempdir()) / "no_such_dir_wh"))[0], 2)
        tmp, root = self.make_root()
        with tmp:
            self.assertEqual(self.run_main("--root", str(root), "--rules", "nope")[0], 2)

    def test_read_only(self):
        tmp, root = self.make_root()
        with tmp:
            before = {p: p.read_bytes() for p in root.rglob("*.y*ml")}
            self.run_main("--root", str(root), "--detail")
            self.assertEqual(before, {p: p.read_bytes() for p in root.rglob("*.y*ml")})


class BaselineAndConfigTests(unittest.TestCase):
    run_main = ScanTests.run_main

    def single(self, text=BAD, config=None):
        tmp = tempfile.TemporaryDirectory()
        repo = Path(tmp.name) / "ARMOR-ONE"
        (repo / ".github" / "workflows").mkdir(parents=True)
        (repo / ".github" / "workflows" / "ci.yml").write_text(text, encoding="utf-8")
        if config is not None:
            (repo / "tools").mkdir()
            (repo / "tools" / "hygiene_config.json").write_text(json.dumps(config), encoding="utf-8")
        return tmp, repo

    def test_write_baseline_then_only_new_findings_block(self):
        tmp, repo = self.single()
        with tmp:
            self.assertEqual(self.run_main("--root", str(repo), "--check")[0], 1)
            code, _, err = self.run_main("--root", str(repo), "--write-baseline")
            self.assertEqual(code, 0)
            self.assertIn("baseline written", err)
            self.assertTrue((repo / "tools" / "workflow_hygiene_baseline.json").is_file())
            code, out, _ = self.run_main("--root", str(repo), "--check")
            self.assertEqual(code, 0)
            self.assertIn("WORKFLOW_HYGIENE=PASS new=0", out)
            wf = repo / ".github" / "workflows" / "ci.yml"
            wf.write_text("# moved down\n" + BAD + "      - uses: another/action@v1\n", encoding="utf-8")   # lines move: still baselined; one more unpinned action is new
            code, out, _ = self.run_main("--root", str(repo), "--check", "--detail")
            self.assertEqual(code, 1)
            self.assertIn("new=1", out)
            self.assertEqual(sum(1 for ln in out.splitlines() if " NEW " in ln), 1)
            self.assertIn("another/action@v1", out)

    def test_config_threshold_enabled_rules(self):
        tmp, repo = self.single(config={"workflow_hygiene": {"rules": ["no-timeout"], "threshold": 5}})
        with tmp:
            code, out, _ = self.run_main("--root", str(repo), "--check")
            self.assertEqual(code, 0)   # one no-timeout, threshold 5
            self.assertIn("new=1", out)
            self.assertEqual(self.run_main("--root", str(repo), "--check", "--threshold", "0")[0], 1)   # the command line wins
            self.assertEqual(self.run_main("--root", str(repo), "--check", "--config", "none")[0], 1)
        tmp, repo = self.single(config={"workflow_hygiene": {"enabled": False}})
        with tmp:
            self.assertEqual(self.run_main("--root", str(repo), "--check")[0], 0)

    def test_stale_baseline_entries_are_counted_not_blocking(self):
        tmp, repo = self.single()
        with tmp:
            self.run_main("--root", str(repo), "--write-baseline")
            (repo / ".github" / "workflows" / "ci.yml").write_text(GOOD, encoding="utf-8")
            code, out, _ = self.run_main("--root", str(repo), "--check", "--json")
            self.assertEqual(code, 0)
            self.assertGreater(json.loads(out)["repos"]["ARMOR-ONE"]["resolved"], 0)

    def test_baseline_never_written_without_the_flag(self):
        tmp, repo = self.single()
        with tmp:
            self.run_main("--root", str(repo), "--check", "--detail")
            self.assertFalse((repo / "tools").exists())


class CiStepTests(unittest.TestCase):
    run_main = ScanTests.run_main
    single = BaselineAndConfigTests.single

    def test_step_does_not_block_without_settings_or_baseline(self):
        tmp, repo = self.single()
        with tmp:
            self.assertEqual(wh.run_in_ci(repo), [])

    def test_step_blocks_new_findings_once_the_repository_opts_in(self):
        tmp, repo = self.single(config={"workflow_hygiene": {"enabled": True}})
        with tmp:
            problems = wh.run_in_ci(repo)
            self.assertTrue(problems)
            self.assertIn("workflow hygiene:", problems[-1])
            self.run_main("--root", str(repo), "--write-baseline")
            self.assertEqual(wh.run_in_ci(repo), [])   # the known findings are in the baseline
            (repo / ".github" / "workflows" / "ci.yml").write_text(BAD + "      - uses: another/action@v1\n", encoding="utf-8")
            self.assertEqual(len(wh.run_in_ci(repo)), 2)   # the new finding and the summary

    def test_step_respects_enabled_false_threshold_and_a_baseline_alone(self):
        tmp, repo = self.single(config={"workflow_hygiene": {"enabled": False}})
        with tmp:
            self.assertEqual(wh.run_in_ci(repo), [])
        tmp, repo = self.single(config={"workflow_hygiene": {"threshold": 100}})
        with tmp:
            self.assertEqual(wh.run_in_ci(repo), [])
        tmp, repo = self.single()
        with tmp:
            (repo / "tools").mkdir()
            (repo / "tools" / "workflow_hygiene_baseline.json").write_text(json.dumps({"findings": {}}), encoding="utf-8")
            self.assertTrue(wh.run_in_ci(repo))   # an empty baseline alone opts in

    def test_step_without_workflows_is_silent(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(wh.run_in_ci(Path(d)), [])


SPEED_BASE = f"""name: CI
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
concurrency:
  group: ${{{{ github.workflow }}}}-${{{{ github.ref }}}}
  cancel-in-progress: ${{{{ github.ref != 'refs/heads/main' && !startsWith(github.ref, 'refs/tags/') }}}}
jobs:
"""
MAC_PLAIN = SPEED_BASE + """  ios:
    runs-on: macos-latest
    timeout-minutes: 30
    steps:
      - run: echo build
"""
MAC_GUARDED = SPEED_BASE + """  ios:
    if: ${{ github.event_name != 'pull_request' || contains(github.event.pull_request.labels.*.name, 'full-ci') }}
    runs-on: macos-latest
    timeout-minutes: 30
    steps:
      - run: echo build
"""
MAC_MATRIX_PLAIN = SPEED_BASE + """  tests:
    runs-on: ${{ matrix.os }}
    timeout-minutes: 30
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    steps:
      - run: echo hi
"""
MAC_MATRIX_GUARDED = SPEED_BASE + """  tests:
    runs-on: ${{ matrix.os }}
    timeout-minutes: 30
    strategy:
      matrix:
        os: ${{ fromJSON(github.event_name == 'pull_request' && '["ubuntu-latest"]' || '["ubuntu-latest","macos-latest"]') }}
    steps:
      - run: echo hi
"""
HEAVY_PLAIN = SPEED_BASE + """  android:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - run: ./gradlew test
"""
HEAVY_GATED = (SPEED_BASE + """  changes:
    uses: JuanenRac/EH3D-DOCS/.github/workflows/changed-paths.yml@3d3c42e5aac5ba805825da76410c181273ba90b1
    with:
      paths: app/**
  android:
    needs: changes
    if: ${{ github.ref == 'refs/heads/main' || needs.changes.outputs.matched == 'true' }}
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - run: ./gradlew test
  ci-gate:
    if: ${{ always() }}
    needs: [android]
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: echo ok
""")


def speed(text, name="ci.yml"):
    return wh.check_workflow(Path(name), text, speed=True)


class SpeedRuleTests(unittest.TestCase):
    """The rules that keep the queue of the runners short without taking a check away."""

    def test_speed_rules_are_off_unless_asked_for(self):
        self.assertEqual(rules(check(MAC_PLAIN)), [])
        self.assertIn("macos-on-pr", rules(speed(MAC_PLAIN)))

    def test_macos_job_needs_a_guard_on_the_event(self):
        self.assertIn("macos-on-pr", rules(speed(MAC_PLAIN)))
        self.assertNotIn("macos-on-pr", rules(speed(MAC_GUARDED)))
        self.assertIn("macos-on-pr", rules(speed(MAC_MATRIX_PLAIN)))
        self.assertNotIn("macos-on-pr", rules(speed(MAC_MATRIX_GUARDED)))

    def test_macos_without_a_pull_request_trigger_is_fine(self):
        text = MAC_PLAIN.replace("  pull_request:\n", "")
        self.assertNotIn("macos-on-pr", rules(speed(text)))

    def test_a_plain_cancel_in_progress_true_cancels_main(self):
        plain = MAC_GUARDED.replace("${{ github.ref != 'refs/heads/main' && !startsWith(github.ref, 'refs/tags/') }}", "true")
        self.assertIn("cancel-main", rules(speed(plain)))
        self.assertNotIn("cancel-main", rules(speed(MAC_GUARDED)))
        only_pr = plain.replace("  push:\n    branches: [main]\n", "")
        self.assertNotIn("cancel-main", rules(speed(only_pr)))   # a workflow that never runs on main may cancel freely

    def test_a_pull_request_workflow_must_cancel_a_superseded_branch_run(self):
        none = MAC_GUARDED.replace("concurrency:\n  group: ${{ github.workflow }}-${{ github.ref }}\n  cancel-in-progress: ${{ github.ref != 'refs/heads/main' && !startsWith(github.ref, 'refs/tags/') }}\n", "")
        self.assertIn("no-branch-cancel", rules(speed(none)))
        never = MAC_GUARDED.replace("${{ github.ref != 'refs/heads/main' && !startsWith(github.ref, 'refs/tags/') }}", "false")
        self.assertIn("no-branch-cancel", rules(speed(never)))
        self.assertNotIn("no-branch-cancel", rules(speed(MAC_GUARDED)))
        self.assertNotIn("no-branch-cancel", rules(speed(none.replace("pull_request:", "workflow_dispatch:"))))   # no pull request: nothing to cancel

    def test_a_heavy_job_needs_a_paths_filter_or_a_changed_paths_answer(self):
        self.assertIn("heavy-no-filter", rules(speed(HEAVY_PLAIN)))
        self.assertNotIn("heavy-no-filter", rules(speed(HEAVY_GATED)))
        filtered = HEAVY_PLAIN.replace("  pull_request:\n", "  pull_request:\n    paths-ignore:\n      - 'docs/**'\n")
        self.assertNotIn("heavy-no-filter", rules(speed(filtered)))

    def test_skipped_jobs_need_a_job_that_always_runs(self):
        self.assertNotIn("no-gate", rules(speed(HEAVY_GATED)))
        without = HEAVY_GATED.replace("if: ${{ always() }}", "if: ${{ success() }}")
        self.assertIn("no-gate", rules(speed(without)))

    def test_changelog_union_is_read_from_gitattributes(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d) / "R"
            (repo / ".github" / "workflows").mkdir(parents=True)
            (repo / ".github" / "workflows" / "ci.yml").write_text(MAC_GUARDED, encoding="utf-8")
            (repo / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
            found = [f["rule"] for r in wh.scan(repo, speed=True).values() for f in r["findings"]]
            self.assertEqual(found, ["changelog-union"])
            (repo / ".gitattributes").write_text("* text=auto\nCHANGELOG.md merge=union\n", encoding="utf-8")
            found = [f["rule"] for r in wh.scan(repo, speed=True).values() for f in r["findings"]]
            self.assertEqual(found, [])

    def test_a_repository_turns_the_speed_rules_on_in_its_settings(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d) / "R"
            (repo / ".github" / "workflows").mkdir(parents=True)
            (repo / "tools").mkdir()
            (repo / ".github" / "workflows" / "ci.yml").write_text(MAC_PLAIN, encoding="utf-8")
            self.assertEqual([f for r in wh.scan(repo).values() for f in r["findings"]], [])
            (repo / "tools" / "hygiene_config.json").write_text(json.dumps({"workflow_hygiene": {"speed": True}}), encoding="utf-8")
            self.assertIn("macos-on-pr", [f["rule"] for r in wh.scan(repo).values() for f in r["findings"]])
            self.assertTrue(wh.run_in_ci(repo))   # and the validation of the repository fails on it

    def test_command_line_speed_flag_and_rule_selection(self):
        with tempfile.TemporaryDirectory() as d:
            repo = Path(d) / "R"
            (repo / ".github" / "workflows").mkdir(parents=True)
            (repo / ".github" / "workflows" / "ci.yml").write_text(MAC_PLAIN, encoding="utf-8")
            for args in (("--speed",), ("--rules", "macos-on-pr")):
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    code = wh.main(["--root", str(repo), "--check", *args])
                self.assertEqual(code, 1, args)
                self.assertIn("WORKFLOW_HYGIENE=FAIL", out.getvalue())
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(wh.main(["--root", str(repo), "--check"]), 0)

    def test_coverage_floor_and_infrastructure_jobs_pin_the_ubuntu_image(self):
        latest = SPEED_BASE + """  coverage:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - run: npm run coverage
  broker:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - run: sudo apt-get install --yes mosquitto
  plain:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - run: echo build
"""
        names = sorted(f["message"].split("'")[1] for f in speed(latest) if f["rule"] == "ubuntu-latest-infra")
        self.assertEqual(names, ["broker", "coverage"])   # the plain job may follow latest
        pinned = latest.replace("runs-on: ubuntu-latest", "runs-on: ubuntu-24.04")
        self.assertNotIn("ubuntu-latest-infra", rules(speed(pinned)))
        self.assertNotIn("ubuntu-latest-infra", rules(check(latest)))   # off unless the speed rules are on

    def test_the_canonical_workflows_of_this_repository_follow_the_rules(self):
        root = Path(__file__).resolve().parents[1]
        if not (root / ".github" / "workflows").is_dir():
            self.skipTest("the workflows are not part of this checkout")
        found = [f"{name}: {f['file']} {f['rule']}" for name, r in wh.scan(root, speed=True).items() for f in r["findings"] if f["rule"] in wh.SPEED_RULES]
        self.assertEqual(found, [])
        template = root / "docs" / "templates" / "new_repo" / "ci.yml"
        if template.is_file():
            self.assertEqual([f["rule"] for f in speed(template.read_text(encoding="utf-8"), "ci.yml") if f["rule"] in wh.SPEED_RULES], [])
            self.assertIn("always()", template.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
