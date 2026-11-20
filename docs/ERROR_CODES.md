# Error codes: how they are named and how the tables are kept in step

A refusal or a failure is told with a stable code, never with a sentence that a program invents. The code does not change its meaning once it is published, and its sentence exists in the eight languages of the suite (English, Spanish, German, French, Italian, Japanese, Chinese and European Portuguese). A code with no text in one of the eight languages is an error of the build, not a text to improvise.

## Families of codes

| Family | Where it is raised | Where it is listed |
|---|---|---|
| `EH3D-PKG-nnn` | the project container (a `.eh3dproj` that is refused or cannot be written) | `registry/EH3D-PKG.md` of this repository |
| `EH3D-ID-nnn` | the identity of an object (an id that cannot be read or made) | `registry/EH3D-ID.md` of this repository |
| `EH3D-MAT-nnn` | the database of board materials (`EH3D-MAT-001` to `EH3D-MAT-009`) | `docs/MATERIALS.md` of EH3D-COMMON |
| `EH3D-FORMATS-nnn` | the files of the Bungard machines (drill, plot and outline files) | `docs/FORMAT_ERRORS.md` of EH3D-COMMON |
| a lower-case word (`bad_policy`, `enclosure_open`...) | the refusals of EH3D-SERVER, with the HTTP status | `docs/error-codes.json` of EH3D-SERVER |

A program that uses a family reports its codes as they are and keeps its own family for its own failures. A new code is a change of the list and of the code in the same commit; the tests of this repository and of the repository that raises it keep both lists in agreement.

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
