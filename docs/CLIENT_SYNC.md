# Keeping the clients in step with the server

A switch, a setting or a route of EH3D-SERVER is useless if the person cannot see it. The rule of the suite is that **every setting and every safety switch of the server can be shown, turned on and turned off from every client, and that a client follows each new one the server gets.** This page is the summary that the repositories link to; the full text, with the commands, is `docs/CLIENT_SYNC.md` of EH3D-SERVER.

## The three files a client copies

| What the clients need | The file | Who writes it |
|---|---|---|
| The sentence of every error code, in eight languages | `docs/error-codes.json` (code, status, description) | the tests of the server, from its source |
| Every setting and switch, with its words | `docs/settings-contract.json` (`eh3d.settings.contract/1`) | `tools/gen_settings_contract.py` of the server (`--check` in the CI) |
| Every route | `docs/openapi.json` | `tools/make_openapi.py` of the server (`--check` in the CI) |

A client copies them from the server it is built for and checks its copy against the server. It never keeps a list of its own.

## The contract of the settings

The contract lists every key of the settings file of the server: its group, its type (`boolean`, `integer`, `string`, `list`), range, default and unit, whether a change is in force at once or only when the server starts, the route that writes it, the role it needs, whether it is a secret, the kind of risk (`none`, `security`, `exposure`, `capacity`, `machine`, `data`) and three texts in each of the eight languages: the label, a short help and the warning. The same document, with the value in force of every key that is not a secret, is the answer of `GET /api/v1/settings/contract` for an administrator.

A key is written in one of two ways. Through the security policy (`PUT /api/v1/auth/policy`): a value looser than the recommended one is refused unless the request says it confirms the weak value, a value that does not fit is refused naming the key, and the change is in the audit. Or through the file of the server alone, which no route writes; the contract lists it so that a client shows its value and says where it is set.

## What a client does

1. Copy the contract into its own tree.
2. Draw the settings page from it: the groups in order, then the settings of each group. A switch for a boolean, a number with its range and unit, a text, a list. Show the warning before a change whose risk is not `none` or that needs a restart.
3. Read the values from the contract route and write them with the `write` of each entry. Do not write a key the contract does not list, and do not hide one it lists.
4. Keep a **parity guard** in the tests: it fails when the copy differs from the file of the server, when a key the client shows is not in the contract, or when a key of the contract is not shown. A client may hide a key only by naming it in a list of exceptions, with its reason.

## Who has done it

| Client | State |
|---|---|
| EH3D-STUDIO | The settings page is drawn from the contract, with the confirmations, the notice of a restart and a backup; the parity guard exists. |
| The phone apps, the touch screens and the programs of the machines | Not done yet. Each one adopts the contract in its own version and then adds the guard. |

The phone apps and the touch screens also owe the other two files: the error codes in eight languages and the routes they call (see [ERROR_CODES.md](ERROR_CODES.md)).

## The rule for the server

A key, a switch or a route added to the server needs its entry in the contract in the same commit, and the CI fails if it is forgotten. A switch that opens something, accepts something looser or turns a feature on is **off by default** and says so in its warning; a client never turns one on by itself.

## When a client falls behind

The check of the contract tells which key is missing. Do not "fix" a red guard by adding the key to the list of exceptions; add the control, or write the reason down in the exception if hiding it is meant. Order of uploading when a contract changes: the server first, then the studio, then the other clients.
