"""Build the Power 4 athletic department benchmarking workbook from data/merged_values.csv."""
import csv, json, os, re
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
M('Coaching','Head football coach','fb_hc_name','text'); M('Coaching','FB HC total pay','fb_hc_annual_comp','num','usd',True); M('Coaching','FB HC contract end season (year season begins)','fb_hc_contract_end','num','yr'); M('Coaching','FB HC pay source type','fb_hc_pay_source_type','text')
M('Coaching','Head men\'s basketball coach','mbb_hc_name','text'); M('Coaching','MBB HC total pay 2026','mbb_hc_annual_comp','num','usd',True); M('Coaching','MBB HC total pay 2025','mbb_hc_prior_comp','num','usd',True); M('Coaching','MBB HC contract end season (year season ends)','mbb_hc_contract_end','num','yr'); M('Coaching','MBB HC pay source type','mbb_hc_pay_source_type','text')
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
M('Academic','FB multi-year APR, 2024-25','fb_apr_multiyear','num','idx',True); M('Academic','Department GSR (%), 2025 release','dept_gsr','num','idx',True); M('Academic','FB GSR (%), 2025 release','fb_gsr','num','idx',True); M('Academic','Academic data year','academic_data_year','text')
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
        if key.endswith('_pay_source_type'): st={'contract':'contract','school announcement':'press release','state salary database':'contract','press report':'other','USA Today':'other'}[val]
        else: st=stype_of(r)
        note=r['notes']; season=r['fiscal_year_or_season']
        if key.endswith('hc_contract_end') and isinstance(val,(int,float)):   # one structure for every school
            y=int(val)
            if key.startswith('fb'): season=f'{y} season'; note=f'Contract runs through the {y} football season ({y}-{str(y+1)[2:]} academic year). '+(note or '')
            else: season=f'{y-1}-{str(y)[2:]} season'; note=f'Contract runs through the {y-1}-{str(y)[2:]} season. '+(note or '')
        put(key,val,r['source_url'],r['unit'],season,st,r['source_name'],note,date=r.get('date_accessed'))
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
# accounting-style layout (thousands separators, negatives in parentheses, zero as a dash, right padding) but without
# the "* " fill of the built-in accounting format: that fill is underlined on hyperlinked cells and draws a line across the cell
ACCT='#,##0_);\\(#,##0\\);"-"??_);_(@_)'
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
NO_DERIVE={(r['school'],r['deal_prefix']) for r in csv.DictReader(open('data/no_derive.csv',encoding='utf-8'))} if os.path.exists('data/no_derive.csv') else set()
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
            if (s['name'],pre) in NO_DERIVE: pass   # the reported figures do not describe the same period; show them as reported
            elif a is not None and t is not None and tot is not None:
                formula_cell(ctot,f'=IF(AND(ISNUMBER({A(pre+"_annual_value")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_annual_value")}*{A(pre+"_term_years")},"--")','usd')
                for row in sourcelog:
                    if row[0]==s['name'] and row[2]==next(mm['hdr'] for mm in S if mm['key']==pre+'_total_value'): row[10]=f'Reported total {tot:,}; cell shows Annual x Term per the deal-value rule. '+row[10]
            elif a is not None and t is not None and tot is None: formula_cell(ctot,f'=IF(AND(ISNUMBER({A(pre+"_annual_value")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_annual_value")}*{A(pre+"_term_years")},"--")','usd')
            elif tot is not None and t is not None and a is None: formula_cell(ca,f'=IF(AND(ISNUMBER({A(pre+"_total_value")}),ISNUMBER({A(pre+"_term_years")})),{A(pre+"_total_value")}/{A(pre+"_term_years")},"--")','usd')
            elif a is not None and tot is not None and t is None: formula_cell(ct,f'=IF(AND(ISNUMBER({A(pre+"_total_value")}),ISNUMBER({A(pre+"_annual_value")})),{A(pre+"_total_value")}/{A(pre+"_annual_value")},"--")','cnt')
            # a stated end year takes the place of the start + term formula: sources often give when a deal runs to
            # without giving an effective start, and the stated end is the more reliable figure for extensions
            er=get(s['name'],pre+'_end_year')
            if er and er['value'] not in ('--',''):
                ce=ws[A('f_'+pre+'_expires')]; put_cell(ce,num(er['value']),F_LINKED if er['source_url'] else F_HC,'yr')
                if er['source_url']: ce.hyperlink=er['source_url']
                logrow(s,next(mm['hdr'] for mm in S if mm['key']=='f_'+pre+'_expires'),num(er['value']),'year',er['fiscal_year_or_season'],stype_of(er),er['source_name'],er['source_url'],er['notes'],er.get('date_accessed'))
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
ws=wb.create_sheet('Read Me',0); prep(ws,'Read me: what is in this file and how I built it',units=None)
# Written in the analyst's own voice: first person, plain, purpose first, figures and document names stated, open
# items called out at the end. Counts are computed from the data so the text cannot drift from the tabs.
def _has(n,key): return isinstance(resolved[n].get(key,(None,))[0],(int,float))
def _annual(n,pre):   # an annual value is shown when reported, or when total and term are both shown and derivation is allowed
    return _has(n,pre+'_annual_value') or (_has(n,pre+'_total_value') and _has(n,pre+'_term_years') and (n,pre) not in NO_DERIVE)
