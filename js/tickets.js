/* THE SPORTS BUSINESS WIRE — ticket price desk
   Reads /data/ticket_prices.json and renders one table per league. */

(function () {
  "use strict";

  const root = document.body.dataset.root || "";
  const statusEl = document.getElementById("feed-status");
  const pricesEl = document.getElementById("prices");
  const tickerEl = document.getElementById("ticker");

  function el(tag, cls, text) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function sourceLink(fig) {
    if (!fig.source_url) return el("span", null, fig.source_name || "");
    const a = el("a", null, fig.source_name || "source");
    a.href = fig.source_url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    return a;
  }

  function renderSeason(season) {
    const card = el("article", "card price-card");
    const missing = !/\d/.test(season.headline);
    card.dataset.category = missing ? "legal" : "investment";

    const meta = el("div", "card-meta");
    meta.appendChild(el("span", "cat-tag", season.season + " season"));
    card.appendChild(meta);

    card.appendChild(el("h3", missing ? "price-headline price-missing" : "price-headline", season.headline));
    card.appendChild(el("p", null, season.note || ""));

    if (season.figures && season.figures.length) {
      const wrap = el("div", "price-table-wrap");
      const table = el("table", "price-table");
      const thead = el("thead");
      const hr = el("tr");
      ["Metric", "Value", "Scope", "Source", "Conf."].forEach((h) => hr.appendChild(el("th", null, h)));
      thead.appendChild(hr);
      table.appendChild(thead);
      const tbody = el("tbody");
      season.figures.forEach((fig) => {
        const tr = el("tr");
        tr.appendChild(el("td", null, fig.metric));
        tr.appendChild(el("td", "price-value", fig.value));
        tr.appendChild(el("td", null, fig.scope));
        const src = el("td");
        src.appendChild(sourceLink(fig));
        if (fig.pub_date) src.appendChild(el("span", "price-date", " · " + fig.pub_date));
        tr.appendChild(src);
        tr.appendChild(el("td", "conf conf-" + fig.confidence.split("-")[0], fig.confidence));
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      wrap.appendChild(table);
      card.appendChild(wrap);
    }
    return card;
  }

  function render(data) {
    pricesEl.innerHTML = "";
    const method = el("p", "price-method", data.method + " Last updated " + data.updated + ".");
    pricesEl.appendChild(method);

    data.leagues.forEach((league) => {
      const group = el("section", "day-group");
      group.id = league.key;
      group.appendChild(el("h2", "day-heading", "▚ " + league.name));
      const cards = el("div", "cards");
      league.seasons.forEach((s) => cards.appendChild(renderSeason(s)));
      group.appendChild(cards);
      pricesEl.appendChild(group);
    });

    if (tickerEl) {
      tickerEl.innerHTML = "";
      data.leagues.forEach((league) => {
        tickerEl.appendChild(el("span", "tick-league", league.name.toUpperCase() + ": "));
        const line = league.seasons.map((s) => s.season + " " + s.headline).join(" / ");
        tickerEl.appendChild(document.createTextNode(line));
        tickerEl.appendChild(el("span", "tick-sep", "+++"));
      });
    }
  }

  fetch(root + "data/ticket_prices.json")
    .then((r) => {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then((data) => {
      statusEl.hidden = true;
      render(data);
    })
    .catch((err) => {
      console.warn("Could not load ticket prices", err);
      statusEl.innerHTML = 'DATA FETCH BLOCKED. If you opened this file directly, run a local server — see <span class="err">README.md</span> (e.g. <code>python3 -m http.server</code>).';
    });
})();
