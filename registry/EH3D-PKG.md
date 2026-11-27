# Registry of container codes: `EH3D-PKG-001` to `EH3D-PKG-026`

These are the stable codes that the shared project container (the `eh3d-container` crate of EH3D-COMMON) and the `.eh3d` project container with branches (the `eh3d-project` crate) report when they refuse a package or fail to write one. Codes 001 to 014 are those of the container; 015 to 026 are those of the project with branches. A code never changes its meaning and is never reused; a new reason gets a new number. Programs show the text through the translation key `diag.<code>` and fill in the entry name; the codes themselves are never translated.

The rules in the table are the **strict policy** that applies to new formats (`.phoenixproj`, `.eh3dproj` 1.1.0). The `.eh3dproj` 1.0.0 preset keeps the behaviour of its readers and writers: names by the old rule, exact duplicates only, and flags and data after the archive not examined.

| Code | Title | Rule | Raised by |
|---|---|---|---|
| EH3D-PKG-001 | Invalid entry name | An entry name that is empty, absolute, longer than the limit, contains `\`, `:`, a control character, an empty part, `.` or `..`, is not valid UTF-8, is not in Unicode normal form C, has a part that ends with a dot or a space or is a Windows device name (`CON`, `NUL`, `COM1`, ...), or has non-ASCII characters without the UTF-8 flag (bit 11). | reader, writer |
| EH3D-PKG-002 | Duplicate entry name | Two names that are equal, or equal once letter case and Unicode form are ignored (they would collide on Windows and macOS). | reader, writer |
| EH3D-PKG-003 | Link, device or special entry | A symbolic link, a device or any entry that is not a regular file. | reader |
| EH3D-PKG-004 | Explicit directory entry | A directory entry (the folders are implied by the names). | reader |
| EH3D-PKG-005 | ZIP64 records not allowed | ZIP64 records when the preset does not allow them. | reader |
| EH3D-PKG-006 | Encrypted entry or compression method not allowed | An encrypted entry, or a compression method outside the list of the preset. | reader |
| EH3D-PKG-007 | Damaged archive | A wrong CRC, a truncated archive, data after the end of the archive, a damaged central directory, or an entry whose size differs from the announced one. | reader |
| EH3D-PKG-008 | General-purpose flags not allowed | Flags other than bit 11 (UTF-8 names) and, when reading, bit 3 (data descriptor). | reader |
| EH3D-PKG-009 | Entry outside the allowed roots or required entry missing | A name outside the required entries, the allowed roots and the extension folders, or a required entry other than `integrity.json` that is missing. | reader, writer |
| EH3D-PKG-010 | Integrity record missing, incomplete or different | `integrity.json` is missing, does not list every other entry, or names an entry with a different size or SHA-256. | reader |
| EH3D-PKG-011 | Limit exceeded | More entries, more total bytes or a larger entry than the preset allows, or a read into memory larger than the call allows. | reader, writer |
| EH3D-PKG-012 | Time or memory budget exceeded | The decompression took longer than the time budget, or a read into memory would exceed the memory budget. | reader |
| EH3D-PKG-013 | Format version newer than supported | The format version has a newer major, or the same major and a newer minor than the reader knows (where the preset refuses newer minors). The version is checked before the roots. | reader |
| EH3D-PKG-014 | Atomic replacement failed | The temporary file could not replace the target after the bounded retries (an antivirus scanner, an indexer or a cloud-sync client may hold a file for a moment). The target is left exactly as it was. | writer |
| EH3D-PKG-015 | Branch or project record missing or invalid | `project.json`, a `branch.json` or an optional record (metadata, index of documents, report of a conversion) is missing, malformed, inconsistent with the files or with the index of the project. | project reader, writer |
| EH3D-PKG-016 | Branch content hash differs from its record | The SHA-256 of the files of a branch is not the content hash that its record or the index of the project states. | project reader |
| EH3D-PKG-017 | Write to a branch of another application refused | A program tried to write a branch that it does not own (the shared branches `common` and `docs/project` excepted). | project writer |
| EH3D-PKG-018 | Reference between branches invalid or dangling | A dependency is malformed, points to the branch itself or to a branch that is not in the file, or a branch that was asked for is not there. | project reader, writer |
| EH3D-PKG-019 | Derived data out of date | A branch was derived from a state of another branch that has changed since. A warning: the file is valid and the derived data can be updated. | project reader |
| EH3D-PKG-020 | Branch or project sealed read-only | A write to a branch or to a project that carries a seal. | project writer |
| EH3D-PKG-021 | Signature does not verify | The signature of a branch or of the project is not correct for its record and key. | project reader |
| EH3D-PKG-022 | Signature required but missing or its key unknown | A signature was required and there is none, no verifier was given, or the key or algorithm is not known. | project reader |
| EH3D-PKG-023 | Branch encrypted and its key not available | A branch is stored encrypted and cannot be read without its key; it is kept and can be extracted as it is. | project reader |
| EH3D-PKG-024 | Branch format version newer than supported | The format of a branch is newer than the program that opens it supports. Only that branch is affected. | project reader |
| EH3D-PKG-025 | File changed on disk since it was read | Another program saved the project, or took it away, after it was read: nothing is written over it. The program offers to read it again or to save under another name. | project writer |
| EH3D-PKG-026 | Signature there already and its replacement not agreed | Signing would put another signature over one that is there and nobody agreed to replace it. | project writer |

## Notes

* Integrity is not authenticity: `integrity.json` does not prove who wrote the package.
* A missing `integrity.json` is 010; any other missing required entry is 009.
* Integrity is not authenticity; 021 and 022 are about authenticity (a signature), which is optional. 019 is the only warning; every other code is a refusal.
* Adding a code is a documentation change here and a change in the container crate in the same step; the test `test_error_codes.py` and a test in the container crate keep both lists in agreement.
