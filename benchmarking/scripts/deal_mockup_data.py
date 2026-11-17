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
 'Blue Cross and Blue Shield of Minnesota':'Blue Cross MN','Addition Financial Credit Union':'Addition Financial','Desert Financial Credit Union':'Desert Financial',"Jersey Mike's Subs":"Jersey Mike's"}
def money(v): 
    return '$'+f'{v/1e6:.2f}'.rstrip('0').rstrip('.')+'M'
def terms(r,pre):
    t,tot,a,ex=[g(r,f'{pre} {x}') for x in ('term (years)','total value','annual value','expires')]
    if num(t) and abs(t-round(t))<1e-6: length=f'{t:.0f} years'
    elif num(ex): length=f'Through {ex:.0f}'
    else: length='Term not disclosed'
    if ws.cell(r,3).value=='Notre Dame' and pre=='Jersey patch': value='$18M to $20M a year'
    elif num(tot): value=f'{money(tot)} total'
    else: value=f'{money(a)} a year'
    return [length,value]
TEXT={'Jersey patch':('JERSEY PATCH DEALS: ALL P4','Jersey patches are new sponsorship inventory generating multi-million-dollar deals for schools. While terms are often undisclosed, publicly reported deals average $10M annually'),
 'Stadium naming rights':('STADIUM NAMING RIGHTS: ALL P4','Stadium naming rights are long-term (10+ year) partnerships, often with local companies, and can include added investment for stadium upgrades.'),
 'Arena naming rights':('ARENA NAMING RIGHTS: ALL P4','Like stadium naming rights, arena naming rights are long-term partnerships that can include added investment for upgrades.')}
out=[]
for pre in ('Jersey patch','Stadium naming rights','Arena naming rights'):
    rows=[r for r in range(7,ws.max_row+1) if ws.cell(r,3).value in LOGO and num(g(r,f'{pre} annual value'))]
    rows.sort(key=lambda r:-g(r,f'{pre} annual value')); vals=[g(r,f'{pre} annual value') for r in rows]
    out.append(dict(key=pre,title=TEXT[pre][0],subtitle=TEXT[pre][1],avg=statistics.mean(vals),med=statistics.median(vals),
        schools=[dict(school=ws.cell(r,3).value,logo=LOGO[ws.cell(r,3).value]['file'],value=g(r,f'{pre} annual value'),
                      sponsor=SHORT.get(g(r,f'{pre} partner'),g(r,f'{pre} partner')),terms=terms(r,pre)) for r in rows]))
json.dump(out,sys.stdout,indent=1)
