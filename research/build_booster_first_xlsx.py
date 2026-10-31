import csv, re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

SRC='/home/user/sportsnews/research/Smash_Booster_Connection_Map_v2.csv'
OUT='/home/user/sportsnews/research/Smash_Booster_Connection_Map_v3_booster_first.xlsx'
raw=list(csv.reader(open(SRC,encoding='utf-8')))
COLS=raw[0]
rows=[dict(zip(COLS,r)) for r in raw[1:] if r[0] in ('1','2','3','Untiered')]

# Orchestrator classification of every connection row (index = position in rows). DROP = path runs through the target school.
DROP = {3,5,15,19,20,22,23,24,28,29,30,32,33,35,36,37,40,43,46,47,48,49,50,51,52,53,54,55,59,60,72,73,76,78,82,83,86,87,93,95,99,100,101,102,108,111,112,121,129,130,135,138,156,158,159,162,168,169,174,188,194,196,197,206,224,229,230,232,233,234,236,250,251,252}
REASON = {
 3:'Bridge is Arizona athletics administrators / AD Reed-Francois', 5:'Bridge is Arizona AD Reed-Francois', 15:'Bridge is Arizona AD Reed-Francois',
 19:'Bridge is UA President Garimella', 20:'Path routes via UA President Garimella / AD Reed-Francois', 22:'Bridge is Arizona AD Reed-Francois', 23:'Bridge is Arizona AD Reed-Francois', 24:'Bridge is Arizona athletics (AD office)',
 28:'Bridge is Clemson AD Neff / Clemson administration', 29:'Bridge is Clemson AD Neff / IPTAY CEO', 30:'Bridge is Clemson AD Neff', 32:'Bridge is Clemson AD Neff', 33:'Bridge is Clemson AD Neff',
 35:'Bridge is K-State AD Gene Taylor', 36:'Bridge is K-State AD Gene Taylor', 37:'Bridge is K-State President Linton / KSU Foundation CEO',
 40:'Bridge is LSU President Rousse', 43:'Bridge is LSU President Rousse', 46:'Bridge is LSU President Rousse / board chair Mallett',
 47:'Bridge is Louisville AD Heird', 48:'Bridge is Louisville AD Heird',
 49:'Bridge is UNC AD Cunningham / Chancellor Roberts', 50:'Bridge is UNC AD Cunningham / Chancellor Roberts / AD Newmark', 51:'Bridge is UNC AD Cunningham / Chancellor Roberts', 52:'Bridge Dean Stoyer is a UNC vice chancellor', 53:'Bridge is UNC AD Cunningham', 54:'Bridge is UNC AD Cunningham / AD Newmark', 55:'Approach led through UNC athletics',
 59:'Bridge is Virginia Tech AD Emeritus Babcock / AD White', 60:'Bridge is Virginia Tech AD White / Babcock',
 72:'Bridge is NC State AD Corrigan', 73:'Bridge is NC State AD Corrigan',
 76:'Bridge Thomas Burish is a sitting SMU trustee', 78:'Bridge John Waldron is a sitting SMU trustee', 82:'Bridge is SMU President Hartzell',
 83:'Bridge is Auburn athletics administrators / AD Cohen', 86:'Path ends through Auburn Sports Properties GM and AD Cohen', 87:'Bridge is Auburn President Roberts',
 93:'Bridge is Florida AD Stricklin', 95:'Bridge is Florida AD Stricklin', 99:'Bridge is Florida administrators / AD Stricklin',
 100:'Bridge Mitch Barnhart remains on UK payroll (donor relations) / President Capilouto', 101:'Path runs through UK Champions Blue board chaired by President Capilouto', 102:'Bridge Mitch Barnhart remains on UK payroll / Capilouto',
 108:'Bridge is Syracuse Chancellor Haynie', 111:'Bridge Steven Barnes is Syracuse trustees vice chair, routed via Chancellor Haynie / athletics development', 112:'Same Barnes / Haynie route',
 121:'Bridge is Arkansas AD Yurachek', 129:'Bridge is Boston College AD Blake James', 130:'Bridge is UC President Pinto',
 135:'Bridge is FSU athletics leadership / Seminole Boosters CEO', 138:'Bridge is Georgia AD Josh Brooks',
 156:'Bridge is Miami Athletics (BHV client contacts)', 158:'Bridge is Miami Athletics (BHV client contacts)', 159:'Bridge is Miami athletics contacts',
 162:'Bridge is Michigan AD Warde Manuel / Champions Circle', 168:'Bridge is UMN advancement / AD Coyle', 169:'Bridge is UMN / Carlson leadership',
 174:'Bridge is Nebraska Foundation / Husker Athletics donor relations', 188:'Bridge is Ohio State AD Bjork / Buckeye Sports Group',
 194:'Bridge is Penn State AD Kraft / athletics', 196:'Bridge is Penn State AD Kraft', 197:'Bridge is Pitt AD Allen Greene',
 206:'Bridge is Stanford Athletics leadership', 224:'Bridge is Texas Tech AD Hocutt',
 229:'Bridge is USC AD Jen Cohen / USC trustee leadership', 230:'Bridge is USC AD Jen Cohen',
 232:'Bridge is Utah President Randall', 233:'Bridge is University of Utah advancement', 234:'Bridge is Utah President Randall / advancement',
 236:'Bridge is Vanderbilt Chancellor Diermeier\'s office / Board of Visitors',
 250:'Bridge is Wake Forest AD Currie', 251:'Bridge is Wake Forest AD Currie', 252:'Bridge is UW AD Pat Chun / Tyee Club',
}
FORMER = {25:'Dan Radakovich (left Clemson 2021; now FBS ADA)', 26:'Jim Clements (retired from Clemson Dec 2025)', 27:'Jim Clements (retired from Clemson Dec 2025)', 31:'Jim Clements (retired from Clemson Dec 2025)', 34:'Jim Clements (retired from Clemson Dec 2025)',
 39:'Scott Woodward (no longer LSU AD)', 90:'Rick George (retired from CU 2025)', 109:'John Wildhack (retired from Syracuse July 2026)', 110:'John Wildhack (retired from Syracuse July 2026)', 113:'Kent Syverud (left Syracuse chancellorship 2026)',
 141:'Fred Glass (former IU AD, now out of IU)', 155:'Dan Radakovich (retired as Miami AD June 2026)', 157:'Dan Radakovich (retired as Miami AD June 2026)', 190:'Joe Castiglione (retired as OU AD Jan 2026)', 257:'Barry Alvarez (retired as Wisconsin AD 2021)'}
