import csv,json,glob,re,collections,importlib.util,sys
D=list(csv.DictReader(open('data/frs_detail.csv',encoding='utf-8')))
COLS=['football','mens_basketball','womens_basketball','other_sports','non_program','total']
by=collections.defaultdict(dict)
for r in D: by[r['school']][(r['section'],r['line_id'])]=[int(r[c]) for c in COLS]+[r['fiscal_year'],r['basis']]
SUB={('Revenue','12')}
res=collections.Counter(); issues=[]
for s,d in by.items():
    fy=d[next(iter(d))][6]
    # 1 columns add across to the line total
    for k,v in d.items():
        if abs(sum(v[:5])-v[5])>1: issues.append((s,'row does not add across',k,sum(v[:5]),v[5]))
        else: res['rows that add across']+=1
    # 2 lines add down to the total, in every column
    for sec in ('Revenue','Expense'):
        if (sec,'') not in d: issues.append((s,sec,'no total line in the source')); continue
        ok=True
        for c in range(6):
            sm=sum(v[c] for k,v in d.items() if k[0]==sec and k[1]!='' and k not in SUB)
            if abs(sm-d[(sec,'')][c])>1: ok=False; issues.append((s,sec,COLS[c],'lines',sm,'total',d[(sec,'')][c],'gap',d[(sec,'')][c]-sm))
        res[f'{sec}: lines add down to the total' if ok else f'{sec}: lines do NOT add down']+=1
    # 3 the NCAA distributions subtotal
    if ('Revenue','12') in d:
        parts=[d.get(('Revenue',i),[0]*6) for i in ('12A','12B','12C')]
        if any(abs(sum(p[c] for p in parts)-d[('Revenue','12')][c])>1 for c in range(6)): issues.append((s,'line 12 is not 12A+12B+12C'))
        else: res['line 12 = 12A+12B+12C']+=1
# 4 nothing left behind in the source: every Sportico row with figures must have landed on a line
data={}
for f in sorted(glob.glob('data/sportico/json*.json')):
    txt=open(f,encoding='utf-8').read(); txt=txt[txt.index('['):].rstrip().rstrip(';')
    for obj in json.loads(txt):
        if isinstance(obj,dict):
            for k,v in obj.items(): data.setdefault(k,{}).update(v if isinstance(v,dict) else {})
SPV={(r['school'],r['metric']):r for r in csv.DictReader(open('data/sportico_values.csv',encoding='utf-8'))}
def num(v):
    s=str(v).replace('$','').replace(',','').strip()
    if s in ('','-'): return 0
    neg=(s.startswith('(') and s.endswith(')')) or s.startswith('-'); s=s.strip('()-')
    try: return -int(round(float(s))) if neg else int(round(float(s)))
    except ValueError: return None
left=[]; excess_ok=0; excess_bad=[]; sport_ok=0; sport_bad=[]
SP=collections.defaultdict(list)
for r in csv.DictReader(open('data/frs_sport_totals.csv',encoding='utf-8')): SP[r['school']].append(r)
for s,d in by.items():
    if d[next(iter(d))][7]!='Sportico (MFRS compilation)': continue
    note=SPV[(s,'sp_fiscal_year')]['notes']; ent=re.search(r"entry '([^']+)'",note).group(1); yr=SPV[(s,'sp_fiscal_year')]['value']
    e=data[ent][yr]; T=e['Totals']
    taken=collections.Counter(tuple(v[:6]) for v in d.values())
    for k,v in T.items():
        if not isinstance(v,list) or not v: continue
        nums=[num(x) for x in v]
        if len(v)!=6: left.append((s,'row with',len(v),'figures',k.strip()[:60])); continue
        key=tuple(nums)
        if re.match(r'\s*Excess',k) or 'Excess (Deficiencies)' in k:
            # 5 independent check: revenue less expenses equals the source's own surplus line
            if ('Revenue','') in d and ('Expense','') in d:
                calc=[d[('Revenue','')][c]-d[('Expense','')][c] for c in range(6)]
                if all(abs(a-b)<=1 for a,b in zip(calc,nums)): excess_ok+=1
                else: excess_bad.append((s,calc[5],nums[5]))
            continue
        if taken[key]>0: taken[key]-=1
        elif any(nums): left.append((s,'not placed',k.strip()[:70],nums[5]))
    # 6 the individual sports add up to the sport columns of the totals
    if s in SP and ('Revenue','') in d:
        rv=sum(int(r['total_revenue']) for r in SP[s] if r['total_revenue'] not in ('--','')); ex=sum(int(r['total_expenses']) for r in SP[s] if r['total_expenses'] not in ('--',''))
        tr=sum(d[('Revenue','')][:4]); te=sum(d[('Expense','')][:4]) if ('Expense','') in d else None
        if abs(rv-tr)<=2 and (te is None or abs(ex-te)<=2): sport_ok+=1
        else: sport_bad.append((s,'revenue: sports',rv,'statement',tr,'| expenses: sports',ex,'statement',te))
print('schools',len(by),'| rows',len(D)); print(dict(res))
print('surplus line matches revenue less expenses:',excess_ok,'| does not:',excess_bad)
print('individual sports add up to the statement:',sport_ok,'| do not:',len(sport_bad)); [print('   ',x) for x in sport_bad[:12]]
print('source rows not placed on a line:',len(left)); [print('   ',x) for x in left[:25]]
print('issues:',len(issues)); [print('   ',x) for x in issues[:30]]
print('lines per school:',collections.Counter((len(d),d[next(iter(d))][6]) for d in by.values()))
