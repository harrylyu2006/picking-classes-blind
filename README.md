# Picking Classes Blind

**A personal portfolio project about course selection among students studying away at NYU New York, Fall 2026.**

**Status:** implemented and tested with a synthetic demonstration. A native Google Sheet and Looker Studio report have also been built and checked against the aggregate CSVs. Open the [native Looker Studio report](https://datastudio.google.com/reporting/8997d2e1-4538-44c5-92bd-4895674be52c/page/1Ln8F) or [HTML demo](demo/public/index.html), and see the [native report build record](docs/looker-studio.md). Live Qualtrics configuration, the pilot, and participant collection remain pending. Start with [START HERE](START-HERE.md).

## Question

Which information sources do students use when choosing courses at an unfamiliar campus, which do they find most useful, and how does reported preparation time relate to schedule satisfaction?

## Method

Qualtrics → an unchanged private CSV export → Python/pandas QA → aggregate CSV tables → Google Sheets → Looker Studio. The instrument has **16 proposal items plus consent**, with a four-row matrix. Target 40–60 responses, a five-person pilot, and a fixed collection window. Rules are set before real outcomes are viewed. Read the [instrument](docs/survey-instrument.md), [prospective methods](docs/methodology.md), and [data dictionary](docs/data-dictionary.csv).

The pipeline flags attention failures, speeders under 90 seconds, straightlining, repeated ResponseIds, invalid source logic, incomplete responses, and invalid/missing values. Flags may overlap; each record gets one disposition. Every run checks **raw rows = analysis rows + excluded rows**, records the exact input checksum and software versions, and produces a private audit with source-row references.

## Run locally

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/). Tested here with Python 3.12.

```bash
uv sync --frozen
uv run pytest
uv run pcb demo --output runs/my-demo
open runs/my-demo/public/index.html
```

The shipped [dashboard preview](demo/public/index.html) and [QA report](demo/qa_report.md) use **synthetic data**. The deterministic default fixture contains 60 rows, 50 retained rows, and one primary example for each of 10 exclusion dispositions. Synthetic and participant runs use the same suppression rules: sources and research-time charts are available, while the campus chart displays **Withheld: at least one nonzero cell is below five.** Source choices are uniformly random; outcome and grouping values are engineered to exercise release rules. These counts test software and are not evidence about students.

After the pilot and launch record are complete, freeze the production version before recruitment. Preserve the supplied baseline lock:

```bash
uv run pcb freeze --lock methods-lock-production.json
uv run pcb verify-lock --lock methods-lock-production.json
# After collection closes:
uv run pcb run data/raw/qualtrics-export.csv --output runs/collection-final --lock methods-lock-production.json
```

`pcb run` requires unchanged methods and the runtime from this checkout. It rejects `SYN_` test records. Every run needs a new output directory; raw files and previous runs are never overwritten. Pilot and production exports must be kept separate. See [Qualtrics setup](docs/qualtrics-setup.md) for the exact values export contract.

## Findings and limits

**Real findings: not yet available.** The delivered evidence is a tested data pipeline, QA outputs, a public HTML demonstration, and a native Looker Studio report connected to a private Google Sheet. The survey cannot establish causal effects, represent all NYU students, or measure retention. Recommendation intention is a different outcome. Below n=25, subgroup charts are withheld; additional small-cell rules apply to both synthetic and participant outcome tables. The source view uses overall counts without demographic filters. No real row-level data or free text are intended for publication.

## Deliverables

- [Qualtrics import text](survey/qualtrics-import.txt), [setup guide](docs/qualtrics-setup.md), and [pilot checklist](docs/pilot-checklist.md).
- Versioned Python package, tests, environment lock, [methods lock](methods-lock.json), and [data dictionary](docs/data-dictionary.csv).
- [One-page HTML dashboard](demo/public/index.html), aggregate CSV tables, and a completed [native Looker Studio report](https://datastudio.google.com/reporting/8997d2e1-4538-44c5-92bd-4895674be52c/page/1Ln8F); see the [build record and reproduction guide](docs/looker-studio.md).
- [Nine-day execution schedule and message drafts](docs/launch-plan.md).

Qualtrics setup, pilot participation, recruitment, collection, and review before publishing participant findings remain real execution steps. Optional API ingestion/scheduled refresh is not implemented; the current workflow starts from an explicit CSV export. The native report requires a manual release-status check whenever its aggregate worksheets are refreshed. [Proposal source](https://claude.ai/code/artifact/af678318-ea6e-4834-9246-53a61d6851c1).