# path clean-ups for kept rows that mentioned a school-side alternative
EDIT = {
 134:'Steve Pagliuca via One Vision Futures Fund co-officers Dan Levitan (Maveron) or Steve Duncker (ex-Goldman Sachs), who run the collective with Fox; do not route through Duke athletics.',
 170:'Gordon Gee via Vanderbilt/Owen alumni relations or Nashville civic circles (Gee was Vanderbilt chancellor; McKinnis is an Owen alumnus); do not route through Mississippi State athletics.',
 177:'Ndamukong Suh directly, as a fellow University of Nebraska Foundation trustee and Husker alumnus, so that Peed can then bring Nebraska athletics in.',
 190:'Jack Swarbrick asks Joe Castiglione (retired OU AD, AD peer) to introduce Brian Kimrey; do not route through current OU athletics staff.',
 199:'Jack Swarbrick directly (he hosted Brees as NBC\'s Notre Dame analyst in 2021); pair with Suh\'s direct NFL-peer approach.',
 227:'Chris Bevilacqua via his Rose Bowl / Tournament of Roses advisory contacts or Rose Bowl Legacy Foundation president Dedan Brozino (PrimeSport circle); do not route through UCLA athletics.',
 113:'Gordon Gee to former Chancellor Kent Syverud (co-authors of the 2024 Chronicle open letter), asking Syverud to introduce Lobdell personally rather than via Syracuse administration. Note Gee and Syverud publicly opposed a super league, so framing matters.',
 109:'Tom Staggs (or Kevin Mayer) to John Wildhack, now retired from Syracuse, as a fellow Disney/ESPN senior executive of the 2015-16 era; Wildhack to Lobdell personally.',
 110:'Kevin Mayer to John Wildhack (Disney/ESPN alumni network; Wildhack retired from Syracuse July 2026), then Wildhack to Lobdell personally.',
 25:'Jack Swarbrick asks Dan Radakovich (former Clemson AD, now FBS ADA executive director, LEAD1 colleague) for a personal introduction to Hendrix, whose cornerstone gift Radakovich designed; do not route through IPTAY or current Clemson staff.',
}
keep=[]; removed=[]
for i,r in enumerate(rows):
    r=dict(r)
    if r['Smash Team Member']=='--':
        keep.append(r); continue
    if i in DROP:
        r['Reason removed']=REASON.get(i,'Path runs through the target school')
        removed.append(r); continue
    if i in EDIT: r['Suggested warm intro path']=EDIT[i]
    if i in FORMER and 'former official' not in r['Suggested warm intro path']:
        r['Suggested warm intro path']+=f" Note: the bridge, {FORMER[i]}, is a former official who no longer works for the school, so the path does not ask the school for the introduction."
    keep.append(r)

