"""Add-on slides for the v13 deck: team travel maps (total, football, basketball), cost per mile, and alternative views
of other slides. Built on the masters of the user's deck so the slides can be pasted straight in.
Usage: python3 scripts/travel/build_travel_slides.py <user deck.pptx> <out.pptx>"""
import sys,json,math,csv,copy,statistics
from pptx import Presentation
from pptx.util import Inches,Pt,Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE,MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
from pptx.chart.data import CategoryChartData,XyChartData
from pptx.enum.chart import XL_CHART_TYPE,XL_LEGEND_POSITION,XL_LABEL_POSITION
from lxml import etree
SRC,OUT=sys.argv[1],sys.argv[2]
DATA={}
INK=RGBColor(0,0,0); GREY=RGBColor(0x59,0x59,0x59); LINE=RGBColor(0x9D,0xC3,0xE6); KSU=RGBColor(0x51,0x28,0x88); LIGHT=RGBColor(0xBF,0xBF,0xBF)
F='Montserrat'
LOGO=json.load(open('slides/logos/logos.json'))
def money(v): return ('-' if v<0 else '')+(f'${abs(v)/1e6:.1f}M' if abs(v)>=1e6 else f'${abs(v)/1e3:,.0f}K')
# ---------------- data
SCH=['Arizona','Arizona State','Cincinnati','Colorado','Houston','Iowa State','Kansas','Kansas State','Oklahoma State','Texas Tech','UCF','Utah','West Virginia']
SUM={(r['school'],r['sport']):r for r in csv.DictReader(open('data/travel/summary.csv',encoding='utf-8'))}
FRS={}
for r in csv.DictReader(open('data/frs_detail.csv',encoding='utf-8')):
    if r['fiscal_year']=='2025' and r['conference']=='Big 12': FRS[(r['school'],r['section'],r['line_id'])]=r
def frs(s,sec,lid,col='total'):
    r=FRS.get((s,sec,lid)); return int(r[col]) if r else 0
TRAV={s:dict(total=frs(s,'Expense','28'),fb=frs(s,'Expense','28','football'),mbb=frs(s,'Expense','28','mens_basketball'),wbb=frs(s,'Expense','28','womens_basketball'),
             fbm=int(SUM[(s,'football')]['round_trip_miles']),mbbm=int(SUM[(s,'mbb')]['round_trip_miles']),wbbm=int(SUM[(s,'wbb')]['round_trip_miles']),
             fbt=int(SUM[(s,'football')]['trips']),mbbt=int(SUM[(s,'mbb')]['trips']),wbbt=int(SUM[(s,'wbb')]['trips'])) for s in SCH}
for s,t in TRAV.items():
    t['fbcpm']=t['fb']/t['fbm']; t['mbbcpm']=t['mbb']/t['mbbm']; t['wbbcpm']=t['wbb']/t['wbbm']
# ---------------- map projection (same as scripts/travel/map_base.py)
MM=json.load(open('slides/travel/map_meta.json'))
la1,la2,la0,lo0=map(math.radians,(29.5,45.5,23.0,-96.0)); nn=(math.sin(la1)+math.sin(la2))/2; CC=math.cos(la1)**2+2*nn*math.sin(la1); r0=math.sqrt(CC-2*nn*math.sin(la0))/nn
def proj(lat,lon):
    la,lo=math.radians(lat),math.radians(lon); r=math.sqrt(CC-2*nn*math.sin(la))/nn; th=nn*(lo-lo0); return r*math.sin(th), r0-r*math.cos(th)
HD={r['UNITID']:r for r in csv.DictReader(open('data/ipeds/extracted/HD2024.csv',encoding='utf-8-sig',errors='replace'))}
MS={s['name']:s for s in json.load(open('data/schools_master.json'))}
MAP=dict(x=0.95,y=1.47,w=8.1); MAP['h']=MAP['w']*MM['aspect']
def pos(s):
    h=HD[MS[s]['unitid']]; x,y=proj(float(h['LATITUDE']),float(h['LONGITUD']))
    return MAP['x']+(x-MM['x0'])/(MM['x1']-MM['x0'])*MAP['w'], MAP['y']+(MM['y1']-y)/(MM['y1']-MM['y0'])*MAP['h']
