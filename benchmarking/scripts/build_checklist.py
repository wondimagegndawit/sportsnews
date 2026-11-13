"""Build P4_Benchmarking_Double_Check_List.xlsx: the short list of cells for the analyst to check by hand, the outcome
for each dollar figure that was first read from a search-result excerpt, and every cell changed by the source re-read.
Usage: python3 -I scripts/build_checklist.py <previous_workbook.xlsx> <previous_layout.json>"""
import openpyxl, warnings, json, re, sys, csv
warnings.simplefilter('ignore')
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter as L
F='Power4_Athletic_Department_Benchmarking.xlsx'
bv=openpyxl.load_workbook(F,data_only=True); lay=json.load(open('data/workbook_layout.json'))
av=openpyxl.load_workbook(sys.argv[1],data_only=True); lo=json.load(open(sys.argv[2]))
def index(wb,layout):
    d={}
    for t,lc in layout['conf_layout'].items():
        ws=wb[t]; H={ws.cell(6,c).value:c for c in range(3,ws.max_column+1)}
        for r in range(lc['first'],lc['last']+1):
            for h,c in H.items(): d[(ws.cell(r,3).value,h)]=(t,f'{L(c)}{r}',ws.cell(r,c).value)
    return d
NEW=index(bv,lay); OLD=index(av,lo)
sl=bv['Source Log']; SH={sl.cell(6,c).value:c for c in range(3,sl.max_column+1)}; LOG={}
for r in range(7,sl.max_row+1): LOG[(sl.cell(r,SH['School']).value,sl.cell(r,SH['Metric']).value)]={k:sl.cell(r,c).value for k,c in SH.items()}
def fmt(v): return f'{v:,.0f}' if isinstance(v,(int,float)) and not isinstance(v,bool) and abs(v)>=10000 else (f'{v:g}' if isinstance(v,float) else v)
# ---------- 1. double-check list ----------
ITEMS=[  # (group, school, column, what to check). Rows settled by the browser check of 2026-11-12 have been removed.
 ('Re-check on the day you send','NC State','Head football coach','Shown as Philip Rivers at your direction, with pay and contract end blank. WRAL reported on the morning of 13 November that NC State "will hire" him "pending approval of his contract by the university\'s Board of Trustees". No report of the vote was found that day, and the staff page (second link) still listed Todd Goebbel as interim head coach. Confirm the hire is official and add pay once terms are published.'),
 ('Re-check on the day you send','Maryland','Head football coach','Interim since 21 October; a national search is under way. Florida State and Baylor football and Oregon men\'s basketball also still show interim coaches on their official staff pages.'),
 ('Your call','Rutgers',"Head men's basketball coach",'The official staff page lists both: Steve Pikiell as head coach and Brandin Knight as acting head coach while Pikiell undergoes treatment. Decide which name to show.'),
 ('Your call','Syracuse','Stadium naming rights start year','Policy question, 13 deals show the year the agreement was announced as the start year because the source gives no effective date (as agreed for Washington\'s arena). Source Log notes mark each one. Say if you would rather blank them.'),
 ('Your call','Oklahoma State','FB HC contract end year','Policy question, contract end years follow the stated expiry date. The page says the deal runs through 31 January 2031, so the cell shows 2031 although the last season is 2030. Texas Tech (2033), Kentucky (2031) and Tennessee (2030) football are the same.'),
 ('Your call','California','Fiscal year','Cal has posted a fiscal 2025 statement (revenue 153,043,652; expenses 165,382,286), but in its own layout with debt service below the operating expense total. It was not used; Cal stays on Sportico fiscal 2024. Say if you want it.'),
 ('Your call','Stanford','MMR partner','Shown as Learfield. Learfield\'s page says it handles national sales for Stanford, and Stanford\'s partnerships page lists its own staff; no page says the rights are wholly in-house. BYU\'s cell is blank for a similar reason.'),
 ('Your call','Miami (FL)','Apparel partner','Shows Nike, which starts in July 2027; adidas is the outfitter through June 2027. Ole Miss is the reverse: adidas starts on 1 July 2027. Decide whether to show the current or the incoming partner.'),
 ('Your call','Arkansas','Stadium naming rights total value','The newspaper reports 70,000,000 over the 14-year agreement, of which 13 years carry the stadium name. The cell shows the 70,000,000 total and the 13 naming years, and no annual value is derived from them. The stadium name is shown ahead of its 2027 start, as with Washington.'),
 ('Your call','North Carolina','MMR annual value','12,600,000 is the stated average. It matches the 2018 contract: royalty fees of 144,750,000 over 12 years, plus a 3,000,000 signing bonus and 4,000,000 of capital subsidies, come to 151,750,000, or 12.65 million a year. The royalty fees alone average 12.06 million, and the June 2023 amendment lists 13,500,000 for 2026-27. Decide whether this column should hold the contract average or the current-year fee.'),
 ('Your call','West Virginia','FB HC annual guaranteed compensation','Blank. AP gives 3.5 million for the first season rising 100,000 a season, which would make 2026 3.6 million, but no page states the 2026 figure. Oklahoma State men\'s basketball is blank for the same reason. USA Today lists 3,600,000 for 2025, but its note says that includes a 100,000 relocation stipend, so it was not used. Say if you want stated schedules like these applied.'),
 ('Your call','Louisville','Arena capacity','The official page says only "22,000-seat"; the earlier 22,090 is not stated on any page that could be read.'),
 ('Your call','Ohio State','Arena naming rights partner','Value City is still on the building, but Ohio State plans to phase the name out with no timetable. The 12,500,000 total is a contribution for the name, not an annual fee.'),
 ('Your call','Kentucky','Arena naming rights annual value','The release says the naming-rights portion will be 1.5 million "upon completion of the renovation", within a wider investment averaging 4.1 million a year, so it may not have applied from the first year.'),
 ('Your call','Georgia','Varsity sports sponsored','21 is from a 2023 article ("Georgia\'s 21 sports teams"). The same article refers to "20 NCAA-sanctioned sports" because equestrian is not an NCAA sport. Decide which count to show.'),
 ('Your call','Kentucky','MBB HC annual guaranteed compensation','22 head coach pay cells (6 football, 16 men\'s basketball) and this one are from USA Today\'s coaches\' pay tables, used where no other source gave a figure. The latest tables cover the 2025 football season and the 2025-26 basketball season, one season earlier than the other pay figures, so scheduled raises since then are not reflected (Kentucky\'s contract rises 250,000 a year). Source Log shows the season on each one. Say if you would rather blank them.'),
 ('Worth a glance','California','Apparel partner','Nike is kept as the partner, but the three-year agreement that began on 1 July 2023 reached the end of its stated term in mid-2026 and no renewal has been found, so the start year and term are now blank. Confirm Cal is still outfitted by Nike.'),
 ('Worth a glance','Florida State','Apparel partner','Nike is shown with no dates or values. The cited page is a 2005 school article; later terms (a 2013 extension with an option through 2022-23) were found only on fan sites, and no current agreement was located.'),
 ('Your call','Maryland','Apparel total value','Blank. The second reviewer reports that the Washington Post (14 June 2024) calls it a "12-year, $98 million contract", while the board minutes say the deal is "projected to provide $98 million". The Post page could not be opened to check it. Decide whether a projected total is acceptable.'),
 ('Your call','Illinois','FB HC contract end year','Shows 2030 from "a new six-year contract through the end of the 2030 season". The same release says the agreement runs "to June 30, 2031", and other coaches use the year of the stated expiry date, which would make this 2031.'),
 ('Worth a glance','Kansas','MMR term (years)','The school\'s release confirms a 10-year extension, but the page displays the date 21 July 2022 while its address carries 22 May 2024. Confirm which extension is current.'),
 ('Worth a glance','Alabama','Arena capacity','The official page text and the 2026 game notes say 13,474, but a capacities table on the same page shows a main-floor total of 14,474.'),
]
THIN=Side(style='thin',color='000000'); FN='Aptos Narrow'
def sheet(wb,title,headers,rows,widths):
    ws=wb.create_sheet(title); ws.sheet_view.showGridLines=False
    ws.column_dimensions['A'].width=1; ws.column_dimensions['B'].width=2
    for j,h in enumerate(headers):
        c=ws.cell(row=2,column=3+j,value=h); c.font=Font(name=FN,size=9,color='FFFFFF'); c.fill=PatternFill('solid',fgColor='000000'); c.border=Border(top=THIN,bottom=THIN); c.alignment=Alignment(horizontal='center')
        ws.column_dimensions[L(3+j)].width=widths[j]
    for i,row in enumerate(rows):
        for j,v in enumerate(row):
            c=ws.cell(row=3+i,column=3+j,value=v); c.font=Font(name=FN,size=9)
            if isinstance(v,str) and v.startswith('http'): c.hyperlink=v; c.font=Font(name=FN,size=9,color='0000FF',underline='single')
    ws.freeze_panes='C3'; return ws
