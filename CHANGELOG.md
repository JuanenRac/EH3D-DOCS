# Changelog

All notable changes to this project are documented here.

## [Unreleased]

- **The map, the matrix and the architecture for the programs that have started:** the launcher, the tool crib, the isolation program, the laser program, the Gerber viewer, the stencil program, the height-map program, pick and place, the debugger and the vision program have a line in the map as started (a library and a command line with tests, no release yet) and a row each in the matrix; the phone apps for Android and iPhone are listed as published; the catalogue of bits is more than 450 and the node of the drill head, the web panel of the nodes and the recovery of a program in MOTIONCNC are mentioned.

- **The node of the drill head through the server and in Studio:** the matrix and the architecture say that the server relays the node (`/api/v1/machines/:id/head/...`), that Studio shows it on the page of a machine, that the cameras are the OV2640 and the OV5640 and that the drivers of the sensors are written but have never run.

## [0.0.2] - The drill head node, the height map of the table and the updates of the services in the map, the matrix and the architecture

- **The map and the matrix:** the node of the drill head (EH3D-NODE-BUNGARD-AUX), the height map of the table, the calibration, the update of the services from GitHub, the keyboards of the touch screen and the other new capabilities are listed with what has been tested and what has not; the lists of repositories of the README are complete in the eight languages.
- **The map, the matrix and the architecture up to date:** EH3D-BUNGARD-GUI and EH3D-MOTIONCNC are published in the map and the matrix, the crates that EH3D-COMMON now holds (the view and the themes, the ZIP archives, the files of the Bungard machines, the controllers, the file windows) are described, and the README in eight languages counts eleven published repositories.
- **README in the universal layout, in eight languages:** the README has the same sections in the same order as the other repositories of the family (status, overview, architecture, features, security, interfaces, configuration, quick start, testing, structure, roadmap and known limits), with figures taken from the code and from the tests that were run. The Architecture and Repository Structure pictures are drawn from `docs/architecture.json` and `docs/structure.json` by `tools/make_architecture.py` and `tools/make_structure.py`, and the CI checks that they match.
- The suite map lists EH3D-DRILLPRO, EH3D-ROUTEPRO, EH3D-SERVER, EH3D-NODE-BUNGARD and ELECTRO-HOBBY-3D-UPDATER as published, the capability matrix has a row for each of them and says that the serial protocol of EH3D-DRILLPRO has moved one real machine, and the architecture notes describe the node and the server.

- **The layout of the README is checked in the CI:** the validator runs `tools/universal_readme_check.py` and lists, as a warning, what differs from the universal layout of the README.

## [0.0.1] - The hub of the documentation

- **The map of the suite** (`docs/SUITE_MAP.md`): every repository of the suite, what it is for and whether it exists yet.
- **The architecture** (`docs/ARCHITECTURE.md`): the layers and the rules every repository follows.
- **The capability matrix** (`docs/CAPABILITY_MATRIX.md`): what has been tested on a computer and what has been run on a machine (nothing yet).
- **The conventions** (`docs/CONVENTIONS.md`): the manifest, the repository check, the README files.
- A check of the links between the documents (`tools/check_links.py`) and the repository check, both in CI.
