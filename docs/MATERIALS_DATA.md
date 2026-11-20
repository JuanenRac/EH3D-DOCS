# Shared data: where it lives and how to add to it

The rule of the suite is that **EH3D-COMMON is the common source of code and data, and this repository is the common source of documentation.** A table that two programs would keep each for itself lives once in COMMON, and the programs read it. Before a program creates a database or a library of its own (materials, tools, packages, components, formats), it looks in COMMON and in EH3D-CORE-LIBS, and if the thing is there it uses it; if it is almost there, it improves it there.

## The databases that exist

| Data | Crate of EH3D-COMMON | What it holds | Who reads it |
|---|---|---|---|
| Board materials | `eh3d-materials` | laminates of many makers, one JSON file per maker, with the values as the sheet publishes them (Tg, Td, Dk and Df at the published frequencies, thicknesses, copper, panel sizes, thermal conductivity of metal cores), the file of each sheet and a catalogue of the reference documents | the machine programs (a summary of each material), the design tool (the whole record, a quick library of laminates) and the server |
| Materials for 3D printing | `eh3d-printmaterials` | filaments and photopolymer resins, with the temperatures, the flow limit, the drying plan, the exposure of a resin for a printer and a layer height (interpolated between published points, never extrapolated), and generic profiles for the slicer | the slicer and the server; a program that keeps its own table of filaments moves to it |

Both databases say `verified: false` on every record until a person has tried the value on a machine. A value that a sheet does not give is left out: it is never guessed, and a bound (`more than 60 min`) or a range goes in the notes, not in a number. Prices are not data: a program takes the price the person paid.

A database that comes from an open source is kept with its licence and its notice in `THIRD_PARTY_NOTICES` of COMMON; a value that only a sheet of a maker gives is quoted from the sheet and not copied beyond the numbers.

## Adding data to COMMON

1. **A material or a maker:** write the record in the file of the maker (`crates/materials/data/<maker>.json`, or the one of the printmaterials crate), with the identifier `<maker>/<name>` in lower case with hyphens, every value as the sheet gives it, with the unit in the name of the field and the file name of the sheet (a plain name, no path) as `source`. Add a new file to the list in the module of the data: the test of that module fails when a file of the folder is not in the list.
2. **Run the tests of the crate.** They check the schema version, unique and coherent identifiers, believable ranges (a Dk or a Tg that cannot be), a plain file name as source and that no field is unknown. A failure has a code (`EH3D-MAT-001` to `EH3D-MAT-009` for board materials) that is listed in [ERROR_CODES.md](ERROR_CODES.md).
3. **Upload COMMON first.** A program repins COMMON to the tag that carries the data, in its own change, and runs its tests on the branch before main (a new COMMON can change a behaviour: for instance, an area of zero width gives a height, not a number that is not a number).
4. **Say it in the documents.** The README of the crate, `docs/MATERIALS.md` or `docs/FILAMENTS.md` of COMMON and the line of [CAPABILITY_MATRIX.md](CAPABILITY_MATRIX.md) change in the same version.

## What is still to move into COMMON

The data below is kept by more than one program today and is to be read from one place. Until it moves, a change to one copy is a change to every copy and the programs must not diverge.

* The tool tables (end mills, drills, V-bits, nozzles): the tool crib is the interface, and each program carries its own table.
* Footprints and package names: the design tool and the pick and place program each have a table of the standard families.
* Components: the component database is a small library with its own tests.
* The rules of the fabricators (the capabilities of a factory, the rules of a stencil, the area ratio): in the design tool, the pick and place program, the stencil program and the manufacturing profile. Put in COMMON as data with `verified: false` until compared with the real rules.
* Materials for the laser and for the CNC (a library with size and position): decide whether they go into the board materials or into a database of their own.

## What not to do

Do not copy a table into a program "for now". Do not write a value that a datasheet does not give. Do not publish a datasheet or a database that someone else owns: the repositories hold the numbers and the name of the file, not the file.
