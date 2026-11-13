# The reusable validation workflow

Every repository of the suite runs the same checks first: the manifest, the versions, the licence, the CHANGELOG, the eight README files and the pictures of the README. Today each repository carries its own copy of that part of `.github/workflows/ci.yml`. `.github/workflows/validate.yml` of this repository holds it once, as a **reusable workflow** (`on: workflow_call`), so that a repository can call it instead of copying the steps.

**Status: three repositories and the template of a new one.** EH3D-SUITE-LAUNCHER, EH3D-TOOL-MANAGER and EH3D-PHOENIX-PNP call it from their `ci.yml`, and so does the CI of a repository made by `new_repo.py`; each pins it to a full commit of this repository (so a change here reaches it only when it chooses). The commit has to be one whose own actions are pinned by commit as well: a run that calls a workflow with actions named by a tag (as it was before the actions were pinned) does not start at all. SUITE-LAUNCHER is where it was tried first, and its pin was moved for that reason; its check is named `validate / Validate the repository` and it keeps its own `changelog` job; the other repositories still carry their own copy of the steps. A reusable workflow can only be tried on GitHub, so the first repositories are where the points of "Trying it in a pilot" below are watched before the others follow.

## What it does

One job, `validate`, on `ubuntu-latest` with these steps, in order:

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

- It cannot be run from a local checkout: the only test is a real run on GitHub, and only three repositories have done it.
- The name of the check changes (`validate / Validate the repository`), which matters wherever a rule requires a check by name.
- A repository whose `ci.yml` runs `ci_validate` with environment variables or in another folder needs an input for it first.

## The supply-chain workflow

`.github/workflows/supply-chain.yml` is a second reusable workflow, for the files of a release: a bill of materials in the CycloneDX format, signed provenance attestations for the files (`actions/attest`) and the bill attached to the **draft** release. It is an opt-in capability and it is **not switched on in any release**: the input `enabled` is `false` by default, and with it off every job is skipped, so calling the workflow reads, writes and signs nothing.

The calling workflow builds the files, uploads them as one artifact (a flat list of files, no folders) and calls the workflow in a job of its own:

```yaml
  supply-chain:
    needs: build
    uses: JuanenRac/EH3D-DOCS/.github/workflows/supply-chain.yml@<full commit>
    permissions:
      contents: write
      id-token: write
      attestations: write
    with:
      enabled: true
      artifact: release-files
      name: ${{ github.event.repository.name }}
      version: "1.2.3"
      tools-ref: <the same full commit>
      attach-to-release: true
      release-tag: v1.2.3
```

| Input | Type | Default | Meaning |
|---|---|---|---|
| `enabled` | boolean | `false` | the switch: nothing runs while it is false |
| `artifact` | string | (required) | the artifact of the calling workflow that holds the files of the release |
| `name` | string | (required) | the name of the release in the bill (the repository) |
| `version` | string | (required) | the version of the release in the bill |
| `tools-ref` | string | `main` | the commit of this repository whose `tools/make_release_sbom.py` writes the bill; name the same commit as in `uses` |
| `attach-to-release` | boolean | `false` | attach the bill to the draft release named by `release-tag` |
| `release-tag` | string | empty | the tag of the draft release that gets the bill |

Three jobs: `sbom` writes `sbom.cdx.json` (the SHA-256 of every file, the same bytes for the same files) and uploads it as the artifact `<artifact>-sbom`; `attest` makes the provenance attestation of the files and attests the bill against them, and it is the only job with `id-token` and `attestations`; `attach` (only with `attach-to-release`) adds the bill to a draft release found by its tag and fails when the release is already published. The default permission of the workflow is `contents: read`, and the permissions a job asks for must be given by the calling job, as in the example. Every action is pinned to a full commit with its version in a comment. The attestations come in addition to the signature of the release files, which does not change.

`.github/workflows/supply-chain-test.yml` tries it on example files: on a pull request it writes the bill for them and checks that the reusable workflow starts and skips its jobs; started by hand with `exercise` on it also makes the bill and the attestations of the example files. To switch the capability on in a release, add the job above to the release workflow of a repository with `enabled: true` and look at the attestations of the first run before the next one.
