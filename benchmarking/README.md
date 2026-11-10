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

Financial line items (the MFRS columns) are summarized for each fiscal year present in the data and for all years; every other column is summarized across all years only. The summary rows sit under the schools on each conference tab and, by conference and for all schools, on `All Schools`. The fiscal-year medians are array formulas.

## Football attendance

`data/d1ticker/` holds the D1.ticker FBS Attendance Trends pages for 2023, 2024 and 2025, saved unmodified. `scripts/build_attendance.py` reads the Final Average column of each season's own page into `data/attendance_values.csv`.
