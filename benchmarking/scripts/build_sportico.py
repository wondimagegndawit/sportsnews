"""Extract Power 4 financials from the Sportico College Sports Finances Database data files (data/sportico/*.json),
which compile NCAA MFRS reports for public FBS schools. Writes data/sportico_values.csv in the research schema
with metric keys prefixed sp_. Latest fiscal year available per school is used; the 'Totals' section, last column
(all-sports total) is read."""
import json, re, glob, csv
DATE='2026-11-10'
URL='https://www.sportico.com/leagues/college-sports/2023/college-sports-finances-database-intercollegiate-1234646029/'
data={}
for f in sorted(glob.glob('data/sportico/json*.json')):
    txt=open(f,encoding='utf-8').read(); txt=txt[txt.index('['):].rstrip().rstrip(';')
    for obj in json.loads(txt):
        for school,years in obj.items():
            for yr,sections in years.items():
                data.setdefault(school,{}).setdefault(yr,{}).update(sections)
master=json.load(open('data/schools_master.json'))
ALIAS={'Virginia Tech':'Virginia Polytechnic Institute and State','Rutgers':'Rutgers, The State University of New','Nebraska':['University of Nebraska, Lincoln','University of Nebraska-Lincoln'],'Colorado':['University of Colorado Boulder','University of Colorado, Boulder'],'Ohio State':'The Ohio State University','North Carolina':'University of North Carolina, Chapel Hill'}
def num(v):
    if v is None: return None
    if isinstance(v,(int,float)): return int(v)
    s=str(v).replace('$','').replace(',','').strip()
    neg=s.startswith('(') and s.endswith(')') or s.startswith('-')
    s=s.strip('()-')
    if s in ('','0.0'): return 0
    try: x=float(s); return -int(x) if neg else int(x)
    except: return None
def line(T,*names):
    for n in names:
        for k,v in T.items():
            if k.strip().lower().startswith(n.lower()) and v not in (None,'',[]): return num(v[-1] if isinstance(v,list) else v)
    return None
out=[]; summary=[]
def add(s,metric,val,unit,fy,note):
    out.append(dict(school=s['name'],metric=metric,value=val if val is not None else '--',unit=unit,fiscal_year_or_season=f'FY{fy}',source_name='Sportico College Sports Finances Database (MFRS compilation)',source_url=URL,date_accessed=DATE,notes=note))
for s in master:
    if s['control']=='Private': continue
    cands=ALIAS.get(s['name'],s['apr_name']); cands=[cands] if isinstance(cands,str) else cands
    years={}
    for c in cands:
        for yr,sec in data.get(c,{}).items(): years[yr]=(c,sec)
    if not years: summary.append((s['name'],'NOT IN SPORTICO')); continue
    def exp_of(T):
        for k,v in T.items():
            if 'total operating expenses' in k.lower() and 'nil' not in k.lower() and v: 
                x=num(v[-1] if isinstance(v,list) else v)
                if x: return x
        return None
    chosen=None; skipped=[]
    for yr in sorted(years,reverse=True):
        cname,sec=years[yr]; T=sec.get('Totals',{})
        rv=line(T,'Total Operating Revenues'); ex=exp_of(T)
        if rv: chosen=yr; break
        skipped.append(f'FY{yr} (total revenue line {rv})')
    if not chosen: summary.append((s['name'],'NO VALID YEAR')); continue
    yr=chosen; cname,sec=years[yr]; T=sec.get('Totals',{}); N=sec.get('Numbers',{})
    note=f"Sportico database entry '{cname}', fiscal year {yr}, Totals view, all-sports total column; compiled from the school's NCAA MFRS report"+(f"; later Sportico year(s) skipped because the total revenue line is missing or zero in the database: "+', '.join(skipped) if skipped else '')
    if exp_of(T) is None: note+='; the Total Operating Expenses line is missing from this Sportico entry'
    vals=dict(
      total_operating_revenue=line(T,'Total Operating Revenues'), total_operating_expenses=exp_of(T),
      media_rights_revenue=line(T,'Media Rights'), ticket_sales_revenue=line(T,'Ticket Sales'), contributions_revenue=line(T,'Contributions'),
      ncaa_distributions=line(T,'Total NCAA Distributions','NCAA Distributions'), conference_distributions=line(T,'Conference Distributions (Non Media'),
      conference_bowl_distributions=line(T,'Conference Distributions of Post','Conference Distributions of Football Bowl'),
      direct_institutional_support=line(T,'Direct Institutional Support'), indirect_6=line(T,'Indirect Institutional Support'), indirect_6a=line(T,'Indirect Institutional Support - Athletic Facilities'),
      student_fees=line(T,'Student Fees'), coaching_salaries=line(T,'Coaching Salaries, Benefits and Bonuses paid by the University'),
      debt_service=line(T,'Athletic Facilities Debt Service'), athletics_related_debt=line(N,'Total Athletics Related Debt') if N else None)
    if vals['athletics_related_debt'] is None:
        for k,v in sec.items():
            if isinstance(v,dict):
                x=line(v,'Total Athletics Related Debt')
                if x is not None: vals['athletics_related_debt']=x; break
    add(s,'sp_fiscal_year',int(yr),'year',yr,note)
    trv=None
    for k,v in T.items():
        if k.strip().lower().startswith('total operating revenues') and isinstance(v,list) and len(v)==6: trv=[num(x) for x in v]; break
    bk=note+'; Total Operating Revenues row, sport column of the Sportico Totals view'
    add(s,'sp_fb_revenue',trv[0] if trv else None,'USD',yr,bk+' (Football)')
    add(s,'sp_mbb_revenue',trv[1] if trv else None,'USD',yr,bk+" (Men's Basketball)")
    add(s,'sp_nonprogram_revenue',trv[4] if trv else None,'USD',yr,bk+' (Non-Program Specific: revenue not attributable to a sport, e.g. media rights, institutional support, student fees)')
    for k in ('total_operating_revenue','total_operating_expenses','media_rights_revenue','ticket_sales_revenue','contributions_revenue','direct_institutional_support','student_fees','coaching_salaries','debt_service','athletics_related_debt'):
        add(s,'sp_'+k,vals[k],'USD',yr,note+('; line 34 includes leases and rental fees' if k=='debt_service' else '')+('; line 22, paid by the university and related entities' if k=='coaching_salaries' else '')+('; line 52' if k=='athletics_related_debt' else ''))
    ind=None
    if vals['indirect_6'] is not None: ind=vals['indirect_6']+(vals['indirect_6a'] or 0)
    add(s,'sp_indirect_institutional_support',ind,'USD',yr,note+f"; line 6 ({vals['indirect_6']}) plus line 6A facilities debt service paid by the institution ({vals['indirect_6a'] or 0})")
    dist=None; parts=[]
    if vals['ncaa_distributions'] is not None and vals['conference_distributions'] is not None:
        dist=vals['ncaa_distributions']+vals['conference_distributions']+(vals['conference_bowl_distributions'] or 0)
        parts=[f"line 12 NCAA distributions {vals['ncaa_distributions']:,}",f"line 13 conference distributions (non media, non post-season) {vals['conference_distributions']:,}",f"line 13A conference post-season distributions {(vals['conference_bowl_distributions'] or 0):,}"]
    add(s,'sp_ncaa_conf_distributions',dist,'USD',yr,note+'; sum of '+'; '.join(parts))
    summary.append((s['name'],yr,vals['total_operating_revenue'],vals['total_operating_expenses'],vals['athletics_related_debt']))
with open('data/sportico_values.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']); w.writeheader(); w.writerows(out)
for x in summary: print(x)
print('rows',len(out))
