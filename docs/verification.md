# Verification record

Verified locally on September 13, 2026, on macOS arm64 with Python 3.12.14 and pandas 3.0.5. Only generated fixtures were used.

| Check | Result |
|---|---|
| Automated tests | 78 passed after the version 1.1 amendment |
| Package statement coverage | 96% (461 statements; 19 not covered) |
| Ruff | All checks passed |
| Environment reproduction | `uv sync --frozen --offline` succeeded using the local dependency cache |
| Methods baseline | Version 1.0 manifest preserved under `docs/methods-history/`; amended baseline frozen and `pcb verify-lock` passed |
| Synthetic end-to-end run | 60 raw = 50 analysis + 10 excluded; 11 exclusive disposition buckets reconcile |
| CSV ingestion | Single header and verified Qualtrics metadata headers; exact-byte SHA256 including BOM; numeric recodes and split/packed P2 cases tested |
| Edge cases | 89/90-second boundary; fractional credits; missing versus invalid attention; screenouts; incomplete responses; duplicate and overlapping flags; malformed values |
| Participant command path | Tested with temporary generated fixtures, including matching lock, runtime mismatch refusal, and refusal to label SYN_ rows as participant data |
| Public outputs | No ResponseId, individual profiles or raw free text in aggregate CSVs or dashboard |
| Shared disclosure rules | Synthetic and participant data use identical gates; default campus CSV is header-only; chart status is suppressed with the stated reason; other three output tables are available |
| Git exclusions | Raw files, virtual environment, run directories and any nested private directory verified ignored |
| Browser desktop | Revised demo at 1280px: no horizontal overflow; campus withholding notice visible; no exact-count disclosure; source randomness caption and GitHub footer link verified |
| Earlier mobile check | Initial version at 390px had no horizontal overflow; not repeated for the version 1.1 amendment |
| Earlier console check | Initial version had no captured warnings or errors |

Independent review found and resolved: mean/median mismatch; methods lock from another checkout authenticating the wrong runtime; hashing a later file read instead of the parsed bytes; arbitrary private-output paths not ignored by Git; and a documented fallback not present in code. Regression tests cover the substantive code fixes.

The version 1.1 amendment removes that campus fallback in favor of a visible withholding notice, and removes synthetic suppression exemptions. New regressions cover both data kinds, small samples, mixed default release states, and rendering. An independent review of all changed code and tests approved the amendment without findings. The regenerated QA output still reconciles 60 raw = 50 analysis + 10 excluded.

## Not live-verified

The Qualtrics Advanced TXT file passed structural checks; actual import, consent/screener routing, carry-forward recodes, 0–10 export, numeric credit validation and anonymous settings must be verified in the user's account. NYU Qualtrics reached the NYU sign-in screen during this session. No survey was created or published, and no pilot or participant collection occurred.

At initial implementation completion, no Google Sheet, Looker Studio report, GitHub remote, public share link, email, recruitment post or scheduled automation had been created. Survey collection and live account setup remain pending.