# logo centre offset from the campus dot (inches) and which side the label goes
# logo centre on the slide (inches) and which side of the logo the label goes; a thin line joins it to the campus dot
OFF={'Utah':(2.30,3.05,'L'),'Arizona State':(1.85,4.35,'L'),'Arizona':(2.05,5.55,'L'),'Colorado':(3.35,2.55,'L'),'Kansas State':(4.45,2.15,'L'),
     'Iowa State':(5.55,2.15,'R'),'Kansas':(6.15,2.95,'R'),'Cincinnati':(7.35,2.45,'R'),'West Virginia':(8.05,3.35,'R'),'Oklahoma State':(5.85,4.55,'R'),
     'Texas Tech':(3.65,5.45,'L'),'Houston':(5.05,6.30,'R'),'UCF':(8.20,5.25,'R')}
# ---------------- deck scaffolding on the user's masters
prs=Presentation(SRC); old=[s for s in prs.slides]; LAY=old[14].slide_layout
def frame(title,sub):
    s=prs.slides.add_slide(LAY)
    for ph in s.placeholders:
        if ph.placeholder_format.idx==0: ph.text=title
        elif ph.placeholder_format.idx==1: ph.text=sub
    pan=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(0.35),Inches(1.35),Inches(9.31),Inches(5.53)); pan.adjustments[0]=0.025
    pan.fill.solid(); pan.fill.fore_color.rgb=RGBColor(255,255,255); pan.line.fill.background(); pan.shadow.inherit=False; pan.name='Panel'
    s.shapes._spTree.remove(pan._element); s.shapes._spTree.insert(2,pan._element)
    return s
def text(s,t,x,y,w,h,size=7,bold=False,color=INK,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,name=None):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame; tf.word_wrap=True
    for m in ('margin_left','margin_right','margin_top','margin_bottom'): setattr(tf,m,0)
    tf.vertical_anchor=anchor
    lines=t if isinstance(t,list) else [t]
    for i,ln in enumerate(lines):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.alignment=align
        parts=ln if isinstance(ln,list) else [(ln,bold,color,size)]
        for seg in parts:
            tx,b,c,sz=seg; r=p.add_run(); r.text=tx; r.font.name=F; r.font.size=Pt(sz); r.font.bold=b; r.font.color.rgb=c
    if name: tb.name=name
    return tb
def footnote(s,t): text(s,t,0.35,7.12,6.75,0.3,6,color=GREY,name='Footnote')
def legend_box(s,lines,x=0.58,y=1.45,w=2.6):
    h=0.12+0.2*len(lines); r=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h)); r.fill.solid(); r.fill.fore_color.rgb=RGBColor(255,255,255)
    r.line.color.rgb=INK; r.line.width=Pt(0.75); r.shadow.inherit=False
    text(s,lines,x+0.1,y+0.06,w-0.2,h-0.1,7)
def logo(s,school,cx,cy,size=0.34):
    s.shapes.add_picture(f"slides/logos/{LOGO[school]['file']}",Inches(cx-size/2),Inches(cy-size/2),Inches(size),Inches(size)).name=f'Logo: {school}'
def travel_map(title,sub,label,foot):
    s=frame(title,sub)
    s.shapes.add_picture('slides/travel/us_map.png',Inches(MAP['x']),Inches(MAP['y']),Inches(MAP['w']),Inches(MAP['h'])).name='US map'
    for sc in SCH:
        lx,ly,side=OFF[sc]; px,py=pos(sc)
        ln=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(px),Inches(py),Inches(lx),Inches(ly)); ln.line.color.rgb=LIGHT; ln.line.width=Pt(0.75)
        d=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(px-0.035),Inches(py-0.035),Inches(0.07),Inches(0.07)); d.fill.solid(); d.fill.fore_color.rgb=KSU if sc=='Kansas State' else INK; d.line.fill.background(); d.shadow.inherit=False
        logo(s,sc,lx,ly)
        lines=label(sc); hl=sc=='Kansas State'
        w=1.2; x=lx+0.21 if side=='R' else lx-0.21-w
        text(s,[[ (ln_[0],ln_[1],KSU if hl else INK,ln_[2]) ] for ln_ in lines],x,ly-0.17,w,0.4,align=PP_ALIGN.LEFT if side=='R' else PP_ALIGN.RIGHT,anchor=MSO_ANCHOR.MIDDLE,name=f'Label: {sc}')
    footnote(s,foot)
    return s
