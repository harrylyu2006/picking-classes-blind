"""Read documented single-header and Qualtrics three-header CSV exports."""

import csv
import hashlib
import io
import json
import math
from pathlib import Path

import pandas as pd

from .schema import CANONICAL_COLUMNS, SOURCE_LABELS, validate_columns


def _import_metadata(cells: list[str]) -> bool:
    nonempty = [cell for cell in cells if cell.strip()]
    if not nonempty:
        return False
    try:
        objects = [json.loads(cell) for cell in nonempty]
    except (ValueError, TypeError):
        return False
    return all(isinstance(item, dict) and "ImportId" in item for item in objects)


def _combine_sources(row: dict[str, str], line: int) -> str:
    selected = []
    for option in range(1, 9):
        field = f"P2_{option}"
        value = row[field].strip()
        if not value:
            continue
        try:
            number = float(value)
        except ValueError:
            number = math.nan
        if number not in {0, 1}:
            raise ValueError(
                f"CSV row {line}: {field} must use 0/blank (unchecked) or 1 (checked). "
                "Export numeric values; choice recodes in split columns are ambiguous."
            )
        if number == 1:
            selected.append(str(option))
    return ",".join(selected)


def _reject_labels(row: dict[str, str], line: int) -> None:
    # Recognize choice-text exports while allowing isolated corrupt values to
    # reach row-level quarantine instead of aborting the whole data file.
    common_labels = {
        "yes",
        "no",
        "very dissatisfied",
        "dissatisfied",
        "neutral",
        "satisfied",
        "very satisfied",
        "strongly disagree",
        "disagree",
        "agree",
        "strongly agree",
        "not at all",
        "slightly",
        "moderately",
        "very",
        "extremely",
        "undecided",
        "nyu shanghai",
        "nyu abu dhabi",
        "another nyu global site",
        "first",
        "second",
        "0–2",
        "3–5",
        "6–10",
        "11–20",
        "more than 20",
        "4 or more",
    }
    for field, value in row.items():
        if field in {"ResponseId", "Status", "P2"}:
            continue
        if value.strip().lower() in common_labels:
            raise ValueError(
                f"CSV row {line}: {field} contains choice labels. "
                "Re-export from Qualtrics with 'Use numeric values' enabled."
            )
    if any(label.lower() in row["P2"].lower() for label in SOURCE_LABELS.values()):
        raise ValueError(
            f"CSV row {line}: P2 contains choice labels. "
            "Re-export from Qualtrics using numeric values, not choice text."
        )


def read_responses(path: Path) -> pd.DataFrame:
    """Read UTF-8 CSV using tags and numeric choice values.

    Two Qualtrics metadata rows are skipped only when the third CSV record is
    verified ImportId JSON. Packed P2 uses numeric recodes. Split P2 requires all
    eight columns with checked=1, unchecked=0/blank. Unknown fields, including
    contact metadata and O4 free text, are discarded. source_row is the physical
    starting line in the original file, including its header records. DataFrame
    attrs record the exact input-byte hash, metadata rows skipped, response row
    count and ignored column names. No input path or ignored values are retained.
    """
    records: list[tuple[int, list[str]]] = []
    input_bytes = Path(path).read_bytes()
    try:
        with io.StringIO(input_bytes.decode("utf-8-sig"), newline="") as stream:
            reader = csv.reader(stream, strict=True)
            while True:
                line = reader.line_num + 1
                try:
                    cells = next(reader)
                except StopIteration:
                    break
                if cells:
                    records.append((line, cells))
    except (csv.Error, UnicodeError) as exc:
        raise ValueError(f"Cannot parse UTF-8 CSV: {exc}") from exc
    if not records:
        raise ValueError("Empty CSV input: export survey responses with column headers.")
    headers = [field.strip() for field in records[0][1]]
    if len(set(headers)) != len(headers):
        raise ValueError("Duplicate CSV column names are not supported.")
    if not all(headers):
        raise ValueError("CSV contains a blank column name.")
    split_fields = {f"P2_{i}" for i in range(1, 9)}
    split_sources = "P2" not in headers and split_fields.issubset(headers)
    validate_columns(headers + (["P2"] if split_sources else []))
    if "P2" in headers and split_fields.intersection(headers):
        raise ValueError(
            "CSV contains both packed P2 and split P2 columns; export one representation."
        )
    start = 3 if len(records) >= 3 and _import_metadata(records[2][1]) else 1
    parsed = []
    for line, cells in records[start:]:
        if len(cells) != len(headers):
            raise ValueError(f"CSV row {line} has {len(cells)} fields; expected {len(headers)}.")
        raw = dict(zip(headers, cells))
        if split_sources:
            raw["P2"] = _combine_sources(raw, line)
        row = {name: raw.get(name, "0" if name == "Status" else "") for name in CANONICAL_COLUMNS}
        _reject_labels(row, line)
        row["source_row"] = line
        parsed.append(row)
    result = pd.DataFrame(parsed, columns=[*CANONICAL_COLUMNS, "source_row"])
    consumed_columns = set(CANONICAL_COLUMNS) | (split_fields if split_sources else set())
    result.attrs.update(
        {
            "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
            "metadata_rows_skipped": start - 1,
            "raw_response_rows": len(parsed),
            "ignored_columns": [field for field in headers if field not in consumed_columns],
        }
    )
    return result
