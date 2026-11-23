"""Two slides on the user's v13 masters: 2025 and 2026 average home football attendance for every Power 4 school
(68 incl. Notre Dame), ranked, coloured by conference. Values are D1.ticker as displayed:
2025 = '2025 Final Average' (data through Week 14), 2026 = '2026 Current Average' (through Week 11).
Also writes a think-cell style backup workbook.
Usage: python3 scripts/attendance/build_attendance_slides.py <user deck.pptx> <out.pptx> <backup.xlsx>"""
import sys,re,html,statistics
sys.path.insert(0,'scripts')
from schools import SCHOOLS
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE,XL_LEGEND_POSITION,XL_LABEL_POSITION,XL_TICK_LABEL_POSITION
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
SRC,OUT,XL=sys.argv[1:4]
F='Montserrat'; INK=RGBColor(0,0,0); GREY=RGBColor(0x59,0x59,0x59)
CONF=['SEC','Big Ten','Big 12','ACC','Independent']
COL={'SEC':RGBColor(0xFF,0xC0,0x00),'Big Ten':RGBColor(0x2E,0x75,0xB6),'Big 12':RGBColor(0x51,0x28,0x88),'ACC':RGBColor(0xED,0x7D,0x31),'Independent':RGBColor(0xA6,0xA6,0xA6)}
LABEL={'Independent':'Notre Dame (Ind.)'}
conf={s['name']:s['conf'] for s in SCHOOLS}
URL='https://www.d1ticker.com/{}-fbs-attendance-trends/'
def table(y,col):
    t=open(f'data/d1ticker/{y}-fbs-attendance-trends.html',encoding='utf-8',errors='replace').read()
    rows=[[html.unescape(re.sub(r'<[^>]+>','',c)).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>',tr,re.S)] for tr in re.findall(r'<tr[^>]*>(.*?)</tr>',t,re.S)]
    i=rows[0].index(col); out={r[0].rstrip('*'):int(r[i].replace(',','')) for r in rows[1:] if len(r)>i and r[0].rstrip('*') in conf}
    miss=[s for s in conf if s not in out]; assert not miss,(y,miss); return out
A25=table(2025,'2025 Final Average'); A26=table(2026,'2026 Current Average')
prs=Presentation(SRC); old=list(prs.slides); LAY=old[14].slide_layout
def frame(title,sub):
    s=prs.slides.add_slide(LAY)
    for ph in s.placeholders:
        if ph.placeholder_format.idx==0: ph.text=title
        elif ph.placeholder_format.idx==1: ph.text=sub
    pan=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(0.35),Inches(1.35),Inches(9.31),Inches(5.53)); pan.adjustments[0]=0.025
    pan.fill.solid(); pan.fill.fore_color.rgb=RGBColor(255,255,255); pan.line.fill.background(); pan.shadow.inherit=False; pan.name='Panel'
    s.shapes._spTree.remove(pan._element); s.shapes._spTree.insert(2,pan._element); return s
def text(s,lines,x,y,w,h,size=7,color=INK,name=None):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame; tf.word_wrap=True
    for m in ('margin_left','margin_right','margin_top','margin_bottom'): setattr(tf,m,0)
    for i,ln in enumerate(lines if isinstance(lines,list) else [lines]):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        for tx,b,c in (ln if isinstance(ln,list) else [(ln,False,color)]):
            r=p.add_run(); r.text=tx; r.font.name=F; r.font.size=Pt(size); r.font.bold=b; r.font.color.rgb=c
    if name: tb.name=name
    return tb
def avg(d,c=None): return statistics.mean(v for s,v in d.items() if c is None or conf[s]==c)
def slide(d,year,title,sub,foot):
    s=frame(title,sub); order=sorted(d,key=lambda x:-d[x])
    cd=CategoryChartData(); cd.categories=order
    for c in CONF: cd.add_series(LABEL.get(c,c),[d[x] if conf[x]==c else None for x in order])
    gf=s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.45),Inches(1.45),Inches(9.1),Inches(5.35),cd); gf.name=f'{year} attendance chart'
    ch=gf.chart; ch.has_title=False; ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout=False
    ch.legend.font.size=Pt(7); ch.legend.font.name=F
    pl=ch.plots[0]; pl.gap_width=35; pl.overlap=100
    for c,ser in zip(CONF,pl.series):
        ser.format.fill.solid(); ser.format.fill.fore_color.rgb=COL[c]; ser.invert_if_negative=False
        ser.has_data_labels=False
    pl.has_data_labels=True; dl=pl.data_labels; dl.number_format='#,##0,"K"'; dl.number_format_is_linked=False; dl.font.size=Pt(4.5); dl.font.name=F; dl.position=XL_LABEL_POSITION.OUTSIDE_END
    ca=ch.category_axis; ca.tick_labels.font.size=Pt(5); ca.tick_labels.font.name=F; ca.format.line.color.rgb=RGBColor(0xBF,0xBF,0xBF)
    txPr=ca._element.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}txPr'); txPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}bodyPr').set('rot','-5400000')
    va=ch.value_axis; va.minimum_scale=0; va.maximum_scale=120000; va.major_unit=20000; va.tick_labels.number_format='#,##0'; va.tick_labels.number_format_is_linked=False
    va.tick_labels.font.size=Pt(6); va.tick_labels.font.name=F; va.has_major_gridlines=True; va.major_gridlines.format.line.color.rgb=RGBColor(0xE7,0xE7,0xE7); va.format.line.fill.background()
    # conference averages box
    lines=[[('Average per home game',True,INK)],[(f'Power 4 (68): {avg(d):,.0f}',True,INK)]]+[[('■ ',False,COL[c]),(f'{LABEL.get(c,c)}: {avg(d,c):,.0f}',False,INK)] for c in CONF]
    bx=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(7.45),Inches(1.85),Inches(1.95),Inches(1.2)); bx.fill.solid(); bx.fill.fore_color.rgb=RGBColor(255,255,255); bx.line.color.rgb=RGBColor(0xBF,0xBF,0xBF); bx.line.width=Pt(0.5); bx.shadow.inherit=False; bx.name='Averages box'
    text(s,lines,7.55,1.92,1.8,1.1,7,name='Averages')
    text(s,foot,0.35,7.12,6.75,0.3,6,GREY,name='Footnote')