FOOT_T="Source: NCAA Membership Financial Reporting System (MFRS) reports, FY2025, as compiled by Sportico, line 28 (team travel). Big 12 excludes Baylor, BYU and TCU (private schools with no public report)."
FOOT_M="Miles: ESPN schedules (2024 football; 2024-25 basketball), regular season and Big 12 championship games; straight-line round trip from campus to each road or neutral site, a multi-game tournament counted once. Spend: FY2025 MFRS line 28, which includes preseason travel and hotel stays before home games and excludes post-season play. Excludes Baylor, BYU and TCU."
# 1. total team travel
tot=[TRAV[s]['total'] for s in SCH]
travel_map('TEAM TRAVEL: BIG 12',f"Big 12 departments spent {money(statistics.mean(tot))} on team travel on average in FY2025 (median {money(statistics.median(tot))}). Kansas spent the most at {money(TRAV['Kansas']['total'])} and Houston the least at {money(TRAV['Houston']['total'])}; Kansas State spent {money(TRAV['Kansas State']['total'])}.",
    lambda sc:[(money(TRAV[sc]['total']),True,9),('team travel, all sports',False,6)],FOOT_T)
# 2. football
fbm=[TRAV[s]['fbm'] for s in SCH]; fbc=[TRAV[s]['fbcpm'] for s in SCH]
travel_map('TEAM TRAVEL, FOOTBALL: BIG 12',f"Big 12 football teams travelled an estimated {statistics.mean(fbm):,.0f} miles round trip on average in the 2024 season, at a median ${statistics.median(fbc):,.0f} per mile. Kansas State travelled {TRAV['Kansas State']['fbm']:,} miles at ${TRAV['Kansas State']['fbcpm']:,.0f} per mile.",
    lambda sc:[(f"{TRAV[sc]['fbm']:,} mi",True,8),(f"${TRAV[sc]['fbcpm']:,.0f} per mile",False,7)],FOOT_M)
# 3. basketball
mm=[TRAV[s]['mbbm'] for s in SCH]; wm=[TRAV[s]['wbbm'] for s in SCH]
travel_map("TEAM TRAVEL, BASKETBALL: BIG 12",f"Big 12 men's basketball teams travelled an estimated {statistics.mean(mm):,.0f} miles on average in 2024-25 (median ${statistics.median([TRAV[s]['mbbcpm'] for s in SCH]):,.0f} per mile) and women's teams {statistics.mean(wm):,.0f} miles (median ${statistics.median([TRAV[s]['wbbcpm'] for s in SCH]):,.0f} per mile).",
    lambda sc:[(f"M: {TRAV[sc]['mbbm']:,} mi  ${TRAV[sc]['mbbcpm']:,.0f}/mi",True,6.5),(f"W: {TRAV[sc]['wbbm']:,} mi  ${TRAV[sc]['wbbcpm']:,.0f}/mi",False,6.5)],FOOT_M)
