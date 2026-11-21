# EH3D-DOCS: status

## Current state

EH3D-DOCS works on a computer: the repository check, the check of the links, the contract between the repositories, the scripts of version and release, the workspace script, the new-repository script and the reusable validation workflow are covered by tests, many of them on toy repositories. The documents (the map, the architecture, the capability matrix and the guides) are written by hand and can fall behind the repositories. No repository has yet published a release with the release tools, and neither the workspace script nor the new-repository script has set up a real workspace or created a real repository.

## Capabilities

The official state of each capability is in `REQUIREMENTS.md`. The register has 33 requirements: 29 implemented, 0 prototype, 4 planned and 0 validated. By progress: 29 done, 0 partial, 1 pending and 3 blocked. This page never states a state that `REQUIREMENTS.md` does not.

## Open questions

* How much of the capability matrix should be written by a script from the manifests instead of by hand.
* Whether the daily contract check should fail, and not only warn, once the repositories it names are up to date.

## What it needs from other repositories

* The manifests and changelogs of the repositories of the suite, which the contract reads.
* A repository that publishes a release with the release tools, to show that they work outside a toy repository.

## Known technical debt and omitted tests

* The map and the matrix are written by hand and are checked only in part (the versions and the releases).
* The release tools, the workspace script and the new-repository script have only run on toy repositories.
* Some tools differ between the repositories that carry them until `sync_shared_tools.py` is run in each one.
