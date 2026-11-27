# Error codes: how they are named and how the tables are kept in step

A refusal or a failure is told with a stable code, never with a sentence that a program invents. The code does not change its meaning once it is published, and its sentence exists in the eight languages of the suite (English, Spanish, German, French, Italian, Japanese, Chinese and European Portuguese). A code with no text in one of the eight languages is an error of the build, not a text to improvise.

## Families of codes

| Family | Where it is raised | Where it is listed |
|---|---|---|
| `EH3D-PKG-nnn` | the project containers: `001` to `014` the container itself (a `.eh3dproj` or `.eh3d` that is refused or cannot be written), `015` to `026` the branches of an `.eh3d` project (`019` is the only warning; `025` and `026` refuse a write that would lose what another program saved or a signature) | `registry/EH3D-PKG.md` of this repository |
| `EH3D-ID-nnn` | the identity of an object (an id that cannot be read or made) | `registry/EH3D-ID.md` of this repository |
| `EH3D-MAT-nnn` | the database of materials: `001` to `009` board materials, `010` to `015` machining materials | `docs/MATERIALS.md` and `docs/MACHINING.md` of EH3D-COMMON |
| `EH3D-PMAT-nnn` | the database of filaments and resins | `crates/printmaterials/README.md` of EH3D-COMMON |
| `EH3D-PRN-nnn` | the catalog of 3D printers (`EH3D-PRN-001` to `EH3D-PRN-009`) | `docs/PRINTERS.md` of EH3D-COMMON |
| `EH3D-BUILD-nnn` | the build text of a program (`EH3D-BUILD-001` to `EH3D-BUILD-008`) | `docs/BUILD.md` of EH3D-COMMON |
| `EH3D-FORMATS-nnn` | the files of the Bungard machines (drill, plot and outline files) | `docs/FORMAT_ERRORS.md` of EH3D-COMMON |
| `EH3D-TASK-nnn` | the tasks of the server | `docs/API.md` of EH3D-SERVER |
| a lower-case word (`bad_policy`, `printers_off`...) | the refusals of EH3D-SERVER, with the HTTP status | `docs/error-codes.json` of EH3D-SERVER |
| `PHOENIX-<AREA>-nnn` | the electronic design program, one area for each part of it; among the newest, `PHOENIX-EAGLEBIN-001` to `011` (what a binary EAGLE library gave) and `PHOENIX-KIT-001` to `008` (the starter kit) | `docs/ERROR_CODES.md` of EH3D-PHOENIX-PCB |
| `PHOENIX-CAD-nnn` | the mechanical design program | `docs/ERROR_CODES.md` of EH3D-PHOENIX-CAD |
| `PHOENIX-PNP-nnn` | the pick and place program | the README of EH3D-PHOENIX-PNP |
| `PHOENIX-PCBPNP-001` to `PHOENIX-PCBPNP-011` | the command `phoenix pnp` of the electronic design program | `docs/ERROR_CODES.md` of EH3D-PHOENIX-PCB |

Up to its release 0.1.6 the electronic design program published the codes of `phoenix pnp` with the prefix `PHOENIX-PNP-`, which belongs to the program EH3D-PHOENIX-PNP, where the same numbers mean other things. They are `PHOENIX-PCBPNP-` since 0.1.7, with the same numbers and meanings, so each prefix has one meaning; a filter or a script that looks for the old prefix has to be changed.

The codes of a family that is not in a release yet are in the repository only. A program that uses a family reports its codes as they are and keeps its own family for its own failures. A new code is a change of the list and of the code in the same commit; the tests of this repository and of the repository that raises it keep both lists in agreement.

## The tables of the clients

The server's refusals reach the person through four kinds of client, and each keeps a table of the eight texts of every code. None of them writes its own sentences: the words are taken from one place.

| Client | The table | How it is made and checked |
|---|---|---|
| EH3D-STUDIO | the rows `err_<code>` of its text catalogue | the tests compare the codes with `docs/error-codes.json` of the server and fail when a code has no text in the eight languages |
| EH3D-ANDROID-CONTROL | `server-errors.json` in its assets and `ErrorTexts.kt` | `tools/gen_server_errors.py` takes the codes from the server and the eight texts from the Studio catalogue; `--check` fails when the table on disk is not what the sources give |
| EH3D-IOS-CONTROL | the same table and `ErrorTexts.swift` | the same generator, so the iPhone says the same words as the Android phone |
| The touch screens (EH3D-NODE-HMI-GUI and EH3D-NODE-BUNGARD-HMI) | a table in the firmware, made by the generator of the firmware base | the generator and its check live in `firmware_base/tools` of EH3D-COMMON; the screens' own host tests read the table |
| The Rust programs | `eh3d-serverclient` of EH3D-COMMON (`text(Lang)` of a `ClientError`) | a test compares its table with the server's list of codes |

## Adding a code

1. The server: the code in its source, the line in `docs/API.md` and in `docs/error-codes.json`, and a test that raises it.
2. The eight texts, in the Studio catalogue (the source of the words), with the formal register in French, German and Portuguese (third person in Portuguese). The Japanese and Chinese texts are written, not machine-translated word by word.
3. Run the generator of every client that keeps a table and commit the new table in that client.
4. Upload in the order of [CLIENT_SYNC.md](CLIENT_SYNC.md): the server, the studio, then the other clients. A client that is not uploaded yet shows the code itself in English, which is still correct; it never shows an empty message.

## What the tests must catch

* a code of the server that a client has no text for;
* a text that exists in seven languages and not in eight;
* a client table that was edited by hand and no longer equals what its generator writes;
* a code that is shown to the person as a raw number or a stack trace.
