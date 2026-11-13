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
ITEMS=[  # (group, school, column, what to check)
 ('Could not re-read the source','Michigan State','Stadium capacity','The official stadium page would not load. An older article gives 75,005.'),
 ('Could not re-read the source','Michigan State','Stadium last major renovation year','The official pages would not load and no other source states the year.'),
 ('Could not re-read the source','Minnesota','Stadium capacity','The official page would not load; the AP calls it a 50,000-seat stadium.'),
 ('Could not re-read the source','Kansas','MMR term (years)','The trade article is behind a login; the 10-year term appeared only in its headline.'),
 ('Could not re-read the source','Alabama','Stadium last major renovation year','The official page would not load.'),
 ('Could not re-read the source','Alabama','Arena capacity','The official page would not load; older articles give 15,032.'),
 ('Could not re-read the source','Alabama','Apparel partner','The cited release showed only its title, which does not name Nike.'),
 ('Could not re-read the source','Florida','Arena year opened','The official page would not load.'),
 ('Could not re-read the source','Oklahoma','Arena year opened','The official page would not load.'),
 ('Could not re-read the source','Georgia Tech','Stadium naming rights start year','The ESPN report (dated 2023) announces the deal but does not state a start year; 2023 is the announcement year.'),
 ('Re-check on the day you send','NC State','Head football coach','ESPN and CBS reported on 12 November that Philip Rivers is expected to be named head coach, with trustees due to finalize it on 13 November. The cell still shows the interim coach.'),
 ('Re-check on the day you send','Maryland','Head football coach','Interim since Mike Locksley was fired on 21 October; a national search is under way. Florida State and Baylor football and Oregon men\'s basketball also show interim coaches.'),
 ('Re-check on the day you send','Rutgers',"Head men's basketball coach",'Steve Pikiell still holds the title but is away for medical treatment; Brandin Knight is acting head coach. Decide which name to show.'),
 ('Re-check on the day you send','Florida','Arena naming rights partner','Trustees approved the Tower Hill naming on 10 November 2026: five years from July 2026 with a five-year option. The value is not disclosed; an unattributed 22.5 million figure is circulating and was not used.'),
 ('Your call','Louisville','FB HC annual guaranteed compensation','Policy question, 19 coach pay cells are now blank. In about half, the page states the base and the supplemental pay for this season separately but never the total (here 6,300,000 base plus a 250,000 retention payment). Under the no-computed-figures rule they are blank; say if you want base plus supplemental entered as a sum. The Changes tab lists all 19.'),
 ('Your call','Syracuse','Stadium naming rights start year','Policy question, 12 deals show the year the agreement was announced as the start year because the source gives no effective date (as agreed for Washington\'s arena). Source Log notes mark each one. Say if you would rather blank them.'),
 ('Your call','Oklahoma State','FB HC contract end year','Policy question, contract end years follow the stated expiry date. Here the page says the deal runs through 31 January 2031, so the cell shows 2031 although the last season is 2030. Texas Tech (2033), Kentucky (2031) and Tennessee (2030) football are the same.'),
 ('Your call','California','Fiscal year','Cal has posted a fiscal 2025 statement (revenue 153,043,652; expenses 165,382,286), but in its own layout without MFRS line numbers and with debt service outside the expense total. It was not used; Cal stays on Sportico fiscal 2024. Say if you want it.'),
 ('Your call','Stanford','MMR partner','Shown as Learfield. Stanford\'s own partnerships page lists only university staff and Learfield describes its role as national sales and radio, so this may now be in-house. BYU\'s cell is blank for the same reason.'),
 ('Your call','Miami (FL)','Apparel partner','Shows Nike, which takes over in July 2027; adidas is the outfitter through June 2027. Ole Miss is the reverse: Nike is shown and adidas takes over in July 2027. Decide whether to show the current or the incoming partner.'),
 ('Your call','Arkansas','Stadium naming rights total value','The 70,000,000 comes from a newspaper\'s reading of a redacted contract; it is unclear whether it covers the 14-year agreement or the 13 naming years (the cell uses 13). The stadium name is shown as CommunityAmerica Razorback Stadium ahead of its 2027 start, as with Washington.'),
 ('Your call','Louisville','Arena capacity','Changed from 22,090 to 22,000 because the official page says only "22,000-seat". No page that could be read states 22,090.'),
 ('Your call','Texas Tech','Arena capacity','Two official figures conflict: 15,098 in the record book (kept) and 15,050 on a university page.'),
 ('Your call','Maryland','Stadium capacity','Changed from 51,802 to 46,185 per the official facility page; the record book still prints 51,802.'),
 ('Your call','Michigan State','MMR term (years)','The 15-year term and 150,000,000 total come from the 2016 agreement signed with Fox Sports, reported by a local radio site. Playfly now holds the rights and no source documents the transfer.'),
 ('Your call','Ohio State','Arena naming rights partner','Value City is still on the building, but its parent filed for bankruptcy and Ohio State plans to phase the name out. The 12,500,000 total is a one-time contribution, not an annual fee.'),
 ('Your call','California','Apparel expires','By its recorded start and term the Nike agreement ends in 2026. No renewal was looked for in this pass.'),
 ('Your call','Texas','Apparel annual value','The earlier 6,500,000 was the annual cash payment only. The cell now divides the reported 250,000,000 total by the 15-year term.'),
 ('Your call','Missouri','Stadium capacity','Blank. The official page gives 57,321 only as approximate for 2025, and the 2026 expansion takes it to "nearly 65,000" with no exact figure published.'),
 ('Your call','Georgia','Varsity sports sponsored','21 is from a 2023 article; a September 2026 article refers to 20 NCAA-sponsored teams, which is a narrower count.'),
 ('Weaker source','North Carolina','MBB HC annual guaranteed compensation','Three outlets say 7.5 million in the first year; one local station says 8 million.'),
 ('Weaker source','Illinois','FB HC annual guaranteed compensation','One outlet states 7.7 million as the annual salary; the school release says salary "would begin at 7.7 million".'),
 ('Weaker source','Ohio State','MBB HC annual guaranteed compensation','One article says 2.5 million a year; another calls it a five-year, 11.5 million deal.'),
 ('Weaker source','Arizona State','MBB HC annual guaranteed compensation','The page says the salary "begins at 3.5 million" without naming the season.'),
 ('Weaker source','Michigan State','FB HC annual guaranteed compensation','The only source is the student newspaper.'),
 ('Weaker source','Rutgers','MBB HC contract end year','The only page stating it carries wire copy from February 2023 on a minor outlet.'),
 ('Weaker source','Kentucky','Jersey patch partner','Confirmed only on a regional sports site; no official release was found.'),
 ('Weaker source','Ohio State','Jersey patch start year','The source is Bleacher Report.'),
 ('Weaker source','Kentucky','Arena naming rights annual value','The release describes 1.5 million as the naming-rights portion of a larger annual investment.'),
 ('Weaker source','North Carolina','MMR annual value','12.6 million is the stated average over 12 years; the contract\'s fee for 2026-27 is 13,750,000.'),
 ('Weaker source','West Virginia','Apparel partner','Nike is kept from an old source because nothing newer was found either way. The same applies to Virginia, Florida State, Syracuse, Wake Forest and Pittsburgh apparel.'),
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
rows=[]
for n,(grp,sch,col,why) in enumerate(ITEMS,1):
    t,addr,val=NEW[(sch,col)]; lg=LOG.get((sch,col),{})
    rows.append([n,grp,sch,t,addr,col,fmt(val),why,lg.get('URL') if str(lg.get('URL','')).startswith('http') else '--'])
sheet(out,'Double-check',['#','Why it is here','School','Tab','Cell','Column','Shown now','What to look at','Source'],rows,[4,26,16,12,7,34,22,150,60])
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
    rows.append([sch,nt,naddr,m,fmt(v),fmt(now),outcome,so.cell(r,10).value,so.cell(r,11).value])
sheet(out,'31 dollar figures',['School','Tab','Cell','Column','Value before','Shown now','Outcome','Source it came from','Source link'],rows,[16,12,7,36,16,16,90,50,60])
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
