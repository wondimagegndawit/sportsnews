"""Full NCAA financial report (MFRS) detail for the public schools: every revenue and expense line, by sport.

For each school the workbook carries on an NCAA report, this writes
  data/frs_detail.csv        one row per line item: football, men's basketball, women's basketball, other sports,
                             non-program specific, total
  data/frs_sport_totals.csv  total revenue and total expenses for every individual sport the school reports
Sources: the Sportico College Sports Finances Database files in data/sportico (the fiscal year the workbook uses), and
for the three schools on their own posted report (California, Illinois, Ole Miss) the saved PDFs in data/mfrs.
Each school's lines are checked against its own totals; anything that does not add up is printed."""
import json, glob, csv, re, subprocess, collections
URL='https://www.sportico.com/leagues/college-sports/2023/college-sports-finances-database-intercollegiate-1234646029/'
SP_NAME='Sportico College Sports Finances Database (MFRS compilation)'
# (section, line id, name, prefixes to match in the source, subtotal?)
CANON=[
 ('Revenue','1','Ticket Sales',['ticket sales'],0),('Revenue','2','Direct State or Other Government Support',['direct state'],0),('Revenue','3','Student Fees',['student fees'],0),
 ('Revenue','4','Direct Institutional Support',['direct institutional support'],0),('Revenue','5','Less - Transfers to Institution',['less - transfers','less- transfers','less transfers','less - transfer','transfers to institution'],0),
 ('Revenue','6','Indirect Institutional Support',['indirect institutional support'],0),('Revenue','6A','Indirect Institutional Support - Athletic Facilities Debt Service, Lease and Rental Fees',['indirect institutional support - athletic','indirect institutional support - facilities','indirect insititutional suport - athletic','indirect insititutional support - athletic'],0),
 ('Revenue','7','Guarantees',['guarantees'],0),('Revenue','8','Contributions',['contributions'],0),('Revenue','9','In-Kind',['in-kind','in kind'],0),
 ('Revenue','10','Compensation and Benefits provided by a third party',['compensation and benefits provided'],0),('Revenue','11','Media Rights',['media rights'],0),
 ('Revenue','12','Total NCAA Distributions (12A to 12C)',['total ncaa distributions'],1),('Revenue','12A','NCAA Distributions',['ncaa distributions'],0),('Revenue','12B','NCAA Host Revenue Settlements',['ncaa host revenue'],0),
 ('Revenue','12C','Post-Season Non-Football NCAA Expense Reimbursements',['post-season non-football ncaa expense','post-season non- football ncaa expense','post-season non-football ncaa'],0),
 ('Revenue','13','Conference Distributions (Non Media and Non Post Season)',['conference distributions (non'],0),('Revenue','13A','Conference Distributions of Post-Season Generated Revenue',['conference distributions of','conference distributions (bowl'],0),
 ('Revenue','14','Program, Novelty, Parking and Concession Sales',['program, novelty','program novelty'],0),('Revenue','15','Royalties, Licensing, Advertisement and Sponsorships',['royalties'],0),
 ('Revenue','16','Sports Camp Revenues',['sports camp revenue'],0),('Revenue','17','Athletics Restricted Endowment and Investments Income',['athletics restricted endowment','endowment and investment'],0),
 ('Revenue','18','Other Operating Revenue',['other operating revenue'],0),('Revenue','19','Post-Season Football Expense Reimbursements',['post-season football expense reimbursements','football bowl revenues','bowl revenues','post-season football expense reimb'],0),
 ('Revenue','','Total Operating Revenues',['total operating revenues'],2),
 ('Expense','20','Athletic Student Aid',['athletic student aid'],0),('Expense','21','Guarantees',['guarantees (expenses)','guarantees'],0),
 ('Expense','22','Coaching Salaries, Benefits and Bonuses paid by the University and Related Entities',['coaching salaries, benefits and bonuses paid by the university','coaching salaries'],0),
 ('Expense','23','Coaching Salaries, Benefits and Bonuses paid by a Third Party',['coaching salaries, benefits and bonuses paid by a third','coaching other compensation'],0),
 ('Expense','24','Support Staff/Administrative Compensation, Benefits and Bonuses paid by the University and Related Entities',['support staff/ administrative compensation, benefits and bonuses paid by the university','support staff/administrative compensation, benefits and bonuses paid by the university','support staff/administrative compensation'],0),
 ('Expense','25','Support Staff/Administrative Compensation, Benefits and Bonuses paid by Third Party',['support staff/ administrative compensation, benefits and bonuses paid by third','support staff/administrative compensation, benefits and bonuses paid by third','support staff/administrative other compensation'],0),
 ('Expense','26','Severance Payments',['severance'],0),('Expense','27','Recruiting',['recruiting'],0),('Expense','28','Team Travel',['team travel'],0),('Expense','29','Sports Equipment, Uniforms and Supplies',['sports equipment','equipment, uniforms'],0),
 ('Expense','30','Game Expenses',['game expenses'],0),('Expense','31','Fund Raising, Marketing and Promotion',['fund raising','fundraising'],0),('Expense','32','Sports Camp Expenses',['sports camp expenses'],0),('Expense','33','Spirit Groups',['spirit groups'],0),
 ('Expense','34','Athletic Facilities Debt Service, Leases and Rental Fee',['athletic facilities debt service','athletic facility debt service'],0),('Expense','35','Direct Overhead and Administrative Expenses',['direct overhead'],0),
 ('Expense','35A','Facilities Maintenance and Operations',['facilities maintenance','facilties maintenance'],0),('Expense','36','Indirect Institutional Support',['indirect institutional support (expenses)','indirect institutional support'],0),
 ('Expense','37','Medical Expenses and Insurance',['medical expenses'],0),('Expense','38','Memberships and Dues',['memberships and dues'],0),('Expense','39','Student-Athlete Meals (non-travel)',['student-athlete meals'],0),
 ('Expense','40','Other Operating Expenses',['other operating expenses'],0),
 ('Expense','41','Post-Season Football Expenses',['post-season football expenses','football bowl expenses','bowl expenses','football bowl'],0),
 ('Expense','41A','Post-Season Football Expenses - Coaching Compensation/Bonuses',['bowl expenses - coaching','football bowl expenses - coaching','post-season football expenses - coaching','post-season football expenses – coaching'],0),
 ('Expense','41B','NCAA Football Host Expense Settlements',['ncaa football host'],0),
 ('Expense','42','NCAA Post-Season Non-Football Expenses',['ncaa post-season non-football expenses','ncaa post-season non- football expenses'],0),
 ('Expense','42A','NCAA Post-Season Non-Football Expenses - Coaching Compensation/Bonuses',['ncaa post-season non-football expenses - coaching','ncaa post-season non-football expenses – coaching','ncaa post-season non- football expenses – coaching','ncaa post-season non- football expenses - coaching'],0),
 ('Expense','42B','NCAA Non-Football Host Expense Settlements',['ncaa non-football host'],0),
 ('Expense','43','Enhanced Educational Benefits (Alston or other)',['enhanced educational'],0),('Expense','44','Institutional NIL Revenue Share',['institutional nil'],0),
 ('Expense','50','Excess Transfers to Institution (counted within expenses on the school statement)',['excess transfers to institution'],0),
 ('Expense','','Total Operating Expenses',['total operating expenses'],2),
]
def num(v):
    s=str(v).replace('$','').replace(',','').strip()
    if s in ('','-','–'): return 0
    neg=(s.startswith('(') and s.endswith(')')) or s.startswith('-')
    s=s.strip('()-')
    try: return -int(round(float(s))) if neg else int(round(float(s)))
    except ValueError: return None
