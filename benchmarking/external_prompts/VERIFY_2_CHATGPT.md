# Step 2: ChatGPT (independent check)

Upload `P4_Benchmarking_Double_Check_List.xlsx` and paste everything below the line.

---

I've attached an Excel file, P4_Benchmarking_Double_Check_List.xlsx. It supports a college athletics benchmarking workbook that is about to go to my firm's partners. I need you to act as an independent reviewer and check it against real web pages. Accuracy matters far more than speed. "Could not confirm" is an acceptable answer; a guess is not.

Say at the top of your answer what today's date is, and use web browsing for every factual check.

THE FILE HAS THREE TABS
- "Double-check": 17 cells that still need a look. Columns: #, Why it is here, School, Tab, Cell, Column, Shown now, What to look at, Source.
- "31 dollar figures": dollar values that were first read from a search-result excerpt, with the outcome after the source page was re-read. Columns: School, Tab, Cell, Column, Value before, Shown now, Outcome, Source it came from, Source link.
- "Changes": every cell changed in the last verification pass. Columns: School, Tab, Cell, Column, Before, After, Type (Changed, Blanked or Filled), Reason or source statement, Source.

CONVENTIONS THE WORKBOOK USES ON PURPOSE (do not report these as errors)
- "--" means no value could be sourced. A blank is deliberate.
- Head coach pay is one figure per coach: total guaranteed annual pay for the current season, meaning base salary plus supplemental compensation (the guaranteed amounts contracts label as talent, rights, media or outside-income fees). Where a page states the base and the supplemental amount but no total, the workbook adds the two. Where a page gives only a contract total and length, or an average, the average is shown. Retention payments, signing bonuses and performance bonuses are deliberately left out of the figure.
- A deal's start year may be the year the agreement was announced when the source gives no effective date.
- A coach's contract end year is the year of the stated expiry date. "Through January 31, 2031" is shown as 2031.
- A deal's annual value may be the reported total divided by the term, and a total may be the annual value times the term.

PART A. Check every row of the "Double-check" tab
Use the "Why it is here" column:
- "Re-check on the day you send": find out what is true today (mostly who the head coach is and whether they are interim) from the school's official athletics site and major news from the last two weeks. Give the date of the most recent announcement.
- "Your call": these are my decisions. Do not recommend a policy. Only check whether the factual description in "What to look at" is accurate, and correct it if it is not.
- "Worth a glance": open the Source link, or the school's current official page, and tell me what it says about the point raised.

PART B. Audit a sample of the changes
From the "Changes" tab, take every 8th row (rows 1, 9, 17 and so on, about 22 rows). For each one, open the Source link and tell me whether the "After" value and the stated reason are supported by the page. For rows of type "Blanked", tell me whether you agree that no acceptable page states the old figure; if you find one that does, give me the URL and quote.

PART C. Audit the dollar figures
From the "31 dollar figures" tab, check every row whose Outcome starts with "Confirmed". Open the source link and tell me whether the page states the figure. For head coach pay, the page may state it as a total or as a base salary and a supplemental amount that add up to it; say which.

RULES FOR ALL PARTS
- Open the page yourself. Never answer from memory, a search-result snippet or an AI summary.
- Report what the page states. Do not compute, add up, average, round or infer a figure yourself, apart from recognising the conventions listed above. For head coach pay, if a retention payment, signing bonus or performance bonus has been folded into the figure shown, report that as DIFFERENT. Quote "about" and "more than" wording exactly.
- Acceptable sources: the school's, university's, conference's or NCAA's own pages and PDFs; partner or agency press releases; executed contracts and board documents; state salary databases; Associated Press, ESPN, Sports Business Journal, Sportico, The Athletic, Front Office Sports, CBS Sports, Yahoo Sports, Sports Illustrated, NBC and Fox Sports; established newspapers and local TV news; USA Today's coaches' pay tables (their figures are for the 2025 football season and the 2025-26 basketball season).
- Not acceptable: Wikipedia or wiki mirrors; fan blogs, team fan networks and message boards; stadium-guide sites.
- For every row give a short exact quote (under 40 words) containing the figure or name, the full URL you read, and the page's date if shown.
- If you cannot open a page, say so. Do not fill the gap from memory.
- Do every row asked for. Do not stop early and do not edit the file.

WHAT TO GIVE ME BACK
1. Part A table, one line per row in row order:
# | School | Column | Shown now | Verdict | What the page says | Exact quote | URL you read | Page date
Verdict must be one of CONFIRMED, DIFFERENT, NOT STATED, COULD NOT OPEN, or FACT CHECK ONLY (for "Your call" rows: say whether the description is accurate).
2. Part B table: School | Cell | Column | Before | After | Supported by the page? (Yes / No / Could not open) | Quote | URL.
3. Part C table: School | Cell | Column | Shown now | Stated on the page? (Yes / No / Could not open) | Quote | URL.
4. "Final change list": one line for each cell that should change, in exactly this format so it can be applied directly:
School | Tab | Cell | Column | Current value | New value (or BLANK) | Source URL | Exact quote
Include only changes where an acceptable page supports the new value, or where no acceptable page supports the current one.
5. "Still unverified": rows you could not confirm either way, so I know what is left.
6. Anything newer you noticed along the way that contradicts the workbook (a coach change, a renamed venue, a new sponsor), with a URL.
