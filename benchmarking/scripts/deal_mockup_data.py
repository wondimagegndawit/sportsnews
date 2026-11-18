"""Data for the deal slides of the benchmarking deck: each school with an annual value, plus a Sponsor line and a Terms line.
Usage: python3 -I scripts/deal_mockup_data.py > slides/spec_deals.json
Terms show the length and the total value; where the total is not reported it is annual value times term, as in the
workbook. Where a term is not a whole number of years the stated end year is shown instead."""
import json, sys, statistics, openpyxl
wb=openpyxl.load_workbook('Power4_Athletic_Department_Benchmarking.xlsx',data_only=True)
ws=wb['All Schools']; H={ws.cell(6,c).value:c for c in range(3,ws.max_column+1)}
LOGO=json.load(open('slides/logos/logos.json'))
g=lambda r,h: ws.cell(r,H[h]).value
num=lambda v: isinstance(v,(int,float)) and not isinstance(v,bool)
SHORT={'JPMorganChase':'JPMorgan Chase','First Horizon Bank':'First Horizon','MSU Federal Credit Union':'MSU Federal CU','CommunityAmerica Credit Union':'Community America CU',
 'Mountain America Credit Union':'Mountain America CU','L&N Federal Credit Union':'L&N Federal CU','TDECU (Texas Dow Employees Credit Union)':'TDECU','SHI International Corp.':'SHI',
 'Blue Cross and Blue Shield of Minnesota':'Blue Cross MN','Addition Financial Credit Union':'Addition Financial','Desert Financial Credit Union':'Desert Financial',"Jersey Mike's Subs":"Jersey Mike's",'TQL (Total Quality Logistics)':'TQL'}
def money(v): 
    return '$'+f'{v/1e6:.2f}'.rstrip('0').rstrip('.')+'M'
def terms(r,pre):
    t,tot,a,ex=[g(r,f'{pre} {x}') for x in ('term (years)','total value','annual value','expires')]
    if num(t) and abs(t-round(t))<1e-6: length=f'{t:.0f} years'
    elif num(ex): length=f'Through {ex:.0f}'
    else: length='Term not disclosed'
    if ws.cell(r,3).value=='Notre Dame' and pre=='Jersey patch': value='$18M to $20M a year'
    elif str(g(r,f'{pre} partner')).startswith('Edward Jones'): value=f'{money(tot)} across 3 schools'   # one total shared by Duke, Oregon and North Carolina
    elif num(tot): value=f'{money(tot)} total'
    elif num(a): value=f'{money(a)} a year'
    else: value='Value not disclosed'
    return [length,value]
def entry(r,pre,sport=None):
    a=g(r,f'{pre} annual value')
    d=dict(school=ws.cell(r,3).value,logo=LOGO[ws.cell(r,3).value]['file'],value=a if num(a) else None,sponsor=SHORT.get(g(r,f'{pre} partner'),g(r,f'{pre} partner')),terms=terms(r,pre))
    if sport: d['sport']=sport
    return d
ALL=[r for r in range(7,ws.max_row+1) if ws.cell(r,3).value in LOGO]
def ranked(rs,pre): return sorted(rs,key=lambda r:(not num(g(r,f'{pre} annual value')),-(g(r,f'{pre} annual value') if num(g(r,f'{pre} annual value')) else 0),ws.cell(r,3).value))
def surface(pre,kind): return ranked([r for r in ALL if g(r,pre.split()[0]+' rights type')==kind],pre)
def words(n): return {1:'One',2:'Two',3:'Three',4:'Four',5:'Five',6:'Six',7:'Seven',8:'Eight',9:'Nine'}.get(n,str(n))
out=[]
def page(key,title,subtitle,sch,note=None):
    vals=[x['value'] for x in sch if x['value'] is not None]
    d=dict(key=key,title=title,subtitle=subtitle,avg=statistics.mean(vals),med=statistics.median(vals),schools=sch)
    if note: d['note']=note
    out.append(d)
for pre,title,sub in (('Jersey patch','JERSEY PATCH DEALS: ALL P4','Jersey patches are new sponsorship inventory generating multi-million-dollar deals for schools. While terms are often undisclosed, publicly reported deals average $10M annually'),
                      ('Stadium naming rights','STADIUM NAMING RIGHTS: ALL P4','Stadium naming rights are long-term (10+ year) partnerships, often with local companies, and can include added investment for stadium upgrades.')):
    page(pre,title,sub,[entry(r,pre) for r in ranked([r for r in ALL if num(g(r,f'{pre} annual value'))],pre)])
# field naming rights: the sponsor's name is on the football field and the stadium keeps its own name; deals without a value get no bar
f=surface('Field naming rights','Naming rights'); nv=sum(1 for r in f if num(g(r,'Field naming rights annual value')))
page('Field naming rights','FIELD NAMING RIGHTS: ALL P4',f"Field naming rights let a school keep its stadium name and still sign a long-term (10+ year) naming partner for the playing surface. {words(len(f))} Power 4 schools have one; {words(nv).lower()} have reported terms.",[entry(r,'Field naming rights') for r in f])
pre='Arena naming rights'
page(pre,'ARENA NAMING RIGHTS: ALL P4','Like stadium naming rights, arena naming rights are long-term partnerships that can include added investment for upgrades.',[entry(r,pre) for r in ranked([r for r in ALL if num(g(r,f'{pre} annual value'))],pre)])
c=surface('Court naming rights','Naming rights'); nv=sum(1 for r in c if num(g(r,'Court naming rights annual value')))
page('Court naming rights','COURT NAMING RIGHTS: ALL P4',f"Selling the name of the basketball court on its own is rare. {words(len(c))} Power 4 schools have a court naming partner, and {words(nv).lower()} {'has' if nv==1 else 'have'} reported terms.",[entry(r,'Court naming rights') for r in c])
# logo-only deals: a paid logo on the field or court, which keeps its own name; football first, then basketball
lg_all=[entry(r,'Field naming rights','Football') for r in surface('Field naming rights','Logo only')]+[entry(r,'Court naming rights','Basketball') for r in surface('Court naming rights','Logo only')]
# only deals with a reported value are charted; the rest are listed by sponsor under the chart
lg=[x for x in lg_all if x['value'] is not None]; rest=[x for x in lg_all if x['value'] is None]
def _group(xs):
    by={}
    for x in xs: by.setdefault(x['sponsor'],[]).append(LOGO[x['school']]['short'])
    return '; '.join(f"{sp} ({', '.join(sorted(ns))})" for sp,ns in sorted(by.items(),key=lambda kv:(-len(kv[1]),kv[0])))
nf=sum(1 for x in lg_all if x['sport']=='Football'); nb=len(lg_all)-nf
note=("No reported value, so not charted. Football fields: "+_group([x for x in rest if x['sport']=='Football'])+". Basketball courts: "+(_group([x for x in rest if x['sport']=='Basketball']) or 'none')
      +". One report puts the going rate for a logo on a major college football field at about $3.5M a year (Insurance Journal, 20 Aug 2026).") if rest else None
page('Logo deals','PLAYING SURFACE LOGO DEALS: ALL P4',f"Logo deals put a sponsor's mark on the field or court without renaming it. {len(lg_all)} are on record ({nf} football fields, {nb} basketball courts), and only Edward Jones' has a reported value: $34M over four years across Duke, North Carolina and Oregon, divided evenly here because the split is not public.",lg,note)
json.dump(out,sys.stdout,indent=1)
