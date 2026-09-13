# Picking Classes Blind — Fall 2026

Version 1.0 · Prospective instrument · Personal portfolio project

This document is the build specification for a new survey; it is not evidence that a Qualtrics survey has been published or that responses have been collected. It preserves the proposal's 16 named items, adds consent, and clarifies wording and privacy. The proposal's “13 items” label was a counting error: there are 16 original items, including one matrix, or 20 response fields after adding consent and expanding the four matrix rows.

## Opening page and consent

**Participant-facing text**

> Picking Classes Blind asks about how students studying away at NYU New York chose their courses for Fall 2026 and how they feel about their current schedules. This is a personal portfolio project, not an official NYU evaluation. It should take about 3–4 minutes.
>
> Taking part is voluntary. You can decline, skip a question, or close the survey at any time before submitting. A consent choice is required to continue. For later questions, you may see a reminder about an unanswered question, but you can continue without answering it. The final comment is optional. Your decision to take part will not affect your classes or access to advising.
>
> The survey does not ask for your name, email, NYU ID, or contact details. Please do not put identifying information about yourself or anyone else in your comment. Responses will be used to create a portfolio report and dashboard showing summaries. Individual responses and raw comments will not be published. Once you submit, the project cannot identify your response to remove it on request.
>
> Answer based on your current schedule and your experience so far this term. There are no right or wrong opinions.

Use this text only after checking the privacy settings in the launch checklist below. Add a project contact outside the response questions before launch so people can ask questions without their message being linked to a response.

**C0 — Voluntary consent**
“I have read the information above and voluntarily agree to take part.”

| Code | Display label |
|---|---|
| 1 | Yes, I agree |
| 2 | No, I do not agree |

Single choice, consent selection required to advance. If C0 = 2, end immediately with: “Thank you. You have chosen not to take part.” Do not show any substantive questions.

## Response settings

C0 requires a Yes/No selection to advance; declining ends participation. For S1 and substantive questions, use **Request Response**, not Force Response, so participants can skip after a reminder. O4 has no reminder. In this document, **analysis-required** means the pipeline needs a valid answer for inclusion in the primary analysis; it does not mean a respondent must answer. Skipped core answers remain missing and are quarantined on an otherwise finished record.

## Screener

**S1 — Study-away eligibility**
“Are you studying away at NYU New York this semester (Fall 2026)?”

| Code | Display label |
|---|---|
| 1 | Yes |
| 2 | No |

Single choice, Request Response; analysis-required. If S1 = 2, end immediately with: “Thank you for your interest. This survey is for students studying away at NYU New York in Fall 2026.” If S1 is skipped, also end because eligibility is unconfirmed, but preserve the missing answer and quarantine it rather than coding it as a valid no. S1 is the eligibility criterion; do not infer eligibility from home campus alone.

**S2 — Home campus**
“What is your home campus or site?”

| Code | Display label |
|---|---|
| 1 | NYU Shanghai |
| 2 | NYU Abu Dhabi |
| 3 | Another NYU global site |

Single choice, Request Response; analysis-required. Do not request the name of the other site.

## Background

**B1 — Year of study**
“What is your current year of undergraduate study?”

| Code | Display label |
|---|---|
| 1 | 1st year |
| 2 | 2nd year |
| 3 | 3rd year |
| 4 | 4th year |

Single choice, Request Response; analysis-required. These options retain the proposal's four-year undergraduate scope. Pilot with the intended audience before launch; if eligible students need a fifth-year or graduate option, revise this instrument and its validation rules together before collecting production responses.

**B2 — Primary field**
“Which option best describes your primary field of study?”

| Code | Display label |
|---|---|
| 1 | Computer Science or Engineering |
| 2 | Business |
| 3 | Natural sciences |
| 4 | Social sciences |
| 5 | Humanities |
| 6 | Undecided |

Single choice, Request Response; analysis-required. For more than one field, select the one you consider primary. Do not add a text field for a specific major.

**B3 — First study-away term**
“Is this your first study-away term?”

