"""Rows from the research pass of 18 Nov 2026 (cells an early pass had left unresearched).
Findings are in data/findings_2026_11_18/rows_*.py. Writes
data/research/verification_zzzzzzzzzzzzzz_research_2026_11_18.csv. Run, then merge_research.py."""
import csv,glob
D='2026-11-18'; ns={}
for f in sorted(glob.glob('data/findings_2026_11_18/rows_*.py')): exec(open(f,encoding='utf-8').read(),ns)
ROWS=[x for k in sorted(ns) if k.startswith('ROWS_') for x in ns[k]]
def unit(m): return 'USD' if m.endswith('_value') or m.endswith('_comp') else 'years' if m.endswith('term_years') else 'year' if m.endswith('_year') or m.endswith('_year_opened') or m.endswith('contract_end') else 'count' if m=='varsity_sports' else 'text'
seen=set(); out=[]
for s,m,v,season,src,url,note in ROWS:
    assert (s,m) not in seen,(s,m); seen.add((s,m)); out.append([s,m,v,unit(m),season,src,url,D,note])
with open('data/research/verification_zzzzzzzzzzzzzz_research_2026_11_18.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']); w.writerows(out)
print('rows',len(out),'values',sum(1 for r in out if r[2]!='--'),'blank reasons',sum(1 for r in out if r[2]=='--'))
