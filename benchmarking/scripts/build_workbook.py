"""Build the Power 4 athletic department benchmarking workbook from data/merged_values.csv."""
import csv, json, re
from collections import defaultdict
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.worksheet.formula import ArrayFormula

OUT='Power4_Athletic_Department_Benchmarking.xlsx'
DATE='2026-11-09'
master=json.load(open('data/schools_master.json'))
CONFS=[('ACC','ACC'),('Big Ten','Big Ten'),('Big 12','Big 12'),('SEC','SEC'),('Independent','Independent')]   # (conference, tab name); tab names carry no number prefix
CONF_URL={'ACC':'https://theacc.com/','Big Ten':'https://bigten.org/','Big 12':'https://big12sports.com/','SEC':'https://www.secsports.com/','Independent':'https://www.d1ticker.com/2025-fbs-attendance-trends/'}
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
M('Identity','School','school','text'); M('Identity','Conference','conference','text'); M('Identity','Public or Private','control','text'); M('Identity','State','state','text')
M('Financial','Fiscal year','fin_fiscal_year','num','yr'); M('Financial','Financial source basis','fin_basis','text'); M('Financial','Financial data type','f_fin_data_type','formula')   # MFRS or EADA, from the basis
M('Financial','Total operating revenue','total_operating_revenue','num','usd',True)
M('Financial','Football revenue','fb_revenue','num','usd',True); M('Financial','Men\'s basketball revenue','mbb_revenue','num','usd',True); M('Financial','Other sports revenue','f_other_sports_revenue','formula','usd',True); M('Financial','Non-program-specific revenue','nonprogram_revenue','num','usd',True)
M('Financial','Total operating expenses','total_operating_expenses','num','usd',True)
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
# attendance: every per-school figure in the two sources. Leader-table columns (top 30 only) carry no average or median.
A_='Attendance'
for _y in (2023,2024,2025): M(A_,f'FB average home attendance {_y}',f'fb_avg_attendance_{_y}','num','cnt',True)
M(A_,'FB attendance year-over-year change 2025','fb_attendance_yoy_change_2025','num','pct',True)
M(A_,'FB 5-year average home attendance','fb_avg_attendance_5yr','num','cnt',True); M(A_,'FB attendance change vs 5-year average 2025','fb_attendance_change_vs_5yr_2025','num','pct',True)
M(A_,'FB attendance % of capacity 2025','fb_attendance_pct_capacity_2025','num','pct',True)
M(A_,'MBB home games 2025-26','mbb_home_games_2526','num','cnt',True); M(A_,'MBB total home attendance 2025-26','mbb_total_home_attendance_2526','num','cnt',True)
M(A_,'MBB average home attendance 2025-26','mbb_avg_attendance_2526','num','cnt',True); M(A_,'MBB attendance % of capacity 2025-26','f_mbb_attendance_pct_capacity','formula','pct',True)
M(A_,'MBB all games played 2025-26 (top 30)','mbb_all_games_2526','num','cnt'); M(A_,'MBB all-games attendance 2025-26 (top 30)','mbb_all_games_attendance_2526','num','cnt')
M(A_,'MBB average home attendance 2024-25 (top 30 increases)','mbb_avg_attendance_2425','num','cnt'); M(A_,'MBB change in average home attendance 2025-26 (top 30 increases)','mbb_avg_attendance_change_2526','num','cnt')
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
for m in S: m['byfy']=bool(m['sec']=='Financial' and m['agg'])   # MFRS line items: averages and medians also broken out by fiscal year
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
def logrow(s,metric_hdr,value,unit,fy,stype,sname,url,note,date=None):
    sourcelog.append([s['name'],s['conf'],metric_hdr,value,unit,fy,stype,sname,url,date or DATE,note])
