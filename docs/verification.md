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

## Native Google Sheets and Looker Studio

Built and checked on September 13, 2026, using only the released synthetic aggregate files. The [native viewer URL](https://datastudio.google.com/reporting/8997d2e1-4538-44c5-92bd-4895674be52c/page/1Ln8F) is now documented following the owner's request to enable sharing.

| Check | Result |
|---|---|
| Native Google Sheet | Six worksheets imported and visually inspected; all 178 cells matched the verified source workbook and CSVs |
| Worksheet row counts | `summary`: 1; `sources`: 8; `satisfaction`: 5; `hours_satisfaction`: 5; `chart_status`: 4; `campus_satisfaction`: 0, with headers only |
| Embedded data sources | Connected `summary`, `sources`, `hours_satisfaction`, and `chart_status`; no campus count source connected |
| QA scorecards | MAX aggregation; 50 analysis rows, 247 seconds median analysis-row duration, 10 excluded out of 60 raw, and 16.7% exclusion rate |
| Source table with bars | All eight categories and all 16 percentage values matched `sources.csv`; numeric category order; matching 0–100% scale references |
| Hours table with bars | Five ordered categories, each with median satisfaction 3 and n=10; median scale 0–5; n displayed as a plain number |
| Release status and notice | Native status table shows three available tables and one suppressed table; campus panel states the exact small-cell withholding reason |
| Interpretation | Synthetic notice and source-randomness caption; balanced outcome/grouping fixture identified; no causal, representative, or retention claim |
| Interactions | No demographic filters, cross-filter interactions, or drill-downs |
| Repository reference | Native footer displays the full GitHub URL as plain text; the public HTML footer has a verified clickable link |
| Access settings | Saved report sharing and reopened the dialog: **Unlisted**, **Anyone on the internet with the link can view**, **Viewer**, with no pending changes. Fresh Google Sheet check showed **Saved to Drive** and **Private to only me**. Anonymous viewing has not been tested. |

The native components are scorecards and tables with bars, not the HTML preview embedded in a report. The source and hours scale references use the table style setting named **Show target**; these mark scale limits rather than performance goals. The connected status table does not control other chart visibility. The campus notice is static text, so future refreshes require manual gate checks and removal of stale charts as described in the [build and refresh guide](looker-studio.md).

## Not live-verified

The Qualtrics Advanced TXT file passed structural checks; actual import, consent/screener routing, carry-forward recodes, 0–10 export, numeric credit validation and anonymous settings must be verified in the user's account. NYU Qualtrics reached the NYU sign-in screen during this session. No survey was created or published, and no pilot or participant collection occurred.

At initial implementation completion, no Google Sheet, Looker Studio report, GitHub remote, public share link, email, recruitment post or scheduled automation had been created. The Google Sheet, native report, and public GitHub repository were subsequently created. The repository now uses `main` as its default branch. Link-based Viewer access was subsequently enabled and its saved setting verified; anonymous public viewing has not been tested. Qualtrics setup, the pilot, and participant collection are still pending. No email or recruitment post has been sent, and no scheduled automation has been created.
