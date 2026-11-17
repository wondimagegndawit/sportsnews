// Mock-up of the three deal slides (jersey patch, stadium naming, arena naming) in the Smash deck layout, with a
// Sponsor row and a Terms row under the logos. Charts are native PowerPoint charts.
// Usage: NODE_PATH=<dir with pptxgenjs>/node_modules node scripts/build_deal_mockups.js slides/spec_deal_mockups.json out.pptx
const fs = require('fs'), path = require('path');
const pptxgen = require('pptxgenjs');
const JSZip = require('jszip');
const [specPath, outPath] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const LOGO_DIR = path.join(path.dirname(specPath), 'logos');
const W = 10, HT = 7.5, F = 'Montserrat';
const C = { page: 'EDEDED', panel: 'FFFFFF', ink: '000000', line: '9DC3E6', muted: '595959', rule: 'BFBFBF' };
const money = v => '$' + (v / 1e6).toFixed(1) + 'M';
// geometry (inches): white panel, legend box, chart, logo row, two table rows
const PANEL = { x: 0.35, y: 1.3, w: 9.3, h: 5.62 };
const CH = { x: 0.5, y: 2.4, w: 9.0, h: 2.55 }, PL = { x: 0.09, y: 0.07, w: 0.9, h: 0.9 };
const ROW = { label: 0.45, labelW: 0.8, sponsorY: 5.58, termsY: 6.14, h: 0.56 };

const pres = new pptxgen();
pres.defineLayout({ name: 'SMASH', width: W, height: HT });
pres.layout = 'SMASH';
pres.theme = { headFontFace: F, bodyFontFace: F };
pres.title = 'Deal slides with sponsor and terms rows: mock-up';

