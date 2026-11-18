// One benchmarking deck in the Smash layout (4:3, Montserrat, gray page, white panel, legend box, black bars).
// Deal pages carry a Sponsor row and a Terms row under the logos; attendance pages show the conference's schools.
// Charts are native PowerPoint charts, so schools and numbers can be swapped by editing the chart data.
// Usage: NODE_PATH=<dir with pptxgenjs>/node_modules node scripts/build_benchmarking_deck.js slides/spec_deals.json slides/spec_big12.json out.pptx
const fs = require('fs'), path = require('path');
const pptxgen = require('pptxgenjs');
const JSZip = require('jszip');
const [dealPath, metricPath, outPath] = process.argv.slice(2);
const deals = JSON.parse(fs.readFileSync(dealPath, 'utf8'));
const metric = JSON.parse(fs.readFileSync(metricPath, 'utf8'));
const LOGO_DIR = path.join(path.dirname(dealPath), 'logos');
const W = 10, HT = 7.5, F = 'Montserrat';
const C = { page: 'EDEDED', panel: 'FFFFFF', ink: '000000', line: '9DC3E6', second: '7F7F7F', rule: 'BFBFBF' };
const money = v => '$' + (v / 1e6).toFixed(1) + 'M';
const PANEL = { x: 0.35, y: 1.3, w: 9.3, h: 5.62 };
const PL = { x: 0.09, y: 0.07, w: 0.9, h: 0.9 };

const pres = new pptxgen();
pres.defineLayout({ name: 'SMASH', width: W, height: HT });
pres.layout = 'SMASH';
pres.theme = { headFontFace: F, bodyFontFace: F };
pres.title = `Power 4 benchmarking: ${metric.conference}`;
let page = 0;
const labelOnly = new Set();          // chart objects whose value labels belong on the first bar series only

function frame(title, subtitle) {
  const slide = pres.addSlide(); page += 1;
  slide.background = { color: C.page };
  slide.addText(title, { x: 0.35, y: 0.2, w: 9.3, h: 0.38, fontFace: F, fontSize: 18, bold: true, color: C.ink, margin: 0, valign: 'middle', isTextBox: true, objectName: 'Title' });
  slide.addText(subtitle, { x: 0.36, y: 0.6, w: 9.0, h: 0.44, fontFace: F, fontSize: 9.5, bold: true, color: C.ink, margin: 0, valign: 'top', isTextBox: true, objectName: 'Subtitle' });
  slide.addShape(pres.shapes.LINE, { x: 0.35, y: 1.1, w: 9.3, h: 0, line: { color: C.ink, width: 0.75 } });
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: PANEL.x, y: PANEL.y, w: PANEL.w, h: PANEL.h, fill: { color: C.panel }, line: { color: C.panel, width: 0 }, rectRadius: 0.08, objectName: 'Panel' });
  slide.addText([{ text: 'SMASH', options: { bold: true } }, { text: 'SPORTS  |  CONFIDENTIAL' }], { x: 6.2, y: 7.05, w: 3.0, h: 0.25, fontFace: F, fontSize: 7, color: C.ink, align: 'right', valign: 'middle', margin: 0, isTextBox: true, objectName: 'Footer' });
  slide.addText(String(page), { x: 9.3, y: 7.05, w: 0.35, h: 0.25, fontFace: F, fontSize: 7, color: C.ink, align: 'right', valign: 'middle', margin: 0, isTextBox: true, objectName: 'Page number' });
  return slide;
}
// legend box, top left of the panel: keys = [['bar'|'solid'|'dash', color, label], ...]
function legend(slide, keys) {
  const step = keys.length > 3 ? 0.22 : 0.26, LG = { x: 0.55, y: 1.42, w: 2.45, h: 0.12 + keys.length * step };
  slide.addShape(pres.shapes.RECTANGLE, { x: LG.x, y: LG.y, w: LG.w, h: LG.h, fill: { color: C.panel }, line: { color: C.ink, width: 0.75 }, objectName: 'Legend box' });
  keys.forEach(([kind, color, label], i) => {
    const y = LG.y + 0.12 + i * step;
    if (kind === 'bar') slide.addShape(pres.shapes.RECTANGLE, { x: LG.x + 0.1, y, w: 0.36, h: 0.14, fill: { color }, line: { color, width: 0 } });
    else slide.addShape(pres.shapes.LINE, { x: LG.x + 0.1, y: y + 0.07, w: 0.36, h: 0, line: { color, width: 1.5, dashType: kind === 'dash' ? 'dash' : 'solid' } });
    slide.addText(label, { x: LG.x + 0.52, y: y - 0.03, w: LG.w - 0.6, h: 0.2, fontFace: F, fontSize: 7, color: C.ink, margin: 0, valign: 'middle', isTextBox: true });
  });
}
function chart(slide, name, CH, labels, bars, colors, lines, fmt, overlap, dense, floor = true) {
  slide.addChart([
    { type: pres.charts.BAR, data: bars.map(b => ({ name: b.name, labels, values: b.values })),
      options: { barDir: 'col', barOverlapPct: overlap, barGapWidthPct: dense ? 45 : 60, chartColors: colors, showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: fmt.label, dataLabelFontSize: dense && (bars.length > 1 || fmt.small) ? 6.5 : 8, dataLabelColor: C.ink, dataLabelFontFace: '+mn-lt' } },
    { type: pres.charts.LINE, data: lines.map(l => ({ name: l.name, labels, values: labels.map(() => l.value) })),
      options: { chartColors: [C.line, C.line], lineSize: 1.5, lineDataSymbol: 'none', lineDash: 'solid', showValue: false } },
  ], { x: CH.x, y: CH.y, w: CH.w, h: CH.h, objectName: name, layout: PL, showLegend: false, catAxisHidden: true, catGridLine: { style: 'none' },
    valAxisLabelFontSize: 8, valAxisLabelColor: C.ink, valAxisLabelFontFace: '+mn-lt', valAxisLabelFormatCode: fmt.axis, ...(floor ? { valAxisMinVal: 0 } : {}),
    valGridLine: { color: C.ink, size: 0.5 }, valAxisLineShow: true });
}

