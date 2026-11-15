# The reusable validation workflow

Every repository of the suite runs the same checks first: the manifest, the versions, the licence, the CHANGELOG, the eight README files and the pictures of the README. Today each repository carries its own copy of that part of `.github/workflows/ci.yml`. `.github/workflows/validate.yml` of this repository holds it once, as a **reusable workflow** (`on: workflow_call`), so that a repository can call it instead of copying the steps.

**Status: three repositories and the template of a new one.** EH3D-SUITE-LAUNCHER, EH3D-TOOL-MANAGER and EH3D-PHOENIX-PNP call it from their `ci.yml`, and so does the CI of a repository made by `new_repo.py`; each pins it to a full commit of this repository (so a change here reaches it only when it chooses). The commit has to be one whose own actions are pinned by commit as well: a run that calls a workflow with actions named by a tag (as it was before the actions were pinned) does not start at all. SUITE-LAUNCHER is where it was tried first, and its pin was moved for that reason; its check is named `validate / Validate the repository` and it keeps its own `changelog` job; the other repositories still carry their own copy of the steps. A reusable workflow can only be tried on GitHub, so the first repositories are where the points of "Trying it in a pilot" below are watched before the others follow.

## What it does

One job, `validate`, on `ubuntu-latest` (or on the runners named by `os`) with these steps, in order:

1. Check out the repository that called it and set up Python.
2. `python -I tools/ci_validate.py` (manifest, versions, licence, CHANGELOG, README files, forbidden words, tracked files, and the file tree: the text tree of every README and the Repository Structure picture against `docs/structure.json` and the files of the repository, through `make_structure.run_in_ci`).
3. The pictures of the README: `tools/make_architecture.py --check` and `tools/make_structure.py --check --readmes` (when `check-pictures` is true).
4. The links between the documents: `tools/check_links.py` (when `check-links` is true).
5. The unit tests of `tools/` (when `run-tool-tests` is true).

The workflow runs the scripts **of the calling repository** (its own `tools/` folder), not the ones of this repository: each repository keeps its copy of the shared tools, and `tools/sync_shared_tools.py` says when a copy has drifted.

## The inputs

| Input | Type | Default | Meaning |
|---|---|---|---|
| `python-version` | string | `"3.12"` | the Python used for the checks |
| `check-pictures` | boolean | `true` | check the Architecture and Repository Structure pictures against `docs/architecture.json` and `docs/structure.json` |
| `check-links` | boolean | `false` | run `tools/check_links.py` (the repository must have it) |
| `run-tool-tests` | boolean | `false` | run the unit tests of `tools/` |
| `isolated` | boolean | `true` | run the Python checks with `-I`; `false` for a repository whose validator is of an older generation and needs its own folder on the path |
| `os` | string | `["ubuntu-latest"]` | the runners to validate on, as a JSON list; two or more run one job per runner and add the runner to the name of the check |
| `timeout-minutes` | number | `15` | minutes after which a validation job is stopped |

A call that names none of the last three behaves exactly as before: one Ubuntu job, isolated Python, the check named `validate / Validate the repository`. The three inputs are there for the repositories that could not call the workflow before (an updater whose validator runs without `-I`, a program that must be validated on Windows too). The file `.github/workflows/test-validate-inputs.yml` tries a call with the defaults and a call with the three inputs on GitHub; no repository has been moved to them yet.

The workflow asks for `contents: read` only and has no secrets.

## How a repository uses it

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validate:
    uses: JuanenRac/EH3D-DOCS/.github/workflows/validate.yml@<tag>
    with:
      check-links: true
      run-tool-tests: true

  build:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      # the repository's own steps: cargo fmt, clippy, test; npm; gradle
```

Replace `<tag>` with a tag or a commit SHA of this repository. A tag moves only when someone moves it, so a repository that wants a change to arrive only when it chooses should name a tag; a repository that wants every change at once could name `main`, but then a change here can turn the CI of every repository red at once, so use a tag.

## Skipping an expensive job: `changed-paths.yml`

A second reusable workflow, `.github/workflows/changed-paths.yml`, answers one question: does this change touch the paths that make a slow job (Windows, macOS, Gradle, firmware) worth running? It only reads the list of changed files (`contents: read`, a sparse checkout of two commits, 5 minutes at most) and has no secrets.

| Input | Type | Default | Meaning |
|---|---|---|---|
| `paths` | string | (required) | globs, one per line: `**` crosses folders, `*` and `?` do not, a line starting with `!` removes what it matches, a name without wildcards also matches the folder of that name, `#` starts a comment |
| `label` | string | empty | a pull request label that forces the answer `true` (for example `full-ci`) |

| Output | Values |
|---|---|
| `matched` | `true` when the job should run, `false` when the change cannot affect it |
| `reason` | `label`, `paths`, `no-paths`, `manual` (any event that is not a push, a pull request or a merge group: a manual or scheduled run always runs everything) or `unknown-base` |

