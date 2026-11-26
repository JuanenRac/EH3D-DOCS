# Glossary of the names of the suite

The names as they are today, one line each. A repository is always called by the name of its repository; where a program has an executable or a command, it is given.

## Platform

| Name | What it is |
|---|---|
| EH3D | The Electro Hobby 3D ecosystem of workshop fabrication: design, CAM, machine control, the server and the clients. |
| EH3D-COMMON | The common source of **code and data**: the container, the machine types, the docking frame, the shared databases, the client of the server and the firmware base of the nodes. |
| EH3D-CORE-LIBS | The readers of Gerber, Excellon and G-code and the geometry and CAM crates that the CAM programs share. |
| EH3D-DOCS | This hub: the common source of **documentation**, the shared checks and the scripts of versions and releases. |
| `.eh3dproj` | The package of a job: a ZIP archive with a manifest, an integrity record and the layers and toolpaths. |
| `.eh3d` | The project of the suite: one file with a branch for each program, attachments and optional signatures ([PROJECT_FILE.md](PROJECT_FILE.md)). |
| `eh3d-project`, `eh3d-viewer` | The crate of the `.eh3d` project, and the viewer of its attachments. |
| `eh3d-filekind`, `eh3d-attachpanel` | The one classification of a file and of its danger, and the panel «Attachments» of the windows. |
| `eh3d-printers` | The catalog of 3D printers, with the page of the maker behind every claim. |
| Manifest | `eh3d.project.json`, the file with which a repository describes itself; nothing keeps a list of repositories. |
| Contract of the settings | The document of the server that lists every setting and switch with its texts ([CLIENT_SYNC.md](CLIENT_SYNC.md)). |
| `eh3d-dock` | The crate of the docking frame ([DOCKING.md](DOCKING.md)). |
| `eh3d-serverclient` | The one client of the server for programs written in Rust. |
| `eh3d-materials`, `eh3d-printmaterials` | The databases of board materials and of filaments and resins ([MATERIALS_DATA.md](MATERIALS_DATA.md)). |
| Firmware base | The shared part of the firmware of the nodes, kept once in COMMON and copied into each node by a tool that checks the copies. |

## Programs of machines and of CAM

| Name | What it is |
|---|---|
| EH3D-DRILLPRO, EH3D-ROUTEPRO | The classic screens of the drilling and the routing programs of the Bungard CCD machines, in Rust. |
| EH3D-BUNGARD-GUI | The modern interface of the Bungard machines. |
| EH3D-PHOENIX-CNC | Machine control: position, jog, zeros, a G-code program with pause and stop, over a simulated controller or a serial link to a GRBL controller. |
| EH3D-PHOENIX-LASER | Laser engraving from an image. |
| EH3D-PHOENIX-PNP | Pick and place assembly of printed boards. |
| EH3D-PHOENIX-3DP | Slicing for 3D printing. |
| EH3D-PHOENIX-PCB | The environment of electronic design: schematic, board, rules, simulation, manufacturing export. The main project of the PHOENIX family. |
| EH3D-PHOENIX-CAD | Mechanical design: sketches with a solver, parametric enclosures, assemblies, and the export to the formats of printing and cutting. |
| EH3D-ISOCAM, EH3D-STENCILCAM | CAM for isolation milling and for solder paste stencils. |
| EH3D-AUTOLEVEL, EH3D-CAM-DEBUGGER | The correction of Z by the height map of the table, and the last look at a G-code program. |
| EH3D-VISION-STUDIO | Marks and the camera of a machine: fiducials, scale, distortion. |
| EH3D-TOOL-MANAGER | The tool crib. |
| EH3D-GERBERVIEWER | Gerber layers and drill files as a picture, with the measurements that matter. |

## The family around the design tool

EH3D-VALIDATION-LAB (the test laboratory), EH3D-DESIGN-VERIFIER, EH3D-MANUFACTURING-PROFILE, EH3D-DESIGN-HISTORY, EH3D-PROJECT-PASSPORT, EH3D-COMPONENT-INTELLIGENCE, EH3D-THERMAL-LAB, EH3D-LAB-BRIDGE and EH3D-DESIGN-EXPLORER are libraries and tools with a command line, small and early. EH3D-HYDRA-BRIDGE is the adapter between the server and the HYDRA-UMC ecosystem.

## Server, clients and nodes

| Name | What it is |
|---|---|
| EH3D-SERVER | The center: jobs, users, machines, plug-ins for each kind of machine (all of them over a simulator today) and the update of the machines. |
| EH3D-STUDIO | The configuration panel of the server, a web application. |
| EH3D-ANDROID-CONTROL, EH3D-IOS-CONTROL | The workshop in a phone; the iPhone app is ported from the Android one and the two are kept in step. |
| EH3D-NODE-BUNGARD, EH3D-NODE-BUNGARD-AUX | The ESP32-S3 nodes: the one in the box of the controller of a Bungard machine, and the one on the drill head. |
| EH3D-NODE-HMI-GUI, EH3D-NODE-BUNGARD-HMI | The touch screens (ESP32-P4): the general purpose one and the one of the Bungard machine. |
| EH3D-UPDATER, ELECTRO-HOBBY-3D-UPDATER | The updater of this ecosystem and the dispatcher above the updaters of the four ecosystems. |
| EH3D-SUITE-LAUNCHER | Finds the programs by their manifests and starts them. |

## Words

| Word | Meaning here |
|---|---|
| Scaffolding, functional | The two values of maturity in a manifest: the first steps, and what works on the evidence it declares. |
| `simulator`, `host-test`, `bench`, `field` | The evidence of a manifest ([DESIGN_RULES.md](DESIGN_RULES.md)). |
| Sibling folder | A repository checked out next to another, from which a program takes COMMON or CORE-LIBS without a published tag. |
| Odometer | The version scheme: each number goes from 0 to 9 and carries to the one before ([RELEASING.md](RELEASING.md)). |
