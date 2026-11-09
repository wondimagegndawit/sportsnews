"""Build the Power 4 athletic department benchmarking workbook from data/merged_values.csv."""
import csv, json, re
from collections import defaultdict
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation

OUT='Power4_Athletic_Department_Benchmarking.xlsx'
DATE='2026-11-09'
master=json.load(open('data/schools_master.json'))
CONFS=[('ACC','02 - ACC'),('Big Ten','03 - Big Ten'),('Big 12','04 - Big 12'),('SEC','05 - SEC')]
CONF_URL={'ACC':'https://theacc.com/','Big Ten':'https://bigten.org/','Big 12':'https://big12sports.com/','SEC':'https://www.secsports.com/'}
by_conf={c:sorted([s for s in master if s['conf']==c],key=lambda s:s['name'].lower()) for c,_ in CONFS}
order=[s for c,_ in CONFS for s in by_conf[c]]
V=defaultdict(dict)   # V[school][metric] = row
for r in csv.DictReader(open('data/merged_values.csv',encoding='utf-8')): V[r['school']][r['metric']]=r

# ---------- styles ----------
AR=lambda **k: Font(name='Arial',size=10,**k)
F_BLUE=AR(color='0000FF',underline='single'); F_BLUE_PLAIN=AR(color='0000FF'); F_GREEN=AR(color='008000'); F_BLACK=AR(color='000000')
F_WHITE_B=AR(color='FFFFFF',bold=True); F_BOLD=AR(bold=True); F_BLACK_B=AR(color='000000',bold=True)
FILL_NAVY=PatternFill('solid',fgColor='1F3864'); FILL_LB=PatternFill('solid',fgColor='DDEBF7'); FILL_GRAY=PatternFill('solid',fgColor='D9D9D9'); FILL_YEL=PatternFill('solid',fgColor='FFFF00')
THIN=Side(style='thin',color='000000'); B_BOTTOM=Border(bottom=THIN); B_TOP=Border(top=THIN)
FMT={'usd':'$#,##0;($#,##0);-','pct':'0.0%','cnt':'#,##0','wp':'0.000','yr':'0','pts':'#,##0.00','idx':'0'}