// ---- deal pages: bars, logos, then Sponsor and Terms rows (and a Sport row on the logo-deal page)
function dealSlide(s) {
  const slide = frame(s.title, s.subtitle);
  const n = s.schools.length, dense = n > 8, bySport = s.schools.some(x => x.sport);
  const CH = { x: 0.5, y: 2.4, w: 9.0, h: 2.55 };
  const fill = { Football: C.ink, Basketball: C.second };
  legend(slide, bySport ? [['bar', fill.Football, '= Football field'], ['bar', fill.Basketball, '= Basketball court'], ['solid', C.line, `= P4 Average (${money(s.avg)})`], ['dash', C.line, `= P4 Median (${money(s.med)})`]]
                        : [['bar', C.ink, '= Annual Value'], ['solid', C.line, `= P4 Average (${money(s.avg)})`], ['dash', C.line, `= P4 Median (${money(s.med)})`]]);
  const labels = s.schools.map(x => x.school);
  const bars = bySport ? ['Football', 'Basketball'].map(sp => ({ name: sp === 'Football' ? 'Football field' : 'Basketball court', values: s.schools.map(x => (x.sport === sp ? x.value || 0 : 0)) }))
                       : [{ name: 'Annual Value', values: s.schools.map(x => x.value || 0) }];
  // the empty zero section of the label format hides the label where no value is reported
  chart(slide, `Chart: ${s.key}`, CH, labels, bars, bySport ? [fill.Football, fill.Basketball] : [C.ink], [{ name: 'P4 Average', value: s.avg }, { name: 'P4 Median', value: s.med }],
        { label: '$#,##0.0,,"M";;', axis: Math.max(...s.schools.map(x => x.value || 0)) < 2.5e6 ? '$#,##0.0,,"M"' : '$#,##0,,"M"' }, bySport ? 100 : 0, dense);   // small scales need the decimal on the axis
  const ROW = bySport ? { sportY: 5.42, sportH: 0.26, sponsorY: 5.68, sponsorH: 0.48, termsY: 6.16, h: 0.56 } : { sponsorY: 5.58, sponsorH: 0.56, termsY: 6.14, h: 0.56 };
  const X0 = 0.45, LW = 0.8;
  const band = Math.min(CH.w * PL.w / n, 2.2), cx = i => CH.x + CH.w * (PL.x + PL.w * (i + 0.5) / n);
  const logo = dense ? 0.36 : 0.46, logoY = CH.y + CH.h + 0.04, fs2 = dense ? 6 : 8;
  // shrink a cell's font when its longest word would not fit the column (Montserrat is about 0.62 em per character)
  const fit = t => { const longest = Math.max(...String(t).split(/\s+/).map(w => w.length)); return Math.max(4.5, Math.min(fs2, Math.floor(2 * (band - 0.04) * 72 / (0.62 * longest)) / 2)); };
  const compact = t => (dense ? t.replace(' years', ' yrs').replace(' total', '').replace('Through', 'Thru').replace(' a year', '/yr').replace('Term not disclosed', 'Term n/d').replace('Value not disclosed', 'Value n/d') : t).replace(' across 3 schools', '\n(3 schools)');
  [...(bySport ? [ROW.sportY] : []), ROW.sponsorY, ROW.termsY, ROW.termsY + ROW.h].forEach(y => slide.addShape(pres.shapes.LINE, { x: X0, y, w: W - 2 * X0, h: 0, line: { color: C.rule, width: 0.5 } }));
  const rowLabel = (t, y, h) => slide.addText(t, { x: X0, y, w: LW, h, fontFace: F, fontSize: 8, bold: true, color: C.ink, margin: 0, valign: 'middle', isTextBox: true, objectName: `Row label: ${t}` });
  if (bySport) rowLabel('Sport', ROW.sportY, ROW.sportH);
  rowLabel('Sponsor', ROW.sponsorY, ROW.sponsorH); rowLabel('Terms', ROW.termsY, ROW.h);
  const cell = (t, i, y, h, size, name) => slide.addText(t, { x: cx(i) - band / 2 + 0.01, y, w: band - 0.02, h, fontFace: F, fontSize: size, color: C.ink, align: 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: name });
  s.schools.forEach((x, i) => {
    slide.addImage({ path: path.join(LOGO_DIR, x.logo), x: cx(i) - logo / 2, y: logoY, w: logo, h: logo, objectName: `Logo: ${x.school}`, altText: `${x.school} logo` });
    if (bySport) cell(x.sport, i, ROW.sportY, ROW.sportH, fs2, `Sport: ${x.school}`);
    cell(x.sponsor, i, ROW.sponsorY, ROW.sponsorH, fit(x.sponsor), `Sponsor: ${x.school}`);
    cell(x.terms.map(compact).join('\n'), i, ROW.termsY, ROW.h, fs2, `Terms: ${x.school}`);
  });
}