def stype_of(r):
    u=(r.get('source_url') or '').lower(); n=(r.get('source_name') or '').lower(); f=r.get('_file','')
    if 'knightnewhouse' in u: return 'Knight-Newhouse'
    if 'sportico' in u: return 'Sportico (MFRS compilation)'
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
    def put(key,val,url,unit,fy,stype,sname,note,log=True,date=None):
        R[key]=(val,url)
        if log: logrow(s,next(m['hdr'] for m in S if m['key']==key),val if val is not None else '--',unit,fy,stype,sname,url if val is not None else '--',note,date)
    nav=f"https://nces.ed.gov/collegenavigator/?id={s['unitid']}"
    put('school',n,nav,'text','','IPEDS','IPEDS College Navigator',nav,f"UNITID {s['unitid']}; {s['ipeds_name']}")
    if s['conf']=='Independent': put('conference',s['conf'],CONF_URL[s['conf']],'text','2025 season','other','D1.ticker, 2025 FBS Attendance Trends (Conference column)',CONF_URL[s['conf']],'Football independent; an ACC member in most other sports, including men\'s basketball')
    else: put('conference',s['conf'],CONF_URL[s['conf']],'text','2026-27','other','Conference official site',CONF_URL[s['conf']],'Membership as of the 2026-27 academic year')
    for key in ('control','state'):
        r=get(n,key); put(key,r['value'],r['source_url'],r['unit'],r['fiscal_year_or_season'],stype_of(r),r['source_name'],r['notes'])
    # financial
    tor=get(n,'total_operating_revenue'); sp=get(n,'sp_total_operating_revenue')
    own_fy=None
    if tor and tor['value']!='--':
        fyr=get(n,'fin_fiscal_year'); own_fy=num(fyr['value']) if fyr and fyr['value']!='--' else num(re.sub(r'\D','',tor['fiscal_year_or_season'])[:4])
    if sp and sp['value']!='--' and num(get(n,'sp_fiscal_year')['value'])>=2024 and not (own_fy and own_fy>num(get(n,'sp_fiscal_year')['value'])):
        fy=num(get(n,'sp_fiscal_year')['value']); SPB='Sportico (MFRS compilation)'
        xnote=''
        if tor and tor['value']!='--':
            rep=get(n,'fin_report_url'); repurl=rep['value'] if rep and rep['value'] not in ('--','') else tor['source_url']
            xnote=f" Cross-check against the school-posted report ({tor['fiscal_year_or_season']}, {repurl}): total operating revenue {num(tor['value']):,} ({'matches' if num(tor['value'])==num(sp['value']) else 'differs'})."
        put('fin_fiscal_year',fy,sp['source_url'],'year',f'FY{fy}',SPB,sp['source_name'],'Fiscal year of the NCAA MFRS report as compiled by Sportico.'+xnote,date=sp['date_accessed'])
        put('fin_basis',SPB,sp['source_url'],'text',f'FY{fy}',SPB,sp['source_name'],"Sportico College Sports Finances Database, compiled from the school's NCAA MFRS report (public schools only)."+xnote,date=sp['date_accessed'])
        for key in ('total_operating_revenue','fb_revenue','mbb_revenue','nonprogram_revenue','total_operating_expenses','media_rights_revenue','ticket_sales_revenue','contributions_revenue','ncaa_conf_distributions','direct_institutional_support','indirect_institutional_support','student_fees','coaching_salaries','athletics_related_debt','debt_service'):
            r=get(n,'sp_'+key); o=get(n,key); on=''
            if r and r['value']!='--':
                if o and o['value']!='--' and key!='ncaa_conf_distributions': on=f" School-posted report value: {num(o['value']):,} ({'matches' if num(o['value'])==num(r['value']) else 'differs'})."
                put(key,num(r['value']),r['source_url'],'USD',f'FY{fy}',SPB,r['source_name'],r['notes']+on,date=r['date_accessed'])
            else: put(key,None,'','USD',f'FY{fy}',SPB,sp['source_name'],'line not reported in the Sportico entry',date=sp['date_accessed'])
    elif tor and tor['value']!='--':
        fyr=get(n,'fin_fiscal_year'); fy=num(fyr['value']) if fyr and fyr['value']!='--' else num(re.sub(r'\D','',tor['fiscal_year_or_season'])[:4])
        rep=get(n,'fin_report_url'); repurl=rep['value'] if rep and rep['value'] not in ('--','') else tor['source_url']
        put('fin_fiscal_year',fy,repurl,'year',f'FY{fy}','MFRS own posting',tor['source_name'],'Fiscal year of the school-posted NCAA MFRS/AUP report')
        put('fin_basis','MFRS own posting',repurl,'text',f'FY{fy}','MFRS own posting',tor['source_name'],'School-posted NCAA Membership Financial Reporting System / agreed-upon procedures report')
        for key in ('total_operating_revenue','fb_revenue','mbb_revenue','nonprogram_revenue','total_operating_expenses','media_rights_revenue','ticket_sales_revenue','contributions_revenue','direct_institutional_support','indirect_institutional_support','student_fees','coaching_salaries','athletics_related_debt','debt_service'):
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
        for key in ('fb_revenue','mbb_revenue','nonprogram_revenue'):
            r=get(n,'eada_'+key)
            if r and r['value']!='--': put(key,num(r['value']),r['source_url'],'USD','FY2025','EADA',r['source_name'],r['notes'])
            else: put(key,None,'','USD','FY2025','EADA','EADA 2024-25','not reported in EADA')
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
        if not r: put(key,None,'','','','other','','not researched (web-search budget exhausted)' if n!='Notre Dame' else 'not sourced in the Notre Dame research pass'); continue
        if r['value']=='--': put(key,None,'',r['unit'],r['fiscal_year_or_season'],stype_of(r),r['source_name'],r['notes'] or 'not sourced'); continue
        val=num(r['value']) if m['kind']=='num' else r['value']
        if key.endswith('_pay_source_type'): st={'contract':'contract','school announcement':'press release','state salary database':'contract','press report':'other'}[val]
        else: st=stype_of(r)
        put(key,val,r['source_url'],r['unit'],r['fiscal_year_or_season'],st,r['source_name'],r['notes'],date=r.get('date_accessed'))
    resolved[n]=R

