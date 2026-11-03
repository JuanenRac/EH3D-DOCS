# The reusable validation workflow

Every repository of the suite runs the same checks first: the manifest, the versions, the licence, the CHANGELOG, the eight README files and the pictures of the README. Today each repository carries its own copy of that part of `.github/workflows/ci.yml`. `.github/workflows/validate.yml` of this repository holds it once, as a **reusable workflow** (`on: workflow_call`), so that a repository can call it instead of copying the steps.

**Status: one pilot.** EH3D-SUITE-LAUNCHER calls it from its `ci.yml`, pinned to the commit of the release 0.0.6 of this repository (a commit SHA, so a change here reaches it only when it chooses); the other repositories still carry their own copy of the steps. A reusable workflow can only be tried on GitHub, so the pilot is where the points of "Trying it in a pilot" below are watched before the others follow.

## What it does

One job, `validate`, on `ubuntu-latest` with these steps, in order:

1. Check out the repository that called it and set up Python.
2. `python -I tools/ci_validate.py` (manifest, versions, licence, CHANGELOG, README files, forbidden words, tracked files).
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

## Trying it in a pilot

1. Give this repository a tag that holds `validate.yml` (a tag is a release step, so it is made when a version is published).
2. In one repository, keep its current `validate` job and add a second job that calls the reusable workflow with the same inputs; watch both go green on the same commit.
3. Delete the old job from the pilot, and move the other repositories one at a time.

What to look at in the pilot: that `tools/ci_validate.py` finds the repository's files (the checkout is of the calling repository), that the job name shown in the checks of a pull request is the one the branch protection expects (a called workflow shows as `validate / Validate the repository`), and that the repositories that need extra setup before the validation (for example a generated file) still get it.

## Why the others have not adopted it yet

- It cannot be run from a local checkout: the only test is a real run on GitHub, and only one repository has done it.
- The name of the check changes (`validate / Validate the repository`), which matters wherever a rule requires a check by name.
- A repository whose `ci.yml` runs `ci_validate` with environment variables or in another folder needs an input for it first.
