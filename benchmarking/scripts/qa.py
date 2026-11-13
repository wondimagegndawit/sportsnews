"""QA checks on the built workbook (run after recalc)."""
import openpyxl, json, random, sys, statistics
from openpyxl.worksheet.formula import ArrayFormula
from collections import Counter
lay=json.load(open('data/workbook_layout.json')); S=lay['S']; OFF=lay.get('col_offset',0); HR=lay.get('header_row',2)
F='Power4_Athletic_Department_Benchmarking.xlsx'
wbf=openpyxl.load_workbook(F); wbv=openpyxl.load_workbook(F,data_only=True)
confs=[v['sheet'] for v in lay['conf_layout'].values()]
DTC=[i for i,m in enumerate(S,1) if m['key']=='f_fin_data_type'][0]
tot=sum(lay['conf_layout'][c]['last']-lay['conf_layout'][c]['first']+1 for c in confs)
print('1 rows: expected',lay.get('n_schools'),'| conference',tot,'| All Schools',lay['all_last']-lay['all_first']+1,'| tabs',wbf.sheetnames)
hits=[(ws.title,c.coordinate) for ws in wbf for row in ws.iter_rows() for c in row if c.value is not None and ('usatoday' in (str(c.value)+(c.hyperlink.target if c.hyperlink else '')).lower() or 'usa today' in str(c.value).lower())]
import csv as _csv, os as _os
_exc=list(_csv.DictReader(open('data/source_exceptions.csv',encoding='utf-8'))) if _os.path.exists('data/source_exceptions.csv') else []
def _allowed(title,coord):
    ws=wbf[title]; c=ws[coord]
    if c.hyperlink and any(c.hyperlink.target==e['url'] for e in _exc): return True
    if title=='Source Log':
        hd={ws.cell(6,k).value:k for k in range(3,ws.max_column+1)}
        return any(ws.cell(c.row,hd['School']).value==e['school'] and ws.cell(c.row,hd['Metric']).value==e['header'] for e in _exc)
    return False
_ok=[h for h in hits if _allowed(*h)]; hits=[h for h in hits if h not in _ok]
print('3 USA Today hits',hits,'| allowed by the analyst\'s direction (data/source_exceptions.csv)',_ok)
bad=[]; blanks=[]; fontbad=[]; trip=[]
for c in confs:
    ws=wbf[c]; wsv=wbv[c]; lc=lay['conf_layout'][c]
    for r in range(lc['first'],lc['sum_last']+1):
        for i,m in enumerate(S,1):
            cell=ws.cell(row=r,column=i+OFF); cv=wsv.cell(row=r,column=i+OFF).value
            if cv is None or cv=='': blanks.append((c,cell.coordinate))
            isf=(isinstance(cell.value,str) and cell.value.startswith('=')) or isinstance(cell.value,ArrayFormula)
            if m['kind']=='num' and r<=lc['last'] and cell.value!='--' and not isf and cell.data_type!='n': bad.append((c,cell.coordinate,cell.value))
            if i==DTC:
                if cv not in ('MFRS','EADA','All'): bad.append((c,cell.coordinate,'data type',cv))
            elif (m['kind']=='formula' or isf) and not (isinstance(cv,(int,float)) or cv=='--'): bad.append((c,cell.coordinate,'formula result',cv))
        if r<=lc['last']:
            for pre in ('stadium_nr','arena_nr','patch','mmr','apparel'):
                cols=[i for i,m in enumerate(S,1) if m['key'] in (pre+'_annual_value',pre+'_term_years',pre+'_total_value')]
                kinds=['formula' if isinstance(ws.cell(row=r,column=i+OFF).value,str) and str(ws.cell(row=r,column=i+OFF).value).startswith('=') else ('dash' if ws.cell(row=r,column=i+OFF).value=='--' else 'hard') for i in cols]
                nd=[ws.cell(row=r,column=1+OFF).value,pre] in lay.get('no_derive',[])   # reported figures cover different periods: shown as reported, nothing derived
                if kinds.count('formula')>1 or kinds.count('hard')==3 or (kinds.count('hard')==2 and kinds.count('formula')!=1 and not nd): trip.append((c,r,pre,kinds))
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
_cells=[cell for ws in wbf for row in ws.iter_rows() for cell in row if cell.value is not None]
print('  hyperlinked cells',sum(1 for c in _cells if c.hyperlink),'| underlined cells',sum(1 for c in _cells if c.font.u),'| underline without hyperlink',sum(1 for c in _cells if c.font.u and not c.hyperlink),'| hyperlink without underline',sum(1 for c in _cells if c.hyperlink and not c.font.u))
empt=0
for ws in wbv:
    if ws.title in confs or ws.title in ('Read Me','Source Log'): continue
    for row in ws.iter_rows(min_row=HR+1):
        for cell in row:
            if (cell.value=='' or cell.value is None) and wbf[ws.title][cell.coordinate].value is not None: empt+=1
