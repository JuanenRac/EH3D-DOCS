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
| EH3D-ANDROID-CONTROL, EH3D-IOS-CONTROL | A page draws every setting from the contract of the server, or read only from the copy kept in the app; a script of the repository checks the copy. The screens of the iPhone have not been seen on a device. |
| The touch screens | They read the contract of the server and, when they cannot, show the copy they carry, read only; a change is off by default. The firmware has not run on a module. |
| The programs of the machines | Not done yet. Each one adopts the contract in its own version and then adds the guard. |

The clients also keep the sentences of the error codes in the eight languages (see [ERROR_CODES.md](ERROR_CODES.md)).

## Example: the printers the server watches, read only

The server can keep a list of 3D printers (Bambu Lab in LAN mode, Klipper through Moonraker, or simulated ones) and read their state. It is **read only** from end to end: there is no route that sends a printer an order, a temperature, G-code or a file.

| Client | What it shows | State |
|---|---|---|
| EH3D-SERVER | `GET /api/v1/printers` and `/printers/:id` (contract `eh3d.printers.status/1`); an administrator changes the list of the server only | released in 0.2.4 |
| EH3D-STUDIO | a Printers tab with health, state, temperatures, progress, layers, job and alerts | released in 0.2.0 |
| EH3D-ANDROID-CONTROL, EH3D-IOS-CONTROL | the same list on the home page | released in 0.1.8 (Android) and 0.1.7 (iPhone); the iPhone screen has not been seen on a device |

What a printer did not say is unknown, never zero. The settings, in `server.cfg`:

| Key | Default | Meaning |
|---|---|---|
| `printers_enabled` | `false` | off: the routes answer `501 printers_off` and no connection to a printer is opened |
| `printers_max` | 8 | most printers in the list (1 to 64) |
| `printer_poll_s` | 5 | seconds between two readings (1 to 3600) |
| `printer_stale_s` | 90 | how old a reading may be and still count (5 to 3600) |
| `printer_timeout_s` | 5 | time limit of a request to Moonraker (1 to 30) |
| `bambu_lan_enabled` | `false` | a real Bambu Lab printer on the local network also needs this |

All of it has been tried against printers in memory only: **nothing has run against a real printer.**

## Example: the nodes of the pick-and-place machines stay heard

A node of a pick-and-place machine goes to its safe state when it stops hearing whoever commands it. The server must therefore ask it more often than the time it waits, also while the node is busy with a long order.

| Time | Where it is set | Default | What happens when it passes |
|---|---|---|---|
| `link_lost_ms` of a head node | `head.cfg` (500 to 600000) | 2000 | no request with the token has arrived: the head goes to its safe state |
| `server_lost_ms` of a feeder node | settings of the node (1000 to 600000) | 15000 | the server is not heard: the node stops its feeders |
| `link_lost_ms` of a feeder | settings of the node (200 to 60000) | 3000 | the feeder does not hear its node: it stops the tape and holds a fault |
| `pnp_node_poll_s` of the server | `server.cfg` (1 to 3600) | 1 | how often each node is asked |

| Piece | What it does | State |
|---|---|---|
| EH3D-SERVER | asks each node on a connection of its own and says `poll_too_slow` when the interval is too long for a node | released in 0.2.5 |
| EH3D-ANDROID-CONTROL, EH3D-IOS-CONTROL | show that warning on the card of the node | released in 0.1.8 and 0.1.7 |
| EH3D-STUDIO | shows the warnings with the time of each node | released in 0.2.1 |
| EH3D-NODE-PNP-HEAD | says its `link_lost_ms` in its status and goes on listening during a long order | released in 0.0.3 |
| EH3D-NODE-PNP-FEEDER | says its `server_lost_ms` in its status | released in 0.0.3 |

Until a node says its time, the server takes the default of its contract. All of it has been tried against simulators only: **no node has firmware or has run on a board.**

## The rule for the server

A key, a switch or a route added to the server needs its entry in the contract in the same commit, and the CI fails if it is forgotten. A switch that opens something, accepts something looser or turns a feature on is **off by default** and says so in its warning; a client never turns one on by itself.

## When a client falls behind

The check of the contract tells which key is missing. Do not "fix" a red guard by adding the key to the list of exceptions; add the control, or write the reason down in the exception if hiding it is meant. Order of uploading when a contract changes: the server first, then the studio, then the other clients.
