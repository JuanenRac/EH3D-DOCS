# One reader for Gerber and Excellon, and our own 2D geometry

The suite once read the same Gerber and Excellon files with several readers: the strict one of EH3D-CORE-LIBS, the one of the design tool and the one of the viewer, besides the Bungard formats crate of EH3D-COMMON that reads the files of the Bungard machines. The same file could be drawn correctly by one program and read differently by the one that drives the machine. The decision is to keep **one** reader, the one of EH3D-CORE-LIBS, with a corpus of boards and snapshots as the safety net, and to move the others to it one at a time. This page is the summary that the repositories link to; the plan with its tests is `docs/MIGRATION.md` of EH3D-CORE-LIBS, the comparison with the Bungard crate is `docs/UNIFICATION.md` and what a caller can rely on is `docs/API.md`.

## What EH3D-CORE-LIBS gives

* **The reader.** It understands block apertures and repeats, the transformations of a layer (mirror, rotation, scale, offset), incremental coordinates, negative polarity and the dialects of the common programs of electronic design. It never panics and never guesses: what it does not understand is a diagnostic with a stable code, a severity and the line.
* **The corpus and the snapshots.** A set of small boards (a board in the dialect of each common program, and one for each feature of the standard) with the SHA-256 of each file in a manifest. Next to each file is the normalised text of its reading: units, format, apertures, macros, the drawing and every diagnostic. Every length is a whole number of millionths of the unit of the file. A test rewrites the snapshots from the code and fails on any difference, so a change of what the reader understands is never unseen.
* **The 2D geometry of the suite.** `eh3d-geometry` holds the shapes of a layer (discs, rectangles, tracks and regions in millimetres with y up), the offset of shapes, the boolean operations on polygons and the fitting of arcs; `eh3d-cam` and `eh3d-raster` build on it. It is written for the suite and depends on nothing but the two readers, so a fix reaches every program that uses it.

## The steps for each program that moves

1. **Take the corpus.** Copy it with a script that checks every SHA-256 against the manifest. Never edit a file of the corpus by hand: the snapshots belong to the files. Mark it `-text` so Windows does not change the line ends.
2. **Write the adapter** that gives, for each board, the same lines as the snapshot, with the lines the old reader cannot give listed by name.
3. **Compare, do not change.** The first run is expected to differ. Each difference is a bug of the old reader, a bug of the new one (fixed there, with a board that shows it added to the corpus) or a choice (written in the table of the plan).
4. **Replace the old reader** only when the corpus passes through the adapter and the tests of the program pass as before. A file that was read correctly must give the same holes before and after.
5. **Show the diagnostics.** A line that was refused or guessed is shown to the person by the programs that drive a machine, because a hole read wrongly is a hole drilled in the wrong place.

## State

| Program | State |
|---|---|
| EH3D-ISOCAM, EH3D-STENCILCAM | already read with the reader of EH3D-CORE-LIBS |
| EH3D-PHOENIX-PCB | an adapter reads a file with both readers and compares them; the old reader is still there |
| EH3D-GERBERVIEWER | not moved yet |
| The Bungard formats crate (EH3D-DRILLPRO, EH3D-ROUTEPRO, EH3D-BUNGARD-GUI) | stays as it is for the machine's own units and DOS files; its Gerber and Excellon input is to come from the reader of CORE-LIBS through an adapter |

## Rules that do not move

* The dependency goes from the program to the library, never the other way, and the library keeps no dependencies.
* The Bungard files are not a variant of the standard ones (whole mils, plotter steps): the unit and the digits come from the machine file, never from a guess.
* The same applies to the other formats the PCB program reads (EAGLE files, the IPC-2581 interchange format, ODB++ in a bounded way): a reader that sees a hostile file reports and stops, and a corpus of examples written for the purpose stands behind it. Files that someone else owns are kept out of the repositories.
