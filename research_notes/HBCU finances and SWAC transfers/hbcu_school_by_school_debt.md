# HBCU school-by-school institutional debt (SWAC first, then wider HBCU set)

Research date: 2026-11-27. All figures are institutional debt (bonds, notes/loans, HBCU Capital Financing loans, lease/financed-purchase obligations). No student-loan debt is included anywhere. Pension, OPEB, compensated absences and (unless stated) subscription-IT liabilities (SBITA) and FASB operating leases are excluded.

Working definition used for every "core debt" figure below: bonds payable (net of premium/discount as carried on the balance sheet) + notes/loans payable + drawn lines of credit + lease / finance-lease / financed-purchase / installment obligations. Components are listed per school so a different definition can be re-computed.

Source tiers (stated per row):
- AUDIT = taken by me directly from the audited (or, for Prairie View, unaudited campus) financial statements PDF.
- 990 = IRS Form 990 Part X balance-sheet lines 20/23/24 (tax-exempt bonds, secured mortgages/notes, unsecured notes) via ProPublica Nonprofit Explorer API.
- IPEDS = NCES IPEDS Finance FY2024 provisional file (F2324_F1A fields F1A07+F1A10 for public/GASB; F2324_F2 field F2A03A for private/FASB), self-reported by the institution.

---

## Key Question 1: For each school, what is total long-term debt / bonds and notes payable outstanding at the latest fiscal year end?

### Takeaway
All 12 SWAC members have a public figure: 10 at FY2025 and 2 (Grambling, Southern) at FY2024, ranging from about $2.8M (Grambling, leases only) to about $134.6M (Alabama State, after an $88.7M bond issue in June 2025). Beyond the SWAC I collected audited FY2025 figures for 37 more HBCUs, plus Form 990 or IPEDS FY2024 figures for 30 others (79 institutions in total); Howard ($899.9M) is an extreme outlier.

### Cited Findings

#### A. SWAC members (12 of 12 found)

