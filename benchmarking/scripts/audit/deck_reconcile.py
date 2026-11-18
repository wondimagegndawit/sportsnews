"""Reconcile the deck, the chart-data workbook, the slide specs and the benchmarking workbook.
For every chart: the numbers stored in the PowerPoint chart, the numbers on the chart-data tab and the numbers in the
slide spec are compared with the cells of the benchmarking workbook they come from, and the average and median on the
slide are recomputed from those cells."""
import json,zipfile,re,statistics,openpyxl,collections,sys
WB='Power4_Athletic_Department_Benchmarking.xlsx'; DECK='slides/P4_Benchmarking_Deck_Big12.pptx'; CD='slides/P4_Benchmarking_Chart_Data_Big12.xlsx'
wb=openpyxl.load_workbook(WB,data_only=True); ws=wb['All Schools']; H={ws.cell(6,c).value:c for c in range(3,ws.max_column+1)}
ROW={ws.cell(r,3).value:r for r in range(7,ws.max_row+1)}
def cell(s,h):
    v=ws.cell(ROW[s],H[h]).value; return v if isinstance(v,(int,float)) and not isinstance(v,bool) else None
spec=json.load(open('slides/spec_big12.json')); deals=json.load(open('slides/spec_deals.json'))
z=zipfile.ZipFile(DECK)
def chart_of(i):
    rel=z.read(f'ppt/slides/_rels/slide{i}.xml.rels').decode(); m=re.search(r'charts/(chart\d+\.xml)',rel)
    if not m: return None
    x=z.read('ppt/charts/'+m.group(1)).decode(); out=[]
    for ser in re.findall(r'<c:ser>.*?</c:ser>',x,re.S):
        nm=re.search(r'<c:tx>.*?<c:v>(.*?)</c:v>',ser,re.S); vals=re.search(r'<c:val>.*?</c:val>',ser,re.S)
        pts={int(a):float(b) for a,b in re.findall(r'<c:pt idx="(\d+)"><c:v>([^<]*)</c:v>',vals.group(0))} if vals else {}
        out.append((nm.group(1) if nm else '',[pts.get(k) for k in range(max(pts)+1)] if pts else []))
    return out
def text_of(i):
    x=z.read(f'ppt/slides/slide{i}.xml').decode(); return ' '.join(re.findall(r'<a:t>([^<]*)</a:t>',x)).replace('&amp;','&').replace('&apos;',"'")
cd=openpyxl.load_workbook(CD,data_only=True)
issues=[]; checked=collections.Counter()
def close(a,b,tol=0.5): return (a is None and b is None) or (a is not None and b is not None and abs(a-b)<=tol)
DEALHDR={'Jersey patch':'Jersey patch annual value','Stadium naming rights':'Stadium naming rights annual value','Field naming rights':'Field naming rights annual value','Arena naming rights':'Arena naming rights annual value','Court naming rights':'Court naming rights annual value','Logo deals':None}
# ---- deal pages (slides 1..6)
for i,d in enumerate(deals,1):
    ch=chart_of(i); nb=[x for x in (ch or []) if 'verage' not in x[0] and 'edian' not in x[0]]
    # a page with football and basketball bars stores them as two series; a bar is the non-zero value at its position
    bars=[max((x[1][k] or 0) for x in nb if k<len(x[1])) for k in range(max((len(x[1]) for x in nb),default=0))]
    vals=[s['value'] for s in d['schools'] if s.get('value') is not None]
    hdr=DEALHDR.get(d['key'])
    for s in d['schools']:
        if s.get('value') is None: continue
        h=hdr or (('Field' if s.get('sport','Football')=='Football' else 'Court')+' naming rights annual value')
        w=cell(s['school'],h); checked['deal bars against the workbook']+=1
        if not close(w,s['value']): issues.append(('DEAL VALUE',d['key'],s['school'],s['value'],w))
    if [round(v) for v in bars[:len(vals)]]!=[round(v) for v in vals]: issues.append(('DEAL CHART CACHE',d['key'],bars[:4],vals[:4]))
    checked['deal charts against the spec']+=1
    if vals and (not close(statistics.mean(vals),d['avg'],1) or not close(statistics.median(vals),d['med'],1)): issues.append(('DEAL AVG/MED',d['key'],statistics.mean(vals),d['avg'],statistics.median(vals),d['med']))
