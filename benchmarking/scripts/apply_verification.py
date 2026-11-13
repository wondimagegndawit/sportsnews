"""Apply the source re-read to the research data.

Inputs in data/verification/ (copied from the research agents' output):
  reread_*.csv    id,school,metric,current_value,verdict,new_value,quote,source_name,source_url,notes
  coach_fb.csv, coach_mbb.csv   school,sport,name_in_file,verdict,correct_name,role,quote,source_name,source_url,source_date,notes
  decisions.csv   school,metric,decision,reason   (analyst overrides: keep / withdraw)
Outputs:
  data/research/verification_r6.csv   corrected values, substitute sources, and confirmed values with the supporting quote
  data/research_withdrawals.csv       values no source states (blanked in the workbook, reason kept in the Source Log)
  data/verification/status_reread.csv school,metric,value,status,quote,url  (read by build_verification.py)
Run from benchmarking/ after merge_research.py has produced data/merged_values.csv for the previous state.
"""
import csv, glob, json, os, re, sys
DATE='2026-11-13'
lay=json.load(open('data/workbook_layout.json')); KEY={m['hdr']:m['key'] for m in lay['S']}
KEY.update({'Department GSR (%)':'dept_gsr','FB GSR (%)':'fb_gsr','FB multi-year APR':'fb_apr_multiyear'})
KEY.update({'FB HC annual guaranteed compensation':'fb_hc_annual_comp','MBB HC annual guaranteed compensation':'mbb_hc_annual_comp','FB HC total pay':'fb_hc_annual_comp','MBB HC total pay 2026':'mbb_hc_annual_comp','MBB HC total pay 2025':'mbb_hc_prior_comp'})   # the single reported figure feeds the base-pay column
# merged values as they stood BEFORE this script's own output, so reruns are idempotent
base={}
for r in csv.DictReader(open('data/merged_values.csv',encoding='utf-8')):
    base[(r['school'],r['metric'])]=r
orig={}
if os.path.exists('data/verification/base_values.csv'):
    for r in csv.DictReader(open('data/verification/base_values.csv',encoding='utf-8')): orig[(r['school'],r['metric'])]=r
dec={}
if os.path.exists('data/verification/decisions.csv'):
    for r in csv.DictReader(open('data/verification/decisions.csv',encoding='utf-8')): dec[(r['school'],r['metric'])]=r
def clean(v): return str(v).replace(',','').replace('$','').strip()
def num_eq(a,b):
    try: return abs(float(clean(a))-float(clean(b)))<1e-9
    except ValueError: return clean(a).lower()==clean(b).lower()
rows=[]; wd=[]; status=[]; stats={}
def bump(k): stats[k]=stats.get(k,0)+1
def research_row(school,key,value,src,url,note):
    b=orig.get((school,key)) or base.get((school,key)) or {}
    rows.append(dict(school=school,metric=key,value=value,unit=b.get('unit',''),fiscal_year_or_season=b.get('fiscal_year_or_season',''),source_name=src,source_url=url,date_accessed=DATE,notes=note))