IDENT={'school','conference','control','state'}
NOLINK={'school','conference','control','state','fin_fiscal_year','total_operating_revenue','total_operating_expenses','media_rights_revenue','ticket_sales_revenue','contributions_revenue','ncaa_conf_distributions','direct_institutional_support','indirect_institutional_support','student_fees','coaching_salaries','athletics_related_debt','debt_service','fb_revenue','mbb_revenue','nonprogram_revenue'}
# ---------- every school in the master list is kept; schools without public MFRS data carry the EADA basis ----------
EXCLUDED=[]
DTYPE={s['name']:('EADA' if resolved[s['name']]['fin_basis'][0]=='EADA' else 'MFRS') for s in order}
NS=len(order); print('schools',NS,'| EADA basis',sorted(n for n,v in DTYPE.items() if v=='EADA'))
# ---------- workbook (house style: SMASHSPORTS diligence workbook conventions) ----------
BRAND=CellRichText(TextBlock(InlineFont(rFont='Montserrat',sz=11,b=True,color='000000'),'SMASH'),TextBlock(InlineFont(rFont='Montserrat',sz=11,b=False,color='000000'),'SPORTS')); ENTITY='Power 4 Athletic Department Benchmarking'
FN='Aptos Narrow'; FS=9
F_BASE=Font(name=FN,size=FS); F_B=Font(name=FN,size=FS,bold=True); F_I=Font(name=FN,size=FS,color='008000'); F_HC=Font(name=FN,size=FS,color='0000FF')
F_HDR=Font(name=FN,size=FS,color='FFFFFF'); F_BRAND=Font(name='Montserrat',size=11,color='000000'); F_LINKED=Font(name=FN,size=FS,color='0000FF',underline='single')   # hardcode with a source hyperlink attached: blue, underlined
FILL_BLACK=PatternFill('solid',fgColor='000000'); FILL_SEC=PatternFill('solid',fgColor='E8E8E8'); FILL_IN=PatternFill('solid',fgColor='FFFFCC'); FILL_SUB=PatternFill('solid',fgColor='D9D9D9')
THIN=Side(style='thin',color='000000'); DBL=Side(style='double',color='000000')
B_TB=Border(top=THIN,bottom=THIN); B_T=Border(top=THIN); B_TOT=Border(top=THIN,bottom=DBL)
ACCT='_(* #,##0_);_(* \\(#,##0\\);_(* "-"??_);_(@_)'
FMT={'usd':ACCT,'pct':'0.0%','cnt':ACCT,'wp':'0.000','yr':'0','pts':'#,##0.00','idx':'0'}
OFF=2                      # data starts in column C; A is a 1-wide gutter, B carries the title block
def CL(i): return L(i+OFF)
R_HDR=6; R0=7
CENTER=Alignment(horizontal='center'); IND1=Alignment(indent=1)
wb=openpyxl.Workbook(); wb.remove(wb.active)
def prep(ws,title,units='Whole dollars unless the column header says otherwise'):
    ws.sheet_view.showGridLines=False
    ws.column_dimensions['A'].width=1; ws.column_dimensions['B'].width=2
    ws.row_dimensions[2].height=16.5; ws.row_dimensions[R_HDR].height=24
    ws['B2']=BRAND; ws['B2'].font=F_BRAND; ws['B2'].alignment=Alignment(horizontal='left')
    ws['B3']=ENTITY; ws['B3'].font=F_B
def header(ws,labels,first_col=1):
    for j,h in enumerate(labels):
        c=ws.cell(row=R_HDR,column=first_col+OFF+j,value=h); c.font=F_HDR; c.fill=FILL_BLACK; c.border=B_TB; c.alignment=CENTER
def setw(ws,widths):
    for c,w in widths.items(): ws.column_dimensions[CL(c)].width=min(max(w,8),70)
