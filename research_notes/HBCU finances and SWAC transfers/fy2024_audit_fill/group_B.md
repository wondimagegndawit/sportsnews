# Group B: FY2024 audited-statement debt figures for 11 private HBCUs that report $0 debt to IPEDS

Research date: 2026-11-28. Companion data file: `group_B.json` (one record per school, item = debt).

## How to read these notes

- Source for ten of the eleven schools is the FY2024 single-audit package filed with the Federal Audit Clearinghouse (FAC). Each PDF was downloaded from `https://app.fac.gov/dissemination/report/pdf/<report-id>` and read directly: the balance sheet, the debt and lease notes, the cash flow statement and the subsequent-events note. Page numbers are PDF page numbers, not the printed folio.
- All ten have a fiscal year ending June 30, 2024. All amounts are whole dollars as printed.
- "Long-term total" follows the brief: bonds + notes/loans/mortgages + finance leases. Lines of credit are listed separately and are not in the total. Operating lease liabilities, pension obligations and refundable federal loan advances are left out.
- Form 990 figures are a cross-check only. They come from the ProPublica Nonprofit Explorer API extract of Part X of the FY2024 Form 990 and are not audited.

## The main finding

IPEDS shows $0 debt for all eleven. The audited statements show that only one of the ten with an audit on file (Voorhees) had no borrowings of any kind at June 30, 2024. The other nine fall into three patterns:

1. New federal HBCU Capital Financing Program borrowing drawn during FY2024: Dillard, Morehouse, Tuskegee.
2. A conventional term note: Shaw, Tougaloo (small).
3. Borrowing that consists mostly or entirely of lines of credit secured by the school's investments or property: Saint Augustine's, Stillman, Jarvis Christian, Le Moyne-Owen, and also part of the debt at Shaw, Dillard and Tougaloo.

Pattern 3 is the one that needs a decision. The brief keeps lines of credit out of the long-term total, and I followed that. But four schools present those lines as long-term debt in their own audited statements, so the total under the brief is far smaller than the figure a reader will see on the school's balance sheet. Both figures are given for each school below.

## Summary table

| School | Long-term total (brief rule) | Lines of credit (separate) | Total if lines are counted | Status |
|---|---|---|---|---|
| Saint Augustine's University | $138,866 | $15,679,098 | $15,817,964 | found |
| Shaw University | $6,309,969 | $4,933,000 | $11,242,969 | found |
| Dillard University | $8,330,744 | $3,900,000 | $12,230,744 | found |
| Stillman College | $0 | $4,927,468 | $4,927,468 | found |
| Tougaloo College | $740,599 | $4,429,692 | $5,170,291 | found |
| Voorhees University | $0 | $0 | $0 | confirmed_zero |
| Jarvis Christian University | $0 | $1,918,035 | $1,918,035 | found |
| Le Moyne-Owen College | $0 | $5,124,617 | $5,124,617 | found |
| Morehouse College | $3,428,978 | $0 | $3,428,978 | found |
| Tuskegee University | $2,980,207 | $0 | $2,980,207 | found |
| Florida Memorial University | not found | not found | not found | not_found |

For Stillman, Jarvis and Le Moyne-Owen I used status "found" with value 0 instead of "confirmed_zero", because "confirmed zero" would read as "this school has no debt", and that is not what the statements show.

## School notes

### Saint Augustine's University (UNITID 199582)

