# Part E: SEC multimedia rights and apparel terms (second research pass of 18 Nov 2026).
_AUB=("Auburn Athletics release (17 Apr 2025)",'https://auburntigers.com/news/2025/4/17/auburn-playfly-sports-agree-to-new-10-year-multimedia-rights-partnership')
_AUBP=("Playfly Sports release (17 Apr 2025)",'https://www.playfly.com/post/auburn-and-playfly-sports-agree-to-new-10-year-multimedia-rights-deal-through-2034-35-academic-year')
_AUBN="Not entered: the release gives anticipated revenue, not a guaranteed fee (‘The total anticipated value of the partnership is expected to exceed $230M over the 10-year term.’; ‘average anticipated annual revenue in the new agreement set to exceed $23M – increasing to over $34M’)."
_UGA=("theScore, citing the Athens Banner-Herald (Jan 2017)",'https://www.thescore.com/ncaab/news/1217282')
_UGA2=("Athens Banner-Herald via Yahoo Sports (29 Oct 2026)",'https://sports.yahoo.com/articles/georgias-extended-deal-learfield-one-123325279.html')
_UGAX=" This agreement is in its last year in 2026-27. An extension announced in October 2026 runs through 2042 (‘Georgia extended its partnership with Learfield for 15 years.’; ‘The school isn't disclosing financial terms.’)."
_SC=("South Carolina Athletics release (16 Sep 2016)",'https://gamecocksonline.com/?p=39967')
_SCN="‘a new 10-year agreement with IMG as the exclusive multimedia rights holder’; ‘This deal will take effect on July 1, 2017.’ IMG College is now Learfield (Gamecock Sports Properties). The trustees amended the agreement on 23 April 2026; the amended terms are not public."
_FL=("Learfield release (25 Aug 2025)",'https://www.learfield.com/2025/08/florida-victorious-and-gators-sports-properties-announce-strategic-partnership-with-nicholas-air/')
_FLN="Gators Sports Properties, Learfield's local team, ‘is the exclusive multimedia rights holder for the University Athletic Association (UAA)’. The terms in force in 2026 are not reported; the last contract on record was extended on 1 July 2019 ‘for an additional six years’ with figures withheld (Sportico, 27 Jul 2022)."
_MO=("Learfield, Missouri Tigers partner page",'https://www.learfield.com/partner/missouri-tigers/')
_MON="‘As the exclusive athletics multimedia rights holder, Mizzou Sports Properties manages all aspects of the rights relationship’. No report of the agreement's start, length or value was located."
_ALA=("OutKick (12 May 2021), citing AL.com",'https://www.outkick.com/nike-playing-hardball-with-alabama-gear-contract-could-cost-in-longrun/')
_ALAN="The last contract on record has ended: ‘Alabama's deal, which runs through 2025, is worth $63 million in apparel and cash, plus a $5 million signing bonus’. Nike is still the outfitter (Nike release, 8 Sep 2026: ‘the university's three-decade, all-sports partnership with Nike’), but the terms of the agreement in force in 2026 are not reported."
_MSU=("247Sports (2025)",'https://247sports.com/college/mississippi-state/article/mississippi-state-adidas-contract-sports-uniforms-252618104/')
_MSUN="‘While terms of the deal are not known at this time, the current deal runs until 2030.’ The start of the extension and its value are not reported."
ROWS_E=[
('Auburn','mmr_partner','Playfly','2025-26 to 2034-35',*_AUB,"Auburn Sports Properties is run by Playfly Sports: ‘a 10-year multimedia rights agreement that will extend their successful partnership through the 2034-35 academic year.’ (Playfly release, 17 Apr 2025)"),
('Auburn','mmr_term_years',10,'2025-26 to 2034-35',*_AUBP,"‘a 10-year multimedia rights agreement that will extend their successful partnership through the 2034-35 academic year.’"),
('Auburn','mmr_start_year',2025,'2025-26 to 2034-35',*_AUBP,"‘a 10-year multimedia rights agreement that will extend their successful partnership through the 2034-35 academic year.’ Ten academic years ending in 2034-35 begin in 2025-26."),
('Auburn','mmr_total_value','--','2025-26 to 2034-35',*_AUB,_AUBN),
('Auburn','mmr_annual_value','--','2025-26 to 2034-35',*_AUB,_AUBN),
('Georgia','mmr_partner','Learfield','2017-18 to 2026-27',*_UGA2,"‘Georgia athletics has struck a new deal with Learfield, its multimedia rights partner, that will run through 2042.’ The agreement in force was signed with IMG College (now Learfield) and JMI Sports."),
('Georgia','mmr_start_year',2017,'2017-18 to 2026-27',*_UGA,"‘signing a new 10-year, $152.5-million multimedia and marketing rights deal with IMG College and JMI Sports’; ‘at least $12.8 million for the 2017-18 academic year’."+_UGAX),
('Georgia','mmr_term_years',10,'2017-18 to 2026-27',*_UGA,"‘signing a new 10-year, $152.5-million multimedia and marketing rights deal with IMG College and JMI Sports’; ‘with increases each year through the duration of the contract, ending in 2026-27.’"+_UGAX),
('Georgia','mmr_total_value',152500000,'2017-18 to 2026-27',*_UGA,"‘signing a new 10-year, $152.5-million multimedia and marketing rights deal with IMG College and JMI Sports’."+_UGAX),
('South Carolina','mmr_partner','Learfield','from 1 July 2017',*_SC,_SCN),
('South Carolina','mmr_start_year',2017,'from 1 July 2017',*_SC,_SCN),
('South Carolina','mmr_term_years',10,'from 1 July 2017',*_SC,_SCN),
('South Carolina','mmr_total_value','--','from 1 July 2017',*_SC,"The release gives no value, and none was reported elsewhere. "+_SCN),
('South Carolina','mmr_annual_value','--','from 1 July 2017',*_SC,"The release gives no value, and none was reported elsewhere."),
('Florida','mmr_partner','Learfield','2026',*_FL,_FLN),
]
for _f in ('start_year','term_years','total_value','annual_value'):
    ROWS_E.append(('Florida','mmr_'+_f,'--','2026',*_FL,_FLN))
    ROWS_E.append(('Missouri','mmr_'+_f,'--','2026',*_MO,_MON))
    ROWS_E.append(('Alabama','apparel_'+_f,'--','2026',*_ALA,_ALAN))
    ROWS_E.append(('Mississippi State','apparel_'+_f,'--','2026',*_MSU,_MSUN))
