"""Analyst review of the NCAA-report financials: arithmetic, ratios, year-over-year swings against the prior year in the
Sportico files, and a comparison with the federal EADA filing. Prints anything that needs a second look."""
import csv,json,glob,re,statistics,collections,openpyxl
wb=openpyxl.load_workbook('Power4_Athletic_Department_Benchmarking.xlsx',data_only=True); ws=wb['All Schools']
H={ws.cell(6,c).value:c for c in range(3,ws.max_column+1)}
def v(r,h):
    x=ws.cell(r,H[h]).value; return x if isinstance(x,(int,float)) and not isinstance(x,bool) else None
MASTER={s['name'] for s in json.load(open('data/schools_master.json'))}
rows=[r for r in range(7,ws.max_row+1) if ws.cell(r,H['Financial data type']).value=='MFRS' and ws.cell(r,3).value in MASTER]
name=lambda r: ws.cell(r,3).value; conf=lambda r: ws.cell(r,H['Conference']).value
print('NCAA-report schools on the main tab:',len(rows),collections.Counter(ws.cell(r,H['Fiscal year']).value for r in rows))
# 1. arithmetic on the main tab
bad=0
for r in rows:
    tr,te,sp=v(r,'Total operating revenue'),v(r,'Total operating expenses'),v(r,'Operating surplus (deficit)')
    if None not in (tr,te,sp) and abs(tr-te-sp)>1: bad+=1; print('SURPLUS ARITHMETIC',name(r),tr,te,sp)
    parts=[v(r,h) for h in ('Football revenue',"Men's basketball revenue",'Other sports revenue','Non-program-specific revenue')]
    if None not in parts and tr is not None and abs(sum(parts)-tr)>2: bad+=1; print('SPORT REVENUE DOES NOT ADD',name(r),sum(parts),tr)
    tt=[v(r,h) for h in ('Team travel: football',"Team travel: men's basketball","Team travel: women's basketball",'Team travel: other sports')]
    if None not in tt and v(r,'Team travel') is not None and sum(tt)>v(r,'Team travel')+2: bad+=1; print('TRAVEL BY SPORT EXCEEDS TOTAL',name(r),sum(tt),v(r,'Team travel'))
print('1. arithmetic exceptions on the main tab:',bad)
# 2. ratio outliers (share of total revenue or expenses), flagged at more than 2.5 median absolute deviations... shown for the Big 12 and for extreme Power 4 values
def ratios(label,num,den):
    xs=[(name(r),conf(r),v(r,num)/v(r,den)) for r in rows if v(r,num) is not None and v(r,den)]
    med=statistics.median(x[2] for x in xs); mad=statistics.median(abs(x[2]-med) for x in xs) or 1e-9
    out=[x for x in xs if abs(x[2]-med)/mad>4 or x[2]==0]
    print(f'   {label}: n={len(xs)} median {med:.1%} range {min(x[2] for x in xs):.1%} to {max(x[2] for x in xs):.1%}'+(' | outliers: '+', '.join(f"{a} {c:.1%}" for a,b,c in sorted(out,key=lambda x:x[2])) if out else ''))
print('2. shares of total (flag: zero, or more than 4 median absolute deviations from the median)')
for lab,n,d in (('ticket sales / revenue','Ticket sales revenue','Total operating revenue'),('media rights / revenue','Media rights revenue','Total operating revenue'),('licensing and sponsorship / revenue','Licensing, advertising and sponsorship revenue','Total operating revenue'),
                ('contributions / revenue','Contributions revenue','Total operating revenue'),('NCAA and conference distributions / revenue','NCAA and conference distributions','Total operating revenue'),
                ('football / revenue','Football revenue','Total operating revenue'),("men's basketball / revenue","Men's basketball revenue",'Total operating revenue'),
                ('coaching pay / expenses','Total coaching salaries and benefits','Total operating expenses'),('support staff pay / expenses','Support and administrative staff pay','Total operating expenses'),
                ('team travel / expenses','Team travel','Total operating expenses'),('fundraising and marketing / expenses','Fundraising, marketing and promotion','Total operating expenses'),
                ('student-athlete meals / expenses','Student-athlete meals','Total operating expenses'),('debt service / expenses','Annual debt service','Total operating expenses'),('surplus / revenue','Operating surplus (deficit)','Total operating revenue')):
    ratios(lab,n,d)
