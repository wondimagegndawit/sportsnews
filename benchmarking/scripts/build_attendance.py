"""Football average home attendance, 2023 to 2025, from the D1.ticker FBS Attendance Trends pages saved unmodified in
data/d1ticker/. Each season is read from that season's own page ("<year> Final Average" column); the prior-year column
on the following season's page is used only as a cross-check and recorded in the note. Writes data/attendance_values.csv."""
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
with open('data/attendance_values.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['school','metric','value','unit','fiscal_year_or_season','source_name','source_url','date_accessed','notes']); w.writerows(out)
print('rows',len(out),'missing',miss); print('cross-check differences',len(diffs))
for d in diffs: print('  DIFF',d)
