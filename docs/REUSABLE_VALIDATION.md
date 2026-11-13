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

## Trying it in a pilot

1. Give this repository a tag that holds `validate.yml` (a tag is a release step, so it is made when a version is published).
2. In one repository, keep its current `validate` job and add a second job that calls the reusable workflow with the same inputs; watch both go green on the same commit.
3. Delete the old job from the pilot, and move the other repositories one at a time.

What to look at in the pilot: that `tools/ci_validate.py` finds the repository's files (the checkout is of the calling repository), that the job name shown in the checks of a pull request is the one the branch protection expects (a called workflow shows as `validate / Validate the repository`), and that the repositories that need extra setup before the validation (for example a generated file) still get it.

## Why the others have not adopted it yet

- It cannot be run from a local checkout: the only test is a real run on GitHub, and only three repositories have done it.
- The name of the check changes (`validate / Validate the repository`), which matters wherever a rule requires a check by name.
- A repository whose `ci.yml` runs `ci_validate` with environment variables or in another folder needs an input for it first.