| Code | Display label |
|---|---|
| 1 | Yes |
| 2 | No |

Single choice, Request Response; analysis-required.

**B4 — Credits**
“How many credits are you enrolled in this term?”

Numeric entry, Request Response; analysis-required. Valid analysis values are numbers from 0 to 24, inclusive; decimal credits are permitted. Use native numeric validation only if a live blank-answer test confirms it remains skippable. Avoid custom validation that makes the field mandatory; the pipeline enforces the range in every case. Store the actual number, not a category code. Do not infer ineligibility from an answer of 0.

## Course-selection process

**P1 — Research time**
“Roughly how many hours did you spend researching courses before you finalized your current schedule? Round to the nearest whole hour.”

| Code | Display label |
|---|---|
| 1 | 0–2 hours |
| 2 | 3–5 hours |
| 3 | 6–10 hours |
| 4 | 11–20 hours |
| 5 | More than 20 hours |

Single choice, Request Response; analysis-required. These are ordered categories, not numeric hour measurements. Preserve their display order.

**P2 — Sources used**
“Which sources did you use when choosing your courses? Select all that apply.”

| Code | Display label |
|---|---|
| 1 | Albert course catalog |
| 2 | Course syllabi |
| 3 | Academic advisor |
| 4 | Upperclassmen or peers |
| 5 | Student group chats |
| 6 | Course-review sites |
| 7 | Professor's own webpage |
| 8 | Other |

Multiple choice, Request Response; at least one valid choice is required for primary analysis, but respondents may skip. Do not collect free text for “Other.” In the pilot, check that everyone can answer truthfully: the proposal assumes at least one source was used. If a “None” option is needed, revise P2, P3 routing, and validation before production collection rather than instructing participants to choose a false source.

**P3 — Most useful source**
“Which one of those sources was most useful when choosing your courses?”

Single choice, Request Response; analysis-required. Carry forward **only the selected choices from P2**, retaining the same recode values and labels. Never renumber the carried-forward subset. For example, selecting P2 codes 1, 4, and 5 must display those three choices and permit only P3 = 1, 4, or 5. If the respondent changes P2, invalidate or clear a P3 answer that is no longer selected, then request a fresh selection while preserving the ability to skip. If P2 is blank, hide P3 or present no selectable source; retain both blanks for validation rather than inventing an answer.

**P4 — Advisor contact**
“How many times did you talk to an academic advisor about course selection?”

| Code | Display label |
|---|---|
| 1 | 0 times |
| 2 | 1 time |
| 3 | 2–3 times |
| 4 | 4 or more times |

Single choice, Request Response; analysis-required. Codes are categories: code 1 means zero contacts.

**P5 — Credit-transfer concern**
“Before registering, how worried were you that credits would not transfer back to your home campus as you expected?”

| Code | Display label |
|---|---|
| 1 | Not at all worried |
| 2 | Slightly worried |
| 3 | Moderately worried |
| 4 | Very worried |
| 5 | Extremely worried |

Single choice, Request Response; analysis-required.

## Current experience

**O1 — Schedule satisfaction**
“How satisfied are you with the schedule you ended up with?”

| Code | Display label |
|---|---|
| 1 | Very dissatisfied |
| 2 | Dissatisfied |
| 3 | Neither satisfied nor dissatisfied |
| 4 | Satisfied |
| 5 | Very satisfied |

Single choice, Request Response; analysis-required. Report this as satisfaction at the time of answering, not final semester satisfaction.

**O2 — Schedule changes**
“Did you add, drop, or swap any course after the term started?”

| Code | Display label |
|---|---|
| 1 | No |
| 2 | Yes, one course |
| 3 | Yes, more than one course |

Single choice, Request Response; analysis-required. This is a self-reported behavior; it is not verified against registration records and is not necessarily a sign of dissatisfaction.

**O3 — Recommendation intention**
“How likely are you to recommend a study-away term to a peer?”

