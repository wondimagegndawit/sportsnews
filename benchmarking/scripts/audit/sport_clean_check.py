"""Independent checks of the by-sport tabs against the raw Sportico files and against each other."""
import json,glob,csv,re,collections,openpyxl
wb=openpyxl.load_workbook('Power4_Athletic_Department_Benchmarking.xlsx',data_only=True)
# 1. FY25 FRS Clean by Sport: the five rows of a school add to its row on FY25 FRS Clean, column by column
a=wb['FY25 FRS Clean']; b=wb['FY25 FRS Clean by Sport']
ha=[c.value for c in a[6]]; hb=[c.value for c in b[6]]
tot={row[2]:dict(zip(ha,row)) for row in a.iter_rows(min_row=7,values_only=True) if row[2]}
sums=collections.defaultdict(lambda:collections.defaultdict(int)); nrows=collections.Counter(); cells=0
for row in b.iter_rows(min_row=7,values_only=True):
    if not row[2]: continue
    nrows[row[2]]+=1
    for h,v in zip(hb,row):
        if isinstance(v,(int,float)) and h not in (None,'School','Conference','Sport','Source'): sums[row[2]][h]+=v; cells+=1
bad=0
for s,d in tot.items():
    for h,v in d.items():
        if isinstance(v,(int,float)) and h in sums[s] and abs(sums[s][h]-v)>2: bad+=1; print('SPORT ROWS DO NOT ADD',s,h,sums[s][h],v)
print('FY25 FRS Clean by Sport: schools',len(nrows),'| rows per school',set(nrows.values()),'| numeric cells',cells,'| columns that do not add to FY25 FRS Clean:',bad)
# 2. every by-sport figure is the figure in the raw Sportico file, in the same sport position
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
POS={'Football':0,"Men's basketball":1,"Women's basketball":2,'Other sports':3,'Non-program specific':4}
miss=0; chk=0
for row in b.iter_rows(min_row=7,values_only=True):
    if not row[2]: continue
    s=row[2]; ent=re.search(r"entry '([^']+)'",SPV[(s,'sp_fiscal_year')]['notes']).group(1); T=data[ent]['2025']['Totals']; p=POS[row[4]]
    raw=collections.Counter(num(v[p]) for k,v in T.items() if isinstance(v,list) and len(v)==6)
    for h,v in zip(hb,row):
        if isinstance(v,(int,float)) and h not in (None,'School','Conference','Sport','Source') and not h.startswith('Excess') and v!=0:
            chk+=1
            if raw[int(v)]==0: miss+=1; print('NOT IN RAW',s,row[4],h,v)
print('by-sport figures checked against the raw Sportico files:',chk,'| not found in the same sport column:',miss)
# 3. FRS Detail: lines by section and row type, and the across check
d=wb['FRS Detail']; hd=[c.value for c in d[6]]; i={h:k for k,h in enumerate(hd) if h}
rt=collections.Counter(); off=0; n=0
for row in d.iter_rows(min_row=7,values_only=True):
    if not row[2]: continue
    n+=1; rt[(row[i['Section']],row[i['Row type']])]+=1
    if abs(row[i['Check: sport columns less total']])>2: off+=1
print('FRS Detail rows',n,dict(rt),'| rows where the sport columns do not add to the total:',off)
t=wb['FRS Tie-Out']; print('FRS Tie-Out:',dict(collections.Counter(row[23] for row in t.iter_rows(min_row=7,values_only=True) if row[2])))