# 4. cost per mile, three ranked panels
s=frame('TEAM TRAVEL COST PER MILE: BIG 12',f"Median cost per mile is ${statistics.median(fbc):,.0f} for football, ${statistics.median([TRAV[x]['mbbcpm'] for x in SCH]):,.0f} for men's basketball and ${statistics.median([TRAV[x]['wbbcpm'] for x in SCH]):,.0f} for women's. Short-trip schools rank highest, since charter and hotel costs don't shrink with distance.")
def bar_panel(s,x,title,key):
    data=sorted(SCH,key=lambda q:-TRAV[q][key]); DATA.setdefault('cost_per_mile',{})[title]=[(q,round(TRAV[q][key],2)) for q in data]; cd=CategoryChartData(); cd.categories=[LOGO[q]['short'] for q in data]; cd.add_series(title,[round(TRAV[q][key]) for q in data])
    gf=s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED,Inches(x),Inches(1.75),Inches(3.0),Inches(4.95),cd); ch=gf.chart
    ch.has_legend=False; ch.has_title=True; ch.chart_title.text_frame.text=title
    tp=ch.chart_title.text_frame.paragraphs[0]; tp.runs[0].font.size=Pt(9); tp.runs[0].font.bold=True; tp.runs[0].font.name=F
    pl=ch.plots[0]; pl.gap_width=40; pl.has_data_labels=True; dl=pl.data_labels; dl.number_format='"$"#,##0'; dl.number_format_is_linked=False; dl.font.size=Pt(7); dl.font.name=F; dl.position=XL_LABEL_POSITION.OUTSIDE_END
    ser=pl.series[0]; ser.format.fill.solid(); ser.format.fill.fore_color.rgb=INK
    for i,q in enumerate(data):
        if q=='Kansas State': pt=ser.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb=KSU
    ca=ch.category_axis; ca.reverse_order=True; ca.tick_labels.font.size=Pt(7); ca.tick_labels.font.name=F; ca.format.line.color.rgb=LIGHT
    va=ch.value_axis; va.visible=False; va.has_major_gridlines=False; va.maximum_scale=max(TRAV[q][key] for q in SCH)*1.3; va.minimum_scale=0
bar_panel(s,0.5,'Football','fbcpm'); bar_panel(s,3.55,"Men's basketball",'mbbcpm'); bar_panel(s,6.6,"Women's basketball",'wbbcpm')
footnote(s,"Cost per mile is FY2025 MFRS line 28 spend for the sport divided by estimated regular-season round-trip miles (ESPN schedules; straight-line from campus). Kansas State highlighted. Excludes Baylor, BYU and TCU (no public report).")
# ---------------- alternative views of other slides
import openpyxl
wb=openpyxl.load_workbook('Power4_Athletic_Department_Benchmarking.xlsx',data_only=True); ws=wb['All Schools']; H={ws.cell(6,c).value:c for c in range(3,ws.max_column+1)}
ROW={ws.cell(r,3).value:r for r in range(7,ws.max_row+1)}
def v(sc,h):
    x=ws.cell(ROW[sc],H[h]).value; return x if isinstance(x,(int,float)) and not isinstance(x,bool) else None
FRS25=[q for q in ROW if ws.cell(ROW[q],H['Conference']).value in ('ACC','Big Ten','Big 12','SEC','Independent') and ws.cell(ROW[q],H['Financial data type']).value=='MFRS' and ws.cell(ROW[q],H['Fiscal year']).value==2025]
B12=[q for q in FRS25 if ws.cell(ROW[q],H['Conference']).value=='Big 12']; REST=[q for q in FRS25 if q not in B12]
# 5. revenue mix, 100% stacked
MIX=[('Ticket sales',['Ticket sales revenue']),('Media rights',['Media rights revenue']),('NCAA and conference',['NCAA and conference distributions']),('Contributions',['Contributions revenue']),
     ('Licensing and sponsorship',['Licensing, advertising and sponsorship revenue']),('Direct school support and student fees',['Direct institutional support','Student fees'])]
def mixrow(q):
    tr=v(q,'Total operating revenue'); parts=[sum(v(q,h) or 0 for h in hs) for _,hs in MIX]; return [p/tr for p in parts]+[1-sum(parts)/tr]
