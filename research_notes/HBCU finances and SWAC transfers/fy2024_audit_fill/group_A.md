# Group A: FY2024 debt for 11 private HBCUs that report $0 debt to IPEDS

Prepared 2026-11-28. Companion data file: `group_A.json` (one record per school, item = debt).

## How the work was done

- Source for nine schools: the FY2024 single-audit package filed with the Federal Audit Clearinghouse (FAC). Each PDF was downloaded from `https://app.fac.gov/dissemination/report/pdf/<report-id>` and the balance sheet, cash flow statement, debt / line-of-credit / lease notes and the ED financial-responsibility schedules were read directly. Report IDs were found through the FAC API (`api.fac.gov/general`) by EIN and by name.
- Page numbers are PDF page numbers of the FAC file, not the printed page numbers.
- Paine and Livingstone print their note tables as images. Those pages were rendered and read visually; every figure taken from them reconciles to the balance sheet text.
- Form 990 data (ProPublica Nonprofit Explorer) was used only as a cross-check and is labelled as such. No 990 figure is in a `value` or `components` field.
- Two schools (Interdenominational Theological Center, Selma University) have no FY2024 audit in FAC and none could be found elsewhere. They are recorded as `not_found` with `value: null`.
- Websites `www.itc.edu` and `www.selmau.edu` returned a browser-verification challenge (HTTP 403). They were not pursued further.

## Summary

| School | Status | Long-term debt (bonds + notes + finance leases) | Line of credit (separate) | FYE | Confidence |
|---|---|---|---|---|---|
| Hampton University | found | $130,545,954 | $0 | 2024-06-30 | high |
| Bennett College | found | $66,481 | $6,472,770 | 2024-06-30 | medium |
| Clinton College | confirmed_zero | $0 | $0 | 2024-06-30 | high |
| Interdenominational Theological Center | not_found | null | null | 2024-06-30 | low |
| Morehouse School of Medicine | confirmed_zero | $0 | $0 | 2024-06-30 | high |
| Morris Brown College | confirmed_zero | $0 | $0 | 2024-06-30 | high |
| Paine College | found | $9,472,065 | $7,465,293 | 2024-06-30 | medium |
| Selma University | not_found | null | null | 2024-07-31 | low |
| Virginia University of Lynchburg | confirmed_zero | $0 | $0 | 2024-06-30 | high |
| Johnson C Smith University | confirmed_zero | $0 | $0 | 2024-06-30 | high |
| Livingstone College | found | $2,250,953 | $2,500,000 | 2024-06-30 | high |

So of the 11 IPEDS zeros: five are true zeros, four are reporting gaps with debt confirmed in the audit, and two could not be verified (both show debt on Form 990, which is not an audited source).

## Per-school notes

### Hampton University (232265): found, $130,545,954
- Document: Hampton University and Subsidiaries, Consolidated Financial Statements, June 30, 2024 and 2023; KPMG LLP; report dated December 23, 2024; FAC 2024-06-GSAFAC-0000363434.
- Balance sheet (p.5): "Bonds payable, net (note 8) 101,120,368"; "Notes payable (note 9) 29,425,586".
- Note 8 (p.21): principal $97,751,236 + unamortized premium $4,005,746 - unamortized issuance costs $636,614 = $101,120,368. Includes $84,855,000 of Virginia Small Business Financing Authority 2014 bonds and a $12,896,236 HBCU Capital Financing "Future Advance Project Funding Bond, Series A 2024-1" drawn in FY2024 (maximum $91,500,000). The 2015 VCBA series was paid off in 2024.
- Note 9 (pp.22-23): notes payable are a $4,414,235 energy-concession improvement note, a $511,351 Department of Education mortgage note, and two notes of 27th Street Hotel, LLC (58.7% owned, consolidated from June 2024): a $22,000,000 senior nonrecourse note and a $2,500,000 junior unsecured note. A multifamily note ($4,155,117) was paid off by the HBCU Capital Financing Program on June 28, 2024.
- Things to know: (a) $24.5 million of the notes belong to the hotel subsidiary and the senior note is nonrecourse; without them the University-level figure would be $106,045,954. (b) The balances quoted in the note 9 text sum to $29,398,538, which is $27,048 less than the balance sheet and maturity table ($29,425,586); the balance sheet figure is used. (c) Another $13,230,623 of HBCU Capital Financing advances came after year end (note 1(r)). (d) No finance leases, no line of credit.
- 990 cross-check (tax period 2024-06): bonds $101,120,368, secured notes $29,425,586. Agrees.

