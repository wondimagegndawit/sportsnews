"""Build bulk-derived values (identity, EADA financial fallback, enrollment, academics, records, Directors' Cup)
for the 67 Power 4 schools and Notre Dame from the raw downloads in data/. Writes data/bulk_values.csv in the common research schema:
school,metric,value,unit,fiscal_year_or_season,source_name,source_url,date_accessed,notes
"""
import csv, json, re, os, sys
import openpyxl
DATE='2026-11-09'
master=json.load(open('data/schools_master.json'))
out=[]
def add(school, metric, value, unit, fy, sname, url, notes=''):
    # Notre Dame was added on 2026-11-11: its NCAA academic records and Sports-Reference page were fetched that day
    d='2026-11-11' if school=='Notre Dame' and ('NCAA' in sname or 'Sports-Reference' in sname) else DATE
    out.append(dict(school=school,metric=metric,value=value,unit=unit,fiscal_year_or_season=fy,source_name=sname,source_url=url,date_accessed=d,notes=notes))

# ---------- Identity (IPEDS HD2024) ----------
HD_URL='https://nces.ed.gov/ipeds/complete-data-files/HD2024.zip'
hd={r['UNITID']:r for r in csv.DictReader(open('data/ipeds/extracted/HD2024.csv',encoding='utf-8-sig'))}
for s in master:
    r=hd[s['unitid']]
    ctrl={'1':'Public','2':'Private','3':'Private'}[r['CONTROL']]
    add(s['name'],'control',ctrl,'text','2024-25','IPEDS HD2024 (CONTROL)',HD_URL,f"UNITID {s['unitid']}; CONTROL={r['CONTROL']} (1=public, 2=private not-for-profit)")
    add(s['name'],'state',r['STABBR'],'text','2024-25','IPEDS HD2024 (STABBR)',HD_URL,f"UNITID {s['unitid']}")
    add(s['name'],'flagship',s['flagship'],'text','','Analyst classification',HD_URL,'Y = the institution generally recognized as its state flagship university; analyst classification, not an IPEDS field')

# ---------- Enrollment (IPEDS EF2024A fall 2024 headcount) ----------
EF_URL='https://nces.ed.gov/ipeds/complete-data-files/EF2024A.zip'
ef={}
for r in csv.DictReader(open('data/ipeds/extracted/ef2024a.csv',encoding='latin-1')):
    if r['EFALEVEL'] in ('1','2'): ef[(r['UNITID'],r['EFALEVEL'])]=int(r['EFTOTLT'])
for s in master:
    u=s['unitid']
    add(s['name'],'total_enrollment',ef[(u,'1')],'students','Fall 2024','IPEDS EF2024A fall headcount',EF_URL,f'UNITID {u}; EFALEVEL=1 (all students total), EFTOTLT')
    add(s['name'],'undergrad_enrollment',ef[(u,'2')],'students','Fall 2024','IPEDS EF2024A fall headcount',EF_URL,f'UNITID {u}; EFALEVEL=2 (undergraduate total), EFTOTLT')
    add(s['name'],'enrollment_year','Fall 2024','text','Fall 2024','IPEDS EF2024A',EF_URL,'')

# ---------- EADA financial fallback (FY ending in 2025, 2024-25 reporting year) ----------
EADA_URL='https://ope.ed.gov/athletics/api/dataFiles/file?fileName=EADA_2024-2025.zip'
wbs=openpyxl.load_workbook('data/eada/extracted/schools.xlsx',read_only=True); wss=wbs.active
its=wss.iter_rows(values_only=True); hdrs=next(its); eada_sport={}
for r in its:
    d=dict(zip(hdrs,r)); u=str(d['unitid'])
    if d.get('Sports')=='Football' and d.get('TOTAL_REVENUE_ALL') is not None: eada_sport.setdefault(u,{})['Football']=int(d['TOTAL_REVENUE_ALL'])
    if d.get('Sports')=='Basketball' and d.get('REV_MEN') is not None: eada_sport.setdefault(u,{})['Basketball']=int(d['REV_MEN'])
wb=openpyxl.load_workbook('data/eada/extracted/instLevel.xlsx',read_only=True); ws=wb.active
it=ws.iter_rows(values_only=True); hdr=next(it)
eada={}
for r in it:
    d=dict(zip(hdr,r)); eada[str(d['unitid'])]=d
