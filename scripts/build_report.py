#!/usr/bin/env python3
"""Turn a week's TrustMRR snapshot into the ranked report + Excel file.

Input:  data/snapshots/YYYY-MM-DD.json  — list of objects written by the weekly
        Claude run, one per startup, with keys:
          slug, name, url, sells, category, revenue_30d, prev_revenue_30d,
          growth_pct, mrr, founded, acquisition_channels (list[str]),
          channel_evidence (list of {claim, source_url}), fit_score (0-10),
          fit_reason
        Every number must come from the TrustMRR page; null if not shown.
Output: reports/YYYY-MM-DD.xlsx and reports/YYYY-MM-DD.md, and updates data/seen.json.
Usage:  python3 scripts/build_report.py data/snapshots/2026-11-02.json
"""
import json, sys, pathlib, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

ROOT = pathlib.Path(__file__).resolve().parent.parent
LO, HI = 1000, 20000  # keep in sync with profile.yaml revenue_window_usd

def load(p): return json.loads((ROOT / p).read_text())

def main(snap_path):
    snap = pathlib.Path(snap_path)
    day = snap.stem
    rows = json.loads(snap.read_text())
    block = set(load("data/blocklist.json")["slugs"])
    seen_doc = load("data/seen.json"); seen = seen_doc["seen"]

    keep = []
    for r in rows:
        if r["slug"] in block: continue
        rev = r.get("revenue_30d")
        if rev is None or not (LO <= rev <= HI): continue
        r["is_new"] = r["slug"] not in seen
        keep.append(r)
    # New winners first, then by fit, then by growth.
    keep.sort(key=lambda r: (not r["is_new"], -(r.get("fit_score") or 0),
                             -(r.get("growth_pct") or 0)))

    wb = Workbook(); ws = wb.active; ws.title = "Winners"
    cols = ["new", "name", "sells", "category", "revenue_30d", "growth_pct", "mrr",
            "fit_score", "fit_reason", "acquisition_channels", "url"]
    ws.append(cols)
    for c in ws[1]: c.font = Font(bold=True)
    hl = PatternFill("solid", fgColor="FFF2CC")
    for r in keep:
        ws.append(["NEW" if r["is_new"] else "", r["name"], r.get("sells"), r.get("category"),
                   r.get("revenue_30d"), r.get("growth_pct"), r.get("mrr"), r.get("fit_score"),
                   r.get("fit_reason"), ", ".join(r.get("acquisition_channels") or []) or "unknown",
                   r.get("url")])
        if r["is_new"]:
            for c in ws[ws.max_row]: c.fill = hl
    ws2 = wb.create_sheet("All checked")
    ws2.append(["slug", "name", "revenue_30d", "growth_pct", "blocked"])
    for r in rows:
        ws2.append([r["slug"], r["name"], r.get("revenue_30d"), r.get("growth_pct"), r["slug"] in block])
    out_dir = ROOT / "reports"; out_dir.mkdir(exist_ok=True)
    wb.save(out_dir / f"{day}.xlsx")

    md = [f"# TrustMRR winners — {day}", "",
          f"Checked {len(rows)} startups; {len(keep)} in the ${LO:,}–${HI:,}/30d band "
          f"({sum(r['is_new'] for r in keep)} new).", "",
          "| | Name | Sells | 30d revenue | Growth | Fit | Channels |", "|---|---|---|---|---|---|---|"]
    for r in keep:
        md.append(f"| {'🆕' if r['is_new'] else ''} | [{r['name']}]({r.get('url')}) | {r.get('sells')} | "
                  f"${r['revenue_30d']:,.0f} | {r.get('growth_pct')}% | {r.get('fit_score')} | "
                  f"{', '.join(r.get('acquisition_channels') or []) or 'unknown'} |")
    (out_dir / f"{day}.md").write_text("\n".join(md) + "\n")

    for r in keep:
        seen.setdefault(r["slug"], day)
    (ROOT / "data/seen.json").write_text(json.dumps(seen_doc, indent=2) + "\n")
    print(f"wrote reports/{day}.xlsx and reports/{day}.md — {len(keep)} winners")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__))
