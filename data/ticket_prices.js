/* Ticket price research — loaded via <script> so the page works without a server.
   Edit the object below; keep it valid JSON (double quotes, no trailing commas). */
window.TICKET_PRICES = {
  "updated": "2026-10-14",
  "method": "Average ticket prices for each league's last three completed regular seasons, compiled from SeatGeek and other ticket marketplaces (Vivid Seats, TickPick, StubHub, Gametime, Logitix, Victory Live), Team Marketing Report, and publications quoting them. Figures from different sources measure different things (resale sold price vs. listing price vs. face value, fees in or out, partial vs. full season), so compare within a source, not across them. Quotes were verified against search-result excerpts of the cited pages; spot-check the originals before citing.",
  "leagues": [
    {
      "key": "pwhl",
      "name": "PWHL",
      "seasons": [
        {
          "season": "2023-24",
          "headline": "No published average",
          "note": "Inaugural season. Only face-value ranges and single-game resale snapshots exist.",
          "figures": [
            {
              "metric": "Primary face-value range (not an average)",
              "value": "$16–$48 USD per seat",
              "scope": "Lower bowl, bench side, multiple venues",
              "source_name": "The Hockey News",
              "source_url": "https://thehockeynews.com/womens/pwhl/pwhl-sends-season-ticket-information-to-fans-who-made-deposits",
              "pub_date": "2023 (late)",
              "confidence": "medium"
            },
            {
              "metric": "Resale snapshot, single game",
              "value": "$54 seat relisted at $198 on StubHub; top section ~$450 (CAD)",
              "scope": "Montreal vs. Toronto, Bell Centre, Apr 20 2024 only",
              "source_name": "CBC Montreal",
              "source_url": "https://www.cbc.ca/news/canada/montreal/pwhl-ticket-sales-1.7148286",
              "pub_date": "2024-03",
              "confidence": "medium"
            }
          ]
        },
        {
          "season": "2024-25",
          "headline": "No published average",
          "note": "No league-wide or team average found from SeatGeek, StubHub, Vivid Seats, TickPick, TMR or trade press. TMR's Fan Cost Index does not cover the PWHL.",
          "figures": []
        },
        {
          "season": "2025-26",
          "headline": "No published average",
          "note": "Record 9,304 average attendance (+28% YoY, per the league's Apr 28 2026 release), but no average price was published. SeatGeek reported PWHL sales up 136% vs. 2025.",
          "figures": [
            {
              "metric": "SeatGeek get-in price, single game",
              "value": "$186 (vs. $112 for Rangers–Red Wings)",
              "scope": "Sirens vs. Torrent at Madison Square Garden, Apr 4 2026 only",
              "source_name": "SeatGeek blog",
              "source_url": "https://seatgeek.ca/blog/pwhl-drawing-more-demand-than-rangers-for-historic-hockey-doubleheader-at-madison-square-garden",
              "pub_date": "2026-03",
              "confidence": "medium-low"
            },
            {
              "metric": "Season-ticket price range, one team",
              "value": "$27–$93 per game (CAD)",
              "scope": "Vancouver Goldeneyes season tickets",
              "source_name": "Daily Hive",
              "source_url": "https://dailyhive.com/vancouver/vancouver-pwhl-season-tickets-on-sale-cost",
              "pub_date": "2025",
              "confidence": "medium"
            }
          ]
        }
      ]
    },
    {
      "key": "wnba",
      "name": "WNBA",
      "seasons": [
        {
          "season": "2024",
          "headline": "$107",
          "note": "Vivid Seats average sold price, regular season and playoffs combined (2023: $64). Logitix had $87.75 before fees through the first half of the season ($61.36 excluding Fever games).",
          "figures": [
            {
              "metric": "Secondary-market avg sold price (incl. playoffs)",
              "value": "$107 (2023: $64, +67%)",
              "scope": "League-wide, Vivid Seats",
              "source_name": "Forbes",
              "source_url": "https://www.forbes.com/sites/maryroeloffs/2024/10/18/wnba-finals-ticket-prices-soaring-over-last-year-as-minnesota-lynx-strive-to-make-history/",
              "pub_date": "2024-10-18",
              "confidence": "high"
            },
            {
              "metric": "Secondary-market avg resale price, excl. fees, first half",
              "value": "$87.75 (2023: $50.10); $61.36 excl. Fever games",
              "scope": "League-wide, Logitix data",
              "source_name": "Sportico",
              "source_url": "https://www.sportico.com/leagues/basketball/2024/fever-sky-wnba-resale-ticket-prices-upward-1234786386/",
              "pub_date": "2024 (mid-season)",
              "confidence": "medium-high"
            },
            {
              "metric": "Secondary-market avg (2024 baseline restated in 2025)",
              "value": "$122",
              "scope": "League-wide, Victory Live",
              "source_name": "Just Women's Sports",
              "source_url": "https://justwomenssports.com/reads/wnba-ticket-prices-surge-on-secondary-market-ahead-of-2025-season/",
              "pub_date": "2025-04-25",
              "confidence": "medium"
            }
          ]
        },
        {
          "season": "2025",
          "headline": "$173–$203",
          "note": "Both figures are early-season or preseason snapshots; no full-season 2025 average was published. Vivid Seats' May 2025 report put the YoY increase at 49%.",
          "figures": [
            {
              "metric": "Secondary-market avg (preseason snapshot)",
              "value": "$173 (from $122, +43%)",
              "scope": "League-wide, Victory Live",
              "source_name": "Just Women's Sports",
              "source_url": "https://justwomenssports.com/reads/wnba-ticket-prices-surge-on-secondary-market-ahead-of-2025-season/",
              "pub_date": "2025-04-25",
              "confidence": "medium"
            },
            {
              "metric": "Secondary-market avg (early season)",
              "value": "$203 (from $135, +50%)",
              "scope": "League-wide, Vivid Seats",
              "source_name": "ESPN",
              "source_url": "https://www.espn.com/wnba/story/_/id/44633851/2025-wnba-draft-ticket-demand-prices-24",
              "pub_date": "2025-04",
              "confidence": "medium"
            }
          ]
        },
        {
          "season": "2026",
          "headline": "No published average",
          "note": "The season was completed (no lockout) with record attendance of ~3.79M. Only team-level SeatGeek data was published: Atlanta, Indiana and Washington had the highest average resale prices.",
          "figures": [
            {
              "metric": "SeatGeek avg resale price, one team",
              "value": "$146 (+26% YoY), 3rd-highest in league",
              "scope": "Washington Mystics only",
              "source_name": "Front Office Sports (SeatGeek data)",
              "source_url": "https://frontofficesports.com/wnba-season-tickets-soaring-prices-cba/",
              "pub_date": "2026-08",
              "confidence": "medium"
            }
          ]
        }
      ]
    },
    {
      "key": "nwsl",
      "name": "NWSL",
      "seasons": [
        {
          "season": "2023",
          "headline": "$51",
          "note": "Vivid Seats average resale price for the regular season. A mid-2023 SeatGeek snapshot of resale listings averaged $23 (MLS: $50).",
          "figures": [
            {
              "metric": "Secondary-market avg resale price, regular season",
              "value": "$51",
              "scope": "League-wide, Vivid Seats",
              "source_name": "Forbes / Axios",
              "source_url": "https://www.forbes.com/sites/maryroeloffs/2024/03/15/womens-soccer-surge-nwsl-ticket-prices-soar-as-team-prices-hit-9-figures/",
              "pub_date": "2024-03-15",
              "confidence": "medium-high"
            },
            {
              "metric": "SeatGeek avg resale listing price (snapshot)",
              "value": "$23 (MLS: $50)",
              "scope": "League-wide, SeatGeek listings, mid-2023",
              "source_name": "NerdWallet (SeatGeek data)",
              "source_url": "https://www.nerdwallet.com/article/finance/womens-soccer-games-are-way-cheaper-than-mens-so-cheer-them-on",
              "pub_date": "2023-07",
              "confidence": "medium"
            }
          ]
        },
        {
          "season": "2024",
          "headline": "$76",
          "note": "Vivid Seats, +49% YoY, measured at the start of the season (not a final full-season average). KC Current led at $208, Angel City second at $87.",
          "figures": [
            {
              "metric": "Secondary-market avg resale price (early season)",
              "value": "$76 (+49%)",
              "scope": "League-wide, Vivid Seats",
              "source_name": "Forbes / Axios",
              "source_url": "https://www.axios.com/local/washington-dc/2024/03/22/washington-spirit-ticket-prices",
              "pub_date": "2024-03-22",
              "confidence": "medium"
            }
          ]
        },
        {
          "season": "2025",
          "headline": "No published average",
          "note": "2025 coverage focused on attendance (10,669 per game, down ~5%) and revenue. No ticket-price average was found from any marketplace.",
          "figures": []
        }
      ]
    },
    {
      "key": "mls",
      "name": "MLS",
      "seasons": [
        {
          "season": "2023",
          "headline": "$73",
          "note": "TickPick average per seat. The Messi effect shows in the numbers: Inter Miami home listings rose from $152 to $864 on TicketIQ after his signing. SeatGeek put the March 2023 average get-in price at $31.",
          "figures": [
            {
              "metric": "Secondary-market avg purchase price",
              "value": "$73 per seat",
              "scope": "League-wide, TickPick",
              "source_name": "CNN",
              "source_url": "https://www.cnn.com/2024/02/20/business/lionel-messi-season-debut-ticket-prices/index.html",
              "pub_date": "2024-02-20",
              "confidence": "medium-high"
            },
            {
              "metric": "SeatGeek average get-in price (preseason)",
              "value": "$31 (St. Louis CITY highest at $73)",
              "scope": "League-wide, SeatGeek",
              "source_name": "KMOV / FirstAlert4",
              "source_url": "https://www.firstalert4.com/2023/03/03/demand-has-never-wavered-st-louis-city-averaging-highest-ticket-price-league/",
              "pub_date": "2023-03-03",
              "confidence": "medium"
            }
          ]
        },
        {
          "season": "2024",
          "headline": "$83",
          "note": "Vivid Seats regular-season average. TickPick's $164 figure was season-to-date in February 2024 and was inflated by Messi games.",
          "figures": [
            {
              "metric": "Secondary-market avg, regular season",
              "value": "$83",
              "scope": "League-wide, Vivid Seats",
              "source_name": "Axios",
              "source_url": "https://www.axios.com/2025/02/20/how-to-watch-major-league-soccer-2025",
              "pub_date": "2025-02-20",
              "confidence": "medium-high"
            },
            {
              "metric": "Secondary-market avg (preseason, season-to-date)",
              "value": "$164",
              "scope": "League-wide, TickPick",
              "source_name": "CNN",
              "source_url": "https://www.cnn.com/2024/02/20/business/lionel-messi-season-debut-ticket-prices/index.html",
              "pub_date": "2024-02-20",
              "confidence": "medium"
            }
          ]
        },
        {
          "season": "2025",
          "headline": "$73–$133",
          "note": "Source-dependent. Vivid Seats reported $133 early in the season (+60%); Gametime put the full-year average at $73. SeatGeek's 2025 data excluded MLS. TMR has not published an MLS Fan Cost Index since 2022 ($38.95 face value).",
          "figures": [
            {
              "metric": "Secondary-market avg (early season)",
              "value": "$133 (+60% vs. 2024)",
              "scope": "League-wide, Vivid Seats",
              "source_name": "Axios",
              "source_url": "https://www.axios.com/2025/02/20/how-to-watch-major-league-soccer-2025",
              "pub_date": "2025-02-20",
              "confidence": "medium"
            },
            {
              "metric": "Avg price on Gametime, full year",
              "value": "$73 (2015: $60 in 2025 dollars, +22% real)",
              "scope": "League-wide, Gametime",
              "source_name": "Axios",
              "source_url": "https://www.axios.com/local/kansas-city/2026/02/05/sports-ticket-prices-soar-as-teams-chase-premium-demand",
              "pub_date": "2026-02-05",
              "confidence": "medium"
            }
          ]
        }
      ]
    },
    {
      "key": "nhl",
      "name": "NHL",
      "seasons": [
        {
          "season": "2023-24",
          "headline": "$88.84",
          "note": "Team Marketing Report weighted average non-premium ticket, a face-value figure (+4.8% YoY; 2022-23: $86.38). No SeatGeek or other league-wide resale average was found.",
          "figures": [
            {
              "metric": "Primary face-value avg, non-premium (TMR Fan Cost Index)",
              "value": "$88.84 (+4.8%)",
              "scope": "League-wide, all teams",
              "source_name": "Team Marketing Report",
              "source_url": "https://teammarketing.com/fci/2023-24-nhl-fan-cost-index/",
              "pub_date": "2024",
              "confidence": "high"
            }
          ]
        },
        {
          "season": "2024-25",
          "headline": "No reliable average",
          "note": "No 2024-25 TMR NHL index was found. An aggregator figure of $146 (Sports Acquisition) was left out: it is internally inconsistent, since its league average sits below its lowest team figure.",
          "figures": []
        },
        {
          "season": "2025-26",
          "headline": "No reliable average",
          "note": "No TMR or SeatGeek league average was found. Bookies.com reports figures built on SeatGeek/TickPick data ($304–$350), but these appear to be family-of-four totals rather than per-ticket prices.",
          "figures": [
            {
              "metric": "Family-of-four cost estimate (not a ticket price)",
              "value": "$304 league average",
              "scope": "League-wide, Bookies.com model",
              "source_name": "Bookies.com (via Wikipedia, 2025-26 Ottawa Senators season)",
              "source_url": "https://en.wikipedia.org/wiki/2025%E2%80%9326_Ottawa_Senators_season",
              "pub_date": "2025-10",
              "confidence": "low"
            }
          ]
        }
      ]
    }
  ]
};
