const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, LevelFormat, AlignmentType } = require('docx');
const F = 'Arial';
const t = (text, o = {}) => new TextRun({ text, font: F, size: 20, ...o });
const P = (children, o = {}) => new Paragraph({ children, ...o });
const donor = (name, school) => P([t(name, { bold: true, size: 22 }), t(`  (${school})`, { color: '555555' })], { numbering: { reference: 'bul', level: 0 }, spacing: { before: 160 } });
const path = (member, conf, text) => P([t(member, { bold: true }), t(` [${conf}] `, { color: '555555' }), t(text)], { numbering: { reference: 'bul', level: 1 } });
const note = (text) => P([t(text, { italics: true, color: '555555', size: 18 })], { numbering: { reference: 'bul', level: 1 } });
const C = 'Confirmed', S = 'Strong inference', H = 'Hypothesis';
const ch = [];
ch.push(P([t('Smash Sports: priority booster connection paths', { bold: true, size: 36 })], { heading: HeadingLevel.TITLE }));
ch.push(P([t('Shortlist of priority donors and the Smash team members connected to them, with the documented path to each. Only paths that reach the booster directly or through someone outside the school are shown; routes that would need the school\'s own AD or president to make the introduction are excluded. Confidence in brackets: Confirmed = both named in the same document or quoted about each other; Strong inference = documented overlap at the same organisation or deal, or a second-degree path with both edges documented; Hypothesis = documented but unverified overlap. Research only; no outreach made. 2 November 2026.', { italics: true, size: 18 })], { spacing: { after: 200 } }));

ch.push(donor('John Condos', 'LSU, Tier 1 — LSU Board of Supervisors; Medicis Pharmacy, Lake Charles'));
ch.push(path('Evan Richter', S, 'Via Gov. Jeff Landry, who appointed Condos to the LSU board (March 2026) and to the Superdome commission, has received $150,000+ from him, and publicly endorsed the Smash Sports plan to Yahoo (March 2026). Richter, who ran the Project Rudy campus meetings and the Dallas summit, approaches through the Governor\'s office; Joey Smith can warm the political side.'));
ch.push(path('Kevin Mayer', S, 'Same Landry bridge, principal to principal: Yahoo names Mayer with Richter and Staggs as leaders of the plan Landry endorsed, and Landry is Condos\' appointer. No Mayer–Landry meeting is documented.'));
ch.push(note('Context: LSU is standing up a company to hold SEC/ESPN broadcast revenue and sell up to 20% to outside investors; Condos is a board vote on that structure. The LSU President Rousse route is on file but excluded as school-side.'));

ch.push(donor('Holden Spaht', 'LSU, Tier 1 — Managing Partner, Thoma Bravo; LSU\'s lead NIL financier'));
ch.push(path('Evan Richter', H, 'Software-PE peer: Thoma Bravo (Spaht) and Insight Partners (Richter\'s former firm) have co-owned Conga since May 2020, with Spaht and Insight MD Nikitas Koutoupes on its board. Richter approaches Spaht directly as a fellow Insight alumnus and Smash co-managing partner, or through the Insight Conga deal team, and can reference Landry\'s public backing of the Smash plan and LSU\'s own media-revenue vehicle.'));
ch.push(path('Kevin Mayer', H, 'Harvard Business School alumni overlap (Spaht HBS MBA, roughly 2001–03; Mayer HBS 1990; no overlapping years) plus the same Landry/LSU framing. Weak on its own; use alongside Richter.'));
ch.push(note('Note: Spaht is Dartmouth and HBS, not Stanford; Morgan Stanley and Thomas H. Lee before Thoma Bravo. Former LSU AD Scott Woodward (Swarbrick\'s Lead1 colleague) is on file as a former-official bridge.'));

ch.push(donor('Rick Kueber', 'Louisville, Tier 1 — Glow Brands (Sun Tan City, Planet Fitness franchisee); 502Circle NIL match'));
ch.push(note('No outside path identified. Every documented route runs through Louisville AD Josh Heird (ACC AD briefed on Project Rudy; thanked Glow Brands for the 2024 NIL match). No PE sponsor, lender, board or political-giving link to any Smash member was found.'));

