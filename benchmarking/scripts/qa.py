"""QA checks on the built workbook (run after recalc)."""
import openpyxl, json, random, sys, statistics
from openpyxl.worksheet.formula import ArrayFormula
from collections import Counter
lay=json.load(open('data/workbook_layout.json')); S=lay['S']; OFF=lay.get('col_offset',0); HR=lay.get('header_row',2)
F='Power4_Athletic_Department_Benchmarking.xlsx'
wbf=openpyxl.load_workbook(F); wbv=openpyxl.load_workbook(F,data_only=True)
confs=['ACC','Big Ten','Big 12','SEC']
tot=sum(lay['conf_layout'][c]['last']-lay['conf_layout'][c]['first']+1 for c in confs)
print('1 rows: expected',lay.get('n_schools'),'| conference',tot,'| All Schools',lay['all_last']-lay['all_first']+1,'| school tabs',len(wbf.sheetnames)-wbf.sheetnames.index('School Lookup')-1)
hits=[(ws.title,c.coordinate) for ws in wbf for row in ws.iter_rows() for c in row if c.value is not None and ('usatoday' in (str(c.value)+(c.hyperlink.target if c.hyperlink else '')).lower() or 'usa today' in str(c.value).lower())]
print('3 USA Today hits',hits)
bad=[]; blanks=[]; fontbad=[]; trip=[]
for c in confs:
    ws=wbf[c]; wsv=wbv[c]; lc=lay['conf_layout'][c]
    for r in range(lc['first'],lc['sum_last']+1):
        for i,m in enumerate(S,1):
            cell=ws.cell(row=r,column=i+OFF); cv=wsv.cell(row=r,column=i+OFF).value
            if cv is None or cv=='': blanks.append((c,cell.coordinate))
            isf=(isinstance(cell.value,str) and cell.value.startswith('=')) or isinstance(cell.value,ArrayFormula)
            if m['kind']=='num' and r<=lc['last'] and cell.value!='--' and not isf and cell.data_type!='n': bad.append((c,cell.coordinate,cell.value))
            if (m['kind']=='formula' or isf) and not (isinstance(cv,(int,float)) or cv=='--'): bad.append((c,cell.coordinate,'formula result',cv))
        if r<=lc['last']:
            for pre in ('stadium_nr','arena_nr','patch','mmr','apparel'):
                cols=[i for i,m in enumerate(S,1) if m['key'] in (pre+'_annual_value',pre+'_term_years',pre+'_total_value')]
                kinds=['formula' if isinstance(ws.cell(row=r,column=i+OFF).value,str) and str(ws.cell(row=r,column=i+OFF).value).startswith('=') else ('dash' if ws.cell(row=r,column=i+OFF).value=='--' else 'hard') for i in cols]
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
            if (f.name not in ('Aptos Narrow','Montserrat')) or (f.name=='Aptos Narrow' and f.size and float(f.size)!=9) or (cell.alignment and cell.alignment.wrap_text): fontbad.append((ws.title,cell.coordinate))
print('  font/wrap issues',len(fontbad))
print('  underlined cells',sum(1 for ws in wbf for row in ws.iter_rows() for cell in row if cell.value is not None and cell.font.u))
empt=0
for ws in wbv:
    if ws.title in confs or ws.title in ('Read Me','Source Log'): continue
    for row in ws.iter_rows(min_row=HR+1):
        for cell in row:
            if (cell.value=='' or cell.value is None) and wbf[ws.title][cell.coordinate].value is not None: empt+=1
print('  empty formula results on link tabs',empt)
# 7: recompute every average and median (by fiscal year and all years) in Python from the school rows and compare
errv=[(ws.title,c.coordinate,c.value) for ws in wbv for row in ws.iter_rows() for c in row if isinstance(c.value,str) and c.value.startswith(('#','Err:'))]
print('7 formula error values anywhere',len(errv),errv[:5])
print('  tab names with a number prefix',[n for n in wbf.sheetnames if n[:1].isdigit()])
FYC=[i for i,m in enumerate(S,1) if m['key']=='fin_fiscal_year'][0]; school={}; nsum=0; sbad=[]
def expect(vals,st): 
    vals=[v for v in vals if isinstance(v,(int,float)) and not isinstance(v,bool)]
    return '--' if not vals else (sum(vals)/len(vals) if st=='Average' else statistics.median(vals))
def same(a,b): return a==b if (a=='--' or b=='--') else (isinstance(a,(int,float)) and abs(a-b)<=1e-6*max(1,abs(b)))
for c in confs:
    conf=c; lc=lay['conf_layout'][conf]; wsv=wbv[c]
    school[conf]=[[wsv.cell(row=r,column=i+OFF).value for i in range(1,len(S)+1)] for r in range(lc['first'],lc['last']+1)]
