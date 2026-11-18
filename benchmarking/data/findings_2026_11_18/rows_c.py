# Part C: reasons for the remaining blank cells that follow from other cells (no new values).
_bc=("Boston College News (Oct 2025)",'https://www.bc.edu/bc-web/sites/bc-news/articles/2025/fall/gift-will-establish-the-edgerley-family-court-in-conte-forum.html')
ROWS_C=[]
for f in ('annual_value','total_value','term_years','start_year','industry'):
    ROWS_C.append(('Boston College','arena_nr_'+f,'--','2026',*_bc,"Conte Forum's name is not classified (no page read says for whom or why it is named), and no naming-rights deal is reported."))
for f in ('annual_value','total_value','term_years','start_year'):
    ROWS_C.append(('BYU','mmr_'+f,'--','2026',"BYU Athletics",'',"The holder of BYU's multimedia rights is not identified, so there are no terms to show."))
for s in ('Boston College','Duke','Stanford','Syracuse','Wake Forest','BYU','Northwestern'):
    ROWS_C.append((s,'fb_hc_pay_source_type','--','2026',"USA Today coaches' pay table",'https://sportsdata.usatoday.com/ncaa/salaries/football/coach',"No pay figure is entered for this coach (private school; not in the USA Today table), so there is no source type."))
for s in ('Boston College','Miami (FL)','SMU','Stanford','Syracuse','BYU','USC'):
    ROWS_C.append((s,'mbb_hc_pay_source_type','--','2026-27',"USA Today coaches' pay table",'https://sportsdata.usatoday.com/ncaa/salaries/mens-basketball/coach',"No pay figure is entered for this coach (private school; not in the USA Today table), so there is no source type."))
ROWS_C+=[
('USC','mbb_hc_annual_comp','--','2026-27',"USA Today coaches' pay table",'https://sportsdata.usatoday.com/ncaa/salaries/mens-basketball/coach',"USC is private and is not in the USA Today table. No page read gives Eric Musselman's pay."),
('SMU','mbb_hc_contract_end','--','2026-27',"SMU Athletics",'',"SMU is private; no report gives the length of Andy Enfield's contract."),
('Stanford','mbb_hc_contract_end','--','2026-27',"Stanford Athletics",'',"Stanford is private; reports of Kyle Smith's March 2024 hiring give no contract length."),
('USC','mbb_hc_contract_end','--','2026-27',"USC Athletics",'',"USC is private; no report gives the length of Eric Musselman's contract."),
('California','field_nr_annual_value','--','2026',"Databricks press release",'https://www.databricks.com/company/newsroom/press-releases/soda-hall-football-field-databricks-returns-berkeley-roots-cal',"The parties did not disclose the value or the term of the field naming agreement."),
('Miami (FL)','stadium_nr_annual_value','--','2026',"CDC Gaming (AP report)",'https://cdcgaming.com/dolphins-hard-rock-stadium-deal-is-for-nearly-250-million/',"Left out at my direction: Hard Rock Stadium is the Miami Dolphins' stadium, where the university plays as a tenant, so the naming deal is the Dolphins' and is not the university's."),
]
