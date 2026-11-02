# Conventions of the repositories

* **The manifest.** Each repository has an `eh3d.project.json` with the fields the validators require (`schema_version`, `ecosystem`, `name`, `version`, `role`, `stack`, `technologies`, `deployment_target`, `maturity`, `family`, `parent`, `build`, `notes` and `native_version`). `native_version` says in which file and with which pattern the repository keeps its own version, and the check fails when it differs from the manifest. Optional fields are `service`, `components`, `evidence`, `hardware_bound`, `depends_on` (schema 1.1) and `binary`: the file name of the executable the repository builds (for example `"binary": "eh3d-server"`; letters, digits, dot, dash and underscore, no folder and no path, and without a platform suffix such as `.exe` unless the program is only built for that platform). A program with several executables names the main one; the others are not listed. The parser of EH3D-UPDATER accepts the field and keeps it, so a tool can find the program of a repository without guessing from its `Cargo.toml`.
* **The check.** `python -I tools/ci_validate.py` verifies the manifest, the versions, the changelog, the licence, the eight README files and that no private reference is in a public file. The same check runs in CI.
* **The README files.** Eight languages (English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese), with the same structure, so a heading appears in the same order in all of them.
* **Honesty about maturity.** A repository says what runs and what has only been tested on a computer; `scaffolding` means the first steps.
* **Commits** are written in English, small and about one thing.
* **The shared tools.** `tools/ci_validate.py` (and the status lights, the drawers of the pictures and the other tools that every repository carries) is changed only in this hub, never in a copy. A repository that needs its own data does not edit the code: it puts it in `tools/ci_config.json` (for example `{"skip_dirs": ["local-data", "re"]}`, the folders the scan for forbidden words skips). Every change of `ci_validate.py` raises `TOOLS_VERSION` and the `# canonical: EH3D-DOCS tools N` line of its header; each copy carries that line and the validator prints it as `tools=N` in its last line (`CI_VALIDATION=PASS project=... version=... tools=N`). To carry a change: run `python -I tools/sync_shared_tools.py` here to see who differs, then, one repository at a time, `python -I tools/sync_shared_tools.py --write --only ci_validate.py --repo <REPOSITORY>`, run `python tools/ci_validate.py` in that repository and commit it ("Use the shared validator of the suite") before going to the next; a repository whose check fails for a reason of its own content is fixed there first. `python -I tools/suite_contract.py --only tools` lists the repositories that are behind.

## Exit codes of the command-line tools

Every command-line tool of the suite (the scripts of `tools/` of every repository, the Updater, the programs with a console mode) ends with one of these codes, so a script or a CI job can tell what happened without reading the text:

| Code | Meaning |
|---|---|
| `0` | Done, nothing to say. |
| `1` | Failed: a check found an error, or something could not be read or written. |
| `2` | Done, with warnings. An option such as `--strict` may turn the warnings into `1`. |
| `10` | Done, and there is something to do (the Updater's `check` ends with it when an update is available). |
| `64` | Wrong use: an option or an argument that does not exist or does not make sense (the code `EX_USAGE` of the BSD `sysexits`). |

Any other code is not part of the convention; a tool that must tell more says it in its last line (for example `SUITE_CONTRACT=PASS ...`), as the checks of this hub do. `argparse` ends a wrong option with `2`, which in this convention means "warnings": the tools of this hub use a parser that ends it with `64` (a small `UsageParser` class), and `--help` ends with `0`.

`python -I tools/exit_conventions.py` reads every command of `tools/` and reports the ones that differ (a literal code outside the table; a `--help` that does not end with 0; a wrong option that does not end with 64), and the unit tests run it. The tools that are copied into every repository (`ci_validate.py`, `status_lights.py`, `make_structure.py`, `make_architecture.py`, `universal_readme_check.py`) are changed only with a new tools version, so their differences are listed in the tool as known and not changed here.

**What differs today in other repositories** (written down, not changed): the validator copies and the drawers of the pictures end a wrong option with `2`; `ELECTRO-HOBBY-3D-UPDATER` passes on the code of the updater it runs, ends `versions` and `pins` with `2` when something is behind and a `--preview` that the chosen ecosystem lacks with `64`, but its parser ends a wrong option with `2`; `EH3D-UPDATER` ends with `1` on every error, `10` for `check` and `0` otherwise, and its parser ends a wrong option with `2`.

## Names

These are the names the suite uses today. Nothing is renamed to make them fit: a name that differs is written here as it is, and a new repository follows the first column.

| What | Convention | Examples |
|---|---|---|
| Repository | `EH3D-` and the name in capitals, words separated by `-`. A board of the suite is `EH3D-NODE-<NAME>`. The updater of the whole family is the exception, `ELECTRO-HOBBY-3D-UPDATER`. | `EH3D-SERVER`, `EH3D-NODE-BUNGARD-HMI` |
| Manifest `name` | The name of the repository, exactly (the validators and the Updater compare it with the folder). | `EH3D-DRILLPRO` |
| Rust package | The repository in lower case; a repository that is only a set of libraries names each crate `eh3d-<what it does>`. | `eh3d-server`, `eh3d-common` |
| Executable | Lower case, words separated by `-`; new ones start with `eh3d-`. Today several programs have a shorter name that people know (`drillpro`, `routepro`, `motioncnc`, `bungard-gui`) and some abbreviate (`eh3d-camdebug`, `eh3d-gerberview`, `eh3d-lasercam`, `eh3d-pnp`, `eh3d-tools`, `eh3d-vision`, `eh3d-launcher`). The manifest field `binary` says which one a repository builds. | `eh3d-server`, `drillpro` |
| npm package | Lower case with the same prefix; the folder and the package are not required to match the repository. | `eh3d-studio` |
| Python package | Lower case with `-` on PyPI-style names and `_` for the import. | `eh3d-updater`, `eh3d_updater` |
| System service | The executable name. | `eh3d-server` |
| Tag and release | `v` and the version of the manifest, with three or four numbers; the tag is made on the commit that carries that version. | `v0.0.7`, `v0.8.0.1` |
| Branch | `main` is the only long-lived branch; a working branch says what it does, in lower case with `-`. | `main`, `fix-port-parsing` |
| Configuration file | Lower case, one concern per file, the extension `.cfg` for `key = value` files and `.json` for structured data; the repository keeps an `.example` copy and the real file is not committed. | `server.cfg`, `machine.cfg`, `hmi.cfg`, `head.cfg` |
| Names the system reserves | On Windows a file cannot be called `aux`, `con`, `nul`, `prn`, `com1` and the like, with or without extension; a node that would be called `aux` uses `head.cfg` for its configuration. | `head.cfg` |
| README | `README.md` in English and `README_<code>.md` with the three letters `spa`, `fra`, `ita`, `deu`, `zho`, `jpn`, `por`; the codes of the languages are in `docs/suite.json`. | `README_por.md` |
