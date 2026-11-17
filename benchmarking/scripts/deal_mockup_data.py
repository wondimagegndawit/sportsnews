"""Data for the deal slide mock-ups: each school with an annual value, plus a Sponsor line and a Terms line.
Usage: python3 -I scripts/deal_mockup_data.py > slides/spec_deal_mockups.json
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
 'Blue Cross and Blue Shield of Minnesota':'Blue Cross MN','Addition Financial Credit Union':'Addition Financial','Desert Financial Credit Union':'Desert Financial',"Jersey Mike's Subs":"Jersey Mike's",'Edward Jones (court logo)':'Edward Jones (logo)'}
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
TEXT={'Jersey patch':('JERSEY PATCH DEALS: ALL P4','Jersey patches are new sponsorship inventory generating multi-million-dollar deals for schools. While terms are often undisclosed, publicly reported deals average $10M annually'),
 'Stadium naming rights':('STADIUM NAMING RIGHTS: ALL P4','Stadium naming rights are long-term (10+ year) partnerships, often with local companies, and can include added investment for stadium upgrades.'),
 'Playing surface':('PLAYING SURFACE DEALS: ALL P4','Schools can keep a stadium or arena name and sell the playing surface instead, through naming rights to the football field or basketball court, or a paid logo on it.'),
 'Arena naming rights':('ARENA NAMING RIGHTS: ALL P4','Like stadium naming rights, arena naming rights are long-term partnerships that can include added investment for upgrades.')}
def entry(r,pre,sport=None):
    a=g(r,f'{pre} annual value')
    d=dict(school=ws.cell(r,3).value,logo=LOGO[ws.cell(r,3).value]['file'],value=a if num(a) else None,sponsor=SHORT.get(g(r,f'{pre} partner'),g(r,f'{pre} partner')),terms=terms(r,pre))
    if sport: d['sport']=sport
    return d
ALL=[r for r in range(7,ws.max_row+1) if ws.cell(r,3).value in LOGO]
out=[]
for pre in ('Jersey patch','Stadium naming rights','Playing surface','Arena naming rights'):
    if pre=='Playing surface':
        # every commercial deal on a field or court is listed, football first; a deal with no reported value gets no bar
        sch=[]
        for p2,sport in (('Field naming rights','Football'),('Court naming rights','Basketball')):
            rs=[r for r in ALL if str(g(r,f'{p2} deal type')).startswith('commercial')]
            rs.sort(key=lambda r:(not num(g(r,f'{p2} annual value')),-(g(r,f'{p2} annual value') if num(g(r,f'{p2} annual value')) else 0),ws.cell(r,3).value))
            sch+=[entry(r,p2,sport) for r in rs]
    else:
        rs=sorted((r for r in ALL if num(g(r,f'{pre} annual value'))),key=lambda r:-g(r,f'{pre} annual value')); sch=[entry(r,pre) for r in rs]
    vals=[x['value'] for x in sch if x['value'] is not None]
    out.append(dict(key=pre,title=TEXT[pre][0],subtitle=TEXT[pre][1],avg=statistics.mean(vals),med=statistics.median(vals),schools=sch))
json.dump(out,sys.stdout,indent=1)