def q(s): return re.sub(r'\s+',' ',str(s or '')).strip().strip('"').replace("'","’")
for f in sorted(glob.glob('data/verification/reread_*.csv')):
    for r in csv.DictReader(open(f,encoding='utf-8',errors='replace')):
        school=r['school']; hdr=r['metric']; key=KEY.get(hdr); v=(r.get('verdict') or '').strip().lower(); cur=r['current_value']
        if not key: bump('unknown metric '+hdr); continue
        b=orig.get((school,key)) or base.get((school,key)) or {}
        d=dec.get((school,key),{}).get('decision')
        quote=q(r.get('quote')); note=q(r.get('notes')); url=(r.get('source_url') or '').strip() or b.get('source_url',''); src=q(r.get('source_name')) or b.get('source_name','')
        if d=='classify':   # a descriptive label the analyst assigns (for example who a venue is named for), not a sourced figure
            status.append(dict(school=school,metric=hdr,value=cur,status='Analyst classification',quote='',url=b.get('source_url',''))); bump('kept as classification'); continue
        if d=='withdraw' or (v=='not_stated' and d!='keep'):
            reason=dec.get((school,key),{}).get('reason') or (note or 'No source read states this figure itself.')
            wd.append(dict(school=school,metric=key,withdrawn_value=clean(cur),reason=q(reason).rstrip('.')+'.',date=DATE)); bump('withdrawn'); continue
        if v=='corrected' and clean(r.get('new_value')) not in ('','--'):
            nv=clean(r['new_value']) if re.fullmatch(r'-?[\d,.$]+',r['new_value'].strip()) else r['new_value'].strip()
            if key=='mmr_partner' and 'in-house' in nv.lower(): note=f'In-house entity: {nv}. '+note; nv='in-house'   # the column uses a fixed set of labels
            research_row(school,key,nv,src,url,f"Source states: ‘{quote}’. Corrected on re-read from {cur}."+(' '+note if note else ''))
            status.append(dict(school=school,metric=hdr,value=nv,status='Re-read and confirmed',quote=quote,url=url)); bump('corrected'); continue
        if v=='confirmed' or d=='keep':
            why=dec.get((school,key),{}).get('reason','')
            n=(f"Source states: ‘{quote}’." if quote else '')+(' '+why if d=='keep' and why else '')+(' '+note if note else '')
            research_row(school,key,clean(cur) if re.fullmatch(r'-?[\d,.]+',str(cur).strip()) else cur,src,url,n.strip())
            status.append(dict(school=school,metric=hdr,value=cur,status='Re-read and confirmed',quote=quote,url=url)); bump('confirmed' if v=='confirmed' else 'kept by decision'); continue
        status.append(dict(school=school,metric=hdr,value=cur,status='Not re-verified',quote='',url=b.get('source_url',''))); bump('unreadable')
# analyst withdrawals for values that were not on a re-read list
seen={(w['school'],w['metric']) for w in wd}
for (school,key),r in dec.items():
    if r['decision']=='withdraw' and (school,key) not in seen:
        b=orig.get((school,key)) or base.get((school,key))
        if b and b['value']!='--': wd.append(dict(school=school,metric=key,withdrawn_value=clean(b['value']),reason=q(r['reason']).rstrip('.')+'.',date=DATE)); bump('withdrawn by decision')
# head coaches
DEP={'football':('fb_hc_name','Head football coach',('fb_hc_annual_comp','fb_hc_contract_end','fb_hc_pay_source_type')),'mens basketball':('mbb_hc_name',"Head men's basketball coach",('mbb_hc_annual_comp','mbb_hc_contract_end','mbb_hc_pay_source_type'))}
for f in ('data/verification/coach_fb.csv','data/verification/coach_mbb.csv'):
    if not os.path.exists(f): continue
    for r in csv.DictReader(open(f,encoding='utf-8',errors='replace')):
        key,hdr,deps=DEP[r['sport'].strip().lower()]; school=r['school']; v=r['verdict'].strip().lower(); quote=q(r['quote']); note=q(r.get('notes'))
        if v=='unclear': status.append(dict(school=school,metric=hdr,value=r['name_in_file'],status='Not re-verified',quote='',url='')); bump('coach unclear'); continue
        name=r['correct_name'].strip() if v=='changed' and r['correct_name'].strip() else r['name_in_file'].strip()
        name=re.sub(r'\s*\(interim\)','',name,flags=re.I)+(' (interim)' if r['role'].strip().lower()=='interim' else '')
        dt=f" Page dated {r['source_date']}." if r.get('source_date','').strip() else ''
        research_row(school,key,name,q(r['source_name']),r['source_url'].strip(),f"Source states: ‘{quote}’.{dt} Confirmed as the current head coach on {DATE}."+(' '+note if note else ''))
        status.append(dict(school=school,metric=hdr,value=name,status='Re-read and confirmed',quote=quote,url=r['source_url'].strip())); bump('coach '+v)
        if v=='changed':   # pay and contract cells described the previous coach
            for dk in deps:
                b=orig.get((school,dk)) or base.get((school,dk))
                if b and b['value']!='--' and dec.get((school,dk),{}).get('decision')!='keep':
                    wd.append(dict(school=school,metric=dk,withdrawn_value=clean(b['value']),reason=f"This figure described the previous head coach ({r['name_in_file']}); {name} is now the coach and no figure for the current contract has been sourced.",date=DATE)); bump('withdrawn (previous coach)')
