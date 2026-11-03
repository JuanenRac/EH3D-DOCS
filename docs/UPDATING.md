# How the suite is kept up to date

Three ways exist, for three different kinds of machine. Use the one that fits; they are not alternatives for the same computer.

| Machine | How it is updated | By what |
|---|---|---|
| The CM5 of the workshop (EH3D-SERVER and the pages of EH3D-STUDIO) | From the releases of GitHub, when an administrator asks | The Updates page of Studio and `deploy/eh3d-update.py` of EH3D-SERVER |
| A development PC | With git, building and testing in a staging copy | EH3D-UPDATER, and ELECTRO-HOBBY-3D-UPDATER above it |
| A PC that runs the modern interface | From the releases of GitHub, when the person asks | The Update window of EH3D-BUNGARD-GUI |

## The CM5 of the workshop: by releases

The CM5 that runs EH3D-SERVER (and the pages of EH3D-STUDIO) is updated **from the releases of GitHub**, by `deploy/eh3d-update.py` of EH3D-SERVER:

* The server never talks to GitHub and never replaces itself. When an administrator asks in Studio (Updates), the server leaves a request in a shared folder (`updates_dir` of `server.cfg`) and a small program started by systemd as root does the work.
* The helper downloads the file of the **latest release** of each service (`eh3d-server-<version>-linux-<arch>.tar.gz`, `eh3d-studio-<version>.tar.gz`), checks it against the SHA-256 that the release publishes, refuses an archive with names outside its folder, unpacks it beside the old one into `/opt` and moves it into place. The old folder is kept as `.previous`.
* Nothing is compiled on the CM5 and nothing is cloned with git: the program that runs is the one the release carries.
* The server refuses to apply an update, or to put one back, while a job is running, because the restart would stop it.
* The helper **replaces itself** with the copy of `eh3d-update.py` that comes in the release of the server, so a fix of the helper reaches the machine with the next update and nobody has to copy it by hand.

### The Updates page of Studio

An administrator sees, for each service, the installed version and the latest one, and:

* **The steps with their progress:** download, check the file, install and, where there is one, restart, each with a bar and its state, and a bar for the whole job (the server gives `steps` and `percent` in `GET /api/v1/updates`). The step that was running when a job failed is marked as failed. While the server restarts the page says so and goes on by itself, and when Studio itself was updated it offers a button to load it again.
* **The notes of the release:** a button beside each service opens the text of the changelog of the latest release, so the person reads what changes before updating.
* **One button for each service** (and a reinstall for the one that is current), besides the button that updates everything that is newer.
* **Undo:** a service that an update left a version behind for shows a button to put that version back (it asks first, and says which version it is when the helper knows it). The version that was installed takes its place, so doing it twice goes forward again. It is `POST /api/v1/updates/undo`; each component says `can_undo` and `previous`.
* **The history:** the last fifteen checks and updates, kept by the helper in `history.json`, and a button that empties the list (`POST /api/v1/updates/clear-history`; that request is not kept in the history it empties).

A helper that is older than the server leaves the new fields empty and the page shows what it can, so the two can be updated in either order.

### Who made the package: signatures

The SHA-256 that a release publishes only proves that the file arrived whole: whoever can replace the file can replace the hash that sits beside it. To know **who made it**, the machine can be given a file of allowed signers:

* `/etc/eh3d-update.signers` (or the option `--signers` of the helper) holds one line per public key, `eh3d-release <key type> <key>`, in the format of `ssh-keygen -Y verify`.
* **With that file present, the check is on:** the helper installs only a package for which the release publishes `<package>.sig`, an OpenSSH signature made with `ssh-keygen -Y sign -n eh3d-release`, that verifies against one of those keys. **A release without the `.sig`, or signed by another key, is refused, nothing is replaced, and the log says why.**
* Without the file the helper works as before and its log says that the hash proves the file arrived whole and not who made it.
* The private half of the key is only for releases and is never kept on a server. The steps for making the key, putting the public half on the machine and signing a release are in `docs/DEPLOY.md` of EH3D-SERVER; the step that signs a release is in [RELEASING.md](RELEASING.md).

Turning the signature check on is a decision about the machine, not about the software: a machine that has the file will refuse every release published before the signing step was part of the process.

## A development PC: by git

**EH3D-UPDATER** (and ELECTRO-HOBBY-3D-UPDATER above it, for the four ecosystems) is for the computers of the people who **develop** the suite: it finds the repositories next to each other in a folder, clones the ones that are missing (and the siblings they depend on, first), updates an existing checkout with git, builds and tests the new version in a staging copy before it replaces the old one, and keeps a backup. It is not how the CM5 is updated. ELECTRO-HOBBY-3D-UPDATER hands over to the latest EH3D-UPDATER and can show a preview of the install; it warns about pins that are behind.

## A PC with the modern interface: from the program

EH3D-BUNGARD-GUI can update itself from the releases of GitHub, **only when the person asks**:

* The Update button opens a window with the installed version and the latest one, the notes of the release as plain text, the steps (ask, download, check, put in place) with a bar each, and the last updates. Nothing is installed unless the person presses the button.
* The code is behind the cargo feature `updates` (`ureq` with `rustls`, so the program brings its own TLS and needs no system library); it sends nothing about the person or the machine.
* **A package is never installed without its SHA-256:** the package of the system (the names the release workflow publishes) is checked against the `.sha256` file that goes with it, and against the checksum of the API when it gives one. A package that does not agree, or a release that is not newer, changes nothing. This check is for integrity; it does not prove who made the package.
* **The update can be undone:** the running program is renamed (Windows) or copied (Linux and macOS) to a `.previous` file with its version, the new one takes its place in one step, the Undo button swaps them back, and the program restarts to use the one in place.
* **Settings of the program:** in its settings file a switch turns all the updates off, another looks for a new release at the start (off by default), with the hours between two looks, the address of the API and the time a connection may wait. The history of the updates is a small file beside the settings.

None of this has updated a real installation yet: the tests use stand-ins for GitHub, for systemd and for the files of the system.
