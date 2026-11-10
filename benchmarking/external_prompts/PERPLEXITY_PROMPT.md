# Perplexity prompts: fill the remaining gaps

Perplexity works best one school at a time. Paste the MASTER INSTRUCTIONS once, then paste one SCHOOL BLOCK per message (or one conference per thread if your plan allows long outputs). Copy each answer table into a CSV with this header and save it as `benchmarking/data/research/external_perplexity.csv`, then run the three build scripts described in `benchmarking/README.md`.

school,metric,value,unit,fiscal_year_or_season,source_name,source_url,date_accessed,notes

## MASTER INSTRUCTIONS (paste first)

I am filling gaps in a benchmarking dataset of Power 4 college athletic departments. For each item I list, find the value and the exact URL where it is stated. Answer ONLY with a markdown table with these columns: school | metric | value | unit | fiscal_year_or_season | source_name | source_url | notes. One row per metric. If a value is not publicly available, put "--" in value and say why in notes (e.g. "terms not disclosed", "report not posted"). Do not guess and do not compute values that were not reported.

RULES (non-negotiable)
1. Do NOT use USA Today / sportsdata.usatoday.com for anything (no NCAA finances database, no coach salary databases), and do not cite Wikipedia or wiki mirrors or fan sites (e.g. Stadium Journey) for any number.
2. Every value must come with the specific URL of the page or PDF where you read it (not a homepage, not a search page). No URL, no value.
3. Values must be clean: bare numbers for numeric fields (no $ , % or words), whole dollars, no rounding of a reported figure. Put qualifiers ("up to", "approximately", "more than") in the notes column and record the base figure. Do not compute a figure that was not reported (no annual = total / term, no escalator math, no averages presented as a year figure, no inferred contract end years). If a figure is not public, say "not public" and move on.
4. Source preference: (a) the school's own posting (athletics site, controller/audit office, board of trustees or regents agenda, state auditor or transparency portal); (b) the partner's press release; (c) Sports Business Journal, Front Office Sports, or the board-approved contract; (d) local beat reporting that quotes contract terms. Say which tier each value came from.
5. Financials: only the NCAA Membership Financial Reporting System (MFRS) report or the NCAA agreed-upon-procedures (AUP) report that includes the Statement of Revenues and Expenses, most recent fiscal year (FY2025 = year ended June 30, 2025 preferred; FY2024 acceptable). Use the ALL SPORTS total column. Do not substitute GAAP audited statements, EADA filings, budgets, or Knight-Newhouse/Sportico compilations.
6. Coaching pay: the guaranteed annual compensation for the current season (2026 football, 2026-27 men's basketball) under the current contract, from the executed contract/term sheet, the school's announcement, or a state salary database. Record the contract end year. Verify the coach is in place as of November 2026.
7. Deal fields: start year = first contract year; term = years; annual and total = only what was reported; deal type for venue names = commercial / honorific (donor or memorial name, no fee) / none.

Metric key meanings: mmr_* = multimedia rights deal (partner one of Learfield / Playfly / Van Wagner / JMI Sports / Legends / in-house / other); apparel_* = apparel/footwear deal; stadium_nr_* and arena_nr_* = naming-rights deal for the football stadium and men's basketball arena (partner, industry, deal_type commercial/honorific/none, start_year, term_years, annual_value, total_value); patch_* = football jersey/helmet patch sponsorship; stadium_capacity / stadium_year_opened / stadium_last_renovation_year / arena_capacity / arena_year_opened from the official facility page; varsity_sports = number of varsity sports sponsored (count men's and women's separately); fb_hc_* / mbb_hc_* = head football / men's basketball coach name, annual guaranteed compensation for the current season, contract end year, pay source type (contract / school announcement / state salary database / press report); financial fields = lines from the NCAA MFRS Statement of Revenues and Expenses, ALL SPORTS column (line 1 ticket sales, 3 student fees, 4 direct institutional support, 6 indirect institutional support, 8 contributions, 11 media rights, 12 NCAA distributions, 13 conference distributions, 13A conference bowl distributions, 22 coaching salaries/benefits/bonuses paid by the university, 34 athletic facilities debt service/leases/rental fees, 52 total athletics-related debt, plus total operating revenues and total operating expenses).

## SCHOOL BLOCKS (paste one per message)

### ACC

School: Boston College (ACC; Private; MA). Already known for context: stadium_name=Alumni Stadium; arena_name=Conte Forum; fb_hc_name=Bill O'Brien; mbb_hc_name=Luke Murray; patch_partner=none; mmr_partner=Van Wagner; apparel_partner=other.
Find these items for Boston College:
- multimedia rights (MMR) deal: term_years, annual_value, total_value
- apparel deal: annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- venues / department: stadium_year_opened

School: California (ACC; Public; CA). Already known for context: stadium_name=California Memorial Stadium; arena_name=Haas Pavilion; fb_hc_name=Tosh Lupoi; mbb_hc_name=Mark Madsen; stadium_nr_partner=Databricks; patch_partner=Dialpad; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for California:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: annual_value, total_value
- football stadium naming-rights deal: term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: annual_value
- venues / department: stadium_year_opened
- coaching: fb_hc_annual_comp, fb_hc_contract_end, fb_hc_pay_source_type, mbb_hc_annual_comp, mbb_hc_pay_source_type
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Clemson (ACC; Public; SC). Already known for context: stadium_name=Memorial Stadium; arena_name=Littlejohn Coliseum; fb_hc_name=Dabo Swinney; mbb_hc_name=Brad Brownell; stadium_nr_partner=none; arena_nr_partner=none; patch_partner=none; mmr_partner=in-house; apparel_partner=Nike.
Find these items for Clemson:
- multimedia rights (MMR) deal: term_years, annual_value, total_value
- apparel deal: annual_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Duke (ACC; Private; NC). Already known for context: stadium_name=Brooks Field at Wallace Wade Stadium; arena_name=Cameron Indoor Stadium; fb_hc_name=Manny Diaz; mbb_hc_name=Jon Scheyer; patch_partner=none; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Duke:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value

School: Florida State (ACC; Public; FL). Already known for context: stadium_name=Doak Campbell Stadium; fb_hc_name=Rick Stockstill (interim); mbb_hc_name=Luke Loucks; patch_partner=Kin Insurance; mmr_partner=other; apparel_partner=Nike.
Find these items for Florida State:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: annual_value, total_value
- venues / department: arena_name, arena_year_opened
- coaching: fb_hc_annual_comp, fb_hc_contract_end, fb_hc_pay_source_type
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Georgia Tech (ACC; Public; GA). Already known for context: stadium_name=Bobby Dodd Stadium at Hyundai Field; arena_name=McCamish Pavilion; fb_hc_name=Brent Key; mbb_hc_name=Scott Cross; stadium_nr_partner=Hyundai; patch_partner=Veritiv; mmr_partner=other; apparel_partner=Under Armour.
Find these items for Georgia Tech:
- multimedia rights (MMR) deal: start_year, annual_value, total_value
- apparel deal: total_value
- football stadium naming-rights deal: annual_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, annual_value, total_value
- coaching: mbb_hc_contract_end
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Louisville (ACC; Public; KY). Already known for context: stadium_name=L&N Federal Credit Union Stadium; arena_name=KFC Yum! Center; fb_hc_name=Jeff Brohm; mbb_hc_name=Pat Kelsey; stadium_nr_partner=L&N Federal Credit Union; patch_partner=L&N Federal Credit Union; mmr_partner=Learfield; apparel_partner=adidas.
Find these items for Louisville:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: annual_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: start_year, term_years, annual_value, total_value
- venues / department: stadium_last_renovation_year
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Miami (FL) (ACC; Private; FL). Already known for context: stadium_name=Hard Rock Stadium; arena_name=Watsco Center; fb_hc_name=Mario Cristobal; mbb_hc_name=Jai Lucas; stadium_nr_partner=Hard Rock International; arena_nr_partner=Watsco; patch_partner=none; apparel_partner=Nike.
Find these items for Miami (FL):
- multimedia rights (MMR) deal: partner, start_year, term_years, annual_value, total_value
- apparel deal: term_years
- football stadium naming-rights deal: annual_value
- basketball arena naming-rights deal: start_year, term_years, annual_value, total_value
- venues / department: stadium_capacity

School: NC State (ACC; Public; NC). Already known for context: stadium_name=Carter-Finley Stadium; arena_name=Lenovo Center; fb_hc_name=Todd Goebbel (interim); mbb_hc_name=Justin Gainey; arena_nr_partner=Lenovo; patch_partner=none; mmr_partner=Learfield; apparel_partner=adidas.
Find these items for NC State:
- multimedia rights (MMR) deal: term_years, annual_value
- apparel deal: start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: annual_value
- venues / department: stadium_last_renovation_year, arena_year_opened
- coaching: fb_hc_annual_comp, fb_hc_contract_end, fb_hc_pay_source_type, mbb_hc_contract_end
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: North Carolina (ACC; Public; NC). Already known for context: stadium_name=Kenan Memorial Stadium; arena_name=Dean E. Smith Center; fb_hc_name=Bill Belichick; mbb_hc_name=Michael Malone; stadium_nr_partner=William Rand Kenan Sr. and Mary Hargrave Kenan; arena_nr_partner=Dean E. Smith; patch_partner=none; mmr_partner=Learfield; apparel_partner=Jordan Brand.
Find these items for North Carolina:
- coaching: mbb_hc_contract_end

School: Pittsburgh (ACC; Public; PA). Already known for context: stadium_name=Acrisure Stadium; arena_name=Petersen Events Center; fb_hc_name=Pat Narduzzi; mbb_hc_name=Jeff Capel; patch_partner=UPMC; mmr_partner=other; apparel_partner=Nike.
Find these items for Pittsburgh:
- multimedia rights (MMR) deal: term_years, annual_value, total_value
- apparel deal: term_years, annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, annual_value, total_value
- venues / department: stadium_last_renovation_year
- coaching: fb_hc_annual_comp, mbb_hc_annual_comp
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: SMU (ACC; Private; TX). Already known for context: stadium_name=Gerald J. Ford Stadium; arena_name=Moody Coliseum; fb_hc_name=Rhett Lashlee; mbb_hc_name=Andy Enfield; stadium_nr_partner=Gerald J. Ford; patch_partner=Texas Capital; mmr_partner=Learfield.
Find these items for SMU:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, annual_value, total_value

School: Stanford (ACC; Private; CA). Already known for context: stadium_name=Stanford Stadium; arena_name=Maples Pavilion; fb_hc_name=Tavita Pritchard; mbb_hc_name=Kyle Smith; arena_nr_partner=Roscoe Maples; patch_partner=DoorDash; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Stanford:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, annual_value, total_value

School: Syracuse (ACC; Private; NY). Already known for context: stadium_name=JMA Wireless Dome; arena_name=JMA Wireless Dome; fb_hc_name=Fran Brown; mbb_hc_name=Gerry McNamara; stadium_nr_partner=JMA Wireless; arena_nr_partner=JMA Wireless; patch_partner=none; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Syracuse:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: term_years, annual_value, total_value
- football stadium naming-rights deal: annual_value, total_value
- basketball arena naming-rights deal: annual_value, total_value

School: Virginia (ACC; Public; VA). Already known for context: stadium_name=Scott Stadium; arena_name=John Paul Jones Arena; fb_hc_name=Tony Elliott; mbb_hc_name=Ryan Odom; stadium_nr_partner=Frederic William Scott family; arena_nr_partner=John Paul Jones; patch_partner=none; mmr_partner=Playfly; apparel_partner=Nike.
Find these items for Virginia:
- multimedia rights (MMR) deal: start_year, annual_value, total_value
- apparel deal: annual_value

School: Virginia Tech (ACC; Public; VA). Already known for context: stadium_name=Lane Stadium/Worsham Field; arena_name=Cassell Coliseum; fb_hc_name=James Franklin; mbb_hc_name=Mike Young; stadium_nr_partner=Edward H. Lane / Wes and Janet Worsham; arena_nr_partner=Carilion Clinic; patch_partner=none; mmr_partner=Playfly; apparel_partner=Nike.
Find these items for Virginia Tech:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: start_year, term_years, annual_value, total_value
- coaching: mbb_hc_annual_comp

School: Wake Forest (ACC; Private; NC). Already known for context: stadium_name=Allegacy Federal Credit Union Stadium; arena_name=Lawrence Joel Veterans Memorial Coliseum; fb_hc_name=Jake Dickert; mbb_hc_name=Steve Forbes; stadium_nr_partner=Allegacy Federal Credit Union; arena_nr_partner=Lawrence Joel; patch_partner=none; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Wake Forest:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: term_years, annual_value, total_value
- football stadium naming-rights deal: term_years, annual_value, total_value
- venues / department: stadium_last_renovation_year

### Big Ten

School: Illinois (Big Ten; Public; IL). Already known for context: stadium_name=Gies Memorial Stadium; arena_name=State Farm Center; fb_hc_name=Bret Bielema; mbb_hc_name=Brad Underwood; stadium_nr_partner=Gies; arena_nr_partner=State Farm; patch_partner=Busey Bank; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Illinois:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: start_year, annual_value, total_value
- basketball arena naming-rights deal: annual_value

School: Indiana (Big Ten; Public; IN). Already known for context: stadium_name=Memorial Stadium; arena_name=Simon Skjodt Assembly Hall; fb_hc_name=Curt Cignetti; mbb_hc_name=Darian DeVries; arena_nr_partner=Simon Skjodt; patch_partner=Merchants Bank; mmr_partner=Learfield; apparel_partner=adidas.
Find these items for Indiana:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: start_year, annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: annual_value, total_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Iowa (Big Ten; Public; IA). Already known for context: stadium_name=Kinnick Stadium; arena_name=Carver-Hawkeye Arena; fb_hc_name=Kirk Ferentz; mbb_hc_name=Ben McCollum; stadium_nr_partner=Kinnick; arena_nr_partner=Carver (Roy J. Carver); patch_partner=none; mmr_partner=Learfield.
Find these items for Iowa:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- coaching: fb_hc_annual_comp
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Maryland (Big Ten; Public; MD). Already known for context: stadium_name=SECU Stadium; arena_name=XFINITY Center; fb_hc_name=Mike Locksley; mbb_hc_name=Buzz Williams; stadium_nr_partner=SECU; arena_nr_partner=Comcast (XFINITY); patch_partner=none; mmr_partner=Playfly; apparel_partner=Under Armour.
Find these items for Maryland:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: annual_value
- football stadium naming-rights deal: annual_value
- basketball arena naming-rights deal: start_year, term_years, annual_value, total_value
- coaching: mbb_hc_annual_comp
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Michigan (Big Ten; Public; MI). Already known for context: stadium_name=Michigan Stadium; arena_name=Crisler Center; fb_hc_name=Kyle Whittingham; mbb_hc_name=Dusty May; stadium_nr_partner=none; arena_nr_partner=Crisler (Herbert 'Fritz' Crisler); patch_partner=none; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Michigan:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: annual_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Michigan State (Big Ten; Public; MI). Already known for context: stadium_name=Spartan Stadium; arena_name=Breslin Center; fb_hc_name=Pat Fitzgerald; mbb_hc_name=Tom Izzo; patch_partner=MSU Federal Credit Union; mmr_partner=Playfly; apparel_partner=Nike.
Find these items for Michigan State:
- multimedia rights (MMR) deal: term_years, annual_value
- apparel deal: start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: start_year, annual_value
- coaching: mbb_hc_contract_end
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Minnesota (Big Ten; Public; MN). Already known for context: stadium_name=Huntington Bank Stadium; arena_name=Williams Arena; fb_hc_name=P.J. Fleck; mbb_hc_name=Niko Medved; stadium_nr_partner=Huntington Bank; arena_nr_partner=Williams (Dr. Henry L. Williams); patch_partner=none; mmr_partner=Learfield.
Find these items for Minnesota:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: term_years
- venues / department: stadium_last_renovation_year

School: Nebraska (Big Ten; Public; NE). Already known for context: stadium_name=Memorial Stadium; arena_name=Pinnacle Bank Arena; fb_hc_name=Matt Rhule; mbb_hc_name=Fred Hoiberg; stadium_nr_partner=none; arena_nr_partner=Pinnacle Bank; patch_partner=none; mmr_partner=Playfly; apparel_partner=adidas.
Find these items for Nebraska:
- multimedia rights (MMR) deal: annual_value
- apparel deal: annual_value
- venues / department: stadium_last_renovation_year
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Northwestern (Big Ten; Private; IL). Already known for context: stadium_name=Ryan Field; arena_name=Welsh-Ryan Arena; fb_hc_name=David Braun; mbb_hc_name=Chris Collins; stadium_nr_partner=Ryan; arena_nr_partner=Welsh and Ryan; patch_partner=none; apparel_partner=Under Armour.
Find these items for Northwestern:
- multimedia rights (MMR) deal: partner, start_year, term_years, annual_value, total_value
- apparel deal: start_year, annual_value, total_value
- venues / department: stadium_year_opened

School: Ohio State (Big Ten; Public; OH). Already known for context: stadium_name=Ohio Stadium; arena_name=Value City Arena at the Jerome Schottenstein Center; fb_hc_name=Ryan Day; mbb_hc_name=Jake Diebler; stadium_nr_partner=none; arena_nr_partner=Value City Furniture; patch_partner=JPMorganChase; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Ohio State:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: start_year, annual_value
- basketball arena naming-rights deal: start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, total_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Oregon (Big Ten; Public; OR). Already known for context: stadium_name=Autzen Stadium; arena_name=Matthew Knight Arena; fb_hc_name=Dan Lanning; mbb_hc_name=Dana Altman; stadium_nr_partner=Autzen; arena_nr_partner=Matthew Knight; patch_partner=none; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Oregon:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: start_year, annual_value
- coaching: fb_hc_annual_comp

School: Penn State (Big Ten; Public; PA). Already known for context: stadium_name=Beaver Stadium (West Shore Home Field at Beaver Stadium); arena_name=Bryce Jordan Center; fb_hc_name=Matt Campbell; mbb_hc_name=Mike Rhoades; stadium_nr_partner=West Shore Home; patch_partner=none; mmr_partner=Playfly; apparel_partner=adidas.
Find these items for Penn State:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: annual_value
- football stadium naming-rights deal: annual_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value

School: Purdue (Big Ten; Public; IN). Already known for context: stadium_name=Ross-Ade Stadium; arena_name=Mackey Arena; fb_hc_name=Barry Odom; mbb_hc_name=Matt Painter; stadium_nr_partner=Ross-Ade; arena_nr_partner=Mackey; patch_partner=none; mmr_partner=Learfield.
Find these items for Purdue:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Rutgers (Big Ten; Public; NJ). Already known for context: stadium_name=SHI Stadium; arena_name=Jersey Mike's Arena; fb_hc_name=Greg Schiano; mbb_hc_name=Steve Pikiell; stadium_nr_partner=SHI International Corp.; arena_nr_partner=Jersey Mike's Subs; patch_partner=none; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Rutgers:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: annual_value, total_value
- football stadium naming-rights deal: term_years, annual_value, total_value
- basketball arena naming-rights deal: term_years, annual_value
- coaching: mbb_hc_annual_comp
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: UCLA (Big Ten; Public; CA). Already known for context: stadium_name=Rose Bowl; arena_name=Pauley Pavilion presented by Wescom Financial; fb_hc_name=Bob Chesney; mbb_hc_name=Mick Cronin; arena_nr_partner=Wescom Financial; patch_partner=none; mmr_partner=other; apparel_partner=Jordan Brand.
Find these items for UCLA:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: start_year, annual_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: annual_value
- venues / department: stadium_last_renovation_year
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: USC (Big Ten; Private; CA). Already known for context: stadium_name=United Airlines Field at the Los Angeles Memorial Coliseum; arena_name=Galen Center; fb_hc_name=Lincoln Riley; mbb_hc_name=Eric Musselman; stadium_nr_partner=United Airlines; arena_nr_partner=Galen; patch_partner=none; mmr_partner=Learfield.
Find these items for USC:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: annual_value, total_value

School: Washington (Big Ten; Public; WA). Already known for context: stadium_name=Husky Stadium; arena_name=Alaska Airlines Arena at Hec Edmundson Pavilion; fb_hc_name=Jedd Fisch; mbb_hc_name=Danny Sprinkle; stadium_nr_partner=none; arena_nr_partner=Alaska Airlines; patch_partner=none; mmr_partner=Learfield; apparel_partner=adidas.
Find these items for Washington:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: annual_value
- basketball arena naming-rights deal: start_year, annual_value
- coaching: mbb_hc_annual_comp

School: Wisconsin (Big Ten; Public; WI). Already known for context: stadium_name=Camp Randall Stadium; arena_name=Kohl Center; fb_hc_name=Luke Fickell; mbb_hc_name=Greg Gard; patch_partner=Culver's; mmr_partner=Learfield; apparel_partner=Under Armour.
Find these items for Wisconsin:
- multimedia rights (MMR) deal: term_years, annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, annual_value, total_value
- venues / department: stadium_year_opened

### Big 12

School: Arizona (Big 12; Public; AZ). Already known for context: stadium_name=Casino Del Sol Stadium; arena_name=McKale Center at ALKEME Arena; fb_hc_name=Brent Brennan; mbb_hc_name=Tommy Lloyd; stadium_nr_partner=Casino Del Sol; arena_nr_partner=ALKEME; patch_partner=Monster Energy; mmr_partner=in-house; apparel_partner=Nike.
Find these items for Arizona:
- multimedia rights (MMR) deal: term_years, annual_value, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: annual_value
- basketball arena naming-rights deal: annual_value
- football jersey/helmet patch deal: term_years, total_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Arizona State (Big 12; Public; AZ). Already known for context: stadium_name=Mountain America Stadium; arena_name=Desert Financial Arena; fb_hc_name=Kenny Dillingham; mbb_hc_name=Randy Bennett; stadium_nr_partner=Mountain America Credit Union; arena_nr_partner=Desert Financial Credit Union; patch_partner=Monster Energy; mmr_partner=in-house; apparel_partner=adidas.
Find these items for Arizona State:
- multimedia rights (MMR) deal: term_years, annual_value, total_value
- apparel deal: term_years, annual_value, total_value
- football stadium naming-rights deal: annual_value
- football jersey/helmet patch deal: term_years, total_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Baylor (Big 12; Private; TX). Already known for context: stadium_name=McLane Stadium; arena_name=Foster Pavilion; fb_hc_name=Joe Klanderman (interim); mbb_hc_name=Scott Drew; stadium_nr_partner=Drayton McLane Jr. and family; arena_nr_partner=Foster family (donor); patch_partner=Monster Energy; mmr_partner=Playfly.
Find these items for Baylor:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, total_value
- venues / department: stadium_last_renovation_year, varsity_sports

School: BYU (Big 12; Private; UT). Already known for context: stadium_name=LaVell Edwards Stadium; arena_name=Marriott Center; fb_hc_name=Kalani Sitake; mbb_hc_name=Kevin Young; stadium_nr_partner=LaVell Edwards; arena_nr_partner=Marriott family; patch_partner=Entrata; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for BYU:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, annual_value, total_value
- venues / department: stadium_last_renovation_year

School: Cincinnati (Big 12; Public; OH). Already known for context: stadium_name=Nippert Stadium; arena_name=Fifth Third Arena; fb_hc_name=Scott Satterfield; mbb_hc_name=Wes Miller; stadium_nr_partner=none; arena_nr_partner=Fifth Third Bank; patch_partner=Jeff Wyler Family Automotive; mmr_partner=in-house; apparel_partner=Nike.
Find these items for Cincinnati:
- multimedia rights (MMR) deal: term_years, annual_value, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: term_years, annual_value, total_value
- football jersey/helmet patch deal: start_year, term_years, annual_value, total_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Colorado (Big 12; Public; CO). Already known for context: stadium_name=Folsom Field; fb_hc_name=Deion Sanders; mbb_hc_name=Tad Boyle; stadium_nr_partner=Folsom (Folsom Field); patch_partner=Monster Energy; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Colorado:
- multimedia rights (MMR) deal: start_year, annual_value, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, total_value
- venues / department: arena_name, arena_capacity, arena_year_opened, varsity_sports
- coaching: mbb_hc_annual_comp, mbb_hc_contract_end, mbb_hc_pay_source_type

School: Houston (Big 12; Public; TX). Already known for context: stadium_name=TDECU Stadium; arena_name=Fertitta Center; fb_hc_name=Willie Fritz; mbb_hc_name=Kelvin Sampson; stadium_nr_partner=TDECU (Texas Dow Employees Credit Union); patch_partner=Monster Energy; mmr_partner=Learfield.
Find these items for Houston:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: annual_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, total_value
- venues / department: stadium_last_renovation_year, arena_capacity, arena_year_opened, varsity_sports
- coaching: fb_hc_contract_end, mbb_hc_annual_comp

School: Iowa State (Big 12; Public; IA). Already known for context: stadium_name=Jack Trice Stadium; fb_hc_name=Matt Campbell; mbb_hc_name=T.J. Otzelberger; patch_partner=Monster Energy; mmr_partner=Learfield.
Find these items for Iowa State:
- multimedia rights (MMR) deal: term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, total_value
- venues / department: stadium_capacity, arena_name, arena_capacity, arena_year_opened, varsity_sports
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Kansas (Big 12; Public; KS). Already known for context: stadium_name=David Booth Kansas Memorial Stadium; arena_name=Allen Fieldhouse; fb_hc_name=Lance Leipold; mbb_hc_name=Bill Self; stadium_nr_partner=David Booth; arena_nr_partner=none; patch_partner=Ripple; mmr_partner=Learfield; apparel_partner=adidas.
Find these items for Kansas:
- multimedia rights (MMR) deal: start_year, annual_value, total_value
- apparel deal: annual_value
- football jersey/helmet patch deal: start_year, term_years, annual_value, total_value
- venues / department: stadium_capacity, varsity_sports
- coaching: mbb_hc_annual_comp, mbb_hc_contract_end

School: Kansas State (Big 12; Public; KS). Already known for context: stadium_name=Bill Snyder Family Stadium; fb_hc_name=Collin Klein; mbb_hc_name=Casey Alexander; stadium_nr_partner=Bill Snyder family; patch_partner=Purple Wave Auction; mmr_partner=Learfield.
Find these items for Kansas State:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: start_year, annual_value, total_value
- venues / department: stadium_capacity, arena_name, arena_capacity, arena_year_opened, varsity_sports
- coaching: mbb_hc_annual_comp
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Oklahoma State (Big 12; Public; OK). Already known for context: stadium_name=Boone Pickens Stadium; arena_name=Gallagher-Iba Arena; fb_hc_name=Eric Morris; mbb_hc_name=Steve Lutz; stadium_nr_partner=T. Boone Pickens; arena_nr_partner=Gallagher and Iba (honorees); patch_partner=Osage Nation; mmr_partner=Learfield.
Find these items for Oklahoma State:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: start_year, term_years, annual_value, total_value
- venues / department: stadium_year_opened, varsity_sports
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: TCU (Big 12; Private; TX). Already known for context: stadium_name=Amon G. Carter Stadium; arena_name=Ed and Rae Schollmaier Arena; fb_hc_name=Sonny Dykes; mbb_hc_name=Jamie Dixon; stadium_nr_partner=Amon G. Carter; arena_nr_partner=Ed and Rae Schollmaier; patch_partner=Monster Energy; mmr_partner=Learfield.
Find these items for TCU:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, total_value
- venues / department: stadium_year_opened, arena_year_opened

School: Texas Tech (Big 12; Public; TX). Already known for context: stadium_name=Galaxy Stadium; arena_name=United Supermarkets Arena; fb_hc_name=Joey McGuire; mbb_hc_name=Grant McCasland; stadium_nr_partner=Galaxy Digital; arena_nr_partner=United Supermarkets; patch_partner=Monster Energy; apparel_partner=adidas.
Find these items for Texas Tech:
- multimedia rights (MMR) deal: partner, start_year, term_years, annual_value, total_value
- apparel deal: annual_value, total_value
- football stadium naming-rights deal: industry, deal_type, annual_value
- basketball arena naming-rights deal: annual_value
- football jersey/helmet patch deal: term_years, total_value
- venues / department: stadium_capacity, varsity_sports
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: UCF (Big 12; Public; FL). Already known for context: stadium_name=Acrisure Bounce House; arena_name=Addition Financial Arena; fb_hc_name=Scott Frost; mbb_hc_name=Johnny Dawkins; stadium_nr_partner=Acrisure; arena_nr_partner=Addition Financial Credit Union; patch_partner=Monster Energy; mmr_partner=Playfly.
Find these items for UCF:
- multimedia rights (MMR) deal: annual_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: annual_value
- basketball arena naming-rights deal: annual_value
- football jersey/helmet patch deal: term_years, total_value
- venues / department: varsity_sports
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Utah (Big 12; Public; UT). Already known for context: stadium_name=Rice-Eccles Stadium; arena_name=Jon M. Huntsman Center; fb_hc_name=Morgan Scalley; mbb_hc_name=Alex Jensen; stadium_nr_partner=Rice and Eccles families (Rice-Eccles); arena_nr_partner=Jon M. Huntsman (Huntsman Center); patch_partner=University of Utah Health; mmr_partner=in-house; apparel_partner=Under Armour.
Find these items for Utah:
- multimedia rights (MMR) deal: term_years, annual_value, total_value
- football jersey/helmet patch deal: start_year, term_years, annual_value, total_value

School: West Virginia (Big 12; Public; WV). Already known for context: stadium_name=Milan Puskar Stadium; arena_name=Hope Coliseum; fb_hc_name=Rich Rodriguez; mbb_hc_name=Ross Hodge; stadium_nr_partner=Milan Puskar; arena_nr_partner=Hope Gas; patch_partner=Antero Resources; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for West Virginia:
- multimedia rights (MMR) deal: term_years, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: annual_value, total_value
- football jersey/helmet patch deal: start_year, annual_value, total_value
- venues / department: stadium_last_renovation_year
- coaching: mbb_hc_annual_comp

### SEC

School: Alabama (SEC; Public; AL). Already known for context: stadium_name=Saban Field at Bryant-Denny Stadium; arena_name=Coleman Coliseum; fb_hc_name=Kalen DeBoer; mbb_hc_name=Nate Oats; patch_partner=none; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Alabama:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Arkansas (SEC; Public; AR). Already known for context: stadium_name=Donald W. Reynolds Razorback Stadium; arena_name=Bud Walton Arena; fb_hc_name=Ryan Silverfield; mbb_hc_name=John Calipari; stadium_nr_partner=CommunityAmerica Credit Union; patch_partner=Tyson Foods; mmr_partner=Learfield.
Find these items for Arkansas:
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: annual_value, total_value
- venues / department: stadium_capacity

School: Auburn (SEC; Public; AL). Already known for context: stadium_name=Jordan-Hare Stadium; arena_name=Neville Arena; fb_hc_name=Alex Golesh; mbb_hc_name=Steven Pearl; stadium_nr_partner=Shug Jordan and Clifford Hare (honorees); patch_partner=none; apparel_partner=Nike.
Find these items for Auburn:
- multimedia rights (MMR) deal: partner, start_year, term_years, annual_value, total_value
- apparel deal: annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- venues / department: stadium_last_renovation_year
- coaching: mbb_hc_annual_comp, mbb_hc_contract_end, mbb_hc_pay_source_type
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Florida (SEC; Public; FL). Already known for context: stadium_name=Ben Hill Griffin Stadium; arena_name=Exactech Arena at the Stephen C. O'Connell Center; fb_hc_name=Jon Sumrall; mbb_hc_name=Todd Golden; stadium_nr_partner=Ben Hill Griffin Jr. (honoree); arena_nr_partner=Exactech; patch_partner=none.
Find these items for Florida:
- multimedia rights (MMR) deal: partner, start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: annual_value
- venues / department: stadium_last_renovation_year
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Georgia (SEC; Public; GA). Already known for context: stadium_name=Sanford Stadium; arena_name=Stegeman Coliseum; fb_hc_name=Kirby Smart; mbb_hc_name=Mike White; stadium_nr_partner=Steadman Vincent Sanford (honoree); arena_nr_partner=Stegeman (honoree); patch_partner=none.
Find these items for Georgia:
- multimedia rights (MMR) deal: partner, start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- coaching: fb_hc_annual_comp, mbb_hc_annual_comp

School: Kentucky (SEC; Public; KY). Already known for context: stadium_name=Kroger Field; arena_name=Rupp Arena at Central Bank Center; fb_hc_name=Will Stein; mbb_hc_name=Mark Pope; stadium_nr_partner=Kroger; arena_nr_partner=Central Bank; patch_partner=UK Invests; mmr_partner=other; apparel_partner=Nike.
Find these items for Kentucky:
- multimedia rights (MMR) deal: start_year, annual_value, total_value
- apparel deal: annual_value
- football stadium naming-rights deal: total_value
- basketball arena naming-rights deal: start_year, total_value
- football jersey/helmet patch deal: term_years, annual_value, total_value

School: LSU (SEC; Public; LA). Already known for context: stadium_name=Tiger Stadium; arena_name=Pete Maravich Assembly Center; fb_hc_name=Lane Kiffin; mbb_hc_name=Will Wade; stadium_nr_partner=none; arena_nr_partner=Pete Maravich (honoree); patch_partner=Woodside Energy; mmr_partner=Playfly.
Find these items for LSU:
- multimedia rights (MMR) deal: start_year, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: start_year, term_years, annual_value, total_value
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Mississippi State (SEC; Public; MS). Already known for context: stadium_name=Davis Wade Stadium at Scott Field; arena_name=Humphrey Coliseum; fb_hc_name=Jeff Lebby; mbb_hc_name=Chris Jans; stadium_nr_partner=Davis Wade (donor honoree) and Scott Field; patch_partner=none; mmr_partner=Learfield; apparel_partner=adidas.
Find these items for Mississippi State:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- venues / department: arena_capacity
- coaching: fb_hc_annual_comp, fb_hc_contract_end, mbb_hc_annual_comp, mbb_hc_contract_end, mbb_hc_pay_source_type
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Missouri (SEC; Public; MO). Already known for context: stadium_name=Faurot Field at Memorial Stadium; arena_name=Mizzou Arena; fb_hc_name=Eli Drinkwitz; mbb_hc_name=Dennis Gates; stadium_nr_partner=Faurot Field at Memorial Stadium (Don Faurot honoree); arena_nr_partner=none; patch_partner=Ambetter Health; mmr_partner=Learfield.
Find these items for Missouri:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football jersey/helmet patch deal: term_years, annual_value, total_value
- coaching: mbb_hc_annual_comp, mbb_hc_pay_source_type
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Oklahoma (SEC; Public; OK). Already known for context: stadium_name=Gaylord Family - Oklahoma Memorial Stadium; arena_name=Lloyd Noble Center; fb_hc_name=Brent Venables; mbb_hc_name=Porter Moser; stadium_nr_partner=Gaylord Family (donor honoree); arena_nr_partner=Lloyd Noble (honoree); patch_partner=none; mmr_partner=Learfield; apparel_partner=Jordan Brand.
Find these items for Oklahoma:
- multimedia rights (MMR) deal: annual_value, total_value
- apparel deal: term_years
- venues / department: stadium_last_renovation_year, arena_capacity
- coaching: mbb_hc_annual_comp, mbb_hc_contract_end, mbb_hc_pay_source_type
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Ole Miss (SEC; Public; MS). Already known for context: stadium_name=Vaught-Hemingway Stadium; arena_name=The Sandy and John Black Pavilion at Ole Miss; fb_hc_name=Pete Golding; mbb_hc_name=Chris Beard; stadium_nr_partner=Vaught and Hemingway (honorees); arena_nr_partner=Sandy and John Black (donor honorees); patch_partner=none; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Ole Miss:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: annual_value, total_value
- coaching: mbb_hc_annual_comp, mbb_hc_contract_end, mbb_hc_pay_source_type

School: South Carolina (SEC; Public; SC). Already known for context: stadium_name=Williams-Brice Stadium; arena_name=Colonial Life Arena; fb_hc_name=Shane Beamer; mbb_hc_name=Lamont Paris; stadium_nr_partner=Williams and Brice (honorees); arena_nr_partner=Colonial Life; patch_partner=none; apparel_partner=Nike.
Find these items for South Carolina:
- multimedia rights (MMR) deal: partner, start_year, term_years, annual_value, total_value
- apparel deal: annual_value
- basketball arena naming-rights deal: term_years, annual_value, total_value
- coaching: fb_hc_annual_comp

School: Tennessee (SEC; Public; TN). Already known for context: stadium_name=Neyland Stadium; arena_name=Thompson-Boling Arena at Food City Center; fb_hc_name=Josh Heupel; mbb_hc_name=Rick Barnes; stadium_nr_partner=Robert Neyland (honoree); arena_nr_partner=Food City; patch_partner=First Horizon Bank; mmr_partner=Learfield; apparel_partner=Adidas.
Find these items for Tennessee:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: annual_value, total_value
- basketball arena naming-rights deal: annual_value
- football jersey/helmet patch deal: annual_value

School: Texas (SEC; Public; TX). Already known for context: stadium_name=Darrell K Royal-Texas Memorial Stadium at Campbell-Williams Field; arena_name=Moody Center; fb_hc_name=Steve Sarkisian; mbb_hc_name=Sean Miller; patch_partner=none; mmr_partner=Learfield; apparel_partner=Nike.
Find these items for Texas:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: start_year
- football stadium naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- basketball arena naming-rights deal: partner, industry, deal_type, start_year, term_years, annual_value, total_value
- venues / department: stadium_last_renovation_year, arena_capacity
- coaching: fb_hc_annual_comp, mbb_hc_annual_comp
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Texas A&M (SEC; Public; TX). Already known for context: stadium_name=Kyle Field; arena_name=Reed Arena; fb_hc_name=Mike Elko; mbb_hc_name=Bucky McMillan; stadium_nr_partner=Edwin Kyle (honoree); arena_nr_partner=Reed (honoree); patch_partner=none; mmr_partner=Playfly; apparel_partner=adidas.
Find these items for Texas A&M:
- multimedia rights (MMR) deal: annual_value
- apparel deal: annual_value, total_value
- venues / department: varsity_sports
- NCAA MFRS / agreed-upon-procedures financial report (all 16 fields: report URL, fiscal year, total operating revenue, total operating expenses, media rights, ticket sales, contributions, NCAA distributions, conference distributions, conference bowl distributions, direct institutional support, indirect institutional support, student fees, coaching salaries line 22, total athletics-related debt line 52, debt service line 34): all fields

School: Vanderbilt (SEC; Private; TN). Already known for context: stadium_name=FirstBank Stadium; arena_name=Memorial Gymnasium; fb_hc_name=Clark Lea; mbb_hc_name=Mark Byington; stadium_nr_partner=FirstBank; arena_nr_partner=none; patch_partner=SRM Concrete; mmr_partner=Learfield.
Find these items for Vanderbilt:
- multimedia rights (MMR) deal: start_year, term_years, annual_value, total_value
- apparel deal: partner, start_year, term_years, annual_value, total_value
- football stadium naming-rights deal: annual_value, total_value
- football jersey/helmet patch deal: term_years, annual_value, total_value
- venues / department: stadium_last_renovation_year, arena_capacity