| School | Core debt | What it includes | Fiscal year end | Level | Tier / Source |
|---|---|---|---|---|---|
| Alabama A&M | $86,621,372 | "Loans payable": HBCU Capital Financing program loans via Rice Capital Access Program (incl. Series A 2024-4 future-advance bond, up to $157M facility still being drawn) plus a land loan. Balance was $73,285,311 at 9/30/2024. | 9/30/2025 | University | AUDIT - [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-09-GSAFAC-0000422111) |
| Alabama State | $134,634,312 | Revenue bonds net $131,897,018 (Series 2022 $35.85M + new Series 2025 $88.725M + premium $7.32M) + note payable $245,000 + lease liability $2,492,294. SBITA $2,409,376 excluded (MD&A states "debt outstanding of $137 million" including it). | 9/30/2025 | University | AUDIT - [ASU FY2025 statements](https://www.alasu.edu/administration/business-and-finance/financial-statements-fy2025.pdf) |
| Alcorn State | $39,442,005 | EBC Series 2016 bonds $36,685,000 + unamortized premium $2,647,060 + lease liability $109,945. | 6/30/2025 | Campus column within Mississippi IHL system audit | AUDIT - [IHL FY2025 audit](https://www.mississippi.edu/sites/default/files/ihl/files/2025%20Audited%20Financial%20Statements%20032626.pdf) |
| Arkansas-Pine Bluff | $40,950,929 | Bonds $27,055,000 + premium $1,678,682 + installment contracts $11,809,794 + inter-system ERP loan $407,453. SBITA $572,508 excluded (balance-sheet total incl. SBITA is $41,523,437). | 6/30/2025 | Campus column within UA System audit | AUDIT - [UA System FY2025 audit, Arkansas Legislative Audit](https://www.arklegaudit.gov/downloadReport.php?id=EDHE14125) |
| Bethune-Cookman | $89,026,374 | "Long-term debt": HBCU Capital Financing loans Series A 2021-2 (refunding 2010 bonds), 2021-3 (lease refinancing), 2021-4 (new money). Was $92,617,760 at 6/30/2024. Operating lease liabilities $2,254,184 excluded. | 6/30/2025 | University (private) | AUDIT - [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412000) |
| Florida A&M | $55,801,381 | Capital improvement debt payable $55,249,283 (Series A 2024-1 HBCU Capital Financing bond, secured by housing revenues; was only $2,449,252 at 6/30/2024) + leases payable $552,098. SBITA $12,137,278 excluded. | 6/30/2025 | University only (component units excluded) | AUDIT - [Florida Auditor General Report 2027-013](https://flauditor.gov/pages/pdf_files/2027-013.pdf) |
| Grambling State | $2,813,563 | Lease obligations only ($973,987 current + $1,839,576 noncurrent). No bonds or notes payable in the Grambling column. Blended component unit Black and Gold Facilities, Inc. shows no long-term liabilities. | 6/30/2024 (FY2025 not found) | Campus column within UL System audit | AUDIT - [UL System FY2024 audit, LLA](https://lla.la.gov/publicreports.nsf/0/ceaac10dcadb296d86258c030070835f/$file/0000895c.pdf) |
| Jackson State | $82,028,463 | EBC bonds $72,890,000 (Series 2017A $24.215M, 2021A $42.38M, 2021B $6.295M) + lease liability $9,138,463. SBITA $204,070 excluded. | 6/30/2025 | Campus column within Mississippi IHL system audit | AUDIT - [IHL FY2025 audit](https://www.mississippi.edu/sites/default/files/ihl/files/2025%20Audited%20Financial%20Statements%20032626.pdf) |
| Mississippi Valley State | $13,500,850 | EBC Series 2015 bonds $13,415,000 + lease liability $85,850. SBITA $74,535 excluded. | 6/30/2025 | Campus column within Mississippi IHL system audit | AUDIT - [IHL FY2025 audit](https://www.mississippi.edu/sites/default/files/ihl/files/2025%20Audited%20Financial%20Statements%20032626.pdf) |
| Prairie View A&M | $10,781,813 | "Notes from direct borrowings" ($705,300 current + $10,076,513 noncurrent). Campus-level only: Texas A&M System Revenue Financing System / PUF bonds issued for PVAMU projects are carried on the System's books and are NOT in this figure. | 8/31/2025 | Campus (UNAUDITED member AFR) | AUDIT-tier document but unaudited - [PVAMU FY2025 AFR](https://assets.system.tamus.edu/files/budgets-acct/pdf/afr/FY2025pvamu.pdf) |
| Southern University (Baton Rouge campus) | $18,688,760 | Finance purchase obligations $17,699,143 (the building financing tied to SU System Foundation revenue bonds) + notes payable $989,617 (drawn portion of HBCU Capital Financing Series A 2021-5/2021-6 loans, up to $69M authorized). System-wide total is $21,127,077 (adds $1,165,857 finance purchase at another campus and $1,272,460 lease liability). | 6/30/2024 (FY2025 not found) | Campus column; system total also given | AUDIT - [SU System FY2024 annual financial report, LLA](https://app.lla.la.gov/publicreports.nsf/0/ff59d2e8e84a231d86258d63006ccacf/$file/000095aaa.pdf) |
| Texas Southern | $130,948,673 | Revenue bonds payable, net $130,479,303 ($7,712,468 current + $122,766,834 noncurrent; principal outstanding $118,990,000 across Series 2016 $35.925M, 2021 refunding $8.635M, 2023 $74.43M) + lease liability $469,370. | 8/31/2025 | University (state agency) | AUDIT - [TSU FY2025 audited AFR](https://www.tsu.edu/about/administration/finance/reports/pdf/FY2025-Audited-AFR-compressed.pdf) (statement pages are scanned images; figures read from page images) |

- Mississippi IHL detail: the FY2025 system audit gives a per-university long-term-liabilities rollforward (bonded debt, leases, SBITA, pension, OPEB) for Alcorn, Jackson State and Mississippi Valley State - [IHL FY2025 audit](https://www.mississippi.edu/sites/default/files/ihl/files/2025%20Audited%20Financial%20Statements%20032626.pdf)
- Southern University System at 6/30/2023 had notes payable $989,617, finance purchase obligations $19,725,001 and lease liability $261,803 (system-wide) - [SU System FY2023 report](https://app.lla.la.gov/publicreports.nsf/0/81dd9fa59648076f86258cb4005ffe58/$file/00007e1d.pdf)
- Alabama A&M's own website archive only posts audited statements through FY2021; at 9/30/2021 notes payable were $12,994,785 after $84.4M of reductions that year - [AAMU FY2021 audited statements](https://www.aamu.edu/about/administrative-offices/comptrollers-office/_documents/aamu_2021_audited_fs.pdf); [AAMU financial report archive](https://www.aamu.edu/about/administrative-offices/comptrollers-office/financial-report-archive.html)

#### B. Other HBCUs - figures taken from audited financial statements

| School | Core debt | What it includes | FYE | Source |
|---|---|---|---|---|
| Howard University | $899,859,000 | Bonds payable net $816,255K + notes payable $331K + finance lease obligations $58,273K + line of credit $25,000K. Consolidated (University + Hospital). Operating lease obligations $106.6M excluded. | 6/30/2025 | [Howard FY2025 consolidated statements](https://howard.edu/sites/home.howard.edu/files/2026-01/Howard%20University%20Audited%20Consolidated%20Financial%20Statements%20June%2030%202025.pdf) |
| Morgan State | $176,089,725 | HBCU (Capital Financing) loan payable $104,640,019 + note payable $1,063,981 + lease liability $70,385,725. SBITA $2,755,196 excluded. | 6/30/2025 | [Morgan FY2025 statements](https://www.morgan.edu/Documents/ADMINISTRATION/OFFICES/comptroller/Morgan%20State%20University%20-%20Financial%20Statements_YE06-30-2025%20Final%20%28signed%29.pdf) |
| North Carolina A&T | $149,799,688 | Revenue bonds net $144,792,729 + note from direct borrowing $2,144,541 + lease liabilities $2,862,419. SBITA $2,786,814 excluded. Discretely presented component unit (foundation) separately carries about $152.6M of bonds/notes, not included. | 6/30/2025 | [NC State Auditor FIN-2025-6070](https://www.auditor.nc.gov/documents/reports/financial/fin-2025-6070/open) |
| North Carolina Central | $94,104,855 | Total long-term debt $93,868,750 (revenue bonds net $92,645,560 + note from direct borrowing) + lease liabilities $236,105. | 6/30/2025 | [NC State Auditor FIN-2025-6090](https://www.auditor.nc.gov/documents/reports/financial/fin-2025-6090/open) |
| South Carolina State | $8,507,313 | Bonds payable $6,390,269 + notes payable $2,117,044. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000410812) |
| Delaware State | $88,864,086 | Long-term debt $86,107,925 (revenue bonds $78.61M + premium + direct-borrowing notes $2.31M) + financed purchase $2,440,162 + lease obligation $315,999. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000410517) |
| Kentucky State | $91,198,684 | Total long-term debt $91,192,953 (bonds, financed purchases) + lease liability $5,731. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000433106) |
| Langston | $24,902,769 | "Total long-term debt" incl. lease obligation $556,199. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412343) |
| Lincoln University (MO) | $15,579,803 | Long-term debt (revenue bonds) $15,009,862 + lease liabilities $569,941. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000408343) |
| Hampton | $152,603,216 | Bonds payable net $123,783,733 (incl. HBCU Capital Financing Series A 2024-3) + notes payable $28,819,483. Consolidated with subsidiaries. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412926) |
| Morehouse College | $12,911,287 | Bond payable net $12,726,548 + finance lease obligations $184,739. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000407095) |
| Spelman | $39,151,262 | Bonds payable. "Obligations under right of use lease" $5,022,693 not included (type not specified). | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000401158) |
| Tuskegee | $34,100,461 | Long-term debt, net (Rice Capital Access Program / HBCU Capital Financing Series A 2023-6 and a fixed note). Was $2,980,207 at 6/30/2024. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412682) |
| Xavier of Louisiana | $96,603,173 | Mortgage payable net $94,108,173 (HBCU Capital Financing loan via Rice Capital) + line of credit $2,495,000. Form 990 showed $57.1M at 6/30/2024. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412804) |
| Clark Atlanta | $2,759,269 | Loans payable. Lease liabilities $647,036 not included (type not specified). | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000404102) |
| Fisk | $51,521,146 | Bonds payable net $33,225,652 (HBCU Capital Financing Series A 2022-2 / 2022-3) + notes payable $16,295,494 + line of credit $2,000,000. | 6/30/2025 | [FAC single audit FY2025 (reissued)](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000424801) |
| Bennett | $8,483,076 | Line of credit (only debt on the balance sheet; finance leases nil). | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412922) |
| Talladega | $56,628,122 | Notes and loans payable ($2,780,303 current + $53,847,819 noncurrent). Form 990 showed $30.2M at 6/30/2024. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000410936) |
| Saint Augustine's | $15,817,964 | "Long-term debt" (up from $11,680,150 a year earlier). Latest audit on file is FY2024; no FY2025 audit found in the Federal Audit Clearinghouse. | 6/30/2024 | [FAC single audit FY2024](https://app.fac.gov/dissemination/report/pdf/2024-06-GSAFAC-0000066734) |
| Dillard | $40,516,047 | HBCU capital project loan $36,328,833 (was $7,981,172) + note payable $3,962,500 + finance leases $224,714. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000411999) |
| Meharry Medical College | $97,921,279 | Bonds payable net $57,414,176 + notes payable to banks $31,327,294 + finance lease liability $9,179,809. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000424212) |
| Claflin | $39,122,870 | Notes payable $19,968,009 + New Markets Tax Credit notes $18,500,000 (partly offset by a $13,885,175 NMTC leverage-loan asset) + finance lease $654,861. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000406201) |
| Benedict | $31,940,810 | Bonds payable net $29,614,074 + bank line of credit $2,326,736. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000384836) |
| Shaw | $20,758,130 | Notes payable net $12,059,766 + line of credit $8,698,364. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412201) |
| Virginia Union | $24,745,115 | Debt obligations $21,978,463 + line of credit $1,800,000 + finance lease liabilities $966,652. Operating lease liabilities $14.3M excluded. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000399466) |
| Morehouse School of Medicine | $16,266,470 | Line-of-credit borrowings only; no bonds or notes payable line found (finance leases not checked). | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000409340) |
| Oakwood | $25,588,909 | Notes payable $15,149,449 + bonds and other notes payable $10,439,460. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000389513) |
| Miles | $19,124,062 | Bonds payable net $11,783,193 + notes payable $6,548,584 + capitalized lease obligations $792,285. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000388498) |
| Paul Quinn | $8,514,046 | Notes payable ($8,387,353 current + $126,693 long-term). | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000414041) |
| Philander Smith | $15,211,028 | Notes payable $9,554,181 + bonds net $3,707,588 + line of credit $1,500,000 + mortgage $257,526 + finance leases $191,733. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000388497) |
| Stillman | $8,097,282 | Notes payable (all shown as current portion). | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000413801) |
| Tougaloo | $1,138,064 | Notes payable $1,131,904 + finance lease $6,160. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000388502) |
| Livingstone | $6,690,831 | Notes payable $2,570,802 + SPE premium-financing loan $3,563,690 + finance leases $556,339. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000415330) |
| Wilberforce | $11,843,667 | Notes payable $10,443,667 + line of credit $1,400,000. A separate "U.S. Department of Education liability" of $3,042,303 is not included. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000410559) |
| Wiley | $13,459,490 | Notes payable $12,478,688 + capital lease obligations $980,802. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000411145) |
| Edward Waters | $9,391,317 | Note and bond payable, net. | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000388500) |
| Lincoln University (PA) | $34,772,124 | Bonds payable net $29,164,019 + line of credit $5,065,980 + loans payable $542,125. Lease liability $492,501 not included (type not specified). | 6/30/2025 | [FAC single audit FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000399614) |

