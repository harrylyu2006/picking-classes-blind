# Picking Classes Blind: prospective methodology

Version 1.0 · Prepared before collection of real responses · Personal portfolio project

This is a prospective plan for a new observational survey. No real responses or findings are asserted here. Save and timestamp this plan with the final instrument before opening production collection, and preserve its version or commit identifier in the report. A local plan is not a registration in an external registry; describe it as “preregistered” only if a timestamped registration was actually completed before data access.

## Question and interpretation

Among consenting students studying away at NYU New York in Fall 2026, how do course-information sources and time spent researching courses relate to satisfaction with their current schedules?

The project will describe source use (P2), the single source selected as most useful (P3), research-time categories (P1), and schedule satisfaction (O1). Advisor contacts (P4), credit-transfer concern (P5), perceived information sufficiency (A1_1), degree-requirement understanding (A1_2), willingness to choose the same schedule (A1_4), self-reported schedule changes (O2), and recommendation intention (O3) provide context. The quality-control row A1_3 is never included in a substantive score.

This design observes experiences at one point in time. It cannot determine whether additional research hours, advising, or a particular source caused satisfaction. Students choose their sources, prior uncertainty may affect effort, and course availability and other factors may influence both process and satisfaction. O3 measures stated recommendation intention, not actual retention or persistence. O2 is a self-report and does not establish why a schedule changed. No causal effect, validated latent scale, retention measure, or representative campus estimate will be claimed.

## Population, sample, and stopping rule

Eligibility is S1 = 1: currently studying away at NYU New York in Fall 2026. Consent requires C0 = 1. The proposed response options assume undergraduates in years 1–4; the pilot must resolve any mismatch between that coverage and the recruited population before the instrument is frozen. Home-campus groups are descriptive categories, not separate sampling frames.

Recruit a convenience sample through accessible student communities after permission from the relevant group administrators. The target is approximately 40–60 eligible responses, with a smaller retained analysis sample possible after quality checks. Participation is voluntary; do not pressure peers to respond or imply the project affects academic services. Avoid collecting identity to track who has answered. Do not assert a response rate without a known invitation denominator.

Use the proposal's nine-day sequence: instrument construction on days 0–1, approximately five pilot testers on day 1, production collection on days 2–6, one reminder around day 4, closure on day 6, and analysis and presentation on days 7–9. Record the actual calendar opening and closing date, time, and timezone before launch. Close at the scheduled time even if the target is missed; do not extend collection because results appear uninteresting or subgroup counts are low. Testers and preview records are excluded from production results.

If the retained analysis sample is below 25, publish only overall descriptive summaries; do not produce cross-tabulations or subgroup comparisons. If there are no retained responses, provide the QA accounting and state that no participant results are available. Synthetic demonstration data are labeled as synthetic and never counted toward a real sample target.

## Privacy and governance

The survey contains no name, email, NYU ID, exact other-campus name, or contact question. Verify anonymous-link settings and exported metadata before launch: no retained IP addresses, geolocation, contact-list identifiers, tracked URL parameters, or device/browser fingerprints. Do not implement the proposal's fingerprint duplicate rule because it conflicts with the anonymous design. A random ResponseId distinguishes records; it cannot reveal whether distinct IDs belong to the same person.

Keep real raw exports and row-level cleaned responses private and out of version control. Public deliverables contain reviewed aggregates only, with no ResponseIds, exact response timestamps, raw free text, or individual background profiles. O4 is optional and is retained only in the private raw export; cleaned-data and audit files omit the free text. Remove identifying material before any separately controlled private thematic coding and report themes only at a safe level of aggregation. Do not publish verbatim comments by default. Set and record the raw-data storage location, access restriction, and deletion date before launch.

Provide voluntary consent before screening. Participants may skip questions or leave before submitting; use Request Response reminders rather than forcing substantive answers. Explain that the project cannot locate an individual's anonymous submitted response for later removal. Add an appropriate project contact outside the response fields. The label “personal portfolio project” does not establish an institutional or IRB exemption. Determine applicable NYU requirements through the appropriate institutional process before recruiting; this document makes no approval claim.

## Data and reproducibility

Use the final [survey instrument](survey-instrument.md) and the machine-readable data dictionary together. Stable substantive export fields are C0, S1, S2, B1–B4, P1–P5, O1–O4, and A1_1–A1_4. Export single-choice recode values; B4 is an actual numeric credit value, O3 an actual integer from 0 to 10, and P2 a comma-packed set of source codes. Other numeric codes are category labels, not interval measurements.

Preserve an untouched private raw export. Run the same versioned pipeline to produce row-level validation, one primary disposition per record, a QA reconciliation, and publication-safe aggregate tables. Do not hand-edit the analysis dataset. Record the instrument version, analysis-plan version, software environment, run time, raw-file checksum, production collection window, and every deviation from the frozen plan. Use synthetic fixtures to verify the pipeline before any real outcome distributions are inspected.

