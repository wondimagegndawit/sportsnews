"""think-cell backup for the add-on slides: one tab per chart, laid out like a think-cell datasheet
(categories across the first row, one series per row, series name in the first column). Reads
slides/travel/chart_data.json written by build_travel_slides.py, so the numbers are the ones on the slides."""
import json,openpyxl,sys
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter as L
D=json.load(open('slides/travel/chart_data.json')); LOGO=json.load(open('slides/logos/logos.json'))
FN='Aptos Narrow'; F=Font(name=FN,size=9); FB=Font(name=FN,size=9,bold=True); FH=Font(name=FN,size=9,bold=True,color='FFFFFF'); BLK=PatternFill('solid',fgColor='000000')
FP=Font(name=FN,size=9,bold=True,color='512888')
wb=openpyxl.Workbook(); wb.remove(wb.active)
def tab(name,title,how):
    ws=wb.create_sheet(name); ws.sheet_view.showGridLines=False
    ws['B2']='SMASHSPORTS'; ws['B2'].font=Font(name='Montserrat',size=11,bold=True); ws['B3']=title; ws['B3'].font=FB; ws['B4']=how; ws['B4'].font=F
    ws.column_dimensions['A'].width=1; ws.column_dimensions['B'].width=2; ws.column_dimensions['C'].width=34
    return ws
def block(ws,r0,cats,series,fmt):
    """cats across row r0 from column D; each series a row: name in C, values from D"""
    for j,c in enumerate(cats):
        x=ws.cell(r0,4+j,c); x.font=FH; x.fill=BLK; x.alignment=Alignment(horizontal='center',wrap_text=True); ws.column_dimensions[L(4+j)].width=max(ws.column_dimensions[L(4+j)].width or 0,12)
    ws.cell(r0,3).fill=BLK
    for i,(nm,vals) in enumerate(series):
        ws.cell(r0+1+i,3,nm).font=FB
        for j,val in enumerate(vals):
            c=ws.cell(r0+1+i,4+j,val); c.font=FP if cats[j] in ('Kansas St','Kansas State') else F; c.number_format=fmt
    return r0+len(series)+1
sh=lambda s: LOGO[s]['short']
T=D['travel']; SCH=list(T)
# 1-3 maps: think-cell has no map chart, so these are plain tables (the map slides stay as built)
ws=tab('1 Travel map','Team travel, all sports, FY2025 (map slide)',"think-cell has no map chart: keep the map slide as built and edit its labels, or paste this table. Kansas State in purple.")
block(ws,6,[sh(s) for s in SCH],[('Team travel, all sports (MFRS line 28)',[T[s]['total'] for s in SCH]),('Latitude',[D['positions'][s]['lat'] for s in SCH]),('Longitude',[D['positions'][s]['lon'] for s in SCH])],'$#,##0')
for j in range(len(SCH)):
    for r in (8,9): ws.cell(r,4+j).number_format='0.0000'
ws=tab('2 Football map','Football travel, 2024 season (map slide)',"Estimated round-trip miles (ESPN schedules) and FY2025 football team travel spend.")
block(ws,6,[sh(s) for s in SCH],[('Estimated round-trip miles',[T[s]['fbm'] for s in SCH]),('Road trips',[T[s]['fbt'] for s in SCH]),('Football team travel spend',[T[s]['fb'] for s in SCH]),('Cost per mile',[T[s]['fbcpm'] for s in SCH])],'#,##0')
for j in range(len(SCH)): ws.cell(9,4+j).number_format='$#,##0'; ws.cell(10,4+j).number_format='$#,##0'
ws=tab('3 Basketball map',"Men's and women's basketball travel, 2024-25 (map slide)","Estimated round-trip miles (ESPN schedules) and FY2025 team travel spend by sport.")
block(ws,6,[sh(s) for s in SCH],[("Men's miles",[T[s]['mbbm'] for s in SCH]),("Men's spend",[T[s]['mbb'] for s in SCH]),("Men's cost per mile",[T[s]['mbbcpm'] for s in SCH]),
    ("Women's miles",[T[s]['wbbm'] for s in SCH]),("Women's spend",[T[s]['wbb'] for s in SCH]),("Women's cost per mile",[T[s]['wbbcpm'] for s in SCH])],'#,##0')
for j in range(len(SCH)):
    for r in (8,9,11,12): ws.cell(r,4+j).number_format='$#,##0'
# 4 cost per mile: three bar charts, each already sorted high to low
ws=tab('4 Cost per mile','Team travel cost per mile, three bar charts (one block per chart, sorted high to low)',"Paste each block into its own think-cell bar chart. Colour the Kansas St bar purple (512888).")
r=6
for title,rows in D['cost_per_mile'].items():
    ws.cell(r-1 if r>6 else 5,3,title).font=FB
    r=block(ws,r,[sh(q) for q,_ in rows],[(f'{title} cost per mile',[x for _,x in rows])],'$#,##0')+2
# 5 revenue mix: 100% stacked column
m=D['revenue_mix']
ws=tab('5 Revenue mix','Revenue mix, FY2025: 100% stacked column (schools sorted by contributions share)',"Paste the dollar block into a think-cell 100% chart (it computes the shares), or the share block into a stacked chart.")
r=block(ws,6,[sh(q) for q in m['schools']],list(zip(m['series'],m['dollars'])),'$#,##0')
ws.cell(r+1,3,'Same data as shares of total revenue').font=FB
block(ws,r+2,[sh(q) for q in m['schools']],list(zip(m['series'],m['shares'])),'0.0%')
# 6 Big 12 gap: clustered bar
g=D['big12_gap']
ws=tab('6 Big 12 gap','Where the Big 12 trails: average revenue by line, FY2025 (clustered bar)',"Three series: rest of Power 4 (grey), Big 12 (black), Kansas State (purple).")
block(ws,6,g['lines'],[(n,vals) for n,vals in g['series']],'$#,##0')
# 7 scatter
ws=tab('7 Revenue vs spending','Revenue against spending, FY2025 (scatter)',"think-cell scatter: label, X, Y. Add a break-even line (X = Y) from 85 to 175 ($M).")
for j,h in enumerate(['Label','Total operating revenue ($M)','Total operating expenses ($M)','Surplus (deficit), $M']):
    c=ws.cell(6,3+j,h); c.font=FH; c.fill=BLK; ws.column_dimensions[L(3+j)].width=max(ws.column_dimensions[L(3+j)].width or 0,24)
for i,(q,rv,ex,sp) in enumerate(D['scatter']):
    for j,val in enumerate([sh(q),rv/1e6,ex/1e6,sp/1e6]):
        c=ws.cell(7+i,3+j,val); c.font=FP if q=='Kansas State' else F; c.number_format='0.0' if j else 'General'
# 8 K-State index
ws=tab('8 K-State index','Kansas State as a share of the Big 12 average, FY2025 (bar)',"Purple where above 100%, grey below.")
block(ws,6,[n for n,_ in D['ksu_index']],[('Kansas State as % of Big 12 average',[x for _,x in D['ksu_index']])],'0%')
wb.save(sys.argv[1]); print('saved',sys.argv[1])
