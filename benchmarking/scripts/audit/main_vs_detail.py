"""Tie every financial column on the All Schools tab to the report detail (data/frs_detail.csv), for NCAA-report schools."""
import csv,openpyxl,collections
wb=openpyxl.load_workbook('Power4_Athletic_Department_Benchmarking.xlsx',data_only=True); ws=wb['All Schools']
H={ws.cell(6,c).value:c for c in range(3,ws.max_column+1)}
det={(r['school'],r['section'],r['line_id']):r for r in csv.DictReader(open('data/frs_detail.csv',encoding='utf-8'))}
MAP=[('Total operating revenue','Revenue','','total'),('Football revenue','Revenue','','football'),("Men's basketball revenue",'Revenue','','mens_basketball'),('Non-program-specific revenue','Revenue','','non_program'),
     ('Ticket sales revenue','Revenue','1','total'),('Licensing, advertising and sponsorship revenue','Revenue','15','total'),('Media rights revenue','Revenue','11','total'),('Contributions revenue','Revenue','8','total'),('Student fees','Revenue','3','total'),('Direct institutional support','Revenue','4','total'),
     ('Total operating expenses','Expense','','total'),('Total coaching salaries and benefits','Expense','22','total'),('Support and administrative staff pay','Expense','24','total'),('Team travel','Expense','28','total'),('Team travel: football','Expense','28','football'),
     ("Team travel: men's basketball",'Expense','28','mens_basketball'),("Team travel: women's basketball",'Expense','28','womens_basketball'),('Fundraising, marketing and promotion','Expense','31','total'),('Student-athlete meals','Expense','39','total'),('Annual debt service','Expense','34','total')]
bad=n=0; fy=collections.Counter()
for r in range(7,ws.max_row+1):
    s=ws.cell(r,3).value
    if (s,'Revenue','') not in det and (s,'Revenue','1') not in det: continue
    fy[(ws.cell(r,H['Fiscal year']).value,det.get((s,'Revenue','1'),{}).get('fiscal_year'))]+=1
    for hdr,sec,lid,col in MAP:
        v=ws.cell(r,H[hdr]).value; d=det.get((s,sec,lid)); n+=1
        dv=int(d[col]) if d else None
        if v!=dv and not (v in ('--',None) and dv is None): bad+=1; print('MISMATCH',s,'|',hdr,'| main tab',v,'| detail',dv)
print('schools by (main tab year, detail year)',dict(fy)); print('cells compared',n,'| mismatches',bad)
