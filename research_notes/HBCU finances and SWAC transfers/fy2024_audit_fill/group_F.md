# Group F notes: Texas public universities reporting $0 debt to IPEDS (FY ended August 31, 2024)

Item needed for all ten schools: DEBT. All documents below were opened and read directly unless stated otherwise. Machine-readable results are in `group_F.json`.

## Bottom line

None of the ten campuses records bonds payable on its own FY2024 statement of net position. In all three systems the bonds and commercial paper are issued by the Board of Regents and carried on the books of the system office. That is why IPEDS shows $0 (IPEDS Part L asks for "debt issued in the name of the institution"). It does not mean the campuses are debt-free: each one transfers money to its system for debt service, and the three Texas State University System campuses disclose the bond principal attributable to them.

What differs between the systems is whether any official FY2024 document puts a campus-level number on the system-held bonds.

| System | Bonds on campus books? | Campus-level figure for system bonds? | Audit status of the documents |
|---|---|---|---|
| University of Texas System | No. Bonds and commercial paper are on UT System Administration's statement only | None found. The audited report has no allocation by institution | System consolidated statements audited by Deloitte & Touche LLP (report dated Dec. 13, 2024). Campus statements are supplementary schedules covered by an "in relation to" opinion. Campus AFRs are unaudited |
| Texas A&M University System | No. "The associated bond liability is reported in total on the A&M System Offices financial statements" | None found | Nothing is audited. Member AFRs and the System combined AFR are stamped UNAUDITED; the System states no independent audit is obtained. Only the State Auditor's audit of the statewide ACFR exists |
| Texas State University System | No. "The associated bond liability and debt service activities are reported in total by System Administration" | Yes. Each campus AFR prints a debt service schedule for the debt "attributable to" it, "for informational purposes only" | Nothing is audited. Campus AFRs and the System combined AFR are stamped UNAUDITED; the State Auditor considers them only as part of the statewide ACFR audit |

How this is coded in the JSON:

- UT and A&M campuses: status `held_at_system_level`, value null. The campus's own small on-books items (direct-borrowing notes, state energy loans) are in `components` and `arithmetic`.
- Texas State University System campuses: status `found`, `audited=false`, value = par principal attributable to the campus from its unaudited AFR note. This is not a balance-sheet liability of the campus and excludes bond premium.

I did not allocate system debt to any campus.

## Decisions I made that the coordinator may want to change

1. GASB 87 lease liabilities. Public institutions report one "lease liability" with no finance/operating split. I reported the amounts in `arithmetic` and `caveats` but did not put them in `finance_lease_obligations` or in any total. IPEDS line 10 is "long-term debt arising from debt issuance and lease-purchase agreements", which does not clearly cover right-to-use leases. If other groups counted GASB 87 lease liabilities as finance leases, the amounts to add are: Texas A&M $133,578,998.19; East Texas A&M $11,848,936.08; A&M-Corpus Christi $74,018.67; Sam Houston $2,588,080.29; Texas State $1,539,298.04; UTEP $29,484.16. UTSA and UT Arlington cannot be split (see below).
2. A&M "Notes From Direct Borrowings" are financed purchases (ownership passes at the end of the lease). I entered them under `notes_loans_mortgages_payable` to follow the printed caption; they could equally sit under `finance_lease_obligations`.
3. Texas A&M's SECO LoanSTAR balance ($3,282,518.71) is a loan from the State Energy Conservation Office carried as an interfund payable. I included it in the notes/loans component.
4. Texas State University System campuses are coded `found` with an unaudited, par-value, off-balance-sheet figure. If the workbook should treat all three systems the same way, the alternative is `held_at_system_level` for these three as well, keeping the attributable principal as a disclosed note.

## University of Texas System