ch.push(donor('Kathy Koster', 'Kansas State, Tier 1 — Koster family / American Implement (John Deere dealerships); 2026 stadium-lighting leadership gift'));
ch.push(path('Mags Kala', H, 'Via Paul Edgerley: Bain Capital managing director 1990–2016 and now senior advisor (overlapping Kala\'s Bain Capital Consumer years), a 1978 K-State graduate and one of the university\'s largest donors ($20M to the College of Business, Edgerley Family Deanship, KSU Foundation trust board executive committee). Kala asks Edgerley, as a fellow Bain alumnus and leading K-State benefactor, to introduce the Kosters. The Edgerley–Koster personal edge is not documented; both are top-tier K-State donors, and Edgerley\'s athletics giving could not be confirmed from the K-State athletics donor page.'));
ch.push(note('Routes via K-State AD Gene Taylor and President Linton are on file but excluded as school-side. Identity: Kathy is the widow of Duane Koster (d. Oct 2025); son Chad Koster is CEO of American Implement.'));

ch.push(donor('Arte Moreno', 'Arizona, Tier 1 — Angels owner; Outdoor Systems founder; Arizona athletics donor since the 1980s'));
ch.push(path('Tom Staggs', S, 'Disney sold the Anaheim Angels to Moreno in 2003 while Staggs was Disney\'s Senior EVP and CFO; Staggs signed and certified the May 2003 10-Q disclosing the agreement with Moreno. Staggs approaches directly, citing the sale; no personal negotiation between them is documented (Disney used Lehman Brothers; Anaheim Sports reported to Paul Pressler).'));
ch.push(note('Also on file: Gordon Gee via Ken Kendrick (fellow Baseball Hall of Fame director; WVU benefactor Gee knows directly) and Kevin Mayer via the 2019 Fox RSN divestiture Moreno tried to buy into.'));

ch.push(donor('Chris Ackerley', 'Arizona, Tier 1 — Ackerley Partners / Ackerley Sports Group, Seattle; Kraken minority owner; UA alumnus'));
ch.push(path('Evan Richter', H, 'Disney-alumni and sports-investing overlap: Richter is ex-Disney (Innovation) and Ackerley sits on the ESH Acquisition Corp board with former Disney Parks executives Al Weiss and Thomas Wolber, while Ackerley Sports Group invests in sports, media and technology. No document names Richter with Ackerley, so Richter should go in alongside the stronger Smash paths below.'));
ch.push(note('Also on file (stronger): Chris Bevilacqua, Confirmed — Ackerley Partners and Bevilacqua are both named selling CSTV stockholders in CBS\'s 2006 SEC filing; Tom Staggs, Strong inference — via Al Weiss and Thomas Wolber, who ran Disney Parks units under Staggs; Ndamukong Suh via Cliff Avril (Lions teammate, Leeds United co-investor); Steve Pagliuca via David Bonderman or John Fish. Background only: Dawit Wondimagegn shares Lakeside School and nine LinkedIn mutuals.'));

ch.push(donor('Humberto Lopez', 'Arizona, Tier 1 — HSL Properties, Tucson; UA\'s leading athletics benefactor; NIL-collective co-founder'));
ch.push(path('Gordon Gee', H, 'Shared public advocacy: Gee testified at Chairman Cruz\'s June 3, 2026 Senate Commerce hearing on the Protect College Sports Act, and Lopez is listed in the committee\'s support packet as "National Board of Advisors & Benefactor, University of Arizona". Gee approaches directly, citing the shared campaign and Big 12 ties (Gee chaired the Big 12 board executive committee while Arizona joined). Kitchy Cook can warm the Cruz/Commerce side: FEC shows Lopez gave to Cruz\'s Senate committee in Nov 2024 and $25K to the RNC in 2025. Caution: the bill\'s August 2026 revision targets super-league structures.'));
ch.push(note('The route via UA President Garimella (Gee\'s former Big 12 board colleague; Lopez sat on the search committee that chose him) is on file but excluded as school-side.'));

ch.push(donor('Bill Hendrix', 'Clemson, Tier 1 — Former Clemson trustees chair; ex-Remington Arms CEO, Clayton Dubilier & Rice; first athletics cornerstone donor'));
ch.push(path('Jack Swarbrick', S, 'Via Dan Radakovich, who as Clemson AD designed the cornerstone-gift plan that Hendrix anchored (Swinney pitched him at Kiawah) and who was Swarbrick\'s fellow ACC AD 2013–21 and LEAD1 colleague; Radakovich left Clemson in 2021, retired as Miami AD in June 2026 and now runs the FBS ADA, so the ask does not go through Clemson. Alternative bridge: Jim Clements, who thanked Hendrix by name for the 2014 gift and sat on the CFP Board of Managers while Swarbrick sat on the CFP Management Committee; Clements retired from Clemson in Dec 2025.'));
ch.push(note('Also on file: Gordon Gee via Jim Clements (Gee succeeded Clements at WVU and they were CFP board colleagues). Hendrix\'s son Jim Hendrix sits on the Clemson University Foundation board.'));

