"""Verification workbook for the Big 12 travel estimates: one row per game with ESPN links, a per-school summary with
FY2025 team travel spend and cost per mile, and the method and sources. Output: slides/travel/Big12_Team_Travel_FY2025.xlsx"""
import csv,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
FN='Aptos Narrow'; F=Font(name=FN,size=9); FB=Font(name=FN,size=9,bold=True); FH=Font(name=FN,size=9,bold=True,color='FFFFFF')
FL=Font(name=FN,size=9,color='0000FF',underline='single'); FHC=Font(name=FN,size=9,color='0000FF'); FG=Font(name=FN,size=9,color='000000')
BLK=PatternFill('solid',fgColor='000000'); THIN=Side(style='thin',color='000000')
G=list(csv.DictReader(open('data/travel/games.csv',encoding='utf-8'))); SM=list(csv.DictReader(open('data/travel/summary.csv',encoding='utf-8')))
FRS={}
for r in csv.DictReader(open('data/frs_detail.csv',encoding='utf-8')):
    if r['fiscal_year']=='2025' and r['line_id']=='28': FRS[r['school']]=r
SP={'football':'Football (2024 season)','mbb':"Men's basketball (2024-25)",'wbb':"Women's basketball (2024-25)"}; COL={'football':'football','mbb':'mens_basketball','wbb':'womens_basketball'}
wb=openpyxl.Workbook(); wb.remove(wb.active)
def prep(ws,title):
    ws.sheet_view.showGridLines=False; ws['B2']='SMASHSPORTS'; ws['B2'].font=Font(name='Montserrat',size=11,bold=True); ws['B3']=title; ws['B3'].font=FB
    ws.column_dimensions['A'].width=1; ws.column_dimensions['B'].width=2
def header(ws,labels):
    for j,h in enumerate(labels):
        c=ws.cell(6,3+j,h); c.font=FH; c.fill=BLK; c.alignment=Alignment(horizontal='center',vertical='center'); c.border=Border(top=THIN,bottom=THIN)
    ws.row_dimensions[6].height=24
def widths(ws,ws_):
    for j,w in enumerate(ws_): ws.column_dimensions[openpyxl.utils.get_column_letter(3+j)].width=w
# Summary
ws=wb.create_sheet('Summary'); prep(ws,'Big 12 team travel, FY2025: estimated miles from the schedules against reported team travel spend')
header(ws,['School','Sport','Games','Home','Away','Neutral site','Road trips','Estimated round-trip miles','FY2025 team travel spend (MFRS line 28)','Cost per mile','Cost per road trip','ESPN schedule'])
r=7
for s in SM:
    f=FRS.get(s['school']); spend=int(f[COL[s['sport']]]) if f else None
    vals=[s['school'],SP[s['sport']],int(s['games']),int(s['home']),int(s['away']),int(s['neutral']),int(s['trips']),int(s['round_trip_miles'])]
    for j,v in enumerate(vals): c=ws.cell(r,3+j,v); c.font=F if j<2 else FG; c.number_format='#,##0'
    c=ws.cell(r,11,spend if spend is not None else '--'); c.font=FHC if spend is not None else F; c.number_format='$#,##0'
    L=openpyxl.utils.get_column_letter
    ws.cell(r,12,f'=IF(ISNUMBER(K{r}),K{r}/J{r},"--")').number_format='$#,##0'; ws.cell(r,13,f'=IF(ISNUMBER(K{r}),K{r}/I{r},"--")').number_format='$#,##0'
    for cc in (12,13): ws.cell(r,cc).font=F
    c=ws.cell(r,14,'ESPN schedule'); c.hyperlink=s['schedule_url']; c.font=FL
    r+=1
last=r-1; r+=1
for sp in ('football','mbb','wbb'):
    ws.cell(r,3,f'Big 12 average, {SP[sp]}').font=FB
    for cc,col in ((10,'J'),(11,'K'),(12,'L'),(13,'M')):
        c=ws.cell(r,cc,f'=IFERROR(AVERAGEIFS({col}7:{col}{last},D7:D{last},"{SP[sp]}",K7:K{last},">0"),"--")'); c.font=FB; c.number_format='$#,##0' if cc>10 else '#,##0'
    r+=1
