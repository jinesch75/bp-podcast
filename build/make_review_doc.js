// Builds the partner review Word document for one capsule: intro (FR) + script & quiz in FR, DE, EN.
// Usage (from the project root): node build/make_review_doc.js <key>[,<key>...]
// Reads podcast_script_<key>{_fr,_de,}.md, the quiz/titles/durations from episodes_data.js and the review
// token from build/review_tokens.json; writes "Relecture partenaires/Biergerpakt_Capsule_<key>_relecture.docx"
// (folder is git-ignored). Make sure the scripts match the recorded audio before sending.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Header, Footer,
  PageNumber, PageBreak, BorderStyle, ExternalHyperlink, ShadingType,
} = require('docx');

const ROOT = path.join(__dirname, '..');
const E = new Function(fs.readFileSync(path.join(ROOT, 'episodes_data.js'), 'utf8') + ';return EPISODES;')();
const TOK = JSON.parse(fs.readFileSync(path.join(__dirname, 'review_tokens.json'), 'utf8'));
const OUTDIR = path.join(ROOT, 'Relecture partenaires'); fs.mkdirSync(OUTDIR, { recursive: true });
for (const key of process.argv[2].split(',')) build(key);
function build(key) {
const dir = ROOT;
const e = E.find((x) => x.key === key); if (!e) throw new Error('unknown key ' + key);
const Q = {};
for (const L of ['', '_fr', '_de']) { Q['title' + L] = e['title' + L]; Q['duration' + L] = e['duration' + L]; Q['questions' + L] = e['questions' + L].map((q) => ({ t: q.text, o: q.options, c: q.correct, x: q.explanation })); }
const reviewUrl = `https://bp-podcast-production.up.railway.app/review/${key.replace(/_/g, '-')}-${TOK[key]}/`;
const out = path.join(OUTDIR, `Biergerpakt_Capsule_${key}_relecture.docx`);
const FONT = 'Arial';

const LANGS = [
  { sfx: '_fr', q: '_fr', name: 'Version française', script: 'Script', quiz: 'Quiz', dur: 'Durée', ok: 'Bonne réponse', expl: 'Explication', src: 'Sources', c: ' : ' },
  { sfx: '_de', q: '_de', name: 'Deutsche Fassung', script: 'Skript', quiz: 'Quiz', dur: 'Dauer', ok: 'Richtige Antwort', expl: 'Erklärung', src: 'Quellen', c: ': ' },
  { sfx: '', q: '', name: 'English version', script: 'Script', quiz: 'Quiz', dur: 'Length', ok: 'Correct answer', expl: 'Explanation', src: 'Sources', c: ': ' },
];

const mmss = (s) => `${Math.floor(s / 60)} min ${String(Math.round(s % 60)).padStart(2, '0')}`;
const p = (children, opts = {}) => new Paragraph({ children, ...opts });
const t = (text, o = {}) => new TextRun({ text, font: FONT, ...o });

function parseScript(file) {
  const md = fs.readFileSync(file, 'utf8');
  const turns = [...md.matchAll(/^\*\*(ANNA|TOM)\s?:\*\*\s?(.*)$/gm)].map((m) => ({ sp: m[1], text: m[2].trim() }));
  const src = [...md.matchAll(/^\*([^*].*)\*\s*$/gm)].map((m) => m[1].trim()).pop() || '';
  return { turns, src };
}

const children = [];
// ---- Cover / instructions (French) ----
children.push(p([t('Biergerpakt – capsule audio', { size: 24, color: '595959' })], { spacing: { after: 80 } }));
children.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [t(Q.title_fr, { size: 40, bold: true })] }));
children.push(p([t(`Document de relecture – version du ${new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}`, { size: 22, italics: true, color: '595959' })], { spacing: { after: 360 } }));

children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t('Comment relire ce document')] }));
const intro = [
  'Ce document contient le script de la capsule audio et le quiz qui l\'accompagne, en français, en allemand et en anglais. Le texte correspond mot pour mot à l\'enregistrement.',
  'Vous pouvez relire dans la langue de votre choix : nous reporterons vos corrections dans les autres langues.',
  'Pour proposer une correction, activez le mode « Suivi des modifications » (onglet Révision) puis modifiez directement le texte, ou ajoutez un commentaire. Vous pouvez aussi simplement nous décrire les erreurs par e-mail.',
  'Dans le quiz, la bonne réponse est indiquée en vert. Merci de vérifier aussi les questions, les réponses et les explications.',
];
const bullet = (txt) => new Paragraph({ numbering: { reference: 'bullets', level: 0 }, spacing: { after: 80 }, children: [t(txt)] });
intro.forEach((s) => children.push(bullet(s)));
children.push(p([t('Écouter la capsule (version interne, merci de ne pas diffuser) : ', { bold: true }),
  new ExternalHyperlink({ link: reviewUrl, children: [new TextRun({ text: reviewUrl, font: FONT, style: 'Hyperlink' })] })], { spacing: { before: 160, after: 160 } }));