ch.push(donor('Jim Brown and Candace Brown', 'Clemson, Tier 1 — Synergi Partners, Florence SC; largest gift in IPTAY history'));
ch.push(note('No Smash member on your list. On file: Jack Swarbrick or Gordon Gee via retired President Jim Clements, who praised the Browns in the 2022 gift release (Strong inference / Hypothesis). Routes via AD Graham Neff are school-side. Flag: FITSNews has reported ERC-related federal suits and an investigation involving Synergi; the Browns are not named as defendants.'));

ch.push(donor('Charlie Loudermilk', 'UNC, Tier 1 — Aaron\'s founder (deceased Aug 2022); family and foundation now steward the UNC relationship'));
ch.push(note('No outside path on your list. On file: Steve Pagliuca via Atlanta Hawks CEO Steve Koonin, who sits on the Atlanta Police Foundation board chaired by son Robin Loudermilk (Hypothesis). The UNC AD Cunningham routes are school-side. Approach the R. Charles Loudermilk Sr. Foundation (Robin Loudermilk, president; Lisa DeGolian, executive director).'));

ch.push(donor('John Preyer', 'UNC, Tier 1 — Restoration Systems co-founder; former UNC trustees chair (resigned Jan 2026); led the Belichick hire'));
ch.push(note('No outside path identified. Every documented route runs through UNC\'s AD or chancellor, and Preyer clashed publicly with AD Cunningham in 2024. He is out of office, so a direct approach is possible; his public positions (ACC financial model "would cause real concern", a well-funded collective is "essential") are useful framing.'));

ch.push(donor('David Miller', 'SMU, Tier 2 — EnCap Investments co-founder; SMU trustee (board chair 2022–26); funded SMU\'s ACC entry'));
ch.push(path('Gordon Gee', S, 'Via Oliver Luck, the consultant SMU hired for its realignment campaign, who sat beside Miller in the ACC and Pac-12 meetings. Luck was WVU athletic director until Dec 2014 and Gee became WVU president in Jan 2014, so Gee was Luck\'s boss for most of that year. Gee asks Luck to introduce Miller; no direct Miller–Gee contact is documented.'));
ch.push(note('Also on file: Jack Swarbrick via ACC Commissioner Jim Phillips (Miller negotiated SMU\'s entry with Phillips face to face; Phillips sat with Swarbrick on the CFP Management Committee and is reported open to the Smash model). Miller\'s quotes on media rights and NIL are in the main file.'));

ch.push(donor('Jeff Crawford', 'Colorado, Tier 3 — RMI, Denver; CU\'s largest one-time athletics gift; son of media investor Gordon Crawford'));
ch.push(path('Kevin Mayer', S, 'Via Gordon "Gordy" Crawford, Jeff\'s father, president of the Crawford Family Foundation on which Jeff is treasurer. Gordon was Paley Center vice chair alongside Bob Iger (2006) and is trustee emeritus; Mayer has been a Paley trustee since Nov 2023 and appeared on a 2006 Paley panel as a Disney EVP; the foundation is an annual Paley donor. Mayer reaches Gordon through the Paley board (CEO Maureen Reidy or chairman Frank Bennack can facilitate), then Jeff.'));
ch.push(note('Also on file: Gordon Gee directly (CU president 1985–90, Jeff\'s graduating class; sat on the Big 12 board that admitted CU in 2023) and Tom Staggs via Gordon Crawford\'s Disney-era investor relationship.'));

ch.push(donor('Britt Brockman', 'Kentucky, Tier 3 — Ophthalmologist; UK Board of Trustees chair; signed the memo creating Champions Blue LLC'));
ch.push(note('No direct outside path on your list. Brockman is best reached alongside Joe Craft (below): the two are UK\'s governance chair and lead athletics donor, and UK\'s Champions Blue athletics LLC (chaired by President Capilouto; Mitch Barnhart non-voting) is the structure Smash would be discussing. Routes via Barnhart and Capilouto are school-side. Brockman does not chair Champions Blue.'));