ords=sorted(B12,key=lambda q:-mixrow(q)[3])
_rk=[q for q in ords].index('Kansas State')+1
s=frame('REVENUE MIX: BIG 12',f"Contributions are {mixrow('Kansas State')[3]:.0%} of Kansas State's revenue ({['','1st','2nd','3rd','4th'][_rk]} in the Big 12), and it gets no direct school support or student fees. Houston, Cincinnati and UCF get a third or more of their revenue that way.")
cd=CategoryChartData(); cd.categories=[LOGO[q]['short'] for q in ords]
COLS=[RGBColor(0,0,0),RGBColor(0x40,0x40,0x40),RGBColor(0x7F,0x7F,0x7F),KSU,RGBColor(0xA6,0xA6,0xA6),RGBColor(0x9D,0xC3,0xE6),RGBColor(0xD9,0xD9,0xD9)]
names=[n for n,_ in MIX]+['Other']
for j,nm in enumerate(names): cd.add_series(nm,[round(mixrow(q)[j],4) for q in ords])
DATA['revenue_mix']=dict(schools=ords,series=names,shares=[[round(mixrow(q)[j],4) for q in ords] for j in range(len(names))],dollars=[[round((sum(v(q,h) or 0 for h in MIX[j][1]) if j<len(MIX) else v(q,'Total operating revenue')-sum(sum(v(q,h) or 0 for h in hs) for _,hs in MIX))) for q in ords] for j in range(len(names))])
gf=s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED_100,Inches(0.55),Inches(1.5),Inches(8.9),Inches(5.25),cd); ch=gf.chart
ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout=False; ch.legend.font.size=Pt(7); ch.legend.font.name=F
pl=ch.plots[0]; pl.gap_width=40; pl.overlap=100
for j,ser in enumerate(pl.series):
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb=COLS[j]
    if names[j]=='Contributions':
        ser.data_labels.show_value=True; ser.data_labels.number_format='0%'; ser.data_labels.number_format_is_linked=False; ser.data_labels.font.size=Pt(7); ser.data_labels.font.color.rgb=RGBColor(255,255,255); ser.data_labels.font.name=F