out=openpyxl.Workbook(); out.remove(out.active)
# links for rows whose cell has no source of its own, and a second page to open where two pages matter
LINK={('West Virginia','FB HC annual guaranteed compensation'):'https://sportsdata.usatoday.com/ncaa/salaries/football/coach/team/3423',
      ('Maryland','Apparel total value'):'https://www.washingtonpost.com/sports/2024/06/14/under-armour-maryland-athletics-deal/'}
SECOND={('NC State','Head football coach'):'https://gopack.com/sports/football/coaches',
        ('Maryland','Head football coach'):'https://umterps.com/news/2026/10/21/football-maryland-athletics-michael-locksley-mutually-agree-to-part-ways',
        ('California','Fiscal year'):'https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/calberk.sidearmsports.com/documents/2026/2/23/FY25_UCB_NCAA_SRE_Final___POSTED_.pdf',
        ('Stanford','MMR partner'):'https://www.learfield.com/partner/stanford-cardinal/',
        ('Miami (FL)','Apparel partner'):'https://olemisssports.com/news/2026/10/7/athletics-adidas-ole-miss-announce-7-year-partnership-beginning-in-2027',
        ('North Carolina','MMR annual value'):'https://s3.us-east-2.amazonaws.com/sidearm.nextgen.sites/unc.sidearmsports.com/documents/2025/1/27/UNC_Learfield_MMR_Amendment_June_2023_-_Executed60.pdf',
        ('Kentucky','MBB HC annual guaranteed compensation'):'https://www.kentucky.com/sports/college/kentucky-sports/article311606298.html',
        ('Maryland','Apparel total value'):'https://www.usmd.edu/content/regents/minutes/2024/20240529-FC-PublicClosedSession.pdf',
        ('Kansas','MMR term (years)'):'https://www.sportsbusinessjournal.com/Daily/Closing-Bell/2022/07/21/KU-partnership-with-Learfield/',
        ('Ohio State','Arena naming rights partner'):'https://ohiostatebuckeyes.com/news/2026/9/16/mens-basketball-complete-20-game-big-ten-schedule-announced'}
