# Round 2 instructions (read together with BRIEF.md; all BRIEF rules still apply)

HARD BUDGET: the WebSearch tool allows at most 200 calls per turn SHARED by all four conference agents. You may use AT MOST 48 WebSearch calls. Count them. When you reach 48, stop searching and finish with WebFetch only (WebFetch has no limit). Do not try to work around the limit.

Work ONLY on the (school, metric) cells listed in your gaps file. Write rows for those cells only, to the round-2 CSV path in your prompt (same 9-column header as BRIEF.md).

Make each search count: one query per school per topic, on the official domain where possible, and read the result snippets carefully (they often contain capacity, year opened, salary and deal terms). Then WebFetch the best page(s). Suggested queries:
 1. site:<athletics domain> facilities stadium arena capacity opened   (venues: stadium_name, stadium_capacity, stadium_year_opened, stadium_last_renovation_year, arena_name, arena_capacity, arena_year_opened; also look for the sports list for varsity_sports)
 2. <school> head football coach contract salary 2026 OR <school> men's basketball coach contract salary 2026   (coaches: verify who is current as of November 2026; comp = guaranteed annual under current contract; end year; source type)
 3. <school> stadium naming rights OR arena naming rights OR jersey patch OR multimedia rights Learfield Playfly OR Nike adidas apparel deal   (commercial deals; record base figures, qualifiers in notes; honorific names -> deal_type honorific)
 4. ONLY for public schools with financial gaps: one search such as  site:<school domain> "agreed upon procedures" OR "NCAA membership financial" 2025 filetype:pdf . If nothing, write nothing further for financials (the EADA fallback is already in place) and move on.

Priority order within your budget: venues first (7 cells per school), then coaches, then commercial deals, then one financial attempt per public school. Prefer schools with the most gaps. Stop early rather than exceed the budget. Many athletics sites render via JavaScript; if WebFetch returns only a title, rely on the search snippet of that official page and cite the page URL, noting "value taken from the official page's search snippet" in notes.

When done, reply with: searches used, rows written, and which cells remain unsourced.
