# EH3D-DOCS: requirements

This register is the single source of the state of each capability: `STATUS.md` and the README files cite it and never state a state that it does not. A state is one of `planned`, `prototype`, `implemented` and `validated`. `validated` means that a person has run the capability on a real machine and the evidence of the manifest says `bench` or `field`; nothing here is validated, because these are documents and tools that run on a computer and nowhere else, the tools have been tried on toy repositories and on the repositories of the suite, and no repository has published a release with the release tools.

The register has 33 requirements: 29 implemented, 0 prototype, 4 planned and 0 validated. By progress: 29 done, 0 partial, 1 pending and 3 blocked. High coverage is not proof of correctness, so each row says how it is checked: the test that names it, and what it shows.

## How to read the register

* **ID:** `DOCS-NNN`, never reused and never renumbered; a new capability takes the next number.
* **State:** `implemented` is code that is complete and tested on a computer, `prototype` is part of the capability, `planned` is not written.
* **Progress:** `done`, `partial`, `pending` (can be written without hardware) or `blocked` (waits for hardware or for another program of the suite).
* **Evidence:** `simulator` when the test runs against a toy repository built in a temporary folder, `host-test` when it checks a calculation, a reader or a screen-less piece, `none` when nothing is written yet.
* **Test:** the acceptance criterion: `file::name` is the test `name` of `tools/file.py`; a name with a slash, such as `registry/file::name`, is the path from the root without the extension. The test must exist. For a capability that is not written the cell says `planned:` and the name of the test that will show it; the day that test exists, the row must change.
* **Limits:** what is not done or not proven; a row that is `partial` or `blocked` always says it.

The check is `tools/test_requirements.py`: it reads this table, finds each test and fails when a state, a test or a count does not agree.

## Checks that every repository carries

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| DOCS-001 | The first level of the file tree is read from the README and a file the tree leaves out is named. | implemented | done | host-test | `test_ci_validate::test_a_versioned_entry_the_tree_leaves_out_is_named` | - |
| DOCS-002 | A link to a missing file or to the wrong case is found. | implemented | done | host-test | `test_check_links::test_a_link_to_a_missing_file_or_to_the_wrong_case_fails` | - |
| DOCS-003 | A banner that does not say what the manifest says is found. | implemented | done | host-test | `test_banner_check::test_the_name_of_another_repository_is_found` | - |
| DOCS-004 | The README has its sections in the order of the universal structure. | implemented | done | host-test | `test_universal_readme_check::test_the_twenty_two_sections_have_one_icon_each_and_fourteen_are_required` | - |
| DOCS-005 | The status lights are sorted from the worst to the best and the eight README names are the eight languages. | implemented | done | host-test | `test_status_lights::test_the_order_runs_from_the_worst_light_to_the_best` | - |
| DOCS-006 | A script that ends with a code outside the convention is reported. | implemented | done | host-test | `test_exit_conventions::test_a_script_that_ends_with_a_code_outside_the_convention_differs` | - |
| DOCS-007 | A workflow with an action not pinned to a commit is reported. | implemented | done | host-test | `test_workflow_hygiene::test_unpinned_and_own_and_local` | - |
| DOCS-008 | A command without a time limit is reported. | implemented | done | host-test | `test_lessons_lint::test_flags_missing_timeout_in_all_forms` | - |
| DOCS-009 | A change of code without a line in the changelog fails the check. | implemented | done | host-test | `test_changelog_pr_check::test_code_without_line_fails` | - |
| DOCS-010 | A translation that fell behind the English README is told section by section. | implemented | done | host-test | `test_readme_staleness::test_a_section_changed_only_in_english_is_told_for_every_other_language` | - |

## Shared tools

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| DOCS-011 | A copy of a shared tool that was changed is told and fails the check. | implemented | done | host-test | `test_sync_shared_tools::test_a_copy_that_was_changed_is_told_and_fails_the_check` | - |
| DOCS-012 | A tool that no longer names a vendored one is listed without deleting anything. | implemented | done | host-test | `test_vendored_tools_report::test_the_report_lists_without_deleting_and_is_the_same_twice` | - |

