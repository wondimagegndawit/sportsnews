/* THE SPORTS BUSINESS WIRE — client-side renderer
   Reads /data/*.json and renders the feed. No build step. */

(function () {
  "use strict";

  const LEAGUES = {
    nfl:     { name: "NFL",                file: "nfl.json" },
    nba:     { name: "NBA",                file: "nba.json" },
    mlb:     { name: "MLB",                file: "mlb.json" },
    nhl:     { name: "NHL",                file: "nhl.json" },
    cfb:     { name: "College Football",   file: "cfb.json" },
    cbb:     { name: "College Basketball", file: "cbb.json" },
    soccer:  { name: "Soccer",             file: "soccer.json" },
    other:   { name: "Other Sports",       file: "other.json" },
  };

  const CATEGORIES = {
    legal:       "Legal / Regulatory",
    investment:  "Investments / M&A",
    media:       "Media / Rights",
    partnership: "Partnerships",
    business:    "League / Team Biz",
  };

  const body = document.body;
  const leagueKey = body.dataset.league || "all"; // "all" for homepage
  const root = body.dataset.root || "";           // "" at site root, "../" in /leagues/

  const feedEl = document.getElementById("feed");
  const statusEl = document.getElementById("feed-status");
  const searchEl = document.getElementById("search");
  const filterWrap = document.getElementById("filters");
  const tickerEl = document.getElementById("ticker");

  let allEntries = [];
  let activeCategory = "all";
  let searchTerm = "";

  /* ---------- data loading ---------- */

  function fetchLeague(key) {
    return fetch(root + "data/" + LEAGUES[key].file)
      .then((r) => {
        if (!r.ok) throw new Error(key + ": HTTP " + r.status);
        return r.json();
      })
      .then((entries) => entries.map((e) => ({ ...e, league: key })))
      .catch((err) => {
        console.warn("Could not load", key, err);
        return [];
      });
  }

  function loadData() {
    const keys = leagueKey === "all" ? Object.keys(LEAGUES) : [leagueKey];
    return Promise.all(keys.map(fetchLeague)).then((lists) => {
      allEntries = lists
        .flat()
        .filter((e) => e && e.date && e.headline)
        .sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));
      if (leagueKey === "all") allEntries = allEntries.slice(0, 20);
    });
  }

  /* ---------- rendering ---------- */

  function fmtDate(iso) {
    const [y, m, d] = iso.split("-").map(Number);
    const dt = new Date(y, m - 1, d);
    return dt.toLocaleDateString("en-US", {
      weekday: "short", month: "short", day: "numeric", year: "numeric",
    });
  }

  function isNew(iso) {
    const [y, m, d] = iso.split("-").map(Number);
    const ageDays = (Date.now() - new Date(y, m - 1, d).getTime()) / 86400000;
    return ageDays < 3;
  }

  function el(tag, cls, text) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function renderCard(entry) {
    const card = el("article", "card");
    card.dataset.category = entry.category || "business";

    const meta = el("div", "card-meta");
    meta.appendChild(el("span", "cat-tag", CATEGORIES[entry.category] || entry.category));
    if (leagueKey === "all" && LEAGUES[entry.league]) {
      meta.appendChild(el("span", "card-league", LEAGUES[entry.league].name));
    }
    if (isNew(entry.date)) meta.appendChild(el("span", "new-badge", "★NEW★"));
    meta.appendChild(el("span", "card-date", entry.date));
    card.appendChild(meta);

    card.appendChild(el("h3", null, entry.headline));
    card.appendChild(el("p", null, entry.summary || ""));

    if (entry.source_url) {
      const src = el("div", "card-source");
      const a = el("a", null, "» " + (entry.source_name || "source"));
      a.href = entry.source_url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      src.appendChild(a);
      card.appendChild(src);
    }
    return card;
  }

  function visibleEntries() {
    return allEntries.filter((e) => {
      if (activeCategory !== "all" && e.category !== activeCategory) return false;
      if (searchTerm) {
        const hay = (e.headline + " " + (e.summary || "") + " " + (e.source_name || "")).toLowerCase();
        if (!hay.includes(searchTerm)) return false;
      }
      return true;
    });
  }

  function renderFeed() {
    if (!feedEl) return;
    feedEl.innerHTML = "";
    const entries = visibleEntries();

    if (!entries.length) {
      statusEl.hidden = false;
      statusEl.innerHTML = allEntries.length
        ? "NO MATCHES FOUND... TRY ANOTHER FILTER"
        : 'NO DATA LOADED. If you opened this file directly, run a local server first — see <span class="err">README.md</span> (e.g. <code>python3 -m http.server</code>).';
      return;
    }
    statusEl.hidden = true;

    // group by date (entries already sorted desc)
    let currentDate = null;
    let group = null;
    let cardsWrap = null;
    entries.forEach((entry) => {
      if (entry.date !== currentDate) {
        currentDate = entry.date;
        group = el("section", "day-group");
        const h = el("h2", "day-heading", "▚ " + fmtDate(entry.date));
        group.appendChild(h);
        cardsWrap = el("div", "cards");
        group.appendChild(cardsWrap);
        feedEl.appendChild(group);
      }
      cardsWrap.appendChild(renderCard(entry));
    });
  }

  /* ---------- ticker ---------- */

  function renderTicker() {
    if (!tickerEl) return;
    const items = allEntries.slice(0, 12);
    if (!items.length) {
      tickerEl.textContent = "*** THE SPORTS BUSINESS WIRE *** TRACKING DEALS, LAWSUITS + MEDIA RIGHTS ACROSS THE SPORTS WORLD ***";
      return;
    }
    tickerEl.innerHTML = "";
    items.forEach((e) => {
      const league = LEAGUES[e.league] ? LEAGUES[e.league].name.toUpperCase() : "";
      const lg = el("span", "tick-league", league + ": ");
      tickerEl.appendChild(lg);
      tickerEl.appendChild(document.createTextNode(e.headline));
      tickerEl.appendChild(el("span", "tick-sep", "+++"));
    });
  }

  /* ---------- controls ---------- */

  function initFilters() {
    if (!filterWrap) return;
    filterWrap.addEventListener("click", (ev) => {
      const btn = ev.target.closest(".filter-btn");
      if (!btn) return;
      activeCategory = btn.dataset.cat;
      filterWrap.querySelectorAll(".filter-btn").forEach((b) => {
        b.setAttribute("aria-pressed", String(b === btn));
      });
      renderFeed();
    });
  }

  function initSearch() {
    if (!searchEl) return;
    searchEl.addEventListener("input", () => {
      searchTerm = searchEl.value.trim().toLowerCase();
      renderFeed();
    });
  }

  /* ---------- retro flourishes ---------- */

  function initHitCounter() {
    const counter = document.getElementById("hit-counter");
    if (!counter) return;
    let hits = 31337;
    try {
      const stored = Number(localStorage.getItem("sbw-hits") || 0);
      hits += stored + 1;
      localStorage.setItem("sbw-hits", String(stored + 1));
    } catch (e) { /* private browsing — keep the classic number */ }
    counter.innerHTML = "";
    String(hits).padStart(7, "0").split("").forEach((digit) => {
      counter.appendChild(el("span", null, digit));
    });
  }

  /* ---------- boot ---------- */

  loadData().then(() => {
    renderTicker();
    renderFeed();
  });
  initFilters();
  initSearch();
  initHitCounter();
})();
