"""Actual CSV ingestion tests; no header heuristics may discard participant rows."""

import csv
import hashlib
import json

import pytest

from picking_classes_blind.ingestion import read_responses

HEADERS = [
    "ResponseId",
    "Finished",
    "Duration (in seconds)",
    "C0",
    "S1",
    "S2",
    "B1",
    "B2",
    "B3",
    "B4",
    "P1",
    "P2",
    "P3",
    "P4",
    "P5",
    "O1",
    "O2",
    "O3",
    "A1_1",
    "A1_2",
    "A1_3",
    "A1_4",
]
VALUES = [
    "R_1",
    "1",
    "180",
    "1",
    "1",
    "1",
    "3",
    "1",
    "1",
    "16",
    "2",
    "1,4",
    "4",
    "2",
    "3",
    "4",
    "2",
    "8",
    "3",
    "4",
    "2",
    "4",
]


def write_csv(tmp_path, rows, encoding="utf-8"):
    path = tmp_path / "responses.csv"
    with path.open("w", newline="", encoding=encoding) as stream:
        csv.writer(stream).writerows(rows)
    return path


def test_single_header_bom_preserves_first_two_data_rows(tmp_path):
    path = write_csv(tmp_path, [HEADERS, VALUES, ["R_2"] + VALUES[1:]], "utf-8-sig")
    result = read_responses(path)
    assert result["ResponseId"].tolist() == ["R_1", "R_2"]
    assert result["source_row"].tolist() == [2, 3]
    assert result["Status"].tolist() == ["0", "0"]


def test_qualtrics_metadata_rows_are_detected_by_importid_json(tmp_path):
    metadata = [json.dumps({"ImportId": name}) for name in HEADERS]
    path = write_csv(tmp_path, [HEADERS, ["Question wording"] * len(HEADERS), metadata, VALUES])
    result = read_responses(path)
    assert result["ResponseId"].tolist() == ["R_1"]
    assert result["source_row"].tolist() == [4]


def test_arbitrary_question_like_first_response_is_not_dropped(tmp_path):
    path = write_csv(tmp_path, [HEADERS, ["R_question"] + VALUES[1:], ["R_2"] + VALUES[1:], VALUES])
    assert len(read_responses(path)) == 3


def test_split_multiselect_checked_columns_are_combined(tmp_path):
    fields = [name for name in HEADERS if name != "P2"] + [f"P2_{i}" for i in range(1, 9)]
    values = [value for name, value in zip(HEADERS, VALUES) if name != "P2"] + [
        "1",
        "0",
        "",
        "1.0",
        "0",
        "",
        "0",
        "0",
    ]
    result = read_responses(write_csv(tmp_path, [fields, values]))
    assert result.iloc[0]["P2"] == "1,4"
    assert "P2_1" not in result


def test_split_multiselect_ambiguous_recodes_are_rejected(tmp_path):
    fields = [name for name in HEADERS if name != "P2"] + [f"P2_{i}" for i in range(1, 9)]
    values = [value for name, value in zip(HEADERS, VALUES) if name != "P2"] + [
        "1",
        "0",
        "0",
        "4",
        "0",
        "0",
        "0",
        "0",
    ]
    with pytest.raises(ValueError, match="P2_4.*0.*1"):
        read_responses(write_csv(tmp_path, [fields, values]))


@pytest.mark.parametrize(
    "field,label",
    [("C0", "Yes"), ("O1", "Very satisfied"), ("P2", "Albert catalog,Upperclassmen or peers")],
)
def test_choice_label_exports_fail_with_actionable_values_message(tmp_path, field, label):
    row = dict(zip(HEADERS, VALUES)) | {field: label}
    with pytest.raises(ValueError, match="[Vv]alues"):
        read_responses(write_csv(tmp_path, [HEADERS, [row[key] for key in HEADERS]]))


def test_unknown_fields_are_not_returned(tmp_path):
    result = read_responses(
        write_csv(
            tmp_path,
            [
                HEADERS + ["IPAddress", "RecipientEmail", "O4"],
                VALUES + ["203.0.113.3", "private@example.com", "private free text"],
            ],
        )
    )
    assert not {"IPAddress", "RecipientEmail", "O4"} & set(result.columns)


def test_missing_column_duplicate_column_and_wrong_width_fail(tmp_path):
    with pytest.raises(ValueError, match="O1"):
        read_responses(write_csv(tmp_path, [[field for field in HEADERS if field != "O1"]]))
    with pytest.raises(ValueError, match="[Dd]uplicate"):
        read_responses(write_csv(tmp_path, [HEADERS + ["O1"]]))
    with pytest.raises(ValueError, match="row 2"):
        read_responses(write_csv(tmp_path, [HEADERS, VALUES[:-1]]))


def test_empty_input_and_header_only_are_distinct(tmp_path):
    with pytest.raises(ValueError, match="[Ee]mpty"):
        read_responses(write_csv(tmp_path, []))
    result = read_responses(write_csv(tmp_path, [HEADERS]))
    assert result.empty
    assert "source_row" in result


def test_provenance_hashes_exact_input_bytes_including_bom(tmp_path):
    path = write_csv(tmp_path, [HEADERS, VALUES], "utf-8-sig")
    original_bytes = path.read_bytes()
    result = read_responses(path)
    assert result.attrs["input_sha256"] == hashlib.sha256(original_bytes).hexdigest()
    assert result.attrs["input_sha256"] != hashlib.sha256(original_bytes[3:]).hexdigest()
    path.write_bytes(b"changed after parsing")
    assert result.iloc[0]["ResponseId"] == "R_1"
    assert result.attrs["input_sha256"] == hashlib.sha256(original_bytes).hexdigest()
    assert result.attrs["metadata_rows_skipped"] == 0
    assert result.attrs["raw_response_rows"] == 1


def test_metadata_provenance_counts_response_rows_without_leaking_unknown_values(tmp_path):
    headers = HEADERS + ["RecipientEmail", "O4"]
    metadata = [json.dumps({"ImportId": name}) for name in headers]
    path = write_csv(
        tmp_path,
        [
            headers,
            ["Question wording"] * len(headers),
            metadata,
            VALUES + ["private@example.com", "Private comment"],
        ],
    )
    result = read_responses(path)
    assert result.attrs["metadata_rows_skipped"] == 2
    assert result.attrs["raw_response_rows"] == 1
    assert result.attrs["ignored_columns"] == ["RecipientEmail", "O4"]
    assert "private@example.com" not in repr(result.attrs)
    assert "Private comment" not in repr(result.attrs)
    assert "private@example.com" not in result.to_csv(index=False)
