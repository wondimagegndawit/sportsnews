"""Automated check of every researched hardcode against the text of its cited source page.

Usage (from benchmarking/):  python3 -I scripts/verify_sources.py <cache_dir>
  1. lists each researched value in the workbook's Source Log with its cell and source URL (bulk datasets are skipped:
     they are tied out against the raw files in data/);
  2. fetches each distinct URL once into <cache_dir>/pages (kept outside the repository; pages are third-party content);
  3. looks for the value in the page text (numbers with and without separators, dollar amounts in "million" forms,
     terms as "N-year", names and partner names as text) and writes data/verification/auto_check.csv.
A value that is found is strong evidence for specific numbers and names and weak evidence for bare years and small
counts; the strength is recorded. Pages are untrusted input: only their text is read.
"""
import openpyxl,warnings,re,json,csv,hashlib,sys,os,subprocess,html,collections
warnings.simplefilter('ignore')
from openpyxl.utils import get_column_letter as L
out=sys.argv[1]; os.makedirs(out+'/pages',exist_ok=True); d=out
F='Power4_Athletic_Department_Benchmarking.xlsx'
wb=openpyxl.load_workbook(F); bv=openpyxl.load_workbook(F,data_only=True); lay=json.load(open('data/workbook_layout.json'))
cell={}
for t,lc in lay['conf_layout'].items():
    ws=wb[t]; H={ws.cell(6,c).value:c for c in range(3,ws.max_column+1)}
    for r in range(lc['first'],lc['last']+1):
        for h,c in H.items(): cell[(ws.cell(r,3).value,h)]=(t,f'{L(c)}{r}',ws.cell(r,c).value,bv[t].cell(r,c).value)
BULK=('nces.ed.gov','ope.ed.gov','espn.com/college-football/standings','sports-reference.com/cbb/schools','nacda.com/documents','d1ticker.com','fs.ncaa.org','sportico.com','web3.ncaa.org')
sl=bv['Source Log']; rows=[]
for r in range(7,sl.max_row+1):
    v=sl.cell(r,6).value; url=str(sl.cell(r,11).value or ''); school=sl.cell(r,3).value; metric=sl.cell(r,5).value
    if v in (None,'--') or not url.startswith('http') or any(b in url for b in BULK): continue
    if metric in ('School','Conference','Public or Private','State'): continue
    tab,addr,raw,shown=cell[(school,metric)]
    note=str(sl.cell(r,13).value or ''); src=str(sl.cell(r,10).value or '')
    rows.append(dict(log_row=r,school=school,tab=tab,cell=addr,metric=metric,value=v,shown=shown,is_formula=isinstance(raw,str) and str(raw).startswith('='),source=src,url=url,note=note,
                     snippet=bool(re.search(r'search (snippet|summary|excerpt|result)',note+' '+src,re.I)),uid=hashlib.md5(url.encode()).hexdigest()[:12]))
json.dump(rows,open(out+'/rows.json','w'))
urls=sorted({(x['uid'],x['url']) for x in rows})
with open(out+'/urls.tsv','w') as f:
    for u,url in urls: f.write(f'{u}\t{url}\n')
print('researched hardcodes',len(rows),'| unique source URLs',len(urls),'| snippet-sourced',sum(x['snippet'] for x in rows))

UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
def fetch(uid,url):
    b=f'{out}/pages/{uid}'
    if os.path.exists(b+'.meta') and os.path.getsize(b+'.meta')>0: return
    r=subprocess.run(['curl','-sS','-L','-m','40','--max-filesize','30000000','-A',UA,'-H','Accept: text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8','-o',b+'.bin','-w','%{http_code}\t%{content_type}',url],capture_output=True,text=True)
    open(b+'.meta','w').write((r.stdout or '000\t')+'\n')
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(8) as ex_: list(ex_.map(lambda p: fetch(*p),urls))
cache={}
WORDS={1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten',11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen',16:'sixteen',17:'seventeen',18:'eighteen',19:'nineteen',20:'twenty',25:'twenty-five',30:'thirty'}
def text(uid):
    if uid in cache: return cache[uid]
    p=f'{d}/pages/{uid}.bin'; meta=open(f'{d}/pages/{uid}.meta').read().strip().split('\t'); code=meta[0]; ct=meta[1] if len(meta)>1 else ''
    t=''
    if os.path.exists(p) and code=='200':
        raw=open(p,'rb').read()
        if raw[:5]==b'%PDF-' or 'pdf' in ct: t=subprocess.run(['pdftotext','-layout',p,'-'],capture_output=True,text=True,errors='replace').stdout
        else:
            s=raw.decode('utf-8',errors='replace')
            meta_c=' '.join(re.findall(r'content="([^"]{20,})"',s)); ld=' '.join(re.findall(r'"(?:articleBody|description|headline|content)"\s*:\s*"((?:[^"\\]|\\.){20,})"',s))
            body=re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>',' ',s,flags=re.S|re.I))
            t=html.unescape(body+' '+meta_c+' '+ld.replace('\\u003c',' ').replace('\\n',' '))
            t=re.sub(r'<[^>]+>',' ',t)
    t=re.sub(r'\s+',' ',t).replace('’',"'").replace('‑','-').replace('–','-').replace('—','-')
    cache[uid]=(code,t); return cache[uid]