When it cannot find what the change is compared with (a push of several commits whose first parent is not in the clone, a new branch, a pull request checked out without its merge commit) it answers `true` with `unknown-base`: it never skips a job by mistake. A pull request is compared with its base branch, a push with the commit before it.

```yaml
jobs:
  changes:
    uses: JuanenRac/EH3D-DOCS/.github/workflows/changed-paths.yml@<tag>
    with:
      label: full-ci
      paths: |
        app/**
        gradle/**
        !app/docs/**

  android:
    needs: changes
    if: ${{ needs.changes.outputs.matched == 'true' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "the slow job"
```

A job skipped by `if` shows as skipped, not red; a rule that requires that job by name must accept a skipped one. `.github/workflows/test-changed-paths.yml` runs the decision rules on throw-away repositories (a change that touches the paths and one that does not, the label, a push, a manual run, the patterns) and one real call; the file also starts only when one of the two workflows changes.

## A quicker CI without taking a check away

The runners of GitHub are a shared queue, and a macOS job can wait for an hour. Four habits keep a repository's checks as they are and still keep the queue short; `python tools/workflow_hygiene.py --root . --speed` (or `"speed": true` in `tools/hygiene_config.json`) reports a workflow that does not follow them.

1. **A macOS job does not start on every pull request.** It runs on a push to main, on a tag, on the scheduled run and on a manual start; a pull request can ask for it with the label `full-ci`.

   ```yaml
   macos:
     if: ${{ github.event_name != 'pull_request' || contains(github.event.pull_request.labels.*.name, 'full-ci') }}
     runs-on: macos-latest
   ```

   For a matrix, build the list of runners from the event: `os: ${{ fromJSON(github.event_name == 'pull_request' && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest","windows-latest","macos-latest"]') }}`.

2. **A newer push to a branch cancels the run before it, and main and the tags are never cancelled.**

   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: ${{ github.ref != 'refs/heads/main' && !startsWith(github.ref, 'refs/tags/') }}
   ```

   A plain `cancel-in-progress: true` also cancels a push to main when the next one arrives, so a release workflow or a check of main could end up cancelled.

3. **An expensive job (Gradle, Xcode, ESP-IDF, PlatformIO, a heavy build) runs when its paths changed.** Call `changed-paths.yml` as shown above and let main, the tags and the scheduled run force everything:

   ```yaml
   android:
     needs: changes
     if: ${{ github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/') || github.event_name == 'schedule' || needs.changes.outputs.matched == 'true' }}
   ```

   The label `full-ci` is given to `changed-paths.yml` as its `label` input, so a pull request can force the job too.

4. **One check to require, which always runs.** A job skipped by a condition counts as passed, but a matrix job skipped that way keeps the name of the matrix, and a rule that requires it would wait for ever. The template of a new repository ends with a `ci-gate` job (`if: always()`, `needs` every other job) that fails only when a job failed or was cancelled; require that one check in the rules of the branch.

   ```yaml
   ci-gate:
     name: CI gate
     if: ${{ always() }}
     needs: [validate, android]
     runs-on: ubuntu-latest
     timeout-minutes: 5
     steps:
       - env:
           RESULTS: ${{ join(needs.*.result, ' ') }}
         run: case " $RESULTS " in *" failure "*|*" cancelled "*) exit 1 ;; esac
   ```

A fifth habit concerns the runner image: `ubuntu-latest` moves to a newer Ubuntu without notice, and a job that measures a coverage floor (the branch counts of gcov change) or tests infrastructure (systemd, mosquitto, containers, AppArmor profiles) turns red for no change of the code. Pin `runs-on: ubuntu-24.04` on those jobs, with a comment saying why; the other jobs may follow `latest`. The rule `ubuntu-latest-infra` reports the ones that do not.

The CHANGELOG has a sixth habit, in `.gitattributes`: `CHANGELOG.md merge=union` (and the same for `CHANGELOG_*.md` and `CHANGELOG.*.md`) makes git keep both sides when two branches add an entry at the same place. It applies to the merges and rebases that git does; the checks that read the CHANGELOG compare the set of entries, not their order, so they pass either way. If two branches edit the same entry, git keeps both versions and the duplicate must be removed by hand.

## Trying it in a pilot

1. Give this repository a tag that holds `validate.yml` (a tag is a release step, so it is made when a version is published).
2. In one repository, keep its current `validate` job and add a second job that calls the reusable workflow with the same inputs; watch both go green on the same commit.
3. Delete the old job from the pilot, and move the other repositories one at a time.

What to look at in the pilot: that `tools/ci_validate.py` finds the repository's files (the checkout is of the calling repository), that the job name shown in the checks of a pull request is the one the branch protection expects (a called workflow shows as `validate / Validate the repository`), and that the repositories that need extra setup before the validation (for example a generated file) still get it.

## Why the others have not adopted it yet

- It cannot be run from a local checkout: the only test is a real run on GitHub, and only three repositories have done it.
- The name of the check changes (`validate / Validate the repository`), which matters wherever a rule requires a check by name.
- A repository whose `ci.yml` runs `ci_validate` with environment variables or in another folder needs an input for it first.
