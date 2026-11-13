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
ITEMS=[  # (group, school, column, what to check). Rows the analyst settled on 13 November 2026 have been removed.
 ('Re-check on the day you send','NC State','Head football coach','Shown as Philip Rivers at your direction, with pay and contract end blank. WRAL reported on the morning of 13 November that NC State "will hire" him "pending approval of his contract by the university\'s Board of Trustees". No report of the vote was found that day, and the staff page (second link) still listed Todd Goebbel as interim head coach. Confirm the hire is official and add pay once terms are published.'),
 ('Re-check on the day you send','Maryland','Head football coach','Interim since 21 October; a national search is under way. Florida State and Baylor football and Oregon men\'s basketball also still show interim coaches on their official staff pages.'),
 ('Worth a glance','Indiana','FB HC total pay','Coach pay now comes from the Total Pay column of USA Today\'s tables: football 2025, men\'s basketball 2026 and 2025. The tables are one season old, so contracts signed since are not reflected. For 46 of the 92 cells another source gives a different figure for the current season, and the Source Log note on each cell quotes it. The largest gaps: Indiana football 8,300,000 against 13,200,000; Texas A&M football 7,000,000 against 10,750,000; Oklahoma football 7,552,750 against 10,000,000; Alabama football 10,250,000 against 12,500,000; Texas Tech football 4,554,960 against 6,500,000. Where USA Today has no figure for the current coach, the other source\'s figure is shown and the pay source type column says so.'),
 ('Your call','Illinois','FB HC contract end year','Now 2031, the year of the stated expiry date (30 June 2031). Other coaches whose sources give only a final season, such as "through the 2030 season", still show that season\'s year, because moving them forward a year would be an end year no page states. Say if you want every football contract described by its last season shown as the following year.'),
 ('Worth a glance','Arkansas','Stadium naming rights term (years)','Shows the full 14-year agreement, 2026 to 2040, with the 70,000,000 total. The stadium name itself starts in 2027. The annual value is blank because the newspaper\'s own average, "about $5.4 million", is not 70,000,000 divided by 14 (5,000,000). Say if you want 5,000,000 shown.'),
 ('Worth a glance','Maryland','Apparel total value','98,000,000 over 12 years through 2036, from the Washington Post passage you supplied; the page itself could not be opened by the build tools. The annual value (8,166,667) is a formula, total divided by term.'),
 ('Worth a glance','California','Total operating expenses','California now shows fiscal 2025 from the statement the school posted. Its expense total of 165,382,286 leaves out 8,474,702 of facilities debt service, which the statement lists below the total; other schools\' totals include debt service. Indirect institutional support and athletics-related debt are not on the statement and are blank.'),
 ('Worth a glance','Louisville','Arena capacity','22,090 is from Wikipedia at your direction, the only Wikipedia figure in the workbook. Louisville\'s own page says only "22,000-seat".'),
 ('Worth a glance','Ohio State','Arena naming rights partner','Shown as Value City Arena with the 12,500,000 contribution as the total value and no term or annual value. The article says the name is to be phased out with no timetable.'),
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
LINK={}
SECOND={('NC State','Head football coach'):'https://gopack.com/sports/football/coaches',
        ('Maryland','Head football coach'):'https://umterps.com/news/2026/10/21/football-maryland-athletics-michael-locksley-mutually-agree-to-part-ways',
        ('Indiana','FB HC total pay'):'https://sportsdata.usatoday.com/ncaa/salaries/mens-basketball/coach',
        ('Arkansas','Stadium naming rights term (years)'):'https://www.wholehogsports.com/news/2026/jun/30/contract-communityamerica-deal-with-arkansas-football-stadium-longer-than-announced/',
        ('Maryland','Apparel total value'):'https://www.usmd.edu/content/regents/minutes/2024/20240529-FC-PublicClosedSession.pdf',
        ('Louisville','Arena capacity'):'https://gocards.com/facilities/kfc-yum-center/7'}
# headers renamed on 13 November 2026; the earlier workbook and its Source Log use the old names
RENAME={'FB HC annual guaranteed compensation':'FB HC total pay','MBB HC annual guaranteed compensation':'MBB HC total pay 2026'}
OLDNAME={v:k for k,v in RENAME.items()}
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
    t,addr,_=OLD[(sch,m)]; m2=RENAME.get(m,m); nt,naddr,now=NEW[(sch,m2)]; lg=LOG.get((sch,m2),{})
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
    ko=(k[0],OLDNAME.get(k[1],k[1]))
    if ko not in OLD: continue
    before=OLD[ko][2]
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
