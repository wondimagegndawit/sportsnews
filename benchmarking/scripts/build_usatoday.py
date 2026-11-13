"""Head coach pay from USA Today's coaches' pay tables: the primary source for coach pay (analyst's decision, 13 Nov 2026).

Source data saved in data/usatoday/:
  football_coach_2025.html                      football table, 2025 season (updated 8 Oct 2025)
  mens_basketball_coach_2025-26.html            men's basketball table, year "2026" = 2025-26 season (updated 8 Apr 2026)
  mens_basketball_team_pages_2025_2026.json     the "2026" and "2025" rows of each school's men's basketball page
  other_source_pay.csv                          the figure another source gives for the same coach (quoted in the note only)

The "Total Pay" column is used as shown. A figure is used only when the table lists the school's current head coach
and shows a figure; otherwise the pay cell keeps the figure from another source (contract, release or press report),
and the 2025 basketball column is left blank. Current head coaches are read from data/merged_values.csv, so run
merge_research.py, then this script, then merge_research.py again.
Writes data/research/verification_zzzzz_usatoday.csv."""
import re, json, csv, html, unicodedata
ALIAS={'Miami (FL)':'Miami (Fla.)','NC State':'North Carolina State'}
def norm(s): return re.sub(r'[^a-z]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower().replace('(interim)','').replace(' jr.','').replace(' jr',''))
def same(table_name,current):
    a,b=norm(table_name),norm(current)
    if a==b or (a[-5:]==b[-5:] and a[:2]==b[:2]): return True
    parts=[norm(p) for p in current.replace('(interim)','').split()]
    return len(parts)>=2 and all(p in a for p in (parts[0],parts[-1]))      # e.g. Henry Ward "Bucky" McMillan III
def clean(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s or ''))).strip()
M=list(csv.DictReader(open('data/merged_values.csv',encoding='utf-8')))
COACH={(r['school'],r['metric']):r['value'] for r in M if r['metric'] in ('fb_hc_name','mbb_hc_name')}
SCHOOLS=sorted({r['school'] for r in M if r['metric']=='fb_hc_name'})
OTHER={(r['school'],r['metric']):r for r in csv.DictReader(open('data/usatoday/other_source_pay.csv',encoding='utf-8'))}
def nextdata(f):
    raw=open(f,encoding='utf-8',errors='replace').read()
    return json.loads(re.search(r'(?s)<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',raw).group(1))['props']['pageProps']['fallback']
fb=nextdata('data/usatoday/football_coach_2025.html'); assert str(fb['config']['currentSeason'])=='2025'
FB={s['teamName']:s for s in fb['salaries']}
MB=json.load(open('data/usatoday/mens_basketball_team_pages_2025_2026.json'))
FBN="USA Today college football head coach pay table, 2025 season (updated 8 October 2025)"
MBN="USA Today men's basketball head coach pay table, {y} ({s} season; updated 8 April 2026)"
D='2026-11-13'
rows=[['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']]
count={'fb':0,'mbb':0,'mbb_prior':0}
def note(s,label,metric,school):
    coach=f"{s['firstName']} {s['lastName']}"
    parts=f"school pay ${s['schoolPay']:,}"+(f", other pay ${s['otherPay']:,}" if (s.get('otherPay') or 0)>0 else '')
    n=f"USA Today table, {label}: {coach}, total pay ${s['totalPay']:,} ({parts}). Bonuses are listed separately in the table and are not included."
    if clean(s.get('note')): n+=f" Table note: {clean(s['note'])}"
    o=OTHER.get((school,metric))
    if o and metric.endswith('annual_comp') and abs(float(o['value'])-s['totalPay'])>0.5:
        n+=f" Another source gives {float(o['value']):,.0f} for {o['season'] or 'the current season'} ({o['source_name']})."
    return n
for school in SCHOOLS:
    # football, 2025 season
    s=FB.get(school) or FB.get(ALIAS.get(school,school)); cur=COACH[(school,'fb_hc_name')]
    if s and s['totalPay']>0 and same(f"{s['firstName']} {s['lastName']}",cur):
        url=f"https://sportsdata.usatoday.com/ncaa/salaries/football/coach/team/{s['teamID']}"
        rows.append([school,'fb_hc_annual_comp',s['totalPay'],'USD','2025',FBN,url,D,note(s,'2025 season','fb_hc_annual_comp',school)])
        rows.append([school,'fb_hc_pay_source_type','USA Today','text','2025',FBN,url,D,"USA Today's table, compiled from contracts and other records obtained from the schools."]); count['fb']+=1
    # men's basketball: table year 2026 (2025-26 season) and 2025 (2024-25 season)
    hs={h['season']:h for h in MB[school]}; cur=COACH[(school,'mbb_hc_name')]
    for season,label,ss,metric in ((2025,'2026','2025-26','mbb_hc_annual_comp'),(2024,'2025','2024-25','mbb_hc_prior_comp')):
        s=hs.get(season); name=MBN.format(y=label,s=ss)
        ok=bool(s) and s['totalPay']>0 and same(f"{s['firstName']} {s['lastName']}",cur)
        if ok:
            url=f"https://sportsdata.usatoday.com/ncaa/salaries/mens-basketball/coach/team/{s['teamID']}"
            rows.append([school,metric,s['totalPay'],'USD',ss,name,url,D,note(s,f'year {label} ({ss} season)',metric,school)])
            if metric=='mbb_hc_annual_comp':
                rows.append([school,'mbb_hc_pay_source_type','USA Today','text',ss,name,url,D,"USA Today's table, compiled from contracts and other records obtained from the schools."]); count['mbb']+=1
            else: count['mbb_prior']+=1
        elif metric=='mbb_hc_prior_comp':
            why=("USA Today's 2025 row for this school lists "+f"{s['firstName']} {s['lastName']}, not the current head coach." if s and not same(f"{s['firstName']} {s['lastName']}",cur)
                 else "USA Today shows no 2025 figure for this coach.")
            rows.append([school,metric,'--','USD',ss,name,'',D,why])
with open('data/research/verification_zzzzz_usatoday.csv','w',newline='',encoding='utf-8') as fh: csv.writer(fh).writerows(rows)
print('USA Today pay:',count,'| rows',len(rows)-1)
