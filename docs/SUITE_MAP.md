# The map of the suite

What each repository of the EH3D Fabrication Suite is for, and whether it exists yet. "Published" means the repository is on GitHub with its tests and CI; "Planned" means there is a design and no code that anybody can run. Nothing here has been run on a machine yet.

| Repository | Kind | State | What it is for |
|---|---|---|---|
| [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON) | Library | Published | The project container (`.eh3dproj`), the machine telemetry types and the colours of the suite. |
| [EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS) | Library | Published | Readers for Gerber, Excellon and G-code that never panic and report what they could not understand. |
| [EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER) | Tool | Published | Finds, installs and updates the repositories of the suite on the PC. |
| [EH3D-DOCS](https://github.com/JuanenRac/EH3D-DOCS) | Documentation | Published | This hub. |
| EH3D-SUITE-LAUNCHER | Desktop program | Planned | The central window: workspaces, projects and the other programs. |
| EH3D-TOOL-MANAGER | Desktop program | Planned | The inventory of drill bits, V-bits and routers. |
| EH3D-ISOCAM | CAM program | Planned | Copper isolation toolpaths from Gerber layers. |
| [EH3D-DRILLPRO](https://github.com/JuanenRac/EH3D-DRILLPRO) | Desktop program | Published | The classic screens of the Bungard CCD drilling software in Rust: Excellon files, the manual and the basic automatic tool change, on a simulator or a real machine. |
| [EH3D-ROUTEPRO](https://github.com/JuanenRac/EH3D-ROUTEPRO) | Desktop program | Published | The classic screens of the Bungard CCD routing software in Rust: HP-GL files, multi-pass paths, on a simulator or a real machine. |
| EH3D-LASER-CAM | CAM program | Planned | Job preparation for laser cutting and engraving. |
| EH3D-GERBERVIEWER | Viewer | Planned | A light viewer for Gerber and drill files. |
| EH3D-STENCILCAM | CAM program | Planned | Solder paste stencils from the paste layers. |
| EH3D-AUTOLEVEL | Utility | Planned | Height maps from probing and G-code correction. |
| EH3D-MOTIONCNC | Desktop program | Planned | Real-time machine control and G-code streaming. |
| EH3D-PNP-MANAGER | Desktop program | Planned | Pick-and-place assembly management. |
| EH3D-PENDANT-GUI | Touch interface | Planned | A remote manual controller for small touch screens. |
| EH3D-CAM-DEBUGGER | Desktop program | Planned | A layer-by-layer simulator and analyser of toolpaths. |
| EH3D-VISION-STUDIO | Desktop program | Planned | Camera calibration and fiducial alignment. |

The layering and the rules every repository follows are in [ARCHITECTURE.md](ARCHITECTURE.md); what has actually been tested is in [CAPABILITY_MATRIX.md](CAPABILITY_MATRIX.md).
