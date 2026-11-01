# How the suite is kept up to date

Two ways exist and they are for two different kinds of machine. Use the one that fits; they are not alternatives for the same computer.

## The CM5 of the workshop: by releases

The CM5 that runs EH3D-SERVER (and the pages of EH3D-STUDIO) is updated **from the releases of GitHub**, by `deploy/eh3d-update.py` of EH3D-SERVER:

* The server never talks to GitHub and never replaces itself. When an administrator asks in Studio (Updates), the server leaves a request in a shared folder and a small program started by systemd as root does the work.
* The helper downloads the file of the **latest release** of each service (`eh3d-server-<version>-linux-<arch>.tar.gz`, `eh3d-studio-<version>.tar.gz`), checks it against the SHA-256 that the release publishes, unpacks it beside the old one into `/opt` and moves it into place. The old folder is kept as `.previous`.
* With a file of allowed signers on the machine the helper also requires a signature of the release (see `docs/DEPLOY.md` of EH3D-SERVER); without it the hash only proves that the file arrived whole.
* Nothing is compiled on the CM5 and nothing is cloned with git: the program that runs is the one the release carries.
* The server refuses to apply an update while a job is running, because the restart would stop it.

## A development PC: by git

**EH3D-UPDATER** (and ELECTRO-HOBBY-3D-UPDATER above it, for the four ecosystems) is for the computers of the people who **develop** the suite: it finds the repositories next to each other in a folder, clones the ones that are missing (and the siblings they depend on, first), updates an existing checkout with git, builds and tests the new version in a staging copy before it replaces the old one, and keeps a backup. It is not how the CM5 is updated.
