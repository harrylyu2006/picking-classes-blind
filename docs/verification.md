# Verification record

Verified locally on September 13, 2026, on macOS arm64 with Python 3.12.14 and pandas 3.0.5. Only generated fixtures were used.

| Check | Result |
|---|---|
| Automated tests | 59 passed |
| Package statement coverage | 95% (460 statements; 22 not covered) |
| Ruff | All checks passed |
| Environment reproduction | `uv sync --frozen --offline` succeeded using the local dependency cache |
| Methods baseline | `pcb freeze` produced the initial manifest; `pcb verify-lock` passed |
| Synthetic end-to-end run | 60 raw = 50 analysis + 10 excluded; 11 exclusive disposition buckets reconcile |
| CSV ingestion | Single header and verified Qualtrics metadata headers; exact-byte SHA256 including BOM; numeric recodes and split/packed P2 cases tested |
| Edge cases | 89/90-second boundary; fractional credits; missing versus invalid attention; screenouts; incomplete responses; duplicate and overlapping flags; malformed values |
| Participant command path | Tested with temporary generated fixtures, including matching lock, runtime mismatch refusal, and refusal to label SYN_ rows as participant data |
| Public outputs | No ResponseId, individual profiles or raw free text in aggregate CSVs or dashboard |
| Git exclusions | Raw files, virtual environment, run directories and any nested private directory verified ignored |
| Browser desktop | 1280px viewport; no horizontal overflow; exact-count disclosure opens correctly |
| Browser mobile | 390px viewport; no horizontal overflow with exact-count table open |
| Browser console | No captured warnings or errors |

Independent review found and resolved: mean/median mismatch; methods lock from another checkout authenticating the wrong runtime; hashing a later file read instead of the parsed bytes; arbitrary private-output paths not ignored by Git; and a documented fallback not present in code. Regression tests cover the substantive code fixes.

## Not live-verified

The Qualtrics Advanced TXT file passed structural checks; actual import, consent/screener routing, carry-forward recodes, 0–10 export, numeric credit validation and anonymous settings must be verified in the user's account. NYU Qualtrics reached the NYU sign-in screen during this session. No survey was created or published, and no pilot or participant collection occurred.

No Google Sheet, Looker Studio report, GitHub remote, public share link, email, recruitment post or scheduled automation was created. The dashboard is a local synthetic preview. These boundaries are also reflected in START-HERE and the launch record.
