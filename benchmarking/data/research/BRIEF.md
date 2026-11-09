# Research brief: Power 4 athletic department benchmarking (per-conference subagent)

Date accessed for every row: 2026-11-09. You are researching ONE conference's schools (listed in your task prompt).
Output: a CSV file at the path given in your prompt, with EXACTLY this header row:

school,metric,value,unit,fiscal_year_or_season,source_name,source_url,date_accessed,notes

Append rows to the file as you go (open in append mode / use `>>`), so partial work survives. Quote fields that contain commas.
Use the school names EXACTLY as given in your prompt (e.g. "Miami (FL)", "Ole Miss", "NC State", "Texas A&M").

## HARD RULES
1. NEVER use USA Today / sportsdata.usatoday.com (NCAA finances DB, coach salary DBs) for anything. NEVER cite Wikipedia as the source of a number. Rows citing either will be rejected.
2. Every row must have a specific, working source_url (the page or PDF you actually read, not a homepage or search page). No URL = row rejected.
3. `value` must be a CLEAN value: a bare number (no $ , % or words) for numeric metrics; a short plain string for text metrics (names, partner, industry, deal type). NEVER put qualifiers like "approx", "up to", "~", "(2023)", "est." in `value` — put them in `notes`. Never round a reported figure: if the report says 185,432,117 write 185432117. If a deal is reported as "up to $X" or "approximately $X", record the base figure X in value and write "reported as up to / approximately" in notes.
4. Do not guess. If you cannot source a value to the standard below, write a row with value `--` and explain in `notes` why (e.g. "private school; MFRS not public", "no commercial naming deal; honorific name", "contract not located on school site or state portal"). Do not skip metrics silently.
5. Prefer primary/official sources in this order; record which in source_name:
   - Financials: the school's own posted NCAA Membership Financial Reporting System (MFRS) report or NCAA Agreed-Upon Procedures (AUP) report (athletics site, university controller/finance site, board of regents/trustees agenda, state transparency portal). Use the MOST RECENT fiscal year posted: FY2025 (year ended June 30, 2025) if posted, else FY2024. Do NOT use any compiled database (no USA Today, no Sportico, no Knight-Newhouse — the latter is unreachable from this environment). If no own-posted MFRS/AUP report can be found, write `--` rows with note "no school-posted MFRS report located" — the main agent will fall back to the federal EADA file.
   - Coaching pay: executed contract/amendment posted by the school or a state public-records portal; the school's official announcement; or a state employee salary database (Texas Tribune salaries, Ohio Checkbook, Transparent California, etc.). Local beat reporting ONLY if it quotes the contract terms and nothing better exists; say so in notes.
   - Venues: the school's official athletics site facility page first; a school-posted fact book or media guide second. Not Wikipedia.
   - Commercial deals: the school's or partner's press release first; Sports Business Journal, Front Office Sports, or the school's board-approved contract second; local beat reporting third. Record which.

## METRICS (use these exact `metric` keys)

### A. Financial — PUBLIC schools only (skip private schools entirely for this section; privates are listed in your prompt)
Locate the school's own posted MFRS report (search terms: "<school> NCAA agreed upon procedures 2025", "<school> membership financial report FY2025", "<school> athletics NCAA financial report", check the controller/audit/board agenda sites and state transparency sites). Read the "Statement of Revenues and Expenses" page. Report the ALL-SPORTS TOTAL column (not football-only). Use whole dollars.
- fin_report_url : value = the URL of the MFRS/AUP PDF itself (unit "url"); fiscal_year_or_season = "FY2025" or "FY2024" etc.
- fin_fiscal_year : value = 2025 (or 2024) — the fiscal year of the report used (unit "year")
- total_operating_revenue : MFRS "Total Operating Revenues" (unit "USD")
- total_operating_expenses : MFRS "Total Operating Expenses" (unit "USD")
- media_rights_revenue : MFRS line 11 Media Rights (unit "USD")
- ticket_sales_revenue : MFRS line 1 Ticket Sales (USD)
- contributions_revenue : MFRS line 8 Contributions (USD)
- ncaa_distributions : MFRS line 12 NCAA Distributions (USD)
- conference_distributions : MFRS line 13 Conference Distributions (Non Media and Non Bowl) (USD)
- conference_bowl_distributions : MFRS line 13A Conference Distributions of Football Bowl Generated Revenue (USD); 0 if the line is blank/zero
- direct_institutional_support : MFRS line 4 Direct Institutional Support (USD)
- indirect_institutional_support : MFRS line 6 Indirect Institutional Support (USD); 0 if blank
- student_fees : MFRS line 3 Student Fees (USD)
- coaching_salaries : MFRS line 22 Coaching Salaries, Benefits and Bonuses paid by the University and Related Entities (USD)
- athletics_related_debt : MFRS line 52 Total Athletics Related Debt (USD) (in "Other Reporting Items")
- debt_service : MFRS line 34 Athletic Facilities Debt Service, Leases and Rental Fees (USD) — note in notes that this line includes leases/rental fees
Every financial row for a school must come from the SAME report (same fiscal year). fiscal_year_or_season = "FY2025" style for all of them.

