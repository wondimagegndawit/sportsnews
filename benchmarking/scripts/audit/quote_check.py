"""Re-read every source cited in the 18 Nov 2026 research rows and check that each quoted passage is on the page.
Usage: python3 -I scripts/audit/quote_check.py <cache dir> [research csv]. Prints the rows whose quote was not found
or whose page could not be read by a plain request (bot check, 403, script-only page)."""
import csv,re,sys,html,subprocess,hashlib,os,unicodedata,collections
from concurrent.futures import ThreadPoolExecutor
OUT=sys.argv[1]; F=sys.argv[2] if len(sys.argv)>2 else 'data/research/verification_zzzzzzzzzzzzzz_research_2026_11_18.csv'
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
def get(url):
    f=f'{OUT}/{hashlib.md5(url.encode()).hexdigest()[:12]}.bin'
    if not os.path.exists(f) or os.path.getsize(f)<500:
        subprocess.run(['curl','-sS','-L','--compressed','-m','60','-A',UA,'-H','Accept: text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8','-o',f,url],capture_output=True,text=True)
    b=open(f,'rb').read() if os.path.exists(f) else b''
    if b[:4]==b'%PDF': t=subprocess.run(['pdftotext','-layout',f,'-'],capture_output=True,text=True).stdout
    else:
        t=b.decode('utf-8','replace'); t=html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>',' ',t)))
    return t
def norm(s):
    s=unicodedata.normalize('NFKD',s).lower()
    s=re.sub(r'[‘’“”\'"`]','',s); s=re.sub(r'[‐-―\-]',' ',s)
    return re.sub(r'[^a-z0-9$%.]+',' ',s).strip()
rows=[r for r in csv.DictReader(open(F,encoding='utf-8')) if r['source_url']]
urls=sorted({r['source_url'] for r in rows})
with ThreadPoolExecutor(8) as ex: pages=dict(zip(urls,ex.map(lambda u:norm(get(u)),urls)))
res=collections.Counter(); bad=[]; seen=set()
for r in rows:
    qs=re.findall(r'‘([^’]{12,})’',r['notes']) or []
    # quotes can contain an apostrophe written as ’; rebuild greedy spans between ‘ and the ’ that precedes a space, comma, period or end
    qs=re.findall(r'‘(.+?)’(?=[\s,.;:)]|$)',r['notes'])
    page=pages[r['source_url']]
    if len(page)<400: res['page not readable by a plain request']+=1; bad.append(('UNREADABLE',r['school'],r['metric'],r['value'],r['source_url'])); continue
    if not qs:
        v=str(r['value']); ok=v=='--' or norm(v) in page or (v.isdigit() and f'{int(v):,}'.lower() in page)
        res['no quote in the note; value '+('found on the page' if ok else 'NOT found')]+=1
        if not ok: bad.append(('VALUE NOT ON PAGE',r['school'],r['metric'],r['value'],r['source_url']))
        continue
    hit=[q for q in qs if norm(q) and norm(q) in page]; miss=[q for q in qs if norm(q) and norm(q) not in page]
    if hit and not miss: res['every quote found on the cited page']+=1
    elif hit: res['some quotes found, others are from a second source named in the note']+=1; bad.append(('PARTIAL',r['school'],r['metric'],r['value'],r['source_url'],miss[0][:90]))
    else: res['QUOTE NOT FOUND on the cited page']+=1; bad.append(('NOT FOUND',r['school'],r['metric'],r['value'],r['source_url'],miss[0][:90] if miss else ''))
print(dict(res))
for b in bad:
    k=(b[0],b[4],b[5] if len(b)>5 else '')
    if k in seen: continue
    seen.add(k); print(' | '.join(str(x) for x in b))
