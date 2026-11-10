# Round 4 instructions (BRIEF.md rules still apply: no USA Today, no Wikipedia or wiki mirrors, no fan sites, clean values, URL on every valued row, qualifiers in notes)

HARD BUDGET: at most 48 WebSearch calls (200 per turn shared by four agents). Count them; at 48 stop searching and finish with WebFetch only (unlimited). Do not work around the limit.

Work only on the cells in your gaps4 file. Priority order (the user is an investor in media rights and revenue generation, so commercial deal TERMS matter most):
1. Multimedia rights (MMR): partner (Learfield / Playfly / Van Wagner / in-house / other), start year, term, annual and total value. Best sources: Learfield/Playfly/Van Wagner press releases, Sports Business Journal, Front Office Sports, board-approved contracts, local reporting of records requests. Query pattern: "<school>" multimedia rights Learfield OR Playfly OR "Van Wagner" extension years million.
2. Apparel: partner, start year, term, annual and total value. Query: "<school>" Nike OR adidas OR "Under Armour" OR Jordan apparel contract years million.
3. Stadium and arena naming rights terms (start year, term, annual, total) for deals already identified as commercial, plus partner/deal type where still missing. Honorific names need only partner + deal_type=honorific.
4. Jersey patch terms (start year, term, annual, total) where a partner is known; partner/industry where missing (2025-26 and 2026 season deals).
5. Remaining venue cells and varsity_sports counts (official pages; search snippets of the official page are acceptable, say so in notes).
6. Remaining coaching cells (year-specific guaranteed figures only; no averages, no escalator math).
7. Financial: only if you have a concrete lead (West Virginia 2024-25 AUP PDF link on wvusports.com; Rutgers FY2025 KPMG AUP; Kansas State "Forms, Documents and Reports" page; Oklahoma State AUP archive). One search each at most.

Values rule for deals: record what was publicly reported; "up to"/"approximately"/"more than" -> record the base figure and put the qualifier in notes (that is acceptable; do NOT write "estimate" in notes unless the source itself calls it an estimate). Never compute annual from total or vice versa; the workbook derives the third figure. Record the deal's start year as the first contract year and term in years.

Output: your round-4 CSV path, same 9-column header as BRIEF.md, append rows as you go. When done, reply with searches used, rows written by category, and what remains unsourced.