print('  empty formula results on link tabs',empt)
print('  cells whose number format has a fill character (long underline)',sum(1 for ws in wbf for row in ws.iter_rows() for cell in row if cell.value is not None and '*' in (cell.number_format or '')))
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
SC={x[0]:x for x in lay['scopes']}
def check(sheet,rr,st,key,rows):
    global nsum
    _,ty,fy,_lab=SC[key]
    for i,m in enumerate(S,1):
        if i in (1,FYC,DTC): continue
        got=wbv[sheet].cell(row=rr,column=i+OFF).value
        scope=[row[i-1] for row in rows if (ty=='All' or row[DTC-1]==ty) and (fy=='All' or row[FYC-1]==fy)]
        if st=='Count': exp=sum(1 for v in scope if v!='--') if (key=='All' or m['sec']=='Financial') else '--'
        elif not m['agg'] or (key!='All' and not m['byfy']): exp='--'
        else: exp=expect(scope,st)
        nsum+=1
        if not same(got,exp): sbad.append((sheet,rr,m['hdr'],got,exp))
    if (wbv[sheet].cell(row=rr,column=DTC+OFF).value,wbv[sheet].cell(row=rr,column=FYC+OFF).value)!=(ty,fy): sbad.append((sheet,rr,'criteria cells'))
for c in confs:
    for st,d in lay['conf_layout'][c]['summary'].items():
        for key,rr in d.items(): check(c,rr,st,key,school[c])
allrows=[x for c in confs for x in school[c]]
for st,d in lay['all_layout']['summary'].items():
    for key,rr in d.items(): check('All Schools',rr,st,key,allrows)
print('  conference names left in the All Schools summary rows',sum(1 for r in range(lay['all_layout']['sum_first'],lay['all_layout']['breakdown']['last']+1) for c in range(1,8) if wbv['All Schools'].cell(row=r,column=c+OFF).value in confs))
print('  summary cells recomputed',nsum,'| mismatches',len(sbad),sbad[:5])
# 8: data-breakdown tables (schools by data type and fiscal year, and by financial source basis)
BASC=[i for i,m in enumerate(S,1) if m['key']=='fin_basis'][0]; bbad=[]; nb=0
def bcheck(sheet,bd,groups):
    global nb
    def cellv(rr,j): return wbv[sheet].cell(row=rr,column=2+OFF+j).value
    for j,rows in enumerate(groups):
        for ty,d in bd['types'].items():
            tot=0
            for fy,rr in d['fy'].items():
                exp=sum(1 for row in rows if row[DTC-1]==ty and str(row[FYC-1])==fy); tot+=exp; nb+=1
                if cellv(rr,j)!=exp: bbad.append((sheet,rr,ty,fy,j,cellv(rr,j),exp))
            nb+=1
            if cellv(d['total'],j)!=tot or tot!=sum(1 for row in rows if row[DTC-1]==ty): bbad.append((sheet,d['total'],ty,'total',j,cellv(d['total'],j),tot))
        tot=0
        for lab,rr in bd['basis'].items():
            exp=sum(1 for row in rows if row[BASC-1]==lab); tot+=exp; nb+=1
            if cellv(rr,j)!=exp: bbad.append((sheet,rr,lab,j,cellv(rr,j),exp))
        nb+=1
        if cellv(bd['basis_total'],j)!=tot or tot!=len(rows): bbad.append((sheet,bd['basis_total'],'basis total',j,cellv(bd['basis_total'],j),tot,len(rows)))
for c in confs: bcheck(c,lay['conf_layout'][c]['breakdown'],[school[c]])
bd=lay['all_layout']['breakdown']; bcheck('All Schools',bd,[allrows])
print('8 breakdown cells recomputed',nb,'| mismatches',len(bbad),bbad[:5])
# 9: relevance and audit trail
H0={m['hdr']:i for i,m in enumerate(S,1)}; lapsed=[]
for c in confs:
    lc=lay['conf_layout'][c]
    for r in range(lc['first'],lc['last']+1):
        for pre in ('Stadium naming rights','Arena naming rights','Jersey patch','MMR','Apparel'):
            e=wbv[c].cell(row=r,column=H0[pre+' expires']+OFF).value
            if isinstance(e,(int,float)) and e<2026: lapsed.append((wbv[c].cell(row=r,column=1+OFF).value,pre,e))
print('9 deals whose recorded term ended before 2026',lapsed)
slq=wbv['Source Log']; SH={slq.cell(row=HR,column=c).value:c for c in range(1,slq.max_column+1)}
print('  verification status',dict(Counter(slq.cell(row=r,column=SH['Verification']).value for r in range(HR+1,slq.max_row+1))))
print('  All Schools breakdown:',bd['cols'])
for ty,d in bd['types'].items():
    for fy,rr in list(d['fy'].items())+[('total',d['total'])]: print(f'   {ty+" FY"+fy if fy!="total" else "Total "+ty:30s}',[wbv['All Schools'].cell(row=rr,column=2+OFF+j).value for j in range(len(bd['cols']))])
for lab,rr in list(bd['basis'].items())+[('Total',bd['basis_total'])]: print(f'   {lab:30s}',[wbv['All Schools'].cell(row=rr,column=2+OFF+j).value for j in range(len(bd['cols']))])
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