def put_cell(cell,val,font,fmt=None,fill=None,border=None,align=None):
    cell.value=val; cell.font=font
    if fmt: cell.number_format=FMT[fmt]
    if fill: cell.fill=fill
    if border: cell.border=border
    if align: cell.alignment=align

# ---- summary scopes: a grid of fiscal year (each year, then all years) by data source (MFRS, EADA, then all sources);
# combinations with no schools are left out, and the last scope (all years, all sources) is the overall row ----
FYS=sorted({resolved[s['name']]['fin_fiscal_year'][0] for s in order},reverse=True)
TYPES=('MFRS','EADA')
def _has(ty,fy): return any((ty=='All' or DTYPE[s['name']]==ty) and (fy=='All' or resolved[s['name']]['fin_fiscal_year'][0]==fy) for s in order)
SCOPES=[]   # (key, type criterion, year criterion, label)
for _fy in FYS+['All']:
    for _ty in TYPES+('All',):
        if not _has(_ty,_fy): continue
        _yl='all years' if _fy=='All' else f'FY{_fy}'
        if (_ty,_fy)==('All','All'): SCOPES.append(('All','All','All','overall'))
        else: SCOPES.append((f'{_ty}|{_fy}',_ty,_fy,f"{_yl} {_ty if _ty!='All' else 'all sources'}"))
STATS=(('Average','AVERAGE'),('Median','MEDIAN'),('Count','COUNT'))   # Count = schools with a value in the column
BASES=('Sportico (MFRS compilation)','MFRS own posting','EADA')
BASC=COL['fin_basis']; FYC=COL['fin_fiscal_year']; DTC=COL['f_fin_data_type']
F_BG=Font(name=FN,size=FS,bold=True,color='008000')
NOT_DASH='"<>--"'   # COUNTIFS criterion: the cell holds a value, not the -- placeholder
def counts_for(m,key): return m['key']!='school' and (key=='All' or m['sec']=='Financial')   # scoped counts cover the financial columns only
def breakdown(ws,top,cols,count_formula):
    """Table of school counts: by financial data type and fiscal year, then by financial source basis.
    count_formula(kind, band_cell, label_cell, header_cell, j, r) returns the formula for one count cell."""
    out=dict(header=top,cols=cols,types={},basis={})
    for j,h in enumerate(['Data breakdown']+cols):
        c=ws.cell(row=top,column=1+OFF+j,value=h); c.font=F_HDR; c.fill=FILL_BLACK; c.border=B_TB; c.alignment=CENTER
    r=top+1
    def band(title):
        nonlocal r
        for j in range(len(cols)+1):
            c=ws.cell(row=r,column=1+OFF+j); c.fill=FILL_SEC; c.font=F_B; c.border=B_TB
        ws.cell(row=r,column=1+OFF).value=title; r+=1; return r-1
    def total(label,first):
        nonlocal r
        for j in range(len(cols)+1):
            c=ws.cell(row=r,column=1+OFF+j); c.font=F_B; c.border=B_T
            if j==0: c.value=label; c.alignment=IND1
            else: c.value=f'=SUM({CL(1+j)}{first}:{CL(1+j)}{r-1})'; c.number_format=FMT['cnt']
        r+=1; return r-1
    def item(kind,bandrow,value):
        nonlocal r
        lab=ws.cell(row=r,column=1+OFF,value=value); lab.font=F_BASE; lab.alignment=IND1
        if kind=='fy': lab.number_format='"FY"0'
        for j in range(len(cols)):
            c=ws.cell(row=r,column=2+OFF+j,value=count_formula(kind,f'${CL(1)}${bandrow}',f'${CL(1)}{r}',f'{CL(2+j)}${top}',j,r)); c.font=F_BASE; c.number_format=FMT['cnt']
        r+=1; return r-1
    for ty in TYPES:                       # the band label (MFRS, EADA) is the criterion for the rows under it
        b=band(ty); first=r; d=dict(band=b,fy={})
        for fy in FYS: d['fy'][str(fy)]=item('fy',b,fy)
        d['total']=total(f'Total {ty}',first); out['types'][ty]=d
    b=band('Schools by financial source basis'); first=r
    for bs in BASES: out['basis'][bs]=item('basis',b,bs)
    out['basis_total']=total('Total',first); out['last']=r-1
    return out
def summary_style(cell,top=False,bottom=False):
    cell.fill=FILL_SUB; cell.font=F_B
    if top and bottom: cell.border=Border(top=THIN,bottom=DBL)
    elif top: cell.border=B_T
    elif bottom: cell.border=Border(bottom=DBL)