# Re-route Dawit rows: lead must be a Smash member with a KEPT path for that target
CONF={'Confirmed':0,'Strong inference':1,'Hypothesis':2}
by_t={}
for r in keep: by_t.setdefault((r['Tier'],r['School'],r['Target Name']),[]).append(r)
for k,rs in by_t.items():
    others=sorted([r for r in rs if r['Smash Team Member'] not in ('Dawit Wondimagegn','--')], key=lambda r:CONF.get(r['Confidence'],9))
    for r in rs:
        if r['Smash Team Member']=='Dawit Wondimagegn':
            p=r['Suggested warm intro path']
            ctx=p.split('warm the approach:')[-1].strip() if 'warm the approach:' in p else p
            if 'insight' in (r['Connection Detail']+p).lower(): lead,why='Evan Richter',"as Co-Managing Partner, a software-PE peer and Dawit's former Insight Partners colleague"
            elif others: lead,why=others[0]['Smash Team Member'],f"as the Smash member with the strongest booster-first path to this target ({others[0]['Connection Type']}, {others[0]['Confidence']})"
            else: lead,why='Evan Richter',"as Co-Managing Partner and Dawit's former Insight Partners colleague (no other booster-first path exists for this target)"
            r['Suggested warm intro path']=f"{lead} leads the outreach, {why}; Dawit Wondimagegn should not be the point of contact. Use his overlap only as background to warm the approach: {ctx}"

# Targets that lost every connection row
all_t={}
for r in rows: all_t.setdefault((r['Tier'],r['School'],r['Target Name']),r)
for k,r0 in all_t.items():
    if k not in by_t:
        keep.append({**{c:r0[c] for c in COLS}, 'Smash Team Member':'--','Connection Type':'--','Confidence':'--',
                     'Connection Detail':'No booster-first path found. Every documented connection to this target runs through the school (see the Removed tab); approaching the booster would require a cold or new outside intermediary.',
                     'Source URL or LinkedIn observation':'See Removed (school-side paths) tab for the sources checked.','Suggested warm intro path':'--'})
TIER={'1':0,'2':1,'3':2,'Untiered':3}
order={}
for r in rows: order.setdefault((r['Tier'],r['School']),len(order))
keep.sort(key=lambda r:(TIER[r['Tier']],order[(r['Tier'],r['School'])],r['Target Name'],CONF.get(r['Confidence'],9)))
removed.sort(key=lambda r:(TIER[r['Tier']],order[(r['Tier'],r['School'])],r['Target Name'],CONF.get(r['Confidence'],9)))

