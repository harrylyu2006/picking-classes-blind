"""Behavior tests for exclusions, normalization and private-field boundaries."""

import pandas as pd
import pytest

from picking_classes_blind.cleaning import clean_responses


def response(**changes):
    row = {
        "ResponseId": "R_1",
        "Finished": "1",
        "Status": "0",
        "Duration (in seconds)": "180",
        "C0": "1",
        "S1": "1",
        "S2": "1",
        "B1": "3",
        "B2": "1",
        "B3": "1",
        "B4": "16",
        "P1": "2",
        "P2": "1,4",
        "P3": "4",
        "P4": "2",
        "P5": "3",
        "O1": "4",
        "O2": "2",
        "O3": "8",
        "A1_1": "3",
        "A1_2": "4",
        "A1_3": "2",
        "A1_4": "4",
        "O4": "Private optional text",
    }
    return row | changes


def test_valid_decimal_recodes_and_fractional_credits_are_normalized():
    result = clean_responses(pd.DataFrame([response(B4="18.5", O3="0.0", P1="1.0")]))
    assert result.analysis.iloc[0]["B4"] == 18.5
    assert result.analysis.iloc[0]["O3"] == 0
    assert result.analysis.iloc[0]["P1"] == 1
    assert result.analysis.iloc[0]["P2"] == [1, 4]
    assert result.qa["analysis_rows"] == 1
    assert result.qa["median_duration_seconds"] == 180.0


@pytest.mark.parametrize("duration,disposition", [(89, "speeder"), (90, "analysis")])
def test_duration_boundary(duration, disposition):
    result = clean_responses(pd.DataFrame([response(**{"Duration (in seconds)": duration})]))
    assert result.audit.iloc[0]["disposition"] == disposition


@pytest.mark.parametrize(
    "credits,expected",
    [(0, "analysis"), (24, "analysis"), (-0.1, "quarantined"), (24.1, "quarantined")],
)
def test_credit_range_includes_endpoints(credits, expected):
    assert (
        clean_responses(pd.DataFrame([response(B4=credits)])).audit.iloc[0]["disposition"]
        == expected
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("O3", "5.5"),
        ("B1", "5"),
        ("O1", "NaN"),
        ("P5", "oops"),
        ("A1_3", ""),
        ("P2", "1,9"),
        ("P2", "1,,4"),
        ("P2", "1,1"),
        ("Duration (in seconds)", "inf"),
        ("ResponseId", " "),
        ("Finished", "2"),
        ("Status", "7"),
    ],
)
def test_invalid_values_are_quarantined_with_reasons(field, value):
    result = clean_responses(pd.DataFrame([response(**{field: value})]))
    assert result.qa["analysis_rows"] == 0
    assert result.audit.iloc[0]["disposition"] == "quarantined"
    assert field in result.audit.iloc[0]["validation_errors"]


@pytest.mark.parametrize("flag", ["failed_attention", "speeder", "straightline", "logic_error"])
def test_each_exclusion_is_independently_actionable(flag):
    changes = {
        "failed_attention": {"A1_3": 3},
        "speeder": {"Duration (in seconds)": 60},
        "straightline": {"A1_1": 2, "A1_2": 2, "A1_3": 2, "A1_4": 2},
        "logic_error": {"P3": 8},
    }
    result = clean_responses(pd.DataFrame([response(**changes[flag])]))
    assert result.audit.iloc[0]["disposition"] == flag
    assert bool(result.audit.iloc[0][flag])


def test_sparse_terminated_and_incomplete_rows_have_primary_disposition():
    rows = [response(), response(), response(), response()]
    for index, row in enumerate(rows):
        row.update(
            {
                key: ""
                for key in row
                if key
                not in {"ResponseId", "Finished", "Status", "C0", "S1", "Duration (in seconds)"}
            }
        )
        row["ResponseId"] = f"R_{index}"
    rows[0].update(C0=2, S1="", Finished=0)
    rows[1].update(S1=2, Finished=0)
    rows[2].update(Finished=0)
    rows[3].update(Status="Survey Preview", C0="", S1="", Finished=0)
    result = clean_responses(pd.DataFrame(rows))
    assert result.audit["disposition"].tolist() == [
        "not_consented",
        "ineligible",
        "incomplete",
        "preview_test",
    ]
    assert not result.audit["quarantined"].any()
    assert result.qa["raw_rows"] == result.qa["excluded_rows"] == 4


def test_overlapping_flags_do_not_double_count_and_duplicate_keeps_first():
    rows = [
        response(),
        response(A1_3=4, **{"Duration (in seconds)": 45}),
        response(ResponseId="R_3", P3=8),
    ]
    result = clean_responses(pd.DataFrame(rows))
    assert result.audit["disposition"].tolist() == ["analysis", "possible_dupe", "logic_error"]
    assert result.qa["flag_counts"]["failed_attention"] == 1
    assert result.qa["flag_counts"]["speeder"] == 1
    assert result.qa["flag_counts"]["possible_dupe"] == 1
    assert result.qa["raw_rows"] == result.qa["analysis_rows"] + result.qa["excluded_rows"]
    assert sum(result.qa["disposition_counts"].values()) == 3
    assert result.qa["balanced"] is True


def test_cleaning_never_leaks_unknown_identifiers_or_free_text_and_preserves_rows():
    raw = pd.DataFrame(
        [response(source_row=8, IPAddress="203.0.113.3", Email="secret@example.com")]
    )
    result = clean_responses(raw)
    for table in [result.analysis, result.audit]:
        assert not {"IPAddress", "Email", "O4"} & set(table.columns)
        assert table.iloc[0]["source_row"] == 8
    assert "IPAddress" in raw.columns
    assert raw.iloc[0]["P2"] == "1,4"


def test_empty_frame_is_balanced_and_has_no_median():
    result = clean_responses(pd.DataFrame(columns=response().keys()))
    assert result.qa["balanced"] is True
    assert result.qa["median_duration_seconds"] is None
    assert result.qa["exclusion_rate"] == 0.0


def test_missing_structural_column_fails_instead_of_publishing_empty_numbers():
    with pytest.raises(ValueError, match="O1"):
        clean_responses(pd.DataFrame([response()]).drop(columns="O1"))


def test_cleaning_carries_only_allowlisted_import_provenance():
    raw = pd.DataFrame([response()])
    raw.attrs.update(
        {
            "input_sha256": "a" * 64,
            "metadata_rows_skipped": 2,
            "raw_response_rows": 1,
            "ignored_columns": ["RecipientEmail", "O4"],
            "private_export_context": "private@example.com",
        }
    )
    result = clean_responses(raw)
    assert result.qa["input_sha256"] == "a" * 64
    assert result.qa["metadata_rows_skipped"] == 2
    assert result.qa["raw_response_rows"] == 1
    assert result.qa["ignored_columns"] == ["RecipientEmail", "O4"]
    assert "private_export_context" not in result.qa
    assert "private@example.com" not in repr(result.qa)
    raw.attrs["ignored_columns"].append("LaterColumn")
    assert result.qa["ignored_columns"] == ["RecipientEmail", "O4"]
