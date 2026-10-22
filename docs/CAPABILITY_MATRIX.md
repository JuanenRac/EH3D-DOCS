# What works and what has been run

"Tested" here means the tests of the repository pass on a computer. "Run on a machine" means a real CNC, laser or pick-and-place machine moved because of it. **Nothing of the suite has been run on a machine yet.**

| Capability | Repository | Tested | Run on a machine | Notes |
|---|---|---|---|---|
| `.eh3dproj` container: write, read, SHA-256 integrity, limits on entries | EH3D-COMMON | Yes | No | The format is in the EH3D-COMMON repository (`docs/FORMAT.md`). |
| Telemetry types of a machine (axes, spindle, states, GRBL alarm codes) | EH3D-COMMON | Yes | No | Types only; nothing produces them yet. |
| Gerber (RS-274X) reader | EH3D-CORE-LIBS | Yes | No | Not tried on a collection of real production files. |
| Excellon drill reader | EH3D-CORE-LIBS | Yes | No | Same. |
| G-code reader and modal interpreter (GRBL, Marlin, PlanetCNC) | EH3D-CORE-LIBS | Yes | No | Cutter compensation and canned cycles are reported as unsupported. |
| Find, install and update the repositories of the suite | EH3D-UPDATER | Yes | No | Tested with a fake GitHub and local repositories; only EH3D-COMMON and EH3D-CORE-LIBS exist to be installed. |
| 2D geometry (offsets, booleans), toolpaths, HP-GL | | No | No | Planned in EH3D-CORE-LIBS. |
| Every program of the suite (CAM, viewers, machine control, launcher) | | No | No | Planned; see [SUITE_MAP.md](SUITE_MAP.md). |