def match(items):
    """items: ordered list of (source name, six numbers). Returns {(section, id): six numbers}. Revenue lines come before
    'Total Operating Revenues', expense lines after, which settles names used on both sides (Guarantees, Indirect support)."""
    out={}; section='Revenue'; used=set()
    for name,vals in items:
        n=re.sub(r'\s+',' ',name.strip().lower())
        best=None
        for sec,i,cname,pres,sub in CANON:
            if sec!=section or (sec,i) in used: continue
            for p in pres:
                if n.startswith(p) and (best is None or len(p)>best[1]): best=((sec,i),len(p))
        if best: out[best[0]]=vals; used.add(best[0])
        if n.startswith('total operating revenues'): section='Expense'
    return out
def check(school,d,report):
    for sec,tot in (('Revenue',('Revenue','')),('Expense',('Expense',''))):
        if tot not in d: report.append((school,sec,'no total line')); continue
        for c in range(6):
            s=sum(v[c] for (s_,i),v in d.items() if s_==sec and i!='' and not next(x[4] for x in CANON if (x[0],x[1])==(s_,i)))
            if abs(s-d[tot][c])>2: report.append((school,sec,['FB','MBB','WBB','Other','Non-program','Total'][c],'lines',s,'total',d[tot][c],'diff',s-d[tot][c]))
        for (s_,i),v in d.items():
            if s_==sec and abs(sum(v[:5])-v[5])>2: report.append((school,sec,i,'columns do not add to the line total',sum(v[:5]),v[5]))
