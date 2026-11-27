# Design rules that hold for the whole suite

These are the decisions that every repository follows. They are written here once, and the repositories link to this page instead of repeating them.

## Safety and security

* **No program decides that something is safe to run on a machine.** Limits, interlocks and the emergency stop belong to the machine and its controller. A window, a server or a phone app asks, shows and refuses; it never takes the place of the safety of the machine.
* **Every option that concerns security has a switch that a person can see and change in the studio and in every client** (see [CLIENT_SYNC.md](CLIENT_SYNC.md)), and **its default is the conservative one**: a feature that opens something, accepts something looser, writes to a machine or runs code from outside is off until a person turns it on. A client never turns one on by itself, and a value that is looser than recommended needs a confirmation.
* **Safe degradation.** When something goes wrong, the program goes towards what is safer, never towards what is looser. An error path may refuse, stop, latch or keep the old value; it may never relax a restriction or go on as if the thing had worked. A value of a safety setting that is not understood is refused and the value in force is kept; it is never read as "off". A latch is lifted only by the route made for it, by the role that may.
* **A file from outside is hostile until proven otherwise.** Sizes, entry names and number formats are checked before they are used, a reader never panics and never guesses, and what cannot be understood becomes a diagnostic with a stable code and a line.
* **A package is trusted by its hash and, where the machine asks for it, by its signature.** A program that updates itself or a machine installs only what is signed with the key of the releases when the machine has been given one.
* **Scripts and extensions that run inside a program** (post-processors written as code, the scripts of the design tool) are off by default, run in a sandbox without network or files, and have their own switch. The declarative form is the default.
* **A key, a token or a password never enters a repository,** and a firmware that is published carries no secret of any installation.

## Evidence: what "done" means

* **Three kinds of evidence**, written in the manifest and in the status table of every README: `simulator` (the code ran against a simulated machine or data made by the tests), `bench` (it ran on a real board or machine on a bench, not doing work) and `field` (it did real work). Almost the whole suite is `simulator` or `host-test` today.
* **Nothing is shown as working on hardware that has not run on hardware.** The light of the status table is green only for what has been verified in the setting the row names; the capability matrix says what has been run on a machine and what has not. `bench` and `field` are set by a person after trying, never by a script.
* **A plug-in of the server that drives a machine says that it is only a simulator** until it has driven a real one.
* **Hardware that does not exist yet is implemented as if it did:** the code is written and tested against a simulator or a stand-in, marked `simulator`, with the exact test on the board left as pending.

## Parameters and data

* **Every tuned value goes to a configuration file** the person can read and edit (`machine.cfg`, `server.cfg`, the file of a program), never into the code. The code has a default, the file overrides it, and a value that does not read is reported, not replaced by a guess.
* **A value that is shown to a person has its unit in its name** and a range, and a table of data (a material, a tool, a package, a capability of a factory) lives once in COMMON ([MATERIALS_DATA.md](MATERIALS_DATA.md)).
* **No table is copied between repositories;** a constant that is repeated is checked against its source by a test.

## Scope of programs

* **The pick and place program (EH3D-PHOENIX-PNP) assembles printed boards only.** It does not place anything else, and the rules of a feeder, a nozzle or a tray are written for components of boards.
* **A program that has a window shows its panels with the docking frame** ([DOCKING.md](DOCKING.md)).
* **The programs exchange work through `.eh3dproj` files and the server, never through each other.**
* **Exit codes of the checks.** Every `check` command of a program ends with 0 when all passes, 1 when the program failed, 2 when the check did not pass and 64 when it was used wrongly; see the section on the exit codes of [CONVENTIONS.md](CONVENTIONS.md) for the table the tools of the repositories follow today.

## Languages and text

* **The documents and the text that people read exist in eight languages:** English, Spanish, German, French, Italian, Japanese, Chinese and European Portuguese (`ficheiro`, `atualizar`, `ecrã`, `telemóvel`).
* **A text is never improvised for a language;** a code with a text in seven languages is a build error, and a new key goes to every language file in the same change.
* **French, German and Portuguese texts of the catalogues are formal** (vous, Sie, the third person in Portuguese).

## Licences

Software is GPL-3.0-or-later. Mechanical models are CC-BY-SA and electronic designs of hardware use a CERN open hardware licence (the strongly reciprocal variant). A repository that mixes firmware and hardware states the licence of each directory.