Source: The University of Texas System, FY 2024 Audited Financial Report (consolidated statements for the years ended August 31, 2024 and 2023, Independent Auditor's Report by Deloitte & Touche LLP dated December 13, 2024), 205 pages.
https://utsystem.edu/sites/default/files/documents/report-state/2024/consolidated-annual-financial-report-fy-2024/uts-fy24-and-fy23-audit-report121324final.pdf

- Auditor's report, PDF p.7: the "System Administration and Institution Financial Information" was "subjected to the auditing procedures applied in the audit of the consolidated financial statements" and is "fairly stated, in all material respects, in relation to the consolidated financial statements as a whole".
- PDF p.157: "certain balances are only reported at the consolidated level."
- PDF p.158, System Administration Exhibit A: Short-term Debt - Commercial Paper Notes 2,131,500,000.00; Revenue Bonds Payable (Current) 1,107,282,950.04; Revenue Bonds Payable (Noncurrent) 9,217,173,010.80. These equal the consolidated bonds payable on PDF p.20, so all bonds sit with System Administration.
- Note 13, PDF p.96: outstanding bonds par $9,552,880,000 (PUF $2,912,555,000; RFS $6,475,475,000; RFS-Stephen F. Austin $164,850,000). System totals only.
- No allocation of bonds by institution in Notes 10, 12, 13 or the supplementary exhibits.
- UT System Debt Overview, Feb. 19, 2025, p.2: "All U.T. System debt is issued in the name of the Board of Regents and is issued centrally on behalf of the fifteen U.T. System institutions."
  https://utsystem.edu/sites/default/files/documents/publication/2024/debt-overview/finance-debt-program-overview2025-02-19.pdf

The campus exhibits carry one combined caption, "Notes, Loans, and Leases Payable", which per the System's notes includes notes from direct borrowings, GASB 87 lease obligations and SBITA liabilities.

### The University of Texas at San Antonio (229027)
- Audited report PDF p.179: Notes, Loans, and Leases Payable 5,981,388.80 current + 10,465,298.06 noncurrent = 16,446,686.86. No bonds line.
- PDF p.181: Mandatory Transfers to System for Capital Related Debt (46,369,902.00) in FY2024.
- Could not split the caption into notes, leases and SBITA.
- Could not open UTSA's own unaudited FY2024 AFR. The old link (utsa.edu/financialaffairs/resources/docs/financial-reports/afr-fy24.pdf) returns "Page Not Found"; the UTSA Financial Reports page now links FY 2024 to a Microsoft Forms request form. An Internet Archive copy exists but the connection was reset twice from this environment; I did not pursue it further.
- Result: `held_at_system_level`, value null, confidence medium.

### The University of Texas at El Paso (228796)
- Audited report PDF p.170: Notes, Loans, and Leases Payable 248,658.52 current + 219,406.69 noncurrent = 468,065.21. No bonds line.
- PDF p.172: Mandatory Transfers to System for Capital Related Debt (31,150,113.64).
- UTEP "Annual Financial Report (With Detailed Supportive Schedules) UNAUDITED", https://www.utep.edu/vpba/_files/docs/afr-2024.pdf, PDF p.55 (Schedule B-11): Lease Liability, Current 29,484.16; Subscription Right of Use Liability 219,174.36; Subscription Right of Use Liability NC 219,406.69; total 468,065.21. So the whole caption is a small lease plus SBITA; there are no notes or loans.
- Result: `held_at_system_level`, value null; campus on-books bonds/notes/financed purchases = 0. Confidence high.

### The University of Texas at Arlington (228769)
- Audited report PDF p.161: Notes, Loans, and Leases Payable 1,751,719.51 current + 1,793,930.82 noncurrent = 3,545,650.33. Statewide Interfund Payable 121,531.65 current + 199,773.87 noncurrent = 321,305.52. No bonds line.
- PDF p.47: statewide interfund payables include $321,306 "related to the revolving loan programs administered by the Texas State Comptroller's Office". UTA is the only campus exhibit with this caption, and the amounts match, so this appears to be a state revolving loan to UTA. That link is my inference from matching totals; no sentence names UTA.
- PDF p.163: Mandatory Transfers to System for Capital Related Debt (37,539,830.41).
- UTA posts only its three primary statements (8 pages, no notes): https://resources.uta.edu/budgets-planning-and-analysis/files/financial-reports-surveys/fy24-financial-statements.pdf. Same figures as the audited schedule. No report with supporting schedules found, so the caption could not be split.
- Result: `held_at_system_level`, value null, confidence medium.

Not found for UT: the System's "Analysis of Financial Condition" for FY2024 (searched utsystem.edu document pages and Board of Regents Finance and Planning Committee agenda books for February and May 2025; the UTSA-hosted copy sfc-fy24.pdf returns Page Not Found).

## Texas A&M University System

Sources (all UNAUDITED):
- Member AFRs, 19 pages each, statements only: https://assets.system.tamus.edu/files/budgets-acct/pdf/afr/FY2024{tsu|tamu|tamuc|tamucc}.pdf (linked from https://www.tamus.edu/budgets/budgets-and-accounting/reports/statutory-reports/annual-financial-reports/)
- System combined AFR with notes, 155 pages: https://assets.system.tamus.edu/files/budgets-acct/pdf/afr/FY2024tamuscombo.pdf
- "Unaudited Letter", Nov. 20, 2024: https://assets.system.tamus.edu/files/budgets-acct/pdf/afr/FY2024unaudltr.pdf. "The State Auditor expresses an opinion on the financial statements of the State of Texas but not on the financial statements of the individual component units of the State."
- RFS Continuing Disclosure Annual Report, Feb. 21, 2025, PDF p.12: "No independent audit in support of this detailed review is required or obtained by the A&M System." https://assets.system.tamus.edu/files/treasury/pdf/RFS_Continuing_Disclosure_Annual_Report_FY24.pdf
- Outstanding Indebtedness as of August 31, 2024 (by bond series only; total principal $5,176,584,000): https://assets.system.tamus.edu/files/treasury/pdf/Outstanding_Indebtedness_2024-08-31.pdf

Combined AFR Note 6, PDF p.75: "The associated bond liability is reported in total on the A&M System Offices financial statements." No allocation to members in Note 5, Note 6, Schedules 2A-2F, the System Offices AFR, or the continuing disclosure report.

### Tarleton State University (228529)
- Member AFR PDF p.4-5: no bonds, notes, direct-borrowing, lease or subscription liability line at all.
- PDF p.12: Intrasystem Transfers for Capital Debt (Mandatory) (37,909,398.00); Transfer of Capital Debt Proceeds From System 19,572,393.35.
- Result: `held_at_system_level`, value null; campus on-books debt 0.

### Texas A&M University-College Station (228723)
- Member AFR PDF p.5: Notes From Direct Borrowings 196,663.01 + 49,925.44 = 246,588.45. Interfund Payable 1,178,919.44 + 2,103,599.27 = 3,282,518.71, identified as "SECO LoanSTAR" in combined AFR Note 12 (PDF p.103). Lease Liability 8,403,935.56 + 125,175,062.63 = 133,578,998.19. Subscription liability 5,697,333.69 + 4,507,724.97 = 10,205,058.66.
- PDF p.12: Intrasystem Transfers for Capital Debt (Mandatory) (204,828,813.07).
- The member AFR covers "Texas A&M University" (agency 711). Galveston and the Health Science Center file separately; check the IPEDS unit's scope.
- Result: `held_at_system_level`, value null; notes/loans component $3,529,107.

### East Texas A&M University (224554)
- FY2024 report is titled Texas A&M University-Commerce (same member code, agency 751).
- Member AFR PDF p.5: Notes From Direct Borrowings 583,760.84 + 5,278,840.19 = 5,862,601.03. Lease Liability 1,487,206.06 + 10,361,730.02 = 11,848,936.08.
- PDF p.12: Intrasystem Transfers for Capital Debt (Mandatory) (17,101,590.31).
- Result: `held_at_system_level`, value null; notes/loans component $5,862,601.

### Texas A&M University-Corpus Christi (224147)
- Member AFR PDF p.5: Notes From Direct Borrowings 335,680.69 + 4,962,089.12 = 5,297,769.81. Lease Liability 17,550.35 + 56,468.32 = 74,018.67. Subscription liability 282,992.45 + 587,970.50 = 870,962.95.
- PDF p.12: Intrasystem Transfers for Capital Debt (Mandatory) (29,695,731.53).
- Result: `held_at_system_level`, value null; notes/loans component $5,297,770.

## Texas State University System

Sources (all UNAUDITED):
- System Combined AFR, transmittal Nov. 19, 2024: https://docs.gato.txst.edu/713419/Annual%20Financial%20Report%20Combined%202024.pdf. PDF p.2: the report "will be considered for audit by the state auditor as part of the audit of the State of Texas Annual Comprehensive Financial Report (ACFR); therefore, an opinion has not been expressed". PDF p.9: Revenue Bonds Payable 97,380,000.00 current + 1,307,375,000.00 noncurrent = 1,404,755,000.00; unamortized premiums 7,598,045.35 + 130,530,614.48; short-term debt (commercial paper) 14,248,000.00. PDF p.40, Note 6: "The associated bond liability and debt service activities are reported in total by System Administration."
- Continuing disclosure tables FY2024 (system debt service only, no component split): https://docs.gato.txst.edu/725029/Continuing%20Disclosures%20Tables%20FY%202024.pdf

### Sam Houston State University (227881)
- AFR: https://www.shsu.edu/offices-departments/controller/documents/fy24-shsu-afr.pdf (the older /dept/controller/ link is dead).
- PDF p.42-43, Note 6: debt attributable to SHSU, principal total $471,380,300.00; interest $201,575,497.19. The table is an image; I read it from a rendered page and checked that the ten rows sum to the total.
- PDF p.42: "Notes And Loans Payable: None." PDF p.41: no short-term debt activity.
- PDF p.23-24: no bonds line. Right to Use Lease Obligations 192,260.58 + 2,395,819.71 = 2,588,080.29; Subscription Obligations 2,608,570.25 + 4,602,979.76 = 7,211,550.01.
- Schedules 2A-2F (bond schedules) are marked "Schedule Not Used".
- Result: `found`, $471,380,300, audited=false, confidence medium.

### Lamar University (226091)
- AFR: https://secure-resources.lamar.edu/_files/documents/finance-operations/afr_booklet_fy_2024.pdf
- PDF p.26, Note 6: debt attributable to Lamar, principal total 87,495,000.00; interest 18,533,358.89. Rows sum to the total.
- PDF p.9: no bonds, notes or lease liability line. PDF p.24: no short-term debt. PDF p.26: no operating or capital leases above the threshold.
- PDF p.5: "will be audited by the State Auditor as part of the audit of the State of Texas [ACFR]; therefore, an opinion has not been expressed".
- Result: `found`, $87,495,000, audited=false, confidence medium.

### Texas State University (228459)
- AFR: https://docs.gato.txst.edu/718025/FY%202024%20Annual%20Financial%20Report.pdf
- PDF p.39, Note 5: debt attributable to Texas State, principal total $550,400,000.00; interest $308,774,121.98. Rows sum to the total.
- PDF p.29-30, Note 1: "the associated bond liability is reported in total by the TSUS administration and is not included in the liabilities of the university on its financial statements."
- PDF p.13: no bonds or notes line. Right to Use Lease Obligation 292,212.29 + 1,247,085.75 = 1,539,298.04.
- PDF p.26: "The State Auditor expresses an opinion on the ACFR, but not on the financial statements of individual state agencies or universities contained therein."
- Result: `found`, $550,400,000, audited=false, confidence medium.

The three campuses total $1,109,275,300 of the System's $1,404,755,000 revenue bond par; the rest relates to components outside this group.

## What I searched and did not use
- Federal Audit Clearinghouse: not searched; these campuses are part of the State of Texas reporting entity and have no separate single audit.
- EMMA: not searched directly; I used the systems' own posted continuing disclosure reports, which are the EMMA filings.
- Texas Bond Review Board and THECB data: seen in search results, not used; they are not the systems' financial statements.
- IPEDS definition check: OMB-hosted IPEDS Finance package 2024-25, GASB instructions, Part A line 10 and Part L.