CHG={s:A26[s]-A25[s] for s in A25}
def change_slide():
    d=CHG; order=sorted(d,key=lambda x:(-d[x],x))
    up=sum(v>0 for v in d.values()); dn=sum(v<0 for v in d.values()); fl=len(d)-up-dn
    s=frame('POWER 4 FOOTBALL ATTENDANCE: CHANGE, 2026 VS 2025',
      f"Average home attendance is down {abs(avg(d)):,.0f} per game across the Power 4 so far in 2026. {up} schools are up, {dn} are down and {fl} are flat. The SEC is the only conference up ({avg(d,'SEC'):+,.0f}); Kansas State is up {d['Kansas State']:,}.")
    cd=CategoryChartData(); cd.categories=order
    for c in CONF: cd.add_series(LABEL.get(c,c),[d[x] if conf[x]==c else None for x in order])
    gf=s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.45),Inches(1.45),Inches(9.1),Inches(5.35),cd); gf.name='Attendance change chart'
    ch=gf.chart; ch.has_title=False; ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout=False; ch.legend.font.size=Pt(7); ch.legend.font.name=F
    pl=ch.plots[0]; pl.gap_width=35; pl.overlap=100
    for c,ser in zip(CONF,pl.series): ser.format.fill.solid(); ser.format.fill.fore_color.rgb=COL[c]; ser.invert_if_negative=False
    pl.has_data_labels=True; dl=pl.data_labels; dl.number_format='+#,##0;-#,##0;0'; dl.number_format_is_linked=False; dl.font.size=Pt(5); dl.font.name=F; dl.position=XL_LABEL_POSITION.OUTSIDE_END
    from lxml import etree
    A='http://schemas.openxmlformats.org/drawingml/2006/main'
    dtx=dl._element.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}txPr'); dtx.find(f'{{{A}}}bodyPr').set('rot','-5400000'); dtx.find(f'{{{A}}}bodyPr').set('vert','horz')
    ca=ch.category_axis; ca.tick_label_position=XL_TICK_LABEL_POSITION.LOW; ca.tick_labels.font.size=Pt(5); ca.tick_labels.font.name=F; ca.format.line.color.rgb=RGBColor(0x7F,0x7F,0x7F)
    txPr=ca._element.find('{http://schemas.openxmlformats.org/drawingml/2006/chart}txPr'); txPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}bodyPr').set('rot','-5400000')
    va=ch.value_axis; va.minimum_scale=-14000; va.maximum_scale=14000; va.major_unit=4000; va.tick_labels.number_format='+#,##0;-#,##0;0'; va.tick_labels.number_format_is_linked=False
    va.tick_labels.font.size=Pt(6); va.tick_labels.font.name=F; va.has_major_gridlines=True; va.major_gridlines.format.line.color.rgb=RGBColor(0xE7,0xE7,0xE7); va.format.line.fill.background()
    lines=[[('Average change per home game',True,INK)],[(f'Power 4 (68): {avg(d):+,.0f}',True,INK)]]+[[('\u25a0 ',False,COL[c]),(f'{LABEL.get(c,c)}: '+(f'{avg(d,c):+,.0f}' if round(avg(d,c)) else '0'),False,INK)] for c in CONF]
    bx=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(7.3),Inches(1.85),Inches(2.1),Inches(1.2)); bx.fill.solid(); bx.fill.fore_color.rgb=RGBColor(255,255,255); bx.line.color.rgb=RGBColor(0xBF,0xBF,0xBF); bx.line.width=Pt(0.5); bx.shadow.inherit=False; bx.name='Averages box'
    text(s,lines,7.4,1.92,1.95,1.1,7,name='Averages')
    text(s,"Source: D1.ticker, 2026 FBS Attendance Trends: '2026 Current Average' (through Week 11; season in progress) less '2025 Average' (full 2025 season). Average per home game as reported by D1.ticker. Northwestern's 2025 figure (11,548) leaves out its two Wrigley Field games (NCAA average with them: 15,898), so its gain is overstated.",0.35,7.12,6.75,0.3,6,GREY,name='Footnote')
