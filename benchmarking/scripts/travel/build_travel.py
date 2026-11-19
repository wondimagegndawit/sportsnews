"""Road and neutral-site games for the 16 Big 12 schools (2024 football, 2024-25 basketball), the venue of each,
and an estimated travel distance. Writes data/travel/games.csv and data/travel/summary.csv.

Distance method: straight-line (great-circle) miles from the school's campus (IPEDS coordinates) to the venue city
(US Census 2024 place coordinates), doubled for the round trip. Consecutive away or neutral games in the same city with
no home game between them (a multi-game tournament) count as one trip. Road swings are not chained: each trip is
priced from campus and back."""
import json,glob,csv,math,re,collections
TEAMS={'Arizona':12,'Arizona State':9,'Baylor':239,'BYU':252,'Cincinnati':2132,'Colorado':38,'Houston':248,'Iowa State':66,'Kansas':2305,
       'Kansas State':2306,'Oklahoma State':197,'TCU':2628,'Texas Tech':2641,'UCF':2116,'Utah':254,'West Virginia':277}
PAGE={'football':'https://www.espn.com/college-football/team/schedule/_/id/{i}/season/2024','mbb':'https://www.espn.com/mens-college-basketball/team/schedule/_/id/{i}/season/2025',
      'wbb':'https://www.espn.com/womens-college-basketball/team/schedule/_/id/{i}/season/2025'}
GAME={'football':'https://www.espn.com/college-football/game/_/gameId/{g}','mbb':'https://www.espn.com/mens-college-basketball/game/_/gameId/{g}','wbb':'https://www.espn.com/womens-college-basketball/game/_/gameId/{g}'}
M={s['name']:s for s in json.load(open('data/schools_master.json'))}
HD={r['UNITID']:r for r in csv.DictReader(open('data/ipeds/extracted/HD2024.csv',encoding='utf-8-sig',errors='replace'))}
ORIG={s:(float(HD[M[s]['unitid']]['LATITUDE']),float(HD[M[s]['unitid']]['LONGITUD'])) for s in TEAMS}
GZ={}
for r in csv.DictReader(open('data/geo/2024_Gaz_place_national.txt',encoding='latin-1'),delimiter='\t'):
    r={k.strip():v.strip() for k,v in r.items()}
    nm=re.sub(r'\s+(city|town|village|borough|CDP|municipality|city and borough|metropolitan government \(balance\)|consolidated government \(balance\)|unified government \(balance\)|urban county|metro government \(balance\))$','',r['NAME'])
    nm=re.sub(r'\s*\(balance\)','',nm).strip()
    k=(nm.lower(),r['USPS'])
    if k not in GZ or float(r['ALAND'])>GZ[k][2]: GZ[k]=(float(r['INTPTLAT']),float(r['INTPTLONG']),float(r['ALAND']))
# venues outside the Census place list (coordinates from the venue's city)
EXTRA={('paradise island',''):(25.0866,-77.3233),('nassau',''):(25.0443,-77.3504),('lahaina','HI'):(20.8783,-156.6825),('cancun',''):(21.1619,-86.8515),
       ('honolulu','HI'):(21.3069,-157.8583),('st. thomas',''):(18.3381,-64.8941),('niceville','FL'):(30.5169,-86.4822),('uncasville','CT'):(41.4343,-72.1101),
       ('fort myers','FL'):(26.6406,-81.8723),('estero','FL'):(26.4381,-81.8068),('montego bay',''):(18.4762,-77.8939),
       ('maui','HI'):(20.8783,-156.6825),('saint thomas',''):(18.3381,-64.8941),('queens','NY'):(40.7282,-73.7949),('brooklyn','NY'):(40.6782,-73.9442),
       ('charlottetown',''):(46.2382,-63.1311),('george town',''):(19.2866,-81.3744)}
