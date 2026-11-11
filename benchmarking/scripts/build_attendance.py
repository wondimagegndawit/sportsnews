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
        if y==2025:   # percent of capacity as reported on the same row of the 2025 page
            pc=d['Capacity %']; assert re.fullmatch(r'\d+\.\d\d%',pc),(name,pc)
            out.append([name,'fb_attendance_pct_capacity_2025',f'{float(pc[:-1])/100:.4f}','share of capacity','2025 season',src,URL.format(y=y),DATE,
                        f"Column 'Capacity %' as displayed ({pc}), row '{d['School']}', stored as a decimal; D1.ticker does not publish the stadium capacity it divides by, so it can differ from the Stadium capacity column in this workbook."+(" The page marks this school with an asterisk and gives no footnote text." if d['_star'] else '')])
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
mmiss=[]
for s in master:
    name=s['name']; key=MBB_ALIAS.get(name,name); metric='mbb_avg_attendance_2526'
    if key not in teams: mmiss.append(name); out.append([name,metric,'--','fans per game','2025-26 season',MBB_SRC,MBB_URL,DATE,'school not listed in the table']); continue
    g,att,avg=teams[key]
    out.append([name,metric,avg,'fans per game','2025-26 season',MBB_SRC,MBB_URL,DATE,f"Average column as printed, row '{key}': {g} home games, total home attendance {att:,}; the team table ties to the summary line 'NCAA Division I Home Attendance' on page 2 of the PDF."])
print('mbb teams parsed',len(teams),'missing',mmiss)
with open('data/attendance_values.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']); w.writerows(out)
print('rows',len(out),'missing',miss); print('cross-check differences',len(diffs))
for d in diffs: print('  DIFF',d)
