# Power 4 athletic department benchmarking

`Power4_Athletic_Department_Benchmarking.xlsx` benchmarks 68 athletic departments: the 67 Power 4 schools and Notre Dame (a football independent, on its own `Independent` tab). 53 have public NCAA MFRS financial data; the other 15 (the private universities and Pittsburgh) carry the federal EADA 2024-25 figures instead, flagged in the Financial source basis and Financial data type columns. It was built from scratch with openpyxl (`scripts/`) and recalculated with LibreOffice; every hardcoded value on the conference tabs is hyperlinked to its source and logged on `Source Log`.

## Folders

- `data/` raw bulk downloads, saved unmodified: IPEDS HD2024 and EF2024A, EADA 2024-25, NCAA APR/GSR search responses and report PDFs, ESPN standings JSON, Sports-Reference men's basketball pages, NACDA Directors' Cup final standings PDFs. Also the derived `bulk_values.csv`, `merged_values.csv`, `review_rejections.csv` and `coverage.json`.
- `data/research/` the per-conference research CSVs returned by the research subagents, plus the brief they worked from.
- `scripts/` `schools.py` (master list and identifiers), `build_bulk.py`, `fetch_ncaa_academics.py`, `merge_research.py`, `build_workbook.py`.

## Rebuild

Run from this folder:

```bash
python3 -I scripts/build_bulk.py
python3 -I scripts/build_sportico.py
python3 -I scripts/build_attendance.py
python3 -I scripts/merge_research.py
python3 -I scripts/build_workbook.py
soffice --headless --calc --convert-to xlsx:"Calc MS Excel 2007 XML" --outdir /tmp/recalc Power4_Athletic_Department_Benchmarking.xlsx
cp /tmp/recalc/Power4_Athletic_Department_Benchmarking.xlsx .
python3 -I scripts/qa.py
```

`merge_research.py` reads every CSV in `data/research/` and stops if it finds none. `qa.py` recomputes every average and median from the school rows and compares them with the recalculated workbook.

## Averages, medians and counts

Financial line items are summarized across a grid of fiscal year (each year, then all years) by data source (MFRS, EADA, then all sources); combinations with no schools are left out. Rows marked MFRS or EADA never mix the two; rows marked all sources do. An overall row covers every school, and every non-financial column is summarized overall only. Count rows give the number of schools with a value in each column. The summary rows sit under the schools on each conference tab (for that conference) and on `All Schools` (for all schools only; it carries no per-conference rows). The scoped medians are array formulas. Below the summary rows, a Data breakdown table counts schools by data type and fiscal year, and by financial source basis.

There are no per-school tabs; `School Lookup` covers every school.

## Attendance

`scripts/build_attendance.py` writes every per-school attendance figure in the two sources to `data/attendance_values.csv`; the workbook shows them in the Attendance section.

- Football: `data/d1ticker/` holds the D1.ticker FBS Attendance Trends pages for 2023, 2024 and 2025, saved unmodified. Average home attendance for each season is the Final Average column of that season's own page. The 2025 page also supplies the year-over-year change, the 5-year average (the page does not say which five seasons), the change against the 5-year average and the percent of capacity. The pages carry averages only: no totals and no game counts.
- Men's basketball: `data/ncaa_attendance/Attend.pdf` is the NCAA Men's Basketball Attendance Records book (through 2025-26), saved unmodified, with `Attend_layout.txt` as its `pdftotext -layout` extract. The Division I team-by-team table gives home games, total home attendance and average home attendance for 2025-26 for every school; the script checks that the table ties to the PDF's Division I home totals. Three leader tables list only 30 teams each (all-games attendance, and largest increase with the 2024-25 average); those columns are marked top 30, show "--" for other schools and carry no average or median.

## Head coach pay

Each sport has one pay column: total guaranteed annual pay for the current season, meaning base salary plus supplemental compensation (the guaranteed amounts contracts label as talent, rights, media or outside-income fees). Where a source states the two parts but no total, they are added; where it gives only a contract total and length or an average, the average is shown. Retention payments, signing bonuses and performance bonuses are excluded and described in the Source Log note where known. The re-read totals, with the parts quoted, are in `data/research/verification_zzz_coach_pay.csv` (metrics `fb_hc_annual_comp`, `mbb_hc_annual_comp`). Figures that would need a stated escalator applied are left blank. A three-column layout (base, supplemental, total) was tried and dropped on 13 November 2026 because most sources state only a total.

## Source exceptions

USA Today's databases are not used, with one exception made at the analyst's direction on 13 November 2026: Kentucky men's basketball head coach pay (5,250,000, the database's 2025-26 figure). `data/source_exceptions.csv` lists the exception; `merge_research.py` lets only those rows past the source screen and `qa.py` reports them separately from any other hit.

## Verification

A second, independent review of the double-check list (run in another AI tool on 13 November 2026) proposed seven value changes. Each was applied only after the page was read here: six are in `data/research/verification_zzzz_second_review.csv`; the seventh (Kentucky men's basketball pay) stays blank because the cited page could not be opened. Rows in files named `verification_zzz*` are entered after the re-read pass and are never blanked by `data/research_withdrawals.csv`.

Every researched value is checked against its cited source, and the result is shown in the Source Log's Verification column.

1. `scripts/verify_sources.py <cache_dir>` fetches each cited page once (cache kept outside the repo) and looks for the value in the page text. Output: `data/verification/auto_check.csv`.
2. Values that are not found, sit on pages that block automated fetching, or carry a soft research note go to a re-read: a researcher opens the page (or a substitute high-quality source) and records a verdict with a verbatim quote. The verdict files live in `data/verification/` (`reread_*.csv`, `coach_fb.csv`, `coach_mbb.csv`, `currency_*.csv`), with analyst overrides in `decisions.csv` and hand checks in `manual_checks.csv`.
3. `scripts/apply_verification.py` turns the verdicts into `data/research/verification_r6.csv` (corrections and confirmed values with their quotes), `data/research/verification_z_currency.csv` (refreshed stale items, new deals and stated end years) and `data/research_withdrawals.csv` (figures no source states, which `merge_research.py` blanks with the reason kept in the Source Log).
4. `scripts/build_verification.py` writes `data/verification.csv`, which `build_workbook.py` reads for the Verification column.
5. `scripts/build_checklist.py` writes `P4_Benchmarking_Double_Check_List.xlsx`: the cells still worth a manual look, the outcome for each figure first read from a search excerpt, and every changed cell.

Rules applied in the re-read: a figure is kept only if a page states it (no sums of components, no averages presented as a year, no end year derived from a term, nothing attributed to a newspaper-compiled salary database); a start year may be the announcement year where the source gives no effective date, and is noted as such; the expires column takes a stated end year where one exists; coach contract end is the stated expiry year; where two reported figures describe different periods nothing is derived (`data/no_derive.csv`). `qa.py` lists any deal whose recorded term ended before 2026.

## Percent of capacity

Both sports use the same year. Football 2025 is the Capacity % column of the D1.ticker 2025 page, as reported; D1.ticker does not publish the capacity it divides by, so the figure can differ from attendance divided by the workbook's Stadium capacity column. Men's basketball 2025-26 is a workbook formula, average home attendance divided by Arena capacity, because the NCAA book reports no percentage.