- Document: FAC report 2024-06-GSAFAC-0000066734. Auditor Banks, Finley, White & Co., report dated November 17, 2024. The FY2024 audit exists and I read it.
- Balance sheet (p.6): "Long-term debt 15,817,964" (2023: 11,680,150).
- Note 8 (p.23-24): securities-based line of credit $11,504,098; Bank OZK revolving line of credit $4,175,000; auto loans $138,866; total $15,817,964.
- Brief rule: 138,866 (auto loans only). Lines of credit: 15,679,098.
- Why it needs a decision: the University labels all of it long-term debt. The securities-based line has no stated maturity and the maturity schedule puts $10,964,188 in "Thereafter". The Bank OZK line is shown as due in fiscal 2025.
- No bonds, no HBCU Capital Financing loan, no finance leases.
- Things a reader should know:
  - The auditor's report has a going-concern paragraph ("substantial doubt").
  - A prior-year material weakness, that debt receipts and payments were not recorded in the general ledger, is reported as not resolved in 2024 (p.51).
  - After year end (August 16, 2024) the University signed a credit facility with Gothic Ventures for up to $30,000,000 at 24% interest. That is not in the FY2024 balance.
  - About $12.5 million of unpaid payroll taxes with IRS liens (p.30).
  - The FY2022, FY2023 and FY2024 audits were all accepted by FAC within two weeks of each other in November 2024.
  - The supplemental ratio schedule (p.34) has debt sub-lines that do not sum to its total.
- 990 cross-check: secured mortgages and notes $15,817,964; bonds $0.

### Shaw University (UNITID 199643)

- Document: FAC report 2024-06-GSAFAC-0000364469. Auditor BDO USA, P.C., report dated March 31, 2025.
- Balance sheet (p.8): "Note payable 6,309,969"; "Line of credit 4,933,000".
- Note 6 (p.23-24): $6,500,000 promissory note signed June 28, 2023 to refinance earlier lines of credit, 6.00%, matures July 2028, secured by two buildings. Securities-based line of credit obtained February 2024, no stated maturity, balance $4,933,000.
- Brief rule: 6,309,969. Line of credit: 4,933,000. "Total debt" as printed: 11,242,969.
- Things a reader should know:
  - The University was not in compliance with the note's covenants at June 30, 2024 and obtained a waiver.
  - Finding 2024-001 (p.42): the former CFO drew on the line of credit without the knowledge of the President or Board, and the balance was not recorded in the ledger until months after year end.
  - After year end the line was raised to $6,433,000 and the Board authorized borrowing up to $14,000,000 from the endowment.
- 990 cross-check: secured mortgages and notes $11,242,969; bonds $0.

### Dillard University (UNITID 158802)

- Document: FAC report 2024-06-GSAFAC-0000363708. Auditor Sean M. Bruno CPAs, report dated June 20, 2025. The PDF is a scan with OCR text; I checked the balance-sheet page against the page image.
- Balance sheet (p.6): "HBCU capital project loan 7,981,172" (2023: 883,628); "Note payable 3,900,000" (2023: 1,755,028); finance lease liability 124,986 short-term and 224,586 long-term.
- Note 2 (p.17): on October 20, 2023 Dillard signed a Capital Project Loan Agreement under the HBCU Capital Financing Program for up to $41 million for student housing, maturing September 1, 2052. The same note says the $3,900,000 is the drawn balance on a $5,000,000 line of credit at 8.50%.
- Brief rule: 7,981,172 + 349,572 = 8,330,744. Line of credit: 3,900,000.
- Why confidence is medium:
  - The $3,900,000 is captioned "Note payable" on the balance sheet but described as a line of credit in the notes. I treated it as a line of credit. If treated as a note the total is 12,230,744.
  - The finance-lease maturity table (p.48) totals $262,841, which is the prior-year long-term balance, while the balance sheet and the ratio schedule (p.50) show $349,572. I used the balance sheet.
- 990 cross-check: unsecured notes and loans $11,881,172 (= 7,981,172 + 3,900,000); bonds $0.

### Stillman College (UNITID 102270)