def summary_and_breakdown(ws,first,last):
    """Under the school rows first..last: Average, Median and Count rows for every scope, then the data-breakdown table.
    Used unchanged on every conference tab and on All Schools."""
    summary={st:{} for st,_ in STATS}; rr=last+1
    for st,_ in STATS:
        for key,_ty,_fy,_lab in SCOPES: summary[st][key]=rr; rr+=1
    sum_last=rr-1
    fyr=f'${CL(FYC)}${first}:${CL(FYC)}${last}'; typer=f'${CL(DTC)}${first}:${CL(DTC)}${last}'; basr=f'${CL(BASC)}${first}:${CL(BASC)}${last}'
    for st,fn in STATS:
        for k,(key,ty,fy,slab) in enumerate(SCOPES):
            rr=summary[st][key]
            for i,m in enumerate(S,1):
                cell=ws.cell(row=rr,column=i+OFF); summary_style(cell,top=(k==0),bottom=(st==STATS[-1][0] and k==len(SCOPES)-1))
                rng=f'{CL(i)}{first}:{CL(i)}{last}'
                terms=([f'({typer}=${CL(DTC)}{rr})'] if ty!='All' else [])+([f'({fyr}=${CL(FYC)}{rr})'] if fy!='All' else [])
                crit=([typer,f'${CL(DTC)}{rr}'] if ty!='All' else [])+([fyr,f'${CL(FYC)}{rr}'] if fy!='All' else [])
                if i==1: cell.value=f'{st}, {slab}'; continue
                if i==FYC: cell.value=fy; cell.number_format=FMT['yr']; cell.alignment=Alignment(horizontal='right'); continue
                if i==DTC: cell.value=ty; continue
                if st=='Count':
                    if not counts_for(m,key): cell.value='--'; continue
                    cell.number_format=FMT['cnt']
                    cell.value=f'=COUNTIFS({",".join(crit+[rng,NOT_DASH])})'
                    continue
                if not m['agg'] or (key!='All' and not m['byfy']): cell.value='--'; continue
                cell.number_format=FMT[m['fmt']]
                if not terms: cell.value=f'=IFERROR({fn}({rng}),"--")'
                elif st=='Average': cell.value=f'=IFERROR(AVERAGEIFS({rng},{",".join(crit)}),"--")'
                else: cell.value=ArrayFormula(cell.coordinate,f'=IFERROR(MEDIAN(IF({"*".join(terms)},{rng},"")),"--")')
    bd=breakdown(ws,sum_last+2,['Schools'],lambda kind,bandc,lab,hdr,j,r: (f'=COUNTIFS({typer},{bandc},{fyr},{lab})' if kind=='fy' else f'=COUNTIFS({basr},{lab})'))
    return dict(first=first,last=last,avg=summary['Average']['All'],med=summary['Median']['All'],sum_first=last+1,sum_last=sum_last,summary=summary,breakdown=bd)
