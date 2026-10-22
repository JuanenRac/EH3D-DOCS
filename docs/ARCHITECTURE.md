# Architecture

The suite is a set of independent programs that share two libraries and one project file. The programs are written in Rust; the tools around them (the updater, the repository checks) are Python.

## Layers

1. **[EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON)** defines what every program agrees on: the `.eh3dproj` container (a ZIP archive with `project.json`, `integrity.json`, `layers/`, `toolpaths/` and `vision/`), the telemetry types of a machine and the colours of the suite. It depends on nothing of the suite.
2. **[EH3D-CORE-LIBS](https://github.com/JuanenRac/EH3D-CORE-LIBS)** reads the files that other people send (Gerber, Excellon, G-code). It depends on nothing but the standard library and has no window.
3. **The programs** (CAM, viewers, machine control, the launcher) depend on the two libraries and never on each other: they exchange work through `.eh3dproj` files.
4. **[EH3D-UPDATER](https://github.com/JuanenRac/EH3D-UPDATER)** installs and updates the repositories on the PC of the person using them.

## Rules

* **A reader never panics and never guesses.** What cannot be understood becomes a diagnostic with the number of the line.
* **A file from outside is hostile until proven otherwise:** sizes, entry names and number formats are checked before they are used.
* **A program does not decide that a G-code is safe to run.** Limits, interlocks and the emergency stop belong to the machine and its controller.
* **Every repository describes itself** with an `eh3d.project.json` manifest; nothing keeps a list of projects, so a new repository appears by having a manifest.
* **Texts exist in eight languages** wherever a repository shows text to people.
* **Every behaviour has a test**, including the refusals.
