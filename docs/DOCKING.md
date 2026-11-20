# Panels and menus: the docking frame

Every desktop program of the suite is meant to behave like a professional application: panels that can be taken away and put back, moved, tabbed, split, floated over the window, folded into an edge, maximised and locked, and a menu bar with the usual menus. That is written once, as the crate `eh3d-dock` of [EH3D-COMMON](https://github.com/JuanenRac/EH3D-COMMON), and the programs use it instead of drawing a layout of their own. The full guide, with every action and every key, is `docs/DOCKING.md` of EH3D-COMMON; this page is the summary that the other repositories link to.

## What the frame gives a program

* **A tree of panels with rules that are tested.** Groups of tabs, splits with a share for each part, floating windows, folded tabs on an edge, hidden, maximised and locked states, and the repair of a layout that was damaged on disk. The model has no window in it, so all of this is tested without a screen; only the drawing needs the feature `gui` (egui).
* **Layouts kept as text in the configuration file** of the program, under the keys that start with `dock.`, and up to sixteen named workspaces. A layout is a tuned value, so it lives in the file and never in the code.
* **Shortcuts as data** and **menus declared as data**, with their words in the eight languages. A program declares its own menus and panels; the frame draws the bar and the panels, and applies what the person did after the frame has been drawn.
* **A proposal of panels and workspaces for each sector** (design, machine control, pick and place, laser, 3D printing), so every program starts from a sensible arrangement and offers `Restore the layout` to come back to it.

## How a program adopts it

1. Depend on `eh3d-dock` from the sibling folder or the published tag, with the feature `gui` in the programs that draw a window (the way to point at COMMON is in `docs/CONSUMING.md` of EH3D-COMMON).
2. Declare the panels (an identifier, a title in the eight languages, the smallest size) and the menus as data. Register the commands of the menus with the program.
3. Keep the layout and the workspaces in the configuration file of the program; do not add a second file for them.
4. Put the program in the list of migrated programs of its own `docs/STATUS.md` and take new screenshots, because the window changes.
5. Test the program with the model of the frame (no window), and check by hand, once, what the frame cannot check: how it looks.

## Order of migration

The frame is published; the programs move one at a time, each in its own version, and COMMON is repinned by the program that moves. A program that has not moved yet draws its own layout, and its README says so in the status table. Do not copy the model of the frame into a program to avoid the dependency: a fix there would not reach the copy.

## What the frame does not do

It does not decide what a panel shows, and it does not make a window run on a machine: nothing here has controlled a real machine. A locked layout refuses changes of the arrangement but never a safety action of the program.