# ---- conference tabs ----
conf_rows={}; conf_layout={}
for conf,sname in CONFS:
    ws=wb.create_sheet(sname); ss=by_conf[conf]; n=len(ss)
    prep(ws,f'{conf}: one row per school, latest fiscal year')
    header(ws,[m['hdr'] for m in S])
    for j,s in enumerate(ss):
        r=R0+j; conf_rows[s['name']]=(sname,r); R=resolved[s['name']]
        def A(key): return f"{CL(COL[key])}{r}"
        for i,m in enumerate(S,1):
            cell=ws.cell(row=r,column=i+OFF); key=m['key']
            if m['kind']=='formula':
                if key=='f_fin_data_type': f=f'=IF({A("fin_basis")}="EADA","EADA","MFRS")'
                elif key=='f_surplus': f=f'=IF(AND(ISNUMBER({A("total_operating_revenue")}),ISNUMBER({A("total_operating_expenses")})),{A("total_operating_revenue")}-{A("total_operating_expenses")},"--")'
                elif key=='f_subsidy': f=f'=IF(AND(ISNUMBER({A("direct_institutional_support")}),ISNUMBER({A("student_fees")})),{A("direct_institutional_support")}+{A("student_fees")}+IF(ISNUMBER({A("indirect_institutional_support")}),{A("indirect_institutional_support")},0),"--")'
                elif key=='f_other_sports_revenue': f=f'=IF(AND(ISNUMBER({A("total_operating_revenue")}),ISNUMBER({A("fb_revenue")}),ISNUMBER({A("mbb_revenue")}),ISNUMBER({A("nonprogram_revenue")})),{A("total_operating_revenue")}-{A("fb_revenue")}-{A("mbb_revenue")}-{A("nonprogram_revenue")},"--")'
                elif key=='f_subsidy_pct': f=f'=IF(AND(ISNUMBER({A("f_subsidy")}),ISNUMBER({A("total_operating_revenue")}),{A("total_operating_revenue")}>0),{A("f_subsidy")}/{A("total_operating_revenue")},"--")'
                elif key=='f_mbb_attendance_pct_capacity': f=f'=IF(AND(ISNUMBER({A("mbb_avg_attendance_2526")}),ISNUMBER({A("arena_capacity")}),{A("arena_capacity")}>0),{A("mbb_avg_attendance_2526")}/{A("arena_capacity")},"--")'
                elif key=='f_fb_winpct': f=f'=IF(AND(ISNUMBER({A("fb_wins_2021_25")}),ISNUMBER({A("fb_losses_2021_25")})),{A("fb_wins_2021_25")}/({A("fb_wins_2021_25")}+{A("fb_losses_2021_25")}),"--")'
                elif key=='f_mbb_winpct': f=f'=IF(AND(ISNUMBER({A("mbb_wins_2122_2526")}),ISNUMBER({A("mbb_losses_2122_2526")})),{A("mbb_wins_2122_2526")}/({A("mbb_wins_2122_2526")}+{A("mbb_losses_2122_2526")}),"--")'
                elif key.endswith('_expires'):
                    pre=key[2:-8]; f=f'=IF(AND(ISNUMBER({A(pre+"_start_year")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_start_year")}+{A(pre+"_term_years")},"--")'
                put_cell(cell,f,F_BASE,m['fmt']); continue
            val,url=R[key]
            if key in IDENT: put_cell(cell,val if val is not None else '--',F_BASE,m['fmt'],align=IND1 if key=='school' else None)
            elif val is None: put_cell(cell,'--',F_HC,m['fmt'])
            elif key in NOLINK: put_cell(cell,val,F_HC,m['fmt'])
            else:
                put_cell(cell,val,F_LINKED if url else F_HC,m['fmt'])
                if url: cell.hyperlink=url; cell.font=F_LINKED
        for pre in ('stadium_nr','arena_nr','patch','mmr','apparel'):
            a,t,tot=R[pre+'_annual_value'][0],R[pre+'_term_years'][0],R[pre+'_total_value'][0]
            ca,ct,ctot=ws[A(pre+'_annual_value')],ws[A(pre+'_term_years')],ws[A(pre+'_total_value')]
            def formula_cell(c,f,fmt):
                c.hyperlink=None; put_cell(c,f,F_BASE,fmt)
            if a is not None and t is not None and tot is not None:
                formula_cell(ctot,f'=IF(AND(ISNUMBER({A(pre+"_annual_value")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_annual_value")}*{A(pre+"_term_years")},"--")','usd')
                for row in sourcelog:
                    if row[0]==s['name'] and row[2]==next(mm['hdr'] for mm in S if mm['key']==pre+'_total_value'): row[10]=f'Reported total {tot:,}; cell shows Annual x Term per the deal-value rule. '+row[10]
            elif a is not None and t is not None and tot is None: formula_cell(ctot,f'=IF(AND(ISNUMBER({A(pre+"_annual_value")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_annual_value")}*{A(pre+"_term_years")},"--")','usd')
            elif tot is not None and t is not None and a is None: formula_cell(ca,f'=IF(AND(ISNUMBER({A(pre+"_total_value")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_total_value")}/{A(pre+"_term_years")},"--")','usd')
            elif a is not None and tot is not None and t is None: formula_cell(ct,f'=IF(AND(ISNUMBER({A(pre+"_total_value")}),ISNUMBER({A(pre+"_annual_value")})),{A(pre+"_total_value")}/{A(pre+"_annual_value")},"--")','cnt')
    conf_layout[conf]=dict(sheet=sname,**summary_and_breakdown(ws,R0,R0+n-1))
    widths={i:max(len(m['hdr']),max((len(str(resolved[s['name']][m['key']][0] or '--')) for s in ss),default=0) if m['kind']!='formula' else 14)+2 for i,m in enumerate(S,1)}
    widths[1]=max(widths[1],30); setw(ws,widths); ws.freeze_panes=f'{CL(2)}{R0}'

# ---- All Schools ----
ws=wb.create_sheet('All Schools',0)
prep(ws,f'All {NS} schools: links to the conference tabs, with averages, medians and counts for all schools')
header(ws,[m['hdr'] for m in S])
all_first=R0; all_last=R0+len(order)-1
for j,s in enumerate(order):
    sname,sr=conf_rows[s['name']]; r=all_first+j
    for i,m in enumerate(S,1):
        cell=ws.cell(row=r,column=i+OFF,value=f"='{sname}'!{CL(i)}{sr}"); cell.font=F_BASE if m['key'] in IDENT else F_I
        if m['fmt']: cell.number_format=FMT[m['fmt']]
        if m['key']=='school': cell.alignment=IND1