### B. Coaching (all schools, current 2026 football season and 2026-27 men's basketball season; verify the coach is CURRENT as of November 2026 — do not rely on memory)
- fb_hc_name : head football coach (text)
- fb_hc_annual_comp : guaranteed annual compensation for the current season under the current contract, whole dollars (USD). Base + guaranteed supplemental/talent fee; exclude bonuses/incentives. Private schools: `--` with note "private; compensation not disclosed" unless the school itself announced a figure.
- fb_hc_contract_end : last contract year (e.g. 2030) (unit "year")
- fb_hc_pay_source_type : one of: contract / school announcement / state salary database / press report (text)
- mbb_hc_name, mbb_hc_annual_comp, mbb_hc_contract_end, mbb_hc_pay_source_type : same for the men's basketball head coach

### C. Venues (all schools)
- stadium_name : football stadium official name (text)
- stadium_capacity : official listed capacity (unit "seats")
- stadium_year_opened : (unit "year")
- stadium_last_renovation_year : most recent major renovation/expansion completion year (unit "year"); `--` if none documented
- arena_name : men's basketball home arena (text)
- arena_capacity : (unit "seats")
- arena_year_opened : (unit "year")

### D. Stadium naming rights (all schools)
- stadium_nr_partner : corporate partner, or the donor/honoree name if honorific, or "none" (text)
- stadium_nr_industry : partner's industry (e.g. banking, insurance, energy, telecom, retail, healthcare); "--" if honorific/none (text)
- stadium_nr_deal_type : exactly one of: commercial / honorific / none
- stadium_nr_start_year : deal start year (unit "year")
- stadium_nr_term_years : term in years (unit "years")
- stadium_nr_annual_value : annual value USD
- stadium_nr_total_value : total value USD
Only report the value fields that were actually publicly reported; the main agent derives the third from the other two. For honorific names, report partner + deal_type=honorific and `--` for the industry/start/term/annual/total rows (with note "honorific; no commercial fee").

### E. Arena naming rights: arena_nr_partner, arena_nr_industry, arena_nr_deal_type, arena_nr_start_year, arena_nr_term_years, arena_nr_annual_value, arena_nr_total_value (same rules)

### F. Football jersey or helmet patch sponsor (NCAA permitted commercial patches starting with the 2025 season; many schools signed deals in 2025-2026)
- patch_partner, patch_industry, patch_start_year, patch_term_years, patch_annual_value, patch_total_value. If no patch deal: patch_partner = "none" with a source URL supporting that if possible (e.g. a roundup article of patch deals), else `--` with note.

### G. Multimedia rights (MMR)
- mmr_partner : one of Learfield / Playfly / Van Wagner / in-house / other (if other, name it in notes) (text)
- mmr_start_year, mmr_term_years, mmr_annual_value, mmr_total_value (report what was publicly disclosed; many MMR deals disclose total and term)

### H. Apparel
- apparel_partner : Nike / Jordan Brand / adidas / Under Armour / other (text)
- apparel_start_year, apparel_term_years, apparel_annual_value, apparel_total_value

## Priorities and pacing
Work school by school. For each school do section A first (most valuable), then B, C, then D-H. Write rows for a school as soon as you have them. Budget your effort: ~15-25 tool calls per school. If a value is genuinely not public after a reasonable search, write the `--` row and move on. When finished, reply with: number of rows written, the schools for which you found a school-posted MFRS report (with fiscal year), and any metrics you could not source at all.