#### C. Other HBCUs - Form 990 balance-sheet debt lines only (private, FY2024 = fiscal year ended 6/30/2024)

Lines used: Part X line 20 tax-exempt bond liabilities + line 23 secured mortgages and notes payable + line 24 unsecured notes and loans payable. Source for each: ProPublica Nonprofit Explorer organization page.

| School | 990 debt lines total | FYE | Source |
|---|---|---|---|
| Paine College | $16,937,358 (secured $7,465,293 + unsecured $9,472,065) | 6/30/2024 | [ProPublica EIN 237434499](https://projects.propublica.org/nonprofits/organizations/237434499) |
| Texas College | $6,820,882 | 6/30/2024 | [ProPublica EIN 750917417](https://projects.propublica.org/nonprofits/organizations/750917417) |
| Simmons College of Kentucky | $5,495,638 | 6/30/2024 | [ProPublica EIN 205289168](https://projects.propublica.org/nonprofits/organizations/205289168) |
| LeMoyne-Owen College | $5,124,617 | 6/30/2024 | [ProPublica EIN 620475690](https://projects.propublica.org/nonprofits/organizations/620475690) |
| Allen University | $2,096,031 (bonds $1,849,337 + secured notes $246,694) | 6/30/2024 | [ProPublica EIN 570341191](https://projects.propublica.org/nonprofits/organizations/570341191) |
| Jarvis Christian University | $1,918,035 | 6/30/2024 | [ProPublica EIN 750995027](https://projects.propublica.org/nonprofits/organizations/750995027) |
| Morris College | $712,500 | 6/30/2024 | [ProPublica EIN 576000734](https://projects.propublica.org/nonprofits/organizations/576000734) |
| Lane College | $481,272 | 6/30/2024 | [ProPublica EIN 620570060](https://projects.propublica.org/nonprofits/organizations/620570060) |
| Rust College | $441,137 | 6/30/2024 | [ProPublica EIN 640303805](https://projects.propublica.org/nonprofits/organizations/640303805) |
| Johnson C. Smith University | $0 on all three lines (FY2025 audit also says its $10M line of credit was entirely undrawn at 6/30/2025) | 6/30/2024 | [ProPublica EIN 250983069](https://projects.propublica.org/nonprofits/organizations/250983069); [FAC FY2025 audit](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000405036) |
| Florida Memorial University | $0 on all three lines | 6/30/2024 | [ProPublica EIN 590668483](https://projects.propublica.org/nonprofits/organizations/590668483) |

- Form 990 FY2024 cross-checks for schools in table B: Howard bonds $811,021,000 + unsecured notes $97,354,000; Hampton bonds $101,120,368 + secured notes $29,425,586; Spelman bonds $45,364,028; Morehouse College bonds $3,141,497; Xavier secured notes $57,130,957; Fisk secured notes $45,013,019; Talladega secured notes $30,167,523; Bennett secured notes $6,539,251; Saint Augustine's secured notes $15,817,964; Dillard unsecured notes $11,881,172; Meharry bonds $61,239,819 + secured notes $12,078,712; Bethune-Cookman secured notes $92,617,761 - [ProPublica Nonprofit Explorer](https://projects.propublica.org/nonprofits/) (EINs: Howard 530204707, Hampton 540505990, Spelman 580566243, Morehouse 580566205, Xavier 720635884, Fisk 620202000, Talladega 630288870, Bennett 560532296, Saint Augustine's 560547478, Dillard 720408929, Meharry 620488046, Bethune-Cookman 590704726)

#### D. Other HBCUs - IPEDS FY2024 self-reported long-term debt only (four-year publics I did not pull audits for)

Source for every row: [NCES IPEDS FY2024 Finance file F2324_F1A](https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip) (current portion F1A07 + long-term debt F1A10), HBCU flag from [HD2024](https://nces.ed.gov/ipeds/complete-data-files/HD2024.zip). Fiscal years ending in 2024.

| School | IPEDS long-term debt FY2024 |
|---|---|
| Tennessee State | $90,483,738 |
| Winston-Salem State | $79,444,009 |
| Albany State | $79,274,280 |
| Norfolk State | $77,134,020 |
| Virginia State | $67,378,362 |
| Savannah State | $66,657,607 |
| Fort Valley State | $66,335,702 |
| Fayetteville State | $51,876,555 |
| Elizabeth City State | $36,564,390 |
| West Virginia State | $35,484,214 |
| Bowie State | $27,716,107 |
| Coppin State | $22,650,993 |
| University of Maryland Eastern Shore | $19,135,159 |
| Cheyney | $9,545,959 |
| Central State | $6,921,299 |
| University of the Virgin Islands | $3,921,004 |
| Harris-Stowe State | $20,124 |
| University of the District of Columbia | $0 |
| Bluefield State | $0 |

- Two-year HBCUs and other units in the same IPEDS file (not used in my wider computation): St. Philip's College $168.4M (a college of the Alamo Colleges District, so likely district-allocated debt), Gadsden State CC $42.2M, Bishop State CC $19.4M, Shelton State CC $18.4M, Trenholm State CC $10.7M, Drake State $6.0M, Lawson State CC $2.6M, Southern University at Shreveport $2.4M, and $0 for Coahoma CC, Denmark Tech, SUNO, SU Law Center - [IPEDS F2324_F1A](https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip)

### Inferences
- The HBCU Capital Financing Program (loans via Rice Capital Access Program) is the dominant form of new borrowing: it accounts for all or most of the debt at Alabama A&M, Bethune-Cookman, Florida A&M, Morgan State (loan portion), Xavier, Tuskegee, Dillard, Fisk and Hampton's newest series. Several schools whose pre-2021 program loans were discharged have re-borrowed heavily since (Alabama A&M $13.0M in 2021 to $86.6M in 2025; Tuskegee $3.0M to $34.1M in one year; Florida A&M $2.4M to $55.2M in one year; Dillard $8.0M to $36.3M in one year).
- Debt levels are moving quickly, so the fiscal year matters: Alabama State's debt roughly tripled in FY2025 (from about $44.9M to $134.6M core) because of the June 2025 Series 2025 bonds; Talladega's nearly doubled ($30.2M to $56.6M); Xavier's rose from $57.1M to $96.6M.
- System schools are understated relative to stand-alone schools: Prairie View's $10.8M excludes Texas A&M System-held revenue-financing debt; Grambling and Southern show little debt on campus books; several schools' student housing is financed through foundations/component units (NC A&T foundation about $152.6M; Delaware State Student Housing Foundation; SU System Foundation) that are not in the campus figure.
- Mixing FY2024 and FY2025 rows is unavoidable for Grambling, Southern, Saint Augustine's and the tier C/D schools; any average therefore blends two fiscal years.

### Gaps
- Grambling State FY2025: not found. I located only the UL System FY2024 audit; FY2025 management letters for other UL campuses exist on the LLA site but I did not find the FY2025 system audit with a Grambling column.
- Southern University FY2025: not found. The FY2024 system report is dated December 15, 2025, so a FY2025 report may not yet be issued.
- Prairie View A&M's allocable share of Texas A&M System Revenue Financing System / PUF bonds: not found. The campus AFR shows only a "Debt Service Transfer Out" of $5,936,967 for FY2025 and the System's combined AFR does not break bonds out by member in the pages I searched.
- Norfolk State, Coppin State, UMES, Tennessee State, Winston-Salem State and the other tier D schools: audited statements not pulled (IPEDS FY2024 only). Maryland (Coppin, UMES) and Virginia (Norfolk State) report through state/system audits.
- Voorhees University: FY2024 audit balance sheet shows total liabilities of $2,664,812 but I could not isolate a debt line; recorded as not found.
- Huston-Tillotson, Interdenominational Theological Center, Arkansas Baptist, Shorter, Selma, Morris Brown, Clinton College, American Baptist College, Southwestern Christian, Virginia University of Lynchburg: not researched beyond the IPEDS file (several report $0 or small amounts there).
- EMMA (emma.msrb.org) and rating-agency reports were not accessed; no Moody's/S&P/Fitch debt totals are included.

---

## Key Question 2: What context is available - revenues, net position, audit findings, going-concern language, late audits?

### Takeaway
Among SWAC schools, debt is small relative to annual revenue at Grambling, Prairie View, Southern and Florida A&M (under 0.15x), moderate at most others (0.27x to 0.50x), and highest at Alabama State (about 0.70x) and Bethune-Cookman (about 0.9x to 1.0x). The clearest governance red flags are late or deficient audits at Florida A&M, Southern and Texas Southern, and outside the SWAC a going-concern paragraph at Saint Augustine's and very high leverage at Talladega (about 2.85x revenue).

### Cited Findings

#### SWAC context table (debt figures from Key Question 1; ratios are my arithmetic)

| School | Revenue used (FY) | Net position / net assets | Debt / revenue (my calc) | Audit notes |
|---|---|---|---|---|
| Alabama A&M | $259.7M FY2025 (operating $154,695,891 + state appropriations $74,791,404 + investment income $1,720,520 + federal nonoperating $28,484,544) | $156.9M | 0.33 | FAC record: unmodified opinion, no going concern, no material weakness; accepted by FAC 6/30/2026 |
| Alabama State | $191.7M FY2025 (operating $117,394,733 + net nonoperating $74,261,751) | $196.4M (down $5.1M) | 0.70 | Auditor Warren Averett; report dated March 27, 2026 |
| Alcorn State | $126.1M FY2025 (operating $71,567,918 + state appropriations $37,790,212 + gifts and grants $14,804,947 + investment income $1,944,371) | $172.6M | 0.31 | Part of IHL system audit |
| Arkansas-Pine Bluff | $95.9M FY2025 (operating $37,998,816 + nonoperating revenues $57,853,865) | $112.1M (down $10.4M, including a $12,180,268 "adjustment to prior year revenues and expenses") | 0.43 | UA System audit dated December 10, 2025; report describes a $37,375 loss from unauthorized purchases in UAPB facilities management |
| Bethune-Cookman | FY2024: $88.2M (IPEDS) / $100.2M (Form 990 total revenue). FY2025 unrestricted revenues, gains and other support before releases: $60,994,577 | $128.2M FY2025 | about 0.9 to 1.0 | FAC record FY2025: unmodified, no going concern, no material weakness |
| Florida A&M | $384.4M FY2025 (operating $160.885M + nonoperating revenues $210.625M + other revenues $12.930M) | $675.3M | 0.15 | Audit report dated August 7, 2026 (over 13 months after year-end); material weakness 2025-001 on financial recordkeeping/reporting, repeat of 2024-001; $29.5M and $9.7M audit adjustments |
| Grambling State | $134.8M FY2024 (IPEDS total revenues) | $106.9M FY2024 | 0.02 | UL System FY2024 audit notes Grambling restatements ($6.9M over-depreciation; $2.8M understated expenses/payables) |
| Jackson State | $222.3M FY2025 (operating $137,401,280 + state appropriations $49,594,871 + gifts and grants $22,608,661 + investment income $6,780,912 + other nonoperating $5,917,919) | $168.2M | 0.37 | "Other nonoperating expenses" of $22.6M in FY2025; a $1,912,787 "Federal Loan Fund Repayment Contingency" liability |
| Mississippi Valley State | $50.7M FY2025 (operating $22,337,329 + state appropriations $18,359,613 + gifts and grants $8,273,945 + investment income $1,458,460 + other $229,448) | $128.4M (up $32.5M, incl. $19.9M additions to permanent endowments and $15.6M capital appropriations) | 0.27 | Part of IHL system audit |
| Prairie View A&M | $325.4M FY2025 (operating $146,951,873 + net nonoperating $178,415,234) | $920.5M | 0.03 (campus debt only) | Campus AFR is unaudited; audited at Texas A&M System level |
| Southern (Baton Rouge) | System FY2024 total revenues $316.0M; SUBR campus $214.3M (IPEDS FY2024) | System $82.2M; Baton Rouge campus column $14.2M (unrestricted net position -$157.4M, driven by pension/OPEB liabilities) | 0.09 campus / 0.07 system | FY2023 report dated June 13, 2025; FY2024 report dated December 15, 2025 (about 17.5 months after year-end); unmodified opinion with one significant deficiency (Banner system access) |
| Texas Southern | $262.6M FY2025 (operating $139,016,049 + net nonoperating $123,552,284) | $355.3M (down $4.2M) | 0.50 | Material weakness #2025-001 (auditor-proposed adjustments to investments, prepaids, construction in progress, subscriptions, accrued expenses, salaries and insurance payable) |

- Sources for the table: [AAMU FY2025](https://app.fac.gov/dissemination/report/pdf/2025-09-GSAFAC-0000422111); [Alabama State FY2025](https://www.alasu.edu/administration/business-and-finance/financial-statements-fy2025.pdf); [Mississippi IHL FY2025](https://www.mississippi.edu/sites/default/files/ihl/files/2025%20Audited%20Financial%20Statements%20032626.pdf); [UA System FY2025](https://www.arklegaudit.gov/downloadReport.php?id=EDHE14125); [B-CU FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412000) and [B-CU Form 990](https://projects.propublica.org/nonprofits/organizations/590704726); [FAMU Report 2027-013](https://flauditor.gov/pages/pdf_files/2027-013.pdf); [UL System FY2024](https://lla.la.gov/publicreports.nsf/0/ceaac10dcadb296d86258c030070835f/$file/0000895c.pdf); [PVAMU FY2025 AFR](https://assets.system.tamus.edu/files/budgets-acct/pdf/afr/FY2025pvamu.pdf); [SU System FY2024](https://app.lla.la.gov/publicreports.nsf/0/ff59d2e8e84a231d86258d63006ccacf/$file/000095aaa.pdf) and [FY2023](https://app.lla.la.gov/publicreports.nsf/0/81dd9fa59648076f86258cb4005ffe58/$file/00007e1d.pdf); [TSU FY2025 AFR](https://www.tsu.edu/about/administration/finance/reports/pdf/FY2025-Audited-AFR-compressed.pdf); IPEDS revenue for Grambling and SUBR from [F2324_F1A](https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip)
- Florida A&M's president's letter in the FY2025 report acknowledges "this report includes a material weakness"; the Auditor General's finding says "University financial recordkeeping and reporting controls are deficient, increasing the risk for a material misstatement" - [Florida Auditor General Report 2027-013](https://flauditor.gov/pages/pdf_files/2027-013.pdf)
- A Texas State Auditor's Office report (No. 26-012, December 2025) on Texas Southern is described in search results as finding "significant weaknesses in its financial processes related to procurement, asset management, and financial reporting" (I did not open the report itself) - [Texas SAO 26-012](https://sao.texas.gov/Reports/Main/26-012.pdf)
- The Louisiana Legislative Auditor reported an athletics deficit of roughly $5 million at Grambling for FY2025 (news report of an LLA agreed-upon-procedures report; underlying report not opened) - [Lincoln Parish Journal, May 14, 2026](https://lincolnparishjournal.com/2026/05/14/grambling-athletics-deficit-over-5-million-cited-by-legislative-auditor/)
- A Legislative Auditor review found Southern University athletics ran a nearly $1.5 million deficit in fiscal 2025 (news summary) - [Baton Rouge Business Report](https://www.businessreport.com/business/what-the-latest-audit-on-southern-university-athletics-shows)

#### Context for selected non-SWAC schools (ratios are my arithmetic)

- Howard: total revenues and support $1,188.85M FY2025; net assets $1,411.5M; core debt/revenue about 0.76. FAC flags a material weakness for FY2025 - [Howard FY2025 statements](https://howard.edu/sites/home.howard.edu/files/2026-01/Howard%20University%20Audited%20Consolidated%20Financial%20Statements%20June%2030%202025.pdf); [FAC search](https://app.fac.gov/dissemination/search/)
- Morgan State: total revenues $508.4M FY2025; net position $620.9M; debt/revenue about 0.35; audit dated December 8, 2025 - [Morgan FY2025](https://www.morgan.edu/Documents/ADMINISTRATION/OFFICES/comptroller/Morgan%20State%20University%20-%20Financial%20Statements_YE06-30-2025%20Final%20%28signed%29.pdf)
- NC A&T: total revenues $521.6M FY2025; net position $716.8M; debt/revenue about 0.29; audit report dated July 31, 2026 (13 months after year-end) - [NC Auditor FIN-2025-6070](https://www.auditor.nc.gov/documents/reports/financial/fin-2025-6070/open)
- NC Central: total revenues $294.5M FY2025; net position $197.3M; debt/revenue about 0.32; audit dated December 18, 2025, "no material errors" - [NC Auditor FIN-2025-6090](https://www.auditor.nc.gov/documents/reports/financial/fin-2025-6090/open)
- South Carolina State: total revenues $188.3M FY2025; net position $173.3M; debt/revenue about 0.05 - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000410812)
- Delaware State: net position negative, -$23,974,194 at 6/30/2025 (-$27.9M prior year); FAC flags material weakness in both FY2024 and FY2025 - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000410517)
- Kentucky State: operating revenues $61.4M + nonoperating $46.1M FY2025; net position $58.9M; debt/revenue about 0.85; FY2025 audit accepted by FAC on 2026-11-20 and FY2024 audit on 2026-01-22 (both very late); material weakness flagged both years - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000433106)
- Hampton: total revenues $250.1M FY2025; net assets $682.6M; debt/revenue about 0.61; FAC flags material weakness FY2024 and FY2025 - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412926)
- Morehouse College: revenue and support $175.7M; net assets $548.7M; debt/revenue about 0.07 - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000407095)
- Spelman: total operating revenue $150.9M; debt/revenue about 0.26 - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000401158)
- Tuskegee: revenues, gains and other support $169.9M; net assets $571.6M; debt/revenue about 0.20 - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412682)
- Xavier: operating revenues and support $142.0M; net assets $426.5M; debt/revenue about 0.68 - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412804)
- Clark Atlanta: total revenue and other support $175.4M; net assets $367.5M; debt/revenue about 0.02 - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000404102)
- Fisk: total revenue and other support $38.3M; net assets $168.7M; debt/revenue about 1.34. The audit says a covenant breach gave a lender "the right to declare the debt immediately due and payable" (balance reclassified to current) and that Fisk "was not in compliance with the Rice Capital minimum debt service coverage ratio"; the FY2025 audit was reissued (two FAC submissions, June and July 2026) - [FAC FY2025 reissued](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000424801)
- Bennett: operating revenue and support $12.4M; net assets $36.3M; debt/revenue about 0.68; line of credit grew from $6.5M to $8.5M - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412922)
- Talladega: revenues, gains and other support $19.9M; net assets $59.3M (beginning net assets restated to $72.7M; auditor notes FY2024 was restated "to reflect multiple errors"); debt/revenue about 2.85; FAC flags material weakness FY2025; FY2024 audit not accepted until 2026-01-20 - [FAC FY2025](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000410936)
- Saint Augustine's: FY2024 audit carries an emphasis paragraph titled "Substantial Doubt About the University's Ability to Continue as a Going Concern," citing the accreditor's vote to remove the university from membership; operating revenues $20.9M (down from $35.3M); net assets $36.5M; total liabilities $45.4M incl. $14.9M accounts payable; debt/revenue about 0.76; material weakness flagged; no FY2025 single audit on file as of this research - [FAC FY2024](https://app.fac.gov/dissemination/report/pdf/2024-06-GSAFAC-0000066734)
- Other FAC flags (FY2025 unless noted): material weakness = Benedict, Dillard (FY2024 and FY2025), Livingstone, Meharry, Philander Smith (FY2024 accepted 2026-04-28, FY2025 accepted 2026-10-10), Virginia Union; qualified opinion = Wiley (FY2024 and FY2025); going-concern flag = Paul Quinn FY2025 (FAC data field says yes; I did not locate an explicit emphasis paragraph in a quick text scan, so treat as unverified) - [Federal Audit Clearinghouse search](https://app.fac.gov/dissemination/search/)

### Inferences
- On a debt-to-revenue basis the most leveraged schools in the collected set are small privates (Talladega about 2.85x, Fisk about 1.34x, Bethune-Cookman about 0.9 to 1.0x), not the schools with the largest dollar debt. Howard's $900M is about 0.76x its $1.19B revenue.
- Late audits cluster at a handful of schools: Southern (17 to 24 months), Florida A&M (13 months, with repeat material weakness), Kentucky State (FY2025 filed November 2026), Philander Smith, Talladega (FY2024) and NC A&T (13 months for FY2025). The normal single-audit deadline is nine months after year-end.
- Low campus debt does not equal financial strength: Grambling, Southern and Saint Augustine's have little bonded debt but show other stress indicators (athletics deficits, negative campus net position, going-concern language).

### Gaps
- I did not capture audit-report dates or opinion types for the Mississippi IHL and Texas Southern FY2025 audits, or total FY2025 revenue for Bethune-Cookman and Delaware State.
- Revenue definitions differ (GASB operating + nonoperating revenues for publics; FASB total revenues/support for privates; some figures before capital appropriations), so debt/revenue ratios are indicative only.
- No rating-agency commentary was retrieved.

---

## Key Question 3: Are there existing compilations that already list debt per HBCU?

### Takeaway
Yes, three usable public compilations exist (IPEDS Finance, IRS Form 990 data via ProPublica, and the Federal Audit Clearinghouse), but none is a clean ready-made "HBCU debt league table," and IPEDS in particular contains material errors for individual schools. I found no HBCU Money, Forbes or similar published list of institutional debt by HBCU.

### Cited Findings
- IPEDS Finance FY2024 (released as provisional data in the files dated December 30, 2025) contains a long-term-debt field for all 102 institutions flagged HBCU in the HD2024 directory: 50 GASB-form reporters (F1A07 current portion + F1A10 long-term debt) and 52 FASB-form reporters (F2A03A "Debt related to Property, Plant, and Equipment") - [F2324_F1A](https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip); [F2324_F2](https://nces.ed.gov/ipeds/complete-data-files/F2324_F2.zip); [HD2024](https://nces.ed.gov/ipeds/complete-data-files/HD2024.zip); [IPEDS data files page](https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx?year=2024)
- IPEDS FY2024 values for the SWAC 12: Alabama A&M $73,285,311; Alabama State $40,306,132; Alcorn $41,196,551; UAPB $43,467,583; Bethune-Cookman $92,617,760; Florida A&M $2,449,252; Grambling $0; Jackson State $85,442,262; MVSU $14,236,819; Prairie View $10,781,813; Southern (Baton Rouge) $228,786,347; Texas Southern $137,871,771 - [F2324_F1A](https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip); [F2324_F2](https://nces.ed.gov/ipeds/complete-data-files/F2324_F2.zip)
- IPEDS matches the audits exactly where I could test it: Alabama A&M $73,285,311 equals the audited 9/30/2024 loans payable; Alcorn, Jackson State and MVSU equal the FY2024 beginning balances in the IHL rollforward (bonds + leases + SBITA + financed purchases); Bethune-Cookman equals audited 6/30/2024 long-term debt; Florida A&M equals the 6/30/2024 capital improvement debt; Langston equals audited FY2024 total long-term debt - [AAMU FY2025 audit](https://app.fac.gov/dissemination/report/pdf/2025-09-GSAFAC-0000422111); [IHL FY2025 audit](https://www.mississippi.edu/sites/default/files/ihl/files/2025%20Audited%20Financial%20Statements%20032626.pdf); [B-CU FY2025 audit](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412000); [FAMU 2027-013](https://flauditor.gov/pages/pdf_files/2027-013.pdf); [Langston FY2025 audit](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412343)
- IPEDS is wrong or incomplete for some schools: Southern University Baton Rouge reports $228.8M to IPEDS for FY2024 while the audited system-wide notes, finance purchases and leases total only $21.1M (system total long-term liabilities including pensions were $237.1M) - [IPEDS F2324_F1A](https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip); contradicted by [SU System FY2024 audit](https://app.lla.la.gov/publicreports.nsf/0/ff59d2e8e84a231d86258d63006ccacf/$file/000095aaa.pdf)
- IPEDS reports $0 PP&E debt for Hampton for FY2024, while Hampton's Form 990 and audit show $130.5M of bonds and notes at 6/30/2024; IPEDS also shows $0 for Saint Augustine's ($15.8M per audit), Bennett ($6.5M per 990), Dillard ($11.9M per 990), Tuskegee ($3.0M per audit) and Morehouse College ($3.1M per 990) - [IPEDS F2324_F2](https://nces.ed.gov/ipeds/complete-data-files/F2324_F2.zip); contradicted by [Hampton FY2025 audit](https://app.fac.gov/dissemination/report/pdf/2025-06-GSAFAC-0000412926) and [ProPublica Hampton EIN 540505990](https://projects.propublica.org/nonprofits/organizations/540505990)
- IPEDS excludes lease liabilities at some schools: Morgan State's IPEDS FY2024 figure of $69,252,096 equals its HBCU loan plus note payable and omits $43.4M of lease liabilities shown in its audit - [IPEDS F2324_F1A](https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip); [Morgan FY2025 statements](https://www.morgan.edu/Documents/ADMINISTRATION/OFFICES/comptroller/Morgan%20State%20University%20-%20Financial%20Statements_YE06-30-2025%20Final%20%28signed%29.pdf)
- The Urban Institute Education Data API republishes IPEDS finance data with a `longterm_debt` field per institution and an `hbcu` directory flag (101 institutions flagged in its 2023 directory); its "2023" finance record for Alabama A&M carries the same $73.3M value as the NCES FY2024 file - [Urban Institute Education Data API](https://educationdata.urban.org/api/v1/college-university/ipeds/finance/2023/?unitid=100654)
- ProPublica Nonprofit Explorer exposes Form 990 Part X balance-sheet lines (tax-exempt bond liabilities, secured mortgages and notes, unsecured notes) for private HBCUs through FY2024 (a few FY2025) via a free API - [ProPublica Nonprofit Explorer API](https://projects.propublica.org/nonprofits/api)
- The Federal Audit Clearinghouse provides downloadable single-audit PDFs (with full audited financial statements) plus machine-readable flags for going concern, material weakness and opinion type; FY2025 filings exist for nearly every private HBCU and several publics - [FAC search](https://app.fac.gov/dissemination/search/)
- Academic/advocacy context: an AAUP Academe article by Andrew J. Douglas (Morehouse) states that the December 2020 CRRSAA law authorized the Education Department to discharge $1.6 billion of capital-financing debt held by 13 public and 32 private HBCUs, including about $56 million at Morehouse (about $5 million of annual debt service); it names IPEDS and tax filings as the data sources for campus "debt audits" but gives no per-school table - [AAUP Academe, Winter 2022](https://www.aaup.org/article/battling-institutional-debt-hbcus)

### Inferences
- IPEDS is reliable for most public HBCUs (the GASB field tracks audited bonds/notes, sometimes without leases) but unreliable for private HBCUs, many of which leave the FASB debt field at $0; Form 990 Part X or the FAC audit PDFs are better for privates.
- Any published average built straight from IPEDS would be distorted by Southern's $228.8M entry (inflating the SWAC average) and by false zeros at privates (deflating the all-HBCU median).

### Gaps
- No HBCU Money, Forbes financial-grade, College Scorecard or Moody's compilation of institutional debt by HBCU was found. My one search for an HBCU Money debt analysis returned nothing relevant; Forbes grades and College Scorecard were not checked directly (College Scorecard reports student debt, not institutional debt).
- The Education Department press release on the $1.6 billion HBCU Capital Financing discharge (ed.gov) and a Diverse/EduLedger article "Report reveals a differing picture of debt at HBCUs" both returned HTTP 403 and could not be read, so per-school forgiveness amounts are not included.
- An EY report on institutional debt ("The other looming educational debt crisis") surfaced in search but was not opened.

---

## Key Question 4: What are the computed average and median debt for the SWAC set and for the wider HBCU set?

### Takeaway
These are my own computations from the cited figures, not published statistics. SWAC (12 of 12 schools): average about $58.8M, median about $48.4M. Wider set of 79 HBCUs: average about $49.8M, median about $22.7M; excluding Howard, average about $38.9M and median about $21.7M.

### Cited Findings

All inputs are the "core debt" figures listed under Key Question 1 (sources cited there). Arithmetic performed by me.

#### (a) SWAC members, n = 12 (10 at FY2025; Grambling and Southern at FY2024)

Values sorted (in dollars): Grambling 2,813,563; Prairie View (campus) 10,781,813; Mississippi Valley State 13,500,850; Southern Baton Rouge campus 18,688,760; Alcorn State 39,442,005; Arkansas-Pine Bluff 40,950,929; Florida A&M 55,801,381; Jackson State 82,028,463; Alabama A&M 86,621,372; Bethune-Cookman 89,026,374; Texas Southern 130,948,673; Alabama State 134,634,312.

- Sum = $705,238,495
- Average = 705,238,495 / 12 = $58,769,875
- Median = midpoint of 6th and 7th values = (40,950,929 + 55,801,381) / 2 = $48,376,155
- Schools with no public figure: none (but Prairie View is campus-only and unaudited, and Grambling/Southern are one fiscal year older).

Sensitivity checks (also my arithmetic):
- Using the Southern University System total ($21,127,077) instead of the Baton Rouge campus: sum $707,676,812; average $58,973,068; median unchanged at $48,376,155.
- Adding SBITA liabilities where separately reported (Alabama State, UAPB, Florida A&M, Jackson State, MVSU): sum $720,636,262; average $60,053,022; median $54,731,048.
- Straight IPEDS FY2024 values for the same 12 schools: sum $770,441,601; average $64,203,467; median $42,332,067. This version is distorted by Southern's $228.8M IPEDS entry and predates the FY2025 borrowings at Alabama State and Florida A&M - [IPEDS F2324_F1A](https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip); [F2324_F2](https://nces.ed.gov/ipeds/complete-data-files/F2324_F2.zip)

#### (b) All HBCUs collected, n = 79

Composition: 12 SWAC + 37 other schools from audited statements (table B) + 11 from Form 990 FY2024 (table C) + 19 four-year publics from IPEDS FY2024 (table D). Two-year colleges and the Southern University satellite units are excluded.

- Sum = $3,930,395,928
- Average = 3,930,395,928 / 79 = $49,751,847
- Median = 40th of 79 sorted values = $22,650,993 (Coppin State)
- Excluding Howard (n = 78): sum $3,030,536,928; average $38,853,038; median $21,704,562 (midpoint of Shaw $20,758,130 and Coppin State $22,650,993)

Sub-sets:
- Audited statements only (tables A + B), n = 49: sum $3,149,824,936; average $64,282,142; median $31,940,810 (Benedict).
- Audited + Form 990 (tables A + B + C), n = 60: sum $3,189,852,406; average $53,164,207; median $18,906,411.

Full list of the 79 values used, largest to smallest (dollars): Howard 899,859,000; Morgan State 176,089,725; Hampton 152,603,216; NC A&T 149,799,688; Alabama State 134,634,312; Texas Southern 130,948,673; Meharry 97,921,279; Xavier 96,603,173; NC Central 94,104,855; Kentucky State 91,198,684; Tennessee State 90,483,738 (IPEDS); Bethune-Cookman 89,026,374; Delaware State 88,864,086; Alabama A&M 86,621,372; Jackson State 82,028,463; Winston-Salem State 79,444,009 (IPEDS); Albany State 79,274,280 (IPEDS); Norfolk State 77,134,020 (IPEDS); Virginia State 67,378,362 (IPEDS); Savannah State 66,657,607 (IPEDS); Fort Valley State 66,335,702 (IPEDS); Talladega 56,628,122; Florida A&M 55,801,381; Fayetteville State 51,876,555 (IPEDS); Fisk 51,521,146; Arkansas-Pine Bluff 40,950,929; Dillard 40,516,047; Alcorn State 39,442,005; Spelman 39,151,262; Claflin 39,122,870; Elizabeth City State 36,564,390 (IPEDS); West Virginia State 35,484,214 (IPEDS); Lincoln (PA) 34,772,124; Tuskegee 34,100,461; Benedict 31,940,810; Bowie State 27,716,107 (IPEDS); Oakwood 25,588,909; Langston 24,902,769; Virginia Union 24,745,115; Coppin State 22,650,993 (IPEDS); Shaw 20,758,130; UMES 19,135,159 (IPEDS); Miles 19,124,062; Southern Baton Rouge 18,688,760; Paine 16,937,358 (990); Morehouse School of Medicine 16,266,470; Saint Augustine's 15,817,964 (FY2024); Lincoln (MO) 15,579,803; Philander Smith 15,211,028; Mississippi Valley State 13,500,850; Wiley 13,459,490; Morehouse College 12,911,287; Wilberforce 11,843,667; Prairie View 10,781,813; Cheyney 9,545,959 (IPEDS); Edward Waters 9,391,317; Paul Quinn 8,514,046; South Carolina State 8,507,313; Bennett 8,483,076; Stillman 8,097,282; Central State 6,921,299 (IPEDS); Texas College 6,820,882 (990); Livingstone 6,690,831; Simmons College of Kentucky 5,495,638 (990); LeMoyne-Owen 5,124,617 (990); University of the Virgin Islands 3,921,004 (IPEDS); Grambling 2,813,563 (FY2024); Clark Atlanta 2,759,269; Allen 2,096,031 (990); Jarvis Christian 1,918,035 (990); Tougaloo 1,138,064; Morris 712,500 (990); Lane 481,272 (990); Rust 441,137 (990); Harris-Stowe State 20,124 (IPEDS); Johnson C. Smith 0 (990); Florida Memorial 0 (990); University of the District of Columbia 0 (IPEDS); Bluefield State 0 (IPEDS).

#### IPEDS-only uniform computation (for comparison; all 102 IPEDS-flagged HBCUs, FY2024, as self-reported)
- Sum $3,649,743,584; average $35,781,800; median $8,539,550 across all 102 (31 report $0).
- Among the 71 reporting a non-zero amount: average $51,404,839; median $27,319,981.
- Source: [F2324_F1A](https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip); [F2324_F2](https://nces.ed.gov/ipeds/complete-data-files/F2324_F2.zip); [HD2024](https://nces.ed.gov/ipeds/complete-data-files/HD2024.zip). Includes known errors described under Key Question 3.

### Inferences
- The SWAC average ($58.8M) sits above the wider-HBCU average excluding Howard ($38.9M) and well above the wider median ($21.7M), because the wider set includes many small private colleges with little debt. Against the audited-only sub-set (median $31.9M) the SWAC median ($48.4M) is still higher.
- The mean is pulled well above the median in every set; the wider-set mean is dominated by Howard (23% of the 79-school total). The median is the more representative "typical school" number.
- The SWAC median is sensitive to definition: including subscription-IT liabilities raises it from $48.4M to $54.7M, mostly because of Florida A&M's $12.1M SBITA balance.
- Because Alabama State and Florida A&M each added more than $50M of new debt during FY2025, a FY2024-based SWAC figure (median about $42M per IPEDS) understates the current position.

### Gaps
- Schools with no usable public figure in my collection (excluded from the n = 79): Voorhees, Huston-Tillotson (latest 990 with data is FY2023, $0), Interdenominational Theological Center (FY2023 990: $5.0M, not used), Arkansas Baptist, Shorter, Selma, Morris Brown, Clinton College, American Baptist College, Southwestern Christian, Virginia University of Lynchburg, plus all two-year HBCUs and the Southern University satellite units (SUNO, SUSLA, Law Center).
- The wider set mixes three source tiers and two fiscal years (FY2025 audited for 46 schools; FY2024 for the rest), so it is a best-available blend rather than a single-year census.
- Component-unit and system-held debt (university foundations, housing corporations, Texas A&M System financing for Prairie View) is excluded throughout; a "debt that supports the campus" measure would be higher for several schools but could not be built consistently.