// ---- attendance and capacity pages: the conference's schools, one or two seasons, Power 4 average and median
const HEAD = { ticket_sales: 'TICKET SALES REVENUE', licensing_sponsorship: 'LICENSING, ADS AND SPONSORSHIP REVENUE', media_rights: 'MEDIA RIGHTS REVENUE', fb_revenue: 'FOOTBALL OPERATING REVENUE', mbb_revenue: "MEN'S BASKETBALL OPERATING REVENUE", total_expenses: 'TOTAL OPERATING EXPENSES', surplus: 'OPERATING SURPLUS (DEFICIT)', coaching_salaries: 'COACHING SALARIES AND BENEFITS', support_staff_pay: 'SUPPORT AND ADMIN STAFF PAY', team_travel: 'TEAM TRAVEL', team_travel_fb: 'TEAM TRAVEL, FOOTBALL', team_travel_mbb: "TEAM TRAVEL, MEN'S BASKETBALL", team_travel_wbb: "TEAM TRAVEL, WOMEN'S BASKETBALL", fundraising_marketing: 'FUNDRAISING, MARKETING AND PROMOTION', student_meals: 'STUDENT-ATHLETE MEALS', debt_service: 'ANNUAL DEBT SERVICE', fb_hc_pay: 'FOOTBALL HEAD COACH PAY', mbb_hc_pay: "MEN'S BASKETBALL HEAD COACH PAY", fb_attendance: 'FOOTBALL ATTENDANCE', fb_capacity: 'FOOTBALL CAPACITY FILLED', mbb_attendance: "MEN'S BASKETBALL ATTENDANCE", mbb_capacity: "MEN'S BASKETBALL CAPACITY FILLED" };
const FMT = { num: { label: '#,##0.0,"K"', axis: '#,##0,"K"' }, pct: { label: '0%', axis: '0%' }, usd: { label: '$#,##0.0,,"M"', axis: '$#,##0,,"M"' } };
function metricSlide(s) {
  const scope = s.scope === 'conference' ? metric.conference.toUpperCase() : 'ALL P4';
  const slide = frame(`${HEAD[s.key] || s.label.toUpperCase()}: ${scope}`, `${s.title}. ${s.subtitle}`);
  const n = s.categories.length, dense = n > 8, two = s.series.length > 1;
  const byBasis = s.categories.some(c => c.basis === 'EADA');          // private schools on the federal report get a second colour
  const CH = { x: 0.5, y: 2.4, w: 9.0, h: 3.45 };
  const short = t => t.replace('Power 4', 'P4').replace(' average', ' Average').replace(' median', ' Median').replace(', both seasons', ', Both Seasons');
  const all = s.series[0].values.filter(v => v != null), hi = Math.max(...all), lo = Math.min(...all);
  // dollar charts: whole millions on labels once figures pass $100M, and a signed format where a deficit can show
  const fmt = s.unit !== 'usd' ? FMT[s.unit] : lo < 0 ? { label: '$#,##0.0,,"M";-$#,##0.0,,"M";$0.0,,"M"', axis: '$#,##0,,"M";-$#,##0,,"M"', small: true }
            : hi >= 1e8 ? { label: '$#,##0,,"M"', axis: '$#,##0,,"M"' } : FMT.usd;
  const bars = byBasis ? [['MFRS', 'MFRS report (public)'], ['EADA', 'EADA report (private)']].map(([b, nm]) => ({ name: nm, values: s.categories.map((c, i) => (c.basis === b ? s.series[0].values[i] : null)) }))
                       : s.series.map(x => ({ name: x.name, values: x.values.map(v => (v == null ? 0 : v)) }));
  legend(slide, [...(byBasis ? bars.map((b, i) => ['bar', i ? C.second : C.ink, `= ${b.name}`])
                             : s.series.map((x, i) => ['bar', i ? C.second : C.ink, `= ${s.series.length === 1 && s.unit === 'usd' ? 'Annual Value' : x.name.replace(/^(\S+) season$/, '$1 Season')}`])),
                 ['solid', C.line, `= ${short(s.lines[0].name)}`], ['dash', C.line, `= ${short(s.lines[1].name)}`]]);
  const name = `Chart: ${s.key}`;
  chart(slide, name, CH, s.categories.map(c => c.school), bars, two || byBasis ? [C.ink, C.second] : [C.ink], s.lines.map(l => ({ name: short(l.name), value: l.value })), fmt, byBasis ? 100 : 0, dense, lo >= 0);
  if (two) labelOnly.add(name);
  const logo = dense ? 0.36 : 0.46, logoY = CH.y + CH.h + 0.06, cx = i => CH.x + CH.w * (PL.x + PL.w * (i + 0.5) / n);
  s.categories.forEach((c, i) => slide.addImage({ path: path.join(LOGO_DIR, c.logo), x: cx(i) - logo / 2, y: logoY, w: logo, h: logo, objectName: `Logo: ${c.school}`, altText: `${c.school} logo` }));
  slide.addText(s.source, { x: 0.5, y: 6.42, w: 9.0, h: 0.44, fontFace: F, fontSize: 6.5, color: C.ink, margin: 0, valign: 'top', isTextBox: true, objectName: 'Source' });
}

