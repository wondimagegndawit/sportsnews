"""Playing-surface names and field / court naming rights (research pass of 17 Nov 2026).

The football field and the basketball court are tracked apart from the stadium and the arena. A deal that names only
the field or court is moved out of the stadium or arena naming columns into the field or court columns.
Findings are in data/surface/*.py (one list per research pass). Run after merge_research.py, then merge again.
Writes data/research/verification_zzzzzzzzzzz_playing_surface.csv."""
import csv, glob, re, os
import subprocess, sys
OUT='data/research/verification_zzzzzzzzzzz_playing_surface.csv'
if os.path.exists(OUT):      # rebuild from the values as they stood before this file was applied, so a re-run gives the same rows
    os.remove(OUT); subprocess.run([sys.executable,'-I','scripts/merge_research.py'],check=True,stdout=subprocess.DEVNULL)
D='2026-11-17'
M=list(csv.DictReader(open('data/merged_values.csv',encoding='utf-8')))
V={(r['school'],r['metric']):r for r in M}
SCHOOLS=sorted({r['school'] for r in M})
ns={}
for f in sorted(glob.glob('data/surface/surface_*.py')): exec(open(f,encoding='utf-8').read(),ns)
FIELD=[x for k in ns if k.startswith('FIELD_') for x in ns[k]]
COURT=[x for k in ns if k.startswith('COURT_') for x in ns[k]]
# fields already sourced in earlier passes
FIELD+=[
('Duke','Brooks Field','Steve and Eileen Brooks (donors)','honorific',"Duke Today (17 Jul 2015)",'https://today.duke.edu/2015/07/brooks',"‘Duke University alumnus Steve Brooks and his wife, Eileen, have committed $13 million’ and asked that ‘the football field be named Brooks Field at Wallace Wade Stadium’."),
('Florida State','Bobby Bowden Field','Bobby Bowden (honoree)','honorific',"Florida State University, Office of the President",'https://president.fsu.edu/?p=252',"‘the field was named after football coach Bobby Bowden’; the full name is Bobby Bowden Field at Doak S. Campbell Stadium."),
('NC State','Wayne Day Family Field','Wayne T. Day and family (donors)','honorific',"International Association of Venue Managers (30 Mar 2023)",'https://blog.iavm.org/north-carolina-state-university-names-daktronics-for-project-at-wayne-day-family-field-at-carter-finley-stadium/',"‘a new video display at Wayne Day Family Field at Carter-Finley Stadium’. The field was named after a ‘$5 million gift from the Day family’ (NCAA News, 27 May 2002)."),
('Iowa State','MidAmerican Energy Field','MidAmerican Energy','commercial',"Radio Iowa (1 Aug 2018)",'https://www.radioiowa.com/2018/08/01/isu-sells-football-field-naming-rights-to-midamerican-energy/',"‘The utility company will pay up to $1.5 million each year for 10 years to have its name on the field.’ ‘The stadium itself will continue to be called Jack Trice Stadium.’"),
('Indiana','Merchants Bank Field','Merchants Bank','commercial',"WFIU/WTIU News, Indiana Public Media (21 Aug 2025)",'https://www.ipm.org/news/2025-08-21/iu-football-field-has-sponsor-paying-50-million-over-20-years',"‘The field at Memorial Stadium will be renamed Merchants Bank Field at Memorial Stadium. Merchants Bank is paying $50 million over 20 years for naming rights.’"),
('UCLA','Spieker Field','Tod Spieker family (donors)','honorific',"ESPN via ABC7 (19 Sep 2017)",'https://abc7.com/post/ucla-to-play-on-spieker-field-at-the-rose-bowl-after-$10m-donation/2433421/',"A $10 million donation names the field ‘Spieker Field at the Rose Bowl’ ‘for at least the next 25 years’. Donor naming, not a corporate deal."),
('Wisconsin','Barry Alvarez Field','Barry Alvarez (honoree)','honorific',"University of Wisconsin-Madison News (2 Oct 2021)",'https://news.wisc.edu/presenting-barry-alvarez-field',"‘The football field will be named Barry Alvarez Field at Camp Randall Stadium beginning in 2022.’"),
]
seen=set(); F2=[]
for x in FIELD:      # research-pass rows win over the inline ones
    if x[0] not in seen: seen.add(x[0]); F2.append(x)