# summary rows and data breakdown for all schools only; the by-conference figures live on the conference tabs
all_layout=summary_and_breakdown(ws,all_first,all_last)
setw(ws,{i:max(len(m['hdr']),14)+2 for i,m in enumerate(S,1)}); ws.column_dimensions[CL(1)].width=30; ws.freeze_panes=f'{CL(2)}{R0}'

# ---- Read Me ----
ws=wb.create_sheet('Read Me',0); prep(ws,'Read me: scope, sources, conventions',units=None)
lines=[
 f'Coverage: {NS} athletic departments: the 67 Power 4 schools and Notre Dame, a football independent ({", ".join(f"{c} {len(by_conf[c])}" for c,_ in CONFS)}); one row per school on the conference tabs and the Independent tab, which hold every hardcoded value.',
 f'Financial data type: {sum(v=="MFRS" for v in DTYPE.values())} schools have public NCAA MFRS data; the other {sum(v=="EADA" for v in DTYPE.values())} (the private universities, including Notre Dame, and Pittsburgh) do not, so their financials are the federal EADA 2024-25 report (fiscal 2025). EADA reports only total revenue, total expenses, football revenue, men\'s basketball revenue and unallocated revenue, and its definitions differ from MFRS; every other financial line shows -- for those schools.',
 'Structure: All Schools links every row on the conference and Independent tabs; Source Log is the audit trail (values); School Lookup looks up any school.',
 "Financials for public schools come from the Sportico College Sports Finances Database, which compiles each school's NCAA MFRS report (FY2025, FY2024 where that is the latest posted); where the school also posts its own MFRS report, the Source Log records that figure as a cross-check.",
 'The Financial source basis column states Sportico, MFRS own posting or EADA for each school, Financial data type states MFRS or EADA, and the fiscal year column states the report year.',
 "Other sources: NCAA APR and GSR search tools (2024-25 release), IPEDS fall 2024 headcount, ESPN standings (football 2021-25) and Sports-Reference (men's basketball 2021-22 to 2025-26), NACDA Directors' Cup final standings (2024-25 and 2025-26), school and partner releases and trade press for venues and commercial deals.",
 "Football attendance comes from the D1.ticker FBS Attendance Trends pages, as displayed: average home attendance for 2023, 2024 and 2025 (the Final Average column of each season's own page), and from the 2025 page the year-over-year change, the 5-year average (the page does not say which five seasons), the change against that 5-year average and the percent of capacity. The pages give averages only, with no totals or game counts, and do not state their underlying data source or whether figures are announced or paid.",
 "Men's basketball attendance comes from the 2026 Attendance Summary in the NCAA Men's Basketball Attendance Records book (through 2025-26): home games, total home attendance and average home attendance for every school. Columns marked top 30 come from NCAA leader tables that list only 30 teams (all-games attendance, and the prior-year average for the 30 largest increases); they show -- for other schools and carry no average or median.",
 "Percent of capacity covers the same year for both sports: football 2025 is the Capacity % column of the D1.ticker 2025 page, as reported (D1.ticker does not publish the capacity it divides by, so it can differ from the Stadium capacity column); men's basketball 2025-26 is a formula, average home attendance divided by Arena capacity, because the NCAA book reports no percentage.",
 f"Averages, medians and counts: financial line items are summarized by fiscal year and data source ({', '.join(x[3] for x in SCOPES[:-1])}), using the Financial data type and Fiscal year columns as the filters. Rows marked MFRS or EADA never mix the two; rows marked all sources do, and for EADA schools only the five lines EADA reports contribute. The overall rows cover every school, and every non-financial column is summarized overall only. Count rows give the number of schools with a value in each column. Summary rows sit under the schools on each conference tab (for that conference) and on All Schools (for all schools).",
 "Data breakdown: under the summary rows, each conference tab and All Schools carry a table counting schools by financial data type and fiscal year, and by financial source basis.",
 'Conventions: blue cells are hardcoded figures (underlined where a source hyperlink is attached), black cells are formulas and identity text, green cells are links to another tab, gray rows are averages and medians, yellow is the input cell on School Lookup; financial cells are sourced through the hyperlink on Financial source basis; "--" means not publicly sourced, with the reason in Source Log.',
 'No newspaper-compiled finance or coaching-salary databases are used anywhere in this workbook. Date accessed for all sources: 2026-11-09 and 2026-11-10.',
]
for k,t in enumerate(lines): ws.cell(row=R0+k,column=1+OFF,value=t).font=F_BASE
ws.column_dimensions[CL(1)].width=220

