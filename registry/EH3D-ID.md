# Registry of identity codes: `EH3D-ID-001` and `EH3D-ID-002`

These are the stable codes that the object identity (the `ObjectId` of the `eh3d-container` crate of EH3D-COMMON, a UUID version 7 in canonical lowercase text) reports when an id cannot be read or made. A code never changes its meaning and is never reused. Programs show the text through the key `diag.<code>`; the codes themselves are never translated.

| Code | Title | Rule | Raised by |
|---|---|---|---|
| EH3D-ID-001 | Not a canonical UUID v7 | An id text that is not lowercase, has the wrong length or hyphens, is not hexadecimal, is not version 7 or does not have the variant bits of RFC 9562. | reader |
| EH3D-ID-002 | Clock value does not fit in 48 bits | A clock that gives a Unix time in milliseconds that does not fit the 48-bit field of a UUID v7. | generator |

## Notes

* The programs that use the identity (the design tool, the mechanical tool and the formats that name their objects) report these codes as they are and keep their own families for their own failures (`PHOENIX-<AREA>-<NNN>`).
* Adding a code is a documentation change here and a change in the container crate in the same step; the test `test_id_codes.py` and a test in the container crate keep both lists in agreement.
