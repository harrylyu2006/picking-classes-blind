"""An offline, accessible dashboard preview of the exported aggregate tables."""

from html import escape

import pandas as pd

CSS = """
:root{--paper:#f5f2e9;--ink:#202d27;--muted:#5b665e;--green:#267257;--orange:#b74f2c}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 'Helvetica Neue',sans-serif}
main{max-width:1220px;margin:0 auto;padding:36px 48px 30px}.eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:700}
header{display:flex;align-items:flex-end;justify-content:space-between;gap:30px;padding-bottom:23px;border-bottom:2px solid var(--ink)}
h1{font:normal clamp(38px,5vw,62px)/1.05 Georgia,serif;letter-spacing:-.04em;margin:12px 0 14px}p{margin:6px 0;color:var(--muted)}
.tag{display:inline-block;background:#efd4bb;color:#773316;padding:7px 12px;font-size:11px;font-weight:700;letter-spacing:.08em}
.intro{max-width:660px}.edition{text-align:right;white-space:nowrap;font-size:12px;color:var(--muted)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid #b4bbaf;margin-bottom:26px;padding:23px 0}
.stat{padding:0 20px;border-left:1px solid #b4bbaf}.stat:first-child{padding-left:0;border:0}.number{font:38px/1.2 Georgia,serif}.caption{font-size:12px;color:var(--muted)}
.layout{display:grid;grid-template-columns:1.2fr 1fr;gap:34px}.panel{padding:0 0 24px;border-bottom:1px solid #b4bbaf}.sources{grid-row:span 2}
h2{font:24px/1.2 Georgia,serif;margin:8px 0}.sub{font-size:12px;line-height:1.5;margin-bottom:18px}.key{display:flex;gap:20px;font-size:11px;margin-bottom:17px}.key span:before{content:'';display:inline-block;width:9px;height:9px;margin-right:6px;background:var(--green)}.key span:last-child:before{background:var(--orange)}
.source{margin-bottom:15px}.source-name{font-size:12px;font-weight:600;margin-bottom:3px}.bar-row{display:flex;align-items:center;gap:8px;height:17px}.track{height:7px;background:#e2e4d9;flex:1}.fill{height:100%;background:var(--green)}.useful{background:var(--orange)}.value{font:11px/1.2 'Helvetica Neue',sans-serif;width:72px;text-align:right;white-space:nowrap}
.campus{margin:14px 0}.campus-label{font-size:12px;margin-bottom:5px}.stack{height:19px;display:flex;background:#e0e3d8}.segment{height:100%;display:block}.scale{display:flex;justify-content:space-between;font-size:10px;margin-top:7px;color:var(--muted)}
.hours-row{display:grid;grid-template-columns:84px 1fr 68px;align-items:center;gap:10px;font-size:11px;margin:13px 0}.hours-row .track{height:9px}.note{background:#e5e8da;padding:24px 28px;margin-top:26px;border-left:3px solid var(--green)}.note h2{font-size:25px}.note p{max-width:980px;font-size:13px}.muted-box{padding:20px;background:#e9e9de;font-size:13px}
footer{display:flex;justify-content:space-between;gap:20px;margin-top:22px;font-size:11px;color:var(--muted)}a{color:var(--green);text-underline-offset:3px}a:focus-visible{outline:2px solid var(--orange);outline-offset:4px}.links{display:flex;gap:18px;flex-wrap:wrap}
details{font-size:12px;margin-top:15px}summary{cursor:pointer}table{width:100%;border-collapse:collapse;margin-top:8px}th,td{text-align:left;border-bottom:1px solid #cbd0c3;padding:6px}
@media(max-width:760px){main{padding:24px 20px}.layout{grid-template-columns:1fr;gap:24px}.sources{grid-row:auto}header{display:block}.edition{text-align:left;margin-top:14px}.stats{grid-template-columns:1fr 1fr;gap:18px}.stat:nth-child(3){border:0;padding-left:0}.number{font-size:32px}footer{display:block}.links{margin-top:12px}}
@media print{main{padding:15px;max-width:none}body{font-size:12px}.tag{-webkit-print-color-adjust:exact}details,footer .links{display:none}.note{break-inside:avoid}.panel{break-inside:avoid}h1{font-size:40px}}
"""


def _e(value: object) -> str:
    return escape(str(value), quote=True)


def _reason(tables: dict, chart: str) -> str:
    statuses = tables["chart_status"]
    return _e(statuses.loc[statuses.chart == chart, "reason"].item())


def _source_chart(table: pd.DataFrame) -> str:
    result = []
    for row in table.itertuples():
        result.append(f'<div class="source"><div class="source-name">{_e(row.source)}</div>')
        for rate, count, label, style in [
            (row.usage_rate, row.used_count, "Used", ""),
            (row.most_useful_rate, row.most_useful_count, "Most useful", "useful"),
        ]:
            result.append(
                f'<div class="bar-row" aria-label="{label}: {count} of {row.denominator}">'
                f'<div class="track"><div class="fill {style}" style="width:{rate * 100:.2f}%">'
                f'</div></div><span class="value">{rate:.0%} · {count}/{row.denominator}</span></div>'
            )
        result.append("</div>")
    return "".join(result)


