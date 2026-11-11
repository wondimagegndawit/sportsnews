# Power 4 athletic department benchmarking

`Power4_Athletic_Department_Benchmarking.xlsx` benchmarks the 53 Power 4 athletic departments with public NCAA MFRS financial data (the 13 private universities and Pittsburgh are excluded). It was built from scratch with openpyxl (`scripts/`) and recalculated with LibreOffice; every hardcoded value on the conference tabs is hyperlinked to its source and logged on `Source Log`.

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

## Averages and medians

Financial line items (the MFRS columns) are summarized for each fiscal year present in the data and for all years; every other column is summarized across all years only. The summary rows sit under the schools on each conference tab and, by conference and for all schools, on `All Schools`. The fiscal-year medians are array formulas. Count rows give the number of schools with a value in each column for the same scopes. Below the summary rows, a Data breakdown table counts schools by fiscal year reported and by financial source basis (per conference on `All Schools`); EADA is zero by design because EADA-only schools are excluded.

## Attendance

`scripts/build_attendance.py` writes every per-school attendance figure in the two sources to `data/attendance_values.csv`; the workbook shows them in the Attendance section.

- Football: `data/d1ticker/` holds the D1.ticker FBS Attendance Trends pages for 2023, 2024 and 2025, saved unmodified. Average home attendance for each season is the Final Average column of that season's own page. The 2025 page also supplies the year-over-year change, the 5-year average (the page does not say which five seasons), the change against the 5-year average and the percent of capacity. The pages carry averages only: no totals and no game counts.
- Men's basketball: `data/ncaa_attendance/Attend.pdf` is the NCAA Men's Basketball Attendance Records book (through 2025-26), saved unmodified, with `Attend_layout.txt` as its `pdftotext -layout` extract. The Division I team-by-team table gives home games, total home attendance and average home attendance for 2025-26 for every school; the script checks that the table ties to the PDF's Division I home totals. Three leader tables list only 30 teams each (rank by average, all-games attendance, largest increase with the 2024-25 average); those columns are marked top 30, show "--" for other schools and carry no average or median.

## Percent of capacity

Both sports use the same year. Football 2025 is the Capacity % column of the D1.ticker 2025 page, as reported; D1.ticker does not publish the capacity it divides by, so the figure can differ from attendance divided by the workbook's Stadium capacity column. Men's basketball 2025-26 is a workbook formula, average home attendance divided by Arena capacity, because the NCAA book reports no percentage.
