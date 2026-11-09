"""QA checks on the built workbook (run after recalc)."""
import openpyxl, json, random, sys
from collections import Counter
lay=json.load(open('data/workbook_layout.json')); S=lay['S']
F='Power4_Athletic_Department_Benchmarking.xlsx'
wbf=openpyxl.load_workbook(F); wbv=openpyxl.load_workbook(F,data_only=True)
confs=['02 - ACC','03 - Big Ten','04 - Big 12','05 - SEC']
tot=sum(lay['conf_layout'][c.split(' - ')[1]]['last']-lay['conf_layout'][c.split(' - ')[1]]['first']+1 for c in confs)
print('1 rows: conference',tot,'| 01',lay['all_last']-lay['all_first']+1,'| school tabs',sum(1 for n in wbf.sheetnames if int(n[:2])>=8))
hits=[(ws.title,c.coordinate) for ws in wbf for row in ws.iter_rows() for c in row if c.value is not None and ('usatoday' in (str(c.value)+(c.hyperlink.target if c.hyperlink else '')).lower() or 'usa today' in str(c.value).lower())]
print('3 USA Today hits',hits)
bad=[]; blanks=[]; fontbad=[]; trip=[]
for c in confs:
    ws=wbf[c]; wsv=wbv[c]; lc=lay['conf_layout'][c.split(' - ')[1]]
    for r in range(lc['first'],lc['med']+1):
        for i,m in enumerate(S,1):
            cell=ws.cell(row=r,column=i); cv=wsv.cell(row=r,column=i).value
            if cv is None or cv=='': blanks.append((c,cell.coordinate))
            isf=isinstance(cell.value,str) and cell.value.startswith('=')
            if m['kind']=='num' and r<=lc['last'] and cell.value!='--' and not isf and cell.data_type!='n': bad.append((c,cell.coordinate,cell.value))
            if (m['kind']=='formula' or isf) and not (isinstance(cv,(int,float)) or cv=='--'): bad.append((c,cell.coordinate,'formula result',cv))
        if r<=lc['last']:
            for pre in ('stadium_nr','arena_nr','patch','mmr','apparel'):
                cols=[i for i,m in enumerate(S,1) if m['key'] in (pre+'_annual_value',pre+'_term_years',pre+'_total_value')]
                kinds=['formula' if isinstance(ws.cell(row=r,column=i).value,str) and str(ws.cell(row=r,column=i).value).startswith('=') else ('dash' if ws.cell(row=r,column=i).value=='--' else 'hard') for i in cols]
                if kinds.count('formula')>1 or kinds.count('hard')==3 or (kinds.count('hard')==2 and kinds.count('formula')!=1): trip.append((c,r,pre,kinds))
print('4 text-stored numerics / bad formula results',len(bad),bad[:5]); print('  empty results on conference tabs',len(blanks))
print('5 triplet violations',trip)
for ws in wbf:
    if ws.merged_cells.ranges: print('MERGED',ws.title)
    if ws.freeze_panes: print('FROZEN',ws.title)
    for row in ws.iter_rows():
        for cell in row:
            if cell.value is None: continue
            f=cell.font
            if f.name!='Arial' or (f.size and float(f.size)!=10) or f.italic or (cell.alignment and cell.alignment.wrap_text): fontbad.append((ws.title,cell.coordinate))
print('  font/wrap issues',len(fontbad))
empt=0
for ws in wbv:
    if ws.title in confs or ws.title in ('00 - Read Me','06 - Source Log'): continue
    for row in ws.iter_rows(min_row=3):
        for cell in row:
            if (cell.value=='' or cell.value is None) and wbf[ws.title][cell.coordinate].value is not None: empt+=1
print('  empty formula results on link tabs',empt)
cov=[]
for i,m in enumerate(S,1):
    n=sum(1 for c in confs for r in range(lay['conf_layout'][c.split(' - ')[1]]['first'],lay['conf_layout'][c.split(' - ')[1]]['last']+1) if wbv[c].cell(row=r,column=i).value!='--')
    cov.append((m['hdr'],n))
json.dump(cov,open('data/coverage.json','w'))
print('6 coverage:'); [print(f'  {n:3d}/67  {h}') for h,n in cov]
ib=[i for i,m in enumerate(S,1) if m['key']=='fin_basis'][0]; ify=[i for i,m in enumerate(S,1) if m['key']=='fin_fiscal_year'][0]
eada=[]; fy=[]
for c in confs:
    ws=wbf[c]; lc=lay['conf_layout'][c.split(' - ')[1]]
    for r in range(lc['first'],lc['last']+1):
        if ws.cell(row=r,column=ib).value=='EADA': eada.append(ws.cell(row=r,column=1).value)
        if ws.cell(row=r,column=ify).value!=2025: fy.append((ws.cell(row=r,column=1).value,ws.cell(row=r,column=ify).value))
print('EADA basis',len(eada),eada); print('FY not 2025',fy)
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1); cands=[]
for c in confs:
    ws=wbf[c]; lc=lay['conf_layout'][c.split(' - ')[1]]
    for r in range(lc['first'],lc['last']+1):
        for i,m in enumerate(S,1):
            cell=ws.cell(row=r,column=i)
            if cell.hyperlink and m['kind']=='num' and m['key']!='fin_fiscal_year': cands.append((c,ws.cell(row=r,column=1).value,m['hdr'],cell.coordinate,cell.value,cell.hyperlink.target))
for s in random.sample(cands,10): print('SPOT',s)
