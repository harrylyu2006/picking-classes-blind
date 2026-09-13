# Native Looker Studio report

**Built and verified on September 13, 2026.** A native Google Sheet supplies a one-page native Looker Studio report, **Picking Classes Blind | Synthetic Survey QA**. [Open the native report](https://datastudio.google.com/reporting/8997d2e1-4538-44c5-92bd-4895674be52c/page/1Ln8F). The connected Google Sheet remains private. The [HTML dashboard](../demo/public/index.html) is the public, reproducible demonstration. Google's current interface calls the product **Data Studio**; this project retains the proposal's Looker Studio name.

This is a synthetic software demonstration. No students have been surveyed, and none of the values below are participant findings.

## What was built

Six native worksheets were imported from the released aggregate CSVs. All 178 imported cells were checked against the source workbook and CSVs. The row counts below exclude headers:

| Worksheet | Data rows | Native report connection |
|---|---:|---|
| `summary` | 1 | Embedded Google Sheets data source |
| `sources` | 8 | Embedded Google Sheets data source |
| `satisfaction` | 5 | Imported; not used in the report |
| `hours_satisfaction` | 5 | Embedded Google Sheets data source |
| `chart_status` | 4 | Embedded Google Sheets data source |
| `campus_satisfaction` | 0 | Header-only; no chart data source |

No raw responses, individual profiles, private audit files, or free text were uploaded. The Sheet remains private. Each connected worksheet is a separate data source using owner credentials.

| Block | Native components and configuration | Verified demonstration |
|---|---|---|
| QA status | Four scorecards from `summary`, each using MAX on its precomputed value. `exclusion_rate` is formatted as percent. | 50 analysis rows; 247 seconds median duration among analysis rows; 10 excluded out of 60 raw rows; 16.7% excluded. |
| Used versus most useful | A **table with bars**: dimension `source`; MAX(`usage_rate`) and MAX(`most_useful_rate`), formatted as percent; numeric `source_code` ascending. Both bar columns use 1 as the displayed scale reference. | All eight sources and all 16 rates match `sources.csv`. The two columns share a 0–100% scale. Source choices are labeled uniformly random synthetic values. |
| Satisfaction by home campus | A visible text notice in place of the withheld chart. A separate status table displays the `chart` and `status` fields from `chart_status`. | **Withheld: at least one nonzero cell is below five.** The status table shows three available tables and one suppressed table. No campus counts are connected. |
| Hours and satisfaction | A **table with bars**: dimension `hours`; MAX(`median_satisfaction`) with scale reference 5; MAX(`n`) displayed as a plain number; numeric `hours_code` ascending. | Five ordered categories, median 3 and n=10 in each. The median column uses a 0–5 scale. |
| Conclusion and limitations | Visible synthetic notice, explanation of the engineered fixture, and study limitations. | No causal, representative, or retention claim. Recommendation intention is not retention. |

The native report uses tables with bars rather than grouped bar-chart components. This preserves visible exact values beside the bars and was checked in the Google-rendered report. The table style setting is named **Show target**: values 1 and 5 are scale references, not performance goals. There are no demographic filters, cross-filter interactions, or drill-downs.

Source values are uniformly random, while outcome and grouping values are balanced test fixtures that demonstrate available and withheld tables. The 20% “Other” most-useful value is not a substantive result.

The native report footer displays the full GitHub repository URL as plain text. The public HTML dashboard provides a clickable GitHub footer link.

## Reproduce the report

Create a dedicated Google Sheet. Import each CSV from a selected run's `public/` folder into a separate worksheet named after its file, preserving one header row and stable column types. Check `data_kind` and keep synthetic data visibly labeled. Never upload `private/` or the raw Qualtrics export.

Create a Google Sheets data source for each populated worksheet needed by the report. Select the header-row option and inspect numeric field types. Use MAX for the precomputed scorecard and table metrics, and use the **Percent** field type for rates; do not apply a percent-of-total calculation. Keep `source_code` and `hours_code` numeric for ascending category order. The connector connects one worksheet per data source. [Google connector documentation](https://docs.cloud.google.com/data-studio/connect-to-google-sheets).

Reproduce the five blocks above. Keep all eight source rows and all five hours rows visible. Use matching scale references across the two source bar columns. For available participant campus data, a 100% stacked bar chart can use dimension `campus`, breakdown `satisfaction` ordered 1–5, and SUM(`count`), with a MAX(`campus_n`) label per campus. If the campus table is unavailable, retain its reason instead of substituting another chart.

All source rates use analysis n, not the number of selected sources. P2 rates may sum above 100%; P3 rates sum to 100% before rounding. Campus shares use campus n. The hours view reports **median**, not mean, satisfaction and does not interpret category codes as exact hours. Blank medians mean no data, not zero satisfaction.

Keep the synthetic notice beside the title and conclusion. For a reviewed participant run, replace it with the actual collection window, sample size, conclusion, and limitations. Include a visible [GitHub repository](https://github.com/harrylyu2006/picking-classes-blind) link so a forwarded report remains connected to its code and methods.

## Refresh and withheld data

**Release gates are applied by the Python pipeline. Chart visibility in the native report requires manual review.** The connected status table updates from its worksheet, but it does not automatically hide another chart. The campus withholding notice is static text. The generated HTML dashboard applies release status and notices automatically.

For each refresh:

1. Run the pipeline and review `qa_report.md` and `public/chart_status.csv` before changing the Sheet. Preserve the current source files and report version for comparison.
2. Clear the existing source and hours data charts before replacing worksheets, so a withheld or incomplete new release cannot leave old bars visible. Temporarily restrict report access during the update, then restore viewer access only after verification.
3. Replace worksheet contents while retaining headers. Import only the new run's released aggregate tables. Header-only tables mean unavailable, not zero respondents; never fill them from private counterparts.
4. Apply every `chart_status` gate. Restore charts only for available tables, replace unavailable charts with their current reasons, and update the campus notice manually. Recheck the QA cards, conclusion, sample size, and data-kind label against the same run.
5. Compare each displayed value, category order, denominator, and scale with the new CSVs. Check blank-versus-zero behavior and confirm no old chart or cached claim remains before anyone views the refreshed report.

Below n=25, subgroup tables are withheld. Small outcome cells can withhold an entire table at larger n. Source counts are coarse overall totals and are not subject to a per-source minimum count. Synthetic and participant runs follow the same release rules.

The connector reads changes to the Sheet; it does not run the Python pipeline or export Qualtrics data. API ingestion, scheduled refresh, and automatic native chart replacement are not implemented.

## Access and verification

The [native viewer URL](https://datastudio.google.com/reporting/8997d2e1-4538-44c5-92bd-4895674be52c/page/1Ln8F) is supplied for sharing. Sharing is saved as **Unlisted — anyone on the internet with the link can view**, with **Viewer** access. Anonymous access has not been independently tested. Owner credentials can let an authorized report viewer see connected data without direct access to the Sheet, so only reviewed aggregate worksheets belong behind the report. [Google's credential explanation](https://docs.cloud.google.com/data-studio/connect-to-google-sheets).

The [verification record](verification.md) distinguishes the native build checks from the local pipeline tests. Before broadening access further or replacing data, review the rendered viewer experience and permissions. The repository's local code does not create a cloud report or change its sharing settings.
