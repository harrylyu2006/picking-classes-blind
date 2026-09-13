"""Visible release decisions and provenance in the public dashboard."""

import pandas as pd
import pytest

from picking_classes_blind.rendering import render_dashboard
from picking_classes_blind.reporting import build_tables


@pytest.fixture
def report():
    # Overall outcomes and hours qualify, but a one-person campus must be withheld.
    n = 30
    data = pd.DataFrame(
        {
            "P2": [[1, 4]] * n,
            "P3": [4] * n,
            "S2": [1] * (n - 1) + [2],
            "P1": [1] * n,
            "O1": [4] * n,
        }
    )
    qa = {
        "analysis_rows": n,
        "raw_rows": n,
        "excluded_rows": 0,
        "median_duration_seconds": 180,
        "exclusion_rate": 0,
    }
    return data, qa


def test_public_footer_links_to_repository(report):
    data, qa = report
    html = render_dashboard(build_tables(data, qa), qa, synthetic=False)
    footer = html.split("<footer>", 1)[1].split("</footer>", 1)[0]
    assert (
        '<a href="https://github.com/harrylyu2006/picking-classes-blind">'
        "View source on GitHub"
    ) in footer


@pytest.mark.parametrize("synthetic", [False, True])
def test_uniform_random_caption_only_describes_synthetic_sources(report, synthetic):
    data, qa = report
    html = render_dashboard(build_tables(data, qa, synthetic=synthetic), qa, synthetic=synthetic)
    source_panel = html.split('<section class="panel sources">', 1)[1].split("</section>", 1)[0]
    assert ("Source choices are uniformly sampled at random" in source_panel) is synthetic
    assert ("not participant findings" in source_panel) is synthetic


def test_withheld_campus_stays_visible_without_fallback_counts(report):
    data, qa = report
    tables = build_tables(data, qa)
    assert tables["campus_satisfaction"].empty
    assert not tables["satisfaction"].empty
    assert not tables["hours_satisfaction"].empty
    # The renderer displays the release boundary's escaped reason verbatim.
    tables["chart_status"].loc[
        tables["chart_status"].chart == "campus_satisfaction", "reason"
    ] = "Withheld: at least one nonzero cell is below five."
    html = render_dashboard(tables, qa, synthetic=False)
    campus_panel = html.split("02 / The final schedule", 1)[1].split("</section>", 1)[0]
    assert "Schedule satisfaction by home campus" in campus_panel
    assert "Withheld: at least one nonzero cell is below five." in campus_panel
    assert "View exact counts" not in campus_panel
    assert "All respondents" not in campus_panel
    assert '<span class="segment"' not in campus_panel
    assert '<div class="hours-row">' in html


def test_withholding_notice_escapes_release_reason(report):
    data, qa = report
    tables = build_tables(data, qa)
    tables["chart_status"].loc[
        tables["chart_status"].chart == "campus_satisfaction", "reason"
    ] = "Withheld: <script>unsafe</script>"
    html = render_dashboard(tables, qa, synthetic=False)
    assert "<script>" not in html
    assert "Withheld: &lt;script&gt;unsafe&lt;/script&gt;" in html
