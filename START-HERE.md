# Start here

You can run and inspect this project now. Real survey collection has not started.

1. Open [the synthetic dashboard](demo/public/index.html), then [its QA report](demo/qa_report.md). The sample is artificial and exercises all primary exclusion buckets.
2. Sign in to NYU Qualtrics. Import [qualtrics-import.txt](survey/qualtrics-import.txt) into a **new** survey. Follow [the setup guide](docs/qualtrics-setup.md) to configure consent/screening, P3 carry-forward, export tags, recodes, and privacy. TXT import creates content; it does not prove routing or privacy settings are correct.
3. Complete [the five-person pilot checklist](docs/pilot-checklist.md). Keep pilot responses in a separate survey copy. Resolve whether year options 1–4 and P2 source choices cover the actual target students. Check the live 0–10 recommendation export and numeric B4 validation.
4. Record the actual collection window, project contact and raw-data deletion date in [the launch record](docs/launch-record.md). Export the final Qualtrics survey definition as `survey/final-survey.qsf` after setup, and commit it locally with the methods baseline before recruitment.
5. Run `uv sync --frozen` and `uv run pytest`. The supplied `methods-lock.json` records the delivered baseline, including the uncompleted launch record. **After completing the pilot, live setup and launch record, always create a new production lock**, even if the question wording did not change: `uv run pcb freeze --lock methods-lock-production.json`. Preserve the baseline lock, document changes, and commit the new lock and final survey export before recruitment. Subsequent amendments need a separately named lock. No real outcomes should be read before this production freeze.
6. Recruit only after the required setup and administrator permission. Keep to the fixed close date even with fewer responses. Use [the schedule and drafts](docs/launch-plan.md).
7. Export all fields as numeric values without internal-ID headers, following the import guide. Save the untouched file under `data/raw/`. Run `uv run pcb run data/raw/qualtrics-export.csv --output runs/collection-final --lock methods-lock-production.json` (use the newer lock name if subsequently amended). Review `qa_report.md` and private quarantine reasons before reporting findings.
8. Import only the aggregate `public/*.csv` tables into Google Sheets and build the report using [the Looker Studio recipe](docs/looker-studio.md). Suppressed tables remain unavailable. Replace synthetic examples in the portfolio only when real data have been collected and reviewed.

**What is ready:** local survey content, QA code, automated tests, reproducible demo, private/public output separation, dashboard recipe, and operational drafts.

**What still requires execution:** Qualtrics account configuration and pilot; actual collection; Google Sheets and Looker Studio creation; review before making anything public. Draft messages have not been sent, and no reminders have been scheduled.