FIELD=F2
rows=[]
def add(school,metric,value,season,src,url,note):
    unit='USD' if metric.endswith('_value') else 'years' if metric.endswith('term_years') else 'year' if metric.endswith('_year') else 'text'
    rows.append([school,metric,value,unit,season,src,url if value not in ('--','') or url else url,D,note])
def copy(school,old,new):
    r=V.get((school,old))
    if r: rows.append([school,new,r['value'],r['unit'],r['fiscal_year_or_season'],r['source_name'],r['source_url'],r.get('date_accessed') or D,r['notes']])
    return r
# deals that name the playing surface only: (school, building prefix, surface prefix, what the building itself is named for, deal type of the building name, industry)
MOVE={'California':('stadium_nr','field_nr','none','none'),'Georgia Tech':('stadium_nr','field_nr','Bobby Dodd (honoree)','honorific'),'Indiana':('stadium_nr','field_nr','none','none'),
      'Iowa State':('stadium_nr','field_nr','Jack Trice (honoree)','honorific'),'Penn State':('stadium_nr','field_nr','Beaver (stadium name retained)','honorific'),'USC':('stadium_nr','field_nr','none','none'),
      'Virginia Tech':('arena_nr','court_nr','Cassell (honoree)','honorific')}
IND={'Iowa':'telecommunications (cable)','Ohio State':'auto glass'}
def surface(kind,pre,items):
    label='field' if kind=='field' else 'court'
    for school,name,who,cls,src,url,quote in items:
        if cls=='--':
            for m in (f'{kind}_name',f'{pre}_partner',f'{pre}_deal_type',f'{pre}_industry',f'{pre}_start_year',f'{pre}_term_years',f'{pre}_annual_value',f'{pre}_total_value'): add(school,m,'--','2026',src,'',quote)
            continue
        add(school,f'{kind}_name',name,'2026',src,url,quote)
        add(school,f'{pre}_partner',who if cls!='none' or who else 'none','2026',src,url,quote); add(school,f'{pre}_deal_type',cls,'2026',src,url,quote)
        if cls=='commercial' and school in MOVE and MOVE[school][1]==pre:
            old=MOVE[school][0]
            for m in ('industry','start_year','term_years','annual_value','total_value','end_year'): copy(school,f'{old}_{m}',f'{pre}_{m}')
        elif cls=='commercial':
            add(school,f'{pre}_industry',IND.get(school,'--'),'2026',src,url,'Industry classified by researcher.')
            for m in ('start_year','term_years','annual_value','total_value'): add(school,f'{pre}_{m}','--','2026',src,'',f"Terms of the {label} naming agreement have not been released.")
        else:
            why=(f'honorific; no commercial fee' if cls=='honorific' else f"The {label} has no naming deal.")
            for m in ('industry','start_year','term_years','annual_value','total_value'): add(school,f'{pre}_{m}','--','2026',src,'',why)
surface('field','field_nr',FIELD); surface('court','court_nr',COURT)
# the building columns for the moved deals: the building keeps its own name
for school,(old,new,who,cls) in MOVE.items():
    p=V[(school,f'{old}_partner')]; what='field' if new=='field_nr' else 'court'
    note=f"The naming deal with {p['value']} covers the {what} only and is shown in the {what} naming rights columns; the building keeps its own name."
    rows.append([school,f'{old}_partner',who,'text','2026',p['source_name'],p['source_url'],D,note]); rows.append([school,f'{old}_deal_type',cls,'text','2026',p['source_name'],p['source_url'],D,note])
    for m in ('industry','start_year','term_years','annual_value','total_value'): rows.append([school,f'{old}_{m}','--','','2026',p['source_name'],'',D,f"Moved to the {what} naming rights columns: the deal names the {what}, not the building."])
    if (school,f'{old}_end_year') in V: rows.append([school,f'{old}_end_year','--','year','2026',p['source_name'],'',D,f"Moved to the {what} naming rights columns."])