TOP=[("1. Bruce Arians","Virginia Tech (Tier 1)","Ndamukong Suh","Confirmed: Arians was Suh's head coach for all three Buccaneers seasons (2019-21) including Super Bowl LV; Suh can call him directly."),
 ("2. Tilman Fertitta","Houston (Tier 2)","Gordon Gee, then Ndamukong Suh and Steve Pagliuca","Confirmed: Fertitta personally hosted Gee's 2015 UH visit; Suh was a named FAST Acquisition advisor on the 2021 Fertitta merger; Pagliuca shared the NBA Board of Governors with Fertitta 2017-25. All direct or via outside intermediaries (Doug Jacob)."),
 ("3. Chris Ackerley","Arizona (Tier 1)","Chris Bevilacqua, then Tom Staggs","Confirmed: both named selling CSTV stockholders in CBS's 2006 SEC filing; Staggs via Ackerley's ESH Acquisition co-directors Al Weiss and Thomas Wolber (ex-Disney Parks). Background only: Dawit's Lakeside School tie and nine LinkedIn mutuals."),
 ("4. Arte Moreno","Arizona (Tier 1)","Tom Staggs, then Gordon Gee via Ken Kendrick","Strong inference: Staggs certified the 2003 Disney 10-Q disclosing the Angels sale to Moreno; Kendrick (WVU benefactor Gee knows directly) sits with Moreno on the Baseball Hall of Fame board."),
 ("5. David Miller","SMU (Tier 2)","Jack Swarbrick via ACC Commissioner Jim Phillips; Gordon Gee via Oliver Luck","Strong inference: Miller negotiated SMU's ACC entry face-to-face with Phillips (Swarbrick's CFP Management Committee colleague, reported open to the Smash model); Luck, Miller's realignment consultant, reported to Gee at WVU in 2014. Neither bridge is SMU."),
 ("6. Joe Craft","Kentucky (Tier 3)","Kitchy Cook via Sen. Ted Cruz's office","Strong inference: Cruz endorsed and campaigned with Kelly Craft in 2023 and Alliance Resource money flowed to Cruz; a political, not university, route."),
 ("7. John Condos","LSU (Tier 1)","Evan Richter and Kevin Mayer via Gov. Jeff Landry","Strong inference: Landry appointed Condos to the LSU board, has received $150K+ from him and publicly backs the Smash plan; the governor, not LSU, is the bridge."),
 ("8. Bill Heavener","Florida (Tier 3)","Joey Smith via the Romney 2012 Florida finance network","Strong inference: Heavener was a Romney Florida finance co-chair while Smith ran candidate advance; fellow co-chair Mori Hosseini is a named route."),
 ("9. Jeff Crawford","Colorado (Tier 3)","Kevin Mayer via Gordon Crawford / Paley Center; Gordon Gee directly","Strong inference: the Crawford Family Foundation (Jeff is treasurer) is an annual Paley donor where Mayer is a trustee and Gordon Crawford trustee emeritus; Gee was CU president when Jeff graduated and can go direct."),
 ("10. Cody Campbell","Texas Tech (untiered)","Joey Smith; Jack Swarbrick; Gordon Gee","Confirmed/Strong inference: Campbell's Saving College Sports retains Invariant (Smith's former firm) and is run by Cruz's ex-chief of staff; Campbell and Swarbrick sit on the same NCAA reform committee; Campbell and Gee shared the 2026 Sack Symposium program.")]

