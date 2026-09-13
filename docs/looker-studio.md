# One-page Looker Studio build recipe

Use the proposal's five blocks and the pipeline's aggregate CSVs. The local HTML is a runnable preview, not an exported Looker Studio report. A Google account and live report setup are still needed. Google's current documentation may call the product **Data Studio**; this project retains the proposal's Looker Studio name.

## Data preparation

Create a Google Sheet dedicated to this project. Import each CSV from the selected run's `public/` folder into a separate worksheet named after the file. Each has one header row and stable column types. Never upload `private/`, the raw Qualtrics export, individual profiles, or free text. Check `data_kind`: demo worksheets must remain visibly synthetic.

Create a Google Sheets data source for each worksheet. The connector connects one worksheet per data source; choose the header-row option and inspect numeric types. The connector reads changes to the connected Sheet; it does not run the Python pipeline or export Qualtrics data. Updating this project currently means exporting CSV, running `pcb run`, replacing worksheet contents while retaining headers, then checking the dashboard. [Google connector documentation](https://docs.cloud.google.com/data-studio/connect-to-google-sheets).

Suggested layout: 1200 × 1000 px, warm background `#F5F2E9`, ink `#202D27`, source-used green `#267257`, most-useful orange `#B74F2C`. Use a serif title and plain, readable chart text. One report page, no demographic filters, no drill-down.

## The five blocks

| Block | Worksheet | Chart and configuration |
|---|---|---|
| 1. QA status | `summary` | Four scorecards: `analysis_n`, `median_duration_seconds`, `excluded_n`, `exclusion_rate`. Use MAX for these single-row precomputed values; format the rate as percent. Caption excluded/raw and duration among analysis rows. |
| 2. Used versus most useful | `sources` | Grouped horizontal bars, dimension `source`, metrics `usage_rate` and `most_useful_rate`, MAX aggregation, percent format, sort `source_code` ascending. Fixed 0–100% scale. Add `used_count`, `most_useful_count`, and `denominator` as an adjacent compact table or tooltip. |
| 3. Satisfaction | `campus_satisfaction` | 100% stacked horizontal bars, dimension `campus`, breakdown `satisfaction` sorted 1–5, metric SUM(`count`). Show a separate `campus_n` label using MAX per campus. If this table is unavailable, use the available overall `satisfaction` table; otherwise use a text notice from `chart_status`. |
| 4. Hours and satisfaction | `hours_satisfaction` | Horizontal bars, dimension `hours`, metric MAX(`median_satisfaction`), sort `hours_code` ascending, fixed 0–5 scale. Adjacent table shows `n` with MAX aggregation, including zero for empty buckets. Blank median is no data, not zero satisfaction. If unavailable, show its suppression reason. |
| 5. Conclusion | `summary` | Text containing `conclusion`, real sample n, the recorded collection window, and `limitations`. For a synthetic source, prominently display **SYNTHETIC DEMO — not participant findings** beside the title and in this box. |

All source rates use analysis n, not the number of selected sources. P2 rates may sum above 100%; P3 rates sum to 100% before rounding. Campus shares use campus n. The time chart reports **median**, not mean, satisfaction. It does not interpret P1 category codes as hours.

## Withheld data

Read `chart_status.csv` before configuring charts. Header-only tables mean unavailable, not zero respondents. Do not connect their raw/private counterparts to fill the gap. Below n=25 there are no subgroup tables. Small outcome cells can withhold a whole table at larger n. Source counts are coarse overall totals and are not subject to per-source minimum counts; do not claim blanket small-cell suppression.

The live report does not automatically replace a chart with a notice when a worksheet becomes empty. On each refresh, apply the relevant `chart_status` state, remove stale charts or cached claims, and use the provided explanation. The generated local preview performs this fallback automatically.

## Verification before sharing

- Compare every scorecard with `qa_report.json` and each bar with its exported CSV row. Do not let a precomputed rate be summed across duplicate rows.
- Confirm blank versus zero behavior; verify category order, denominators and n labels.
- Keep the synthetic label until the data source is a reviewed participant run. Record the collection window beside real results.
- Check the report's sharing credentials: owner credentials may let viewers see report data without direct access to the Sheet. Only reviewed aggregate worksheets belong behind that report. [Google's data-credential explanation](https://docs.cloud.google.com/data-studio/connect-to-google-sheets).
- Preview the viewer experience before publication. No public report or sharing permissions are created by the local code.
