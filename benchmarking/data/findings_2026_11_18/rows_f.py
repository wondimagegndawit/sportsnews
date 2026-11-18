# Part F: follow-ups from the second research pass of 18 Nov 2026.
ROWS_F=[
('Arkansas','apparel_partner','Nike','2026',"WholeHogSports Daily Podcast, Arkansas Democrat-Gazette (4 Mar 2026)",'https://whole-hog-radio.castos.com/episodes/arkansas-razorbacks-strike-deal-with-tyson-foods',"‘And then, of course, all of the apparel is through Nike.’ A remark in the newspaper's podcast on the Tyson patch deal; no report of the current contract was located, and the last one on record is the five-year Nike deal that began 1 July 2010."),
('BYU','mmr_partner','--','2026',"BYU Athletics, corporate sponsorships page",'https://byucougars.com/athletic-sponsorships',"The page lists a corporate sponsorship team of BYU Athletics staff (‘Sr. Associate Athletic Director, Corporate Sponsorships’) and names no outside rights holder, but it does not state that the rights are sold in-house, so no partner is entered."),
# Texas: Humann logo on the football field (from August 2025) and the basketball court (from 2026-27); neither surface is renamed
]
_SP=("Spectrum News (26 Aug 2025)",'https://spectrumlocalnews.com/tx/austin/news/2025/08/26/humann-logo-to-be-featured-on-the-field-of-dkr-at-ut-austin')
_AP=("Associated Press via ClickOrlando (19 Oct 2025)",'https://www.clickorlando.com/sports/2025/10/19/all-about-the-logo-schools-adding-corporate-gridiron-ads-to-level-revenue-sharing-playing-field/')
_SI=("Sports Illustrated (25 Aug 2025)",'https://www.si.com/college/texas/football/texas-longhorns-make-historic-on-field-branding-partnership')
_Q="‘The company Humann's logo will be featured on the field as they enter a partnership to serve as the Official Cardiovascular Supplement of Texas Athletics.’ ‘The brand's logo will be featured at fields and courts across campus’."
_ND="‘The size of the deal, which is at least the sixth in the Southeastern Conference and involves all 20 Longhorns sports programs, was not disclosed.’ The one agreement covers every Texas venue, so no figure for this surface alone exists."
_TM="Sports Illustrated calls it ‘The multi-year agreement’; no number of years is confirmed (one outlet's unattributed ‘16-year deal’ is not used)."
for _pre,_surf,_yr,_season,_own in (('field_nr','field',2025,'from August 2025','the field keeps its own name (Campbell-Williams Field)'),('court_nr','court',2026,'from 2026-27','the court is not renamed')):
    _w="‘Darrell K Royal–Texas Memorial Stadium (football)’" if _pre=='field_nr' else "‘Moody Center (basketball, beginning in the 2026-2027 season)’"
    ROWS_F+=[
     ('Texas',_pre+'_partner','Humann',_season,*_SP,_Q+' Venue list: '+_w+f'. A paid logo on the {_surf}; {_own}.'),
     ('Texas',_pre+'_deal_type','commercial',_season,*_SP,f'A paid logo on the {_surf}; {_own}. See the rights type column.'),
     ('Texas',_pre+'_rights_type','Logo only',_season,*_SP,f'The sponsor pays for a logo on the {_surf}; {_own}. Classified by the researcher.'),
     ('Texas',_pre+'_industry','nutritional supplements',_season,*_SP,'Humann sells cardiovascular supplements; industry classified by the researcher.'),
     ('Texas',_pre+'_start_year',_yr,_season,*_SP,("‘The logo will start being featured in August.’ (article of 26 August 2025)" if _pre=='field_nr' else _w)),
     ('Texas',_pre+'_term_years','--',_season,*_SI,_TM),
     ('Texas',_pre+'_total_value','--',_season,*_AP,_ND),
     ('Texas',_pre+'_annual_value','--',_season,*_AP,_ND)]