Only Completed/Finished production records that satisfy consent, eligibility, required-field validity, and the quality rules enter primary analysis. A platform completion marker and answered questions are distinct checks: a finished record can still contain missing values because a participant skipped a question or because of import, survey configuration, or interrupted routing problems. Here, required-field validity is an analysis condition, not a demand that participants answer.

## Frozen quality checks

Evaluate all applicable checks and preserve their individual flags. Assign exactly one primary disposition using the priority order below so records reconcile without double counting. An early disposition does not turn later missing answers into quality failures; for example, a non-consenting person is not expected to answer O1.

| Priority | Primary disposition | Rule |
|---|---|---|
| 1 | `preview_test` | Qualtrics Status explicitly identifies preview (1) or test (2). Pilot responses collected through a normal anonymous link may have Status 0, so pilot and production surveys/exports must be kept separate. No automatic pilot-person detector is implemented. |
| 2 | `not_consented` | C0 is a valid no response (2). Do not infer consent from submission alone. |
| 3 | `ineligible` | S1 is a valid no response (2). |
| 4 | `incomplete` | The completion marker explicitly indicates unfinished. Count separately; do not mix into analysis. |
| 5 | `quarantined` | Required data or required QA metadata are missing, malformed, ambiguous, or out of range. Missing consent or eligibility is quarantined, not inferred as a valid no. |
| 6 | `possible_dupe` | Repeated occurrences of the same nonmissing ResponseId beyond the retained first occurrence in raw-file order. This identifies duplicate exported records, not duplicate people. |
| 7 | `failed_attention` | A1_3 is a valid 1–5 answer other than 2. |
| 8 | `speeder` | Valid nonnegative completion duration is strictly below 90 seconds. Exactly 90 seconds passes this check. |
| 9 | `straightline` | All four matrix answers A1_1–A1_4 are valid and identical. |
| 10 | `logic_error` | Valid P3 selects a source absent from the valid P2 set. |
| 11 | `analysis` | No preceding exclusion or quarantine disposition applies. |

The implemented pipeline and import specification must use this same order. Report the distinct primary disposition counts and, separately, overlapping check counts. A row can fail attention and be too fast, but it contributes to only one primary bucket.

**Validity rules.** C0, S1, and B3 accept 1–2; S2 accepts 1–3; B1 accepts 1–4; B2 accepts 1–6; P1 accepts 1–5; P2 is a nonempty set of codes 1–8; P3 accepts 1–8; P4 accepts 1–4; P5 and O1 accept 1–5; O2 accepts 1–3; O3 accepts integers 0–10; all A1 rows accept 1–5. B4 accepts finite numeric credits from 0 through 24, including decimals. Category codes must be integers. Duration must be finite and nonnegative. Required metadata must be interpretable using the documented import contract. Any invalid value is quarantined, not clipped, recoded by guesswork, silently discarded, or converted to missing without an issue record.

**Missingness.** O4 may be blank. Core required answers on an otherwise completed, consenting, eligible record may not be imputed. A missing A1_3 is a missing required quality-check answer and belongs in quarantine; it is not `failed_attention`. A missing duration is not a `speeder`. Matrix variance is evaluated only when all four responses are valid; incomplete rows are not `straightline`. Missing P2 or P3 is a validity problem; `logic_error` applies to a membership contradiction between valid answers. Explicitly unfinished records remain `incomplete` under the priority order even if they also have missing answers.

**Duplicate limits.** A repeated ResponseId may arise from concatenated exports. Retain the first occurrence deterministically and exclude later occurrences under the rule above; inspect repeated records in the private audit for conflicting versions rather than selecting the one with a favorable outcome. Records may have other higher-priority dispositions even when the duplicate flag is present. Without identity or fingerprint collection, repeat participation across different ResponseIds cannot be reliably detected. Do not present ResponseId checking as fraud prevention.

**Straightlining limits.** Equal responses do not prove carelessness. In this four-row matrix, a respondent who selects “Disagree” on every row can pass the attention check while failing the prespecified straightline rule. Retain this limitation in the report. Do not relax or tighten the rule after seeing its effect on satisfaction. Any later sensitivity analysis must be labeled as a deviation or a separate, explicitly declared analysis; it cannot replace the primary result silently.

**Required accounting.** The number of parsed raw response records must equal the sum of the eleven primary disposition counts, including `analysis`. Qualtrics question-label or import-metadata rows are file structure, not respondent records, and are reported separately during import. A reconciliation failure stops export with a nonzero exit status. Quarantine records and reasons remain available for private QA; they are not silently dropped.

