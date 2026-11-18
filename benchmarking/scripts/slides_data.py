"""Build the chart data for the benchmarking slides, for one conference.
Usage: python3 -I scripts/slides_data.py "Big 12" > slides/spec_big12.json   (then: node scripts/build_slides.js spec out.pptx)

Rule (analyst's direction): a chart shows the conference's schools when at least 10 of them have a value; otherwise it
shows every Power 4 school with a value. Every chart carries the average and the median across all Power 4 schools
with a value. Figures come from the All Schools tab of the recalculated workbook; the 2024 football percent of
capacity is read from the saved D1.ticker 2024 page, which the workbook does not carry."""
import sys, json, re, html, statistics, openpyxl
CONF=sys.argv[1] if len(sys.argv)>1 else 'Big 12'; MIN=10
wb=openpyxl.load_workbook('Power4_Athletic_Department_Benchmarking.xlsx',data_only=True)
ws=wb['All Schools']; H={ws.cell(6,c).value:c for c in range(3,ws.max_column+1)}
LOGO=json.load(open('slides/logos/logos.json'))
ROWS=[r for r in range(7,ws.max_row+1) if ws.cell(r,H['Conference']).value in ('ACC','Big Ten','Big 12','SEC','Independent') and ws.cell(r,3).value in LOGO]
def val(r,h):
    v=ws.cell(r,H[h]).value
    return v if isinstance(v,(int,float)) and not isinstance(v,bool) else None