# ---- refresh of stale items and newly found deals (research-schema rows from the currency pass) ----
# valued rows go in as research rows (written to a file that sorts last, so they win); a blank row means the field could
# not be sourced for the agreement now in force, so any older value still in the workbook is withdrawn
cur_rows=[]; NORM={'financial institution (credit union)':'credit union'}
for f in sorted(glob.glob('data/verification/currency_*.csv'))+['data/verification/end_years.csv']:
    if not os.path.exists(f): continue
    for r in csv.DictReader(open(f,encoding='utf-8',errors='replace')):
        school=r['school'].strip(); key=r['metric'].strip(); val=r['value'].strip(); d=dec.get((school,key),{})
        if d.get('decision')=='skip': bump('currency skipped by decision'); continue
        if val in ('','--'):
            b=orig.get((school,key)) or base.get((school,key))
            if b and b['value']!='--' and d.get('decision')=='keep_stale':   # nothing newer found either way: keep, but show it as not re-verified
                hdr=next((h for h,k in KEY.items() if k==key),None)
                if hdr: status.append(dict(school=school,metric=hdr,value=b['value'],status='Not re-verified',quote='',url=b.get('source_url','')))
                bump('kept, not re-verified'); continue
            if b and b['value']!='--' and d.get('decision')!='keep':
                wd.append(dict(school=school,metric=key,withdrawn_value=clean(b['value']),reason=('Not sourced for the agreement now in force. '+q(r['notes'])).strip()[:600].rstrip('.')+'.',date=DATE)); bump('withdrawn (stale)')
            continue
        if key.endswith('_industry') or key.endswith('_deal_type'): val=NORM.get(val.lower(),val.lower())
        cur_rows.append(dict(school=school,metric=key,value=clean(val) if re.fullmatch(r'-?[\d,.$]+',val) else val,unit=r.get('unit',''),fiscal_year_or_season=r.get('fiscal_year_or_season',''),source_name=q(r['source_name']),source_url=r['source_url'].strip(),date_accessed=DATE,notes=q(r['notes'])))
        hdr=next((h for h,k in KEY.items() if k==key),None)
        if hdr and not (key.endswith('_industry') or key.endswith('_deal_type')): status.append(dict(school=school,metric=hdr,value=cur_rows[-1]['value'],status='Re-read and confirmed',quote='',url=r['source_url'].strip()))
        elif key.endswith('_end_year'):
            pre=key[:-9]; hdr=next(h for h,k in KEY.items() if k=='f_'+pre+'_expires'); status.append(dict(school=school,metric=hdr,value=cur_rows[-1]['value'],status='Re-read and confirmed',quote='',url=r['source_url'].strip()))
        bump('currency rows')
# a later withdrawal for the same cell replaces an earlier one; a current value from the currency pass cancels a withdrawal
cur_keys={(r['school'],r['metric']):r['value'] for r in cur_rows}
last={}
for w_ in wd: last[(w_['school'],w_['metric'])]=w_
wd=[w_ for k,w_ in last.items() if not (k in cur_keys and num_eq(cur_keys[k],w_['withdrawn_value']))]
F=['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']
with open('data/research/verification_r6.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=F); w.writeheader(); w.writerows(rows)
with open('data/research/verification_z_currency.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=F); w.writeheader(); w.writerows(cur_rows)
with open('data/research_withdrawals.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['school','metric','withdrawn_value','reason','date']); w.writeheader(); w.writerows(wd)
with open('data/verification/status_reread.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['school','metric','value','status','quote','url']); w.writeheader(); w.writerows(status)
print('research rows',len(rows),'| currency rows',len(cur_rows),'| withdrawals',len(wd),'| statuses',len(status)); print(dict(sorted(stats.items())))
