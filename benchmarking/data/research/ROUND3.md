# Round 3 instructions (BRIEF.md rules still apply: no USA Today, no Wikipedia, clean values, URL on every valued row, qualifiers in notes)

HARD BUDGET: at most 48 WebSearch calls for you (200 per turn shared by four agents). Count them; stop searching at 48 and finish with WebFetch only (unlimited). Do not work around the limit.

Three targets only, in this priority order. Work only on the cells in your gaps3 file.

## 1. MFRS / NCAA agreed-upon-procedures reports via state transparency portals (public schools flagged "MFRS report needed: YES")
This is the highest-value target: one report fills 16 cells. Use at most 2 searches per school. Where to look (search with site: filters, then WebFetch the PDF and read the Statement of Revenues and Expenses, ALL-SPORTS TOTAL column, most recent fiscal year, FY2025 preferred, FY2024 acceptable):
- Ohio (Ohio State, Cincinnati): Auditor of State, site:ohioauditor.gov "NCAA" "agreed-upon procedures" <school>
- Texas (Texas, Texas A&M, Texas Tech): system board agendas and audit offices, site:utsystem.edu / site:tamus.edu / site:texastech.edu "NCAA agreed upon procedures"
- Florida (Florida, Florida State, UCF): site:flbog.edu or the university board of trustees audit committee materials "NCAA agreed-upon procedures"
- Alabama (Alabama, Auburn): site:ua.edu / site:auburn.edu board of trustees "NCAA" "agreed upon procedures"
- Kentucky: the trustees PDF https://www.uky.edu/trustees/sites/www.uky.edu.trustees/files/2025%20-%20University%20of%20Kentucky%20NCAA%20.pdf (try WebFetch; curl failed TLS); Louisville: site:louisville.edu "NCAA" "agreed upon"
- Mississippi (Mississippi State, Ole Miss): site:ihl.state.ms.us board book "NCAA"
- Oklahoma (Oklahoma, Oklahoma State): board of regents agendas site:ou.edu / site:okstate.edu "NCAA agreed upon procedures"
- Missouri: site:umsystem.edu "NCAA" "agreed upon procedures"
- Iowa (Iowa, Iowa State): site:iowaregents.edu "NCAA" "agreed-upon procedures" (the full AUP, not the summary)
- Kansas State: site:k-state.edu or site:kansasregents.gov "NCAA" "agreed upon procedures"
- Nebraska: site:nebraska.edu "NCAA" "agreed-upon procedures"
- Indiana, Purdue: site:iu.edu / site:purdue.edu trustees "NCAA" "agreed-upon procedures"
- Michigan, Michigan State: site:regents.umich.edu / site:trustees.msu.edu "NCAA" "agreed-upon procedures"
- Maryland: site:usmd.edu "NCAA" "agreed upon procedures"; Rutgers: site:rutgers.edu "NCAA" "agreed-upon procedures"
- UCLA, California: site:regents.universityofcalifornia.edu or site:ucop.edu "NCAA" "agreed upon procedures"
- Arizona, Arizona State: site:azregents.edu "NCAA" "agreed-upon procedures"
- West Virginia: site:wvusports.com or site:wvu.edu "agreed upon procedures" 2025 (the athletics site lists a 2024-25 AUP; find the working PDF link)
- Clemson: site:clemson.edu "NCAA" "agreed upon procedures"; North Carolina, NC State: site:northcarolina.edu or university internal audit pages "NCAA agreed-upon procedures"; Georgia Tech: site:gatech.edu "NCAA" "agreed upon procedures"; Pittsburgh: site:pitt.edu "NCAA" "agreed upon procedures"
If found, write all 16 financial rows exactly as BRIEF.md section A specifies (fin_report_url = the PDF URL; fin_fiscal_year = 2025 or 2024). If a 2-search attempt finds nothing, write nothing for financials and move on.

## 2. Varsity sports sponsored (varsity_sports)
One search per school: site:<athletics domain> "varsity sports" OR "sports programs" OR "sponsors" (the department "about" / quick facts / general information page usually states "XX varsity sports"). Record the stated number and that page's URL. If the page only lists sports, count them (men's and women's separately) and say "counted from the official sports listing" in notes.

## 3. Remaining coaching cells
Only the listed cells. For compensation use: the executed contract or term sheet posted by the school or obtained via public records, the school's announcement, or a state salary database. A press report is acceptable only if it quotes the contract's year-specific guaranteed figure for the 2026 season (football) or 2026-27 (basketball); do not report averages, prior-year figures, or figures you compute from an escalator (such rows are rejected). Contract end year = the year the current contract ends. Names: confirm the coach is in place as of November 2026 (note interim status in the value, e.g. "Jane Doe (interim)").

Output: the round-3 CSV path in your prompt, same 9-column header as BRIEF.md, append as you go. When done, reply with searches used, rows written, the schools for which you found an MFRS/AUP report (with fiscal year and URL), and what remains unsourced.
