# Adding news entries

All content lives in `/data/`, one JSON file per league:

| File            | League page                       |
|-----------------|-----------------------------------|
| `nfl.json`      | NFL                               |
| `nba.json`      | NBA                               |
| `mlb.json`      | MLB                               |
| `nhl.json`      | NHL                               |
| `cfb.json`      | College Football                  |
| `cbb.json`      | College Basketball                |
| `soccer.json`   | Soccer (MLS, EPL, global clubs)   |
| `other.json`    | F1, golf, tennis, WNBA, combat…   |

Each file is a JSON **array** of entry objects. Order inside the file doesn't
matter — the site sorts by date (newest first) at render time.

## Entry format

```json
{
  "date": "2026-08-09",
  "category": "investment",
  "headline": "Short, punchy headline",
  "summary": "2-3 sentences of context: who, what, how much, why it matters.",
  "source_url": "https://example.com/article",
  "source_name": "Sportico"
}
```

### Fields

- **date** — `YYYY-MM-DD`. Required.
- **category** — exactly one of:
  - `legal` — lawsuits, antitrust, NIL/rev-share rulings, CBAs, gambling regulation
  - `investment` — PE deals, team sales, valuations, minority stakes, fund launches
  - `media` — broadcast/streaming rights, DTC launches
  - `partnership` — sponsorships, naming rights, betting partnerships
  - `business` — expansion, relocation, facilities, exec hires, league policy
- **headline** — required.
- **summary** — 2–3 sentences.
- **source_url** / **source_name** — link to the reporting. Leave `source_url`
  as `""` if there's genuinely no link; the card just omits the source line.

## Example: adding today's news to the NBA page

Open `data/nba.json` and add an object to the array (a leading position keeps
recent stuff near the top for humans, but isn't required):

```json
[
  {
    "date": "2026-08-10",
    "category": "media",
    "headline": "NBA finalizes streaming package tweak",
    "summary": "The league and its broadcast partner amended the deal to move 12 games to streaming-only. The change starts with the 2026-27 season.",
    "source_url": "https://www.example.com/nba-streaming",
    "source_name": "The Athletic"
  },
  ... existing entries ...
]
```

**Gotchas:** keep the array valid JSON — commas between objects, no trailing
comma after the last one, double quotes only. Validate with:

```bash
python3 -m json.tool data/nba.json > /dev/null && echo OK
```

Refresh the page — the entry appears, color-coded, with a blinking ★NEW★
badge if it's less than 3 days old. The homepage feed and ticker pick it up
automatically.
