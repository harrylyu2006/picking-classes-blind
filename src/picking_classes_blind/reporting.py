"""Produce aggregate-only tables with explicit denominators and release rules."""

import pandas as pd

from .schema import CAMPUS_LABELS, HOURS_LABELS, SOURCE_LABELS

MIN_SUBGROUP_N = 25
MIN_CELL_N = 5


def _sparse(values: pd.Series) -> bool:
    return bool(((values > 0) & (values < MIN_CELL_N)).any())


def build_tables(
    analysis: pd.DataFrame, qa: dict, *, synthetic: bool = False
) -> dict[str, pd.DataFrame]:
    """No individual responses, response identifiers or free text leave this boundary."""
    n = len(analysis)
    if n != qa["analysis_rows"]:
        raise ValueError("Analysis row count does not match QA report.")
    kind = "synthetic" if synthetic else "participant"
    status = []
    tables = {}
    source_rows = []
    if n >= MIN_CELL_N or (synthetic and n > 0):
        for code, label in SOURCE_LABELS.items():
            used = sum(code in choices for choices in analysis["P2"])
            useful = int((analysis["P3"] == code).sum())
            source_rows.append([code, label, used, useful, n, used / n, useful / n])
    tables["sources"] = pd.DataFrame(
        source_rows,
        columns=[
            "source_code",
            "source",
            "used_count",
            "most_useful_count",
            "denominator",
            "usage_rate",
            "most_useful_rate",
        ],
    )
    status.append(
        [
            "sources",
            "available" if source_rows else "suppressed",
            "" if source_rows else "Fewer than five analysis responses.",
        ]
    )

    satisfaction = pd.DataFrame(columns=["satisfaction", "count", "denominator", "share"])
    if n:
        counts = analysis["O1"].value_counts().reindex(range(1, 6), fill_value=0)
        if synthetic or (n >= MIN_CELL_N and not _sparse(counts)):
            satisfaction = pd.DataFrame(
                {
                    "satisfaction": counts.index,
                    "count": counts.values,
                    "denominator": n,
                    "share": counts.values / n,
                }
            )
    tables["satisfaction"] = satisfaction
    status.append(
        [
            "satisfaction",
            "available" if len(satisfaction) else "suppressed",
            "" if len(satisfaction) else "Insufficient data or small outcome cells.",
        ]
    )

    campus = pd.DataFrame(
        columns=[
            "campus",
            "satisfaction",
            "count",
            "campus_n",
            "share",
        ]
    )
    hours = pd.DataFrame(columns=["hours_code", "hours", "n", "median_satisfaction"])
    campus_reason = hours_reason = f"Subgroup charts require at least {MIN_SUBGROUP_N} responses."
    if n >= MIN_SUBGROUP_N:
        campus_rows = []
        for code, group in analysis.groupby("S2", sort=True):
            counts = group["O1"].value_counts().reindex(range(1, 6), fill_value=0)
            for score, count in counts.items():
                campus_rows.append(
                    [CAMPUS_LABELS[int(code)], score, count, len(group), count / len(group)]
                )
        candidate = pd.DataFrame(campus_rows, columns=campus.columns)
        if synthetic or not _sparse(candidate["count"]):
            campus = candidate
            campus_reason = ""
        else:
            campus_reason = "Whole campus chart withheld: at least one nonzero cell is below five."
        hours_rows = []
        for code, label in HOURS_LABELS.items():
            group = analysis[analysis["P1"] == code]
            hours_rows.append(
                [code, label, len(group), float(group["O1"].median()) if len(group) else None]
            )
        candidate_hours = pd.DataFrame(hours_rows, columns=hours.columns)
        if synthetic or not _sparse(candidate_hours["n"]):
            hours = candidate_hours
            hours_reason = ""
        else:
            hours_reason = "Whole hours chart withheld: at least one nonempty group is below five."
    tables["campus_satisfaction"] = campus
    tables["hours_satisfaction"] = hours
    status.extend(
        [
            ["campus_satisfaction", "available" if len(campus) else "suppressed", campus_reason],
            ["hours_satisfaction", "available" if len(hours) else "suppressed", hours_reason],
        ]
    )
    limitations = (
        "Convenience sample; self-reported, cross-sectional answers. "
        "These data cannot establish causation, represent all NYU students, "
        "or measure retention. Recommendation intention is not retention. "
        "Research-hours categories are ordered groups, not exact hours."
    )
    if synthetic:
        conclusion = (
            f"Synthetic demonstration with n = {n} analysis rows; "
            "not participant findings. No students have been surveyed in this demo."
        )
    elif not n:
        conclusion = "No eligible analysis responses. No substantive findings can be reported."
    elif n < MIN_CELL_N:
        conclusion = (
            f"n = {n}. Outcome tables withheld because fewer than five responses qualified."
        )
    else:
        conclusion = (
            f"n = {n} eligible responses after fixed QA rules. "
            "Source usage and perceived usefulness are descriptive counts; "
            "neither measures a source's causal effect on satisfaction."
        )
    tables["summary"] = pd.DataFrame(
        [
            {
                "analysis_n": n,
                "raw_n": qa["raw_rows"],
                "excluded_n": qa["excluded_rows"],
                "exclusion_rate": qa["exclusion_rate"],
                "median_duration_seconds": qa.get("median_duration_seconds"),
                "subgroup_min_n": MIN_SUBGROUP_N,
                "cell_min_n": MIN_CELL_N,
                "conclusion": conclusion,
                "limitations": limitations,
            }
        ]
    )
    tables["chart_status"] = pd.DataFrame(status, columns=["chart", "status", "reason"])
    for table in tables.values():
        table["data_kind"] = kind
    return tables
