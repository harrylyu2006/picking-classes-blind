import pandas as pd

from picking_classes_blind.rendering import render_dashboard
from picking_classes_blind.reporting import build_tables


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


def test_under_25_omits_all_subgroup_rows():
    tables = build_tables(rows(24), qa(24), synthetic=False)
    assert tables["campus_satisfaction"].empty
    assert tables["hours_satisfaction"].empty
    assert not tables["satisfaction"].empty


def test_sparse_subgroups_withhold_whole_table_without_leaking_counts():
    data = rows()
    data.loc[0, "S2"] = 2
    data.loc[0, "P1"] = 2
    tables = build_tables(data, qa(), synthetic=False)
    assert tables["campus_satisfaction"].empty
    assert tables["hours_satisfaction"].empty
    assert "suppressed" in tables["chart_status"]["status"].tolist()


def test_synthetic_data_can_show_sparse_cells_but_remains_labeled():
    data = rows()
    data.loc[0, "S2"] = 2
    tables = build_tables(data, qa(), synthetic=True)
    assert not tables["campus_satisfaction"].empty
    for table in tables.values():
        assert "data_kind" in table.columns
    html = render_dashboard(tables, qa(), synthetic=True)
    assert "SYNTHETIC DEMO" in html
    assert "not participant findings" in html


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