# ---- which report the workbook uses for each school
master=json.load(open('data/schools_master.json'))
MV={(r['school'],r['metric']):r for r in csv.DictReader(open('data/merged_values.csv',encoding='utf-8'))}
SPV={(r['school'],r['metric']):r for r in csv.DictReader(open('data/sportico_values.csv',encoding='utf-8'))}
data={}
for f in sorted(glob.glob('data/sportico/json*.json')):
    txt=open(f,encoding='utf-8').read(); txt=txt[txt.index('['):].rstrip().rstrip(';')
    for obj in json.loads(txt):
        if isinstance(obj,dict):
            for k,v in obj.items(): data.setdefault(k,{}).update(v if isinstance(v,dict) else {})
def sp_entry(school,yr):
    note=SPV[(school,'sp_fiscal_year')]['notes']; m=re.search(r"entry '([^']+)'",note)
    return data[m.group(1)][str(yr)]
PDF={'Illinois':('data/mfrs/illinois_fy2025.pdf','six'),'Ole Miss':('data/mfrs/olemiss_fy2025.pdf','six'),'California':('data/mfrs/california_fy2025.pdf','cal')}
MONEY=r'-?\(?\$?-?[\d,]+\)?|-'
def pdf_items(path,kind):
    txt=subprocess.run(['pdftotext','-layout',path,'-'],capture_output=True,text=True).stdout.split('\n')
    if kind=='six':   # NCAA system printout: the by-sport statement is the last 'Statement of Revenues and Expenses' block
        start=min(i for i,l in enumerate(txt) if 'Statement of Revenues and Expenses' in l and any('Non-Program' in x for x in txt[i:i+6])); rows=txt[start:]
        items=[]; pend=None
        for k,l in enumerate(rows):
            m=re.match(r'^\s*(\d+[A-C]?)?\s+(.*?)\s+((?:-?\$[\d,]+\s+){5}-?\$[\d,]+)\s*$',l)
            if m:
                name=m.group(2).strip()
                # item names wrap over the following lines; totals carry no id
                j=k+1; extra=[]
                while j<len(rows) and rows[j].strip() and not re.search(r'\$[\d,]+',rows[j]) and not re.match(r'^\s*(ID\s|NCAA Membership|Reporting Institution)',rows[j]) and not re.match(r'^(Revenues|Expenses)\s*$',rows[j]) and not re.match(r'^\s*\d+[A-C]?\s',rows[j]): extra.append(rows[j].strip()); j+=1
                full=(name+' '+' '.join(extra)).strip()
                byid=[c[2] for c in CANON if m.group(1) and c[1]==m.group(1)]      # the printed line number settles the item
                items.append((byid[0] if byid else full,[num(x) for x in m.group(3).split()]))
        return items
    # Cal's own statement: football, men's basketball, women's basketball, other men's sports, other women's sports,
    # non-program specific, grand total. Cells can be blank, so each figure is placed by where it ends on the line.
    tok=re.compile(r'\(?-?[\d,]*\d\)?|(?<=\s)-(?=\s|$)')
    ref=next(l for l in txt if l.strip().startswith('Total Operating Expenses')); ends=[m.end() for m in tok.finditer(ref)][-7:]
    items=[]; debt=[0]*6
    for l in txt:
        m=re.match(r'^\s*(\d+[A-C]?)?\s*([A-Za-z].*?)(?=\s{2,}[\(\d-])',l)
        if not m: continue
        name=m.group(2).strip(); v=[0]*7; got=0
        for x in tok.finditer(l,m.end()):
            c=min(range(7),key=lambda k:abs(ends[k]-x.end()))
            if abs(ends[c]-x.end())<=6 and num(x.group(0)) is not None: v[c]=num(x.group(0)); got+=1
        if not got: continue
        six=[v[0],v[1],v[2],v[3]+v[4],v[5],v[6]]
        if name.startswith('Athletic Facilities Debt Service'): debt=[a+b for a,b in zip(debt,six)]; continue   # shown below Cal's expense total
        if name.startswith('Transfers to Institution'): name='Excess Transfers to Institution (Cal statement line 40)'
        items.append((name,six))
    # the workbook counts Cal's facilities debt service within operating expenses, as the other schools report it
    items=[(n_,v_) for n_,v_ in items if not n_.startswith(('Capital Projects','Excess (Deficiency)'))]
    k=next(i_ for i_,(n_,v_) in enumerate(items) if n_.startswith('Total Operating Expenses'))
    items[k]=('Total Operating Expenses',[a+b for a,b in zip(items[k][1],debt)]); items.insert(k,('Athletic Facilities Debt Service',debt))
    return items