# ---------- metric spec: (section, header, key, kind, fmt, agg) ----------
# kind: text | num | formula
S=[]
def M(sec,hdr,key,kind,fmt=None,agg=False): S.append(dict(sec=sec,hdr=hdr,key=key,kind=kind,fmt=fmt,agg=agg))
M('Identity','School','school','text'); M('Identity','Conference','conference','text'); M('Identity','Public or Private','control','text'); M('Identity','State','state','text'); M('Identity','Flagship (Y/N)','flagship','text')
M('Financial','Fiscal year','fin_fiscal_year','num','yr'); M('Financial','Financial source basis','fin_basis','text')
M('Financial','Total operating revenue','total_operating_revenue','num','usd',True); M('Financial','Total operating expenses','total_operating_expenses','num','usd',True)
M('Financial','Operating surplus (deficit)','f_surplus','formula','usd',True)
M('Financial','Media rights revenue','media_rights_revenue','num','usd',True); M('Financial','Ticket sales revenue','ticket_sales_revenue','num','usd',True); M('Financial','Contributions revenue','contributions_revenue','num','usd',True)
M('Financial','NCAA and conference distributions','ncaa_conf_distributions','num','usd',True)
M('Financial','Direct institutional support','direct_institutional_support','num','usd',True); M('Financial','Indirect institutional support','indirect_institutional_support','num','usd',True); M('Financial','Student fees','student_fees','num','usd',True)
M('Financial','Total subsidy','f_subsidy','formula','usd',True); M('Financial','Subsidy as % of revenue','f_subsidy_pct','formula','pct',True)
M('Financial','Total coaching salaries and benefits','coaching_salaries','num','usd',True); M('Financial','Total athletics-related debt outstanding','athletics_related_debt','num','usd',True); M('Financial','Annual debt service','debt_service','num','usd',True)
M('Coaching','Head football coach','fb_hc_name','text'); M('Coaching','FB HC annual guaranteed compensation','fb_hc_annual_comp','num','usd',True); M('Coaching','FB HC contract end year','fb_hc_contract_end','num','yr'); M('Coaching','FB HC pay source type','fb_hc_pay_source_type','text')
M('Coaching','Head men\'s basketball coach','mbb_hc_name','text'); M('Coaching','MBB HC annual guaranteed compensation','mbb_hc_annual_comp','num','usd',True); M('Coaching','MBB HC contract end year','mbb_hc_contract_end','num','yr'); M('Coaching','MBB HC pay source type','mbb_hc_pay_source_type','text')
M('Venues','Football stadium','stadium_name','text'); M('Venues','Stadium capacity','stadium_capacity','num','cnt',True); M('Venues','Stadium year opened','stadium_year_opened','num','yr',True); M('Venues','Stadium last major renovation year','stadium_last_renovation_year','num','yr',True)
M('Venues','Men\'s basketball arena','arena_name','text'); M('Venues','Arena capacity','arena_capacity','num','cnt',True); M('Venues','Arena year opened','arena_year_opened','num','yr',True)
for pre,lab in [('stadium_nr','Stadium naming rights'),('arena_nr','Arena naming rights')]:
    M(lab,f'{lab} partner',f'{pre}_partner','text'); M(lab,f'{lab} industry',f'{pre}_industry','text'); M(lab,f'{lab} deal type',f'{pre}_deal_type','text')
    M(lab,f'{lab} start year',f'{pre}_start_year','num','yr'); M(lab,f'{lab} term (years)',f'{pre}_term_years','num','cnt',True); M(lab,f'{lab} annual value',f'{pre}_annual_value','num','usd',True); M(lab,f'{lab} total value',f'{pre}_total_value','num','usd',True); M(lab,f'{lab} expires',f'f_{pre}_expires','formula','yr')
M('Football jersey or helmet patch','Jersey patch partner','patch_partner','text'); M('Football jersey or helmet patch','Jersey patch industry','patch_industry','text'); M('Football jersey or helmet patch','Jersey patch start year','patch_start_year','num','yr'); M('Football jersey or helmet patch','Jersey patch term (years)','patch_term_years','num','cnt',True); M('Football jersey or helmet patch','Jersey patch annual value','patch_annual_value','num','usd',True); M('Football jersey or helmet patch','Jersey patch total value','patch_total_value','num','usd',True); M('Football jersey or helmet patch','Jersey patch expires','f_patch_expires','formula','yr')
M('Multimedia rights','MMR partner','mmr_partner','text'); M('Multimedia rights','MMR start year','mmr_start_year','num','yr'); M('Multimedia rights','MMR term (years)','mmr_term_years','num','cnt',True); M('Multimedia rights','MMR annual value','mmr_annual_value','num','usd',True); M('Multimedia rights','MMR total value','mmr_total_value','num','usd',True); M('Multimedia rights','MMR expires','f_mmr_expires','formula','yr')
M('Apparel','Apparel partner','apparel_partner','text'); M('Apparel','Apparel start year','apparel_start_year','num','yr'); M('Apparel','Apparel term (years)','apparel_term_years','num','cnt',True); M('Apparel','Apparel annual value','apparel_annual_value','num','usd',True); M('Apparel','Apparel total value','apparel_total_value','num','usd',True); M('Apparel','Apparel expires','f_apparel_expires','formula','yr')
M('Institutional','Undergraduate enrollment','undergrad_enrollment','num','cnt',True); M('Institutional','Total enrollment','total_enrollment','num','cnt',True); M('Institutional','Enrollment year','enrollment_year','text'); M('Institutional','Varsity sports sponsored','varsity_sports','num','cnt',True)
M('Performance','FB wins 2021-25','fb_wins_2021_25','num','cnt',True); M('Performance','FB losses 2021-25','fb_losses_2021_25','num','cnt',True); M('Performance','FB win % 2021-25','f_fb_winpct','formula','wp',True)
M('Performance','MBB wins 2021-22 to 2025-26','mbb_wins_2122_2526','num','cnt',True); M('Performance','MBB losses 2021-22 to 2025-26','mbb_losses_2122_2526','num','cnt',True); M('Performance','MBB win % 2021-22 to 2025-26','f_mbb_winpct','formula','wp',True)
M('Performance','Directors\' Cup rank 2024-25','dcup_rank_2425','num','cnt',True); M('Performance','Directors\' Cup points 2024-25','dcup_points_2425','num','pts',True); M('Performance','Directors\' Cup rank 2025-26','dcup_rank_2526','num','cnt',True); M('Performance','Directors\' Cup points 2025-26','dcup_points_2526','num','pts',True)
M('Academic','FB multi-year APR','fb_apr_multiyear','num','idx',True); M('Academic','Department GSR (%)','dept_gsr','num','idx',True); M('Academic','FB GSR (%)','fb_gsr','num','idx',True); M('Academic','Academic data year','academic_data_year','text')
COL={m['key']:i+1 for i,m in enumerate(S)}; NC=len(S); LAST=L(NC)
assert len({m['hdr'] for m in S})==NC

