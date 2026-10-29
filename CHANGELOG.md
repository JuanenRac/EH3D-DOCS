# Changelog

All notable changes to this project are documented here.

## [Unreleased]

- The suite map lists EH3D-DRILLPRO and EH3D-ROUTEPRO as published programs (they were marked as planned).

- **The layout of the README is checked in the CI:** the validator runs `tools/universal_readme_check.py` and lists, as a warning, what differs from the universal layout of the README.

## [0.0.1] - The hub of the documentation

- **The map of the suite** (`docs/SUITE_MAP.md`): every repository of the suite, what it is for and whether it exists yet.
- **The architecture** (`docs/ARCHITECTURE.md`): the layers and the rules every repository follows.
- **The capability matrix** (`docs/CAPABILITY_MATRIX.md`): what has been tested on a computer and what has been run on a machine (nothing yet).
- **The conventions** (`docs/CONVENTIONS.md`): the manifest, the repository check, the README files.
- A check of the links between the documents (`tools/check_links.py`) and the repository check, both in CI.