ch.category_axis.tick_labels.font.size=Pt(7); ch.category_axis.tick_labels.font.name=F; ch.value_axis.tick_labels.font.size=Pt(7); ch.value_axis.has_major_gridlines=False; ch.value_axis.tick_labels.number_format='0%'; ch.value_axis.tick_labels.number_format_is_linked=False
footnote(s,"Source: FY2025 MFRS reports as compiled by Sportico. Share of total operating revenue. Direct school support and student fees is MFRS lines 3 and 4. Indirect institutional support (line 6, the value of services the university provides, such as facilities and administration) is counted in Other, with guarantees, concessions, camps and endowment income. Excludes Baylor, BYU and TCU.")
# 6. where the Big 12 trails the rest of the Power 4
LINES=[('Media rights','Media rights revenue'),('Ticket sales','Ticket sales revenue'),('Contributions','Contributions revenue'),('Licensing and sponsorship','Licensing, advertising and sponsorship revenue'),('NCAA and conference','NCAA and conference distributions')]
b=[statistics.mean(v(q,h) or 0 for q in B12) for _,h in LINES]; r_=[statistics.mean(v(q,h) or 0 for q in REST) for _,h in LINES]; k=[v('Kansas State',h) or 0 for _,h in LINES]
gap=statistics.mean(v(q,'Total operating revenue') for q in REST)-statistics.mean(v(q,'Total operating revenue') for q in B12)
s=frame('WHERE THE BIG 12 TRAILS: REVENUE',f"The average Big 12 department takes in {money(gap)} a year less than the average school in the other Power 4 conferences. Media rights ({money(r_[0]-b[0])}) and ticket sales ({money(r_[1]-b[1])}) account for most of the gap.")
cd=CategoryChartData(); cd.categories=[n for n,_ in LINES]
cd.add_series(f'Rest of Power 4 average ({len(REST)} schools)',[round(x) for x in r_]); cd.add_series(f'Big 12 average ({len(B12)} schools)',[round(x) for x in b]); cd.add_series('Kansas State',[round(x) for x in k])
DATA['big12_gap']=dict(lines=[n for n,_ in LINES],series=[(f'Rest of Power 4 average ({len(REST)} schools)',[round(x) for x in r_]),(f'Big 12 average ({len(B12)} schools)',[round(x) for x in b]),('Kansas State',[round(x) for x in k])])
gf=s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED,Inches(0.55),Inches(1.5),Inches(8.9),Inches(5.25),cd); ch=gf.chart
ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout=False; ch.legend.font.size=Pt(8); ch.legend.font.name=F
pl=ch.plots[0]; pl.gap_width=60; pl.overlap=-10; pl.has_data_labels=True; dl=pl.data_labels; dl.number_format='"$"#,##0.0,,"M"'; dl.number_format_is_linked=False; dl.font.size=Pt(7); dl.font.name=F; dl.position=XL_LABEL_POSITION.OUTSIDE_END
for ser,c in zip(pl.series,(LIGHT,INK,KSU)): ser.format.fill.solid(); ser.format.fill.fore_color.rgb=c
ch.category_axis.reverse_order=True; ch.category_axis.tick_labels.font.size=Pt(8); ch.category_axis.tick_labels.font.name=F
ch.value_axis.visible=False; ch.value_axis.has_major_gridlines=False
footnote(s,"Source: FY2025 MFRS reports as compiled by Sportico or posted by the school. Averages cover the 13 Big 12 and 36 other Power 4 schools with a public FY2025 report. Left out: 12 private schools that do not publish one (including Notre Dame, Baylor, BYU and TCU), Pittsburgh (no public report located) and Florida, Georgia Tech, Maryland and UCLA (FY2024 only). Big 12 media rights average includes Cincinnati, which books its conference payout as conference distributions ($0 media rights).")
# 7. revenue against expenses
s=frame('REVENUE AGAINST SPENDING: BIG 12',f"Points above the line spent more than they took in. Kansas State had the largest surplus in the Big 12 ({money(v('Kansas State','Operating surplus (deficit)'))}) on one of the smallest budgets.")
cd=XyChartData(); ser=cd.add_series('Big 12 schools')
for q in B12: ser.add_data_point(v(q,'Total operating revenue')/1e6,v(q,'Total operating expenses')/1e6)
DATA['scatter']=[(q,v(q,'Total operating revenue'),v(q,'Total operating expenses'),v(q,'Operating surplus (deficit)')) for q in B12]
lo,hi=85,175; br=cd.add_series('Break-even'); br.add_data_point(lo,lo); br.add_data_point(hi,hi)
gf=s.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER,Inches(0.7),Inches(1.5),Inches(8.6),Inches(5.25),cd); ch=gf.chart; ch.has_legend=False
pts=ch.plots[0].series[0]; pts.marker.style=8; pts.marker.size=7; pts.marker.format.fill.solid(); pts.marker.format.fill.fore_color.rgb=INK; pts.format.line.fill.background()
for i,q in enumerate(B12):
    p=pts.points[i]; dlb=p.data_label; tf=dlb.text_frame; tf.text=LOGO[q]['short']; tf.paragraphs[0].runs[0].font.size=Pt(7); tf.paragraphs[0].runs[0].font.name=F
    dlb.position=XL_LABEL_POSITION.LEFT if q in ('Iowa State','Arizona','UCF') else XL_LABEL_POSITION.RIGHT
    if q=='Kansas State': p.marker.format.fill.solid(); p.marker.format.fill.fore_color.rgb=KSU; tf.paragraphs[0].runs[0].font.color.rgb=KSU; tf.paragraphs[0].runs[0].font.bold=True
bl=ch.plots[0].series[1]; bl.marker.style=None; bl.format.line.color.rgb=LINE; bl.format.line.dash_style=4; bl.smooth=False
from pptx.enum.chart import XL_MARKER_STYLE
bl.marker.style=XL_MARKER_STYLE.NONE
for ax,t_ in ((ch.category_axis,'Total operating revenue ($M)'),(ch.value_axis,'Total operating expenses ($M)')):
    ax.minimum_scale=lo; ax.maximum_scale=hi; ax.has_major_gridlines=False; ax.tick_labels.font.size=Pt(7); ax.tick_labels.font.name=F; ax.has_title=True; ax.axis_title.text_frame.text=t_
    r=ax.axis_title.text_frame.paragraphs[0].runs[0]; r.font.size=Pt(8); r.font.name=F; r.font.bold=False
