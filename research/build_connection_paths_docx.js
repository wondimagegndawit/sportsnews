const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, LevelFormat, AlignmentType } = require('docx');
const rows = JSON.parse(fs.readFileSync('v3_rows.json', 'utf8'));
const TIER = { '1': 'Tier 1', '2': 'Tier 2', '3': 'Tier 3', 'Untiered': 'Untiered schools' };
const order = [];
const groups = {};
for (const r of rows) {
  const k = [r.Tier, r.School, r['Target Name']].join('|');
  if (!groups[k]) { groups[k] = { tier: r.Tier, school: r.School, conf: r.Conference, name: r['Target Name'], company: r['Target Primary Company or Source of Wealth'], conns: [] }; order.push(k); }
  if (r['Smash Team Member'] !== '--') groups[k].conns.push(r); else groups[k].none = r['Connection Detail'];
}
const F = 'Arial';
const t = (text, opts = {}) => new TextRun({ text, font: F, size: 20, ...opts });
const children = [];
children.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [t('Smash Sports booster connection paths', { size: 40, bold: true })] }));
children.push(new Paragraph({ children: [t('Booster-first paths only: each sub-bullet is a Smash team member and how they connect to the booster without asking the school for the introduction. Research only; no outreach made. Built from Smash_Booster_Connection_Map_v3_booster_first (2026-11-02). Confidence in brackets: Confirmed, Strong inference, or Hypothesis.', { italics: true, size: 18 })], spacing: { after: 200 } }));
let lastTier = null, lastSchool = null;
for (const k of order) {
  const g = groups[k];
  if (g.tier !== lastTier) { children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t(TIER[g.tier], { size: 28, bold: true })], spacing: { before: 240 } })); lastTier = g.tier; lastSchool = null; }
  if (g.school !== lastSchool) { children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(`${g.school} (${g.conf})`, { size: 24, bold: true })], spacing: { before: 160 } })); lastSchool = g.school; }
  const short = (g.company || '').split(/(?<=[.;])\s/)[0].slice(0, 160);
  children.push(new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { before: 80 }, children: [t(g.name, { bold: true }), t(short ? ` — ${short}` : '', { color: '444444' })] }));
  if (!g.conns.length) {
    children.push(new Paragraph({ numbering: { reference: 'bul', level: 1 }, children: [t(g.none && g.none.startsWith('No booster-first') ? 'No booster-first path found; every documented route runs through the school.' : 'No connection found.', { italics: true })] }));
    continue;
  }
  for (const c of g.conns) {
    children.push(new Paragraph({ numbering: { reference: 'bul', level: 1 }, children: [t(c['Smash Team Member'], { bold: true }), t(` [${c['Connection Type']}, ${c.Confidence}] `, { color: '555555' }), t(c['Connection Detail'])] }));
    if (c['Suggested warm intro path'] && c['Suggested warm intro path'] !== '--')
      children.push(new Paragraph({ numbering: { reference: 'bul', level: 2 }, children: [t('How to reach: ', { italics: true }), t(c['Suggested warm intro path'], { italics: true, color: '333333' })] }));
  }
}
const doc = new Document({
  styles: { default: { document: { run: { font: F, size: 20 } } } },
  numbering: { config: [{ reference: 'bul', levels: [
    { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 360 } } } },
    { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 900, hanging: 360 } } } },
    { level: 2, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
  ] }] },
  sections: [{ properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } }, children }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync('/home/user/sportsnews/research/Smash_Booster_Connection_Paths_v3.docx', b); console.log('wrote', b.length, 'bytes;', order.length, 'boosters'); });