deals.forEach(dealSlide);
const DEAL_KEYS = new Set(['jersey_patch', 'stadium_naming', 'field_naming', 'arena_naming', 'court_naming', 'logo_deals']);   // drawn from the deal spec above
metric.slides.filter(s => s.section === 'revenue').forEach(metricSlide);
metric.slides.filter(s => s.section === 'expense').forEach(metricSlide);
metric.slides.filter(s => !DEAL_KEYS.has(s.key) && s.section !== 'expense' && s.section !== 'revenue').forEach(metricSlide);

// ---- logo library: every school's logo with its name, to copy from when a school is swapped into a chart
(function library() {
  const cols = 7, per = 35, pages = Math.ceil(metric.logos.length / per), cw = 9.0 / cols;
  for (let pg = 0; pg < pages; pg++) {
    const slide = frame(`LOGO LIBRARY${pages > 1 ? ` (${pg + 1} OF ${pages})` : ''}`, `Copy a logo from here when you swap a school into a chart. All ${metric.logos.length} schools in the benchmarking workbook, in alphabetical order.`);
    metric.logos.slice(pg * per, (pg + 1) * per).forEach((l, i) => {
      const x = 0.5 + (i % cols) * cw, y = 1.6 + Math.floor(i / cols) * 1.02;
      slide.addImage({ path: path.join(LOGO_DIR, l.file), x: x + (cw - 0.46) / 2, y, w: 0.46, h: 0.46, objectName: `Logo: ${l.school}`, altText: `${l.school} logo` });
      slide.addText(l.short, { x, y: y + 0.5, w: cw, h: 0.3, fontFace: F, fontSize: 9, color: C.ink, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: `Name: ${l.school}` });
    });
  }
})();

