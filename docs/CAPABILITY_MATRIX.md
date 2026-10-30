# What works and what has been run

"Tested" here means the tests of the repository pass on a computer. "Run on a machine" means a real CNC, laser or pick-and-place machine moved because of it. **Only the serial protocol of EH3D-DRILLPRO, which EH3D-ROUTEPRO shares, has moved a real machine (one Bungard CCD MTC: the reference run and the moves of each axis); no whole job has run on a machine, and nothing else of the suite has.**

| Capability | Repository | Tested | Run on a machine | Notes |
|---|---|---|---|---|
| `.eh3dproj` container: write, read, SHA-256 integrity, limits on entries | EH3D-COMMON | Yes | No | The format is in the EH3D-COMMON repository (`docs/FORMAT.md`). |
| Telemetry types of a machine (axes, spindle, states, GRBL alarm codes) | EH3D-COMMON | Yes | No | Types only; nothing produces them yet. |
| Gerber (RS-274X) reader | EH3D-CORE-LIBS | Yes | No | Not tried on a collection of real production files. |
| Excellon drill reader | EH3D-CORE-LIBS | Yes | No | Same. |
| G-code reader and modal interpreter (GRBL, Marlin, PlanetCNC) | EH3D-CORE-LIBS | Yes | No | Cutter compensation and canned cycles are reported as unsupported. |
| Find, install and update the repositories of the suite | EH3D-UPDATER | Yes | No | Tested with a fake GitHub and local repositories; it has never installed a project from the real GitHub. |
| Hand the projects of the four ecosystems over to their own updaters | ELECTRO-HOBBY-3D-UPDATER | Yes | Partly | `status` has run against a real checkout of three of the ecosystems and `install` once; the hand-over to EH3D-UPDATER has not been run against a real checkout. |
| Drilling: Excellon files, the tool table, the classic screens, the job on a simulator | EH3D-DRILLPRO | Yes | Partly | The reference run and the moves of every axis were tried on one Bungard CCD MTC; a whole drilling job has not run. |
| Routing: HP-GL files, multi-pass paths, the classic screens, the job on a simulator | EH3D-ROUTEPRO | Yes | No | It shares the protocol of EH3D-DRILLPRO; a whole routing job has not run on a machine. |
| Plan a job, keep users and machines, run it through a node with a stop and operator dialogs | EH3D-SERVER | Yes | No | Tested through its interface with jobs on the simulator; it does not terminate TLS. |
| Control link, lamps, spindle output, web panel and update with rollback of the node | EH3D-NODE-BUNGARD | Yes | No | The rules are tested on a computer and both firmware images build; nothing has been flashed to a board. |
| Several machines and stations at once: the answer of the server for the whole fleet, read by the programs and shown in a window | EH3D-SERVER, EH3D-COMMON | Yes | No | Tested through the interface of the server and a stand-in server; it has never watched real machines. |
| The touch screen of the machine: the gate that every move passes (confirmation, hardware-stop latch, armed link), the settings file, spoken orders and alerts in eight languages | EH3D-NODE-BUNGARD-HMI | Yes | No | The rules are tested on a computer; the firmware has not been built or run on a module and there is no link to a machine yet. |
| The firmware base that every node copies | EH3D-COMMON | Yes | No | Tested only through EH3D-NODE-BUNGARD, the one node that uses it. |
| The files of the Bungard machines: Excellon, HP-GL (with arcs, circles and scaling), tool tables, configuration; Gerber and DXF outlines as routing paths | EH3D-COMMON | Yes | No | Shared by DRILLPRO, ROUTEPRO and BUNGARD-GUI; the outlines were tried on written examples, not on a collection of real files. |
| Jobs in ZIP archives and the Open and Save windows (places, sorting, filters, replace check) | EH3D-COMMON | Yes | No | The state of the windows has no interface of its own; BUNGARD-GUI and MOTIONCNC draw it. |
| Interface of the machine controllers: GRBL on a scripted line, a simulated controller with limits, stored positions and G-code | EH3D-COMMON | Yes | No | GRBL has not been connected to a serial port; the other families are listed as not driven. |
| The job in 2D and 3D, eleven themes, eight languages, simulation at the speed of the machine, panels, board library, recent files, hole counts | EH3D-BUNGARD-GUI | Yes | No | Run on the simulator of the classic programs and on a computer; no machine has been driven from this window. |
| Machine control: position, jog, zeros, stored positions, a G-code program with pause, stop and emergency stop, menus, settings, files | EH3D-MOTIONCNC | Yes | No | Only over the simulated controller; no real controller is connected, and the emergency stop of the window is not a safety circuit. |
| 2D geometry (offsets, booleans), toolpaths, HP-GL | | No | No | Planned in EH3D-CORE-LIBS. |
| The programs that do not exist yet (CAM, viewers, the launcher, the real controllers for machine control) | | No | No | Planned; see [SUITE_MAP.md](SUITE_MAP.md). |