rows=[]
for n,(grp,sch,col,why) in enumerate(ITEMS,1):
    t,addr,val=NEW[(sch,col)]; lg=LOG.get((sch,col),{})
    rows.append([n,grp,sch,t,addr,col,fmt(val),why,lg.get('URL') if str(lg.get('URL','')).startswith('http') else LINK.get((sch,col),'--'),SECOND.get((sch,col),'--')])
sheet(out,'Double-check',['#','Why it is here','School','Tab','Cell','Column','Shown now','What to look at','Link to open','Second link, where one helps'],rows,[4,26,16,12,7,34,22,150,60,60])
# ---------- 2. dollar figures first read from a search-result excerpt ----------
so=av['Source Log']; rows=[]
for r in range(7,so.max_row+1):
    sch,m,v=so.cell(r,3).value,so.cell(r,5).value,so.cell(r,6).value; note=str(so.cell(r,13).value or '')+' '+str(so.cell(r,10).value or '')
    if v in (None,'--') or not re.search(r'search (snippet|summary|excerpt)',note,re.I) or not re.search(r'annual value|total value|compensation',str(m)): continue
    t,addr,_=OLD[(sch,m)]; nt,naddr,now=NEW[(sch,m)]; lg=LOG.get((sch,m),{})
    same=isinstance(lg.get('Value'),(int,float)) and abs(float(lg['Value'])-float(v))<1e-9
    if lg.get('Value') in (None,'--') and now!='--': outcome='Reported figure withdrawn; the cell now shows a formula from the other two terms. '+str(lg.get('Note'))[:220]
    elif lg.get('Value') in (None,'--'): outcome='Blanked: '+str(lg.get('Note'))[:260]
    elif same: outcome={'Re-read and confirmed':'Confirmed: the source page was re-read and states the figure','Found on source page':'Confirmed: the figure was found in the text of the source page'}.get(lg.get('Verification'),str(lg.get('Verification')))
    else: outcome='Corrected to '+fmt(lg['Value'])
    rows.append([sch,nt,naddr,m,fmt(v),fmt(now),outcome,so.cell(r,10).value,so.cell(r,11).value,lg.get('Source name') or '--',lg.get('URL') or '--'])
sheet(out,'31 dollar figures',['School','Tab','Cell','Column','Value before','Shown now','Outcome','Source it first came from','First source link','Source cited now','Link cited now'],rows,[16,12,7,36,16,16,90,50,60,50,60])
n31=len(rows)
# ---------- 3. every changed cell ----------
rows=[]
for k,(t,addr,now) in NEW.items():
    if k not in OLD: continue
    before=OLD[k][2]
    if before==now or (isinstance(now,float) and isinstance(before,(int,float)) and abs(now-before)<1e-9): continue
    lg=LOG.get(k,{}); kind='Blanked' if now=='--' else ('Filled' if before=='--' else 'Changed')
    rows.append([k[0],t,addr,k[1],fmt(before),fmt(now),kind,str(lg.get('Note') or 'Formula result; follows from another cell on this row')[:400],lg.get('URL') if str(lg.get('URL','')).startswith('http') else '--'])
rows.sort(key=lambda r:(r[6],r[0],r[3]))
sheet(out,'Changes',['School','Tab','Cell','Column','Before','After','Type','Reason or source statement','Source'],rows,[16,12,7,36,22,26,9,120,60])
out.save('P4_Benchmarking_Double_Check_List.xlsx')
import collections
print('double-check rows',len(ITEMS),'| dollar figures',n31,'| changes',len(rows),dict(collections.Counter(r[6] for r in rows)))
for r in out['Double-check'].iter_rows(min_row=3,values_only=True): print(' ',r[2],r[3:7],'|',r[9][:50] if r[9] else None)
print(collections.Counter(r[8][:9] for r in out['31 dollar figures'].iter_rows(min_row=3,values_only=True)))
