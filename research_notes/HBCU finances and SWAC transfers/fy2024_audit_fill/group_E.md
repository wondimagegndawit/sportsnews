# Group E notes: FY2024 audited-statement fill-ins

Work date: 2026-11-28. Companion files: `group_E.json` (13 records), `group_E_uc_endowment.json` (7 records).

How to read this: every figure below was read by me from the named document unless it says otherwise. Page numbers are PDF page numbers. "Unaudited" means the document itself says so.

## Summary

| School | Item | Status | Value | FYE | Audited? | Confidence |
|---|---|---|---|---|---|---|
| UC Berkeley | Debt | held_at_system_level | none recorded | 2024-06-30 | system only | medium |
| UCLA | Debt | found (unaudited campus report) | $6,227,866,000 | 2024-06-30 | No | low |
| UC Davis | Debt | held_at_system_level | none recorded | 2024-06-30 | system only | medium |
| UC Irvine | Debt | held_at_system_level | none recorded | 2024-06-30 | system only | medium |
| UC Riverside | Debt | held_at_system_level | none recorded | 2024-06-30 | system only | medium |
| UC San Diego | Debt | found (unaudited campus schedule) | $6,126,770,000 | 2024-06-30 | No | medium |
| UC Santa Barbara | Debt | held_at_system_level | none recorded | 2024-06-30 | system only | medium |
| Colorado Boulder | Endowment | held_at_system_level | none recorded | 2024-06-30 | system and foundation | high |
| Missouri State | Endowment | found | $126,270,574 | 2024-06-30 | Yes | medium |
| Air Force Academy | Debt | not_applicable_federal | none | 2024-09-30 | n/a | medium |
| Military Academy | Debt | not_applicable_federal | none | 2024-09-30 | n/a | medium |
| Military Academy | Endowment | found (alumni association only) | $420,451,000 | 2023-12-31 | Yes | medium |
| Naval Academy | Debt | not_applicable_federal | none | 2024-09-30 | n/a | medium |

## University of California: debt (seven campuses)