def check(sheet,rr,st,fy,rows):
    global nsum
    for i,m in enumerate(S,1):
        if i==1 or i==FYC or (i==2 and sheet=='All Schools'): continue
        got=wbv[sheet].cell(row=rr,column=i+OFF).value
        scope=[row[i-1] for row in rows if fy=='All' or str(row[FYC-1])==fy]
        if st=='Count': exp=sum(1 for v in scope if v!='--') if (fy=='All' or m['sec']=='Financial') else '--'
        elif not m['agg'] or (fy!='All' and not m['byfy']): exp='--'
        else: exp=expect(scope,st)
        nsum+=1
        if not same(got,exp): sbad.append((sheet,rr,m['hdr'],got,exp))
for c in confs:
    conf=c
    for st,d in lay['conf_layout'][conf]['summary'].items():
        for fy,rr in d.items(): check(c,rr,st,fy,school[conf])
for b in lay['all_blocks']:
    for rr,st,conf in b['rows']: check('All Schools',rr,st,b['scope'],[x for k,v in school.items() for x in v] if conf=='All schools' else school[conf])
print('  summary cells recomputed',nsum,'| mismatches',len(sbad),sbad[:5])
# 8: data-breakdown tables (schools by fiscal year reported and by financial source basis)
BASC=[i for i,m in enumerate(S,1) if m['key']=='fin_basis'][0]; bbad=[]; nb=0
def bcheck(sheet,bd,groups):
    global nb
    for kind,col in (('fy',FYC),('basis',BASC)):
        tot=[0]*len(groups)
        for lab,rr in bd[kind].items():
            for j,rows in enumerate(groups):
                exp=sum(1 for row in rows if str(row[col-1])==lab); tot[j]+=exp; got=wbv[sheet].cell(row=rr,column=2+OFF+j).value; nb+=1
                if got!=exp: bbad.append((sheet,rr,lab,j,got,exp))
        for j,rows in enumerate(groups):
            got=wbv[sheet].cell(row=bd[kind+'_total'],column=2+OFF+j).value; nb+=1
            if got!=tot[j] or got!=len(rows): bbad.append((sheet,bd[kind+'_total'],'total',j,got,tot[j],len(rows)))
for c in confs: bcheck(c,lay['conf_layout'][c]['breakdown'],[school[c]])
bcheck('All Schools',lay['all_breakdown'],[school[c] for c in confs]+[[x for c in confs for x in school[c]]])
print('8 breakdown cells recomputed',nb,'| mismatches',len(bbad),bbad[:5])
bd=lay['all_breakdown']; print('  All Schools breakdown:',bd['cols'])
for kind in ('fy','basis'):
    for lab,rr in list(bd[kind].items())+[('Total',bd[kind+'_total'])]: print(f'   {lab:30s}',[wbv['All Schools'].cell(row=rr,column=2+OFF+j).value for j in range(len(bd['cols']))])
cov=[]
for i,m in enumerate(S,1):
    n=sum(1 for c in confs for r in range(lay['conf_layout'][c]['first'],lay['conf_layout'][c]['last']+1) if wbv[c].cell(row=r,column=i+OFF).value!='--')
    cov.append((m['hdr'],n))
json.dump(cov,open('data/coverage.json','w'))
print('6 coverage:'); [print(f"  {n:3d}/{lay.get('n_schools')}  {h}") for h,n in cov]
ib=[i for i,m in enumerate(S,1) if m['key']=='fin_basis'][0]; ify=[i for i,m in enumerate(S,1) if m['key']=='fin_fiscal_year'][0]
eada=[]; fy=[]
for c in confs:
    ws=wbf[c]; lc=lay['conf_layout'][c]
    for r in range(lc['first'],lc['last']+1):
        if ws.cell(row=r,column=ib+OFF).value=='EADA': eada.append(ws.cell(row=r,column=1+OFF).value)
        if ws.cell(row=r,column=ify+OFF).value!=2025: fy.append((ws.cell(row=r,column=1+OFF).value,ws.cell(row=r,column=ify+OFF).value))
print('EADA basis',len(eada),eada); print('FY not 2025',fy)
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1); cands=[]
for c in confs:
    ws=wbf[c]; lc=lay['conf_layout'][c]
    for r in range(lc['first'],lc['last']+1):
        for i,m in enumerate(S,1):
            cell=ws.cell(row=r,column=i+OFF)
            if cell.hyperlink and m['kind']=='num' and m['key']!='fin_fiscal_year': cands.append((c,ws.cell(row=r,column=1+OFF).value,m['hdr'],cell.coordinate,cell.value,cell.hyperlink.target))
for s in random.sample(cands,10): print('SPOT',s)