# 3. year over year against the prior year in the Sportico files
data={}
for f in sorted(glob.glob('data/sportico/json*.json')):
    txt=open(f,encoding='utf-8').read(); txt=txt[txt.index('['):].rstrip().rstrip(';')
    for obj in json.loads(txt):
        if isinstance(obj,dict):
            for k,val in obj.items(): data.setdefault(k,{}).update(val if isinstance(val,dict) else {})
def num(x):
    s=str(x).replace('$','').replace(',','').strip()
    if s in ('','-'): return 0
    neg=s.startswith('(') or s.startswith('-'); s=s.strip('()-')
    try: return -int(round(float(s))) if neg else int(round(float(s)))
    except ValueError: return None
SPV={(r['school'],r['metric']):r for r in csv.DictReader(open('data/sportico_values.csv',encoding='utf-8'))}
def line(T,pre):
    for k,val in T.items():
        if k.strip().lower().startswith(pre) and isinstance(val,list) and len(val)==6: return num(val[5])
print('3. change from the prior fiscal year in the Sportico files (flag: total revenue or expenses moving more than 20%, or a charted line more than doubling or halving)')
LINES=[('ticket sales','ticket sales'),('media rights','media rights'),('royalties','licensing and sponsorship'),('coaching salaries, benefits and bonuses paid by the university','coaching pay'),('team travel','team travel'),('fund raising','fundraising and marketing'),('student-athlete meals','meals'),('athletic facilities debt service','debt service')]
n=0
for r in rows:
    s=name(r); fy=ws.cell(r,H['Fiscal year']).value; e=SPV.get((s,'sp_fiscal_year'))
    if not e or ws.cell(r,H['Financial source basis']).value!='Sportico (MFRS compilation)': continue
    ent=re.search(r"entry '([^']+)'",e['notes']).group(1); cur=data[ent].get(str(fy),{}).get('Totals'); prv=data[ent].get(str(fy-1),{}).get('Totals')
    if not cur or not prv: print('   no prior year in the files:',s); continue
    n+=1; flags=[]
    for pre,lab in (('total operating revenues','total revenue'),('total operating expenses','total expenses')):
        a,b=line(prv,pre),line(cur,pre)
        if lab=='total revenue': b=v(r,'Total operating revenue')
        if lab=='total expenses': b=v(r,'Total operating expenses')
        if a and b and abs(b/a-1)>0.20: flags.append(f'{lab} {a/1e6:.1f}M to {b/1e6:.1f}M ({b/a-1:+.0%})')
    for pre,lab in LINES:
        a,b=line(prv,pre),line(cur,pre)
        if a and b and (b/a>2 or b/a<0.5) and max(a,b)>2e6: flags.append(f'{lab} {a/1e6:.1f}M to {b/1e6:.1f}M')
        if a and a>2e6 and b==0: flags.append(f'{lab} {a/1e6:.1f}M to 0')
    if flags: print(f'   {s} ({conf(r)}) FY{fy-1} to FY{fy}: '+'; '.join(flags))
print('   schools compared with their prior year:',n)
# 4. the federal EADA filing for the same year: a different basis, so only the order of magnitude is compared
E={(r['school'],r['metric']):r for r in csv.DictReader(open('data/merged_values.csv',encoding='utf-8')) if r['metric'].startswith('eada_')}
print('4. total revenue against the EADA filing (flag: more than 25% apart)')
k=0
for r in rows:
    s=name(r); e=E.get((s,'eada_total_revenue')); tr=v(r,'Total operating revenue')
    if e and e['value'] not in ('--','') and tr:
        k+=1; ratio=float(e['value'])/tr
        if abs(ratio-1)>0.25: print(f'   {s}: NCAA report {tr/1e6:.1f}M, EADA {float(e["value"])/1e6:.1f}M ({ratio-1:+.0%})')
print('   schools compared with EADA:',k)