def money_forms(n):
    f={f'{n:,}',str(n)}
    if n>=1_000_000:
        m=n/1e6
        for s in {f'{m:g}',f'{m:.1f}',f'{m:.2f}',f'{m:.3f}'.rstrip('0').rstrip('.')}:
            f|={f'${s} million',f'${s}M',f'{s} million',f'${s}-million',f'${s} mil',f'{s}M'}
        if n>=1_000_000_000: f|={f'${n/1e9:g} billion'}
    elif n>=1000:
        k=n/1e3
        for s in {f'{k:g}'}: f|={f'${s}K',f'${s}k',f'{s}K'}
    return f
def check(x,t):
    v=x['value']; m=x['metric']; tl=t.lower()
    if re.search(r'deal type|pay source type|industry$',m) or str(v).lower() in ('none','in-house','other'): return 'classification',None,'n/a'
    if isinstance(v,(int,float)) and not isinstance(v,bool):
        n=int(v) if float(v).is_integer() else v
        if re.search(r'value|compensation',m):
            for f in sorted(money_forms(int(n)),key=len,reverse=True):
                if re.search(r'(?<![\d,.$])'+re.escape(f)+r'(?![\d,]|\.\d)',t,re.I) or re.search(r'(?<![\d,.])'+re.escape(f)+r'(?![\d,]|\.\d)',t,re.I): return 'found',f,'strong'
            return 'not found',None,'strong'
        if 'term' in m:
            pats=[rf'\b{n}[- ]?years?\b',rf'\b{n}[- ]seasons?\b']+([rf'\b{WORDS[n]}[- ]years?\b',rf'\b{WORDS[n]}[- ]seasons?\b'] if n in WORDS else [])
            for p in pats:
                mm=re.search(p,tl)
                if mm: return 'found',mm.group(0),'medium'
            return 'not found',None,'medium'
        if re.search(r'year|opened|renovation',m):
            return ('found',str(n),'weak') if re.search(rf'(?<!\d){n}(?!\d)',t) else ('not found',None,'weak')
        if 'Varsity' in m:
            mm=re.search(rf'\b({n}|{WORDS.get(n,"zzz")})\b[^.{{}}]{{0,40}}\b(sports?|teams?|varsity|programs?)\b',tl)
            return ('found',mm.group(0)[:40],'medium') if mm else ('not found',None,'medium')
        for f in (f'{n:,}',str(n)):
            if re.search(r'(?<![\d,.])'+re.escape(f)+r'(?![\d,])',t): return 'found',f,'strong' if n>=1000 else 'weak'
        return 'not found',None,'strong' if n>=1000 else 'weak'
    s=str(v).lower().replace('’',"'"); 
    if s in tl: return 'found',str(v),'strong'
    s2=re.sub(r'\s*\(.*?\)','',s).strip()                # drop "(interim)" and similar
    if s2 and s2 in tl: return 'found',s2,'strong'
    toks=[w for w in re.findall(r"[a-z0-9'&.-]+",s2) if len(w)>2 and w not in ('the','and','stadium','arena','field','center','centre','at')]
    if toks and all(w in tl for w in toks): return 'found','all words: '+' '.join(toks),'medium'
    if 'coach' in m.lower() and toks and toks[-1] in tl: return 'found','surname: '+toks[-1],'medium'
    return 'not found',None,'strong'
res=[]
for x in rows:
    code,t=text(x['uid'])
    if code!='200' or len(t)<1200: st,hit,strength=('unreadable',None,'n/a') if not (re.search(r'deal type|pay source type|industry$',x['metric']) or str(x['value']).lower() in ('none','in-house','other')) else ('classification',None,'n/a')
    else: st,hit,strength=check(x,t)
    res.append(dict(x,http=code,textlen=len(t),status=st,hit=hit,strength=strength))
json.dump(res,open(d+'/results.json','w'))
os.makedirs('data/verification',exist_ok=True)
with open('data/verification/auto_check.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['log_row','school','tab','cell','metric','value','status','matched_text','strength','http','source_name','url'])
    for o in res: w.writerow([o['log_row'],o['school'],o['tab'],o['cell'],o['metric'],o['value'],o['status'],o['hit'] or '',o['strength'],o['http'],o['source'],o['url']])
c=collections.Counter((o['status']) for o in res); print('all researched hardcodes:',dict(c))
def grp(m):
    if re.search(r'compensation',m): return 'coach pay'
    if re.search(r'annual value|total value',m): return 'deal dollars'
    if re.search(r'term|start year',m): return 'deal term/start'
    if re.search(r'contract end',m): return 'coach contract end'
    if re.search(r'coach$',m): return 'coach name'
    if re.search(r'partner',m): return 'partner name'
    if re.search(r'capacity|opened|renovation|stadium$|arena$',m,re.I): return 'venue facts'
    if 'Varsity' in m: return 'varsity sports'
    if re.search(r'revenue|expenses|support|fees|salaries|debt|Fiscal|basis',m): return 'financials (own report)'
    return 'other'
g=collections.defaultdict(collections.Counter)
for o in res: g[grp(o['metric'])][o['status']]+=1
for k,v in sorted(g.items()): print(f'  {k:24s}',dict(v))
print('snippet-sourced:',dict(collections.Counter(o['status'] for o in res if o['snippet'])))
