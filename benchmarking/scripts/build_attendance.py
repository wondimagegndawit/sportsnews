"""Football average home attendance, 2023 to 2025, from the D1.ticker FBS Attendance Trends pages saved unmodified in
data/d1ticker/. Each season is read from that season's own page ("<year> Final Average" column); the prior-year column
on the following season's page is used only as a cross-check and recorded in the note.
Men's basketball average home attendance, 2025-26, from the NCAA Men's Basketball Attendance Records PDF saved unmodified in
data/ncaa_attendance/ (Attend_layout.txt is its `pdftotext -layout` extract). Writes data/attendance_values.csv."""
import csv, html, json, re
DATE='2026-11-10'
URL='https://www.d1ticker.com/{y}-fbs-attendance-trends/'
ALIAS={}   # master name -> D1.ticker name, where they differ
master=json.load(open('data/schools_master.json'))
def table(y):
    t=open(f'data/d1ticker/{y}-fbs-attendance-trends.html',encoding='utf-8',errors='replace').read()
    tb=re.search(r'<table.*?</table>',t,re.S).group(0); rows=[]
    for tr in re.findall(r'<tr.*?</tr>',tb,re.S):
        rows.append([html.unescape(re.sub(r'<[^>]+>','',c)).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>',tr,re.S)])
    hdr=rows[0]; through=re.search(r'Data through Week \d+',t).group(0)
    out={}
    for r in rows[1:]:
        if len(r)!=len(hdr): continue
        d=dict(zip(hdr,r)); d['_star']=r[0].endswith('*'); out[r[0].rstrip('*').strip()]=d
    return hdr,out,through
T={y:table(y) for y in (2023,2024,2025)}
for y in T: assert f'{y} Final Average' in T[y][0], T[y][0]
def n(v): return int(v.replace(',',''))
out=[]; miss=[]; diffs=[]
for s in master:
    name=s['name']; key=ALIAS.get(name,name)
    for y in (2023,2024,2025):
        hdr,rows,through=T[y]; metric=f'fb_avg_attendance_{y}'; src=f'D1.ticker, {y} FBS Attendance Trends'
        d=rows.get(key)
        if not d or not re.fullmatch(r'[\d,]+',d[f'{y} Final Average']):
            miss.append((name,y)); out.append([name,metric,'--','fans per game',f'{y} season',src,URL.format(y=y),DATE,'school not listed on the page']); continue
        v=n(d[f'{y} Final Average'])
        note=f"Column '{y} Final Average' as displayed, row '{d['School']}'; {through.lower()}; the page does not state its underlying data source or whether figures are announced or paid."
        if y<2025:
            nx=T[y+1][1].get(key); col=f'{y} Average'
            if nx and re.fullmatch(r'[\d,]+',nx.get(col,'')):
                w=n(nx[col]); same=(w==v)
                note+=f" Cross-check: the {y+1} page shows {w:,} in its '{col}' column ({'matches' if same else 'differs'})."
                if not same: diffs.append((name,y,v,w))
        if d['_star']:
            note+=(" The page marks this school with an asterisk: stadium under renovation and capacity not the same as 2023." if y==2024 else " The page marks this school with an asterisk and gives no footnote text.")
        out.append([name,metric,v,'fans per game',f'{y} season',src,URL.format(y=y),DATE,note])
        if y==2025:   # every other per-school column on the 2025 page, as displayed on the same row
            u=URL.format(y=y); row=f"row '{d['School']}'"; star=(" The page marks this school with an asterisk and gives no footnote text." if d['_star'] else '')
            def pct(col):
                assert re.fullmatch(r'-?\d+\.\d\d%',d[col]),(name,col,d[col]); return f'{float(d[col][:-1])/100:.4f}'
            out.append([name,'fb_attendance_yoy_change_2025',pct('Year-over-Year % Change'),'change','2025 season vs 2024',src,u,DATE,
                        f"Column 'Year-over-Year % Change' as displayed ({d['Year-over-Year % Change']}), {row}, stored as a decimal; the page compares its '2025 Final Average' ({d['2025 Final Average']}) with its '2024 Average' ({d['2024 Average']})."+star])
            assert re.fullmatch(r'[\d,]+',d['5 Year Average']),(name,d['5 Year Average'])
            out.append([name,'fb_avg_attendance_5yr',n(d['5 Year Average']),'fans per game','five-year average shown on the 2025 page',src,u,DATE,
                        f"Column '5 Year Average' as displayed, {row}; the page does not state which five seasons the figure covers."+star])
            out.append([name,'fb_attendance_change_vs_5yr_2025',pct('5 Year-over-Year % Change'),'change','2025 season vs five-year average',src,u,DATE,
                        f"Column '5 Year-over-Year % Change' as displayed ({d['5 Year-over-Year % Change']}), {row}, stored as a decimal; the page compares its '2025 Final Average' with its '5 Year Average'."+star])
            out.append([name,'fb_attendance_pct_capacity_2025',pct('Capacity %'),'share of capacity','2025 season',src,u,DATE,
                        f"Column 'Capacity %' as displayed ({d['Capacity %']}), {row}, stored as a decimal; D1.ticker does not publish the stadium capacity it divides by, so it can differ from the Stadium capacity column in this workbook."+star])
# ---- men's basketball: NCAA attendance records book, 2026 Attendance Summary, Division I Team-by-Team Attendance ----
MBB_URL='http://fs.ncaa.org.s3.amazonaws.com/Docs/stats/m_basketball_RB/Attend.pdf'
MBB_SRC="NCAA Men's Basketball Attendance Records through 2025-26 (2026 Attendance Summary, Division I Team-by-Team Attendance)"
MBB_ALIAS={'USC':'Southern California'}
MBB_ALIAS.update({x:x.replace(' State',' St.') for x in ('Florida State','Michigan State','Ohio State','Penn State','Arizona State','Iowa State','Kansas State','Oklahoma State','Mississippi State')})
txt=open('data/ncaa_attendance/Attend_layout.txt',encoding='utf-8').read().split('\n')
assert any('THROUGH 2025-26' in l for l in txt[:10])
a=next(i for i,l in enumerate(txt) if l.strip().startswith('DIVISION I ') and 'School' in l); b=next(i for i,l in enumerate(txt) if l.strip().startswith('DIVISION II'))
pat=re.compile(r"(?:(\d+)\.\s+)?([A-Z][A-Za-z.&'()\- ]*?[A-Za-z.)])\s+(\d{1,2})\s+([\d,]{3,})\s+([\d,]+)(?=\s|$)")
teams={}
for l in txt[a:b]:
    for m in pat.finditer(l):
        rank,nm,g,att,avg=m.groups()
        if rank: continue                      # ranked leader tables repeat the same teams
        v=(int(g),n(att),n(avg)); assert teams.get(nm,v)==v,(nm,teams[nm],v); teams[nm]=v
# tie-out: Division I home totals plus the four reclassifying teams, as printed on the summary page
d1=next(l for l in txt if l.startswith('NCAA Division I Home Attendance')).split(); rc=[teams[x] for x in ('West Ga.','New Haven','Le Moyne','Mercyhurst')]
assert len(teams)==n(d1[5])+4 and sum(v[0] for v in teams.values())==n(d1[6])+sum(v[0] for v in rc) and sum(v[1] for v in teams.values())==n(d1[7])+sum(v[1] for v in rc), 'team table does not tie to the Division I home totals'
# leader tables in the same summary (each lists 30 teams): rank by average home attendance (parsed only as a check on
# the team table; the rank is not recorded), all-games attendance
# (home, road, neutral), and largest increase in average from the previous year (which carries the 2024-25 average)
NAME=r"([A-Z][A-Za-z.&'()\- ]*?[A-Za-z.)])"
i_rank=next(i for i,l in enumerate(txt) if l.startswith('Rank School') and 'Average' in l and i>a); i_tbt=next(i for i,l in enumerate(txt) if l.startswith('Division I Team-by-Team Attendance'))
leaders={}
for l in txt[i_rank:i_tbt]:
    m=re.match(r"(\d+)\.\s+"+NAME+r"\s{2,}(\d{1,2})\s+([\d,]+)\s+([\d,]+)(?=\s|$)",l)
    if m: leaders[m.group(2)]=int(m.group(1)); assert teams[m.group(2)]==(int(m.group(3)),n(m.group(4)),n(m.group(5))),l
i_inc=next(i for i,l in enumerate(txt) if l.startswith('Largest Division I Average Attendance')); i_all=next(i for i,l in enumerate(txt) if 'Division I All Games Attendance' in l)
increase={}; allgames={}
for l in txt[i_all:b]:
    m=re.search(r"(\d+)\.\s+"+NAME+r"\s{2,}(\d{2})\s+(\d{3},\d{3})\s*$",l)
    if m: allgames[m.group(2)]=(int(m.group(1)),int(m.group(3)),n(m.group(4)))
for l in txt[i_inc:b]:
    m=re.match(r"(\d+)\.\s+"+NAME+r"\s{2,}([\d,]+)\s+([\d,]+)\s+([\d,]+)(?=\s|$)",l)
    if m:
        prev,cur,chg=n(m.group(3)),n(m.group(4)),n(m.group(5)); assert teams[m.group(2)][2]==cur and cur-prev==chg,l
        increase[m.group(2)]=(int(m.group(1)),prev,chg)
for tbl,rk in ((leaders,lambda v:v),(allgames,lambda v:v[0]),(increase,lambda v:v[0])): assert sorted(rk(v) for v in tbl.values())==list(range(1,31)),sorted(rk(v) for v in tbl.values())
S_LEAD="NCAA Men's Basketball Attendance Records through 2025-26 (2026 Attendance Summary, Division I Team Leaders)"
S_ALLG="NCAA Men's Basketball Attendance Records through 2025-26 (2026 Attendance Summary, Division I All Games Attendance)"
S_INC="NCAA Men's Basketball Attendance Records through 2025-26 (2026 Attendance Summary, Largest Division I Average Attendance Increase From Previous Year)"
TOP30='the NCAA table lists only 30 teams and this school is not among them'
mmiss=[]
for s in master:
    name=s['name']; key=MBB_ALIAS.get(name,name); SEA='2025-26 season'
    def add(metric,val,unit,season,srcname,note): out.append([name,metric,val,unit,season,srcname,MBB_URL,DATE,note])
    if key not in teams:
        mmiss.append(name)
        for metric in ('mbb_home_games_2526','mbb_total_home_attendance_2526','mbb_avg_attendance_2526'): add(metric,'--','',SEA,MBB_SRC,'school not listed in the table')
        continue
    g,att,avg=teams[key]; tie="the team table ties to the summary line 'NCAA Division I Home Attendance' on page 2 of the PDF."
    add('mbb_home_games_2526',g,'games',SEA,MBB_SRC,f"G column as printed, row '{key}'; {tie}")
    add('mbb_total_home_attendance_2526',att,'fans',SEA,MBB_SRC,f"Attendance column as printed, row '{key}'; {tie}")
    add('mbb_avg_attendance_2526',avg,'fans per game',SEA,MBB_SRC,f"Average column as printed, row '{key}': {g} home games, total home attendance {att:,}; {tie}")
    if key in allgames:
        rk,tg,ta=allgames[key]
        add('mbb_all_games_2526',tg,'games',SEA,S_ALLG,f"Total Games column as printed, row '{key}' (rank {rk}); home, road and neutral-site games.")
        add('mbb_all_games_attendance_2526',ta,'fans',SEA,S_ALLG,f"Attendance column as printed, row '{key}' (rank {rk}); home, road and neutral-site games.")
    else:
        for metric,unit in (('mbb_all_games_2526','games'),('mbb_all_games_attendance_2526','fans')): add(metric,'--',unit,SEA,S_ALLG,'Not in the source: '+TOP30+'.')
    if key in increase:
        rk,prev,chg=increase[key]
        add('mbb_avg_attendance_2425',prev,'fans per game','2024-25 season',S_INC,f"'2025 Avg.' column as printed, row '{key}' (rank {rk}).")
        add('mbb_avg_attendance_change_2526',chg,'fans per game','2025-26 vs 2024-25',S_INC,f"'Change in Avg.' column as printed, row '{key}' (rank {rk}); the table shows a 2024-25 average of {prev:,} and a 2025-26 average of {avg:,}.")
    else:
        add('mbb_avg_attendance_2425','--','fans per game','2024-25 season',S_INC,'Not in the source: the 2024-25 average is printed only for the 30 teams with the largest increase, and this school is not among them.')
        add('mbb_avg_attendance_change_2526','--','fans per game','2025-26 vs 2024-25',S_INC,'Not in the source: the change is printed only for the 30 teams with the largest increase, and this school is not among them.')
print('mbb teams parsed',len(teams),'missing',mmiss,'| leader tables',len(leaders),len(allgames),len(increase))
with open('data/attendance_values.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']); w.writerows(out)
print('rows',len(out),'missing',miss); print('cross-check differences',len(diffs))
for d in diffs: print('  DIFF',d)