# ---------- per-school value resolution ----------
def num(v):
    try:
        f=float(v); return int(f) if f==int(f) and '.' not in str(v) else f
    except: return None
def get(school,key):
    r=V[school].get(key); 
    if not r: return None
    return r
sourcelog=[]
def logrow(s,metric_hdr,value,unit,fy,stype,sname,url,note):
    sourcelog.append([s['name'],s['conf'],metric_hdr,value,unit,fy,stype,sname,url,DATE,note])
def stype_of(r):
    u=(r.get('source_url') or '').lower(); n=(r.get('source_name') or '').lower(); f=r.get('_file','')
    if 'knightnewhouse' in u: return 'Knight-Newhouse'
    if 'ope.ed.gov' in u or 'eada' in n: return 'EADA'
    if 'ncaa.org' in u: return 'NCAA'
    if 'nces.ed.gov' in u or 'ipeds' in n: return 'IPEDS'
    if 'nacda.com' in u: return 'other'
    if 'sports-reference' in u or 'espn.com' in u: return 'other'
    if 'sportsbusinessjournal' in u: return 'SBJ'
    if 'mfrs' in n or 'agreed' in n or 'aup' in n or 'ncaa financial' in n or 'membership financial' in n: return 'MFRS own posting'
    if 'contract' in n or 'contract' in u or 'salar' in n or 'checkbook' in u or 'transparent' in u: return 'contract'
    if 'release' in n or 'announc' in n or re.search(r'(sports|athletics)\.|\.edu',u) and 'news' in u: return 'press release'
    return 'other'