- Document: FAC report 2024-06-GSAFAC-0000373448. Auditor Banks, Finley, White & Co., report dated June 24, 2025 (late; a finding notes the March 31, 2025 due date).
- Balance sheet (p.6): "Notes payable-current portion 4,927,468" (2023: 3,992,843). No noncurrent debt line.
- Note 6, titled "Long-Term Debt" (p.18): three lines of credit. UBS line secured by pledged investments $4,011,165; two ServisFirst lines opened June 14, 2024, $164,734 and $751,569.
- Brief rule: 0. Lines of credit: 4,927,468.
- No bonds, mortgages or HBCU Capital Financing loan. Lease liabilities of $82,650 are operating copier leases (excluded).
- 990 cross-check: secured mortgages and notes $4,949,965; bonds $0.

### Tougaloo College (UNITID 176406)

- Document: FAC report 2024-06-GSAFAC-0000388291. Auditor The Wesley Peachtree Group, CPAs, report dated February 19, 2025; compliance reports reissued November 20, 2025; accepted by FAC December 13, 2025. Statements are consolidated with 2 Rivers Communications, LLC (WLOO television).
- Balance sheet (p.6): notes payable 60,020 current and 660,169 long-term; finance lease obligations 14,250 current and 6,160 long-term; "Bank lines-of-credit 4,429,692" (current).
- Note 7 (p.20): two bank notes, $378,211 and $341,977, total $720,188. Note 6 (p.19): three lines of credit, $1,087,510, $3,282,641 and $59,542.
- Brief rule: 720,189 + 20,410 = 740,599. Lines of credit: 4,429,692.
- Oddities: the note text gives due dates in December 2024 and May 2025, yet $660,169 is carried as long-term. The ratio schedule (p.30) shows long-term debt of $800,619, which does not match the balance sheet. I used the balance sheet.
- 990 cross-check: secured mortgages and notes $5,149,880 (notes plus lines of credit); bonds $0.

### Voorhees University (UNITID 218919)

- Document: FAC report 2024-06-GSAFAC-0000364011. Auditor Scott and Company LLC, report dated March 31, 2025.
- Confirmed zero. The balance sheet (p.6) lists only accounts payable, accrued expenses and deferred revenue; total liabilities $2,664,812.
- What I checked: both years of the balance sheet; the cash flow statement (p.10), which shows no borrowing or repayment; all fifteen notes, none of which is a debt or lease note; the ratio schedule (p.33), which reports property "without outstanding debt for original purchase".
- Two items that are not external debt: a 2008 advance of $1,136,495 from the University's own endowment (Note 7), and $70,322 of spending listed under the USDA "Community Facilities Loans and Grants" program with no loan liability recorded.
- 990 cross-check: bonds, secured notes and unsecured notes all $0.

### Jarvis Christian University (UNITID 225885)

- Document: FAC report 2024-06-GSAFAC-0000369268. Auditor Banks, Finley, White & Co., report dated April 30, 2025.
- Balance sheet (p.6): "Line of credit 1,918,035" under current liabilities (2023: 1,943,035).
- Note 6, titled "Long-Term Debt" (p.19): a $2,000,000 line of credit from the Board of Church Extension of Disciples of Christ, secured by mortgages and deeds of trust on University real property, due on or before January 1, 2025.
- Brief rule: 0. Line of credit: 1,918,035.
- No bonds or HBCU Capital Financing loan. Lease liabilities of $564,506 are operating copier leases (excluded).
- The auditor's report notes a restatement of 2023 for lease assets and liabilities that had been left out.
- 990 cross-check: secured mortgages and notes $1,918,035; bonds $0.

### Le Moyne-Owen College (UNITID 220604)

- Document: FAC report 2024-06-GSAFAC-0000056944. Auditor The Wesley Peachtree Group, CPAs, report dated March 25, 2025 (date read from the page image; that page has no text layer).
- Balance sheet (p.6), under "Long-term Liabilities": "Bank line of credit 5,124,617" (same in 2023). Capital lease obligations print as "-".
- Note 8 (p.19): $5,200,000 line at 4.3%, secured by investments that are mostly permanently endowed funds; stated maturity November 1, 2021, extended year to year; no principal paid in 2024 or 2023; "classified as long-term given the in-substance performance of this debt".
- Brief rule: 0. Line of credit: 5,124,617.
- Why it needs a decision: this is the clearest case where the school itself classifies the line as a long-term liability.
- 990 cross-check: secured mortgages and notes $5,124,617; bonds $0.

