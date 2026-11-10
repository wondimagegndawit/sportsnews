"""Review the subagent research CSVs against the source rules, merge with bulk values, and write data/merged_values.csv
plus data/review_rejections.csv. One row per (school, metric): first accepted valued row wins; else first '--' row."""
import csv, re, json, os
from collections import OrderedDict
R='/tmp/claude-0/-home-user-sportsnews/13880bdf-16ac-52e7-abd6-56bf6c41826b/scratchpad/research'
import glob
files=["data/bulk_values.csv","data/sportico_values.csv"]+sorted(glob.glob(f"{R}/*.csv"))
NUM=re.compile(r'(revenue|expense|distributions|support|fees|salaries|debt|_comp$|_end$|capacity|opened|renovation|start_year|term_years|annual_value|total_value|varsity|fiscal_year|enrollment$|_wins_|_losses_|apr|gsr$|dcup_)')
QUAL=re.compile(r'(approx|about|~|\best\b|up to|unknown|unverified|tbd|n/a|\?)',re.I)
rows=[]; rej=[]
for f in files:
    for r in csv.DictReader(open(f,encoding='utf-8')):
        r={k:(v or '').strip() for k,v in r.items()}
        r['_file']=os.path.basename(f); rows.append(r)
def reject(r,why):
    rej.append(dict(r,reason=why)); r['value']='--'; r['notes']=f'rejected in review ({why}); '+r['notes']; r['source_url']=''
for r in rows:
    v=r['value']; m=r['metric']
    if v=='--' or v=='': r['value']='--'; continue
    if m in ('fin_report_url',): continue
    url=r['source_url'].lower()
    if not url: reject(r,'no source URL'); continue
    if 'usatoday' in url or 'wikipedia' in url or 'wikiwand' in url or 'usa today' in r['source_name'].lower(): reject(r,'prohibited source'); continue
    if 'stadiumjourney' in url or 'wiki' in url: reject(r,'fan site or wiki mirror not accepted as a source'); continue
    if re.search(r'(projection|expected to generate|conservative estimated)',r['notes'],re.I) and re.search(r'(annual_value|total_value)',m): reject(r,'projected value, not a contract figure'); continue
    if re.search(r'(inferred|computed from|not stated directly|assum|estimat|derived from the term sheet|plus \$?\d|average of|not read directly|probably|unverified|not verified|wikipedia mirror)',r['notes'],re.I) and (m.endswith('_comp') or m.endswith('_contract_end') or re.search(r'(capacity|opened|renovation|start_year|term_years|annual_value|total_value)',m)):
        reject(r,'value inferred, computed or unverified per the note'); continue
    if NUM.search(m) and m not in ('enrollment_year','academic_data_year'):
        if not re.fullmatch(r'-?\d+(\.\d+)?',v.replace(',','')): reject(r,'numeric metric with non-numeric value'); continue
        r['value']=v.replace(',','')
    else:
        if QUAL.search(v) and m not in ('notes',): reject(r,'qualifier text in value'); continue
    if m.endswith('_deal_type'):
        vv=v.lower()
        if vv not in ('commercial','honorific','none'): reject(r,'deal type not commercial/honorific/none'); continue
        r['value']=vv
    if m.endswith('_pay_source_type'):
        vv=v.lower()
        if 'contract' in vv: r['value']='contract'
        elif 'announce' in vv or 'release' in vv: r['value']='school announcement'
        elif 'salary' in vv or 'database' in vv: r['value']='state salary database'
        elif 'press' in vv or 'report' in vv or 'news' in vv: r['value']='press report'
        else: reject(r,'unrecognized pay source type'); continue
merged=OrderedDict()
# files are processed in order (bulk, then research rounds r1..r4 alphabetically); a later valued row overrides an
# earlier one (later rounds only re-reported a cell to correct it). A changed deal partner also voids the earlier
# round's sub-fields for that deal, since they describe the superseded contract.
for r in rows:
    k=(r['school'],r['metric'])
    if k not in merged: merged[k]=r; continue
    if r['value']=='--': continue
    prev=merged[k]
    if prev['value']!='--' and prev['value'].lower()!=r['value'].lower() and r['metric'].endswith('_partner'):
        pre=r['metric'][:-8]
        for kk in list(merged):
            if kk[0]==r['school'] and kk[1].startswith(pre+'_') and kk[1]!=r['metric'] and merged[kk]['_file']!=r['_file']:
                merged[kk]=dict(merged[kk],value='--',source_url='',notes='superseded: deal partner changed to '+r['value']+'; '+merged[kk]['notes'])
    merged[k]=r
fields=['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes','_file']
with open('data/merged_values.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(merged.values())
with open('data/review_rejections.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields+['reason'],extrasaction='ignore'); w.writeheader(); w.writerows(rej)
print('merged',len(merged),'rejected',len(rej))
for r in rej: print('  REJECT',r['school'],r['metric'],repr(r['value'])[:60],r['reason'])
