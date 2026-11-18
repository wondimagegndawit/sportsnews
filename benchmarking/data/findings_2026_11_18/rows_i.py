# Part I: third research pass of 18 Nov 2026 (multimedia rights second look) and corrections found in the final review.
_CU=("Sportico via Yahoo Sports (22 Feb 2024)",'https://sports.yahoo.com/learfield-college-deals-prep-disruption-050100288.html')
_CUQ="‘The deal commits Learfield to paying Deion Sanders' employer at least $46.8 million, and possibly a lot more under shared revenue, for the next ten years through 2035.’ Sportico read the fifth amendment, obtained by public records request."
_MD=("Radio Business Report (29 Jul 2014)",'https://rbr.com/comcast-renames-university-of-maryland-arena/')
_MDQ="‘Comcast has held naming rights under a $20 million, 25-year agreement since the arena opened in 2002.’"
_WI=("UW Board of Regents, Business and Finance Committee book (9 Dec 2021)",'https://www.wisconsin.edu/regents/download/meeting_materials/2021_meeting_materials/Meeting-Book_-Business-&-Finance-Committee-(December-9,-2021).pdf')
_WIN="The agreement runs to 30 June 2029. The regents' book prints only the 2020-21 guarantee, which was a reduced figure (‘Guaranteed Payment reduced to $6,375,000’), and the escalator (‘increases by $200,000 annually’); it gives no guarantee for fiscal 2026 or 2027 and no total, so nothing is entered."
ROWS_I=[
('Colorado','mmr_start_year',2024,'2024-25 to 2034-35',*_CU,"‘The newest iteration of their MMR agreement, which kicks in for the 2024-25 season, includes both guaranteed minimums and a revenue share’."),
('Colorado','mmr_term_years',10,'2024-25 to 2034-35',*_CU,_CUQ),
('Colorado','mmr_total_value',46800000,'2024-25 to 2034-35',*_CU,_CUQ+" This is the guaranteed minimum over the ten years; Colorado also receives 65% of the first $10 million of adjusted gross revenue and 70% above that, so actual payments can be higher."),
('Maryland','arena_nr_total_value',20000000,'2002 to 2027',*_MD,_MDQ),
('Maryland','arena_nr_term_years',25,'2002 to 2027',*_MD,_MDQ),
('Maryland','arena_nr_start_year',2002,'2002 to 2027',*_MD,_MDQ),
('Wisconsin','mmr_total_value','--','2026',*_WI,_WIN),
('Wisconsin','mmr_annual_value','--','2026',*_WI,_WIN),
('Minnesota','stadium_nr_term_years','--','2026',"MPR News, Associated Press report (29 Jun 2021)",'https://www.mprnews.org/story/2021/06/29/gophers-football-home-gets-new-name-huntington-bank-stadium',"‘TCF bought the original naming rights four years before the stadium opened for $35 million, a contract that currently runs through the 2030 season.’ The workbook shows the annual payment after the 2017 revision, so no term is entered to derive a different figure."),
]
for _f,_n in (('term_years',"‘For the first time in program history, the University of Utah football team will wear a sponsorship patch on its jerseys.’ The length of the agreement is not reported."),
              ('total_value',"No value is reported. The Salt Lake Tribune (31 Aug 2026) describes the deal as ‘worth millions’ without a figure."),
              ('annual_value',"No value is reported. The Salt Lake Tribune (31 Aug 2026) describes the deal as ‘worth millions’ without a figure.")):
    ROWS_I.append(('Utah','patch_'+_f,'--','2026',"Deseret News (2 Sep 2026)",'https://www.deseret.com/sports/2026/09/02/utah-utes-football-jersey-patch-sponsor-university-of-utah-health/',_n))
