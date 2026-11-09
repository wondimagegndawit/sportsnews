# Power 4 athletic department benchmarking

`Power4_Athletic_Department_Benchmarking.xlsx` benchmarks all 67 Power 4 athletic departments. It was built from scratch with openpyxl (`scripts/`) and recalculated with LibreOffice; every hardcoded value on the conference tabs is hyperlinked to its source and logged on `06 - Source Log`.

## Folders

- `data/` raw bulk downloads, saved unmodified: IPEDS HD2024 and EF2024A, EADA 2024-25, NCAA APR/GSR search responses and report PDFs, ESPN standings JSON, Sports-Reference men's basketball pages, NACDA Directors' Cup final standings PDFs. Also the derived `bulk_values.csv`, `merged_values.csv`, `review_rejections.csv` and `coverage.json`.
- `data/research/` the per-conference research CSVs returned by the research subagents, plus the brief they worked from.
- `scripts/` `schools.py` (master list and identifiers), `build_bulk.py`, `fetch_ncaa_academics.py`, `merge_research.py`, `build_workbook.py`.

## Rebuild

```bash
python3 -I scripts/build_bulk.py
python3 -I scripts/merge_research.py
python3 -I scripts/build_workbook.py
```

Then recalculate the file in LibreOffice (headless) before use.
