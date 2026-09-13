# QA report — synthetic

Generated UTC: 2026-09-13T15:44:18.756355+00:00

Input SHA-256: `d1db5f1f6197e163d1276e4f29c748b80f47970234870a395b8f191427babb7c`

Raw **60** = analysis **50** + excluded **10**. Balanced: **True**.

Every row belongs to exactly one disposition. These counts reconcile:

| Disposition | Rows |
|---|---:|
| preview_test | 1 |
| not_consented | 1 |
| ineligible | 1 |
| incomplete | 1 |
| quarantined | 1 |
| possible_dupe | 1 |
| failed_attention | 1 |
| speeder | 1 |
| straightline | 1 |
| logic_error | 1 |
| analysis | 50 |

Flags overlap. Do not sum this table to calculate exclusions:

| Flag | Rows |
|---|---:|
| preview_test | 1 |
| not_consented | 1 |
| ineligible | 1 |
| incomplete | 1 |
| quarantined | 1 |
| possible_dupe | 1 |
| failed_attention | 1 |
| speeder | 1 |
| straightline | 1 |
| logic_error | 1 |

All row-level audit and analysis files are private. Public files contain aggregate tables only. Optional free text is retained only in the original raw export, not copied into generated reports.

This report describes synthetic test cases, not participant responses.
