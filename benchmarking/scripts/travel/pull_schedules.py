"""Pull the 2024 football and 2024-25 men's and women's basketball schedules for the 16 Big 12 schools from ESPN's
public schedule feed (the same data as the ESPN team schedule pages). Saves the raw files in data/travel/raw.
Regular season only, which in ESPN's feed includes the Big 12 football championship game and the Big 12 basketball
tournaments; bowls and NCAA/NIT games sit in the post-season feed and are not pulled."""
import json,subprocess,os,time
TEAMS={'Arizona':12,'Arizona State':9,'Baylor':239,'BYU':252,'Cincinnati':2132,'Colorado':38,'Houston':248,'Iowa State':66,'Kansas':2305,
       'Kansas State':2306,'Oklahoma State':197,'TCU':2628,'Texas Tech':2641,'UCF':2116,'Utah':254,'West Virginia':277}
SPORTS={'football':('football/college-football',2024),'mbb':('basketball/mens-college-basketball',2025),'wbb':('basketball/womens-college-basketball',2025)}
for sp,(path,season) in SPORTS.items():
    for s,i in TEAMS.items():
        f=f'data/travel/raw/{sp}_{i}.json'
        if os.path.exists(f) and os.path.getsize(f)>1000: continue
        url=f'https://site.api.espn.com/apis/site/v2/sports/{path}/teams/{i}/schedule?season={season}'
        subprocess.run(['curl','-sS','-o',f,url],check=True); time.sleep(0.3)
        d=json.load(open(f)); assert d.get('requestedSeason',{}).get('year')==season,(s,sp)
        print(sp,s,len(d['events']))
