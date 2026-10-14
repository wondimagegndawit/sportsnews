/* THE SPORTS BUSINESS WIRE — ticket price desk
   Reads window.TICKET_PRICES (from /data/ticket_prices.js) and renders one table per league. */

(function () {
  "use strict";

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

  if (window.TICKET_PRICES) {
    statusEl.hidden = true;
    render(window.TICKET_PRICES);
  } else {
    statusEl.innerHTML = 'PRICE DATA MISSING. Check that <span class="err">data/ticket_prices.js</span> exists and is valid.';
  }
})();