for s in master:
    d=eada.get(s['unitid'])
    if not d: print('EADA missing',s['name']); continue
    note=f"EADA institution-level file, unitid {s['unitid']}, {d['institution_name']}; EADA revenue/expense definitions differ from NCAA MFRS; institution page https://ope.ed.gov/athletics/#/institution/{s['unitid']}"
    add(s['name'],'eada_total_revenue',int(d['GRND_TOTAL_REVENUE']),'USD','FY2025 (2024-25 EADA reporting year)','EADA 2024-25 (GRND_TOTAL_REVENUE)',EADA_URL,note)
    add(s['name'],'eada_total_expense',int(d['GRND_TOTAL_EXPENSE']),'USD','FY2025 (2024-25 EADA reporting year)','EADA 2024-25 (GRND_TOTAL_EXPENSE)',EADA_URL,note)
    na=d.get('TOT_REVENUE_ALL_NOTALLOC')
    add(s['name'],'eada_nonprogram_revenue',int(na) if na is not None else '--','USD','FY2025 (2024-25 EADA reporting year)','EADA 2024-25 (TOT_REVENUE_ALL_NOTALLOC)',EADA_URL,note+'; Total Revenues Not Allocated by Sex/Sport')
    sp=eada_sport.get(s['unitid'],{})
    add(s['name'],'eada_fb_revenue',sp.get('Football','--'),'USD','FY2025 (2024-25 EADA reporting year)','EADA 2024-25 schools file (Football TOTAL_REVENUE_ALL)',EADA_URL,note+'; per-sport file, Football row, total revenue')
    add(s['name'],'eada_mbb_revenue',sp.get('Basketball','--'),'USD','FY2025 (2024-25 EADA reporting year)','EADA 2024-25 schools file (Basketball REV_MEN)',EADA_URL,note+"; per-sport file, Basketball row, men's revenue")

# ---------- Academics (NCAA APR / GSR search) ----------
NCAA='https://web3.ncaa.org'
for s in master:
    org=s['apr_org']
    f=f'data/ncaa/apr/{org}_MFB_2025.json'
    if os.path.exists(f) and os.path.getsize(f)>50:
        j=json.load(open(f))
        rec=[x for x in j if x.get('sportCode')=='MFB' and x.get('academicYear')==2025]
        if rec:
            x=rec[0]
            add(s['name'],'fb_apr_multiyear',int(x['apr']),'APR','2024-25','NCAA APR search (public institutional report)',x['publicFilename'],f"Multiyear APR (2021-22 through 2024-25), Football; NCAA org {org}; search tool https://web3.ncaa.org/aprsearch/aprsearch")
        else: add(s['name'],'fb_apr_multiyear','--','APR','2024-25','NCAA APR search','https://web3.ncaa.org/aprsearch/aprsearch','no football 2024-25 APR record returned')
    else: add(s['name'],'fb_apr_multiyear','--','APR','2024-25','NCAA APR search','https://web3.ncaa.org/aprsearch/aprsearch','APR search not retrieved')
    f=f'data/ncaa/gsr/{org}_all.json'
    if os.path.exists(f) and os.path.getsize(f)>50:
        j=json.load(open(f))
        latest=max(x['cohortYear'] for x in j)
        for code,metric,label in [('ALL','dept_gsr','Overall (all sports)'),('MFB','fb_gsr','Football')]:
            rec=[x for x in j if x['sportCode']==code and x['cohortYear']==latest]
            if rec:
                x=rec[0]; url=NCAA+x['gsrReportLink'].split('?')[0]
                add(s['name'],metric,int(x['gsr']),'GSR %',f'{latest} cohort (2024-25 release)' if latest==2018 else f'{latest} cohort','NCAA GSR search (public report)',url,f"{label} Graduation Success Rate from the NCAA's most recent release (published November 2025). It measures student-athletes who entered in the four years {latest-3}-{str(latest-2)[2:]} through {latest}-{str(latest+1)[2:]} and allows six years to graduate, which is why the entering years look old. Search tool https://web3.ncaa.org/aprsearch/gsrsearch")
            else: add(s['name'],metric,'--','GSR %','','NCAA GSR search','https://web3.ncaa.org/aprsearch/gsrsearch',f'no {label} GSR record')
        add(s['name'],'academic_data_year','2024-25' if latest==2018 else f'cohort {latest}','text','2024-25','NCAA APR/GSR search','https://web3.ncaa.org/aprsearch/aprsearch','Most recent NCAA releases as of November 2026. APR: 2024-25 multiyear rate. GSR: published November 2025, covering student-athletes who entered 2015-16 through 2018-19.')
    else:
        for metric in ('dept_gsr','fb_gsr'): add(s['name'],metric,'--','GSR %','','NCAA GSR search','https://web3.ncaa.org/aprsearch/gsrsearch','GSR search not retrieved')
        add(s['name'],'academic_data_year','--','text','','','', '')

# ---------- Football records 2021-2025 (ESPN standings) ----------
def espn_records(sport_path, season):
    d=json.load(open(f'data/espn/{sport_path}_standings_{season}.json')); res={}
    def walk(n):
        if 'standings' in n:
            for e in n['standings']['entries']:
                st={x['name']:x.get('displayValue') for x in e['stats']}
                res[e['team']['displayName']]=st.get('overall')
        for c in n.get('children',[]): walk(c)
    walk(d); return res