# ---- metric pages
metric=[s for s in spec['slides'] if s['key'] not in ('jersey_patch','stadium_naming','field_naming','arena_naming','court_naming','logo_deals')]
order=[s for s in metric if s.get('section')=='revenue']+[s for s in metric if s.get('section')=='expense']+[s for s in metric if s.get('section') not in ('revenue','expense')]
TAB=None
for k,s in enumerate(order):
    i=len(deals)+1+k; ch=chart_of(i); txt=text_of(i)
    names=[c['school'] for c in s['categories']]
    for j,ser in enumerate(s['series']):
        # 1. spec against the benchmarking workbook (first series is a workbook column; the 2024 capacity series comes from the saved D1.ticker page)
        if j==0 or s['key']=='fb_attendance':
            hdr=s['metric'] if j==0 else 'FB average home attendance 2024'
            for n,v in zip(names,ser['values']):
                checked['metric bars against the workbook']+=1
                if not close(cell(n,hdr),v,1e-6 if s['unit']=='pct' else 0.5): issues.append(('METRIC VALUE',s['key'],n,v,cell(n,hdr)))
        # 2. PowerPoint chart cache against the spec
        pv=ch[j][1] if ch and j<len(ch) else []
        if len(pv)!=len(ser['values']) or any(not close(a,b,1e-6 if s['unit']=='pct' else 0.5) for a,b in zip(pv,ser['values'])): issues.append(('PPT CHART CACHE',s['key'],j,pv[:3],ser['values'][:3]))
        checked['PowerPoint series against the spec']+=1
    # 3. average and median recomputed from the bars shown
    shown=[v for ser in s['series'] for v in ser['values'] if v is not None]
    if s['scope']=='conference':
        if not close(statistics.mean(shown),s['lines'][0]['value'],1e-6) or not close(statistics.median(shown),s['lines'][1]['value'],1e-6): issues.append(('AVG/MED',s['key']))
        lv=[ser[1][0] for ser in ch[len(s['series']):]] if ch else []
        if len(lv)<2 or not close(lv[0],s['lines'][0]['value'],1e-6 if s['unit']=='pct' else 0.5) or not close(lv[1],s['lines'][1]['value'],1e-6 if s['unit']=='pct' else 0.5): issues.append(('PPT AVG/MED LINES',s['key'],lv[:2]))
        checked['average and median recomputed']+=1
    # 4. completeness: every school of the conference that qualifies is on the chart
    if s.get('section') in ('revenue','expense') and s['key'] not in ('fb_hc_pay','mbb_hc_pay'):
        want=[n for n,r in ROW.items() if ws.cell(r,H['Conference']).value==spec['conference'] and ws.cell(r,H['Financial data type']).value=='MFRS' and ws.cell(r,H['Fiscal year']).value==2025 and cell(n,s['metric']) is not None and not (s['key']=='media_rights' and cell(n,s['metric'])==0)]
        if sorted(want)!=sorted(names): issues.append(('SCHOOLS SHOWN',s['key'],sorted(set(want)^set(names))))
        checked['school lists checked']+=1
    # 5. the title and subtitle on the slide are the spec's
    if s['title'].split(',')[0][:40] not in txt: issues.append(('SLIDE TEXT',s['key'],s['title'][:60]))
    # 6. chart-data workbook tab
    tab=next((t for t in cd.sheetnames if cd[t]['B3'].value and str(cd[t]['B3'].value).strip()==s['metric']),None) or next((t for t in cd.sheetnames if any(str(c.value).startswith('Slide title: '+s['title'][:50]) for row in cd[t].iter_rows(min_row=1,max_row=20) for c in row if c.value)),None)
    if not tab: issues.append(('NO CHART-DATA TAB',s['key'])); continue
    t=cd[tab]; hr=next(r for r in range(1,15) if t.cell(r,3).value=='School'); tn=[t.cell(hr,c).value for c in range(4,4+len(names))]
    if tn!=names: issues.append(('CHART-DATA SCHOOLS',s['key'],tn[:3],names[:3]))
    for j,ser in enumerate(s['series']):
        tv=[t.cell(hr+1+j,c).value for c in range(4,4+len(names))]; tv=[x if isinstance(x,(int,float)) else None for x in tv]
        if any(not close(a,b,1e-6 if s['unit']=='pct' else 0.5) for a,b in zip(tv,ser['values'])): issues.append(('CHART-DATA VALUES',s['key'],j,tv[:3],ser['values'][:3]))
        checked['chart-data rows against the spec']+=1
    if s['scope']=='conference':
        a=t.cell(hr+1+len(s['series']),4).value; m=t.cell(hr+2+len(s['series']),4).value
        if not close(a,s['lines'][0]['value'],1e-6 if s['unit']=='pct' else 0.5) or not close(m,s['lines'][1]['value'],1e-6 if s['unit']=='pct' else 0.5): issues.append(('CHART-DATA AVG/MED',s['key'],a,m))
print('slides in the deck:',len([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml',n)]),'| charts:',len([n for n in z.namelist() if re.match(r'ppt/charts/chart\d+\.xml',n)]),'| chart-data tabs:',len(cd.sheetnames))
print(dict(checked)); print('differences:',len(issues))
for x in issues: print('  ',x)