ws.cell(r+1,3,'Spend is blank for Baylor, BYU and TCU: private schools that do not publish an NCAA report. Averages cover the 13 schools with reported spend, as on the slides.').font=F
widths(ws,[16,24,7,7,7,10,10,16,22,12,14,16]); ws.freeze_panes='E7'; ws.auto_filter.ref=f'C6:N{last}'
# Games
ws=wb.create_sheet('Games'); prep(ws,'Every regular-season game, including Big 12 championship games, with the venue and estimated miles')
header(ws,['School','Sport','Date','Opponent','Site','Venue','City','State','Game note','One-way miles from campus','Counted as a new trip','Round-trip miles counted','ESPN game page'])
for j,g in enumerate(G):
    r=7+j; vals=[g['school'],SP[g['sport']],g['date'],g['opponent'],g['site'],g['venue'],g['city'],g['state'],g['note'] or '--',int(g['one_way_miles']),('--' if g['site']=='Home' else ('Yes' if g['trip_start']=='yes' else 'No, same trip as the game before')),int(g['round_trip_miles'])]
    for k,v in enumerate(vals): c=ws.cell(r,3+k,v); c.font=F; c.number_format='#,##0' if isinstance(v,int) else 'General'
    c=ws.cell(r,15,'ESPN game'); c.hyperlink=g['game_url']; c.font=FL
widths(ws,[16,24,11,30,9,34,18,8,44,12,22,12,12]); ws.freeze_panes='E7'; ws.auto_filter.ref=f'C6:O{6+len(G)}'
# Method
ws=wb.create_sheet('Method and Sources'); prep(ws,'How the estimates were built, and what the NCAA report counts as team travel')
LINES=[('Seasons','FY2025 runs July 2024 to June 2025, so football is the 2024 season and basketball is 2024-25.'),
 ('Games included','Every regular-season game and the Big 12 championship games (the football championship on 7 Dec 2024 in Arlington, and the men\'s and women\'s Big 12 tournaments in Kansas City). Bowl games, the NCAA tournaments, the NIT and the WBIT are left out.'),
 ('Why post-season is left out','The NCAA report puts post-season travel on other lines. Line 28 (team travel) covers "competition related to preseason and regular season", with the note "Expenses related to post-season play should be included in Categories 41 or 42 respectively." Line 41 (post-season football) says "Entries should not include conference tournaments or championships", so conference championship travel stays in line 28.'),
 ('NCAA reimbursement','Confirmed: the NCAA pays team travel to its own championships. Its 2024-25 Division I policy says "The NCAA will spend more than $100 million to transport student-athletes, teams, officials and support personnel", with air travel booked and billed through the NCAA\'s travel agency and per diem reimbursed after the event. Conference tournaments are not NCAA championships and are paid by the school (or the conference).'),
 ('Schedules','ESPN team schedules (links on each row). Home, away and neutral site as ESPN lists them.'),
 ('Distance','Straight-line (great-circle) miles from the campus (IPEDS coordinates) to the venue city (US Census 2024 place coordinates; a few venues abroad or outside the Census list placed by their city), doubled for the round trip. Consecutive games in the same city with no home game between them (a holiday tournament, the Big 12 tournament) count as one trip. Road swings (two road games in a row in different cities) are priced as separate trips from campus, so miles are somewhat overstated for schools that chain road games.'),
 ('Spend','NCAA MFRS FY2025, line 28 team travel, by sport column, as compiled by Sportico. The line also includes preseason travel and hotel stays before home games, which the mileage does not capture, so cost per mile is an indicator, not a true per-mile cost.'),
 ('Sources','ESPN schedules: espn.com team schedule pages. NCAA report definitions: University of Illinois FY2025 NCAA MFRS report (same form for every school). NCAA travel policy: 2024-25 Division I Championships Transportation and Per Diem Policies.')]
for j,(a,b) in enumerate(LINES):
    ws.cell(7+j,3,a).font=FB; c=ws.cell(7+j,4,b); c.font=F; c.alignment=Alignment(wrap_text=True,vertical='top'); ws.row_dimensions[7+j].height=48
c=ws.cell(7+len(LINES)+1,3,'NCAA 2024-25 travel policy'); c.font=FL; c.hyperlink='https://ncaaorg.s3.amazonaws.com/championships/resources/travel/2024-25D1Champs_TravelPolicies.pdf'
c=ws.cell(7+len(LINES)+2,3,'Illinois FY2025 NCAA report (definitions)'); c.font=FL; c.hyperlink='https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/fightingillini.com/documents/2026/1/29/FY25_IL_NCAA_Full_Report__Revised_1-22-26_.pdf'
ws.column_dimensions['C'].width=24; ws.column_dimensions['D'].width=120
wb.save('slides/travel/Big12_Team_Travel_FY2025.xlsx'); print('rows',len(G))
