"""Deterministic survey normalization and row-level quality audit."""

import math
import re
from copy import deepcopy
from dataclasses import dataclass

import pandas as pd

from .schema import (
    CANONICAL_COLUMNS,
    DISPOSITION_PRIORITY,
    DURATION_COLUMN,
    MATRIX_COLUMNS,
    NUMERIC_RULES,
    RULES_VERSION,
    validate_columns,
)


@dataclass
class CleanResult:
    audit: pd.DataFrame
    analysis: pd.DataFrame
    qa: dict[str, object]


def _blank(value: object) -> bool:
    if isinstance(value, (list, tuple)):
        return not value
    return value is None or bool(pd.isna(value)) or str(value).strip() == ""


def _number(value: object, low: float, high: float, integer: bool) -> int | float | None:
    if _blank(value) or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or not low <= number <= high:
        return None
    if integer and not number.is_integer():
        return None
    return int(number) if integer else number


def _sources(value: object) -> list[int] | None:
    if _blank(value):
        return None
    parts = value if isinstance(value, (list, tuple)) else re.split(r"[,;|]", str(value))
    sources = [_number(part, 1, 8, True) for part in parts]
    if any(item is None for item in sources) or len(sources) != len(set(sources)):
        return None
    return sorted(sources)


def _status(value: object) -> int | None:
    labels = {"survey preview": 1, "survey test": 2}
    if str(value).strip().lower() in labels:
        return labels[str(value).strip().lower()]
    return _number(value, 0, 2, True)


def _normalize(raw: dict[str, object]) -> tuple[dict[str, object], list[str]]:
    normalized = {field: _number(raw[field], *rule) for field, rule in NUMERIC_RULES.items()}
    normalized["ResponseId"] = "" if _blank(raw["ResponseId"]) else str(raw["ResponseId"]).strip()
    normalized["Status"] = _status(raw.get("Status", "0"))
    normalized["P2"] = _sources(raw["P2"])
    # Skips after consent/screening and missing answers in unfinished responses
    # are expected. Invalid *provided* values remain visible in the audit.
    sparse = (
        normalized["Status"] in {1, 2}
        or normalized["C0"] == 2
        or normalized["S1"] == 2
        or normalized["Finished"] == 0
    )
    always_required = {"ResponseId", "Finished", "Status", DURATION_COLUMN}
    errors = []
    for field in CANONICAL_COLUMNS:
        invalid = normalized[field] is None or normalized[field] == ""
        required = not sparse or field in always_required
        if invalid and (required or not _blank(raw.get(field))):
            errors.append(field + ": missing or invalid value")
    return normalized, errors


def clean_responses(df: pd.DataFrame) -> CleanResult:
    """Apply frozen exclusions, retaining all raw rows in a private audit.

    Unknown columns and optional free text never enter either returned table.
    Duplicate handling keeps the first occurrence in input order, even if that
    earlier occurrence fails another rule. Flags overlap; dispositions do not.
    """
    validate_columns(df.columns)
    if df.columns.duplicated().any():
        raise ValueError("Duplicate column names are not supported.")
    records = []
    seen: set[str] = set()
    for position, raw in enumerate(df.to_dict(orient="records"), start=1):
        row, errors = _normalize(raw)
        row["source_row"] = raw.get("source_row", position)
        response_id = row["ResponseId"]
        matrix = [row[field] for field in MATRIX_COLUMNS]
        flags = {
            "preview_test": row["Status"] in {1, 2},
            "not_consented": row["C0"] == 2,
            "ineligible": row["S1"] == 2,
            "incomplete": row["Finished"] == 0,
            "quarantined": bool(errors),
            "possible_dupe": bool(response_id) and response_id in seen,
            "failed_attention": row["A1_3"] is not None and row["A1_3"] != 2,
            "speeder": row[DURATION_COLUMN] is not None and row[DURATION_COLUMN] < 90,
            "straightline": all(value is not None for value in matrix) and len(set(matrix)) == 1,
            "logic_error": row["P3"] is not None
            and row["P2"] is not None
            and row["P3"] not in row["P2"],
        }
        if response_id:
            seen.add(response_id)
        row.update(flags)
        row["validation_errors"] = "; ".join(errors)
        row["disposition"] = next(
            (flag for flag in DISPOSITION_PRIORITY if flags[flag]), "analysis"
        )
        records.append(row)

    safe_columns = list(CANONICAL_COLUMNS) + ["source_row"]
    audit_columns = safe_columns + list(DISPOSITION_PRIORITY) + ["validation_errors", "disposition"]
    audit = pd.DataFrame(records, columns=audit_columns)
    for flag in DISPOSITION_PRIORITY:
        audit[flag] = audit[flag].astype(bool)
    analysis = (
        audit.loc[audit["disposition"] == "analysis", safe_columns].copy().reset_index(drop=True)
    )
    counts = {
        name: int((audit["disposition"] == name).sum())
        for name in (*DISPOSITION_PRIORITY, "analysis")
    }
    raw_rows = len(audit)
    analysis_rows = len(analysis)
    excluded_rows = sum(counts[name] for name in DISPOSITION_PRIORITY)
    balanced = raw_rows == analysis_rows + excluded_rows == sum(counts.values())
    if not balanced:
        raise RuntimeError("QA reconciliation failed: raw rows do not match disposition totals.")
    qa = {
        "rules_version": RULES_VERSION,
        "raw_rows": raw_rows,
        "analysis_rows": analysis_rows,
        "excluded_rows": excluded_rows,
        "exclusion_rate": excluded_rows / raw_rows if raw_rows else 0.0,
        "disposition_counts": counts,
        "flag_counts": {flag: int(audit[flag].sum()) for flag in DISPOSITION_PRIORITY},
        "balanced": balanced,
        "median_duration_seconds": float(analysis[DURATION_COLUMN].median())
        if analysis_rows
        else None,
    }
    for key in ("input_sha256", "metadata_rows_skipped", "raw_response_rows", "ignored_columns"):
        if key in df.attrs:
            qa[key] = deepcopy(df.attrs[key])
    return CleanResult(audit=audit, analysis=analysis, qa=qa)
