# Conventions of the repositories

* **The manifest.** Each repository has an `eh3d.project.json` with the fields the validators require (`schema_version`, `ecosystem`, `name`, `version`, `role`, `stack`, `technologies`, `deployment_target`, `maturity`, `family`, `parent`, `build`, `notes` and `native_version`). `native_version` says in which file and with which pattern the repository keeps its own version, and the check fails when it differs from the manifest.
* **The check.** `python -I tools/ci_validate.py` verifies the manifest, the versions, the changelog, the licence, the eight README files and that no private reference is in a public file. The same check runs in CI.
* **The README files.** Eight languages (English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese), with the same structure, so a heading appears in the same order in all of them.
* **Honesty about maturity.** A repository says what runs and what has only been tested on a computer; `scaffolding` means the first steps.
* **Commits** are written in English, small and about one thing.
