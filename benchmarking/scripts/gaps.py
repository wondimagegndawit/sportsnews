"""Write the remaining research gaps (cells still '--') per conference as markdown briefs and one CSV."""
import csv, json, sys
from collections import defaultdict
master={s['name']:s for s in json.load(open('data/schools_master.json'))}
rows=list(csv.DictReader(open('data/merged_values.csv',encoding='utf-8')))
FIN=['fin_report_url','fin_fiscal_year','total_operating_revenue','total_operating_expenses','media_rights_revenue','ticket_sales_revenue','contributions_revenue','ncaa_distributions','conference_distributions','conference_bowl_distributions','direct_institutional_support','indirect_institutional_support','student_fees','coaching_salaries','athletics_related_debt','debt_service']
PAY={'fb_hc_annual_comp','fb_hc_contract_end','fb_hc_pay_source_type','mbb_hc_annual_comp','mbb_hc_contract_end','mbb_hc_pay_source_type'}
ORDER=['mmr_partner','mmr_start_year','mmr_term_years','mmr_annual_value','mmr_total_value','apparel_partner','apparel_start_year','apparel_term_years','apparel_annual_value','apparel_total_value',
 'stadium_nr_partner','stadium_nr_industry','stadium_nr_deal_type','stadium_nr_start_year','stadium_nr_term_years','stadium_nr_annual_value','stadium_nr_total_value',
 'arena_nr_partner','arena_nr_industry','arena_nr_deal_type','arena_nr_start_year','arena_nr_term_years','arena_nr_annual_value','arena_nr_total_value',
 'patch_partner','patch_industry','patch_start_year','patch_term_years','patch_annual_value','patch_total_value',
 'stadium_name','stadium_capacity','stadium_year_opened','stadium_last_renovation_year','arena_name','arena_capacity','arena_year_opened','varsity_sports',
 'fb_hc_name','fb_hc_annual_comp','fb_hc_contract_end','fb_hc_pay_source_type','mbb_hc_name','mbb_hc_annual_comp','mbb_hc_contract_end','mbb_hc_pay_source_type']+FIN
have=defaultdict(dict)
for r in rows:
    if r['value']!='--': have[r['school']][r['metric']]=r['value']
gaps={}
for sch,s in master.items():
    k=[m for m in ORDER if m not in have[sch] and not (s['control']=='Private' and (m in FIN or m in PAY))]
    for pre in ('stadium_nr','arena_nr','patch','mmr','apparel'):
        if have[sch].get(pre+'_partner','').lower()=='none': k=[m for m in k if not m.startswith(pre+'_')]
        if have[sch].get(pre+'_deal_type','').lower()=='honorific': k=[m for m in k if m not in (pre+'_industry',pre+'_start_year',pre+'_term_years',pre+'_annual_value',pre+'_total_value')]
    gaps[sch]=k
tag=sys.argv[1] if len(sys.argv)>1 else 'gaps4'
R='/tmp/claude-0/-home-user-sportsnews/13880bdf-16ac-52e7-abd6-56bf6c41826b/scratchpad/research'
with open('data/gaps_remaining.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['school','conference','public_or_private','state','metric','already_known_context'])
    for conf in ('ACC','Big Ten','Big 12','SEC'):
        for sch in sorted([s for s in master if master[s]['conf']==conf],key=str.lower):
            s=master[sch]
            ctx='; '.join(f"{m}={have[sch][m]}" for m in ('stadium_name','arena_name','fb_hc_name','mbb_hc_name','stadium_nr_partner','arena_nr_partner','patch_partner','mmr_partner','apparel_partner') if m in have[sch])
            for m in gaps[sch]: w.writerow([sch,conf,s['control'],s['state'],m,ctx])
for conf,t in [('ACC','acc'),('Big Ten','bigten'),('Big 12','big12'),('SEC','sec')]:
    with open(f'{R}/{tag}_{t}.md','w') as f:
        f.write(f'# Remaining gaps: {conf}\nOnly these cells are unsourced. Do not re-research anything else.\n\n')
        for sch in sorted([s for s in master if master[s]['conf']==conf],key=str.lower):
            s=master[sch]; k=gaps[sch]
            known={m:have[sch][m] for m in ('stadium_name','arena_name','fb_hc_name','mbb_hc_name','stadium_nr_partner','arena_nr_partner','patch_partner','mmr_partner','apparel_partner') if m in have[sch]}
            f.write(f"## {sch} ({s['control']}, {s['state']}) — {len(k)} cells\nAlready known: {known}\nCells: {', '.join(k)}\n\n")
    print(conf, sum(len(gaps[s]) for s in master if master[s]['conf']==conf))
print('total gaps', sum(len(v) for v in gaps.values()))
