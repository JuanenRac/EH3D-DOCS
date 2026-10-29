# Changelog

All notable changes to this project are documented here.

## [Unreleased]

- **README in the universal layout, in eight languages:** the README has the same sections in the same order as the other repositories of the family (status, overview, architecture, features, security, interfaces, configuration, quick start, testing, structure, roadmap and known limits), with figures taken from the code and from the tests that were run. The Architecture and Repository Structure pictures are drawn from `docs/architecture.json` and `docs/structure.json` by `tools/make_architecture.py` and `tools/make_structure.py`, and the CI checks that they match.
- The suite map lists EH3D-DRILLPRO, EH3D-ROUTEPRO, EH3D-SERVER, EH3D-NODE-BUNGARD and ELECTRO-HOBBY-3D-UPDATER as published, the capability matrix has a row for each of them and says that the serial protocol of EH3D-DRILLPRO has moved one real machine, and the architecture notes describe the node and the server.

- **The layout of the README is checked in the CI:** the validator runs `tools/universal_readme_check.py` and lists, as a warning, what differs from the universal layout of the README.

## [0.0.1] - The hub of the documentation

- **The map of the suite** (`docs/SUITE_MAP.md`): every repository of the suite, what it is for and whether it exists yet.
- **The architecture** (`docs/ARCHITECTURE.md`): the layers and the rules every repository follows.
- **The capability matrix** (`docs/CAPABILITY_MATRIX.md`): what has been tested on a computer and what has been run on a machine (nothing yet).
- **The conventions** (`docs/CONVENTIONS.md`): the manifest, the repository check, the README files.
- A check of the links between the documents (`tools/check_links.py`) and the repository check, both in CI.
