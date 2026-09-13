# Qualtrics setup — Picking Classes Blind

Status: local preparation only. No survey has been imported into an account, tested live, published, or distributed. Complete this guide and the [pilot checklist](pilot-checklist.md) before collecting final responses. The instrument contains **16 original questions plus C0 consent**, not the proposal's stated 13.

## 1. Import into an empty survey

Use an account you are authorized to use; institutional access, license features, and applicable project requirements still need confirmation. Create an empty Survey project called `Picking Classes Blind — Fall 2026 — PILOT`. Under **Survey → Tools → Import/Export → Import survey**, choose `survey/qualtrics-import.txt`. TXT imports append to the current survey, so avoid importing twice into the same project. The supplied file uses documented Advanced TXT question, block, choice, answer, ID, and page-break tags; it is UTF-8, not UTF-16. [Qualtrics import documentation](https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/)

The import defines content and suggested recodes. **Routing, carry-forward behavior, privacy settings, response requirements, and numeric validation must be configured in the editor.** Do not publish the imported content as-is. Compare every question with [the instrument](survey-instrument.md), preserving the row and choice order.

## 2. Set consent and eligibility routing

Keep C0 alone in the Consent block and S1 alone in the Eligibility block. Add Force Response to C0; both Yes and No remain available. Immediately after Consent, add a Survey Flow branch: if C0 is not Yes, end the survey with “Thank you. You have chosen not to take part.” No substantive questions should appear on that path.

Use Request Response on S1. Immediately after Eligibility, add a branch: if S1 is not Yes, end with “Thank you for your interest. This survey is for students studying away at NYU New York in Fall 2026.” This includes a skipped S1. Preserve skipped S1 as missing and quarantine the record; do not recode it as an ineligible No. Preview the Yes, No, and skipped paths. Branching is configured in Survey Flow, not by editing this TXT file. [Qualtrics branch logic](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/branch-logic/)

Apply **Request Response**, rather than Force Response, to remaining substantive questions except O4. Leave O4 entirely optional. Request Response permits skipping after a reminder; Force Response blocks progression. Missing core answers remain missing and are quarantined on an otherwise finished response. Never add a validation rule that forces the correct A1 attention-check answer. [Qualtrics response requirements](https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/validation/)

## 3. Configure P3 carry-forward correctly

P2 and P3 are on separate pages. The imported P3 currently has all eight static choices so its wording and code order are reviewable. On P3, use **Question behavior → Carry forward choices → P2 → Selected Choices**. Remove the eight original static P3 choices after adding the carried choices; otherwise both sets remain and unselected sources can appear. If P2 is blank, hide P3 using question display logic; a skipped P2/P3 remains missing in the export.

Manually check P3 recodes against P2 for every potential source. Carry-forward does **not guarantee equal numeric codes** between the source and destination. [Qualtrics carry-forward documentation](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/carry-forward-choices/)

| P2 and P3 code | Source |
|---:|---|
| 1 | Albert course catalog |
| 2 | Course syllabi |
| 3 | Academic advisor |
| 4 | Upperclassmen or peers |
| 5 | Student group chats |
| 6 | Course-review sites |
| 7 | Professor's own webpage |
| 8 | Other |

Do not add an Other text box. Verify all eight mappings with pilot exports, including selecting P2 codes 2 and 7 then P3 code 7. Going back and changing P2 must not leave an unselected old P3 answer in the saved response.

## 4. Lock codes and validate numeric fields

Set editable question numbers/export tags to `C0,S1,S2,B1,B2,B3,B4,P1,P2,P3,P4,P5,O1,O2,O3,A1,O4`. Preserve A1's four rows; exported columns must be `A1_1,A1_2,A1_3,A1_4`, with the attention check in `A1_3`. A live CSV is the acceptance check for these names. Question numbers and internal Qualtrics QIDs are different; the pipeline needs the editable tags.

Use the Recode Values menu to explicitly lock the intended values before final collection. C0, S1, and B3 use Yes=1 / No=2. Other categorical items follow the listed order from 1. A1 scale points are Strongly disagree=1, Disagree=2, Neither agree nor disagree=3, Agree=4, Strongly agree=5. [Qualtrics recode values](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/recode-values/)