fb={yr:espn_records('cfb',yr) for yr in range(2021,2026)}
for s in master:
    W=L=0; parts=[]
    for yr in range(2021,2026):
        rec=fb[yr].get(s['espn']); w,l=[int(v) for v in rec.split('-')[:2]]
        W+=w; L+=l; parts.append(f'{yr}: {w}-{l}')
    note='Season-by-season overall records (incl. bowls/CFP) from ESPN FBS standings pages 2021-2025: '+'; '.join(parts)+'. Sports-Reference CFB and stats.ncaa.org refused automated access from this environment.'
    add(s['name'],'fb_wins_2021_25',W,'wins','2021-2025 seasons','ESPN college football standings','https://www.espn.com/college-football/standings/_/season/2025',note)
    add(s['name'],'fb_losses_2021_25',L,'losses','2021-2025 seasons','ESPN college football standings','https://www.espn.com/college-football/standings/_/season/2025',note)

# ---------- Men's basketball records 2021-22 to 2025-26 (Sports-Reference CBB school page) ----------
mbb_espn={yr:espn_records('mbb',yr) for yr in range(2022,2027)}
for s in master:
    f=f"data/sports_reference/cbb/{s['sr_cbb']}.html"; url=f"https://www.sports-reference.com/cbb/schools/{s['sr_cbb']}/men/"
    seasons=['2021-22','2022-23','2023-24','2024-25','2025-26']; got={}
    if os.path.exists(f) and os.path.getsize(f)>20000:
        h=open(f,encoding='utf-8',errors='ignore').read()
        for tr in re.findall(r'<tr[^>]*>(.*?)</tr>',h,re.S):
            cells=dict((k,re.sub('<[^>]+>','',v).strip()) for k,v in re.findall(r'<t[hd][^>]*data-stat="([^"]*)"[^>]*>(.*?)</t[hd]>',tr,re.S))
            if cells.get('season') in seasons and cells.get('wins','').isdigit() and cells['season'] not in got:
                got[cells['season']]=(int(cells['wins']),int(cells['losses']))
    if len(got)==5:
        W=sum(v[0] for v in got.values()); L=sum(v[1] for v in got.values())
        # cross-check vs ESPN
        xw=xl=0
        for yr in range(2022,2027):
            rec=mbb_espn[yr].get(s['espn']); 
            if rec: w,l=[int(v) for v in rec.split('-')[:2]]; xw+=w; xl+=l
        flag='' if (xw,xl)==(W,L) else f' NOTE: ESPN standings cross-check differs ({xw}-{xl}).'
        note='Season-by-season overall records from the Sports-Reference school page: '+'; '.join(f'{k}: {v[0]}-{v[1]}' for k,v in sorted(got.items()))+'.'+flag
        add(s['name'],'mbb_wins_2122_2526',W,'wins','2021-22 to 2025-26','Sports-Reference (CBB) school page',url,note)
        add(s['name'],'mbb_losses_2122_2526',L,'losses','2021-22 to 2025-26','Sports-Reference (CBB) school page',url,note)
    else:
        add(s['name'],'mbb_wins_2122_2526','--','wins','2021-22 to 2025-26','Sports-Reference (CBB)',url,f'page not retrieved or seasons missing ({len(got)} of 5)')
        add(s['name'],'mbb_losses_2122_2526','--','losses','2021-22 to 2025-26','Sports-Reference (CBB)',url,f'page not retrieved or seasons missing ({len(got)} of 5)')

# ---------- Directors' Cup (NACDA final standings PDFs) ----------
dc=json.load(open('data/nacda/directors_cup_p4_parsed.json'))
DC_URLS={'2024-25':'https://nacda.com/documents/2025/6/23/24.25DivIStandingsFinal.pdf','2025-26':'https://nacda.com/documents/2026/6/24/25.26DI_Final.pdf'}
for season,suffix in [('2024-25','2425'),('2025-26','2526')]:
    byname={r['inst']:r for r in dc[season]}
    for s in master:
        r=byname.get(s['nacda'])
        if r:
            add(s['name'],f'dcup_rank_{suffix}',r['rank'],'rank',season,f"NACDA LEARFIELD Directors' Cup {season} Division I Final Standings",DC_URLS[season],'Final Division I standings PDF (nacda.com)')
            add(s['name'],f'dcup_points_{suffix}',r['points'],'points',season,f"NACDA LEARFIELD Directors' Cup {season} Division I Final Standings",DC_URLS[season],'Final Division I standings PDF (nacda.com)')
        else:
            add(s['name'],f'dcup_rank_{suffix}','--','rank',season,'NACDA',DC_URLS[season],'not found in parsed standings')
            add(s['name'],f'dcup_points_{suffix}','--','points',season,'NACDA',DC_URLS[season],'not found in parsed standings')

with open('data/bulk_values.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']); w.writeheader(); w.writerows(out)
print('rows',len(out)); 
from collections import Counter
c=Counter((r['metric'],r['value']=='--') for r in out); print(sorted(c.items()))
