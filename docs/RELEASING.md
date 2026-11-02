# Raising a version and publishing a release

Three scripts of this repository do the mechanical part. They are Python with no dependencies and run on Windows and Linux. They find the repositories next to this one; `--workspace FOLDER` says where they are when they are elsewhere, and a path can be given instead of a name.

## The version number: the odometer

Every number of the version goes from 0 to 9 and carries to the one before it: `0.0.9` becomes `0.1.0`, never `0.0.10`. Three numbers reach `0.7.9`; the next one is `0.8.0.0`, and from there four numbers: `0.8.0.9` becomes `0.8.1.0`, `0.8.9.9` becomes `0.9.0.0`, `0.9.9.9` becomes `1.0.0.0`. `bump_version.py` accepts only the version the odometer gives, unless `--explicit` is passed.

## Step by step

1. **Put the entries in the CHANGELOG.** Every change of the repository is one line under `## [Unreleased]` of its `CHANGELOG.md`, in English. A release is meant to hold at least 3 entries.
2. **See what would change.**

   ```
   python tools/bump_version.py EH3D-SERVER next "Title of the version" --dry-run
   ```

   It writes nothing and prints the changes of every file (`next` is the version of the odometer; a version can be written instead).
3. **Raise the version.**

   ```
   python tools/bump_version.py EH3D-SERVER next "Title of the version"
   ```

   It writes the new version in the manifest (`eh3d.project.json`), `Cargo.toml` and `Cargo.lock`, `package.json` and `package-lock.json`, `pyproject.toml` and the `__version__` mirror, `versionName` of the Gradle files (`versionCode` goes up by one), `MARKETING_VERSION` of `project.yml` (the build number goes up by one), the file named by `native_version`, the badge and the "Version" row of the eight README files, and it turns the `[Unreleased]` entries into `## [X.Y.Z] - Title`. The line ends (CRLF or LF) of each file stay as they were.
   It refuses to start, and writes nothing, when a file that should carry the version is missing or holds another version (`--fix-drift` overwrites the other versions on purpose). When it has written, it reads everything again and fails if any place differs from the manifest: that is the check that a package never carries an old number inside.
4. **Build what the version goes into** (firmware, APK, package) *after* the bump, and look in the result for the new number.
5. **Commit, push, and wait for the CI** of that commit.
6. **Check that everything is ready.**

   ```
   python tools/prerelease_check.py EH3D-SERVER
   ```

   It prints `OK`, `WARN`, `SKIP` or `FAIL` for the versions of all the files, the CHANGELOG, the eight README files (the status table with the same lights), the git tree (clean, nothing unpushed), the repository's own `ci_validate`, and the GitHub Actions runs of the commit (they must exist and be green; without `gh` it says it skipped them). It publishes nothing. `--no-ci` does not ask GitHub; `--allow-short` accepts a CHANGELOG section with fewer than 3 entries.
7. **Take the notes of the release.**

   ```
   python tools/release_notes.py EH3D-SERVER --check
   python tools/release_notes.py EH3D-SERVER --notes > notes.md
   python tools/release_notes.py EH3D-SERVER --title
   ```

   `--check` fails when the CHANGELOG has no section for the version of the manifest or `[Unreleased]` still holds entries. Fewer than 3 entries exits with 2 and a warning (`--allow-short` accepts it). Then publish with `gh release create vX.Y.Z --title "<the title>" --notes-file notes.md <files>`; the scripts do not publish.

## Other reports

* `python tools/readme_staleness.py [REPOSITORY ...] [--all]` says which sections of a translated README are older than the English one. It is informative and never fails.
* `python tools/vendored_tools_report.py --write docs/VENDORED_TOOLS_REPORT.md` writes the list of the scripts in `tools/` that nothing uses (see `docs/VENDORED_TOOLS_REPORT.md`). It deletes nothing.

## What the scripts do not do

* They do not change a dependency version that points at another repository of the suite (`version = "..."` next to a `path = "..."`): that number is the version of the other repository.
* They only look for `package.json` and `package-lock.json` in the root of the repository, and raise the number only in the `[package]` / `[workspace.package]` of the `Cargo.toml` files (a crate of a workspace whose version differs is left alone).
* They do not build, tag or publish.