wb=Workbook(); ws=wb.active; ws.title='Connection Map (booster-first)'
HF=Font(name='Arial',bold=True,color='FFFFFF'); BF=Font(name='Arial',size=10); FILL=PatternFill('solid',fgColor='1F3864')
WRAP=Alignment(wrap_text=True,vertical='top')
def write(ws, cols, data, widths):
    ws.append(cols)
    for c in ws[1]: c.font=HF; c.fill=FILL; c.alignment=WRAP
    for r in data: ws.append([r.get(c,'') for c in cols])
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font=BF; c.alignment=WRAP
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    ws.freeze_panes='E2'; ws.auto_filter.ref=f"A1:{get_column_letter(len(cols))}{len(data)+1}"
W=[8,16,11,26,40,20,16,70,16,45,50]
write(ws,COLS,keep,W)
n=len(keep)+3
ws.cell(row=n,column=1,value='Ten warmest booster-first paths (ranked)').font=Font(name='Arial',bold=True,size=11)
for j,(a,b,c,d) in enumerate(TOP,1):
    for col,val in zip((1,2,4,8),(a,b,c,d)):
        cell=ws.cell(row=n+j,column=col,value=val); cell.font=BF; cell.alignment=WRAP
ws2=wb.create_sheet('Removed (school-side paths)')
write(ws2,COLS+['Reason removed'],removed,W+[45])
ws3=wb.create_sheet('Read Me')
notes=[
 'Smash Sports booster connection map, v3 (booster-first). Research only; no outreach was made. Built 2026-10-31.',
 'Purpose: reach boosters so they can help bring their school to the table. Therefore every path that would require the school itself (its AD, president, chancellor, sitting trustees, coaches, booster-club or foundation staff, or administrators briefed on Project Rudy) to introduce Smash to the booster has been removed from the main tab and placed on the Removed tab with the reason.',
 'Kept: connections where a Smash member reaches the booster directly, or through an intermediary outside the school (conference commissioners, governors and political networks, business partners and co-directors, family members, sponsors/vendors, co-investors, Dawit\'s LinkedIn mutuals as background). Former school officials who have fully left the school (e.g., Jim Clements, Dan Radakovich, Scott Woodward, Rick George, John Wildhack, Fred Glass, Barry Alvarez, Joe Castiglione) are kept and labelled, since asking them does not ask the school.',
 'Dawit Wondimagegn is never the point of contact; where his LinkedIn mutuals or affiliations are the connection, the row names the senior Smash member with the strongest remaining booster-first path as lead.',
 'Row order: Tier (1, 2, 3, untiered), then school in the original target-list order, then target, then confidence. All rows for a school are contiguous. Targets with no remaining booster-first path carry one row saying so.',
 'Confidence: Confirmed = both people named in the same document or a direct quote about the other person; Strong inference = each side separately documented in the same organisation, deal or role at overlapping times, or a second-degree path with both edges documented and the bridge named; Hypothesis = a documented but unverified overlap.',
 'Sources: every row carries a URL or a LinkedIn observation (Polar Browser pass, 2026-10-28). Rows noting a "prior pass" read cite a source (SBJ, Forbes, On3, Senate PDFs) that could not be re-opened in this pass. Chris Bevilacqua\'s reported College Sports Tomorrow membership could not be independently confirmed, so rows depending on it are Hypothesis.',
 f'Counts: main tab {len([r for r in keep if r["Smash Team Member"]!="--"])} connection rows across {len(set((r["Tier"],r["School"],r["Target Name"]) for r in keep))} targets ({len([r for r in keep if r["Smash Team Member"]=="--"])} with no booster-first path); Removed tab {len(removed)} rows.',
]
for i,t in enumerate(notes,1):
    c=ws3.cell(row=i,column=1,value=t); c.font=BF; c.alignment=WRAP
ws3.column_dimensions['A'].width=140
wb.save(OUT)
import collections
print('kept',len(keep),'removed',len(removed),'targets',len(set((r['Tier'],r['School'],r['Target Name']) for r in keep)))
print('kept conf',collections.Counter(r['Confidence'] for r in keep))
print('no-path targets',[r['Target Name'] for r in keep if r['Smash Team Member']=='--' and 'booster-first' in r['Connection Detail']])