**O3 is a score from 0 through 10, not choice positions 1 through 11.** Although the TXT requests explicit 0–10 recodes, open O3's Recode Values and verify each number. Submit test choices 0, 5, and 10 and inspect the exported values. If the account refuses or resets zero, do not collect final responses until a tested numeric-entry version or explicit pipeline mapping is agreed and documented; never silently treat 1–11 as the score.

B4 is a single-line text entry accepting fractional credits (for example, 15.5), with an intended inclusive range of 0–24. Try native **Content validation → Number**; retain it only if a live blank-answer test still permits skipping. If native minimum/maximum controls are available, set 0 and 24 under the same condition. Otherwise retain optional text entry and enforce numeric/range checks in the cleaning pipeline. Do not use integer-only validation. [Qualtrics text-entry validation](https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/question-types-guide/standard-content/text-entry/)

Custom validation conflicts with Request Response and makes an answer required, so do not add custom bounds to an optional item. Invalid numeric values that reach the export must be quarantined by the pipeline, not edited in the CSV. [Qualtrics validation compatibility](https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/validation/)

P1 remains the proposal's five categorical time bands. Its wording asks respondents to estimate to the nearest whole hour to avoid gaps between 2 and 3 hours, etc. It is not a numeric-hours measure.

## 5. Configure privacy before any pilot response

Enable **Survey options → Security → Anonymize Responses** before collecting anything. An anonymous link alone can collect IP address and IP-derived location. Avoid individual links, contact-list fields, authentication, URL parameters that identify people, and external tracking scripts. [Qualtrics anonymous links](https://www.qualtrics.com/support/survey-platform/distributions-module/web-distribution/anonymous-link/)

Leave Same Session Detection off. Inspect Survey Flow for embedded identifying fields. Anonymize Responses applies prospectively; turning it on later is not a reliable way to remove identifying information already recorded. Review pilot exports for IPAddress, location, recipient, external-reference, and account-identity fields; they must be absent or empty. [Qualtrics security settings](https://www.qualtrics.com/support/survey-platform/survey-module/survey-options/survey-protection/)

Do not implement the proposal's browser-fingerprint matching. The local pipeline can identify repeated ResponseIds; this is not proof that different responses came from different people. Optional basic cookie-based duplicate prevention may deter repeat submissions but cannot establish one response per person. Record whether it was used. Keep raw responses and free text private, and publish only reviewed aggregates. Describing the activity as a personal portfolio project does not itself decide institutional review requirements.

## 6. Export a pilot CSV that matches the pipeline

In **Data & Analysis → Export & Import → Export Data**, choose CSV. Export the complete recorded dataset without an analysis filter. Use:

- Export **values**, not labels.
- Download all fields: **on**.
- Split multi-value fields into columns: **off**.
- Use internal IDs in header: **off**.
- Recode unanswered questions as -99: **off**; leave missing values blank.
- Use commas for decimals: **off**.

These options control numeric recodes, editable headers, missing values, and whether multiple answers share one column. [Qualtrics export options](https://www.qualtrics.com/support/survey-platform/data-and-analysis-module/data/download-data/export-options/)

Keep the original CSV unchanged, including its metadata/header rows. Verify a P2 multi-selection appears in a single `P2` field as comma-separated recodes, such as `2,7` (CSV may quote that field). Confirm B4 `15.5`, O3 `0`, and A1_3 `2` survive unchanged. Confirm `ResponseId`, `Finished`, and `Duration (in seconds)` are present; duration is in seconds. Compare the complete column list with the pipeline's data dictionary before running final collection.

## 7. Freeze after the five-person pilot

Complete [the pilot checklist](pilot-checklist.md). Keep the five-person pilot and scripted routing tests separate from final data. Create a clean production copy after wording fixes, re-check privacy, logic, recodes, and export names, and save a Qualtrics-generated QSF backup. Record the instrument version, setup date, owner, field dates, and pre-specified QA decisions. A local import file is not evidence of a working live survey.

Only then publish and obtain the anonymous link for authorized recruitment. At the planned close, ensure in-progress responses are closed/recorded as intended and export all recorded rows; the analysis distinguishes eligible completed responses from screenouts and incompletes.