ch.push(donor('Joe Craft', 'Kentucky, Tier 3 — Alliance Resource Partners chairman/CEO; UK\'s largest athletics donor; husband of former Ambassador Kelly Craft'));
ch.push(path('Kitchy Cook', S, 'Via Sen. Ted Cruz\'s office, where Cook was a Commerce Committee legislative aide. Cruz endorsed Kelly Craft for Kentucky governor in May 2023, campaigned with her at Louisville and Richmond rallies, and defended her in 2019; Kelly Craft calls him "my friend, Sen. Cruz", and Courthouse News reported Alliance Resource money flowing to Cruz among senators who advanced her UN nomination. Cook reaches Kelly Craft through Cruz-office alumni, then Joe.'));
ch.push(path('Joey Smith', H, 'Trump-administration overlap: Smith was Treasury Director of Operations (March 2017–May 2020) while Kelly Craft was Ambassador to Canada and then UN Ambassador; a second route is Ronna McDaniel, who joined the Alliance Resource board in Dec 2024 and, as RNC chair, named the Crafts co-chairs of the RNC Presidential Trust in Jan 2024 — Smith\'s Romney/RNC background makes her a plausible bridge, but no document places Smith with McDaniel or the Crafts.'));

ch.push(donor('Tilman Fertitta', 'Houston, Tier 2 — Fertitta Entertainment / Landry\'s / Houston Rockets; UH regent emeritus; U.S. Ambassador to Italy'));
ch.push(path('Tom Staggs', H, 'Landry\'s has operated Rainforest Cafe, T-REX and Yak & Yeti inside Disney parks since the late 1990s, overlapping Staggs\'s tenure as chairman of Walt Disney Parks and Resorts (2010–15). Staggs approaches via the Disney Parks operating and real-estate executives who managed the Landry\'s concepts at Disney Springs; no Staggs–Fertitta meeting is documented.'));
ch.push(path('Steve Pagliuca', S, 'Fellow NBA governors 2017–25 (Fertitta as Rockets owner; Pagliuca as Celtics co-owner and Board of Governors member), and Front Office Sports (Dec 2025) names both as rival bidders for the WNBA\'s Connecticut Sun. Pagliuca approaches owner to owner; Pagliuca\'s Atalanta role is a further opening while Fertitta is Ambassador in Rome.'));
ch.push(path('Chris Bevilacqua', H, 'Fertitta sold Golden Nugget Online Gaming to DraftKings in May 2022 and remains one of its largest shareholders; DraftKings later acquired Bevilacqua\'s SimpleBet. Bevilacqua approaches via DraftKings leadership (Jason Robins) as a common counterparty, or joins a Gee-led approach.'));
ch.push(path('Mags Kala', H, 'Through Steve Pagliuca (PagsGroup) using the NBA governor and Connecticut Sun overlaps above; no Kala–Fertitta contact is documented.'));
ch.push(note('Also on file (strongest): Gordon Gee, Confirmed — Fertitta told CBS Sports he "basically hosted" Gee\'s Nov 2015 UH campus visit during Big 12 expansion; Ndamukong Suh, Strong inference — named FAST Acquisition advisor on the 2021 Fertitta Entertainment SPAC merger (bridge Doug Jacob).'));

ch.push(donor('Jimmy Rane', 'Auburn, Tier 3 — Great Southern Wood / YellaWood founder; Auburn trustee since 1999'));
ch.push(path('Kevin Mayer', H, 'YellaWood has been presenting sponsor of SEC Network\'s TrueSouth since 2018, streamed on ESPN+, which sat inside the Disney Direct-to-Consumer segment Mayer chaired (2018–20). Mayer approaches via ESPN/SEC Network sponsorship-sales leadership that manages the YellaWood account; the HBS link also helps — Rane completed HBS\'s OPM program (1984) and credits it with reshaping his company.'));
ch.push(note('Routes via Auburn AD John Cohen, Playfly\'s Auburn Sports Properties and President Chris Roberts are on file but excluded as school-side. Rane\'s May 2026 quote: "we\'re in the professional sports business."'));

ch.push(donor('Bruce Arians', 'Virginia Tech, Tier 1 — Former Buccaneers and Cardinals head coach; VT alumnus and donor; on VT\'s 2025 head-coach search committee'));
ch.push(path('Ndamukong Suh', C, 'Arians was Suh\'s head coach for all three Buccaneers seasons (2019–21) including Super Bowl LV, and each has publicly praised the other: Arians called Suh "a big, big part" of the defense in 2020 and praised his "tremendous leadership" in 2021; Suh said Arians told him on the parade podium "you\'re not going anywhere". Suh calls Arians directly; Arians remains a Buccaneers senior consultant.'));

