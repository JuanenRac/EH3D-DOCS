# The documents every repository carries

Besides the README in eight languages and the CHANGELOG, a repository of the suite has five documents that say what it is, what it must do, where it stands, what was left out on purpose and how to change it. The repositories of the design family (the PHOENIX project and the libraries around it) already have them; the others are to receive them. This page is the template and the check, and the list of the repositories that still lack them.

## The five documents

| Document | Where | What it says |
|---|---|---|
| `SCOPE.md` | `docs/` | The purpose in a paragraph; what it does and what it will not do; where it sits among the other repositories (what it reads, what reads it); what it never decides (for a program that drives a machine: that the limits, the interlocks and the emergency stop belong to the machine). It begins with a line `Status:` that says what runs and what has only been tested on a computer. |
| `REQUIREMENTS.md` | `docs/` | The register of capabilities, the single source of the state of each. A table: an identifier with the prefix of the repository (`PPNP-001`), a description, the state (`planned`, `prototype`, `implemented`, `validated`), **how it will be checked**, the expected result and the known limits. High coverage is not proof of correctness: each row says how it is checked and what result is expected. |
| `STATUS.md` | `docs/` | What exists, what is missing and what the last change decided: the current state in a paragraph, the capabilities (a pointer to the register; this page never states a state that the register does not), the open questions, what it needs from other repositories and the known technical debt and the tests that were omitted. |
| `NOT_YET.md` | `docs/` | Good ideas that are not in the current version, so that nobody implements them early: the idea, why not yet, and when to revisit it. |
| `AGENTS.md` | the root | The rules for anyone, a person or a tool, who changes the repository: what to read first, how to build and test (the exact commands that the CI runs), the code rules (a reader never panics and never guesses, the safety rules, a parameter that is tuned goes to the configuration file), the documents rules (eight languages, generated files are generated), the limits of what may be done without asking, and how to report. |

## What each one must keep true

* **The state is written once.** `REQUIREMENTS.md` holds it; `STATUS.md`, the README and the capability matrix of this hub cite it. A requirement is `validated` only when a person has run it in the real setting the row names, and the evidence of the manifest (`simulator`, `host-test`, `bench`, `field`) says the same.
* **A requirement has an identifier that never changes** and a check that someone else could run.
* **The documents are in English** and short sentences are better than long ones. The README, which is in eight languages, links them; it does not copy them.
* **No date and no private reference.** The state is told as it is, not as it was on a day.

## The check

For each repository the check is: the five files exist; every requirement of the register has a state from the list; `STATUS.md` names the same number of requirements and states as the register; and the README links `docs/SCOPE.md` and `docs/STATUS.md`. The repository's own validator can run it (a small test that reads the table is enough), and a repository adopts it in the version in which it adds the documents. The hub does not create these files in the other repositories; each repository adds them in its own change.

## Who still lacks them

The list comes from the trees of the repositories and is replaced when a repository adds the documents.

| Group | Repositories |
|---|---|
| With the five documents | the nine design libraries and tools (the test laboratory, the verifier, the manufacturing profiles, the history of a design, the project passport, the component database, the thermal laboratory, the bridge to laboratory measurements and the explorer of alternatives), EH3D-HYDRA-BRIDGE, EH3D-PHOENIX-PCB, EH3D-PHOENIX-CAD |
| Without `NOT_YET.md` and `AGENTS.md` | EH3D-PHOENIX-3DP |
| With none of the five | EH3D-PHOENIX-PNP, EH3D-PHOENIX-CNC, EH3D-PHOENIX-LASER, EH3D-ISOCAM, EH3D-VISION-STUDIO, EH3D-STENCILCAM, EH3D-AUTOLEVEL, EH3D-CAM-DEBUGGER, EH3D-TOOL-MANAGER, EH3D-GERBERVIEWER, EH3D-SUITE-LAUNCHER, ELECTRO-HOBBY-3D-UPDATER, EH3D-UPDATER, EH3D-SERVER, EH3D-STUDIO, EH3D-DRILLPRO, EH3D-ROUTEPRO, EH3D-BUNGARD-GUI, EH3D-COMMON, EH3D-CORE-LIBS, EH3D-DOCS (this hub), EH3D-ANDROID-CONTROL, EH3D-IOS-CONTROL, EH3D-NODE-BUNGARD, EH3D-NODE-BUNGARD-AUX, EH3D-NODE-BUNGARD-HMI, EH3D-NODE-HMI-GUI |

The first twelve of the third row (the programs of the machines and of CAM, the viewer, the launcher and the dispatcher of the updaters) are the next to receive them; the libraries, the server, the clients and the nodes follow.
