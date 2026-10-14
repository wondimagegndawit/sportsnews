# THE SPORTS BUSINESS WIRE 📟

A retro-styled static site for tracking business, legal, and investment
developments across major sports leagues. 90s aesthetic, modern engineering:
plain HTML/CSS/JS, no build step, all content in JSON files.

## Run it locally

The site fetches JSON data files, so browsers need it served over HTTP
(opening `index.html` directly via `file://` blocks the data fetch in most
browsers). One line, from the repo root:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Any static server works, e.g. `npx serve`.

## Folder structure

```
/index.html        Homepage — 20 most recent entries across all leagues
/leagues/*.html    One page per league (nfl, nba, mlb, nhl, cfb, cbb, soccer, other)
/leagues/tickets.html  Average ticket prices by league (PWHL, WNBA, NWSL, MLS, NHL)
/data/*.json       All news content — one JSON file per league
/data/ticket_prices.json  Ticket price research, one entry per league-season, with sources
/css/style.css     All styling
/js/app.js         Client-side rendering, filters, search, ticker
/js/tickets.js     Renders the ticket price desk
ADD_NEWS.md        How to add new entries daily
```

## Adding news

Edit the relevant file in `/data/` — see [ADD_NEWS.md](ADD_NEWS.md).
No HTML/CSS changes needed, ever.

## Deploy for free

### GitHub Pages

1. Push this repo to GitHub.
2. Repo **Settings → Pages → Source**: select *Deploy from a branch*, choose
   your branch and `/ (root)`.
3. Your site is live at `https://<username>.github.io/<repo>/` within a minute.

### Vercel

```bash
npx vercel
```

Accept the defaults (no framework, no build command, output directory `.`).
Or import the repo at <https://vercel.com/new> — it deploys static sites as-is.

## Features

- **Marquee ticker** with the latest headlines (pauses on hover)
- **Category filters** (Legal / Invest / Media / Sponsor / Biz) + keyword search, all client-side
- **Blinking ★NEW★ badge** on entries less than 3 days old
- Responsive at 375px / 768px / 1440px; keyboard navigable; `prefers-reduced-motion` respected
- One gratuitous retro flourish per page, as required by law (the 1996 one)
