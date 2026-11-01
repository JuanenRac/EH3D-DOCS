# Changelog

All notable changes to this project are documented here.

## [Unreleased]

## [0.0.4] - The matrix and the architecture with resuming and the GRBL switch

- **Going on from a stopped job, and the `$` lines of GRBL per machine:** the matrix and the architecture say that the server keeps the request of every job and makes a new, never started job from a stopped one with the work done left out, that the three clients use it, and that an administrator can allow the `$` lines of GRBL on one machine with a safety switch that is off by default.

## [0.0.3] - The map, the matrix and the architecture with G-code, GRBL and the new releases

- **Free G-code jobs, the GRBL connection and the programs that send their work to the server:** the map, the matrix and the architecture say that the server runs a program of G-code line by line on the simulator or on a GRBL controller, that it can be held, resumed and gone on from the line where it stopped, that the spindle and the coolant start again only when asked, that a node, a GRBL controller and the simulator take different kinds of job, and that the drilling, routing and machine control programs, Studio and the phone apps work with the server; the matrix has two new rows.

- **The Release column and the rows of the newest releases:** the map lists the release that is on GitHub for each repository (the Android and iPhone apps 0.0.3, the touch screens 0.0.4 and 0.0.2, the drill head node 0.0.5, the programs 0.0.9, the modern interface 0.1.5), what a release now holds is no longer said to be on the main branch, and the Android APK of 0.0.3 is said to have been tried on a phone.

- **The map with the release of each repository, and the newest work:** the map has a Release column; the map and the matrix say that the interfaces of the programs, the touch screens and the panel of the nodes speak 37 languages, that a Bungard machine has two spindles (60000 rpm the original one, 24000 rpm the one with a drive) with limits that the server enforces, that a job can be the drilling, the routing or both with any tool switched off, and what the sensors of the node of the drill head do (laser, several temperature sensors, a reflective speed sensor with a filter and the settings of the camera picture), each with what has not been tried on a real machine. The general purpose touch screen is described with its kind of machine, and the README in eight languages counts the twenty-seven published repositories.

- **The new programs are published:** the launcher, the tool crib, the isolation program, the laser program, the Gerber viewer, the stencil program, the levelling utility, the pick and place manager, the vision studio, the G-code debugger and the general purpose touch screen have their first release, so the map lists them as published.

- **The ring of LEDs and the quality check of the drill head:** two rows in the matrix (the ring of LEDs around the camera with its colour signals and the picture on request; the quality check of the holes and of the milled channels with one verdict) and a sentence in the map for each repository that has it. Both say what has not happened: no ring has been driven and no real board has been photographed.

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
