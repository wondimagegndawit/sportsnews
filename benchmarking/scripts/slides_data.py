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
def money(v): return f'${v/1e6:.1f}M'
def num(v): return f'{v:,.0f}'
def pct(v): return f'{v*100:.0f}%'
FMT={'usd':money,'num':num,'pct':pct}
def names(rs,n=3): 
    x=[LOGO[school(r)]['short'] for r in rs]
    return ', '.join(x[:-1])+' and '+x[-1] if len(x)>1 else x[0]
def build(key,metric,unit,label,getters,source,second=None):
    """getters: list of (series name, function row->value); the first series ranks the schools and feeds the Power 4 lines."""
    g0=getters[0][1]
    have=[r for r in ROWS if g0(r) is not None]
    inconf=[r for r in have if conf(r)==CONF]
    scope='conference' if len(inconf)>=MIN else 'all'
    rs=sorted(inconf if scope=='conference' else have,key=lambda r:-g0(r))
    p4=[g0(r) for r in have]; avg=statistics.mean(p4); med=statistics.median(p4); f=FMT[unit]
    cats=[dict(school=school(r),short=LOGO[school(r)]['short'],abbr=LOGO[school(r)]['abbr'],conference=conf(r),logo=LOGO[school(r)]['file']) for r in rs]
    series=[dict(name=nm,values=[g(r) for r in rs]) for nm,g in getters]
    return dict(key=key,metric=metric,unit=unit,label=label,scope=scope,conference=CONF,n_conf=len(inconf),n_conf_total=sum(1 for r in ROWS if conf(r)==CONF),n_p4=len(have),
                categories=cats,series=series,lines=[dict(name=f'Power 4 average ({f(avg)})',value=avg),dict(name=f'Power 4 median ({f(med)})',value=med)],
                avg=avg,med=med,source=source,rows=rs,inconf=inconf)
SRC_WB='Source: Power 4 Athletic Department Benchmarking workbook.'
def deal(key,hdr,label):
    s=build(key,hdr,'usd',label,[(label,lambda r:val(r,hdr))],SRC_WB+' Annual value is the reported figure or, where a source gives a total and a term, the total divided by the term.')
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
    return s
slides=[deal('jersey_patch','Jersey patch annual value','Jersey patch annual value'),
        deal('stadium_naming','Stadium naming rights annual value','Stadium naming rights annual value'),
        deal('arena_naming','Arena naming rights annual value','Arena naming rights annual value')]
# football: average home attendance, 2025 against 2024
a25='FB average home attendance 2025'; a24='FB average home attendance 2024'
s=build('fb_attendance',a25,'num','Football average home attendance',[('2025 season',lambda r:val(r,a25)),('2024 season',lambda r:val(r,a24))],
        'Source: D1.ticker FBS Attendance Trends, 2025 and 2024 pages, as carried in the benchmarking workbook.')
rs=s['rows']; up=[r for r in rs if val(r,a24) is not None and val(r,a25)>val(r,a24)]; cavg=statistics.mean(val(r,a25) for r in rs)
s['title']=f"{CONF} football: {len(up)} of {len(rs)} schools drew more fans per home game in 2025 than in 2024"
s['subtitle']=f"The {CONF} averaged {num(cavg)} per game in 2025, against a Power 4 average of {num(s['avg'])} and a median of {num(s['med'])}; {LOGO[school(rs[0])]['short']} led at {num(val(rs[0],a25))}."
slides.append(s)
# football: percent of capacity, 2025 against 2024
p25='FB attendance % of capacity 2025'
s=build('fb_capacity',p25,'pct','Football percent of capacity filled',[('2025 season',lambda r:val(r,p25)),('2024 season',lambda r:PCT24.get(school(r)))],
        'Source: D1.ticker FBS Attendance Trends, Capacity % column of the 2025 and 2024 pages. D1.ticker does not publish the capacity it divides by.')
rs=s['rows']; cavg=statistics.mean(val(r,p25) for r in rs); up=[r for r in rs if PCT24.get(school(r)) is not None and val(r,p25)>PCT24[school(r)]]; full=[r for r in rs if val(r,p25)>=0.95]
s['title']=f"{CONF} football stadiums were {pct(cavg)} full on average in 2025, against a Power 4 average of {pct(s['avg'])}"
s['subtitle']=f"{len(full)} of {len(rs)} {CONF} schools filled at least 95% of capacity; {len(up)} filled a larger share than in 2024. Power 4 median is {pct(s['med'])}."
slides.append(s)
# men's basketball: average home attendance and percent of capacity, 2025-26
m26='MBB average home attendance 2025-26'
s=build('mbb_attendance',m26,'num',"Men's basketball average home attendance",[('2025-26 season',lambda r:val(r,m26))],
        "Source: NCAA Men's Basketball Attendance Records book, 2026 Attendance Summary (home games, 2025-26). The book does not list 2024-25 for every school, so one season is shown.")
rs=s['rows']; cavg=statistics.mean(val(r,m26) for r in rs); above=[r for r in rs if val(r,m26)>s['med']]
s['title']=f"{CONF} men's basketball averaged {num(cavg)} fans per home game in 2025-26, against a Power 4 average of {num(s['avg'])}"
s['subtitle']=f"{len(above)} of {len(rs)} {CONF} schools were above the Power 4 median of {num(s['med'])}; {LOGO[school(rs[0])]['short']} led at {num(val(rs[0],m26))}."
slides.append(s)
mp='MBB attendance % of capacity 2025-26'
s=build('mbb_capacity',mp,'pct',"Men's basketball percent of capacity filled",[('2025-26 season',lambda r:val(r,mp))],
        "Source: average home attendance (NCAA Attendance Records book, 2025-26) divided by arena capacity, as calculated in the benchmarking workbook.")
rs=s['rows']; cavg=statistics.mean(val(r,mp) for r in rs); missing=[school(r) for r in ROWS if conf(r)==CONF and val(r,mp) is None]
s['title']=f"{CONF} men's basketball arenas were {pct(cavg)} full on average in 2025-26, against a Power 4 average of {pct(s['avg'])}"
s['subtitle']=f"{LOGO[school(rs[0])]['short']} filled the largest share at {pct(val(rs[0],mp))}; Power 4 median is {pct(s['med'])}."+(f" Not shown, no arena capacity in the workbook: {', '.join(missing)}." if missing and s['scope']=='conference' else '')
slides.append(s)
for s in slides: s.pop('rows'); s.pop('inconf')
json.dump(dict(conference=CONF,slides=slides,logos=[dict(school=k,short=v['short'],file=v['file']) for k,v in sorted(LOGO.items())]),sys.stdout,indent=1)