children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t('Contenu')] }));
LANGS.forEach((L, i) => children.push(p([t(`${i + 1}. ${L.name} – ${L.script} (${mmss(Q['duration' + L.q])}) et ${L.quiz.toLowerCase()}`)], { spacing: { after: 60 } })));

// ---- Per language: script + quiz ----
LANGS.forEach((L, li) => {
  const { turns, src } = parseScript(path.join(dir, `podcast_script_${key}${L.sfx}.md`));
  children.push(new Paragraph({ children: [new PageBreak()] }));
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t(`${li + 1}. ${L.name}`)] }));
  children.push(p([t(Q['title' + L.q], { bold: true, size: 26 })], { spacing: { after: 120 } }));
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(`${L.script}`)] }));
  children.push(p([t(`${L.dur}${L.c}${mmss(Q['duration' + L.q])} · Anna & Tom`, { italics: true, color: '595959', size: 20 })], { spacing: { after: 160 } }));
  turns.forEach((tu) => children.push(new Paragraph({
    spacing: { after: 140, line: 300 },
    children: [t(tu.sp === 'ANNA' ? 'Anna' : 'Tom', { bold: true, color: tu.sp === 'ANNA' ? '7B2C5A' : '1F4E79' }), t(L.c), t(tu.text)],
  })));
  if (src) children.push(p([t(`${L.src}${L.c}`, { italics: true, bold: true, size: 18, color: '595959' }), t(src.replace(/^(Sources?|Quellen?)\s*:\s*/i, ''), { italics: true, size: 18, color: '595959' })], { spacing: { before: 200 } }));

  children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, pageBreakBefore: true, children: [t(L.quiz)] }));
  Q['questions' + L.q].forEach((q, qi) => {
    children.push(p([t(`${qi + 1}. ${q.t}`, { bold: true })], { spacing: { before: 240, after: 100 }, keepNext: true }));
    q.o.forEach((o, oi) => {
      const ok = oi === q.c;
      children.push(new Paragraph({
        indent: { left: 360 }, spacing: { after: 60 }, keepNext: true,
        shading: ok ? { type: ShadingType.CLEAR, fill: 'E2EFDA', color: 'auto' } : undefined,
        children: [t(`${'abcd'[oi]})  `, { bold: ok }), t(o, { bold: ok, color: ok ? '375623' : undefined }), ...(ok ? [t(`   ✓ ${L.ok}`, { bold: true, color: '375623', size: 18 })] : [])],
      }));
    });
    children.push(p([t(`${L.expl}${L.c}`, { italics: true, bold: true, size: 20 }), t(q.x, { italics: true, size: 20 })], { indent: { left: 360 }, spacing: { before: 80, after: 120 } }));
  });
});

const doc = new Document({
  creator: 'Biergerpakt – MIFA',
  title: `Capsule audio – ${Q.title_fr} – relecture`,
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', run: { font: FONT, size: 40, bold: true, color: '1F3864' }, paragraph: { spacing: { before: 0, after: 120 }, keepNext: true } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 32, bold: true, color: '1F3864' }, paragraph: { spacing: { before: 240, after: 160 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 26, bold: true, color: '2E5597' }, paragraph: { spacing: { before: 240, after: 120 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: 'bullet', text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { margin: { top: 1300, bottom: 1200, left: 1300, right: 1300 } } },
    headers: { default: new Header({ children: [p([t(`Biergerpakt – capsule audio « ${Q.title_fr.split(' – ')[0]} » – document de relecture`, { size: 16, color: '7F7F7F' })], { border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 4 } } })] }) },
    footers: { default: new Footer({ children: [p([t('Page ', { size: 16, color: '7F7F7F' }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: '7F7F7F' }), t(' / ', { size: 16, color: '7F7F7F' }), new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: '7F7F7F' })], { alignment: AlignmentType.CENTER })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(out, b);
  // drop the ZIP's folder entries (Word can refuse such files when opened through cloud co-editing)
  require('child_process').execFileSync('python3', ['-c', "import sys,zipfile,shutil\np=sys.argv[1];t=p+'.tmp'\nwith zipfile.ZipFile(p) as a, zipfile.ZipFile(t,'w',zipfile.ZIP_DEFLATED) as b:\n  [b.writestr(i,a.read(i)) for i in a.infolist() if not i.filename.endswith('/')]\nshutil.move(t,p)", out]);
  console.log('written', out);
});
}
