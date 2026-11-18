"""One-off (18 Nov 2026): give blank deal cells their actual reason where an early research pass left only a
'not researched' note. No values are entered. Three cases, each settled by rows already in the workbook:
  - the venue name is honorific, or the school has no deal of that kind: there are no terms to find
  - multimedia rights are run in-house: there is no rights fee
  - one of total value, annual value and term is blank while the other two are reported: the workbook derives it
Writes data/research/verification_zzzzzzzzzzzzz_blank_reasons.csv. Run after merge_research.py, then merge again."""
import csv,re
D='2026-11-18'; OUT='verification_zzzzzzzzzzzzz_blank_reasons.csv'
M=list(csv.DictReader(open('data/merged_values.csv',encoding='utf-8')))
V={(r['school'],r['metric']):r for r in M}
def stale(r): return r['value'] in ('--','') and ('budget' in (r['notes'] or '') or r['_file']==OUT)
def val(s,m):
    r=V.get((s,m)); return r['value'] if r and r['value'] not in ('--','') else None
LABEL={'apparel':'apparel agreement','mmr':'multimedia rights agreement','patch':'jersey patch deal','stadium_nr':'stadium naming-rights deal','arena_nr':'arena naming-rights deal','field_nr':'field naming-rights deal','court_nr':'court naming-rights deal'}
rows=[]; n={'none':0,'honorific':0,'in-house':0,'derived':0}
FIELDS={'apparel':['start_year','term_years','annual_value','total_value'],'mmr':['start_year','term_years','annual_value','total_value'],'patch':['industry','start_year','term_years','annual_value','total_value'],
        'stadium_nr':['industry','start_year','term_years','annual_value','total_value'],'arena_nr':['industry','start_year','term_years','annual_value','total_value']}
UNIT=lambda f:'USD' if f.endswith('_value') else 'years' if f=='term_years' else 'year' if f=='start_year' else 'text'
# cells an early pass never wrote a row for (mostly SEC): treat them like the stale blanks
CAND=list(M)+[dict(school=s,metric=f'{g}_{f}',value='--',unit=UNIT(f),fiscal_year_or_season='2026',notes='budget',_file='')
              for s in sorted({r['school'] for r in M}) for g,fs in FIELDS.items() for f in fs if (s,f'{g}_{f}') not in V]
for r in CAND:
    if not stale(r): continue
    s,m=r['school'],r['metric']
    g=next((g for g in LABEL if m.startswith(g+'_')),None)
    if not g: continue
    f=m[len(g)+1:]
    if f in ('partner','deal_type'): continue
    partner=val(s,g+'_partner'); dt=val(s,g+'_deal_type'); pr=V.get((s,g+'_partner'))
    src=(pr['source_name'],pr['source_url']) if pr and pr['value'] not in ('--','') else ('','')
    note=None
    if partner and partner.lower()=='none' or dt=='none': note=f"The school has no {LABEL[g]}, so there are no terms."; n['none']+=1
    elif dt=='honorific': note="The name is honorific (a donor or honoree), not a paid naming-rights deal, so there are no commercial terms."; n['honorific']+=1
    elif g=='mmr' and partner and partner.lower()=='in-house': note="The school sells its multimedia rights in-house, so there is no rights fee from an outside rights holder."; n['in-house']+=1
    elif f in ('annual_value','total_value','term_years'):
        others=[x for x in ('annual_value','total_value','term_years') if x!=f]
        if all(val(s,f'{g}_{x}') for x in others):
            note="Not reported by the source; the workbook derives this figure from the two that are reported."; n['derived']+=1
    if note: rows.append([s,m,'--',r['unit'],r['fiscal_year_or_season'] or '2026',src[0],src[1],D,note])
with open('data/research/'+OUT,'w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']); w.writerows(rows)
print('blank-reason rows',len(rows),n)