ALIAS={('st. louis','MO'):('st. louis','MO'),('saint louis','MO'):('st. louis','MO'),('nashville','TN'):('nashville-davidson','TN'),('louisville','KY'):('louisville/jefferson county','KY'),
       ('lexington','KY'):('lexington-fayette','KY'),('indianapolis','IN'):('indianapolis city','IN'),('athens','GA'):('athens-clarke county','GA'),('augusta','GA'):('augusta-richmond county','GA'),
       ('honolulu','HI'):('urban honolulu','HI'),('boise','ID'):('boise city','ID'),('macon','GA'):('macon-bibb county','GA'),('saint joseph','MO'):('st. joseph','MO')}
def geo(city,state,venue):
    c=(city or '').strip().lower(); s=(state or '').strip()
    for k in (ALIAS.get((c,s),(c,s)),(c,s)):
        if k in GZ: return GZ[k][:2],'Census 2024 place'
    for (ec,es),v in EXTRA.items():
        if ec==c and (es==s or es==''): return v,'venue city (manual)'
    return None,None
def miles(a,b):
    R=3958.8; la1,lo1,la2,lo2=map(math.radians,(a[0],a[1],b[0],b[1]))
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))
rows=[]; miss=collections.Counter()
for sp in ('football','mbb','wbb'):
    for s,i in TEAMS.items():
        d=json.load(open(f'data/travel/raw/{sp}_{i}.json'))
        evs=[e for e in d['events'] if e.get('seasonType',{}).get('name')=='Regular Season']
        for e in sorted(evs,key=lambda e:e['date']):
            c=e['competitions'][0]; me=next(x for x in c['competitors'] if str(x['team']['id'])==str(i)); opp=next(x for x in c['competitors'] if str(x['team']['id'])!=str(i))
            v=c.get('venue',{}); a=v.get('address',{}); neutral=bool(c.get('neutralSite')); ha='Neutral' if neutral else ('Home' if me['homeAway']=='home' else 'Away')
            note='; '.join(n.get('headline','') for n in c.get('notes',[]) if n.get('headline'))
            pt,how=geo(a.get('city'),a.get('state'),v.get('fullName'))
            if ha!='Home' and not pt: miss[(a.get('city'),a.get('state'),v.get('fullName'))]+=1
            dist=round(miles(ORIG[s],pt)) if (pt and ha!='Home') else 0
            rows.append(dict(school=s,sport=sp,date=e['date'][:10],opponent=opp['team']['displayName'],site=ha,venue=v.get('fullName',''),city=a.get('city',''),state=a.get('state',''),
                             note=note,one_way_miles=dist if ha!='Home' else 0,trip_start='',round_trip_miles=0,geocode=how or '',game_url=GAME[sp].format(g=e['id']),schedule_url=PAGE[sp].format(i=i)))
# trips: consecutive away or neutral games in the same city, with no home game between, are one trip
for (s,sp),grp in collections.OrderedDict((k,None) for k in [(r['school'],r['sport']) for r in rows]).items():
    g=[r for r in rows if r['school']==s and r['sport']==sp]; prev=None
    for r in g:
        if r['site']=='Home': prev=None; continue
        key=(r['city'],r['state'])
        if prev and prev['key']==key: r['trip_start']='no (same trip as the game before)'; r['round_trip_miles']=0
        else: r['trip_start']='yes'; r['round_trip_miles']=2*r['one_way_miles']
        prev={'key':key}
with open('data/travel/games.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
S=[]
for s in TEAMS:
    for sp in ('football','mbb','wbb'):
        g=[r for r in rows if r['school']==s and r['sport']==sp]
        S.append(dict(school=s,sport=sp,games=len(g),home=sum(r['site']=='Home' for r in g),away=sum(r['site']=='Away' for r in g),neutral=sum(r['site']=='Neutral' for r in g),
                      trips=sum(r['trip_start']=='yes' for r in g),round_trip_miles=sum(r['round_trip_miles'] for r in g),schedule_url=PAGE[sp].format(i=TEAMS[s])))
with open('data/travel/summary.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=list(S[0])); w.writeheader(); w.writerows(S)
print('games',len(rows),'| away/neutral without coordinates:',dict(miss))