resolved={}   # resolved[school][key] = (value, url, logged?) ; value None -> '--'
for s in order:
    n=s['name']; R={}
    def put(key,val,url,unit,fy,stype,sname,note,log=True):
        R[key]=(val,url)
        if log: logrow(s,next(m['hdr'] for m in S if m['key']==key),val if val is not None else '--',unit,fy,stype,sname,url if val is not None else '--',note)
    nav=f"https://nces.ed.gov/collegenavigator/?id={s['unitid']}"
    put('school',n,nav,'text','','IPEDS','IPEDS College Navigator',nav,f"UNITID {s['unitid']}; {s['ipeds_name']}")
    put('conference',s['conf'],CONF_URL[s['conf']],'text','2026-27','other','Conference official site',CONF_URL[s['conf']],'Membership as of the 2026-27 academic year')
    for key in ('control','state','flagship'):
        r=get(n,key); put(key,r['value'],r['source_url'],r['unit'],r['fiscal_year_or_season'],stype_of(r),r['source_name'],r['notes'])
    # financial
    tor=get(n,'total_operating_revenue')
    if tor and tor['value']!='--':
        fyr=get(n,'fin_fiscal_year'); fy=num(fyr['value']) if fyr and fyr['value']!='--' else num(re.sub(r'\D','',tor['fiscal_year_or_season'])[:4])
        rep=get(n,'fin_report_url'); repurl=rep['value'] if rep and rep['value'] not in ('--','') else tor['source_url']
        put('fin_fiscal_year',fy,repurl,'year',f'FY{fy}','MFRS own posting',tor['source_name'],'Fiscal year of the school-posted NCAA MFRS/AUP report')
        put('fin_basis','MFRS own posting',repurl,'text',f'FY{fy}','MFRS own posting',tor['source_name'],'School-posted NCAA Membership Financial Reporting System / agreed-upon procedures report')
        for key in ('total_operating_revenue','total_operating_expenses','media_rights_revenue','ticket_sales_revenue','contributions_revenue','direct_institutional_support','indirect_institutional_support','student_fees','coaching_salaries','athletics_related_debt','debt_service'):
            r=get(n,key)
            if r and r['value']!='--': put(key,num(r['value']),r['source_url'],'USD',f'FY{fy}','MFRS own posting',r['source_name'],r['notes'])
            else: put(key,None,'','USD',f'FY{fy}','MFRS own posting',tor['source_name'],(r['notes'] if r else 'line not reported'))
        parts=[]; tot=0; ok=True; notes=[]
        for key,lab in (('ncaa_distributions','line 12 NCAA distributions'),('conference_distributions','line 13 conference distributions'),('conference_bowl_distributions','line 13A conference bowl distributions')):
            r=get(n,key)
            if r and r['value']!='--': tot+=num(r['value']); parts.append(f"{lab} {num(r['value']):,}"); notes.append(r['notes'])
            elif key!='conference_bowl_distributions': ok=False
        put('ncaa_conf_distributions',tot if ok else None,tor['source_url'] if ok else '','USD',f'FY{fy}','MFRS own posting',tor['source_name'],('Sum of '+'; '.join(parts)+'. '+' '.join(x for x in notes if x)) if ok else 'NCAA or conference distribution line not reported')
    else:
        er=get(n,'eada_total_revenue'); ee=get(n,'eada_total_expense')
        why=(tor['notes'] if tor else ('private school; NCAA MFRS report not public' if s['control']=='Private' else 'no school-posted MFRS report located'))
        put('fin_fiscal_year',2025,er['source_url'],'year','FY2025','EADA',er['source_name'],'EADA 2024-25 reporting year (institution fiscal year ending in 2025); '+why)
        put('fin_basis','EADA',er['source_url'],'text','FY2025','EADA',er['source_name'],'EADA basis: U.S. Dept. of Education Equity in Athletics data; revenue and expense definitions differ from NCAA MFRS. '+why)
        put('total_operating_revenue',num(er['value']),er['source_url'],'USD','FY2025','EADA',er['source_name'],er['notes'])
        put('total_operating_expenses',num(ee['value']),ee['source_url'],'USD','FY2025','EADA',ee['source_name'],ee['notes'])
        for key in ('media_rights_revenue','ticket_sales_revenue','contributions_revenue','ncaa_conf_distributions','direct_institutional_support','indirect_institutional_support','student_fees','coaching_salaries','athletics_related_debt','debt_service'):
            put(key,None,'','USD','FY2025','EADA','EADA 2024-25','EADA basis; this MFRS line item is not reported in EADA. '+why)
    # everything else straight from merged rows
    for m in S:
        key=m['key']
        if key in R or m['kind']=='formula': continue
        r=get(n,key)
        if key.endswith('_pay_source_type') and (not r or r['value']=='--'):
            comp=get(n,key.replace('_pay_source_type','_annual_comp'))
            if comp and comp['value']!='--':
                u=comp['source_url'].lower(); txt=(comp['source_name']+' '+comp['notes']).lower()
                if re.search(r'(contract|agreement|term sheet|offer sheet|mou|public records|records request|salary database|checkbook)',u+' '+txt): st='contract'
                elif re.search(r'(sports|athletics)\.|\.edu',u): st='school announcement'
                else: st='press report'
                put(key,st,comp['source_url'],'text',comp['fiscal_year_or_season'],{'contract':'contract','school announcement':'press release','press report':'other'}[st],comp['source_name'],'Pay source type classified from the compensation row source: '+comp['source_name'])
                continue
        if not r: put(key,None,'','','','other','','not researched (web-search budget exhausted)'); continue
        if r['value']=='--': put(key,None,'',r['unit'],r['fiscal_year_or_season'],stype_of(r),r['source_name'],r['notes'] or 'not sourced'); continue
        val=num(r['value']) if m['kind']=='num' else r['value']
        if key.endswith('_pay_source_type'): st={'contract':'contract','school announcement':'press release','state salary database':'contract','press report':'other'}[val]
        else: st=stype_of(r)
        put(key,val,r['source_url'],r['unit'],r['fiscal_year_or_season'],st,r['source_name'],r['notes'])
    resolved[n]=R