### Bennett College (197993): found, $66,481 (plus $6,472,770 line of credit shown separately)
- Document: Bennett College, Financial Statements, Supplementary Information, and Compliance Reports, Years Ended June 30, 2024 and 2023; DMJPS PLLC; report dated October 17, 2024; FAC 2024-06-GSAFAC-0000345556.
- Balance sheet (p.6): "Line of credit $6,472,770"; "Financing leases 66,481". No bonds or notes payable.
- Note 8 (p.25): finance leases for office equipment, expiring during 2025, $66,481. Note 9 (p.25): line of credit with the investment manager, secured by investments, "has no maturity date".
- Judgement call for a human: under the brief the line of credit is excluded, giving $66,481. The College's own ED financial-responsibility schedule (p.35, line 22) labels it "Line of credit for long-term purposes 6,472,770". Counting it would give $6,539,251. This is why confidence is medium.
- 990 cross-check: secured mortgages and notes $6,539,251 (= line of credit + leases). Consistent.

### Clinton College (217891): confirmed zero
- Document: Clinton College, Financial Statements for the Year Ended June 30, 2024; Martin Smith and Company CPAs PA (Greenville, SC); report dated March 28, 2025; FAC 2024-06-GSAFAC-0000364117.
- Balance sheet (p.5): liabilities are only "Accounts payable 88,664" and "Accrued expenses 341,276" (total $429,940). Cash flow (p.7): "Payments on notes payable -"; "Interest paid -0-". No debt, line-of-credit or finance-lease note.
- Operating leases were not capitalised (note 6, p.12); small.
- EIN correction: FAC and IRS list Clinton College as 57-0387838. The group list has 570387830.
- Other: ED composite score 1.3 (note 14); net assets fell $1,431,359 in FY2024.
- 990 cross-check: all debt lines zero; total liabilities $429,940. Agrees.