footnote(s,"Source: FY2025 MFRS reports as compiled by Sportico. The dashed line is break-even (revenue equals expenses). Excludes Baylor, BYU and TCU.")
# 8. Kansas State against the Big 12 average
MET=[('Total revenue','Total operating revenue'),('Football revenue','Football revenue'),("Men's basketball revenue","Men's basketball revenue"),('Ticket sales','Ticket sales revenue'),('Media rights','Media rights revenue'),
     ('Contributions','Contributions revenue'),('Licensing and sponsorship','Licensing, advertising and sponsorship revenue'),('Total expenses','Total operating expenses'),('Coaching pay','Total coaching salaries and benefits'),
     ('Support staff pay','Support and administrative staff pay'),('Team travel','Team travel'),('Fundraising and marketing','Fundraising, marketing and promotion'),('Debt service','Annual debt service')]
idx=[(n,v('Kansas State',h)/statistics.mean(v(q,h) for q in B12 if v(q,h) is not None)) for n,h in MET]
s=frame('KANSAS STATE AGAINST THE BIG 12 AVERAGE',"Kansas State against the Big 12 average (100%): above on tickets, media, contributions and travel; well below on football revenue (69%), fundraising and marketing (38%) and debt service (74%).")
DATA['ksu_index']=[(n,round(x,4)) for n,x in idx]
cd=CategoryChartData(); cd.categories=[n for n,_ in idx]; cd.add_series('Kansas State as % of Big 12 average',[round(x,3) for _,x in idx])
gf=s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED,Inches(0.55),Inches(1.5),Inches(8.9),Inches(5.25),cd); ch=gf.chart; ch.has_legend=False; ch.has_title=False
pl=ch.plots[0]; pl.gap_width=50; pl.has_data_labels=True; dl=pl.data_labels; dl.number_format='0%'; dl.number_format_is_linked=False; dl.font.size=Pt(7); dl.font.name=F; dl.position=XL_LABEL_POSITION.OUTSIDE_END
ser=pl.series[0]; ser.format.fill.solid(); ser.format.fill.fore_color.rgb=KSU
for i,(_,x) in enumerate(idx):
    if x<1: pt=ser.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb=LIGHT
ch.category_axis.reverse_order=True; ch.category_axis.tick_labels.font.size=Pt(8); ch.category_axis.tick_labels.font.name=F
va=ch.value_axis; va.minimum_scale=0; va.maximum_scale=1.6; va.major_unit=0.5; va.tick_labels.number_format='0%'; va.tick_labels.number_format_is_linked=False; va.tick_labels.font.size=Pt(7); va.has_major_gridlines=True; va.major_gridlines.format.line.color.rgb=RGBColor(0xD9,0xD9,0xD9)
footnote(s,"Source: FY2025 MFRS reports as compiled by Sportico. Big 12 average of the 13 schools that file a public report (excludes Baylor, BYU and TCU). Purple: above the Big 12 average; grey: below.")
# ---------------- keep only the new slides
sldIdLst=prs.slides._sldIdLst
for sl in old:
    for sid in list(sldIdLst):
        if prs.slides.get(int(sid.get('id'))) is sl or sid.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')==prs.part.relate_to(sl.part,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide'):
            prs.part.drop_rel(sid.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')); sldIdLst.remove(sid); break
DATA['travel']={s:{k:(round(x,2) if isinstance(x,float) else x) for k,x in TRAV[s].items()} for s in SCH}; DATA['positions']={s:dict(zip(('lat','lon'),(float(HD[MS[s]['unitid']]['LATITUDE']),float(HD[MS[s]['unitid']]['LONGITUD'])))) for s in SCH}
json.dump(DATA,open('slides/travel/chart_data.json','w'),indent=1)
prs.save(OUT); print('saved',OUT,len(prs.slides),'slides')