# ---------- workbook ----------
wb=openpyxl.Workbook(); wb.remove(wb.active)
def prep(ws,ncols,title):
    ws.sheet_view.showGridLines=False
    for c in range(1,ncols+1):
        cell=ws.cell(row=1,column=c); cell.fill=FILL_NAVY; cell.font=F_WHITE_B
    ws['A1']=title
def setw(ws,widths):
    for c,w in widths.items(): ws.column_dimensions[L(c)].width=min(max(w,8),70)
def write_text(cell,val,font,fmt=None):
    cell.value=val; cell.font=font
    if fmt: cell.number_format=FMT[fmt]

# conference tabs
conf_rows={}   # name -> (sheetname, row)
conf_layout={}
for conf,sname in CONFS:
    ws=wb.create_sheet(sname); ss=by_conf[conf]; n=len(ss)
    prep(ws,NC,f'Power 4 athletic department benchmarking: {conf}')
    for i,m in enumerate(S,1):
        c=ws.cell(row=2,column=i,value=m['hdr']); c.font=F_BOLD; c.fill=FILL_LB; c.border=B_BOTTOM
    r0=3; avg_row=r0+n; med_row=avg_row+1
    conf_layout[conf]=dict(sheet=sname,first=r0,last=r0+n-1,avg=avg_row,med=med_row)
    for j,s in enumerate(ss):
        r=r0+j; conf_rows[s['name']]=(sname,r); R=resolved[s['name']]
        def A(key): return f"{L(COL[key])}{r}"
        for i,m in enumerate(S,1):
            cell=ws.cell(row=r,column=i); key=m['key']
            if m['kind']=='formula':
                if key=='f_surplus': f=f'=IF(AND(ISNUMBER({A("total_operating_revenue")}),ISNUMBER({A("total_operating_expenses")})),{A("total_operating_revenue")}-{A("total_operating_expenses")},"--")'
                elif key=='f_subsidy': f=f'=IF(AND(ISNUMBER({A("direct_institutional_support")}),ISNUMBER({A("student_fees")})),{A("direct_institutional_support")}+{A("student_fees")}+IF(ISNUMBER({A("indirect_institutional_support")}),{A("indirect_institutional_support")},0),"--")'
                elif key=='f_subsidy_pct': f=f'=IF(AND(ISNUMBER({A("f_subsidy")}),ISNUMBER({A("total_operating_revenue")})),{A("f_subsidy")}/{A("total_operating_revenue")},"--")'
                elif key=='f_fb_winpct': f=f'=IF(AND(ISNUMBER({A("fb_wins_2021_25")}),ISNUMBER({A("fb_losses_2021_25")})),{A("fb_wins_2021_25")}/({A("fb_wins_2021_25")}+{A("fb_losses_2021_25")}),"--")'
                elif key=='f_mbb_winpct': f=f'=IF(AND(ISNUMBER({A("mbb_wins_2122_2526")}),ISNUMBER({A("mbb_losses_2122_2526")})),{A("mbb_wins_2122_2526")}/({A("mbb_wins_2122_2526")}+{A("mbb_losses_2122_2526")}),"--")'
                elif key.endswith('_expires'):
                    pre=key[2:-8]; f=f'=IF(AND(ISNUMBER({A(pre+"_start_year")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_start_year")}+{A(pre+"_term_years")},"--")'
                write_text(cell,f,F_BLACK,m['fmt']); continue
            val,url=R[key]
            if val is None: write_text(cell,'--',F_BLUE_PLAIN,m['fmt'])
            else:
                write_text(cell,val,F_BLUE,m['fmt'])
                if url: cell.hyperlink=url; cell.font=F_BLUE
        # deal triplets: derive the third when two are reported
        for pre in ('stadium_nr','arena_nr','patch','mmr','apparel'):
            a,t,tot=R[pre+'_annual_value'][0],R[pre+'_term_years'][0],R[pre+'_total_value'][0]
            ca,ct,ctot=ws[A(pre+'_annual_value')],ws[A(pre+'_term_years')],ws[A(pre+'_total_value')]
            if a is not None and t is not None and tot is not None:
                write_text(ctot,f'=IF(AND(ISNUMBER({A(pre+"_annual_value")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_annual_value")}*{A(pre+"_term_years")},"--")',F_BLACK,'usd'); ctot.hyperlink=None
                for row in sourcelog:
                    if row[0]==s['name'] and row[2]==next(mm['hdr'] for mm in S if mm['key']==pre+'_total_value'): row[10]=f'Reported total {tot:,}; cell shows Annual x Term per the deal-value rule. '+row[10]
            elif a is not None and t is not None and tot is None: write_text(ctot,f'=IF(AND(ISNUMBER({A(pre+"_annual_value")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_annual_value")}*{A(pre+"_term_years")},"--")',F_BLACK,'usd'); ctot.hyperlink=None
            elif tot is not None and t is not None and a is None: write_text(ca,f'=IF(AND(ISNUMBER({A(pre+"_total_value")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_total_value")}/{A(pre+"_term_years")},"--")',F_BLACK,'usd'); ca.hyperlink=None
            elif a is not None and tot is not None and t is None: write_text(ct,f'=IF(AND(ISNUMBER({A(pre+"_total_value")}),ISNUMBER({A(pre+"_annual_value")})),{A(pre+"_total_value")}/{A(pre+"_annual_value")},"--")',F_BLACK,'cnt'); ct.hyperlink=None
    for rr,lab,fn in ((avg_row,'Average','AVERAGE'),(med_row,'Median','MEDIAN')):
        for i,m in enumerate(S,1):
            cell=ws.cell(row=rr,column=i); cell.fill=FILL_GRAY; cell.font=F_BLACK_B
            if rr==avg_row: cell.border=B_TOP
            if i==1: cell.value=lab; continue
            if m['agg']: cell.value=f'=IFERROR({fn}({L(i)}{r0}:{L(i)}{r0+n-1}),"--")'; cell.number_format=FMT[m['fmt']]
            else: cell.value='--'
    widths={i:max(len(m['hdr']),max((len(str(resolved[s['name']][m['key']][0] or '--')) for s in ss),default=0) if m['kind']!='formula' else 14)+2 for i,m in enumerate(S,1)}
    widths[1]=max(widths[1],18); setw(ws,widths)

