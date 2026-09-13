# QA report — synthetic

Generated UTC: 2026-09-13T15:00:15.341565+00:00

Input SHA-256: `fdcd131e6a1fad66a7e350e13836ddee90be625aaf58746c5d5e6935fbf46df2`

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
