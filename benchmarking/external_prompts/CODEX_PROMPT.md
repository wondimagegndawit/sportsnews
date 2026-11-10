# Codex prompt: fill the remaining gaps in the Power 4 athletic department benchmarking workbook

Paste everything below this line into Codex, run from the repository root (branch `claude/sleepy-hamilton-613gvu`).

---

You are working in the `benchmarking/` folder of this repository. It contains a finished, formula-driven Excel workbook (`Power4_Athletic_Department_Benchmarking.xlsx`) benchmarking the 67 Power 4 athletic departments, the raw data under `data/`, research CSVs under `data/research/`, and build scripts under `scripts/`. Do not change the workbook structure, the scripts, or any existing CSV. Your job is research: find publicly sourced values for the cells that are still "--", write them to ONE new CSV, then rebuild.

Read first: `data/research/BRIEF.md` (metric keys, CSV schema, source rules) and `data/gaps_remaining.csv` (1430 open cells: school, conference, public/private, state, metric, and what is already known for context).

RULES (non-negotiable)
1. Do NOT use USA Today / sportsdata.usatoday.com for anything (no NCAA finances database, no coach salary databases), and do not cite Wikipedia or wiki mirrors or fan sites (e.g. Stadium Journey) for any number.
2. Every value must come with the specific URL of the page or PDF where you read it (not a homepage, not a search page). No URL, no value.
3. Values must be clean: bare numbers for numeric fields (no $ , % or words), whole dollars, no rounding of a reported figure. Put qualifiers ("up to", "approximately", "more than") in the notes column and record the base figure. Do not compute a figure that was not reported (no annual = total / term, no escalator math, no averages presented as a year figure, no inferred contract end years). If a figure is not public, say "not public" and move on.
4. Source preference: (a) the school's own posting (athletics site, controller/audit office, board of trustees or regents agenda, state auditor or transparency portal); (b) the partner's press release; (c) Sports Business Journal, Front Office Sports, or the board-approved contract; (d) local beat reporting that quotes contract terms. Say which tier each value came from.
5. Financials: only the NCAA Membership Financial Reporting System (MFRS) report or the NCAA agreed-upon-procedures (AUP) report that includes the Statement of Revenues and Expenses, most recent fiscal year (FY2025 = year ended June 30, 2025 preferred; FY2024 acceptable). Use the ALL SPORTS total column. Do not substitute GAAP audited statements, EADA filings, budgets, or Knight-Newhouse/Sportico compilations.
6. Coaching pay: the guaranteed annual compensation for the current season (2026 football, 2026-27 men's basketball) under the current contract, from the executed contract/term sheet, the school's announcement, or a state salary database. Record the contract end year. Verify the coach is in place as of November 2026.
7. Deal fields: start year = first contract year; term = years; annual and total = only what was reported; deal type for venue names = commercial / honorific (donor or memorial name, no fee) / none.

OUTPUT: write `data/research/external_codex.csv` with exactly this header and one row per cell you can source (append as you go so partial work survives):
school,metric,value,unit,fiscal_year_or_season,source_name,source_url,date_accessed,notes
Use the exact school names and metric keys from `data/gaps_remaining.csv`. date_accessed = the date you read the page. For MFRS reports also write a `fin_report_url` row (value = the PDF URL) and a `fin_fiscal_year` row (value = 2025 or 2024).

PRIORITY ORDER (the workbook owner is an investor in media rights and athletic revenue):
1. Multimedia rights deal terms (mmr_start_year, mmr_term_years, mmr_annual_value, mmr_total_value) and apparel deal terms, for every school listed.
2. Stadium and arena naming-rights terms and jersey patch terms where a commercial partner is already known.
3. MFRS/AUP financial reports for the 32 public schools still on the EADA fallback. Concrete leads: Cincinnati FY2025 AUP on ohioauditor.gov (AuditSearch); Oklahoma State AUP archive on adminfinance.okstate.edu; Kansas State athletics "Forms, Documents and Reports" page; Rutgers FY2025 KPMG AUP via the Board of Governors; Iowa and Iowa State via iowaregents.edu (full AUP, not the summary); Texas, Texas A&M and Texas Tech via system board audit materials; Florida, Florida State and UCF via trustees audit committees; Arizona and Arizona State via azregents.edu; Mississippi State and Ole Miss via the IHL board book; Missouri via umsystem.edu; Michigan and Michigan State via regents/trustees; Indiana and Purdue via trustees; Nebraska via nebraska.edu; Maryland via usmd.edu; UCLA and California via UC regents; Alabama and Auburn via trustees; Oklahoma via OU regents; Clemson, Georgia Tech, Louisville, NC State, Florida State, Pittsburgh via internal audit or controller pages.
4. Remaining venue cells (capacity, year opened, last major renovation) from the official athletics facility page or media guide, varsity sports counts from the official "about" page, and the remaining coaching cells.

WHEN FINISHED, run from `benchmarking/`:
python3 -I scripts/merge_research.py
python3 -I scripts/build_workbook.py
(then recalculate the workbook headlessly with LibreOffice, e.g. soffice --headless --convert-to xlsx --outdir /tmp/recalc Power4_Athletic_Department_Benchmarking.xlsx, and copy it back)
python3 -I scripts/qa.py
Report: rows written, rows rejected by merge_research.py (it prints them), the QA output, and the cells you could not source with the reason.