# 01 - All Schools
ws=wb.create_sheet('01 - All Schools',0)
prep(ws,NC,'Power 4 athletic department benchmarking: all 67 schools')
for i,m in enumerate(S,1):
    c=ws.cell(row=2,column=i,value=m['hdr']); c.font=F_BOLD; c.fill=FILL_LB; c.border=B_BOTTOM
all_first=3; all_last=3+len(order)-1
for j,s in enumerate(order):
    sname,sr=conf_rows[s['name']]; r=all_first+j
    for i,m in enumerate(S,1):
        cell=ws.cell(row=r,column=i,value=f"='{sname}'!{L(i)}{sr}"); cell.font=F_GREEN
        if m['fmt']: cell.number_format=FMT[m['fmt']]
r=all_last+2
blockrows=[]
for conf,sname in CONFS:
    blockrows.append((r,'Average',conf)); r+=1
for conf,sname in CONFS:
    blockrows.append((r,'Median',conf)); r+=1
blockrows.append((r,'Average','All schools')); blockrows.append((r+1,'Median','All schools'))
for rr,lab,conf in blockrows:
    for i,m in enumerate(S,1):
        cell=ws.cell(row=rr,column=i); cell.fill=FILL_GRAY; cell.font=F_BLACK_B
        if i==1: cell.value=lab; continue
        if i==2: cell.value=conf; continue
        if not m['agg']: cell.value='--'; continue
        col=L(i); cell.number_format=FMT[m['fmt']]
        if conf=='All schools': cell.value=f'=IFERROR({"AVERAGE" if lab=="Average" else "MEDIAN"}({col}{all_first}:{col}{all_last}),"--")'
        elif lab=='Average': cell.value=f'=IFERROR(AVERAGEIF($B${all_first}:$B${all_last},$B{rr},{col}{all_first}:{col}{all_last}),"--")'
        else:
            lay=conf_layout[conf]; cell.value=f"='{lay['sheet']}'!{col}{lay['med']}"; cell.font=AR(color='008000',bold=True)
