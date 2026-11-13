# Step 1: browser agent (run this first)

Upload `P4_Benchmarking_Double_Check_List.xlsx`, then paste everything below the line.

---

I've attached an Excel file, P4_Benchmarking_Double_Check_List.xlsx. It lists cells in a college athletics benchmarking workbook that need a human-quality check before the workbook goes to my firm's partners. Your job is to check every row on the first tab, "Double-check", by opening real web pages in the browser. Accuracy matters far more than speed. A row marked "could not confirm" is fine; a guess is not.

Today's date matters: treat "now" as the day you run this, and say what that date is at the top of your answer.

HOW THE TAB IS LAID OUT
Each row is one cell in the workbook. The columns are: # (row number), Why it is here, School, Tab, Cell, Column (what the value is), Shown now (the value currently in the workbook), What to look at (what was uncertain), and Source (the page the value came from, if any).

WHAT TO DO FOR EACH ROW, BY THE "Why it is here" COLUMN
1. "Could not re-read the source": an automated tool could not open the page. Open the Source link in the browser and find the value. If that page does not state it, find the school's current official page that does (athletics site facility page, media guide, record book, official release). Tell me whether the page states exactly the value in "Shown now".
2. "Re-check on the day you send": these are things that may have changed in the last few days, mostly head coaches. Search current news and the school's official athletics site and tell me who holds the job today, whether they are interim or permanent, and the date of the most recent announcement.
3. "Weaker source": the value was confirmed, but only on a weak or conflicting source. Look for a stronger source that states the same figure, or one that contradicts it. Stronger means: the school's or university's own page or release, an executed contract or board document, a state salary database, Associated Press, ESPN, Sports Business Journal, Sportico, The Athletic, Front Office Sports, or an established newspaper.
4. "Your call": these are decisions for me, not for you. Do not recommend a policy. Only check the factual claim in "What to look at" (for example, that a page gives a base salary and a supplemental payment separately but no total) and tell me whether that description is accurate.

RULES
- Open the page yourself. Never answer from memory and never rely on a search-result snippet or an AI summary.
- Never compute, add up, average, round or infer a figure, with one exception: head coach pay in the workbook is base salary plus supplemental compensation, so if a page gives those two parts for the season and they add up to the value shown, that is CONFIRMED (quote both parts). Retention payments, signing bonuses and performance bonuses are not part of the figure. If a page says "five-year deal" but gives no end year, the end year is "not stated". If a page says "about" or "more than", quote that wording.
- Do not use Wikipedia, wiki mirrors, USA Today's coaching salary or athletics finance databases (or any article that attributes its figure to them), fan blogs, team fan networks, message boards or stadium-guide sites.
- For every row give a short exact quote from the page (under 40 words) that contains the figure or name, and the full URL of the page you actually read. If the page shows a date, give it.
- If a page is behind a login or paywall that I am signed into in this browser, use it. If you cannot get in, say so and move on.
- Do every row. Do not stop early, do not skip rows, and do not edit the file.

WHAT TO GIVE ME BACK
First, one table with one line per row, in row order, with these columns:
# | School | Column | Shown now | Verdict | Value on the page | Exact quote | URL you read | Page date | Note

Verdict must be one of: CONFIRMED (the page states exactly the value shown), DIFFERENT (the page states another value; put it in "Value on the page"), NOT STATED (no acceptable page states the value itself), COULD NOT OPEN, or FACT CHECK ONLY (for "Your call" rows: say whether the description is accurate).

Then, under the table:
- "Changes I would make": only the DIFFERENT rows, each as School, Tab, Cell, Column, new value, URL, quote.
- "Should be blank": the NOT STATED rows, with what the page does say.
- "Could not check": the COULD NOT OPEN rows, with what you tried.
- Anything newer you noticed along the way that contradicts the workbook (a coach change, a renamed stadium, a new sponsor), with a URL.