### Morehouse College (UNITID 140553)

- Document: FAC report 2024-06-GSAFAC-0000062405. Auditor KPMG LLP, report dated November 26, 2024. Consolidated statements (College and subsidiaries).
- Balance sheet (p.5): "Bond payable, net 3,141,497" (2023: 473,037); "Obligations under finance leases 287,481"; "Margin credit facility" nil (2023: 5,000,000).
- Note 7 (p.18-19): HBCU Capital Financing Program bonds through the Rice Capital Access Program, Series A 2023-4 ($58,500,000 original issue) and Series A 2024-2 ($11,500,000), maturing 2053. Gross drawn $4,129,306 less issuance costs $987,809.
- Brief rule: 3,141,497 + 287,481 = 3,428,978. Lines of credit: 0 (margin facility repaid; new $20,000,000 Regions revolving loan undrawn).
- The balance will grow as project advances are drawn. Payments begin December 1, 2025.
- 990 cross-check: tax-exempt bond liabilities $3,141,497.

### Tuskegee University (UNITID 102377)

- Document: FAC report 2024-06-GSAFAC-0000362062. Auditor Warren Averett, LLC, report dated March 20, 2025.
- Balance sheet (p.7): "Long-term debt, net 2,980,207" (2023: nil).
- Note 6 (p.27-28): Rice Capital Access Program (HBCU Capital Financing Program) Series A 2023-6, obtained November 8, 2023, up to $35,000,000, maturing September 1, 2053. Drawn $3,831,096 less unamortized issuance costs $850,889.
- Brief rule: 2,980,207. Line of credit: $15,200,000 Regions facility with a zero balance.
- The University had no long-term debt a year earlier. Operating lease obligations of $720,881 are excluded; the University states it has no financing leases.
- 990 cross-check: no FY2024 Form 990 data was available in the ProPublica API on the research date.

### Florida Memorial University (UNITID 133979)

- Not found. No FY2024 audited statements could be located, so no figure is recorded.
- What I searched:
  - FAC API by EIN 590668483, by UEI C3B8EZBZSCP3, by name, by city (Miami Gardens) and by ZIP 33054. The latest submission is audit year 2023 (report 2023-06-GSAFAC-0000034387, accepted April 1, 2024). There is nothing for audit year 2024 or 2025. A FY2024 single audit would have been due by March 31, 2025.
  - Florida Auditor General non-profit e-file index pages and direct guesses at the file name.
  - The University website (fmuniv.edu, now resolving to fmu.edu): sitemap of 713 URLs, Finance and Administration and Controller pages, site searches for "audit" and "financial statements".
  - General web searches.
  - EMMA quick search: results are rendered by script and could not be read.
- Context only, not FY2024 figures:
  - The FY2023 audit shows no bonds or notes at June 30, 2023, only a lease liability of $720,357.
  - The FY2024 Form 990 extract shows $0 bonds, $0 secured notes and $0 unsecured notes, with total liabilities of $13,995,788. That agrees with the IPEDS $0 but is not audited.
  - The University's notice of December 19, 2025 says SACSCOC placed it on Probation for Good Cause for twelve months over financial responsibility, control of finances, and federal and state responsibilities.

## Classification choices made

- Lines of credit are kept out of the long-term total for every school, whatever the school calls them. This is the brief's rule applied uniformly.
- HBCU Capital Financing Program borrowings: Dillard's and Tuskegee's are under notes/loans as the brief directs. Morehouse's is under bonds because its audited caption is "Bond payable". The totals are not affected.
- Carrying values are net of unamortized issuance costs where the statements present them that way (Morehouse, Tuskegee).