for i in range(1,NC+1): ws.cell(row=blockrows[0][0],column=i).border=B_TOP
setw(ws,{i:max(len(m['hdr']),14)+2 for i,m in enumerate(S,1)}); ws.column_dimensions['A'].width=20

# 00 - Read Me
ws=wb.create_sheet('00 - Read Me',0); prep(ws,2,'Power 4 athletic department benchmarking: read me')
lines=[
 'Coverage: all 67 Power 4 athletic departments (ACC 17, Big Ten 18, Big 12 16, SEC 16); one row per school on the conference tabs, which hold every hardcoded value.',
 'Structure: 01 links every conference-tab cell; 06 is the audit trail (values); 07 looks up any school; tabs 08 onward are one per school, all formulas.',
 'Source hierarchy for financials: school-posted NCAA MFRS or agreed-upon procedures report first (FY2025 where posted), otherwise the federal EADA file (2024-25 reporting year).',
 'Knight-Newhouse was not reachable from the build environment, so no school uses that basis; the Financial source basis column states MFRS own posting or EADA for each school.',
 'MFRS vs. EADA caveat: EADA revenue and expense definitions differ from NCAA MFRS, and EADA reports no line-item detail, so media rights, ticketing, contributions, subsidy and debt lines are "--" on EADA-basis rows.',
 'Other sources: NCAA APR and GSR search tools (2024-25 release), IPEDS fall 2024 headcount, ESPN standings (football 2021-25) and Sports-Reference (men\'s basketball 2021-22 to 2025-26), NACDA Directors\' Cup final standings (2024-25 and 2025-26), school and partner releases and trade press for venues and commercial deals.',
 'Conventions: blue cells are hardcodes hyperlinked to their source, black cells are formulas, green cells are cross-tab links, yellow is the input cell on 07; "--" means not publicly sourced, with the reason in 06 - Source Log.',
 'No newspaper-compiled finance or coaching-salary databases are used anywhere in this workbook. Date accessed for all sources: 2026-11-09.',
]
for k,t in enumerate(lines): ws.cell(row=3+k,column=1,value=t).font=F_BLACK
ws.column_dimensions['A'].width=200

# 06 - Source Log
ws=wb.create_sheet('06 - Source Log')
hdr=['School','Conference','Metric','Value','Unit','Fiscal year or season','Source type','Source name','URL','Date accessed','Note']
prep(ws,len(hdr),'Source log: one row per sourced value (values, not formulas)')
for i,h in enumerate(hdr,1):
    c=ws.cell(row=2,column=i,value=h); c.font=F_BOLD; c.fill=FILL_LB; c.border=B_BOTTOM
for j,row in enumerate(sourcelog):
    for i,v in enumerate(row,1):
        c=ws.cell(row=3+j,column=i,value=(v if v not in (None,'') else '--')); c.font=F_BLACK
