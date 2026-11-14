"""Write the chart data behind the slides to an Excel file, one tab per slide, in the benchmarking workbook's style.
Usage: python3 -I scripts/slides_workbook.py slides/spec_big12.json slides/P4_Benchmarking_Chart_Data_Big12.xlsx
Layout (analyst's direction): school names run across row 6 from column D, with the values underneath, one row per
series, followed by the Power 4 average and median repeated under every school (the two line series). Blue cells are
hardcoded figures, black cells are formulas."""
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
RIGHT=Alignment(horizontal='right')
wb=Workbook(); wb.remove(wb.active)
for s in spec['slides']:
    ws=wb.create_sheet(TAB.get(s['key'],s['key'][:31])); ws.sheet_view.showGridLines=False
    ws.column_dimensions['A'].width=1; ws.column_dimensions['B'].width=2
    ws['B2']=CellRichText(TextBlock(InlineFont(rFont='Montserrat',sz=11,b=True,color='000000'),'SMASH'),TextBlock(InlineFont(rFont='Montserrat',sz=11,b=False,color='000000'),'SPORTS')); ws['B2'].font=Font(name='Montserrat',size=11)
    ws['B3']=s['label']; ws['B3'].font=F(bold=True)
    scope=(f"{CONF} schools" if s['scope']=='conference' else 'All Power 4 schools with a reported value')
    unit={'usd':'whole dollars','num':'fans per home game','pct':'share of capacity'}[s['unit']]
    ws['B4']=f"{scope}; {unit}"; ws['B4'].font=F()
    ser=s['series']; cats=s['categories']; n=len(cats); nf=NUMF[s['unit']]
    C0=4; CL=C0+n-1; first,last=L(C0),L(CL)          # schools run from column D
    # row 6: school names
    for cc,h in [(3,'School')]+[(C0+i,c['school']) for i,c in enumerate(cats)]:
        c=ws.cell(6,cc,h); c.font=F(color='FFFFFF'); c.fill=BLACK; c.border=Border(top=THIN,bottom=THIN); c.alignment=Alignment(horizontal='center')
    ws.row_dimensions[6].height=24
    # one row per bar series
    r=7
    for x in ser:
        ws.cell(r,3,x['name'] if len(ser)>1 or s['unit']!='usd' else s['label']).font=F()
        for i,v in enumerate(x['values']):
            c=ws.cell(r,C0+i,v if v is not None else '--'); c.font=F(color=BLUE); c.number_format=nf; c.alignment=RIGHT
        r+=1
    r1=7                                              # the first series feeds the Power 4 lines
    def summary(row,label,values):
        for cc in range(3,CL+1):
            c=ws.cell(row,cc); c.fill=GRAY; c.font=F(bold=True)
        ws.cell(row,3,label)
        for cc,(v,blue) in values.items():
            c=ws.cell(row,cc,v); c.number_format=nf; c.font=F(bold=True,color=BLUE if blue else '000000'); c.fill=GRAY; c.alignment=RIGHT
    # Power 4 average and median, repeated under every school so they chart as flat lines
    for label,fn,val in ((f"Power 4 average ({s['n_p4']} schools)",'AVERAGE',s['avg']),(f"Power 4 median ({s['n_p4']} schools)",'MEDIAN',s['med'])):
        if s['scope']=='conference':   # the Power 4 figure covers schools that are not on this tab: hardcoded once, then repeated
            cells={C0:(val,True)}; cells.update({cc:(f'=${first}${r}',False) for cc in range(C0+1,CL+1)})
        else:
            cells={cc:(f'={fn}(${first}${r1}:${last}${r1})',False) for cc in range(C0,CL+1)}
        summary(r,label,cells); r+=1
    if s['scope']=='conference':
        for k,x in enumerate(ser):
            suffix=f", {x['name']}" if len(ser)>1 else ''
            for label,fn in ((f'{CONF} average{suffix}','AVERAGE'),(f'{CONF} median{suffix}','MEDIAN')):
                summary(r,label,{C0:(f'={fn}({first}{7+k}:{last}{7+k})',False)}); r+=1
    r+=1
    ws.cell(r,3,'Conference').font=F()
    for i,c in enumerate(cats): 
        x=ws.cell(r,C0+i,c['conference']); x.font=F(); x.alignment=RIGHT
    ws.cell(r+2,3,'Slide title: '+s['title']).font=F(); ws.cell(r+3,3,'Slide subtitle: '+s['subtitle']).font=F(); ws.cell(r+4,3,s['source']).font=F()
    ws.column_dimensions['C'].width=44
    for cc in range(C0,CL+1): ws.column_dimensions[L(cc)].width=max(13,len(str(ws.cell(6,cc).value))+2)
    ws.freeze_panes='D7'
wb.save(out); print('saved',out,wb.sheetnames)
