"""Enrollment and endowment table for the 68 schools.
Enrollment: IPEDS fall 2024 headcount (2024-25 academic year), already in data/merged_values.csv.
Endowment, FY2025: NACUBO-Commonfund Study of Endowments, FY2025 market values (saved in data/endowment).
Endowment, FY2024: IPEDS Finance survey 2023-24, value of endowment assets at the end of the fiscal year (F1H02 public, F2H02 private).
Writes data/enrollment_endowment.csv."""
import csv,json,openpyxl
NAC_URL='https://edge.sitecorecloud.io/nacubo1-nacubo-prd-dc8b/media/Nacubo/Documents/EndowmentFiles/2025-NCSE-Endowment-Market-Values-for-US-and-Canadian-Institutions-FINAL.xlsx'
IPEDS_FIN={'f2324_f1a':'https://nces.ed.gov/ipeds/complete-data-files/F2324_F1A.zip','f2324_f2':'https://nces.ed.gov/ipeds/complete-data-files/F2324_F2.zip'}
M=json.load(open('data/schools_master.json')); MV={(r['school'],r['metric']):r for r in csv.DictReader(open('data/merged_values.csv',encoding='utf-8'))}
ws=openpyxl.load_workbook('data/endowment/2025-NCSE-Endowment-Market-Values.xlsx',data_only=True).active
NAC={str(r[1]):r for r in ws.iter_rows(min_row=6,values_only=True) if r[1] and isinstance(r[9],(int,float))}
IP={}
for f,col in (('f2324_f1a','F1H02'),('f2324_f2','F2H02')):
    for r in csv.DictReader(open(f'data/ipeds/extracted/{f}.csv',encoding='latin-1')):
        if r.get(col,'').strip(): IP[r['UNITID']]=(int(float(r[col])),f)
# schools whose endowment is reported for a system or for a parent foundation, so the figure is not comparable to a single campus
NOTE={'Texas A&M':"The IPEDS figure includes the Texas A&M University System and the Texas A&M Foundation, not the College Station campus alone; NACUBO reports the system total only.",
      'Colorado':"CU Boulder's endowment is held by the University of Colorado Foundation for all CU campuses; neither source reports a Boulder-only figure.",
      'LSU':"NACUBO reports only the LSU System total.",
      'Texas':"NACUBO reports UT Austin separately from the UT System; this is the Austin figure."}
out=[]
for s in M:
    n=s['name']; u=s['unitid']; nr=NAC.get(u); ip=IP.get(u)
    ug=MV.get((n,'undergrad_enrollment')); tt=MV.get((n,'total_enrollment'))
    note=NOTE.get(n,'')
    if not nr and n not in NOTE: note=(note+' ' if note else '')+"Not in the NACUBO FY2025 study (participation is voluntary)."
    out.append(dict(school=n,conference=s['conf'],unitid=u,
        undergrad=ug['value'] if ug else '--',total=tt['value'] if tt else '--',enroll_url=f'https://nces.ed.gov/collegenavigator/?id={u}',
        endow_fy25=int(round(nr[9]*1000)) if nr else '--',nacubo_entity=str(nr[2]).rstrip('*^§°£¶x ') if nr else '--',nacubo_url=NAC_URL,
        endow_fy24=ip[0] if ip else '--',ipeds_url=IPEDS_FIN[ip[1]] if ip else '',note=note or '--'))
with open('data/enrollment_endowment.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print('schools',len(out),'| NACUBO FY2025',sum(1 for r in out if r['endow_fy25']!='--'),'| IPEDS FY2024',sum(1 for r in out if r['endow_fy24']!='--'))
