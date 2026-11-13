"""Write the chart data behind the slides to an Excel file, one tab per slide, in the benchmarking workbook's style.
Usage: python3 -I scripts/slides_workbook.py slides/spec_big12.json slides/P4_Benchmarking_Chart_Data_Big12.xlsx
Each tab: one row per school with the bar values, then the Power 4 average and median repeated on every row (the two
line series), and summary rows underneath. Blue cells are hardcoded figures, black cells are formulas."""
import sys, json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
spec=json.load(open(sys.argv[1])); out=sys.argv[2]; CONF=spec['conference']
FN='Aptos Narrow'; BLUE='0000FF'
F=lambda **k: Font(name=FN,size=9,**k)
THIN=Side(style='thin',color='000000'); BLACK=PatternFill('solid',fgColor='000000'); GRAY=PatternFill('solid',fgColor='D9D9D9')
NUMF={'usd':'#,##0_);\\(#,##0\\);"-"??_);_(@_)','num':'#,##0_);\\(#,##0\\);"-"??_);_(@_)','pct':'0.0%'}
TAB={'jersey_patch':'Jersey patch','stadium_naming':'Stadium naming','arena_naming':'Arena naming','fb_attendance':'FB attendance','fb_capacity':'FB capacity','mbb_attendance':'MBB attendance','mbb_capacity':'MBB capacity'}
wb=Workbook(); wb.remove(wb.active)
for s in spec['slides']:
    ws=wb.create_sheet(TAB.get(s['key'],s['key'][:31])); ws.sheet_view.showGridLines=False
    ws.column_dimensions['A'].width=1; ws.column_dimensions['B'].width=2
    ws['B2']=CellRichText(TextBlock(InlineFont(rFont='Montserrat',sz=11,b=True,color='000000'),'SMASH'),TextBlock(InlineFont(rFont='Montserrat',sz=11,b=False,color='000000'),'SPORTS')); ws['B2'].font=Font(name='Montserrat',size=11)
    ws['B3']=s['label']; ws['B3'].font=F(bold=True)
    scope=(f"{CONF} schools" if s['scope']=='conference' else 'All Power 4 schools with a reported value')
    unit={'usd':'whole dollars','num':'fans per home game','pct':'share of capacity'}[s['unit']]
    ws['B4']=f"{scope}; {unit}"; ws['B4'].font=F()
    ser=s['series']; n=len(s['categories']); R0=7; RL=R0+n-1; nf=NUMF[s['unit']]
    hdr=['School','Conference']+[x['name'] if len(ser)>1 or s['unit']!='usd' else s['label'] for x in ser]+['Power 4 average','Power 4 median']
    for j,h in enumerate(hdr):
        c=ws.cell(row=6,column=3+j,value=h); c.font=F(color='FFFFFF'); c.fill=BLACK; c.border=Border(top=THIN,bottom=THIN); c.alignment=Alignment(horizontal='center')
    ws.row_dimensions[6].height=24
    c0=5; ca=c0+len(ser); cm=ca+1          # first series column, average column, median column
    # summary rows sit under the schools
    rows=[]; r=RL+1
    if s['scope']=='conference': rows+=[(f'{CONF} average','AVERAGE'),(f'{CONF} median','MEDIAN')]
    rP4a=RL+1+len(rows); rP4m=rP4a+1
    for i,cat in enumerate(s['categories']):
        rr=R0+i
        ws.cell(rr,3,cat['school']).font=F(); ws.cell(rr,4,cat['conference']).font=F()
        for k,x in enumerate(ser):
            v=x['values'][i]; c=ws.cell(rr,c0+k,v if v is not None else '--'); c.font=F(color=BLUE); c.number_format=nf; c.alignment=Alignment(horizontal='right')
        a=ws.cell(rr,ca,f'=${L(c0)}${rP4a}'); a.font=F(); a.number_format=nf
        m=ws.cell(rr,cm,f'=${L(c0)}${rP4m}'); m.font=F(); m.number_format=nf
    def summary(row,label,cells):
        for cc in range(3,cm+1):
            c=ws.cell(row,cc); c.fill=GRAY; c.font=F(bold=True)
        ws.cell(row,3,label)
        for cc,(v,blue) in cells.items():
            c=ws.cell(row,cc,v); c.number_format=nf; c.font=F(bold=True,color=BLUE if blue else '000000'); c.fill=GRAY; c.alignment=Alignment(horizontal='right')
    for label,fn in rows:
        summary(r,label,{c0+k:(f'={fn}({L(c0+k)}{R0}:{L(c0+k)}{RL})',False) for k in range(len(ser))}); r+=1
    if s['scope']=='conference':   # Power 4 figures cover schools that are not on this tab, so they are hardcoded
        summary(rP4a,f"Power 4 average ({s['n_p4']} schools; {ser[0]['name']})",{c0:(s['avg'],True)}); summary(rP4m,f"Power 4 median ({s['n_p4']} schools; {ser[0]['name']})",{c0:(s['med'],True)})
    else:
        summary(rP4a,f"Power 4 average ({s['n_p4']} schools)",{c0:(f'=AVERAGE({L(c0)}{R0}:{L(c0)}{RL})',False)}); summary(rP4m,f"Power 4 median ({s['n_p4']} schools)",{c0:(f'=MEDIAN({L(c0)}{R0}:{L(c0)}{RL})',False)})
    ws.cell(rP4m+2,3,'Slide title: '+s['title']).font=F(); ws.cell(rP4m+3,3,'Slide subtitle: '+s['subtitle']).font=F(); ws.cell(rP4m+4,3,s['source']).font=F()
    ws.column_dimensions['C'].width=44; ws.column_dimensions['D'].width=12
    for cc in range(c0,cm+1): ws.column_dimensions[L(cc)].width=max(18,len(str(ws.cell(6,cc).value))+2)
    ws.freeze_panes='D7'
wb.save(out); print('saved',out,wb.sheetnames)
