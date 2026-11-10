"""Flatten the Sportico College Sports Finances Database data files (data/sportico/*.json) into one CSV and one XLSX:
every school, every fiscal year, every line item. Totals rows carry the six columns of the database view
(Football, Men's Basketball, Women's Basketball, Other Sports, Non-Program Specific, Total)."""
import json, glob, csv, re, openpyxl
from openpyxl.styles import Font
data={}
for f in sorted(glob.glob('data/sportico/json*.json')):
    txt=open(f,encoding='utf-8').read(); txt=txt[txt.index('['):].rstrip().rstrip(';')
    for obj in json.loads(txt):
        for school,years in obj.items():
            for yr,sections in years.items(): data.setdefault(school,{}).setdefault(yr,{}).update(sections)
def num(v):
    if v is None or v=='' or isinstance(v,list): return None
    if isinstance(v,(int,float)): return v
    s=str(v).replace('$','').replace(',','').strip(); neg=s.startswith('-') or (s.startswith('(') and s.endswith(')')); s=s.strip('()-')
    try: x=float(s); x=int(x) if x==int(x) else x; return -x if neg else x
    except: return v
cols=['school','fiscal_year','section','line_item','football','mens_basketball','womens_basketball','other_sports','non_program_specific','total','value']
rows=[]
for school in sorted(data):
    for yr in sorted(data[school]):
        for section,content in data[school][yr].items():
            if not isinstance(content,dict): continue
            for item,v in content.items():
                if item.strip()=='' : continue
                if section=='Totals' and isinstance(v,list) and len(v)==6:
                    rows.append([school,int(yr),section,item.strip()]+[num(x) for x in v]+[None])
                elif section=='Totals' and isinstance(v,list) and v==[]: continue
                else:
                    rows.append([school,int(yr),section,item.strip(),None,None,None,None,None,None,num(v)])
with open('data/sportico/sportico_database_flat.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(cols); w.writerows(rows)
wb=openpyxl.Workbook(); ws=wb.active; ws.title='Sportico database'
ws.append(cols)
for c in ws[1]: c.font=Font(name='Arial',size=10,bold=True)
for r in rows: ws.append(r)
ws.append([]); 
wb.create_sheet('Read me').append(['Source: Sportico College Sports Finances Database, https://www.sportico.com/leagues/college-sports/2023/college-sports-finances-database-intercollegiate-1234646029/ (data files served from https://d3data.sportico.com/NCAADatabase/), downloaded 2026-11-10, unmodified values. Totals section columns follow the database view: Football, Men\'s Basketball, Women\'s Basketball, Other Sports, Non-Program Specific, Total. Numbers section holds the MFRS other reporting items (debt, endowments, capital expenditures). Revenues and Expenses sections are per-sport totals.'])
for sh in wb:
    for col in sh.columns: sh.column_dimensions[col[0].column_letter].width=24
    for row in sh.iter_rows():
        for c in row: c.font=Font(name='Arial',size=10,bold=c.font.bold)
wb.save('data/sportico/sportico_database_flat.xlsx')
print('rows',len(rows),'schools',len(data),'years',sorted({int(y) for s in data for y in data[s]}))
