"""Tie-out of the 2025 football attendance averages used in the workbook (D1.ticker, 2025 FBS Attendance Trends)
against the NCAA Football Attendance Records book (2025 Attendance, All FBS Schools), saved unmodified in
data/ncaa_attendance/Football_Attend.pdf with Football_Attend_layout.txt as its `pdftotext -layout` extract.
Writes data/fb_attendance_reconciliation.csv. Changes nothing in the workbook."""
import csv, json, re
n=lambda v:int(v.replace(',',''))
txt=[l.lstrip('\f') for l in open('data/ncaa_attendance/Football_Attend_layout.txt',encoding='utf-8').read().split('\n')]
a=next(i for i,l in enumerate(txt) if l.startswith('2025 ATTENDANCE')); p2=next(i for i,l in enumerate(txt) if i>a and l.startswith('2025 Attendance'))
end=next(i for i,l in enumerate(txt) if i>p2 and l.startswith('#Reclassifying team.'))
ENT=r"#?([A-Z][A-Za-z.&'()\- ]*?[A-Za-z.)])\s{2,}(\d{1,2})\s+([\d,]{5,})\s+([\d,]{4,})(?=\s|$)"
teams={}
def take(m):
    name=re.split(r'\s{2,}',m.group(1))[-1]      # drop any column heading that shares the line
    v=(int(m.group(2)),n(m.group(3)),n(m.group(4))); assert teams.get(name,v)==v; teams[name]=v
for l in txt[a:p2]:                      # first page: leaders (ranked, skipped) and the list in two columns
    left=re.match(ENT,l)                 # left column: unranked list entry at the start of the line
    if left: take(left)
    right=re.search(r"\s{2,}"+ENT+r"\s*$",l) or (re.match(r"\s{20,}"+ENT+r"\s*$",l))   # right column: entry at the end of the line
    if right and (not left or right.start()>left.end()-1) and not re.match(r"\d+\s",l[:right.start()].strip()[-4:] if False else 'x'):
        # ranked leader rows sit in the left column and start with a number; an entry reached through one is the right column
        take(right)
for l in txt[p2:end]:                    # second page: the list continues in the left column only
    m=re.match(ENT,l)
    if m: take(m)
# the first row of the right-hand column is broken across lines by the page header
i=next(i for i,l in enumerate(txt[a:p2],a) if l.strip()=='Fla. Atlantic'); nums=[x.strip() for x in txt[i+1:i+7] if re.fullmatch(r'\s*[\d,]+\s*',x)]
teams['Fla. Atlantic']=(int(nums[0]),n(nums[1]),n(nums[2]))
tot=next(l for l in txt if l.startswith('Home Attendance, Division I-FBS')).split()
G,A=sum(v[0] for v in teams.values()),sum(v[1] for v in teams.values())
assert len(teams)==n(tot[4]) and all(abs(v[1]/v[0]-v[2])<1 for v in teams.values())
print(f"NCAA FBS table parsed: {len(teams)} teams (printed {tot[4]}), {G} games (printed {tot[5]}), {A:,} total (printed {tot[6]}); residual {n(tot[5])-G} game(s), {n(tot[6])-A:,}")
ALIAS={'USC':'Southern California'}; ALIAS.update({x:x.replace(' State',' St.') for x in ('Florida State','Michigan State','Ohio State','Penn State','Arizona State','Iowa State','Kansas State','Oklahoma State','Mississippi State')})
d1={r['school']:int(r['value']) for r in csv.DictReader(open('data/attendance_values.csv')) if r['metric']=='fb_avg_attendance_2025'}
master=json.load(open('data/schools_master.json')); wb=set(json.load(open('data/workbook_layout.json'))['excluded'])
rows=[]
for s in master:
    g,att,avg=teams[ALIAS.get(s['name'],s['name'])]; d=d1[s['name']]
    rows.append([s['name'],s['conf'],'no' if s['name'] in wb else 'yes',d,avg,d-avg,g,att,'ties' if d==avg else 'differs'])
with open('data/fb_attendance_reconciliation.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['school','conference','in_workbook','d1ticker_2025_final_average','ncaa_2025_average','difference','ncaa_home_games','ncaa_total_home_attendance','result']); w.writerows(rows)
inwb=[r for r in rows if r[2]=='yes']
print('workbook schools:',len(inwb),'| tie exactly',sum(r[8]=='ties' for r in inwb),'| differ',sum(r[8]=='differs' for r in inwb))
for r in sorted([r for r in inwb if r[8]=='differs'],key=lambda r:-abs(r[5])): print(f"  {r[0]:18s} D1.ticker {r[3]:>7,}  NCAA {r[4]:>7,}  diff {r[5]:>+7,}  NCAA games {r[6]}  total {r[7]:,}")
ex=[r for r in rows if r[2]=='no']; print('excluded schools:',len(ex),'| tie',sum(r[8]=='ties' for r in ex),'| differ',[(r[0],r[3],r[4]) for r in ex if r[8]=='differs'])