setw(ws,{1:20,2:10,3:36,4:18,5:10,6:26,7:18,8:40,9:60,10:13,11:80})

# 07 - School Lookup and school tabs
def vertical_sheet(ws,title,name_cell_value,name_font,src_sheet,first,last,avg_row,with_avg):
    ncols=4 if with_avg else 2
    prep(ws,ncols,title)
    ws['A3']='School'; ws['A3'].font=F_BOLD
    ws['B3']=name_cell_value; ws['B3'].font=name_font
    hdrs=['Metric','Value']+(['Conference average','Difference'] if with_avg else [])
    for i,h in enumerate(hdrs,1):
        c=ws.cell(row=5,column=i,value=h); c.font=F_BOLD; c.fill=FILL_LB; c.border=B_BOTTOM
    r=6; sec=None
    rng=f"'{src_sheet}'!$A${first}:${LAST}${last}"; hdrrng=f"'{src_sheet}'!$A$2:${LAST}$2"; namerng=f"'{src_sheet}'!$A${first}:$A${last}"
    for m in S:
        if m['sec']!=sec:
            sec=m['sec']
            for i in range(1,ncols+1):
                c=ws.cell(row=r,column=i); c.fill=FILL_LB; c.font=F_BOLD
            ws.cell(row=r,column=1).value=sec; r+=1
        ws.cell(row=r,column=1,value=m['hdr']).font=F_BLACK
        c=ws.cell(row=r,column=2,value=f'=INDEX({rng},MATCH($B$3,{namerng},0),MATCH($A{r},{hdrrng},0))'); c.font=F_GREEN
        if m['fmt']: c.number_format=FMT[m['fmt']]
        if with_avg:
            avgrng=f"'{src_sheet}'!$A${avg_row}:${LAST}${avg_row}"
            c2=ws.cell(row=r,column=3,value=f'=IF(ISNUMBER(B{r}),INDEX({avgrng},1,MATCH($A{r},{hdrrng},0)),"--")'); c2.font=F_GREEN
            c3=ws.cell(row=r,column=4,value=f'=IF(AND(ISNUMBER(B{r}),ISNUMBER(C{r})),B{r}-C{r},"--")'); c3.font=F_BLACK
            if m['fmt']: c2.number_format=FMT[m['fmt']]; c3.number_format=FMT[m['fmt']]
        r+=1
    setw(ws,{1:40,2:44,3:22,4:22})
ws=wb.create_sheet('07 - School Lookup')
vertical_sheet(ws,'School lookup: choose a school in the yellow cell','Alabama',AR(color='0000FF'),'01 - All Schools',all_first,all_last,None,False)
ws['B3'].fill=FILL_YEL
dv=DataValidation(type='list',formula1=f"='01 - All Schools'!$A${all_first}:$A${all_last}",allow_blank=False); ws.add_data_validation(dv); dv.add('B3')
for k,s in enumerate(order,8):
    sname,sr=conf_rows[s['name']]; conf=s['conf']; lay=conf_layout[conf]
    ws=wb.create_sheet(f"{k:02d} - {s['name']}")
    vertical_sheet(ws,f"School profile: {s['name']}",f"='{sname}'!A{sr}",F_GREEN,sname,lay['first'],lay['last'],lay['avg'],True)
# sheet order: 00,01,02..05,06,07,08..
names=['00 - Read Me','01 - All Schools']+[sn for _,sn in CONFS]+['06 - Source Log','07 - School Lookup']+[f"{k:02d} - {s['name']}" for k,s in enumerate(order,8)]
wb._sheets=[wb[n] for n in names]
for ws in wb: ws.sheet_view.showGridLines=False
wb.save(OUT); print('saved',OUT,'sheets',len(wb.sheetnames),'sourcelog rows',len(sourcelog))
json.dump(dict(S=S,conf_layout=conf_layout,all_first=all_first,all_last=all_last),open('data/workbook_layout.json','w'))
