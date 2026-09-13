# Pilot and release checklist

Status: **not run**. This file is a protocol, not a completed test report. Pilot responses and deliberately invalid tests must never be pooled with final collection.

## Five-person wording and usability pilot

Use a separate pilot survey. Ask five volunteers who understand the study-away context to complete it naturally; include phone and laptop use. Do not coach them on the attention check. Record elapsed time, confusing wording, navigation issues, and their interpretation of “researching courses,” “most useful,” and “recommend a study-away term.” Use anonymous pilot labels only; do not collect names or contact details in the survey.

| Pilot | Device class | Elapsed seconds | Wording/navigation problem | Change needed |
|---|---|---:|---|---|
| Pilot 1 | pending | | | |
| Pilot 2 | pending | | | |
| Pilot 3 | pending | | | |
| Pilot 4 | pending | | | |
| Pilot 5 | pending | | | |

The 3–4 minute completion estimate is provisional. If the observed time or comprehension differs, revise that estimate and wording before final launch. Five volunteers do not establish survey validity. Do not revise exclusion thresholds merely to improve a result. Any change informed by the pilot must be versioned and fixed before final responses are collected.

## Scripted live acceptance tests

These deliberate tests are additional to the five natural completions. Record the expected input, observed output, and pass/fail evidence in a private test log. Run all tests on the configured survey, then repeat critical paths on the clean production copy before recruitment.

| Check | Input/action | Required observation |
|---|---|---|
| Consent | C0 blank | Cannot advance without selecting Yes or No; closing the survey remains possible. |
| Decline | C0=2 | Ends before S1 or any substantive item. |
| Eligibility | C0=1, S1=2; separately skip S1 | Both end before background/process questions. |
| Normal completion | Consent and eligible, valid answers | Final page reachable; exported Finished indicates completion. |
| Optional answers | Skip a substantive item after its reminder; leave O4 blank | Can continue; export is blank rather than a numeric zero. |
| Credit boundaries | B4=0, 15.5, 24 | All accepted and preserved as numeric values. |
| Credit errors | B4=-1, 24.1, abc | Rejected by configured native validation or quarantined by pipeline; never silently accepted for analysis. |
| Time boundaries | Interpret 2.4 and 2.6 hours | Wording makes nearest whole hour unambiguous: first and second bands, respectively. |
| Carry-forward | P2=2,7, then P3=7 | Only the selected two choices appear; exported P3=7 belongs to P2. |
| Every source recode | Exercise all eight P2/P3 sources across test responses | P2/P3 codes match the documented 1–8 source mapping. |
| No source answer | Skip P2 | P3 is hidden and blank. |
| Back navigation | Select P3, go back, remove that choice from P2 | Saved P3 is cleared or respondent must choose a currently selected source. |
| Recommendation scale | Select O3=0, 5, and 10 in three tests | Export is exactly 0, 5, 10, never 1, 6, 11. |
| Matrix mapping | A1 rows=1,3,2,5 | Export columns A1_1…A1_4 contain 1,3,2,5. |
| Attention error | Deliberately choose A1_3=4 | Survey does not correct the answer; pipeline flags failed_attention. |
| Uniform matrix | Deliberately answer all four rows=2 | Pipeline flags straightline while attention alone passes. |
| Incomplete | Exit after starting substantive items | When the partial is recorded, pipeline labels incomplete and excludes it from the primary analysis. |
| Fast response | Deliberate complete response below 90 seconds | Pipeline labels speeder; this test is never a real participant result. |
| Duration boundary | Synthetic fixtures at 89 and 90 seconds | Strict rule is below 90; 89 is flagged and 90 is not. |
| Privacy | Inspect original pilot CSV and flow | No populated IP/location, contact, external-reference, or account-identity fields; no fingerprint collection. |
| Small screen | Complete on a phone and using keyboard navigation | No clipped wording or unreachable controls; matrix choices remain legible. |

Request Response and Force Response differ in whether skipping is allowed; custom validation can inadvertently make an item mandatory. [Qualtrics validation reference](https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/validation/)

Carry-forward recodes can differ from their source, which is why both visible choices and exported numbers require testing. [Qualtrics carry-forward reference](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/carry-forward-choices/)

## Evidence required before final collection

- [ ] All five natural pilot entries recorded above, with wording decisions documented.
- [ ] Critical consent, eligibility, carry-forward, score, matrix, skip, and privacy checks pass live.
- [ ] A real pilot CSV successfully loads through the cleaning pipeline; synthetic fixtures alone are insufficient.
- [ ] Multi-select P2 uses one comma-packed field; all editable IDs match the data dictionary.
- [ ] Overlapping QA flags do not cause double-counting; primary disposition totals reconcile to imported response rows.
- [ ] Raw pilot export is private, immutable, and separate from final input.
- [ ] Instrument version, chosen QA thresholds, final start/close dates, and changes are recorded before launch.
- [ ] Clean production survey has been checked again; no pilot responses are present.
- [ ] Qualtrics-generated QSF backup and export settings are retained privately.
- [ ] Authorized recruitment wording contains the tested anonymous link and realistic completion estimate.

**Release decision:** pending live setup and evidence. **Owner/date:** pending.
