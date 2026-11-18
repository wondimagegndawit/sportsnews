"""Independent check of the FY25 FRS Clean tab against the raw Sportico files (no use of the build scripts)."""
import json,glob,csv,re,collections,openpyxl
data={}
for f in sorted(glob.glob('data/sportico/json*.json')):
    txt=open(f,encoding='utf-8').read(); txt=txt[txt.index('['):].rstrip().rstrip(';')
    for obj in json.loads(txt):
        if isinstance(obj,dict):
            for k,v in obj.items(): data.setdefault(k,{}).update(v if isinstance(v,dict) else {})
def num(v):
    s=str(v).replace('$','').replace(',','').strip()
    if s in ('','-'): return 0
    neg=s.startswith('(') or s.startswith('-'); s=s.strip('()-')
    return -int(round(float(s))) if neg else int(round(float(s)))
SPV={(r['school'],r['metric']):r for r in csv.DictReader(open('data/sportico_values.csv',encoding='utf-8'))}
master=json.load(open('data/schools_master.json'))
entry={}
for s in master:
    r=SPV.get((s['name'],'sp_fiscal_year'))
    if r:
        m=re.search(r"entry '([^']+)'",r['notes']); entry[s['name']]=m.group(1) if m else None
wb=openpyxl.load_workbook('Power4_Athletic_Department_Benchmarking.xlsx',data_only=True); ws=wb['FY25 FRS Clean']
hdr=[c.value for c in ws[6]]; c0=hdr.index('School')
schools=[]; bad=0; cells=0; unplaced=0
for row in ws.iter_rows(min_row=7,values_only=True):
    if not row[c0]: continue
    n=row[c0]; schools.append(n); T=data[entry[n]]['2025']['Totals']
    raw=collections.Counter(); rawname={}
    for k,v in T.items():
        if isinstance(v,list) and len(v)==6: raw[num(v[5])]+=1; rawname.setdefault(num(v[5]),[]).append(k)
    used=collections.Counter()
    for h,v in zip(hdr[c0+2:],row[c0+2:]):
        if h in ('Note','Source') or h is None or h.startswith('Excess'): continue
        if v in ('--',None): continue
        cells+=1
        if raw[v]-used[v]>0 or v==0: used[v]+=1
        else:
            bad+=1; print('NOT IN RAW',n,'|',h,'|',v)
    # every non-zero raw line placed?
    for k,v in T.items():
        if isinstance(v,list) and len(v)==6 and num(v[5])!=0 and used[num(v[5])]==0 and not re.match(r'(?i)excess|total ncaa distributions$',k.strip()):
            unplaced+=1; print('RAW NOT ON TAB',n,'|',k,'|',num(v[5]))
    # surplus tie
    ex=[num(v[5]) for k,v in T.items() if isinstance(v,list) and len(v)==6 and k.strip().lower().startswith('excess')]
    sur=row[hdr.index('Excess (deficiency) of revenues over expenses')]
    if ex and sur!=ex[0]: print('SURPLUS',n,sur,ex[0])
print('schools on tab',len(schools),'| numeric cells checked',cells,'| not in raw',bad,'| raw lines not on tab',unplaced)
# coverage: every public Power 4 school with a 2025 Sportico entry is on the tab, and the others have none
pub=[s['name'] for s in master if s['name'] in entry]
for n in pub:
    has=entry[n] in data and '2025' in data[entry[n]]
    if has and n not in schools: print('HAS FY2025 IN SPORTICO BUT NOT ON TAB:',n,'| workbook basis year',SPV[(n,'sp_fiscal_year')]['value'])
    if not has and n in schools: print('ON TAB WITHOUT FY2025 ENTRY:',n)
print('schools with a Sportico entry',len(pub),'| with FY2025',sum(1 for n in pub if '2025' in data.get(entry[n],{})),'| latest year for the rest',{n:max(data[entry[n]]) for n in pub if '2025' not in data.get(entry[n],{})})
print('master schools without a Sportico entry',[s['name'] for s in master if s['name'] not in entry])
print('conferences',collections.Counter(r[c0+1] for r in ws.iter_rows(min_row=7,values_only=True) if r[c0]))