# ---- Source Log ----
ws=wb.create_sheet('Source Log')
hdr=['School','Conference','Metric','Value','Unit','Fiscal year or season','Source type','Source name','URL','Date accessed','Note']
prep(ws,'Source log: one row per sourced value (values, not formulas)',units=None)
header(ws,hdr)
for j,row in enumerate(sourcelog):
    for i,v in enumerate(row,1):
        c=ws.cell(row=R0+j,column=i+OFF,value=(v if v not in (None,'') else '--')); c.font=F_BASE
setw(ws,{1:20,2:10,3:36,4:18,5:10,6:26,7:22,8:40,9:60,10:13,11:80}); ws.freeze_panes=f'{CL(1)}{R0}'

# ---- School Lookup ----
def vertical_sheet(ws,title,name_value,name_font,name_fill,src_sheet,first,last,avg_row,with_avg):
    ncols=4 if with_avg else 2
    prep(ws,title,units=None)
    ws.cell(row=5,column=1+OFF,value='School').font=F_B
    nc=ws.cell(row=5,column=2+OFF,value=name_value); nc.font=name_font
    if name_fill: nc.fill=name_fill
    NAME=f'${CL(2)}$5'
    header(ws,['Metric','Value']+(['Conference average','Difference'] if with_avg else []))
    r=R0; sec=None
    rng=f"'{src_sheet}'!${CL(1)}${first}:${CL(NC)}${last}"; hdrrng=f"'{src_sheet}'!${CL(1)}${R_HDR}:${CL(NC)}${R_HDR}"; namerng=f"'{src_sheet}'!${CL(1)}${first}:${CL(1)}${last}"
    for m in S:
        if m['sec']!=sec:
            sec=m['sec']
            for i in range(1,ncols+1):
                c=ws.cell(row=r,column=i+OFF); c.fill=FILL_SEC; c.font=F_B; c.border=B_TB
            ws.cell(row=r,column=1+OFF).value=sec; r+=1
        lab=ws.cell(row=r,column=1+OFF,value=m['hdr']); lab.font=F_BASE; lab.alignment=IND1
        labref=f'${CL(1)}{r}'
        c=ws.cell(row=r,column=2+OFF,value=f'=INDEX({rng},MATCH({NAME},{namerng},0),MATCH({labref},{hdrrng},0))'); c.font=F_BASE if m['key'] in IDENT else F_I
        if m['fmt']: c.number_format=FMT[m['fmt']]
        if with_avg:
            avgrng=f"'{src_sheet}'!${CL(1)}${avg_row}:${CL(NC)}${avg_row}"
            c2=ws.cell(row=r,column=3+OFF,value=f'=IF(ISNUMBER({CL(2)}{r}),INDEX({avgrng},1,MATCH({labref},{hdrrng},0)),"--")'); c2.font=F_BASE if m['key'] in IDENT else F_I
            c3=ws.cell(row=r,column=4+OFF,value=f'=IF(AND(ISNUMBER({CL(2)}{r}),ISNUMBER({CL(3)}{r})),{CL(2)}{r}-{CL(3)}{r},"--")'); c3.font=F_BASE
            if m['fmt']: c2.number_format=FMT[m['fmt']]; c3.number_format=FMT[m['fmt']]
        r+=1
    setw(ws,{1:40,2:44,3:22,4:22}); ws.freeze_panes=f'{CL(2)}{R0}'
ws=wb.create_sheet('School Lookup')
vertical_sheet(ws,'School lookup: choose a school in the yellow cell','Alabama',F_BASE,FILL_IN,'All Schools',all_first,all_last,None,False)
dv=DataValidation(type='list',formula1=f"='All Schools'!${CL(1)}${all_first}:${CL(1)}${all_last}",allow_blank=False); ws.add_data_validation(dv); dv.add(f'{CL(2)}5')
names=['Read Me','All Schools']+[sn for _,sn in CONFS]+['Source Log','School Lookup']   # no per-school tabs: School Lookup covers every school
wb._sheets=[wb[n] for n in names]
for ws in wb: ws.sheet_view.showGridLines=False
wb.save(OUT); print('saved',OUT,'sheets',len(wb.sheetnames),'sourcelog rows',len(sourcelog))
json.dump(dict(S=S,conf_layout=conf_layout,all_first=all_first,all_last=all_last,all_layout=all_layout,bases=list(BASES),types=list(TYPES),scopes=[list(x) for x in SCOPES],fiscal_years=FYS,n_schools=NS,excluded=EXCLUDED,col_offset=OFF,header_row=R_HDR),open('data/workbook_layout.json','w'))
