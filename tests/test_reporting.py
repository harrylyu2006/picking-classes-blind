import pandas as pd
import pytest

from picking_classes_blind.cleaning import clean_responses
from picking_classes_blind.rendering import render_dashboard
from picking_classes_blind.reporting import build_tables
from picking_classes_blind.synthetic import make_synthetic


def rows(n=30):
    return pd.DataFrame(
        {
            "P2": [[1, 4]] * n,
            "P3": [4] * n,
            "S2": [1] * n,
            "P1": [1] * n,
            "O1": [4] * n,
        }
    )


def qa(n=30):
    return {
        "analysis_rows": n,
        "raw_rows": n + 2,
        "excluded_rows": 2,
        "median_duration_seconds": 180,
        "exclusion_rate": 2 / (n + 2),
        "disposition_counts": {"analysis": n, "speeder": 2},
        "balanced": True,
    }


def test_multiselect_denominator_is_people_not_selections():
    sources = build_tables(rows(), qa(), synthetic=True)["sources"]
    assert sources.loc[sources.source_code == 1, "usage_rate"].item() == 1
    assert sources.loc[sources.source_code == 4, "most_useful_rate"].item() == 1
    assert sources["denominator"].unique().tolist() == [30]


@pytest.mark.parametrize("synthetic", [False, True])
def test_under_25_omits_all_subgroup_rows(synthetic):
    tables = build_tables(rows(24), qa(24), synthetic=synthetic)
    assert tables["campus_satisfaction"].empty
    assert tables["hours_satisfaction"].empty
    assert not tables["satisfaction"].empty


@pytest.mark.parametrize("synthetic", [False, True])
def test_sparse_subgroups_withhold_whole_table_without_leaking_counts(synthetic):
    data = rows()
    data.loc[0, "S2"] = 2
    data.loc[0, "P1"] = 2
    tables = build_tables(data, qa(), synthetic=synthetic)
    assert tables["campus_satisfaction"].empty
    assert tables["hours_satisfaction"].empty
    status = tables["chart_status"].set_index("chart")
    assert status.loc["campus_satisfaction", "status"] == "suppressed"
    assert status.loc["hours_satisfaction", "status"] == "suppressed"
    assert "at least one nonzero cell is below five" in status.loc[
        "campus_satisfaction", "reason"
    ]


def test_synthetic_data_withholds_sparse_cells_and_remains_labeled():
    data = rows()
    data.loc[0, "S2"] = 2
    tables = build_tables(data, qa(), synthetic=True)
    assert tables["campus_satisfaction"].empty
    for table in tables.values():
        assert "data_kind" in table.columns
    html = render_dashboard(tables, qa(), synthetic=True)
    assert "SYNTHETIC DEMO" in html
    assert "not participant findings" in html


@pytest.mark.parametrize("synthetic", [False, True])
def test_fewer_than_five_responses_withholds_all_chart_tables(synthetic):
    tables = build_tables(rows(4), qa(4), synthetic=synthetic)
    for chart in ("sources", "satisfaction", "campus_satisfaction", "hours_satisfaction"):
        assert tables[chart].empty
    assert tables["chart_status"]["status"].eq("suppressed").all()


@pytest.mark.parametrize("synthetic", [False, True])
def test_sparse_overall_satisfaction_withholds_whole_distribution(synthetic):
    data = rows()
    data.loc[0, "O1"] = 1
    tables = build_tables(data, qa(), synthetic=synthetic)
    assert tables["satisfaction"].empty
    assert not tables["sources"].empty


@pytest.mark.parametrize("synthetic", [False, True])
def test_zero_cells_do_not_withhold_otherwise_safe_charts(synthetic):
    tables = build_tables(rows(), qa(), synthetic=synthetic)
    assert tables["chart_status"]["status"].eq("available").all()
    assert tables["satisfaction"]["count"].tolist() == [0, 0, 0, 30, 0]
    assert tables["hours_satisfaction"]["n"].tolist() == [30, 0, 0, 0, 0]


def test_default_demo_exercises_available_and_withheld_charts_with_same_release_rules():
    result = clean_responses(make_synthetic())
    synthetic = build_tables(result.analysis, result.qa, synthetic=True)
    participant = build_tables(result.analysis, result.qa, synthetic=False)
    status = synthetic["chart_status"].set_index("chart")
    assert status["status"].to_dict() == {
        "sources": "available",
        "satisfaction": "available",
        "campus_satisfaction": "suppressed",
        "hours_satisfaction": "available",
    }
    assert synthetic["campus_satisfaction"].empty
    assert synthetic["hours_satisfaction"]["n"].ge(5).all()
    assert synthetic["hours_satisfaction"]["n"].sum() == 50
    for chart in status.index:
        pd.testing.assert_frame_equal(
            synthetic[chart].drop(columns="data_kind"),
            participant[chart].drop(columns="data_kind"),
        )
    pd.testing.assert_frame_equal(
        synthetic["chart_status"].drop(columns="data_kind"),
        participant["chart_status"].drop(columns="data_kind"),
    )


def test_empty_data_has_no_percentages_or_fake_conclusion():
    tables = build_tables(rows(0), qa(0), synthetic=False)
    assert tables["sources"].empty
    assert "No eligible analysis responses" in tables["summary"]["conclusion"].item()
    assert "nan" not in render_dashboard(tables, qa(0), synthetic=False).lower()


def test_generated_html_escapes_dynamic_text():
    tables = build_tables(rows(), qa(), synthetic=True)
    tables["summary"].loc[0, "conclusion"] = "<script>alert(1)</script>"
    html = render_dashboard(tables, qa(), synthetic=True)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_hours_chart_reports_prespecified_median_not_mean():
    data = rows()
    data["O1"] = [5] * 20 + [1] * 10
    hours = build_tables(data, qa(), synthetic=True)["hours_satisfaction"]
    assert hours.loc[hours.hours_code == 1, "median_satisfaction"].item() == 5
