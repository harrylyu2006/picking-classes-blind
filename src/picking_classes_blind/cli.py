"""Commands for synthetic demonstration, methods freezing and participant-data runs."""

import argparse
import json
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from .cleaning import clean_responses
from .ingestion import read_responses
from .locking import freeze_methods, sha256, verify_methods, verify_runtime
from .rendering import render_dashboard
from .reporting import build_tables
from .synthetic import make_synthetic


def _csv_frame(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    if "P2" in result:
        result["P2"] = result["P2"].apply(
            lambda value: (
                ",".join(str(item) for item in value) if isinstance(value, (list, tuple)) else value
            )
        )
    # Prevent formula evaluation when private audit CSVs are opened in a spreadsheet.
    for column in result.select_dtypes(include=["object", "str"]).columns:
        result[column] = result[column].apply(
            lambda value: (
                "'" + value
                if isinstance(value, str) and value.startswith(("=", "+", "-", "@", "\t", "\r"))
                else value
            )
        )
    return result


def _qa_markdown(qa: dict) -> str:
    rows = "\n".join(f"| {name} | {count} |" for name, count in qa["disposition_counts"].items())
    flags = "\n".join(f"| {name} | {count} |" for name, count in qa["flag_counts"].items())
    return f"""# QA report — {qa["data_kind"]}

Generated UTC: {qa["generated_utc"]}

Input SHA-256: `{qa["input_sha256"]}`

Raw **{qa["raw_rows"]}** = analysis **{qa["analysis_rows"]}** + excluded **{qa["excluded_rows"]}**. Balanced: **{qa["balanced"]}**.

Every row belongs to exactly one disposition. These counts reconcile:

| Disposition | Rows |
|---|---:|
{rows}

Flags overlap. Do not sum this table to calculate exclusions:

| Flag | Rows |
|---|---:|
{flags}

All row-level audit and analysis files are private. Public files contain aggregate tables only. Optional free text is retained only in the original raw export, not copied into generated reports.

This report describes {"synthetic test cases, not participant responses" if qa["data_kind"] == "synthetic" else "participant data after the locked rules"}.
"""


def _write_run(
    frame: pd.DataFrame,
    output: Path,
    *,
    synthetic: bool,
    input_hash: str,
    lock_hash: str | None,
    seed: int | None = None,
) -> dict:
    cleaned = clean_responses(frame)
    qa = dict(cleaned.qa)
    qa.update(
        {
            "data_kind": "synthetic" if synthetic else "participant",
            "generated_utc": datetime.now(UTC).isoformat(),
            "input_sha256": input_hash,
            "methods_lock_sha256": lock_hash,
            "python_version": platform.python_version(),
            "pandas_version": pd.__version__,
            "seed": seed,
        }
    )
    if not qa["balanced"] or qa["raw_rows"] != qa["analysis_rows"] + qa["excluded_rows"]:
        raise ValueError("Row reconciliation failed; no dashboard was written.")
    tables = build_tables(cleaned.analysis, qa, synthetic=synthetic)
    html = render_dashboard(tables, qa, synthetic=synthetic)
    # Compute and validate everything before creating the immutable run directory.
    output.mkdir(parents=True, exist_ok=False)
    private = output / "private"
    private.mkdir(mode=0o700)
    public = output / "public"
    public.mkdir()
    for name, data in [("audit", cleaned.audit), ("analysis", cleaned.analysis)]:
        destination = private / f"{name}.csv"
        _csv_frame(data).to_csv(destination, index=False)
        destination.chmod(0o600)
    for name, table in tables.items():
        table.to_csv(public / f"{name}.csv", index=False)
    (public / "index.html").write_text(html, encoding="utf-8")
    (output / "qa_report.json").write_text(json.dumps(qa, indent=2, allow_nan=False) + "\n")
    (output / "qa_report.md").write_text(_qa_markdown(qa), encoding="utf-8")
    return qa


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Generate and process explicitly synthetic responses")
    demo.add_argument("--output", type=Path, default=Path("demo"))
    demo.add_argument("--seed", type=int, default=20260913)
    demo.add_argument("--n", type=int, default=60)
    run = commands.add_parser("run", help="Clean a Qualtrics numeric CSV under frozen methods")
    run.add_argument("input", type=Path)
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--project", type=Path, default=Path("."))
    run.add_argument("--lock", type=Path, default=Path("methods-lock.json"))
    lock = commands.add_parser("freeze", help="Record methods before collection; never overwrite")
    lock.add_argument("--project", type=Path, default=Path("."))
    lock.add_argument("--lock", type=Path, default=Path("methods-lock.json"))
    check = commands.add_parser(
        "verify-lock", help="Check locked methods without reading responses"
    )
    check.add_argument("--project", type=Path, default=Path("."))
    check.add_argument("--lock", type=Path, default=Path("methods-lock.json"))
    args = parser.parse_args(argv)
    try:
        if args.command == "freeze":
            freeze_methods(args.project, args.lock)
            print(f"Methods recorded: {args.lock}. Commit this file before collection.")
        elif args.command == "verify-lock":
            verify_methods(args.project, args.lock)
            print("Locked methods match current files.")
        else:
            if args.output.exists():
                raise FileExistsError(
                    f"Output already exists: {args.output}. Use a new run directory."
                )
            if args.command == "demo":
                import hashlib

                frame = make_synthetic(seed=args.seed, n=args.n)
                raw_csv = frame.to_csv(index=False)
                digest = hashlib.sha256(raw_csv.encode()).hexdigest()
                qa = _write_run(
                    frame,
                    args.output,
                    synthetic=True,
                    input_hash=digest,
                    lock_hash=None,
                    seed=args.seed,
                )
                (args.output / "private/synthetic-input.csv").write_text(raw_csv, encoding="utf-8")
            else:
                manifest = verify_methods(args.project, args.lock)
                from .locking import METHOD_FILES

                if set(manifest["files"]) != set(METHOD_FILES):
                    raise ValueError("Participant run requires the complete methods manifest.")
                verify_runtime(args.project)
                frame = read_responses(args.input)
                if frame["ResponseId"].astype(str).str.startswith("SYN_").any():
                    raise ValueError("Synthetic SYN_ records cannot be labeled participant data.")
                qa = _write_run(
                    frame,
                    args.output,
                    synthetic=False,
                    input_hash=frame.attrs["input_sha256"],
                    lock_hash=sha256(args.lock),
                )
            print(
                f"{qa['data_kind']}: {qa['raw_rows']} raw = {qa['analysis_rows']} analysis + "
                f"{qa['excluded_rows']} excluded. Dashboard: {args.output / 'public/index.html'}"
            )
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
