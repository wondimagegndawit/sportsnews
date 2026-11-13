"""Head coach pay from USA Today's coaches' pay tables, for cells no other source fills.
Pages saved in data/usatoday/ (football: 2025 season, updated 8 Oct 2025; men's basketball: 2025-26 season, updated
8 Apr 2026). These are the latest editions and are one season behind the rest of the coaching columns, so the season
is recorded on every row. A figure is used only when (a) the table's coach is the school's current head coach,
(b) the school is public (private-school and Pittsburgh figures come from tax filings about two years old), and
(c) the table's note does not say the figure includes a retention, stay, relocation or other one-time payment.
Writes data/research/verification_zzzzz_usatoday.csv. Run before merge_research.py."""
import re, json, csv, html
FILL={'fb':['Oregon','Wisconsin','Georgia','Mississippi State','South Carolina','Texas'],
      'mbb':['California','Virginia Tech','Maryland','Rutgers','Washington','Wisconsin','Colorado','Houston','Oklahoma State','Texas Tech',
             'West Virginia','Auburn','Mississippi State','Missouri','Ole Miss','Georgia','Kentucky']}
SRC={'fb':('data/usatoday/football_coach_2025.html','football','2025',"USA Today college football head coach pay table (2025 season; updated 8 October 2025)"),
     'mbb':('data/usatoday/mens_basketball_coach_2025-26.html','mens-basketball','2025-26',"USA Today men's basketball head coach pay table (2025-26 season; updated 8 April 2026)")}
rows=[['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']]
for sp,(f,slug,season,name) in SRC.items():
    raw=open(f,encoding='utf-8',errors='replace').read()
    d=json.loads(re.search(r'(?s)<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',raw).group(1))['props']['pageProps']['fallback']
    assert str(d['config']['currentSeason'])=='2025'
    by={s['teamName']:s for s in d['salaries']}
    for school in FILL[sp]:
        s=by[school]; assert s['totalPay']>0,(school,s['totalPay'])
        coach=f"{s['firstName']} {s['lastName']}"; note=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s['note'] or ''))).strip()
        assert not re.search(r'retention|stay benefit|relocation|one-time|tax record',note,re.I),(school,note)
        url=f"https://sportsdata.usatoday.com/ncaa/salaries/{slug}/coach/team/{s['teamID']}"
        parts=f"school pay ${s['schoolPay']:,}"+(f" and other pay ${s['otherPay']:,}" if s['otherPay'] and s['otherPay']>0 else '')
        n=f"Table lists {coach}, total pay ${s['totalPay']:,} ({parts}), for the {season} season, one season earlier than the other pay figures. Bonuses are listed separately in the table and are not included."+(f" Table note: {note}" if note else '')
        rows.append([school,f'{sp}_hc_annual_comp',s['totalPay'],'USD',season,name,url,'2026-11-13',n])
        rows.append([school,f'{sp}_hc_pay_source_type','press report','text',season,name,url,'2026-11-13','Compiled by USA Today from contracts and other documents obtained from the schools.'])
with open('data/research/verification_zzzzz_usatoday.csv','w',newline='',encoding='utf-8') as fh: csv.writer(fh).writerows(rows)
print('USA Today rows',len(rows)-1)