(async () => {
  await pres.writeFile({ fileName: outPath });
  const zip = await JSZip.loadAsync(fs.readFileSync(outPath));
  // which chart part belongs to which named chart object
  const owner = {};
  for (const sn of Object.keys(zip.files).filter(n => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    const sx = await zip.file(sn).async('string'); const rels = zip.file(sn.replace('slides/', 'slides/_rels/') + '.rels');
    if (!rels) continue; const rx = await rels.async('string');
    for (const m of sx.matchAll(/<p:graphicFrame>[\s\S]*?<\/p:graphicFrame>/g)) {
      const nm = (m[0].match(/<p:cNvPr [^>]*name="([^"]*)"/) || [])[1], rid = (m[0].match(/r:id="([^"]+)"/) || [])[1];
      const tgt = rid && (rx.match(new RegExp(`Id="${rid}"[^>]*Target="([^"]+)"`)) || rx.match(new RegExp(`Target="([^"]+)"[^>]*Id="${rid}"`)) || [])[1];
      if (nm && tgt) owner['ppt/charts/' + tgt.split('/').pop()] = nm.replace(/&apos;/g, "'").replace(/&amp;/g, '&');
    }
  }
  for (const name of Object.keys(zip.files).filter(n => /^ppt\/charts\/chart\d+\.xml$/.test(n))) {
    let xml = await zip.file(name).async('string');
    const bm = xml.match(/<c:barChart>[\s\S]*?<\/c:barChart>/);
    if (bm) {
      let b = bm[0], k = 0;
      if (labelOnly.has(owner[name])) b = b.replace(/<c:ser>[\s\S]*?<\/c:ser>/g, ser => (k++ === 0 ? ser : ser.replace(/<c:showVal val="1"\/>/g, '<c:showVal val="0"/>')));   // grouped bars: label the first season only
      b = b.replace(/(<c:dLbls><c:numFmt [^>]*\/>)/g, '$1<c:spPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></c:spPr>');                                           // white behind each value label
      xml = xml.replace(bm[0], b);
    }
    const lm = xml.match(/<c:lineChart>[\s\S]*?<\/c:lineChart>/);
    if (lm) { let j = 0; xml = xml.replace(lm[0], lm[0].replace(/<c:ser>[\s\S]*?<\/c:ser>/g, ser => (j++ === 1 ? ser.replace(/<a:prstDash val="solid"\/>/g, '<a:prstDash val="dash"/>') : ser))); }   // dashed median
    zip.file(name, xml);
  }
  const out = new JSZip();
  for (const name of Object.keys(zip.files)) if (!zip.files[name].dir) out.file(name, await zip.file(name).async('nodebuffer'), { createFolders: false });
  fs.writeFileSync(outPath, await out.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
  console.log('wrote', outPath, '| slides', page);
})();
