"""Fetch NCAA APR (football, 2024-25) and GSR (cohort 2018 = 2024-25 release) search results for the 67 schools.
Saves raw JSON responses unmodified under data/ncaa/apr and data/ncaa/gsr."""
import json, re, subprocess, time, os, sys
BASE='https://web3.ncaa.org'
master=json.load(open('data/schools_master.json'))
def session(form_path, ck):
    if os.path.exists(ck): os.remove(ck)
    html=subprocess.run(['curl','-sS','-m','40','-c',ck,'-b',ck,BASE+form_path],capture_output=True,text=True).stdout
    tok=re.search(r'name="_csrf" content="([^"]*)"',html).group(1)
    return tok
def post(path, ck, tok, data, out):
    r=subprocess.run(['curl','-sS','-m','90','-c',ck,'-b',ck,'-H','X-CSRF-TOKEN: '+tok,'-H','X-Requested-With: XMLHttpRequest','-o',out,'-w','%{http_code}','--data',data,BASE+path],capture_output=True,text=True)
    return r.stdout
tok_a=session('/aprsearch/aprsearch','data/ncaa/apr_cookies.txt')
tok_g=session('/aprsearch/gsrsearch','data/ncaa/gsr_cookies.txt')
for s in master:
    org=s['apr_org']
    out=f'data/ncaa/apr/{org}_MFB_2025.json'
    if not (os.path.exists(out) and os.path.getsize(out)>50):
        code=post('/aprsearch/aprsearch','data/ncaa/apr_cookies.txt',tok_a,f'_csrf={tok_a}&academicYear=2025&schoolOrgId={org}&sportCode=MFB&conferenceOrgId=&state=&penaltyType=&postSeasonType=',out)
        print('APR',s['name'],code,os.path.getsize(out),flush=True); time.sleep(1)
    out=f'data/ncaa/gsr/{org}_all.json'
    if not (os.path.exists(out) and os.path.getsize(out)>50):
        code=post('/aprsearch/gsrsearch','data/ncaa/gsr_cookies.txt',tok_g,f'_csrf={tok_g}&cohortYear=&schoolOrgId={org}&sportCode=&conferenceOrgId=&state=',out)
        print('GSR',s['name'],code,os.path.getsize(out),flush=True); time.sleep(1)
print('DONE')