# Virginia Tech court: the 2015 terms have run their course
VT="Virginia Tech News (5 Aug 2015)"; VTU='https://news.vt.edu/articles/2015/08/080515-development-cassellfloornamed.html'
rows[:]=[r for r in rows if not (r[0]=='Virginia Tech' and r[1] in ('court_nr_start_year','court_nr_term_years','court_nr_annual_value','court_nr_total_value','court_nr_end_year'))]
for m in ('start_year','term_years','annual_value','total_value'):
    add('Virginia Tech','court_nr_'+m,'--','2026',VT,'',"The 2015 agreement gave Carilion ‘naming privileges to the court for 10 years’ at ‘$500,000 a year’. That term has run and no renewal terms were found, so no current terms are entered.")
# Georgia Tech: cite the report that states the field deal and the stadium's own name
FX="FOX 5 Atlanta (8 Aug 2023)"; FXU='https://www.fox5atlanta.com/sports/georgia-tech-announces-field-naming-deal-with-hyundai-for-bobby-dodd-stadium'
FXQ="‘a deal on Tuesday for Hyundai to pay Georgia Tech approximately $55 million over 20 years for naming rights to the field.’"
rows[:]=[r for r in rows if not (r[0]=='Georgia Tech' and r[1] in ('field_nr_term_years','field_nr_total_value','stadium_nr_partner','stadium_nr_deal_type'))]
add('Georgia Tech','field_nr_term_years',20,'2023 to 2043',FX,FXU,FXQ); add('Georgia Tech','field_nr_total_value',55000000,'2023 to 2043',FX,FXU,FXQ)
for m,v in (('stadium_nr_partner','Bobby Dodd (honoree)'),('stadium_nr_deal_type','honorific')):
    add('Georgia Tech',m,v,'2026',FX,FXU,"‘renamed Bobby Dodd Stadium in 1988 in honor of the former Georgia Tech coach and athletic director.’ Hyundai's deal covers the field only and is shown in the field naming rights columns.")
# Ohio State: the release gives the start of the field naming and no other terms
rows[:]=[r for r in rows if not (r[0]=='Ohio State' and r[1]=='field_nr_start_year')]
add('Ohio State','field_nr_start_year',2022,'from 2022',"WOSU (26 Aug 2022)",'https://www.wosu.org/sports/2022-08-26/safelite-becomes-sponsor-of-ohio-stadium-field',"Safelite became the sponsor of the Ohio Stadium field for the 2022 season under a multi-year agreement. ‘No financial terms were disclosed.’")
# stadium name column: the building's name only, where the stored name also carried the field
def building(n):
    n=re.sub(r'\s*\(.*\)$','',n)
    for pat,rep in ((r'^(.+ Field) at (the )?(.+)$',r'\3'),(r'^(.+ Stadium) at (.+ Field)$',r'\1'),(r'^(.+ Stadium)\s*/\s*(.+ Field)$',r'\1')):
        m=re.match(pat,n)
        if m: n=m.expand(rep); break
    return n
for s in SCHOOLS:
    r=V.get((s,'stadium_name'))
    if not r or r['value'] in ('--',''): continue
    b=building(r['value'])
    if b!=r['value']: rows.append([s,'stadium_name',b,'text',r['fiscal_year_or_season'],r['source_name'],r['source_url'],r.get('date_accessed') or D,(r['notes']+' ' if r['notes'] else '')+f"Building name only; the playing surface is in the Playing surface name column (stored before as ‘{r['value']}’)."])
done={r[0] for r in rows if r[1]=='field_name'}; donec={r[0] for r in rows if r[1]=='court_name'}
print('rows',len(rows),'| fields',len(done),'missing',sorted(set(SCHOOLS)-done),'| courts',len(donec),'missing',sorted(set(SCHOOLS)-donec))
with open(OUT,'w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']); w.writerows(rows)