### What the audited statements show
- Document: University of California Annual Financial Report 2023-24, https://www.ucop.edu/uc-controller/financial-reports/systemwide-reports/annual-financial-reports/23-24/annual-financial-report-2024.pdf (129 PDF pages). Auditor PricewaterhouseCoopers LLP, report dated November 18, 2024 (p. 33).
- Debt is reported for the University as a whole. Statements of net position (p. 34, thousands): commercial paper 1,587,500; current portion of long-term debt 3,113,605; long-term debt 33,208,243. Note 13 Table 13.1 (p. 79): total outstanding debt 37,909,349, of which UC revenue bonds 30,481,462, financing obligations 64,893, other University borrowings 807,504, leases 2,519,174, SBITAs 236,471, blended component unit revenue bonds 2,212,345.
- There is no schedule of debt by campus anywhere in the report. "Campus Facts in Brief" (pp. 10-11) is labelled unaudited and has no debt line.
- The single audit is also one report for the system: the FY2024 Uniform Guidance report cover lists every campus EIN (https://www.ucop.edu/uc-controller/financial-reports/systemwide-reports/a133/2024report.pdf).
- I did not allocate system debt to any campus.

### Campus by campus
- **UCLA (found, unaudited).** UCLA Annual Financial Report 2023-2024, https://ucla.box.com/v/acct-pdf-AFR-23-24 (linked from https://finance.ucla.edu/corporate-accounting/ucla-annual-financial-reports). Statement of Net Position (Unaudited), p. 27, thousands: commercial paper 20,456; current portion of long-term debt 682,638; long-term debt 5,545,228. Sum of the two long-term lines: 6,227,866. With commercial paper: 6,248,322, agreeing with the MD&A's "$6,248 million" (p. 13).
  - The cover and p. 3 say the information is unaudited and prepared by management. The document says debt is kept centrally by the UC Office of the President and that UCLA uses estimates to allocate it. FY2023 was restated for methodology changes.
  - The PDF now posted was generated on 2026-04-04, so it is a later edition of the 2023-24 report.
  - No breakdown into bonds, notes and leases. The same caption in the audited system statements includes leases and SBITAs, so this number is probably wider than the IPEDS-style definition. It includes the medical center.
- **UC San Diego (found, unaudited).** Detailed Financial Schedules for Fiscal Year 2024, https://blink.ucsd.edu/_files/finance-tab/FY24%20UCSD%20Detailed%20Financial%20Schedules.pdf (listing page: https://blink.ucsd.edu/finance/resources-training/calendar-schedules/schedules-deadlines/dd-detailed-financial-schedules.html, which says the schedules "are intended for internal use and are not audited").
  - Statement of net position (p. 14, thousands): current portion of long-term debt 430,500; long term debt 5,736,403; sum 6,166,903.
  - Debt schedules (pp. 42-49) give the same total, 6,166,903, split as: recorded at campus 3,449,300 (capital lease obligations 30,196; finance lease ROU obligations 167,513; SBITA 40,133; revenue bonds 1,224,213; central bank loans 1,933,551; third-party debt 53,694) and recorded at UCOP 2,717,603 (mortgages and other borrowings 152,747; revenue bonds 2,564,856).
  - Brief-definition total: bonds 3,789,069 + notes/loans 2,139,992 + finance leases 197,709 = 6,126,770 (SBITA 40,133 excluded).
  - Judgment calls: "central bank loans" are internal UC loans; the UCOP "mortgages and other borrowings" lines are prefixed "CP" and may be commercial-paper interim financing; lease obligations are GASB 87 liabilities that the document calls finance leases. Includes the medical center.
- **UC Berkeley (no figure recorded).** A campus document "UC Berkeley Annual Financial Statements 2023-24" (unaudited) has existed at https://controller.berkeley.edu/sites/default/files/2023-24_ucb_annual_financial_statements.pdf, but the file returned HTTP 404 and the listing page https://controller.berkeley.edu/uc-berkeley-financial-reports-unaudited returned "Access denied. You are not authorized to access this page." The 2022-23 file is also 404. Lead only, NOT verified and not to be used as a figure: search-engine summaries of the removed PDF describe long-term debt of roughly $2.41 billion plus a current portion of roughly $181 million at June 30, 2024.
- **UC Davis (no figure recorded).** Davis publishes its annual report as web pages with a Tableau dashboard: https://afs.ucdavis.edu/finance/accounting-financial-reporting/annual-report/snp-new (mirror host financeandbusiness.ucdavis.edu). Both hosts returned HTTP 403 (Cloudflare block) to direct requests and to the fetch tool; I did not try to get around it. Lead only, NOT verified: search-engine summaries say the page covers "UC Davis campus and UC Davis Medical Center" and shows FY2024 long-term debt of about 4,264 plus a current portion of about 182 (apparently millions). A person with a browser can read it in a minute.
- **UC Irvine, UC Riverside, UC Santa Barbara (no campus document found).** Searched: accounting.uci.edu (Campus Financial Reports pages are internal ledger tools), budgetoffice.uci.edu; accounting.ucr.edu, bfs.ucr.edu/finance-reports, fpa.ucr.edu/campus-financial-information; bfs.ucsb.edu (Controller, General Accounting), bap.ucsb.edu; plus web searches for "<campus> annual financial report 2023-24", "financial schedules", "statement of net position", "long-term debt". The old UCOP "campus financial schedules" URLs (ucop.edu/uc-controller/financial-reports/campus-financial-schedules/...) return 404, and finreports.universityofcalifornia.edu could not be reached (connection reset). Only the three campus foundations' audited statements turned up, which do not carry campus debt.

## University of California: endowment by campus (added request)

Question: does each UC campus have its own endowment, and what do the IPEDS figures represent?

Finding: for all seven campuses the IPEDS FY2024 endowment figure equals, to the thousand, the **campus foundation's** endowment as printed in the UC annual report's unaudited "Campus Financial Facts" table. It does not include the endowment that The Regents hold for the campus, which is the larger part for four of the seven campuses (Berkeley, Los Angeles, Davis, Riverside).

Source: UC Annual Financial Report 2023-24, "Campus Facts in Brief (Unaudited)", PDF pp. 10-11, thousands of dollars. Sums are mine; the table prints the two component lines only.

| Campus | Regents-held (nonspendable + other) | Campus foundation (nonspendable and gifts + other) | Both together | IPEDS | IPEDS equals |
|---|---|---|---|---|---|
| Berkeley | 430,078 + 4,440,052 = 4,870,130 | 1,879,882 + 1,296,224 = 3,176,106 | 8,046,236 | 3,176,106 | foundation only |
| Los Angeles | 337,290 + 3,781,970 = 4,119,260 | 2,102,256 + 1,427,289 = 3,529,545 | 7,648,805 | 3,529,545 | foundation only |
| Davis | 136,056 + 1,489,802 = 1,625,858 | 432,193 + 341,024 = 773,217 | 2,399,075 | 773,217 | foundation only |
| Irvine | 13,665 + 575,677 = 589,342 | 529,542 + 369,814 = 899,356 | 1,488,698 | 899,356 | foundation only |
| Riverside | 16,707 + 494,833 = 511,540 | 154,110 + 122,972 = 277,082 | 788,622 | 277,082 | foundation only |
| San Diego | 63,240 + 1,323,691 = 1,386,931 | 783,818 + 773,997 = 1,557,815 | 2,944,746 | 1,557,815 | foundation only |
| Santa Barbara | 37,617 + 184,472 = 222,089 | 213,479 + 230,565 = 444,044 | 666,133 | 444,044 | foundation only |

Checks made:
- Foundation audited statements (all PwC, dated September 20, 2024) agree with the foundation column for the four I could open: Irvine prints "Total endowments $899,356,518" (p. 20); Riverside 154,110,350 + 104,913,387 + 18,058,803 = 277,082,540 (p. 10); San Diego 783,818 + 477,347 + 296,650 = 1,557,815 thousand (p. 9); Santa Barbara 213,479 + 116,740 + 113,825 = 444,044 thousand (p. 11).
- Berkeley and Davis foundation sites returned HTTP 403; UCLA Foundation audited statements were not located. For UCLA, the unaudited campus report's foundations column shows nonexpendable 2,102,256, which agrees.
- The University nonspendable line sums across all campuses and systemwide to 1,316,568, the audited statement-of-net-position figure for "Restricted: Nonexpendable: Endowments and gifts".
- UC San Diego's own unaudited schedules show "Endowment funds held at UCOP 1,386,932", agreeing with the Regents-held figure.

A second official document gives different numbers on a different basis: UC Annual Endowment Report, fiscal year ended June 30, 2024 (prepared by Mercer for UC Investments, unaudited market values), https://www.ucop.edu/investment-office/investment-reports/annual-reports/annual-endwoment-report-fy-2023-2024.pdf, section 3.2, p. 7, $ thousands:

| Campus | Regents | Foundation in GEP | in BGP | in STIP | Foundation | Total endowment assets |
|---|---|---|---|---|---|---|
| Berkeley | 5,768,629 | - | - | 16,169 | 3,096,139 | 8,880,937 |
| Davis | 1,615,705 | 623,867 | - | 14,331 | 132,203 | 2,386,106 |
| Irvine | 1,823,060 | 341,041 | - | 1,564 | 556,752 | 2,722,417 |
| Los Angeles | 5,492,353 | 10,153 | - | 19,515 | 4,268,950 | 9,790,971 |
| Riverside | 1,012,876 | 271,750 | 490 | 364 | 2,032 | 1,287,513 |
| San Diego | 1,430,363 | 1,085,828 | - | 2,556 | 500,528 | 3,019,275 |
| Santa Barbara | 646,130 | 411,821 | - | 10,587 | 5,966 | 1,074,503 |

Why the two differ: the endowment report's "Regents" column is everything the Regents manage in the General Endowment Pool and Blue & Gold Pool for the campus, which is wider than the annual report's "University endowments"; its foundation figures are investment market values supplied by each foundation. None of its figures match IPEDS.

Plain answer: each campus has two pools working for it. One is legally an asset of The Regents (the system) and is designated for the campus. The other belongs to the campus's own foundation, a separate nonprofit. IPEDS shows only the second.

## University of Colorado Boulder: endowment
- No official Boulder-only endowment figure exists in the audited documents. Status held_at_system_level; nothing allocated.
- CU system Annual Financial Report FY2024, https://www.cu.edu/doc/fy2024-cu-afrpdf-1 (Forvis Mazars, LLP, December 5, 2024): p. 16 says most endowment assets are held by the CU Foundation; p. 28 shows restricted nonexpendable (endowments) 49,212 thousand for the whole University; p. 100 says the University has endowments and other assets held by the CU Foundation of about $258,303,000.
- CU Foundation consolidated financial report, June 30, 2024 (Plante & Moran, PLLC, October 17, 2024), Note 12, pp. 24-25: total managed endowments $2,245,165,855, including University custodial endowments $258,302,711; Foundation endowment net assets $1,986,863,144. No campus split. Read from the Colorado State Auditor's repository because the Foundation's site lists only its latest year: https://s3.us-east-2.amazonaws.com/lg.colorado.gov/published_audits/2024/8322.00%20University%20of%20Colorado%20Foundation%2C%20Inc..pdf
- CU Unaudited Supplement to the Annual Financial Report, June 30, 2024, https://www.cu.edu/doc/supplementals-fy2024pdf-1: the Boulder statement of net position (pp. 11-12) has no endowment fund column; the endowment fund sits under System Administration (pp. 32-33: total net position 337,773,963.87; nonexpendable 49,212,544.89). The Boulder long-term debt line there, 987,440,374.30, equals the IPEDS debt figure, so IPEDS for Boulder appears to come from this supplement.
- Searched for a Boulder-specific figure on cu.edu, colorado.edu and giving.cu.edu; third-party "CU Boulder endowment" numbers were ignored.

## Missouri State University: endowment
- University report (Forvis Mazars, LLP, December 5, 2024): https://www.missouristate.edu/FinancialServices/_Files/FY24MSUUnivReportRevised0325.pdf. Statements of net position pp. 14-15: "Due from Foundation $6,199,762"; restricted nonexpendable net position 6,199,762. Note 15, p. 48: the University's endowment fund ($199,762 in 1982, plus $6,000,000 of Department of Education endowment grants in 2023) was transferred to the Foundation for management; earnings are recorded in the Foundation's books.
- Foundation report (Forvis Mazars, LLP, December 5, 2024): https://www.missouristate.edu/FinancialServices/_Files/MSU_Foundation_2024_Audit_Report.pdf. Note 5, p. 14: total endowment funds $120,070,812 (donor-restricted 116,814,419; board-designated 3,256,393). Statement of financial position, p. 5: "Funds managed for Missouri State University 6,199,762" as a liability.
- Recorded: institution-owned 6,199,762; foundation 120,070,812; total 126,270,574 (my addition).
- Cautions: the notes do not say whether earnings on the University's funds are inside the Foundation's endowment net assets, so a small overlap cannot be excluded. The audited entity includes the West Plains campus. The University file is a March 2025 re-posting with an immaterial revision to a 2023 disclosure.

## Service academies
- Debt, all three: not_applicable_federal. Federal Audit Clearinghouse searches by EIN (311575142, 141364902, 973806000) returned "No results found". Name searches returned only separate nonprofits (Air Force Academy Athletic Corporation; Army West Point Athletic Association, Inc.) or nothing (Naval Academy).
- I could not open department-level financial reports to quote them: asafm.army.mil, comptroller.defense.gov and gao.gov returned HTTP 403. The records therefore carry a plain statement of what was searched, not a citation.
- West Point endowment: the Academy has no audited endowment of its own. The West Point Association of Graduates, a separate private nonprofit, reports endowment net assets of $420,451 thousand at December 31, 2023 (Note 15, p. 25; $20,338 thousand without and $400,113 thousand with donor restrictions). Report: https://westpointaog.org/wp-content/uploads/2024/06/West-Point-Association-of-Graduates-Audit-Report-12-31-23.pdf, auditor's report dated May 2, 2024; auditor Baker Tilly US, LLP per the release memo. Its year-end is December 31; the 2023 year-end is the one inside the brief's FY2024 window.
- Not examined or not found: the Academy's federally held gift funds; Army West Point Athletic Association; the Air Force and Navy alumni organizations (endowment was not requested for those two).

## Needs a human decision
1. UCLA and UC San Diego debt: accept unaudited campus figures or show "held at system level" for all seven campuses for consistency. The two figures are not on the same basis as each other (UCLA includes SBITAs and all leases; the San Diego figure excludes SBITAs) and both include medical centers.
2. UC Berkeley and UC Davis debt: campus figures appear to exist but I could not open the documents. Someone with browser access should read the Davis page and ask Berkeley's Controller for the 2023-24 statements.
3. UC endowment: whether to show the IPEDS (foundation-only) figure, the Regents-held figure, or both, and which document's basis to use.
4. West Point endowment: whether an independent alumni association's endowment should be shown against a federal academy at all, and if so whether December 31, 2023 is the right date.
5. Missouri State: whether to use the combined $126,270,574 or the Foundation-only $120,070,812.
6. Colorado Boulder: leave blank with a note, or ask CU or the CU Foundation for a Boulder share.
