# The PHOENIX programs: colour, About window and recent projects

The six PHOENIX programs share a look. It is written once, in the crate `eh3d-dock` of [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON) (`docs/DOCKING.md` there has the full tables); this page is the summary.

## One colour for each program

| Program | Palette | Principal tone |
|---|---|---|
| EH3D-PHOENIX-PCB | fire | `#FF5A1F` |
| EH3D-PHOENIX-PNP | emerald | `#2FFF94` |
| EH3D-PHOENIX-CAD | ice blue | `#2F8CFF` |
| EH3D-PHOENIX-CNC | amethyst | `#A52FFF` |
| EH3D-PHOENIX-LASER | crimson | `#FF2F43` |
| EH3D-PHOENIX-3DP | gold | `#FFD53E` |

* Only the accents of a window take the colour: main buttons, what is selected, the active tab, links and some titles. Grounds, panels, bars and body text stay as the program set them.
* Text in a colour uses a tone of the same hue that reads at 4.5 to 1 on its ground; the tests of the crate check it for the six programs on light and dark looks.
* Amber is left for cautions, and the colours that carry meaning in a drawing do not change.

## The About window

Each program shows its picture (a phoenix) inside a ring of its colour, its name, one sentence about what it is in the eight languages, the version, the author and the e-mail, links to the page of the author and to the repository, the licence, the notices of data of others where the program carries them and the notice about trademarks. The program gives only which one it is and the bytes of its picture.

## Recent projects

The list of *File > Open recent* is kept in the folder of the user, one file for each program:

| System | File |
|---|---|
| Windows | `%APPDATA%\EH3D\recent-phoenix-<program>.txt` |
| Linux, macOS | `$XDG_CONFIG_HOME/eh3d/recent-phoenix-<program>.txt`, or `~/.config/eh3d/` |

It holds paths and nothing else: an entry with `://`, which could carry a password, is never written or read. The list that the settings file held moves there the first time, and a damaged file is left aside. How many are kept is still `dock.recent_limit` of the settings file (1 to 30, 10 by default).

## State

| Piece | EH3D-COMMON | The six programs |
|---|---|---|
| Palette and About window | released in 0.3.2 | released in EH3D-PHOENIX-PCB 0.1.7 and EH3D-PHOENIX-CAD 0.1.5; in the repositories of the other four, not yet in a release |
| Accents of the window and recent projects | released in 0.3.3 | released in EH3D-PHOENIX-PCB 0.1.7 and EH3D-PHOENIX-CAD 0.1.5; in the repositories of the other four, not yet in a release |

EH3D-PHOENIX-3DP also has the golden phoenix as its application icon, in its repository.

The tests check the contrasts, the words and the files, and draw frames without a window. **No person has reviewed these windows on a screen yet.**
