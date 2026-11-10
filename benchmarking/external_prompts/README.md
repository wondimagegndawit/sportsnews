# External research prompts

- `CODEX_PROMPT.md`: one prompt for a coding agent with web access (OpenAI Codex). It reads `data/gaps_remaining.csv`, writes `data/research/external_codex.csv`, and reruns the build.
- `PERPLEXITY_PROMPT.md`: master instructions plus one block per school for a search-answer engine. Paste the returned tables into `data/research/external_perplexity.csv`.

Any CSV dropped into `data/research/` with the standard 9-column header is picked up automatically by `scripts/merge_research.py`, which applies the same review rules (prohibited sources, missing URLs, dirty numbers, inferred figures) and writes rejections to `data/review_rejections.csv`. Then run `scripts/build_workbook.py`, recalculate in LibreOffice, and `scripts/qa.py`.
