// Build the benchmarking chart slides from a spec written by scripts/slides_data.py.
// Usage: NODE_PATH=<dir with pptxgenjs>/node_modules node scripts/build_slides.js slides/spec_big12.json slides/out.pptx [width_in height_in]
// The slide size defaults to 10 x 7.5 in (4:3), the Smash deck format; pass a width and height in inches for another, e.g. 13.33 7.5 (16:9).
// All text is Montserrat (the deck's theme font, which the charts inherit).
// Every chart is a native PowerPoint chart (Edit Data swaps the schools and numbers). The average and median are line
// series in the same chart. Logos are separate pictures in a row under the chart, in the same order as the bars.
const fs = require('fs'), path = require('path');
const pptxgen = require('pptxgenjs');
const JSZip = require('jszip');
const [specPath, outPath, wArg, hArg] = process.argv.slice(2);
const W = wArg ? parseFloat(wArg) : 10, HT = hArg ? parseFloat(hArg) : 7.5, M = 0.5;   // slide width, height and side margin, inches
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const LOGO_DIR = path.join(path.dirname(specPath), 'logos');
const C = { ink: '000000', prior: 'A6A6A6', avg: 'E4572E', med: '2E86AB', muted: '595959', grid: 'E5E7EB', white: 'FFFFFF' };
const FMT = { usd: { label: '$#,##0.0,,"M"', axis: '$#,##0,,"M"' }, num: { label: '#,##0.0,"K"', axis: '#,##0' }, pct: { label: '0%', axis: '0%' } };
const LBL = 9;   // chart label size (axis and data labels), points
// chart frame and the plot area inside it (fractions of the chart), fixed so logos line up with the bars
const NARROW = W < 12;                                   // narrower formats get smaller logos and labels
const LOGO = NARROW ? 0.34 : 0.42;
const TOP = NARROW ? 1.9 : 2.05, FOOT = NARROW ? 0.85 : 0.6;   // top of the chart; height kept for the source note
const CH = { x: M, y: TOP, w: W - 2 * M, h: HT - TOP - LOGO - 0.08 - FOOT - 0.3 }, PL = { x: NARROW ? 0.075 : 0.055, y: NARROW ? 0.15 : 0.13, w: NARROW ? 0.915 : 0.935, h: NARROW ? 0.72 : 0.70 };

const pres = new pptxgen();
pres.defineLayout({ name: 'BENCH', width: W, height: HT });
pres.layout = 'BENCH';
pres.theme = { headFontFace: 'Montserrat', bodyFontFace: 'Montserrat' };
pres.title = `Power 4 benchmarking charts: ${spec.conference}`;
pres.defineSlideMaster({
  title: 'Chart slide', background: { color: C.white },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', x: M, y: 0.35, w: W - 2 * M, h: NARROW ? 0.75 : 1.0, fontSize: NARROW ? 20 : 26, bold: true, color: C.ink, align: 'left', valign: 'top', margin: 0 }, text: '' } },
    { placeholder: { options: { name: 'body', type: 'body', x: M, y: NARROW ? 1.18 : 1.38, w: W - 2 * M, h: 0.6, fontSize: NARROW ? 13 : 15, color: C.muted, align: 'left', valign: 'top', margin: 0 }, text: '' } },
  ],
  slideNumber: { x: W - M - 0.5, y: HT - 0.5, w: 0.5, h: 0.3, fontSize: 10, color: C.muted, align: 'right' },
});

function chartSlide(s) {
  const slide = pres.addSlide({ masterName: 'Chart slide' });
  const nb = x => x.replace(/(\d{4})-(\d{2})\b/g, '$1\u2011$2');   // keep a season such as 2025-26 on one line
  slide.addText(nb(s.title), { placeholder: 'title' });
  slide.addText(nb(s.subtitle), { placeholder: 'body' });
  const dense = NARROW && s.categories.length > 10;          // many schools on a 4:3 slide: abbreviations keep the labels level
  const labels = s.categories.map(c => (dense ? c.abbr : c.short));
  const bars = s.series.map(x => ({ name: x.name, labels, values: x.values.map(v => (v == null ? 0 : v)) }));
  const lines = s.lines.map(l => ({ name: l.name, labels, values: labels.map(() => l.value) }));
  const f = FMT[s.unit];
  slide.addChart([
    { type: pres.charts.BAR, data: bars, options: { barDir: 'col', barGrouping: 'clustered', barGapWidthPct: s.series.length > 1 ? 45 : 60, chartColors: [C.ink, C.prior].slice(0, bars.length),
        showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: f.label, dataLabelFontSize: LBL, dataLabelColor: C.ink, dataLabelFontFace: '+mn-lt' } },
    { type: pres.charts.LINE, data: lines, options: { chartColors: [C.avg, C.med], lineSize: 2, lineDataSymbol: 'none', lineDash: 'solid', showValue: false } },
  ], {
    x: CH.x, y: CH.y, w: CH.w, h: CH.h, objectName: `Chart: ${s.label}`, layout: PL,
    showLegend: true, legendPos: 't', legendFontSize: 10, legendColor: C.ink, legendFontFace: '+mn-lt',
    catAxisLabelFontSize: LBL, catAxisLabelColor: C.ink, catAxisLabelFontFace: '+mn-lt', catGridLine: { style: 'none' },
    valAxisLabelFontSize: LBL, valAxisLabelColor: C.muted, valAxisLabelFontFace: '+mn-lt', valAxisLabelFormatCode: f.axis, valAxisMinVal: 0,
    valGridLine: { color: C.grid, size: 0.75 }, valAxisLineShow: false,
  });
  // logo row: one picture per bar group, centered under its category
  const n = s.categories.length;
  s.categories.forEach((c, i) => {
    const cx = CH.x + CH.w * (PL.x + PL.w * (i + 0.5) / n);
    slide.addImage({ path: path.join(LOGO_DIR, c.logo), x: cx - LOGO / 2, y: CH.y + CH.h + 0.08, w: LOGO, h: LOGO, objectName: `Logo: ${c.school}`, altText: `${c.school} logo` });
  });
  slide.addText(s.source, { x: M, y: HT - FOOT - 0.15, w: W - 2 * M - 0.7, h: FOOT, fontSize: 10, color: C.muted, align: 'left', valign: 'top', margin: 0, isTextBox: true, objectName: 'Source' });
  slide.addNotes(`To reuse this slide: duplicate it, right-click the chart and choose Edit Data, then replace the school names and numbers. The last two columns are the Power 4 average and median, repeated on every row; update them and rename the two series so the legend shows the new figures. The logos under the chart are separate pictures in the same order as the bars; swap them from the logo library on the last slide. Chart data: ${s.metric}; ${s.scope === 'conference' ? s.conference + ' schools' : 'all Power 4 schools with a value'}.`);
}
spec.slides.forEach(chartSlide);