### Interdenominational Theological Center (140146): not found
- No FY2024 (or FY2025) audit in FAC. FAC has FY2021, FY2022 and FY2023 only; the FY2023 package (2023-06-GSAFAC-0000036018) was accepted April 1, 2024.
- Searched: FAC API by EIN 580814544 and by name for audit years 2021-2025; web searches for "Interdenominational Theological Center audited financial statements June 30, 2024" (open web and itc.edu only). The itc.edu site returned a browser-verification challenge and was not pursued.
- Evidence the audit is late or unpublished: the ATS Commission on Accrediting action letter of June 6, 2025 (https://www.ats.edu/files/galleries/2025-06_itc.pdf, read directly) places ITC on probation and requires a report by April 1, 2026 that "must include: audits for FY 2024 and FY 2025". The letter also says "the FY 2023 audit names a 'going concern'".
- Context only, not a FY2024 value: the FY2023 audit (The Wesley Peachtree Group, dated March 29, 2024; a scanned PDF read through its OCR layer) shows at June 30, 2023 a note payable of $4,908,121 (bank loan secured by endowment investments, interest-only, maturing May 2026), a line of credit of $92,675 and finance lease obligations of $131,761, with a going-concern paragraph.
- 990 cross-check (not audited): the FY2025 Form 990 shows secured mortgages and notes payable of $5,115,287 at the beginning of the year (June 30, 2024). No Form 990 for the year ending June 2024 is posted on ProPublica.
- Observation: ITC's IPEDS FY2024 endowment ($5,963,716) is within $1 of donor-restricted investments in the FY2023 audit ($5,963,717). The IPEDS FY2024 submission may have used FY2023 numbers.
- Conclusion: IPEDS $0 is very probably a reporting gap of about $5 million, but there is no audited FY2024 figure to cite.

### Morehouse School of Medicine (140562): confirmed zero
- Document: Morehouse School of Medicine, Inc., Subsidiary and Affiliate, Consolidated Financial Statements, Years Ended June 30, 2024 and 2023; BDO USA, P.C.; report dated March 27, 2025; FAC 2024-06-GSAFAC-0000359681.
- Balance sheet (p.23): liabilities are accounts payable, accrued expenses, deferred revenue, "Operating lease liabilities 28,096,680" and "Government advances for student loans 303,362". No bonds, notes or finance leases.
- Note 9 (p.44): margin line of credit, "$0 in principal and $0 in interest" outstanding. MD&A (unaudited, p.15): "MSM has no long-term debt." The MD&A five-year table (p.20) shows long-term debt of $37,373,126 in FY2020 and $2,590,143 in FY2021, nil since.
- Excluded: operating lease liabilities $28,096,680.
- EIN correction: FAC and IRS list the school as 58-1438873. The group list has 581438877.
- 990 cross-check: all debt lines zero. Agrees.

### Morris Brown College (140571): confirmed zero
- Document: Morris Brown College, Financial Statements With Independent Auditors' Report and Federal Awards, Year Ended June 30, 2024; CapinCrouse LLP; report dated January 10, 2025; FAC 2024-06-GSAFAC-0000346322.
- Balance sheet (p.5): liabilities are "Accounts payable and accrued expenses 375,092" and "Asset retirement obligation 588,740".
- Note 10 (p.20): $200,000 revolving line of credit, "balance outstanding was $0". Note 11: the former note payable was forgiven by the AME Church in FY2020.
- 990 cross-check: all debt lines zero; total liabilities $963,832. Agrees.

### Paine College (140720): found, $9,472,065 (plus $7,465,293 line of credit shown separately)
- Document: Paine College, Financial Statements as of June 30, 2024 and 2023; The Wesley Peachtree Group, CPAs; report dated March 25, 2025; FAC 2024-07-GSAFAC-0000056811.
- Balance sheet (p.6): "Notes payable 9,472,065"; "Bank line of credit 7,465,293".
- Note 11 (pp.24-25): $10,000,000 note to Capital Plus Financial, LLC dated December 29, 2021, 9.5%, through December 2031; principal $9,914,489 less unamortized debt issuance costs $442,424 = $9,472,065. Secured by substantially all property and equipment, rents, leases and investments.
- Note 12 (p.25): $7,500,000 bank line of credit, no maturity date, secured by investments (mostly permanently endowed funds), $7,465,293 outstanding at both year ends.
- Judgement call for a human: the College's own ED disclosure (pp.32-35) reports "Long-term debt - for long-term purposes - Total 16,937,358", i.e. note + line of credit. Under the brief the line is excluded ($9,472,065). This is why confidence is medium.
- Other: Emphasis of Matter on "significant cash flow constraints" (opinion not modified); a new $7,600,000 line of credit opened March 6, 2025 to pay off the old one (note 17); interest expense $1,389,282.
- 990 cross-check: unsecured notes $9,472,065; secured notes $7,465,293. Agrees.

### Selma University (102058): not found
- Fiscal year ends July 31 (Form 990 tax year August 1, 2023 to July 31, 2024), inside the FY2024 window.
- No Selma University submission exists in FAC for any audit year 2021-2025 (searched by EIN 630367461, by name and by city). Web searches (open web and selmau.edu only) found no audit document. The selmau.edu site returned a browser-verification challenge and was not pursued.
- The Form 990 says the financial statements were audited by an independent accountant, so an audit exists but is not public. It would have to be requested from the University or the Department of Education.
- 990 cross-check (not audited): at July 31, 2024, secured mortgages and notes payable $11,926 and unsecured notes and loans payable $391,031 (total $402,957); total liabilities $1,003,590.
- Conclusion: IPEDS $0 is probably a reporting gap of about $0.4 million, but there is no audited figure to cite.

### Virginia University of Lynchburg (234137): confirmed zero
- Document: Virginia University of Lynchburg, Inc., Financial Report - June 30, 2024; Accutax Bizsolutions LLC (Kalispell, MT); report dated November 29, 2024; FAC 2024-06-GSAFAC-0000364001.
- Balance sheet (p.6): "Long-term debt (Note 6) -"; total liabilities $111,049 (accounts payable and accrued expenses).
- Note 6 (p.22): "The University had no debt at June 30, 2024 and June 30, 2023 respectively." Cash flow (p.9): no debt activity in FY2024; $474,134 repaid in FY2023.
- Only month-to-month operating leases ($9,900 a year).
- Document quality: some internal inconsistencies unrelated to debt (the ED schedule on p.37 shows "Total assets 22,109,604", which is the net assets figure; balance sheet total assets are $22,220,653).
- 990 cross-check: no FY2024 Form 990 in ProPublica summary data yet.

### Johnson C Smith University (198756): confirmed zero
- Document: Johnson C. Smith University, Financial Statements, Years Ended June 30, 2024 and 2023; BDO USA, P.C.; report dated March 17, 2025; FAC 2024-06-GSAFAC-0000363926.
- Balance sheet (p.13): "Note payable -" (2023: $287,180); "Operating lease obligations 22,141,097".
- Note 8 (p.29): the Department of Education note "matured during the fiscal year ending June 30, 2024. There are no amounts outstanding as of June 30, 2024." Note 2 (p.24): $10,000,000 line of credit, entire balance available (nothing drawn).
- Flag: $22,141,097 of lease obligations for a student housing complex and a parking complex (through January 2038) are classified as operating leases in the audited statements and note 9, so they are excluded. The unaudited MD&A (p.8) calls them "finance lease obligations". The audited classification was followed.
- 990 cross-check: all debt lines zero. Agrees.

### Livingstone College (198862): found, $2,250,953 (plus $2,500,000 line of credit shown separately)
- Document: Livingstone College, Financial Statements as of June 30, 2024 and 2023; Murphy and Company, P.C., a member firm of The Wesley Peachtree Group, CPAs; report dated March 25, 2025; FAC 2024-06-GSAFAC-0000056817.
- Balance sheet (p.6): finance lease liability $1,611,786 current + $556,339 noncurrent = $2,168,125; notes payable $2,512,362 current + $70,466 noncurrent = $2,582,828.
- Note 6 (p.19): $2,500,000 revolving line of credit opened November 29, 2023, fully drawn at June 30, 2024. It sits inside "Notes payable - current portion" on the balance sheet.
- Note 7 (p.20): the only note is an automobile loan, $82,828. No bonds.
- Note 8 (pp.21-23): finance leases $2,168,125 (turf field and scoreboard $1,834,476; vehicles and office equipment $333,649).
- Arithmetic: $82,828 + $2,168,125 = $2,250,953. Adding the $2,500,000 line gives $4,750,953, which equals "Total Debt at June 30, 2024" in note 13 (p.30).
- Other: the turf-field lease had a $1.2 million balloon due July 2024 and was modified in September 2024; the line of credit matured February 2025 and was extended to May 29, 2025 (note 12). Some labelling errors in the document (cash flow heading years; p.33 total assets $15,000 higher than the balance sheet) do not affect the debt figures.
- 990 cross-check: secured mortgages and notes $2,582,828. Consistent.

## Items needing a human decision

1. Bennett College: whether the $6,472,770 no-maturity line of credit counts as long-term debt ($66,481 without, $6,539,251 with).
2. Paine College: same question for the $7,465,293 no-maturity line of credit ($9,472,065 without, $16,937,358 with; the College's own ED schedule uses the larger figure).
3. Hampton University: whether to show the consolidated figure ($130,545,954) or note that $24.5 million is debt of a 58.7%-owned hotel subsidiary, mostly nonrecourse.
4. Interdenominational Theological Center and Selma University: no audited FY2024 statements available. Decide whether to leave them as "not found" or request the audits directly from the schools. The 990 figures must not be used as audited values.
5. Johnson C Smith University: $22.1 million of operating leases for student housing and parking are outside the debt definition; decide whether a footnote is wanted.
6. EIN corrections for Clinton College (57-0387838) and Morehouse School of Medicine (58-1438873).