ch.push(donor('Wendell H. Murphy', 'NC State, Tier 2 — Murphy Family Farms founder; former state senator; NC State trustee; Murphy Center naming donor'));
ch.push(note('No Smash member on your list. On file: Barry Snyder via David C. Nelson, a Smithfield Foods co-director with Murphy 2008–13 who was a Credit Suisse managing director 1997–2007 (Hypothesis; Snyder must confirm he knows Nelson). The AD Boo Corrigan route is school-side. Family: son Dell Murphy and daughter-in-law Wendy Floyd Murphy (UNC System Board of Governors chair) run Murphy Family Ventures.'));

ch.push(donor('Brian McMurray', 'NC State, Tier 2 — McMurray Fabrics / ATEX Technologies; endowed the NC State AD position'));
ch.push(note('No outside path identified. The only documented route is through AD Boo Corrigan, whose position the McMurrays endowed, which is school-side. No investor, board, political-giving or civic link to a Smash member was found.'));

ch.push(donor('Bill Heavener', 'Florida, Tier 3 — The Heavener Company / Full Sail University; UF trustee; Heavener Football Training Center'));
ch.push(path('Joey Smith', S, 'Same 2012 campaign: Heavener was named a State Co-Chair of Mitt Romney\'s Florida Finance Team (Oct 2011) while Smith was the Romney campaign\'s Director of Candidate Advance and Trip Director. Smith approaches through the Romney Florida network — fellow co-chairs Mori Hosseini (now UF Board chair) or Brian Ballard — rather than cold.'));
ch.push(path('Kevin Mayer', H, 'Full Sail University ran a joint venture with ESPN — the Full Sail Sports Lab Powered by ESPN (opened Nov 2010) and a 2011 ESPN Wide World of Sports partnership, with a Disney corporate release in 2013 — during Mayer\'s years as Disney EVP Corporate Strategy. Mayer approaches via the ESPN/Disney Orlando executives who ran the venture; names are not in the public releases.'));
ch.push(path('Tom Staggs', H, 'Same Full Sail–ESPN overlap: ESPN Wide World of Sports is a Walt Disney World property in the Parks and Resorts division Staggs chaired 2010–15. Staggs approaches via former Parks/ESPN Wide World of Sports leadership who signed the 2011 agreement.'));
ch.push(note('Flag: Heavener is a named defendant in a federal False Claims Act suit over Full Sail job-placement figures (unsealed May 2025). The AD Scott Stricklin route is school-side.'));

ch.push(donor('Gary Condron', 'Florida, Tier 3 — The Conlan Company founder; largest donor in Gator Boosters history; Florida Victorious advisory board'));
ch.push(note('No outside path identified. The only documented route is through UF AD Scott Stricklin (fellow Gator Boosters director), which is school-side. No Disney, Jaguars/PGA Tour, banking or political link to a Smash member was found; Condron\'s July 2025 NIL quote ("deep, dark hole ... unless we get some guardrails") is useful framing.'));

ch.push(donor('Vinny Lobdell', 'Syracuse, Tier 3 — HealthWay co-founder (sold to AE Industrial 2021); lead men\'s basketball donor and NIL organiser'));
ch.push(path('Kevin Mayer', H, 'Via John Wildhack, Syracuse athletic director 2016–June 2026, under whom all of Lobdell\'s athletics giving took place. Wildhack spent 36 years at ESPN, rising to EVP Programming and Production (2007–16) while Mayer was Disney\'s chief strategy officer; Mayer and Staggs also advised Disney on ESPN in 2023. Wildhack is now retired from Syracuse, so Mayer asks him personally to introduce Lobdell; no document ties Mayer to Wildhack directly.'));
ch.push(path('Tom Staggs', H, 'Same Wildhack bridge: as Disney COO (2015–16) Staggs had every segment head, including ESPN\'s senior team, reporting jointly to him and Iger. Staggs approaches Wildhack as a fellow Disney/ESPN executive of that era, then Wildhack to Lobdell.'));
ch.push(note('Note: Lobdell is not a Syracuse trustee. The Chancellor Haynie and trustee Steven Barnes (Bain Capital/Celtics) routes are on file but excluded as school-side.'));

const doc = new Document({
  styles: { default: { document: { run: { font: F, size: 20 } } } },
  numbering: { config: [{ reference: 'bul', levels: [
    { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 360 } } } },
    { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 900, hanging: 360 }, spacing: { before: 40 } } } },
  ] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } }, children: ch }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync('/home/user/sportsnews/research/Smash_Priority_Booster_Paths.docx', b); console.log('wrote', b.length); });