// logo library: every school's logo with its name, to copy from when a chart is reused (two slides on a 4:3 deck)
(function library() {
  const cols = NARROW ? 7 : 12, perSlide = NARROW ? 35 : spec.logos.length, pages = Math.ceil(spec.logos.length / perSlide);
  const cw = (W - 2 * M) / cols, top = NARROW ? 1.9 : 1.95, rh = NARROW ? 0.95 : 0.84;
  for (let pg = 0; pg < pages; pg++) {
    const slide = pres.addSlide({ masterName: 'Chart slide' });
    slide.addText('Logo library: copy a logo from here when you swap a school into a chart' + (pages > 1 ? ` (${pg + 1} of ${pages})` : ''), { placeholder: 'title' });
    slide.addText(`All ${spec.logos.length} schools in the benchmarking workbook, in alphabetical order.`, { placeholder: 'body' });
    spec.logos.slice(pg * perSlide, (pg + 1) * perSlide).forEach((l, i) => {
      const x = M + (i % cols) * cw, y = top + Math.floor(i / cols) * rh;
      slide.addImage({ path: path.join(LOGO_DIR, l.file), x: x + (cw - 0.42) / 2, y, w: 0.42, h: 0.42, objectName: `Logo: ${l.school}`, altText: `${l.school} logo` });
      slide.addText(l.short, { x, y: y + 0.46, w: cw, h: 0.3, fontSize: 10, color: C.ink, align: 'center', valign: 'top', margin: 0, isTextBox: true, objectName: `Name: ${l.school}` });
    });
  }
})();

(async () => {
  await pres.writeFile({ fileName: outPath });
  // keep value labels on the first bar series only, so grouped charts stay readable
  const zip = await JSZip.loadAsync(fs.readFileSync(outPath));
  for (const name of Object.keys(zip.files).filter(n => /^ppt\/charts\/chart\d+\.xml$/.test(n))) {
    let xml = await zip.file(name).async('string');
    const m = xml.match(/<c:barChart>[\s\S]*?<\/c:barChart>/);
    if (!m) continue;
    let k = 0;
    const WHITE = '<c:spPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></c:spPr>';   // white behind each label so the average and median lines do not cross the figures
    const bar = m[0].replace(/<c:ser>[\s\S]*?<\/c:ser>/g, ser => (k++ === 0
      ? ser.replace(/(<c:dLbls><c:numFmt [^>]*\/>)/, '$1' + WHITE)
      : ser.replace(/<c:dLbls>[\s\S]*?<\/c:dLbls>/, '<c:dLbls><c:delete val="1"/></c:dLbls>')));
    xml = xml.replace(m[0], bar);
    // the median line (second line series) is dashed; pptxgenjs sets one dash style for the whole chart
    const lm = xml.match(/<c:lineChart>[\s\S]*?<\/c:lineChart>/);
    if (lm) { let j = 0; xml = xml.replace(lm[0], lm[0].replace(/<c:ser>[\s\S]*?<\/c:ser>/g, ser => (j++ === 1 ? ser.replace(/<a:prstDash val="solid"\/>/g, '<a:prstDash val="dash"/>') : ser))); }
    zip.file(name, xml);
  }
  const out = new JSZip();   // copy files only: folder entries in the package can stop a deck opening through a cloud service
  for (const name of Object.keys(zip.files)) if (!zip.files[name].dir) out.file(name, await zip.file(name).async('nodebuffer'), { createFolders: false });
  fs.writeFileSync(outPath, await out.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
  console.log('wrote', outPath, '| chart slides', spec.slides.length);
})();