## The contract between the repositories

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| DOCS-013 | A suite that fits passes, and a manifest that does not fit its folder is an error. | implemented | done | simulator | `test_suite_contract::test_a_manifest_that_does_not_fit_its_folder_is_an_error` | Tried on toy suites and on the repositories next to this one. |
| DOCS-014 | A dependency by path with no version is a warning and fails only when strict. | implemented | done | simulator | `test_suite_contract::test_a_path_dependency_with_no_version_is_a_warning_and_fails_only_when_strict` | - |
| DOCS-015 | The versions of the map are those of the manifests. | implemented | done | simulator | `test_suite_contract::test_the_version_of_the_map_is_the_one_of_the_manifest` | - |
| DOCS-016 | The screens and the server agree on the port. | implemented | done | simulator | `test_suite_contract::test_the_screens_and_the_server_agree_on_the_port` | - |
| DOCS-017 | The shared data of the suite keeps the eight languages once each, with the European Portuguese. | implemented | done | host-test | `test_docs_contracts::test_portuguese_is_the_european_one` | - |
| DOCS-018 | The version of this repository is the same in its file, its manifest and its changelog. | implemented | done | host-test | `test_docs_contracts::test_the_version_file_the_manifest_and_the_changelog_say_the_same` | - |

## Versions and releases

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| DOCS-019 | A version is raised in every place that holds it and the old one is left nowhere but in the history. | implemented | done | simulator | `test_bump_version::test_every_place_gets_the_new_version_and_the_old_one_is_left_nowhere_but_in_the_history` | Tried on toy repositories; no repository has published a release with it. |
| DOCS-020 | A file left behind is found by the check and stops the bump. | implemented | done | simulator | `test_bump_version::test_a_file_left_behind_is_found_by_the_check_and_stops_the_bump` | - |
| DOCS-021 | The notes of a release are those of the version of the manifest, and a version without a section is an error. | implemented | done | simulator | `test_release_tools::test_a_version_without_a_section_is_an_error` | - |
| DOCS-022 | A release with a package without a signature is a problem. | implemented | done | host-test | `test_verify_release::test_a_package_without_a_signature_is_a_problem` | - |
| DOCS-023 | The list of materials of a release gives the same bytes for the same files. | implemented | done | host-test | `test_make_release_sbom::test_the_same_files_give_the_same_bytes` | - |
| DOCS-024 | The reusable validation workflow only reads and its inputs are those of the guide. | implemented | done | host-test | `test_validate_workflow::test_it_is_a_reusable_workflow_that_only_reads` | - |

## Workspace and new repositories

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| DOCS-025 | A path to a sibling in any folder of the repository is a need, and one that leaves the workspace is not. | implemented | done | simulator | `test_bootstrap_workspace::test_a_path_that_leaves_the_workspace_is_not_a_need` | Tried on toy repositories in a temporary folder; it has not set up a real workspace. |
| DOCS-026 | A new repository has its base files and its workflow calls the reusable validation fixed to a full commit. | implemented | done | simulator | `test_new_repo::test_the_workflow_calls_the_reusable_validation_fixed_to_a_full_commit` | Tried in a temporary folder; it has not created a real repository. |
| DOCS-027 | No light of a new repository is green when nothing ran on hardware. | implemented | done | simulator | `test_new_repo::test_no_light_is_green_because_nothing_ran_on_hardware` | - |

## Registers

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| DOCS-028 | The error codes are numbered without gaps or repeats and every row is complete. | implemented | done | host-test | `registry/test_error_codes::test_codes_are_numbered_without_gaps_or_repeats` | - |
| DOCS-029 | The identifier codes are numbered without gaps or repeats. | implemented | done | host-test | `registry/test_id_codes::test_codes_are_numbered_without_gaps_or_repeats` | - |

## Not written yet

| ID | Requirement | State | Progress | Evidence | Test | Limits |
|---|---|---|---|---|---|---|
| DOCS-030 | The capability matrix is checked against the manifests of the repositories. | planned | pending | none | `planned:matrix_check::the_capability_matrix_follows_the_manifests` | Written by hand today; only the versions and the releases of the map are checked. |
| DOCS-031 | A repository publishes a release with the release tools. | planned | blocked | none | `planned:real_release::a_repository_publishes_a_release_with_the_tools` | Needs a repository that is ready to release. |
| DOCS-032 | The workspace script sets up a real workspace and the new-repository script makes a real repository. | planned | blocked | none | `planned:real_workspace::a_real_workspace_is_set_up_and_a_real_repository_is_made` | Needs a clean computer and a new project of the suite. |
| DOCS-033 | The daily contract check reports no warning. | planned | blocked | none | `planned:contract_clean::the_suite_contract_has_no_warning` | Waits for the repositories it names to be brought up to date. |