def _distribution(table: pd.DataFrame, by_campus: bool) -> str:
    colors = ["#b65b42", "#c99069", "#c8cbb2", "#81a58a", "#267257"]
    groups = table.groupby("campus", sort=False) if by_campus else [("All respondents", table)]
    result = []
    for campus, group in groups:
        n = int(group.iloc[0]["campus_n" if by_campus else "denominator"])
        result.append(
            f'<div class="campus"><div class="campus-label">{_e(campus)} · n = {n}</div><div class="stack">'
        )
        for row in group.itertuples():
            label = f"{int(row.satisfaction)}/5: {int(row.count)} of {n}"
            result.append(
                f'<span class="segment" role="img" aria-label="{label}" title="{label}" '
                f'style="width:{row.share * 100:.4f}%;background:{colors[int(row.satisfaction) - 1]}"></span>'
            )
        result.append("</div></div>")
    result.append(
        '<div class="scale"><span>1 · Very dissatisfied</span><span>5 · Very satisfied</span></div>'
    )
    result.append("<details><summary>View exact counts</summary>")
    result.append(table.drop(columns=["data_kind"]).to_html(index=False, border=0, escape=True))
    result.append("</details>")
    return "".join(result)


def render_dashboard(tables: dict[str, pd.DataFrame], qa: dict, *, synthetic: bool) -> str:
    summary = tables["summary"].iloc[0]
    badge = "SYNTHETIC DEMO" if synthetic else "DESCRIPTIVE PERSONAL PROJECT"
    sources = (
        _source_chart(tables["sources"])
        if len(tables["sources"])
        else (f'<div class="muted-box">{_reason(tables, "sources")}</div>')
    )
    campus = tables["campus_satisfaction"]
    overall = tables["satisfaction"]
    if len(campus):
        satisfaction = _distribution(campus, True)
        satisfaction_sub = "Schedule satisfaction by home campus. Each row sums to 100%."
    elif len(overall):
        satisfaction = _distribution(overall, False)
        satisfaction_sub = "Overall distribution. " + _reason(tables, "campus_satisfaction")
    else:
        satisfaction = f'<div class="muted-box">{_reason(tables, "satisfaction")}</div>'
        satisfaction_sub = "Schedule satisfaction · 1–5 scale"
    hours = []
    for row in tables["hours_satisfaction"].itertuples():
        score = f"{row.median_satisfaction:.2f}" if row.n else "—"
        width = row.median_satisfaction * 20 if row.n else 0
        hours.append(
            f'<div class="hours-row"><span>{_e(row.hours)}</span><div class="track">'
            f'<div class="fill" style="width:{width:.2f}%"></div></div>'
            f"<span>{score} · n={row.n}</span></div>"
        )
    hours_chart = (
        "".join(hours) or f'<div class="muted-box">{_reason(tables, "hours_satisfaction")}</div>'
    )
    median = qa.get("median_duration_seconds")
    duration = f"{float(median):.0f}s" if median is not None and pd.notna(median) else "—"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Picking Classes Blind — {badge}</title><style>{CSS}</style></head><body><main>
<header><div class="intro"><div class="eyebrow">Student experience / Fall 2026</div>
<h1>Picking Classes Blind</h1><p>Which information sources help students navigate an unfamiliar campus?</p></div>
<div class="edition"><span class="tag">{badge}</span><p>Qualtrics → pandas → dashboard</p><p>Local preview · 01</p></div></header>
<section class="stats" aria-label="Data quality">
<div class="stat"><div class="number">{qa["analysis_rows"]}</div><div class="caption">Analysis responses</div></div>
<div class="stat"><div class="number">{duration}</div><div class="caption">Median duration · analysis rows</div></div>
<div class="stat"><div class="number">{qa["excluded_rows"]} <small>/ {qa["raw_rows"]}</small></div><div class="caption">Excluded from analysis</div></div>
<div class="stat"><div class="number">{qa["exclusion_rate"]:.1%}</div><div class="caption">Excluded / raw · rows reconcile</div></div></section>
<div class="layout"><section class="panel sources"><div class="eyebrow">01 / Information sources</div>
<h2>Used often. Useful most?</h2><p class="sub">Share of analysis respondents. Multiple sources may be used; only one can be most useful.</p>
<div class="key"><span>Used</span><span>Most useful</span></div>{sources}</section>
<section class="panel"><div class="eyebrow">02 / The final schedule</div><h2>How did it feel?</h2>
<p class="sub">{satisfaction_sub}</p>{satisfaction}</section>
<section class="panel"><div class="eyebrow">03 / Time spent choosing</div><h2>More time, better fit?</h2>
<p class="sub">Median satisfaction / 5, with each group's n. Descriptive association only.</p>{hours_chart}</section></div>
<section class="note"><div class="eyebrow">04 / What these numbers can say</div><h2>Keep the conclusion proportional.</h2>
<p>{_e(summary.conclusion)}</p><p>{_e(summary.limitations)}</p></section>
<footer><span>Fixed QA rules · aggregate tables only · no individual responses</span><nav class="links" aria-label="Download tables">
<a href="sources.csv">Source data ↗</a><a href="summary.csv">Summary ↗</a><a href="chart_status.csv">Chart availability ↗</a></nav></footer>
</main></body></html>"""