## Descriptive analysis and denominators

The primary results are descriptive; no hypothesis-test or causal-model result is planned. Give each table's sample size and denominator. Ordinal categories retain their ordered labels; do not turn P1 codes into exact hours or treat the open-ended “more than 20” category as a known numeric value.

1. **Data-quality summary:** show retained analysis n, median valid completion duration among analysis records, and the number and percentage of records assigned to each disposition. Specify the denominator of the excluded percentage as all parsed raw response records; show a separate quality-rule count if discussing only attention, speed, straightlining, duplicates, and logic checks.
2. **Source use versus most useful:** for each source, P2 usage is the number of analysis respondents who selected it divided by analysis n. P3 most-useful share is the number who selected it as the single most useful divided by analysis n. Each participant contributes at most once to a source-use count. P2 percentages can sum above 100%; P3 shares sum to 100% before rounding and privacy suppression. The P3 share is a share of all respondents, not a usefulness rating among users of that source.
3. **Schedule satisfaction:** show the count and percentage for each O1 category. With analysis n at least 25 and privacy requirements satisfied, an optional home-campus view shows the same distribution within each campus, using that campus's sample as its denominator. Small-group comparisons are exploratory and cannot establish campus differences.
4. **Research time and satisfaction:** with analysis n at least 25 and privacy requirements satisfied, show the median of O1 within each P1 category and its group n. Do not infer that more research improves or worsens satisfaction. If this chart is withheld, show its unavailability reason. The satisfaction panel may use the overall O1 distribution if available; no separate overall P1 fallback is implemented.
5. **Conclusion and limits:** state the real analysis n and collection window, describe the largest safely reportable descriptive patterns, and name the convenience sample, small size, self-report, timing, selection effects, and absence of causal or retention evidence. A zero-result run states that findings are not available.

O2, O3, P4, P5, and the three substantive A1 rows can receive overall descriptive summaries as secondary context when disclosure rules permit. They are not a composite scale and do not determine exclusions. O4 may inform an exploratory theme summary after privacy review, with the number of comments and coding approach documented; blank comments are not interpreted as “no problem.” No unplanned favorable subgroup or open-text anecdote substitutes for the primary summaries.

## Public disclosure rules

Do not publish real row-level data, raw comments, or response/audit identifiers. The implemented release rules operate on complete output tables rather than replacing small values with zeros:

| Output | Rule for real participant data |
|---|---|
| All participant-outcome summaries | Withhold when analysis n is below 5. QA and the insufficient-data status may still be shown. |
| Overall O1 satisfaction distribution | Withhold the entire table when any nonzero response-category count is below 5, or analysis n is below 5. |
| O1 satisfaction by home campus | Withhold when analysis n is below 25 or any nonzero campus-by-satisfaction cell is below 5. Withhold the entire table instead of exposing values reconstructable from totals. |
| P1 research time and median O1 satisfaction | Withhold when analysis n is below 25 or any nonempty research-time bucket contains fewer than 5 respondents. Withhold the entire table. |
| P2/P3 overall source-use and most-useful summaries | Release only when analysis n is at least 5. Use overall counts and percentages with the overall denominator; do not offer demographic filters or cross-tabulations. This rule does not apply a minimum of 5 to each individual source count. |

The source rule is narrower than a blanket small-cell suppression policy: an individual source total can be 1–4 even when the overall sample is larger. Do not describe the outputs as suppressing every count below 5. Review those coarse overall source totals before any public release, and document a stricter decision before publishing if the project requires every nonzero released count to be at least 5.

Withheld tables are absent or explicitly marked unavailable, never displayed as zero-response groups. Do not add filters, drill-down, downloads, or extra overlapping tables that recreate suppressed subgroup cells. Do not create many crossed demographic views for this small convenience sample. For analysis n below 25, omit all cross-tabulations even if some individual cells would exceed 5.

Synthetic demonstration charts may show small counts only with an unmistakable synthetic-data label. They remain subject to the n = 25 gate for subgroup views so the demo exercises the same sample-size rule. No synthetic result is evidence about real students.

## Readiness and deviations

Before recruitment, finish the approximately five-person pilot; confirm the institution's applicable requirements; verify privacy settings; lock wording, recodes, and routing; record the exact collection window and retention plan; and timestamp the instrument, methodology, and tested pipeline. These are launch steps, not assertions that accounts or approvals are already configured.

After closure, run the frozen pipeline, review reconciliation and quarantine issues before publishing outcomes, and verify all released figures against the aggregate tables. Any change to collection, eligibility, coding, thresholds, or analysis is recorded with its date, reason, whether outcomes had already been seen, and effect on comparability. Keep demonstrator output and actual participant findings visibly separate throughout the portfolio.
