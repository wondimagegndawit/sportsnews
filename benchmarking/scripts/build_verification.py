"""Combine the automated page check, the re-read results and manual checks into data/verification.csv, the
status shown in the Source Log's Verification column. Run after verify_sources.py and apply_verification.py.
Priority: re-read verdict, then manual check, then automated check. A status is tied to the value it was checked
against; build_workbook.py ignores it if the value has since changed."""
import csv, os
out={}
def same(a,b):
    try: return abs(float(str(a).replace(',',''))-float(str(b).replace(',','')))<1e-9
    except ValueError: return str(a).strip().lower()==str(b).strip().lower()
if os.path.exists('data/verification/auto_check.csv'):
    for r in csv.DictReader(open('data/verification/auto_check.csv',encoding='utf-8')):
        if r['status']=='found': out[(r['school'],r['metric'])]=dict(school=r['school'],metric=r['metric'],value=r['value'],status='Found on source page',method=f"automated text check ({r['strength']} match: {r['matched_text']})",url=r['url'])
if os.path.exists('data/verification/manual_checks.csv'):
    for r in csv.DictReader(open('data/verification/manual_checks.csv',encoding='utf-8')):
        out[(r['school'],r['metric'])]=dict(school=r['school'],metric=r['metric'],value=r['value'],status=r['status'],method=r['note'],url='')
if os.path.exists('data/verification/status_reread.csv'):
    for r in csv.DictReader(open('data/verification/status_reread.csv',encoding='utf-8')):
        k=(r['school'],r['metric']); prev=out.get(k)
        if r['status']=='Not re-verified' and prev and same(prev['value'],r['value']): continue   # an automated match on the page still stands
        out[k]=dict(school=r['school'],metric=r['metric'],value=r['value'],status=r['status'],method='page re-read on 2026-11-13'+(f": ‘{r['quote']}’" if r['quote'] else ''),url=r['url'])
with open('data/verification.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['school','metric','value','status','method','url']); w.writeheader(); w.writerows(out.values())
import collections; print(len(out),dict(collections.Counter(v['status'] for v in out.values())))