Single choice on an integer scale from 0 to 10, Request Response; analysis-required. Show every value, with endpoints “0 — Not at all likely” and “10 — Extremely likely.” Store the actual displayed value, including 0. No default selection. This measures recommendation intention; it does not measure retention, persistence, or whether someone later recommends a term.

**A1 — Information and schedule agreement**
“How much do you agree or disagree with each statement?”

Use one response per row, Request Response; all four rows are analysis-required, but each may be skipped. Keep this row order fixed; do not randomize the quality-control row.

| Export field | Statement |
|---|---|
| A1_1 | I had enough information to judge course workload before registering. |
| A1_2 | I understood how these courses count toward my degree requirements. |
| A1_3 | For quality control, please select “Disagree” for this row. |
| A1_4 | I would choose the same schedule again. |

| Code | Display label for every row |
|---|---|
| 1 | Strongly disagree |
| 2 | Disagree |
| 3 | Neither agree nor disagree |
| 4 | Agree |
| 5 | Strongly agree |

The valid attention answer is **A1_3 = 2**. A missing answer is missing data, not a failed attention check. Render row labels and all response labels accessibly on mobile; do not depend on a wide desktop-only grid.

**O4 — Optional comment**
“What is one thing that would have made course selection easier? Please do not include names, contact details, course sections, or other details that could identify you or someone else.”

Text entry, optional, with no forced response. Blank is valid. Do not publish raw comments; retain O4 only in the private raw export, not in cleaned-data or row-audit files. Review for identifying details before any separately controlled internal thematic summary.

**Submission message**
“Thank you for sharing your experience. Your response has been submitted.”

## Export contract

Use the original item IDs as stable Qualtrics export tags. Export recode values, not display text. One substantive response has these 20 fields, in addition to explicitly allowed technical metadata:

```text
C0,S1,S2,B1,B2,B3,B4,P1,P2,P3,P4,P5,O1,O2,O3,A1_1,A1_2,A1_3,A1_4,O4
```

Canonical P2 stores distinct selected codes in one comma-separated cell, such as `"1,4,5"`; normal CSV quoting is necessary. A single selected option can be `4`. A blank is missing and is not the same as “Other.” Do not treat an unselected P2 source as a missing response once P2 contains a valid selection.

Retain `ResponseId`, `Duration (in seconds)`, `Finished`, and the platform's response/test classification only as needed for QA. The project pipeline's import specification controls accepted metadata aliases. ResponseId is a random record key, not a participant identifier; do not create persistent device or person IDs. Missing analysis-required answers remain missing; never replace them with 0, the neutral scale point, or a guessed answer.

## Launch and pilot checks

- Configure an anonymous survey link. Disable collection and retention of IP address, geolocation, contact-list fields, identifying URL parameters, and device/browser fingerprints. Do not use individual tracked links or fingerprint-based duplicate detection. Check the actual export before describing the survey as anonymous.
- Do not ask for names, emails, NYU IDs, login identity, precise home sites, or identifying course details. Restrict private raw data to the project owner; publish only reviewed aggregates.
- Verify C0 = 2 and S1 = 2 end correctly; a skipped S1 also ends without recoding missing as no. No later answers are expected on these routes. Verify every substantive item can be skipped after a reminder. Keep screen-out and non-consent records separate from eligible completions.
- Check numeric recodes in an exported test file, especially P4 = 1 meaning zero contacts, O3 = 0 remaining a valid value, decimal B4 values, and A1_3 = 2 being “Disagree.”
- Test P2-to-P3 carry-forward, including going back and removing the previously selected most-useful source. Preserve original source codes.
- Pilot with approximately five people from the intended audience. Check wording, actual duration, mobile rendering, and truthful coverage of the answer options. Keep pilot and preview records out of production analysis.
- Freeze the final wording, recodes, flow, collection window, and methodology before production responses. Make any later correction a dated versioned deviation; do not silently combine incompatible instrument versions.

Review the applicable NYU requirements before recruitment. Calling this a personal project or using anonymous questions does not establish an IRB exemption or other institutional approval.
