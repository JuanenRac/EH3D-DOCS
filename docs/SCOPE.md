# EH3D-DOCS: scope

Status: **host-test**. EH3D-DOCS is the hub of the suite: the documents that describe it as a whole and the tools that every repository carries or calls. The tools run on a computer and are tried on toy repositories and on the repositories of the suite; the documents are written by hand and checked by scripts. This page says what it is for, what it will not do and where it sits among the other programs of the suite.

## Purpose

The one place where the suite is described as a whole (the map of the repositories, the architecture, the capability matrix, the conventions and the common guides) and where the tools live that no repository can hold by itself: the repository check and the drawers of the pictures that are copied into every repository, the contract between the repositories, the scripts that raise a version and prepare a release, the one that sets up a workspace and the one that makes a new repository.

## What it does

* Holds the map of the suite, the architecture notes, the capability matrix, the conventions and the common guides, so that the repositories link to them instead of copying them.
* Holds the repository check (`ci_validate`), the check of the links between documents, the drawers of the README pictures and the status lights, and copies them into the repositories (`sync_shared_tools.py` says who is behind).
* Checks with `suite_contract.py` the relations that no repository can check alone: every manifest is readable and carries the name of its folder, a dependency by path says which version it needs, the versions of the map are those of the manifests, and the screens and the server agree on the port.
* Raises a version in every place that holds it, writes the notes of a release and checks a release before it is published (`bump_version.py`, `release_notes.py`, `prerelease_check.py`, `verify_release.py`).
* Offers a reusable validation workflow that the repositories call, pinned by commit.
* Fetches what a repository needs (`bootstrap_workspace.py`) and makes a new repository from the template (`new_repo.py`).
* Keeps the registers of the identifiers and of the error codes that several repositories share.

## What it will not do

* No code of a program of the suite: each repository holds its own, and this one only describes how they fit together.
* No update of a machine or of a computer: the CM5 is updated by releases and the development computers by the updater.
* No claim of what has run on a machine that the repositories do not support: the capability matrix cites what has been run, and it is only the serial protocol of the drilling program on one machine.
* No push to another repository: the tools check and prepare, and a person publishes.

## Where it sits

* **It reads:** the manifests, the changelogs, the READMEs and the workflows of the repositories of the suite that sit next to it.
* **It writes:** the files of a repository only when it is asked to (the version, the notes, the map, a copy of a shared tool, a new repository) and nothing in another folder.
* **It is read by:** every repository of the suite, through the reusable validation workflow and the copies of the shared tools, and the people who set up a workspace.
* **It depends on:** Python and `git`; the tools use the standard library only.

## What it never decides

Whether a repository is right. The manifest and the code of each repository are the source and a document here can fall behind them; the check finds many differences and does not find all of them, so a green check is not a statement that the suite is consistent or safe.

The requirements of the program, with the state of each and the test that shows it, are in `REQUIREMENTS.md`; the state in a paragraph is in `STATUS.md`.