spec.forEach((s, idx) => {
  const slide = pres.addSlide();
  slide.background = { color: C.page };
  const n = s.schools.length, dense = n > 8;
  slide.addText(s.title, { x: 0.35, y: 0.2, w: 9.3, h: 0.38, fontFace: F, fontSize: 18, bold: true, color: C.ink, margin: 0, valign: 'middle', isTextBox: true, objectName: 'Title' });
  slide.addText(s.subtitle, { x: 0.36, y: 0.6, w: 9.0, h: 0.44, fontFace: F, fontSize: 9.5, bold: true, color: C.ink, margin: 0, valign: 'top', isTextBox: true, objectName: 'Subtitle' });
  slide.addShape(pres.shapes.LINE, { x: 0.35, y: 1.1, w: 9.3, h: 0, line: { color: C.ink, width: 0.75 } });
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: PANEL.x, y: PANEL.y, w: PANEL.w, h: PANEL.h, fill: { color: C.panel }, line: { color: C.panel, width: 0 }, rectRadius: 0.08, objectName: 'Panel' });
  // legend box
  const LG = { x: 0.55, y: 1.42, w: 2.3, h: 0.9 };
  slide.addShape(pres.shapes.RECTANGLE, { x: LG.x, y: LG.y, w: LG.w, h: LG.h, fill: { color: C.panel }, line: { color: C.ink, width: 0.75 }, objectName: 'Legend box' });
  const ly = i => LG.y + 0.12 + i * 0.26;
  slide.addShape(pres.shapes.RECTANGLE, { x: LG.x + 0.1, y: ly(0), w: 0.36, h: 0.14, fill: { color: C.ink }, line: { color: C.ink, width: 0 } });
  slide.addShape(pres.shapes.LINE, { x: LG.x + 0.1, y: ly(1) + 0.07, w: 0.36, h: 0, line: { color: C.line, width: 1.5 } });
  slide.addShape(pres.shapes.LINE, { x: LG.x + 0.1, y: ly(2) + 0.07, w: 0.36, h: 0, line: { color: C.line, width: 1.5, dashType: 'dash' } });
  [`= Annual Value`, `= P4 Average (${money(s.avg)})`, `= P4 Median (${money(s.med)})`].forEach((t, i) =>
    slide.addText(t, { x: LG.x + 0.52, y: ly(i) - 0.03, w: LG.w - 0.6, h: 0.2, fontFace: F, fontSize: 7, color: C.ink, margin: 0, valign: 'middle', isTextBox: true }));
  // chart: bars plus average and median lines
  const labels = s.schools.map(x => x.school);
  slide.addChart([
    { type: pres.charts.BAR, data: [{ name: 'Annual Value', labels, values: s.schools.map(x => x.value || 0) }],
      options: { barDir: 'col', barGapWidthPct: dense ? 45 : 60, chartColors: [C.ink], showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '$#,##0.0,,"M";;', dataLabelFontSize: 8, dataLabelColor: C.ink, dataLabelFontFace: '+mn-lt' } },
    { type: pres.charts.LINE, data: [{ name: 'P4 Average', labels, values: labels.map(() => s.avg) }, { name: 'P4 Median', labels, values: labels.map(() => s.med) }],
      options: { chartColors: [C.line, C.line], lineSize: 1.5, lineDataSymbol: 'none', lineDash: 'solid', showValue: false } },
  ], { x: CH.x, y: CH.y, w: CH.w, h: CH.h, objectName: `Chart: ${s.key}`, layout: PL, showLegend: false,
    catAxisHidden: true, catGridLine: { style: 'none' },
    valAxisLabelFontSize: 8, valAxisLabelColor: C.ink, valAxisLabelFontFace: '+mn-lt', valAxisLabelFormatCode: '$#,##0,,"M"', valAxisMinVal: 0,
    valGridLine: { color: C.ink, size: 0.5 }, valAxisLineShow: true });
  // logos, then the Sponsor and Terms rows, one cell under each bar
  const logo = dense ? 0.36 : 0.46, logoY = CH.y + CH.h + 0.04;
  const band = CH.w * PL.w / n, cx = i => CH.x + CH.w * (PL.x + PL.w * (i + 0.5) / n);
  const fs2 = dense ? 6 : 8;
  // shrink a cell's font when its longest word would not fit the column (Montserrat is about 0.62 em per character)
  const fit = t => { const longest = Math.max(...t.split(/\s+/).map(w => w.length)); return Math.max(4.5, Math.min(fs2, Math.floor(2 * (band - 0.04) * 72 / (0.62 * longest)) / 2)); };
  const compact = t => (dense ? t.replace(' years', ' yrs').replace(' total', '').replace('Through', 'Thru').replace(' a year', '/yr') : t);
  [ROW.sponsorY, ROW.termsY, ROW.termsY + ROW.h].forEach(y => slide.addShape(pres.shapes.LINE, { x: ROW.label, y, w: W - 2 * ROW.label, h: 0, line: { color: C.rule, width: 0.5 } }));
  slide.addText('Sponsor', { x: ROW.label, y: ROW.sponsorY, w: ROW.labelW, h: ROW.h, fontFace: F, fontSize: 8, bold: true, color: C.ink, margin: 0, valign: 'middle', isTextBox: true, objectName: 'Row label: Sponsor' });
  slide.addText('Terms', { x: ROW.label, y: ROW.termsY, w: ROW.labelW, h: ROW.h, fontFace: F, fontSize: 8, bold: true, color: C.ink, margin: 0, valign: 'middle', isTextBox: true, objectName: 'Row label: Terms' });
  s.schools.forEach((x, i) => {
    slide.addImage({ path: path.join(LOGO_DIR, x.logo), x: cx(i) - logo / 2, y: logoY, w: logo, h: logo, objectName: `Logo: ${x.school}`, altText: `${x.school} logo` });
    slide.addText(x.sponsor, { x: cx(i) - band / 2 + 0.01, y: ROW.sponsorY, w: band - 0.02, h: ROW.h, fontFace: F, fontSize: fit(x.sponsor), color: C.ink, align: 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: `Sponsor: ${x.school}` });
    slide.addText(x.terms.map(compact).join('\n'), { x: cx(i) - band / 2 + 0.01, y: ROW.termsY, w: band - 0.02, h: ROW.h, fontFace: F, fontSize: fs2, color: C.ink, align: 'center', valign: 'middle', margin: 0, isTextBox: true, objectName: `Terms: ${x.school}` });
  });
  // footer
  slide.addText([{ text: 'SMASH', options: { bold: true } }, { text: 'SPORTS  |  CONFIDENTIAL' }], { x: 6.2, y: 7.05, w: 3.0, h: 0.25, fontFace: F, fontSize: 7, color: C.ink, align: 'right', valign: 'middle', margin: 0, isTextBox: true, objectName: 'Footer' });
  slide.addText(String(idx + 1), { x: 9.3, y: 7.05, w: 0.35, h: 0.25, fontFace: F, fontSize: 7, color: C.ink, align: 'right', valign: 'middle', margin: 0, isTextBox: true, objectName: 'Page number' });
});

(async () => {
  await pres.writeFile({ fileName: outPath });
  const zip = await JSZip.loadAsync(fs.readFileSync(outPath));
  for (const name of Object.keys(zip.files).filter(n => /^ppt\/charts\/chart\d+\.xml$/.test(n))) {
    let xml = await zip.file(name).async('string');
    // white behind each value label, and a dashed median line
    xml = xml.replace(/(<c:barChart>[\s\S]*?<c:dLbls><c:numFmt [^>]*\/>)/, '$1<c:spPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></c:spPr>');
    const lm = xml.match(/<c:lineChart>[\s\S]*?<\/c:lineChart>/);
    if (lm) { let j = 0; xml = xml.replace(lm[0], lm[0].replace(/<c:ser>[\s\S]*?<\/c:ser>/g, ser => (j++ === 1 ? ser.replace(/<a:prstDash val="solid"\/>/g, '<a:prstDash val="dash"/>') : ser))); }
    zip.file(name, xml);
  }
  const out = new JSZip();
  for (const name of Object.keys(zip.files)) if (!zip.files[name].dir) out.file(name, await zip.file(name).async('nodebuffer'), { createFolders: false });
  fs.writeFileSync(outPath, await out.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
  console.log('wrote', outPath, '| slides', spec.length);
})();