def school(r): return ws.cell(r,3).value
def conf(r): return ws.cell(r,H['Conference']).value
def d1ticker_pct(year):
    t=open(f'data/d1ticker/{year}-fbs-attendance-trends.html',encoding='utf-8',errors='replace').read()
    tb=re.search(r'<table.*?</table>',t,re.S).group(0); out={}; hdr=None
    for tr in re.findall(r'<tr.*?</tr>',tb,re.S):
        c=[html.unescape(re.sub(r'<[^>]+>','',x)).strip() for x in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>',tr,re.S)]
        if hdr is None: hdr=c; continue
        if len(c)==len(hdr):
            d=dict(zip(hdr,c)); p=d['Capacity %'].rstrip('%')
            if re.fullmatch(r'[\d.]+',p): out[c[0].rstrip('*').strip()]=float(p)/100
    return out
PCT24=d1ticker_pct(2024)
def money(v): return ('-' if v<0 else '')+f'${abs(v)/1e6:.1f}M'
def num(v): return f'{v:,.0f}'
def pct(v): return f'{v*100:.0f}%'
FMT={'usd':money,'num':num,'pct':pct}
def names(rs,n=3): 
    x=[LOGO[school(r)]['short'] for r in rs]
    return ', '.join(x[:-1])+' and '+x[-1] if len(x)>1 else x[0]
def build(key,metric,unit,label,getters,source,second=None,only=None):
    """getters: list of (series name, function row->value); the first series ranks the schools.
    only: predicate that limits which schools are eligible at all (for example, fiscal 2025 NCAA-report schools).
    A page that shows the conference's schools carries the conference average and median of the schools shown (all
    seasons shown, where there are two); a page that shows every Power 4 school with a value carries the Power 4 lines."""
    g0=getters[0][1]
    have=[r for r in ROWS if g0(r) is not None and (only is None or only(r))]
    inconf=[r for r in have if conf(r)==CONF]
    scope='conference' if len(inconf)>=MIN else 'all'
    rs=sorted(inconf if scope=='conference' else have,key=lambda r:-g0(r))
    p4=[g0(r) for r in have]; avg=statistics.mean(p4); med=statistics.median(p4); f=FMT[unit]
    cats=[dict(school=school(r),short=LOGO[school(r)]['short'],abbr=LOGO[school(r)]['abbr'],conference=conf(r),logo=LOGO[school(r)]['file']) for r in rs]
    series=[dict(name=nm,values=[g(r) for r in rs]) for nm,g in getters]
    shown=[v for x in series for v in x['values'] if v is not None]; cavg=statistics.mean(shown); cmed=statistics.median(shown)
    both=', both seasons' if len(getters)>1 else ''
    lines=([dict(name=f'{CONF} average{both} ({f(cavg)})',value=cavg),dict(name=f'{CONF} median{both} ({f(cmed)})',value=cmed)] if scope=='conference'
           else [dict(name=f'Power 4 average ({f(avg)})',value=avg),dict(name=f'Power 4 median ({f(med)})',value=med)])
    return dict(key=key,metric=metric,unit=unit,label=label,scope=scope,conference=CONF,n_conf=len(inconf),n_conf_total=sum(1 for r in ROWS if conf(r)==CONF),n_p4=len(have),
                categories=cats,series=series,lines=lines,avg=avg,med=med,cavg=cavg,cmed=cmed,source=source,rows=rs,inconf=inconf)
SRC_WB='Source: Power 4 Athletic Department Benchmarking workbook.'
def deal(key,hdr,label):
    s=build(key,hdr,'usd',label,[(label,lambda r:val(r,hdr))],SRC_WB+' Annual value is the reported figure or, where a source gives a total and a term, the total divided by the term.')
    novalue=[]
    if key=='jersey_patch' and any(school(r)=='Notre Dame' for r in s['rows']): s['source']+=' Notre Dame is shown at the low end of a reported range of $18 million to $20 million a year.'
    f=money; rs=s['rows']; top=rs[0]
    who=f"the {CONF} schools" if s['scope']=='conference' else 'all Power 4 schools with a reported value'
    noun=label.replace(' annual value','')+(' deals' if 'patch' in label else '')
    s['title']=f"{noun}: {s['n_p4']} Power 4 schools have a reported annual value, averaging {f(s['avg'])} with a median of {f(s['med'])}"
    if s['scope']=='all':
        inn=s['inconf']
        tail=(f"{len(inn)} of the {s['n_p4']} are in the {CONF} ({names(inn)})" if inn else f"no {CONF} school has a reported value")
        s['source']+=f" All Power 4 schools with a value are shown because fewer than {MIN} {CONF} schools have one."
        s['subtitle']=f"{LOGO[school(top)]['short']} is highest at {f(val(top,hdr))}; {tail}."
    else:
        s['subtitle']=f"{LOGO[school(top)]['short']} is highest in the {CONF} at {f(val(top,hdr))}; {s['n_conf']} of {s['n_conf_total']} {CONF} schools have a reported value."
    if novalue: s['subtitle']+=f" {len(novalue)} more field deals have no reported value ({names(novalue)})."
    return s
slides=[deal('jersey_patch','Jersey patch annual value','Jersey patch annual value'),
        deal('stadium_naming','Stadium naming rights annual value','Stadium naming rights annual value'),
        deal('arena_naming','Arena naming rights annual value','Arena naming rights annual value')]
# playing surface: field naming rights, court naming rights and logo-only deals, each on its own page
def surface(key,label,picks,note):
    """picks: list of (column prefix, sport, rights type). Only deals with a value are charted; the rest are named in the source line."""
    items=[(r,sport,val(r,hdr+' annual value')) for hdr,sport,kind in picks for r in ROWS if ws.cell(r,H[hdr.split()[0]+' rights type']).value==kind]
    have=sorted((x for x in items if x[2] is not None),key=lambda x:(x[1]!='Football',-x[2])); none=[x for x in items if x[2] is None]
    vals=[x[2] for x in have]; avg=statistics.mean(vals); med=statistics.median(vals); inn=[x for x in have if conf(x[0])==CONF]
    cats=[dict(school=school(r),short=LOGO[school(r)]['short'],abbr=LOGO[school(r)]['abbr'],conference=conf(r),logo=LOGO[school(r)]['file'],sport=sport) for r,sport,_ in have]
    return dict(key=key,metric=label,unit='usd',label=label,scope='all',conference=CONF,n_conf=len(inn),n_conf_total=sum(1 for r in ROWS if conf(r)==CONF),n_p4=len(have),
        categories=cats,series=[dict(name=label,values=vals)],lines=[dict(name=f'Power 4 average ({money(avg)})',value=avg),dict(name=f'Power 4 median ({money(med)})',value=med)],avg=avg,med=med,rows=[],inconf=[],
        source=SRC_WB+' '+note+(f" {len(none)} more {'deal has' if len(none)==1 else 'deals have'} no reported value ({', '.join(LOGO[school(x[0])]['short'] for x in none)})." if none else ''),
        title=f"{label.replace(' annual value','')}: {len(have)} Power 4 {'school has' if len(have)==1 else 'schools have'} a reported annual value, averaging {money(avg)} with a median of {money(med)}",
        subtitle=f"{LOGO[school(have[0][0])]['short']} is highest at {money(have[0][2])}; "+(f"{len(inn)} of the {len(have)} {'is' if len(inn)==1 else 'are'} in the {CONF} ({', '.join(LOGO[school(x[0])]['short'] for x in inn)})." if inn else f"no {CONF} school has a reported value."))
slides.insert(2,surface('field_naming','Field naming rights annual value',[('Field naming rights','Football','Naming rights')],'These deals name the football field only; the stadium keeps its own name and is not counted under stadium naming rights.'))
slides.insert(4,surface('court_naming','Court naming rights annual value',[('Court naming rights','Basketball','Naming rights')],'These deals name the basketball court only; the arena keeps its own name and is not counted under arena naming rights.'))
slides.insert(5,surface('logo_deals','Playing surface logo deals annual value',[('Field naming rights','Football','Logo only'),('Court naming rights','Basketball','Logo only')],'These are paid logos on the field or court, which keeps its own name. Duke, Oregon and North Carolina share one $34 million, four-year Edward Jones agreement, split evenly here because each school\'s share is not known.'))
# football: average home attendance, 2025 against 2024
a25='FB average home attendance 2025'; a24='FB average home attendance 2024'
s=build('fb_attendance',a25,'num','Football average home attendance',[('2025 season',lambda r:val(r,a25)),('2024 season',lambda r:val(r,a24))],
        'Source: D1.ticker FBS Attendance Trends, 2025 and 2024 pages, as carried in the benchmarking workbook.')
rs=s['rows']; up=[r for r in rs if val(r,a24) is not None and val(r,a25)>val(r,a24)]
s['title']=f"{CONF} football: {len(up)} of {len(rs)} schools drew more fans per home game in 2025 than in 2024"
s['subtitle']=f"Across the two seasons the {CONF} averaged {num(s['cavg'])} per game, with a median of {num(s['cmed'])}; {LOGO[school(rs[0])]['short']} led in 2025 at {num(val(rs[0],a25))}. The Power 4 average in 2025 was {num(s['avg'])}."
slides.append(s)
# football: percent of capacity, 2025 against 2024
p25='FB attendance % of capacity 2025'
s=build('fb_capacity',p25,'pct','Football percent of capacity filled',[('2025 season',lambda r:val(r,p25)),('2024 season',lambda r:PCT24.get(school(r)))],
        'Source: D1.ticker FBS Attendance Trends, Capacity % column of the 2025 and 2024 pages. D1.ticker does not publish the capacity it divides by.')
rs=s['rows']; full=[r for r in rs if val(r,p25)>=0.95]
s['title']=f"{CONF} football stadiums were {pct(s['cavg'])} full on average across 2025 and 2024, with a median of {pct(s['cmed'])}"
s['subtitle']=f"{len(full)} of {len(rs)} {CONF} schools filled at least 95% of capacity in 2025; {LOGO[school(rs[0])]['short']} filled the largest share at {pct(val(rs[0],p25))}. The Power 4 average in 2025 was {pct(s['avg'])}."
slides.append(s)
# men's basketball: average home attendance and percent of capacity, 2025-26
m26='MBB average home attendance 2025-26'
s=build('mbb_attendance',m26,'num',"Men's basketball average home attendance",[('2025-26 season',lambda r:val(r,m26))],
        "Source: NCAA Men's Basketball Attendance Records book, 2026 Attendance Summary (home games, 2025-26). The book does not list 2024-25 for every school, so one season is shown.")
rs=s['rows']
s['title']=f"{CONF} men's basketball averaged {num(s['cavg'])} fans per home game in 2025-26, with a median of {num(s['cmed'])}"
s['subtitle']=f"{LOGO[school(rs[0])]['short']} led at {num(val(rs[0],m26))} and {LOGO[school(rs[-1])]['short']} drew the fewest at {num(val(rs[-1],m26))}. The Power 4 average was {num(s['avg'])}."
slides.append(s)
mp='MBB attendance % of capacity 2025-26'
s=build('mbb_capacity',mp,'pct',"Men's basketball percent of capacity filled",[('2025-26 season',lambda r:val(r,mp))],
        "Source: average home attendance (NCAA Attendance Records book, 2025-26) divided by arena capacity, as calculated in the benchmarking workbook.")
rs=s['rows']
s['title']=f"{CONF} men's basketball arenas were {pct(s['cavg'])} full on average in 2025-26, with a median of {pct(s['cmed'])}"
s['subtitle']=f"{LOGO[school(rs[0])]['short']} filled the largest share at {pct(val(rs[0],mp))} and {LOGO[school(rs[-1])]['short']} the smallest at {pct(val(rs[-1],mp))}. The Power 4 average was {pct(s['avg'])}."
slides.append(s)
# ---- expenses: what the department spends, where the money goes, and what the head coaches are paid
# Financial pages show only schools that file the NCAA report and are on fiscal 2025 (analyst's direction, 18 Nov 2026).
def dtype(r): return ws.cell(r,H['Financial data type']).value
def fy(r): return ws.cell(r,H['Fiscal year']).value
frs25=lambda r: dtype(r)=='MFRS' and fy(r)==2025
OUT=[LOGO[school(r)]['short'] for r in ROWS if conf(r)==CONF and not frs25(r)]
MF="Source: NCAA Membership Financial Reporting System (MFRS) reports for fiscal 2025, as compiled by Sportico or posted by the school, in the benchmarking workbook."
def scope_note(s): return f" Shown: the {len(s['rows'])} {CONF} schools that file the NCAA report and are on fiscal 2025"+(f"; not shown: {', '.join(OUT)}" if OUT else '')+f". The Power 4 figure covers {s['n_p4']} schools on the same basis."
def finance(key,hdr,label):
    s=build(key,hdr,'usd',label,[(label,lambda r:val(r,hdr))],MF,only=frs25); s['section']='expense'; s['source']=MF+scope_note(s)
    return s
ex='Total operating expenses'
s=finance('total_expenses',ex,'Total operating expenses'); rs=s['rows']
s['title']=f"{CONF} departments spent {money(s['cavg'])} on average in fiscal 2025, with a median of {money(s['cmed'])}"
s['subtitle']=f"{LOGO[school(rs[0])]['short']} spent the most at {money(val(rs[0],ex))} and {LOGO[school(rs[-1])]['short']} the least at {money(val(rs[-1],ex))}. The Power 4 average is {money(s['avg'])}."
slides.append(s)
sp='Operating surplus (deficit)'
s=finance('surplus',sp,'Operating surplus (deficit)'); rs=s['rows']; neg=[r for r in rs if val(r,sp)<0]
s['source']=MF+' Operating revenue less operating expenses.'+scope_note(s)
s['title']=f"{len(neg)} of {len(rs)} {CONF} departments spent more than they took in in fiscal 2025"
s['subtitle']=f"{LOGO[school(rs[0])]['short']} had the largest surplus at {money(val(rs[0],sp))} and {LOGO[school(rs[-1])]['short']} the largest deficit at {money(val(rs[-1],sp))}; the {CONF} median is {money(s['cmed'])}. The Power 4 average is {money(s['avg'])}."
slides.append(s)
cs='Total coaching salaries and benefits'
s=finance('coaching_salaries',cs,'Total coaching salaries and benefits'); rs=s['rows']; share=statistics.mean(val(r,cs)/val(r,ex) for r in rs if val(r,ex))
s['title']=f"{CONF} departments pay coaches {money(s['cavg'])} a year on average, with a median of {money(s['cmed'])}"
s['subtitle']=f"{LOGO[school(rs[0])]['short']} is highest at {money(val(rs[0],cs))} and {LOGO[school(rs[-1])]['short']} lowest at {money(val(rs[-1],cs))}; coaching pay is {pct(share)} of the average {CONF} budget. The Power 4 average is {money(s['avg'])}."
s['source']=MF+' Line 22: salaries, benefits and bonuses for all coaches, paid by the university and related entities.'+scope_note(s); slides.append(s)
ds='Annual debt service'
s=finance('debt_service',ds,'Annual debt service'); rs=s['rows']; big=[r for r in rs if val(r,ds)>=10e6]
s['title']=f"{CONF} departments pay {money(s['cavg'])} a year in debt service on average, with a median of {money(s['cmed'])}"
s['subtitle']=f"{len(big)} of {len(rs)} pay $10M or more a year; {LOGO[school(rs[0])]['short']} is highest at {money(val(rs[0],ds))}. The Power 4 average is {money(s['avg'])}."
s['source']=MF+' Line 34: debt service on athletics facilities (principal and interest), leases and rental fees.'+scope_note(s); slides.append(s)
def missing(rs,hdr): return [LOGO[school(r)]['short'] for r in ROWS if conf(r)==CONF and val(r,hdr) is None]
for key,hdr,sport,season in (('fb_hc_pay','FB HC total pay','football','2025 season'),('mbb_hc_pay','MBB HC total pay 2026',"men's basketball",'2025-26 season')):
    s=build(key,hdr,'usd',f"{sport.capitalize()} head coach total pay",[(f"{sport.capitalize()} head coach total pay",lambda r,h=hdr:val(r,h))],
            "Source: USA Today coaches' pay tables (Total Pay: school pay plus pay from other sources, before bonuses), "+season+"; contracts, school releases or press reports where USA Today has no figure for the current coach. Benchmarking workbook.")
    rs=s['rows']; miss=missing(rs,hdr)
    s['title']=f"{CONF} {sport} head coaches are paid {money(s['cavg'])} on average, with a median of {money(s['cmed'])}"
    s['subtitle']=f"{LOGO[school(rs[0])]['short']} is highest at {money(val(rs[0],hdr))} and {LOGO[school(rs[-1])]['short']} lowest at {money(val(rs[-1],hdr))}. The Power 4 average is {money(s['avg'])}."
    if miss: s['source']+=f" Not shown, no current pay figure: {', '.join(miss)}."
    s['section']='expense'; slides.append(s)
# expense lines from the NCAA report: one page each
def line_item(key,hdr,noun,what,extra=''):
    s=finance(key,hdr,hdr); rs=s['rows']; share=statistics.mean(val(r,hdr)/val(r,ex) for r in rs if val(r,ex))
    s['title']=f"{CONF} departments spend {money(s['cavg'])} a year on {noun} on average, with a median of {money(s['cmed'])}"
    s['subtitle']=f"{LOGO[school(rs[0])]['short']} is highest at {money(val(rs[0],hdr))} and {LOGO[school(rs[-1])]['short']} lowest at {money(val(rs[-1],hdr))}; the line is {share*100:.1f}% of the average {CONF} budget. The Power 4 average is {money(s['avg'])}."
    s['source']=MF+' '+what+extra+scope_note(s)
    slides.append(s)
line_item('support_staff_pay','Support and administrative staff pay','support and administrative staff','Line 24: compensation, benefits and bonuses for non-coaching staff paid by the university and related entities.')
line_item('team_travel','Team travel','team travel','Line 28: air and ground travel, lodging and meals for the preseason and regular season, all sports; post-season travel is reported on other lines.')
for key,hdr,noun in (('team_travel_fb','Team travel: football','football team travel'),('team_travel_mbb',"Team travel: men's basketball","men's basketball team travel"),('team_travel_wbb',"Team travel: women's basketball","women's basketball team travel")):
    line_item(key,hdr,noun,'Line 28, the '+hdr.split(': ')[1]+' column: regular-season travel, lodging and meals; post-season travel is reported on other lines.')
line_item('fundraising_marketing','Fundraising, marketing and promotion','fundraising, marketing and promotion','Line 31: costs of fundraising, marketing and promotion.',' Schools classify these costs differently (some include their foundation or outsourced marketing), so the line varies widely.')
line_item('student_meals','Student-athlete meals','student-athlete meals','Line 39: meal allowances and food provided to student-athletes, other than meals during team travel.')
# keep the expense pages in a reading order: the totals, then pay, travel, other lines, debt, head coaches
ORDER=['total_expenses','surplus','coaching_salaries','support_staff_pay','team_travel','team_travel_fb','team_travel_mbb','team_travel_wbb','fundraising_marketing','student_meals','debt_service','fb_hc_pay','mbb_hc_pay']
slides=[s for s in slides if s.get('section')!='expense']+sorted((s for s in slides if s.get('section')=='expense'),key=lambda s:ORDER.index(s['key']))
for s in slides: s.pop('rows'); s.pop('inconf')
json.dump(dict(conference=CONF,slides=slides,logos=[dict(school=k,short=v['short'],file=v['file']) for k,v in sorted(LOGO.items())]),sys.stdout,indent=1)
