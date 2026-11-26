# The `.eh3d` project: one file for the whole design

A project of the suite can be one file with the extension `.eh3d`: a ZIP archive with one branch for each program, so the board, the case, the print, the laser and milling work and the assembly travel together and each can tell when what it was made from has changed. This page is the summary that the repositories link to. The format is defined in [`docs/FORMAT_EH3D.md`](https://github.com/JuanenRac/EH3D-COMMON/blob/main/docs/FORMAT_EH3D.md) of EH3D-COMMON, with the decisions in `docs/adr/0002-eh3d-project-container.md` and `docs/adr/0003-eh3d-attachments.md`; the code is the crate `eh3d-project`, on top of `eh3d-container`.

The older package `.eh3dproj` (the job of a machine: layers, toolpaths and vision) is not replaced. It lives inside an `.eh3d` file as the branch `manufacturing/` and comes out byte for byte.

## Branches

| Branch | What is in it | Who writes it |
|---|---|---|
| `pcb/`, `cad/`, `cnc/`, `laser/`, `pnp/`, `drillpro/`, `routepro/`, `stencilcam/`, `gerberviewer/`, `isocam/` and the like | the work of one program | that program only |
| `manufacturing/` | a `.eh3dproj` package, the job of the machines | the program that prepares the job |
| `common/`, `docs/project/`, `attachments/` | what belongs to the project as a whole | any program |
| `docs/<program>/` | the documentation of a program | that program |
| `x-<name>/` | an extension of somebody else | nobody of the suite: kept, never read |

* A program writes only its own branch. A branch it does not know is kept byte for byte.
* A branch built from another one records the content hash its source had. When the source changes, the derived branch is **out of date**: a warning (`EH3D-PKG-019`), never an error, and no program rewrites the branch of another.
* The codes of a refusal are `EH3D-PKG-001` to `EH3D-PKG-024` ([registry](../registry/EH3D-PKG.md)).

## The modules every program shares

| Module of `eh3d-project` | What it holds |
|---|---|
| `appbranch` | what a program does with its branch: save, open, import with the original and a report, take from another branch, list, extract |
| `manufacturing` | reading the job of a project and keeping what a program makes from it |
| `suiteview`, `suitetext` | what a window shows and asks about a project, and its words in the eight languages |
| `attachments`, `attachfile` | the attached files |

Before a settings file goes into a project the program asks `suiteview::sets_key` whether it gives a value to a credential, because a project is a file that is passed on.

## Who uses it today

| Program | What it does with a project | State |
|---|---|---|
| EH3D-PHOENIX-CAD | the branch `cad/`; makes a box round the board that the branch `pcb/` describes | released |
| EH3D-GERBERVIEWER | opens the job and keeps the picture in its branch | released |
| EH3D-DRILLPRO | plans the drill layers of the job and keeps the plans in its branch | released in 0.2.2 |
| EH3D-STENCILCAM | turns the paste layers of the job into stencils kept in its branch | released in 0.1.3 |
| EH3D-PHOENIX-PCB | the branch `pcb/` | in the repository, not yet in a release |
| EH3D-PHOENIX-CNC, EH3D-PHOENIX-LASER | their branch, from the command line and from the File menu of the window | in the repository, not yet in a release |
| EH3D-PHOENIX-PNP | the branch `pnp/`, from the command line | in the repository, not yet in a release |
| EH3D-ISOCAM, EH3D-ROUTEPRO | read the layers of the job and keep their results in their branch | in the repository, not yet in a release |
| EH3D-PHOENIX-3DP, EH3D-SERVER and its clients | nothing yet | not done |

The box round the board has only been tried with boards made up by tests: the board program does not write that description yet. None of the windows that handle a project has been looked at on a screen by a person.

## Attachments

Any file can be attached to a project: data sheets, manuals, office documents, drawings, video, sound or anything else. They are in the shared branch `attachments/`, stored once under the SHA-256 of their content and linked to the pieces of the design that use them (designator, value, or part number with or without manufacturer), or kept only as a link with its address and hash.

* Programs, scripts, documents with macros, compressed archives and pages that can run code are accepted, marked as dangerous and taken out only when a person agrees. Nothing is run, opened or downloaded by itself, and no name from outside becomes a path.
* One attachment may be up to 1 GiB (setting `attachments.max_mb`, 1 to 4096, 1024 by default) and the whole project stays under 4 GiB. A large file is stored in parts, so a program that knows nothing of attachments still opens the project and keeps them.
* From the command line: `eh3d-project attach`, `attach-link`, `attachments`, `extract-attachment`, `attachment-links` and `detach`.

**State:** in the repository of EH3D-COMMON and not yet in a release. No window of a program shows attachments yet.

## The viewer of attachments

The crate `eh3d-viewer` ([`docs/VIEWER.md`](https://github.com/JuanenRac/EH3D-COMMON/blob/main/docs/VIEWER.md) of EH3D-COMMON) shows an attachment inside a program: PDF pages with zoom and search (drawn by PDFium, built without a script engine or XFA, pinned by version and SHA-256 and loaded only from the folder of the program), pictures, text, Markdown, tables of values, and the text and tables of office documents. A dangerous file shows only its warning until the person confirms, and a program or a script is never launched.

| Setting | Default | Meaning |
|---|---|---|
| `viewer.max_attachment_mb` | 1024 | largest attachment shown, opened or saved |
| `viewer.max_pdf_mb` | 256 | largest PDF shown inside |
| `viewer.max_image_mb` | 64 | largest picture file shown |
| `viewer.max_text_mb` | 2 | bytes of a text file shown; the rest is cut |
| `viewer.max_office_mb` | 128 | largest office document previewed |

**State:** in the repository of EH3D-COMMON and not yet in a release. No program uses it yet, so no person has used the panel. PDFium reads the document inside the process of the program, not in a separate sandbox.

## Security

Integrity (SHA-256 of every file, and of every branch) is always there. It detects damage; it does not say who wrote the file. Everything else is optional and off by default.

* **Signatures** of a branch or of the project with Ed25519 (since EH3D-COMMON 0.3.2): `eh3d-project keygen` and `sign`, and `verify --pubkey`. Keys are always files outside the project, are never written into it and have no password. Whoever can change a file can also remove a signature, so a program that depends on signatures requires them.
* **Seal** read-only and **audit log**: done.
* **Encryption** of a branch: the record and the refusal exist; the cipher is not written.