change_slide()
ids=prs.slides._sldIdLst; RID='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
for sl in old:
    for sid in list(ids):
        if prs.part.related_part(sid.get(RID)) is sl.part: prs.part.drop_rel(sid.get(RID)); ids.remove(sid); break
prs.save(OUT); print('saved',OUT,len(prs.slides),'slides')
# think-cell backup: one tab, categories down column B, one column per conference series (blank where not that conference)
wb=Workbook(); ws=wb.active; ws.title='Attendance change'; ws.sheet_view.showGridLines=False
H=Font(name='Aptos Narrow',size=9,bold=True,color='FFFFFF'); N=Font(name='Aptos Narrow',size=9); BL=Font(name='Aptos Narrow',size=9,color='0000FF',underline='single'); U26=URL.format(2026)
ws['B2']='SMASHSPORTS'; ws['B2'].font=Font(name='Montserrat',size=11,bold=True)
ws['B3']="Change in average home football attendance, 2026 (through Week 11) vs 2025 (full season), Power 4 (68 schools), ranked. Source: D1.ticker 2026 FBS Attendance Trends, '2026 Current Average' and '2025 Average'."; ws['B3'].font=N
ws['B4']=U26; ws['B4'].hyperlink=U26; ws['B4'].font=BL
hdr=['School','Conference','2025 average','2026 average (through Week 11)','Change','Change %','Rank']+[LABEL.get(c,c) for c in CONF]
for j,h in enumerate(hdr): c=ws.cell(6,2+j,h); c.font=H; c.fill=PatternFill('solid',fgColor='000000')
for i,x in enumerate(sorted(CHG,key=lambda x:(-CHG[x],x))):
    r=7+i; ws.cell(r,2,x).font=N; ws.cell(r,3,conf[x]).font=N
    for col,v in ((4,A25[x]),(5,A26[x])): c=ws.cell(r,col,v); c.font=BL; c.hyperlink=U26; c.number_format='#,##0'
    c=ws.cell(r,6,f'=E{r}-D{r}'); c.font=N; c.number_format='+#,##0;-#,##0;0'
    c=ws.cell(r,7,f'=F{r}/D{r}'); c.font=N; c.number_format='+0.0%;-0.0%;0.0%'
    ws.cell(r,8,i+1).font=N
    for j,cf in enumerate(CONF): cc=ws.cell(r,9+j,f'=IF($C{r}="{cf}",$F{r},"")'); cc.font=N; cc.number_format='+#,##0;-#,##0;0'
e=6+len(CHG); r=e+2; ws.cell(r,2,'Power 4 average').font=Font(name='Aptos Narrow',size=9,bold=True)
for col in 'DEF': ws[f'{col}{r}']=f'=AVERAGE({col}7:{col}{e})'; ws[f'{col}{r}'].number_format='#,##0' if col!='F' else '+#,##0;-#,##0;0'
for k2,cf in enumerate(CONF):
    rr=r+1+k2; ws.cell(rr,2,f'{LABEL.get(cf,cf)} average').font=N
    for col in 'DEF': c=ws[f'{col}{rr}']; c.value=f'=AVERAGEIF($C$7:$C${e},"{cf}",{col}7:{col}{e})'; c.font=N; c.number_format='#,##0' if col!='F' else '+#,##0;-#,##0;0'
for colw,w in zip('ABCDEFGHIJKLM',(2,22,12,12,14,10,10,6,10,10,10,10,16)): ws.column_dimensions[colw].width=w
wb.save(XL); print('saved',XL)