rows=[]; sport_rows=[]; report=[]; done=[]
for s in master:
    n=s['name']; sp=SPV.get((n,'sp_fiscal_year')); tor=MV.get((n,'total_operating_revenue'))
    own=tor and tor['value'] not in ('--','') and MV.get((n,'fin_fiscal_year')) and MV[(n,'fin_fiscal_year')]['value'] not in ('--','')
    spy=int(sp['value']) if sp and sp['value'] not in ('--','') else None
    if n in PDF and own and (spy is None or int(MV[(n,'fin_fiscal_year')]['value'])>spy):
        path,kind=PDF[n]; items=pdf_items(path,kind); d=match(items); fy=int(MV[(n,'fin_fiscal_year')]['value']); basis='MFRS own posting'
        src=tor['source_name']; url=MV[(n,'fin_report_url')]['value'] if MV.get((n,'fin_report_url')) and MV[(n,'fin_report_url')]['value'] not in ('--','') else tor['source_url']; sports=None
        if kind=='cal':   # Cal reports facilities debt service below its expense total; the workbook counts it within expenses
            pass
    elif spy and spy>=2024:
        e=sp_entry(n,spy); T=e.get('Totals',{}); items=[(k,[num(x) for x in v]) for k,v in T.items() if isinstance(v,list) and len(v)==6]
        d=match(items); fy=spy; basis='Sportico (MFRS compilation)'; src=SP_NAME; url=URL
        sports={k:(num(e.get('Revenues',{}).get(k)),num(e.get('Expenses',{}).get(k))) for k in list(dict.fromkeys(list(e.get('Revenues',{}))+list(e.get('Expenses',{}))))}
    else: continue
    check(n,d,report); done.append((n,fy,basis,len(d)))
    for sec,i,cname,pres,sub in CANON:
        v=d.get((sec,i))
        if v is None: continue
        rows.append([n,s['conf'],fy,basis,sec,i,cname]+v+[src,url])
    if sports:
        for k,(rv,ex) in sports.items(): sport_rows.append([n,s['conf'],fy,k,rv if rv is not None else '--',ex if ex is not None else '--',src,url])
with open('data/frs_detail.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['school','conference','fiscal_year','basis','section','line_id','line_item','football','mens_basketball','womens_basketball','other_sports','non_program','total','source_name','source_url']); w.writerows(rows)
with open('data/frs_sport_totals.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['school','conference','fiscal_year','sport','total_revenue','total_expenses','source_name','source_url']); w.writerows(sport_rows)
print('schools',len(done),'| detail rows',len(rows),'| sport rows',len(sport_rows),'| by basis',collections.Counter((b,f) for _,f,b,_ in done))
print('lines per school',collections.Counter(k for *_,k in done))
print('checks that failed:',len(report))
for r in report[:60]: print('  ',r)