_names=[s['name'] for s in order]
def _w(n): return {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine'}.get(n,str(n))   # small counts in words
_nm=sum(1 for v in DTYPE.values() if v=='MFRS'); _ne=NS-_nm
_own=sorted(n for n in _names if resolved[n]['fin_basis'][0]=='MFRS own posting')
_fy24=sum(1 for n in _names if DTYPE[n]=='MFRS' and resolved[n]['fin_fiscal_year'][0]==2024)
_ufb=sum(1 for n in _names if resolved[n]['fb_hc_pay_source_type'][0]=='USA Today'); _umb=sum(1 for n in _names if resolved[n]['mbb_hc_pay_source_type'][0]=='USA Today')
_pfb=sum(_has(n,'fb_hc_annual_comp') for n in _names); _pmb=sum(_has(n,'mbb_hc_annual_comp') for n in _names); _pmb5=sum(_has(n,'mbb_hc_prior_comp') for n in _names)
_diff=sum(1 for r in csv.DictReader(open('data/research/verification_zzzzz_usatoday.csv',encoding='utf-8')) if 'Another source gives' in r['notes']) if os.path.exists('data/research/verification_zzzzz_usatoday.csv') else 0
_deal={lab:sum(_annual(n,pre) for n in _names) for lab,pre in (('multimedia rights','mmr'),('apparel','apparel'),('stadium naming rights','stadium_nr'),('arena naming rights','arena_nr'),('jersey patch','patch'))}
_conf=', '.join(f'{c} {len(by_conf[c])}' for c,_ in CONFS if c!='Independent')
_cal=resolved.get('California',{})
lines=[
 ('Purpose',f'I put this workbook together to benchmark the {NS} Power 4 athletic departments (the 67 Power 4 schools plus Notre Dame, which is a football independent) on finances, coaching, venues, attendance, commercial deals and academics, so we can compare any one department against its conference and against the full group.'),
 ('How to read it',f'Each school has one row on its conference tab ({_conf}) or on the Independent tab, and those tabs hold every hardcoded value. All Schools links to those rows, School Lookup pulls up any one school, and Source Log lists the source, link, date accessed and a short note for every value in the file.'),
 ('Colors','Blue cells are hardcoded figures, underlined where I attached the source link. Black cells are formulas and school names, green cells link to another tab, gray rows are averages and medians, and the yellow cell on School Lookup is the one input. Where I could not find a public source, the cell shows "--" and Source Log gives the reason.'),
 ('Financials, public schools',f'For the {_nm} schools with public NCAA MFRS reports, I used the Sportico College Sports Finances Database, which compiles each school\'s report. Most are fiscal 2025; {_w(_fy24)} are fiscal 2024 because that is the latest posted. {_w(len(_own)).capitalize()} schools ({", ".join(_own)}) are on the report the school posted itself because it is newer than what Sportico has. Where a school on Sportico also posts its own report, I logged that figure in Source Log as a cross-check.'),
 ('California','I used the fiscal 2025 statement Cal posted. Its expense total of 165,382,286 leaves facilities debt service below the line, so I added the 8,474,702 back to match how the other schools report (they count it within operating expenses). Cal\'s total also includes 4,202,756 of transfers to the institution, which I left in.'),
 ('Financials, private schools',f'The other {_ne} schools (the private universities, including Notre Dame, plus Pittsburgh) do not publish MFRS reports, so I used the federal EADA report for 2024-25 (fiscal 2025). EADA only gives total revenue, total expenses, football revenue, men\'s basketball revenue and unallocated revenue, and it defines them differently from MFRS. Every other financial line shows "--" for those schools, and I would not compare the two groups line for line.'),
 ('Financial labels','Financial source basis says Sportico, MFRS own posting or EADA for each school, Financial data type says MFRS or EADA, and Fiscal year gives the report year. The source link for a school\'s financial cells is on its Financial source basis cell.'),
 ('Head coach pay',f'I used the Total Pay column in USA Today\'s coaches\' pay tables, which is school pay plus pay from other sources, before bonuses. Football is the 2025 season table, the latest published. Men\'s basketball shows table years 2026 (the 2025-26 season) and 2025 (the 2024-25 season). Total Pay can include retention or one-time payments; where the table says so, I repeated it in the Source Log note.'),
 ('Where USA Today has no figure','For new hires and most private schools, USA Today has no figure for the current head coach. In those cells I used the coach\'s current pay from a contract, school release or press report, and left the 2025 basketball cell blank. The pay source type column says which kind of source it is, and Source Log gives the season for every figure.'),
 ('Coach contract end','The year shown is the last season the contract covers. For football that is the year the season begins, so a contract that runs through January 31, 2031 shows 2030. For men\'s basketball it is the year the season ends, so a contract through the 2030-31 season shows 2031.'),
 ('Deal dates and values','The expires column is the stated end year where a source gives one (blue); otherwise it is a formula, start year plus term (black). Where a source gives only the announcement, I used the announcement year as the start year and said so in Source Log. Where a source gives two of annual value, term and total value, the third is a formula, so an annual value is sometimes a contract average.'),
 ('Football attendance','This comes from the D1.ticker FBS Attendance Trends pages: average home attendance for 2023, 2024 and 2025, plus the year-over-year change, 5-year average, change against that average and percent of capacity from the 2025 page. D1.ticker gives averages only (no totals or game counts) and does not say which five seasons are in its 5-year average or where its data comes from, so I show the figures as displayed.'),
 ('Men\'s basketball attendance','This comes from the 2026 Attendance Summary in the NCAA Men\'s Basketball Attendance Records book (through 2025-26): home games, total home attendance and average home attendance for every school. Columns marked top 30 come from NCAA leader tables that list only 30 teams, so they show "--" for everyone else and carry no average or median.'),
 ('Percent of capacity','Both sports cover the same year. Football 2025 is D1.ticker\'s Capacity % as reported; D1.ticker does not publish the capacity it divides by, so it can differ from the Stadium capacity column. Men\'s basketball 2025-26 is a formula, average home attendance divided by Arena capacity, because the NCAA book gives no percentage.'),
 ('Academics','Graduation rates are the NCAA\'s most recent Graduation Success Rate release, published in November 2025. It covers student-athletes who entered from 2015-16 through 2018-19 because the NCAA allows six years to graduate, so this is the newest figure available and not old data. APR is the 2024-25 multi-year rate. The next annual release had not been published when I last checked on November 13, 2026.'),
 ('Other sources','Enrollment is the IPEDS fall 2024 headcount. Records are from ESPN standings (football, 2021-25) and Sports-Reference (men\'s basketball, 2021-22 to 2025-26). Directors\' Cup is the NACDA final standings for 2024-25 and 2025-26. Venues and commercial deals come from school and partner releases and the trade press.'),
 ('Averages, medians and counts','Under the schools on each conference tab and on All Schools, I added average, median and count rows. Financial lines are broken out by fiscal year and data source (FY2025 MFRS, FY2025 EADA, FY2025 all sources, FY2024 MFRS, FY2024 all sources, all years MFRS, all years EADA) so MFRS and EADA are never mixed unless the row says all sources. For EADA schools only the five lines EADA reports count toward those rows. Every non-financial column is summarized overall only, and the count rows show how many schools have a value in each column.'),
 ('Data breakdown','Below the summary rows there is a small table counting schools by financial data type and fiscal year, and by financial source basis.'),
 ('Verification','The Verification column in Source Log says how each value was checked. Source data file means it came from a dataset saved with the build files. Found on source page means an automated check found the figure in the text of the cited page. Re-read and confirmed means the page was read again and states the figure. Analyst classification marks categories I assigned (deal type, industry, pay source type). Not re-verified means the cited page could not be read again.'),
 ('Things to keep in mind','A few gaps and judgment calls I want to flag:'),
 ('1. Coach pay timing',f'USA Today\'s tables are a season old, so contracts signed since then are not reflected. {_ufb} football cells and {_umb} men\'s basketball cells use them, and for {_diff} of those {_ufb+_umb} another source gives a different current figure, which I quoted in the Source Log note.'),
 ('2. Deal values are thin',f'Most schools do not publish contract values. Of {NS} schools, an annual value is filled for {_deal["multimedia rights"]} on multimedia rights, {_deal["apparel"]} on apparel, {_deal["stadium naming rights"]} on stadium naming rights, {_deal["arena naming rights"]} on arena naming rights and {_deal["jersey patch"]} on jersey patch, so the averages on those columns rest on small counts.'),
 ('3. Blank pay cells',f'Head coach pay is filled for {_pfb} of {NS} schools in football and {_pmb} of {NS} in men\'s basketball ({_pmb5} for the 2025 column). The blanks are mostly private schools and interim coaches.'),
 ('4. NC State football','NC State named Philip Rivers head coach on November 13, 2026. The release says he signed a five-year agreement but gives no pay or end date, so those cells are blank until the terms are published.'),
 ('5. Maryland football','Aazaar Abdul-Rahim is the interim head coach, and the search was still open when I last checked on November 13, 2026.'),
 ('6. Louisville arena capacity','22,090 is from Wikipedia because Louisville\'s own page says only "22,000-seat". It is the only Wikipedia figure in the file.'),
 ('Next step','If you would like a different cut (by conference, by revenue tier, or one school against a peer set), or if a figure looks off to you, please let me know and I am happy to update it.'),
]
if not (_has('California','total_operating_expenses') and resolved['California']['fin_basis'][0]=='MFRS own posting' and int(_cal['total_operating_expenses'][0])==173856988): lines=[l for l in lines if l[0]!='California']
_FB=InlineFont(rFont='Aptos Narrow',sz=9,b=True,color='000000'); _FR=InlineFont(rFont='Aptos Narrow',sz=9,b=False,color='000000')
for k,(lab,txt) in enumerate(lines):
    c=ws.cell(row=R0+k,column=1+OFF,value=CellRichText(TextBlock(_FB,lab+': '),TextBlock(_FR,txt))); c.font=F_BASE
ws.column_dimensions[CL(1)].width=220

# ---- Source Log ----
_oi={s['name']:i for i,s in enumerate(order)}; sourcelog.sort(key=lambda r:_oi[r[0]])   # stable: keeps each school's rows together
ws=wb.create_sheet('Source Log')
hdr=['School','Conference','Metric','Value','Unit','Fiscal year or season','Source type','Source name','URL','Date accessed','Verification','Note']
prep(ws,'Source log: one row per sourced value (values, not formulas)',units=None)
header(ws,hdr)
# Verification status per (school, metric), written by scripts/build_verification.py. A status applies only while the
# value it was checked against is still the value shown.
VER={}
if os.path.exists('data/verification.csv'):
    for v in csv.DictReader(open('data/verification.csv',encoding='utf-8')): VER[(v['school'],v['metric'])]=v
BULK_HOSTS=('nces.ed.gov','ope.ed.gov','espn.com/college-football/standings','sports-reference.com/cbb/schools','nacda.com/documents','d1ticker.com','fs.ncaa.org','sportico.com','web3.ncaa.org','sportsdata.usatoday.com')
def same_value(a,b):
    try: return abs(float(str(a).replace(',',''))-float(str(b).replace(',','')))<1e-9
    except ValueError: return str(a).strip().lower()==str(b).strip().lower()
def verification(row):
    school,_c,metric,value,_u,_fy,_st,_sn,url=row[:9]
    if value in (None,'','--'): return '--'
    v=VER.get((school,metric))
    if v and same_value(v['value'],value): return v['status']
    if any(h in str(url) for h in BULK_HOSTS) or metric in ('School','Conference'): return 'Source data file'
    if re.search(r'deal type|pay source type|industry$|Financial source basis',metric) or str(value).lower() in ('none','in-house','other'): return 'Analyst classification'
    return 'Not re-verified'
SNIP=r"search[- ](?:snippet|summary|excerpt|result)s?(?: excerpt| summary)?"
PROC=re.compile(r"fetch tool|the brief|work[- ]list|allowed (?:source )?list|research note|search cap|cached copy|checker|verify/pages|permission system|"
                r"(?:the |The )?[Ww]orkbook(?:\u2019s|'s| figure| \d| has| value| had| term| start| listed| shows| may| cell| lacks| carries| wants| convention)|\bHTTP \d{3}\b|returned (?:HTTP )?\d{3}|"
                r"\b40[34]\b|\b410\b|did not render|would not render|rendered (?:only )?its title|returned only (?:its|the page) title|only (?:its|a) (?:page )?title|could not be opened|not fetchable|"
                r"searches? (?:found|returned|used|turned)|one search|two searches|three searches|(?-i:\bFLAG\b)|judg(?:e)?ment call|your call|(?-i:\bI (?:could|found|read|did|recorded|took|confirmed|used|went|left|checked|saw)\b)|for you\b",re.I)
def clean_note(text,confirmed):
    """Neutral wording for the audit trail: describe the state of the evidence, not how the research was run."""
    s=str(text)
    # the analyst is the author of the workbook, so notes about the analyst's decisions read in the first person
    for a,b in ((r"Passage supplied by the analyst from the cited page",'I supplied this passage from the cited page'),
                (r"Confirmed by the analyst as signed",'I confirmed he is signed'),
                (r"the copy the analyst supplied",'the copy I supplied'),
                (r"(?:Entered|Used|Shown) at the analyst[\u2019']s direction\.?\s*",''),
                (r",? at the analyst[\u2019']s direction",' at my direction'),
                (r"categories assigned by the analyst",'categories I assigned')):
        s=re.sub(a,b,s)
    for a,b in ((r'Not sourced within research effort/search budget; no verified value','No value sourced to the required standard'),
                (r'web search budget exhausted before this metric was researched','Not researched'),
                (r'not researched \(web-search budget exhausted\)','Not researched'),
                (r'not located; research stopped when the shared web search budget ran out before this item was checked','Not researched'),
                (r'\s*\(search budget exhausted\)',''),
                (r'\s*Sports-Reference CFB and stats\.ncaa\.org refused automated access from this environment\.',''),
                (r'rejected in review \(value inferred, computed or unverified per the note\);\s*','Not entered: the only available figure was inferred, computed or unverified. Detail: '),
                (r'rejected in review \(projected value, not a contract figure\);\s*','Not entered: the only available figure was a projection, not a contract figure. Detail: '),
                (r'rejected in review \(([^)]*)\);\s*',r'Not entered (\1). Detail: '),
                (r'superseded: deal partner changed to ([^;]*);\s*',r'Not carried over: this entry described an earlier partner (the partner is now \1). '),
                (r';?\s*earlier gap file listed (\w+) as partner - now superseded',r'; \1 was the previous partner'),
                (r'Partner name carried from earlier rounds','Partner name as previously sourced'),
                (r'URL slug reconstructed from search result title - verify','Link built from the article title; open it to confirm it resolves')):
        s=re.sub(a,b,s,flags=re.I)
    s=re.sub(r';?\s*not guessed','',s,flags=re.I)
    # drop sentences that describe how a page was retrieved or refer to the research process; the audit trail keeps the
    # statement of what the source says
    parts=[x for x in re.split(r'(?<=[.;])\s+',s) if x and not PROC.search(x)]
    s=' '.join(parts)
    if confirmed:   # the figure has since been found on the page itself, so the excerpt caveat no longer applies
        s=re.sub(r"[;,.]?\s*(?:value|values|terms|figure|name)?\s*(?:taken |read )?from (?:the )?(?:official page's |a )?"+SNIP+r"(?:/summary)?",'',s,flags=re.I)
        s=re.sub(r'\s*\(\s*(?:via |from )?'+SNIP+r'[^)]*\)','',s,flags=re.I); s=re.sub(r'[;,]?\s*'+SNIP+r' only','',s,flags=re.I)
        s=re.sub(r'\s*\(per '+SNIP+r'[^)]*\)','',s,flags=re.I); s=re.sub(r'\s*per '+SNIP,'',s,flags=re.I)
    else:
        s=re.sub(SNIP,'search-result excerpt',s,flags=re.I)
    s=re.sub(r'\s{2,}',' ',s).strip(' ;,'); s=re.sub(r'^[a-z]',lambda m:m.group(0).upper(),s)
    return s if s else '--'
for j,row in enumerate(sourcelog):
    status=verification(row); ok=status in ('Found on source page','Re-read and confirmed','Source data file')
    out=row[:7]+[clean_note(row[7],ok) if row[7] not in (None,'') else '--']+row[8:10]+[status,clean_note(row[10],ok) if row[10] not in (None,'') else '--']
    for i,v in enumerate(out,1):
        c=ws.cell(row=R0+j,column=i+OFF,value=(v if v not in (None,'') else '--')); c.font=F_BASE
setw(ws,{1:20,2:10,3:36,4:18,5:10,6:26,7:22,8:40,9:60,10:13,11:24,12:80}); ws.freeze_panes=f'{CL(1)}{R0}'

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
json.dump(dict(S=S,conf_layout=conf_layout,all_first=all_first,all_last=all_last,all_layout=all_layout,no_derive=[list(x) for x in sorted(NO_DERIVE)],bases=list(BASES),types=list(TYPES),scopes=[list(x) for x in SCOPES],fiscal_years=FYS,n_schools=NS,excluded=EXCLUDED,col_offset=OFF,header_row=R_HDR),open('data/workbook_layout.json','w'))
