// ── Biergerpakt Podcast – app logic ──────────────────────
let user = {};
let selectedEpisode = null;

// Quiz state
let answers = [];
let wrongIndices = [];
let retryIndices = [];
let retryPos = 0;
let curIndex = 0;
let isRetry = false;

// Transcript / audio sync state
let segEls = [];
let segTimes = [];
let activeSeg = -1;
let userScrolling = false;
let userScrollTimer = null;
let currentLang = 'en';   // site language: UI, audio, quiz, content, AND transcript (en | fr | de)
// The transcript always shows the chosen UI language. Other-language scripts (incl. Luxembourgish)
// remain in the data (segments_lb etc.) but are not displayed.

// ── i18n: interface strings ──────────────────────────────
const I18N = {
  en: {
    podcast_name: 'The Biergerpakt Podcast',
    reg_tag: 'Biergerpakt · Podcast Programme',
    reg_intro: 'Living together in Luxembourg – discover the country, listen to each episode, follow along with the script, and prove what you have learned. Complete a quiz to earn your personal certificate.',
    reg_card_title: 'Your details',
    reg_card_sub: 'Please tell us your name. It is used only to personalise your certificate – nothing is sent anywhere or stored online.',
    label_first: 'First name *', ph_first: 'First name', err_first: 'Please enter your first name.',
    label_last: 'Last name *', ph_last: 'Last name', err_last: 'Please enter your last name.',
    label_email: 'Email address (optional)', ph_email: 'you@email.com',
    hint_email: 'Optional. Used only if it appears on your certificate.',
    btn_browse: 'Browse the episodes →',
    programme_badge: 'Biergerpakt · Podcast Programme',
    episodes_h1: 'The Biergerpakt Podcast – All Episodes',
    episodes_intro: 'Choose an episode, listen along with the full script, then take the quiz to earn your personal certificate.',
    btn_listen_quiz: 'Listen & take the quiz →',
    filter_heading: 'Browse by topic',
    filter_all: 'All topics',
    eps_count: '{n} of {total} episodes',
    btn_all_episodes: '← All episodes',
    listen_title: '🎧 Listen to this episode',
    player_hint: 'Press play and the script below will highlight along with the audio. Click any line to jump to that point.',
    script_title: '📝 Episode script',
    autoscroll: 'Auto-scroll with audio',
    lang_note_tmpl: 'The audio is in {lang}. This script is shown for reading along.',
    topics_title: '📋 Topics in this episode',
    quiz_cta_h2: 'Ready for the quiz?',
    quiz_cta_p: 'Answer 5 questions about this episode. All answers must be correct to earn your personal certificate of participation.',
    btn_start_quiz: 'Start the quiz →',
    quiz_cta_meta: '5 questions · Multiple choice · Wrong answers come back at the end until you get them right',
    episode_word: 'Episode',
    q_counter: 'Question {n} of {total}',
    q_word: 'Question',
    fb_ok: '✅ Correct!',
    fb_fail_prefix: '❌ Not quite.',
    fb_fail_mid: 'The correct answer is:',
    btn_next: 'Next →',
    of_word: 'of',
    res_all_title: '🎉 Excellent – all correct!',
    res_all_msg: 'You answered every question correctly. You can now download your certificate of participation.',
    res_partial_title: '{n} of {total} questions correct',
    res_partial_msg: 'To earn the certificate, every question must be correct. Listen again to the relevant parts of the episode, then retry the questions below.',
    retry_h3: '⚠️ Questions you answered incorrectly',
    retry_p: 'Listen again to the relevant parts of the episode and try these questions once more. You must answer all questions correctly to earn the certificate.',
    btn_retry: 'Try the incorrect questions again →',
    success_p: '🎉 Congratulations! You answered every question correctly.',
    btn_get_cert: 'Get my certificate 🎓',
    btn_choose_another: '← Choose another episode',
    cert_label: 'Certificate of Participation',
    cert_body1: 'This is to certify that',
    cert_body2: 'has listened to the following podcast episode and successfully completed the knowledge quiz:',
    cert_verified: 'Verified',
    cert_email_label: 'Email:',
    cert_date_label: 'Date of issue:',
    btn_print: '🖨️ Print / Save as PDF',
    btn_back_episode: '← Back to the episode'
  },
  fr: {
    podcast_name: 'Le podcast Biergerpakt',
    reg_tag: 'Programme Biergerpakt · Podcast',
    reg_intro: 'Vivre ensemble au Luxembourg – découvrez le pays, écoutez chaque épisode, suivez le script et prouvez ce que vous avez appris. Réussissez un quiz pour obtenir votre certificat personnel.',
    reg_card_title: 'Vos coordonnées',
    reg_card_sub: 'Indiquez-nous votre nom. Il sert uniquement à personnaliser votre certificat – rien n’est envoyé ni stocké en ligne.',
    label_first: 'Prénom *', ph_first: 'Prénom', err_first: 'Veuillez saisir votre prénom.',
    label_last: 'Nom *', ph_last: 'Nom', err_last: 'Veuillez saisir votre nom.',
    label_email: 'Adresse e-mail (facultatif)', ph_email: 'vous@email.com',
    hint_email: 'Facultatif. Utilisé uniquement s’il figure sur votre certificat.',
    btn_browse: 'Parcourir les épisodes →',
    programme_badge: 'Programme Biergerpakt · Podcast',
    episodes_h1: 'Le podcast Biergerpakt – tous les épisodes',
    episodes_intro: 'Choisissez un épisode, écoutez-le en suivant le script complet, puis répondez au quiz pour obtenir votre certificat personnel.',
    btn_listen_quiz: 'Écouter et faire le quiz →',
    filter_heading: 'Parcourir par sujet',
    filter_all: 'Tous les sujets',
    eps_count: '{n} sur {total} épisodes',
    btn_all_episodes: '← Tous les épisodes',
    listen_title: '🎧 Écouter cet épisode',
    player_hint: 'Appuyez sur lecture et le script ci-dessous se surlignera au rythme de l’audio. Cliquez sur une ligne pour y accéder directement.',
    script_title: '📝 Script de l’épisode',
    autoscroll: 'Défilement automatique avec l’audio',
    lang_note_tmpl: 'L’audio est en {lang}. Ce script est affiché pour suivre la lecture.',
    topics_title: '📋 Sujets de cet épisode',
    quiz_cta_h2: 'Prêt pour le quiz ?',
    quiz_cta_p: 'Répondez à 5 questions sur cet épisode. Toutes les réponses doivent être correctes pour obtenir votre certificat de participation personnel.',
    btn_start_quiz: 'Commencer le quiz →',
    quiz_cta_meta: '5 questions · Choix multiple · Les mauvaises réponses reviennent à la fin jusqu’à ce qu’elles soient justes',
    episode_word: 'Épisode',
    q_counter: 'Question {n} sur {total}',
    q_word: 'Question',
    fb_ok: '✅ Correct !',
    fb_fail_prefix: '❌ Pas tout à fait.',
    fb_fail_mid: 'La bonne réponse est :',
    btn_next: 'Suivant →',
    of_word: 'sur',
    res_all_title: '🎉 Excellent – tout est juste !',
    res_all_msg: 'Vous avez répondu correctement à toutes les questions. Vous pouvez maintenant télécharger votre certificat de participation.',
    res_partial_title: '{n} sur {total} questions correctes',
    res_partial_msg: 'Pour obtenir le certificat, toutes les questions doivent être correctes. Réécoutez les passages concernés de l’épisode, puis recommencez les questions ci-dessous.',
    retry_h3: '⚠️ Questions auxquelles vous avez mal répondu',
    retry_p: 'Réécoutez les passages concernés de l’épisode et réessayez ces questions. Vous devez répondre correctement à toutes les questions pour obtenir le certificat.',
    btn_retry: 'Réessayer les questions incorrectes →',
    success_p: '🎉 Félicitations ! Vous avez répondu correctement à toutes les questions.',
    btn_get_cert: 'Obtenir mon certificat 🎓',
    btn_choose_another: '← Choisir un autre épisode',
    cert_label: 'Certificat de participation',
    cert_body1: 'Le présent document certifie que',
    cert_body2: 'a écouté l’épisode de podcast suivant et réussi le quiz de connaissances :',
    cert_verified: 'Vérifié',
    cert_email_label: 'E-mail :',
    cert_date_label: 'Date de délivrance :',
    btn_print: '🖨️ Imprimer / Enregistrer en PDF',
    btn_back_episode: '← Retour à l’épisode'
  },
  de: {
    podcast_name: 'Der Biergerpakt-Podcast',
    reg_tag: 'Biergerpakt · Podcast-Programm',
    reg_intro: 'Zusammenleben in Luxemburg – entdecken Sie das Land, hören Sie jede Folge, lesen Sie das Skript mit und beweisen Sie, was Sie gelernt haben. Absolvieren Sie ein Quiz, um Ihr persönliches Zertifikat zu erhalten.',
    reg_card_title: 'Ihre Angaben',
    reg_card_sub: 'Bitte teilen Sie uns Ihren Namen mit. Er wird nur verwendet, um Ihr Zertifikat zu personalisieren – nichts wird irgendwohin gesendet oder online gespeichert.',
    label_first: 'Vorname *', ph_first: 'Vorname', err_first: 'Bitte geben Sie Ihren Vornamen ein.',
    label_last: 'Nachname *', ph_last: 'Nachname', err_last: 'Bitte geben Sie Ihren Nachnamen ein.',
    label_email: 'E-Mail-Adresse (optional)', ph_email: 'sie@email.com',
    hint_email: 'Optional. Wird nur verwendet, wenn sie auf Ihrem Zertifikat erscheint.',
    btn_browse: 'Folgen durchsuchen →',
    programme_badge: 'Biergerpakt · Podcast-Programm',
    episodes_h1: 'Der Biergerpakt-Podcast – alle Folgen',
    episodes_intro: 'Wählen Sie eine Folge, hören Sie mit dem vollständigen Skript mit und absolvieren Sie dann das Quiz, um Ihr persönliches Zertifikat zu erhalten.',
    btn_listen_quiz: 'Anhören & Quiz machen →',
    filter_heading: 'Nach Thema stöbern',
    filter_all: 'Alle Themen',
    eps_count: '{n} von {total} Folgen',
    btn_all_episodes: '← Alle Folgen',
    listen_title: '🎧 Diese Folge anhören',
    player_hint: 'Drücken Sie auf Wiedergabe, und das Skript unten wird im Takt des Audios hervorgehoben. Klicken Sie auf eine Zeile, um direkt dorthin zu springen.',
    script_title: '📝 Skript der Folge',
    autoscroll: 'Automatisch mit dem Audio scrollen',
    lang_note_tmpl: 'Das Audio ist auf {lang}. Dieses Skript dient zum Mitlesen.',
    topics_title: '📋 Themen dieser Folge',
    quiz_cta_h2: 'Bereit für das Quiz?',
    quiz_cta_p: 'Beantworten Sie 5 Fragen zu dieser Folge. Alle Antworten müssen richtig sein, um Ihr persönliches Teilnahmezertifikat zu erhalten.',
    btn_start_quiz: 'Quiz starten →',
    quiz_cta_meta: '5 Fragen · Multiple Choice · Falsche Antworten kommen am Ende wieder, bis sie richtig sind',
    episode_word: 'Folge',
    q_counter: 'Frage {n} von {total}',
    q_word: 'Frage',
    fb_ok: '✅ Richtig!',
    fb_fail_prefix: '❌ Nicht ganz.',
    fb_fail_mid: 'Die richtige Antwort lautet:',
    btn_next: 'Weiter →',
    of_word: 'von',
    res_all_title: '🎉 Ausgezeichnet – alles richtig!',
    res_all_msg: 'Sie haben alle Fragen richtig beantwortet. Sie können jetzt Ihr Teilnahmezertifikat herunterladen.',
    res_partial_title: '{n} von {total} Fragen richtig',
    res_partial_msg: 'Um das Zertifikat zu erhalten, müssen alle Fragen richtig sein. Hören Sie sich die betreffenden Teile der Folge noch einmal an und versuchen Sie dann die folgenden Fragen erneut.',
    retry_h3: '⚠️ Falsch beantwortete Fragen',
    retry_p: 'Hören Sie sich die betreffenden Teile der Folge noch einmal an und versuchen Sie diese Fragen erneut. Sie müssen alle Fragen richtig beantworten, um das Zertifikat zu erhalten.',
    btn_retry: 'Falsche Fragen erneut versuchen →',
    success_p: '🎉 Glückwunsch! Sie haben alle Fragen richtig beantwortet.',
    btn_get_cert: 'Mein Zertifikat erhalten 🎓',
    btn_choose_another: '← Eine andere Folge wählen',
    cert_label: 'Teilnahmezertifikat',
    cert_body1: 'Hiermit wird bescheinigt, dass',
    cert_body2: 'die folgende Podcast-Folge angehört und das Wissensquiz erfolgreich abgeschlossen hat:',
    cert_verified: 'Verifiziert',
    cert_email_label: 'E-Mail:',
    cert_date_label: 'Ausstellungsdatum:',
    btn_print: '🖨️ Drucken / Als PDF speichern',
    btn_back_episode: '← Zurück zur Folge'
  },
  lb: {
    podcast_name: 'De Biergerpakt-Podcast',
    reg_tag: 'Biergerpakt · Podcast-Programm',
    reg_intro: 'Zesummeliewen zu Lëtzebuerg – entdeckt d’Land, lauschtert all Episode, liest de Skript mat a beweist, wat Dir geléiert hutt. Maacht e Quiz fir Äre perséinleche Certificat ze kréien.',
    reg_card_title: 'Är Donnéeën',
    reg_card_sub: 'Sot eis w.e.g. Ären Numm. Hie gëtt nëmme benotzt fir Äre Certificat ze perséinaliséieren – näischt gëtt iergendwouhin geschéckt oder online gespäichert.',
    label_first: 'Virnumm *', ph_first: 'Virnumm', err_first: 'Gitt w.e.g. Äre Virnumm an.',
    label_last: 'Numm *', ph_last: 'Numm', err_last: 'Gitt w.e.g. Äre Numm an.',
    label_email: 'E-Mail-Adress (fakultativ)', ph_email: 'iech@email.com',
    hint_email: 'Fakultativ. Gëtt nëmme benotzt wann se op Ärem Certificat erschéngt.',
    btn_browse: 'D’Episode kucken →',
    programme_badge: 'Biergerpakt · Podcast-Programm',
    episodes_h1: 'De Biergerpakt-Podcast – all Episoden',
    episodes_intro: 'Wielt eng Episode, lauschtert se mam komplette Skript mat, a maacht dann de Quiz fir Äre perséinleche Certificat ze kréien.',
    btn_listen_quiz: 'Lauschteren & Quiz maachen →',
    filter_heading: 'No Thema kucken',
    filter_all: 'All Themen',
    eps_count: '{n} vu(n) {total} Episoden',
    btn_all_episodes: '← All Episoden',
    listen_title: '🎧 Dës Episode lauschteren',
    player_hint: 'Dréckt op Play an de Skript hei ënnen gëtt am Takt vum Audio ervirgehuewen. Klickt op eng Zeil fir direkt dohinner ze sprangen.',
    script_title: '📝 Skript vun der Episode',
    autoscroll: 'Automatesch mam Audio scrollen',
    lang_note_tmpl: 'Den Audio ass op {lang}. Dëse Skript gëtt fir matzelauschteren ugewisen.',
    topics_title: '📋 Themen an dëser Episode',
    quiz_cta_h2: 'Prett fir de Quiz?',
    quiz_cta_p: 'Beäntwert 5 Froen zu dëser Episode. All Äntwerte musse richteg sinn fir Äre perséinleche Participatiouns-Certificat ze kréien.',
    btn_start_quiz: 'De Quiz starten →',
    quiz_cta_meta: '5 Froen · Multiple Choice · Falsch Äntwerte kommen um Enn erëm, bis se richteg sinn',
    episode_word: 'Episode',
    q_counter: 'Fro {n} vu(n) {total}',
    q_word: 'Fro',
    fb_ok: '✅ Richteg!',
    fb_fail_prefix: '❌ Net ganz.',
    fb_fail_mid: 'Déi richteg Äntwert ass:',
    btn_next: 'Weider →',
    of_word: 'vu(n)',
    res_all_title: '🎉 Excellent – alles richteg!',
    res_all_msg: 'Dir hutt all Froe richteg beäntwert. Dir kënnt elo Äre Participatiouns-Certificat eroflueden.',
    res_partial_title: '{n} vu(n) {total} Froe richteg',
    res_partial_msg: 'Fir de Certificat ze kréien, musse all Froe richteg sinn. Lauschtert déi betreffend Deeler vun der Episode nach eng Kéier, a probéiert dann déi ënnescht Froen erëm.',
    retry_h3: '⚠️ Froen, déi Dir falsch beäntwert hutt',
    retry_p: 'Lauschtert déi betreffend Deeler vun der Episode nach eng Kéier a probéiert dës Froen erëm. Dir musst all Froe richteg beäntwerte fir de Certificat ze kréien.',
    btn_retry: 'Déi falsch Froen erëm probéieren →',
    success_p: '🎉 Felicitatioun! Dir hutt all Froe richteg beäntwert.',
    btn_get_cert: 'Mäi Certificat kréien 🎓',
    btn_choose_another: '← Eng aner Episode wielen',
    cert_label: 'Participatiouns-Certificat',
    cert_body1: 'Hiermat gëtt bestätegt, datt',
    cert_body2: 'déi folgend Podcast-Episode gelauschtert an de Wëssensquiz erfollegräich ofgeschloss huet:',
    cert_verified: 'Verifizéiert',
    cert_email_label: 'E-Mail:',
    cert_date_label: 'Ausstellungsdatum:',
    btn_print: '🖨️ Drécken / Als PDF späicheren',
    btn_back_episode: '← Zréck zur Episode'
  }
};
const DATE_LOCALE = { en: 'en-GB', fr: 'fr-FR', de: 'de-DE', lb: 'fr-LU' };
// Language display names, keyed by [UI language][target language] — used in the read-along note.
const LANG_NAMES = {
  en: { en: 'English', fr: 'French', de: 'German', lb: 'Luxembourgish' },
  fr: { en: 'anglais', fr: 'français', de: 'allemand', lb: 'luxembourgeois' },
  de: { en: 'Englisch', fr: 'Französisch', de: 'Deutsch', lb: 'Luxemburgisch' },
  lb: { en: 'Englesch', fr: 'Franséisch', de: 'Däitsch', lb: 'Lëtzebuergesch' }
};
function langName(target) {
  return (LANG_NAMES[currentLang] && LANG_NAMES[currentLang][target]) || LANG_NAMES.en[target] || target;
}

// ── Topic categories (tags) ──────────────────────────────
// Ordered list; each episode's `categories` array holds these ids. Edit labels/order here.
const CATEGORIES = [
  { id: 'digital',     en: 'Digital services',          fr: 'Services en ligne',           de: 'Online-Dienste' },
  { id: 'social',      en: 'Social support',            fr: 'Aides sociales',              de: 'Soziale Hilfen' },
  { id: 'housing',     en: 'Housing',                   fr: 'Logement',                    de: 'Wohnen' },
  { id: 'energy',      en: 'Environment & energy',      fr: 'Environnement & énergie',     de: 'Umwelt & Energie' },
  { id: 'research',    en: 'Research & innovation',     fr: 'Recherche & innovation',      de: 'Forschung & Innovation' },
  { id: 'work',        en: 'Work & careers',            fr: 'Travail & carrière',          de: 'Arbeit & Beruf' },
  { id: 'family',      en: 'Family & children',         fr: 'Famille & enfants',           de: 'Familie & Kinder' },
  { id: 'health',      en: 'Health',                    fr: 'Santé',                       de: 'Gesundheit' },
  { id: 'seniors',     en: 'Seniors',                   fr: 'Seniors',                     de: 'Senioren' },
  { id: 'inclusion',   en: 'Inclusion & accessibility', fr: 'Inclusion & accessibilité',   de: 'Inklusion & Barrierefreiheit' },
  { id: 'safety',      en: 'Safety & emergencies',      fr: 'Sécurité & urgences',         de: 'Sicherheit & Notfälle' },
  { id: 'civic',       en: 'Civic engagement',          fr: 'Engagement citoyen',          de: 'Bürgerengagement' },
  { id: 'crossborder', en: 'Cross-border',              fr: 'Transfrontalier',             de: 'Grenzüberschreitend' }
];
function catLabel(id) {
  var c = CATEGORIES.find(function (x) { return x.id === id; });
  return c ? (c[currentLang] || c.en) : id;
}
let selectedCat = null;   // single active topic filter; null = show all

function t(key, vars) {
  var s = (I18N[currentLang] && I18N[currentLang][key]) || I18N.en[key] || key;
  if (vars) Object.keys(vars).forEach(function (k) { s = s.replace('{' + k + '}', vars[k]); });
  return s;
}

// ── Localised episode content (fallback to English) ──────
function epField(ep, base) { return ep[base + '_' + currentLang] || ep[base]; }
function epTopics(ep) { return ep['topics_' + currentLang] || ep.topics; }
function epQuestions(ep) { return ep['questions_' + currentLang] || ep.questions; }
function epNumber(ep) {
  var n = String(ep.number).replace(/\D/g, '');
  return t('episode_word') + ' ' + n;
}
// Which language the playing audio is in (the site language if a native track exists, else English).
function audioLangFor(ep) { return ep['audio_' + currentLang] ? currentLang : 'en'; }
function audioForLang(ep) { var l = audioLangFor(ep); return l === 'en' ? ep.audio : ep['audio_' + l]; }
// The displayed script can be karaoke-synced to the audio when its timestamps match that audio:
//  - same language as the audio, or
//  - the audio is English and that script has no native track (its segments are aligned to the English audio).
function isScriptSynced(ep) {
  var a = audioLangFor(ep);
  return currentLang === a || (a === 'en' && !ep['audio_' + currentLang]);
}

// ── Apply current language to the whole page ─────────────
function applyLang() {
  document.documentElement.setAttribute('lang', currentLang);
  document.querySelectorAll('[data-i18n]').forEach(function (el) {
    el.textContent = t(el.getAttribute('data-i18n'));
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(function (el) {
    el.setAttribute('placeholder', t(el.getAttribute('data-i18n-ph')));
  });
  // Header switcher reflects the site language (EN/FR/DE).
  document.querySelectorAll('#lang-switch-global .lang-btn').forEach(function (b) {
    b.classList.toggle('active', b.getAttribute('data-lang') === currentLang);
  });
  // Re-render whichever dynamic screen is currently visible.
  var active = document.querySelector('.screen.active');
  var id = active ? active.id : '';
  if (id === 'screen-episodes') renderEpisodeList();
  else if (id === 'screen-episode') renderEpisodeDetail();
  else if (id === 'screen-quiz') { setQuizLabel(); renderQuestion(curIndex); }
  else if (id === 'screen-results') showResults();
  else if (id === 'screen-certificate') showCertificate();
}

// ── Helpers ──────────────────────────────────────────────
function showScreen(id) {
  // Stop audio playback whenever we leave the episode page (logo, back buttons, quiz, etc.).
  if (id !== 'screen-episode') {
    var a = document.getElementById('ep-audio');
    if (a) a.pause();
  }
  document.querySelectorAll('.screen').forEach(function (s) { s.classList.remove('active'); });
  document.getElementById(id).classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
function hide(id) { document.getElementById(id).classList.add('hidden'); }
function show(id) { document.getElementById(id).classList.remove('hidden'); }
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// ── Registration ─────────────────────────────────────────
function doRegister() {
  var fn = document.getElementById('inp-first').value.trim();
  var ln = document.getElementById('inp-last').value.trim();
  var em = document.getElementById('inp-email').value.trim();
  var ok = true;

  function check(val, inputId, errId, testFn) {
    var inp = document.getElementById(inputId);
    var err = document.getElementById(errId);
    if (!testFn(val)) { inp.classList.add('error'); err.style.display = 'block'; ok = false; }
    else { inp.classList.remove('error'); err.style.display = 'none'; }
  }
  check(fn, 'inp-first', 'err-first', function (v) { return v.length > 0; });
  check(ln, 'inp-last', 'err-last', function (v) { return v.length > 0; });
  if (!ok) return;

  user = { firstName: fn, lastName: ln, email: em };
  renderEpisodeList();
  showScreen('screen-episodes');
}

// ── Episode list ─────────────────────────────────────────
function episodeMatchesFilter(ep) {
  if (!selectedCat) return true;
  return (ep.categories || []).indexOf(selectedCat) >= 0;
}
function renderFilterBar() {
  var bar = document.getElementById('filter-bar');
  if (!bar) return;
  bar.innerHTML = '';
  var all = document.createElement('button');
  all.type = 'button';
  all.className = 'filter-chip' + (selectedCat === null ? ' active' : '');
  all.textContent = t('filter_all');
  all.addEventListener('click', function () { selectedCat = null; renderEpisodeList(); });
  bar.appendChild(all);
  CATEGORIES.forEach(function (c) {
    var count = EPISODES.filter(function (e) { return (e.categories || []).indexOf(c.id) >= 0; }).length;
    if (!count) return;   // hide categories with no episodes yet
    var chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'filter-chip' + (selectedCat === c.id ? ' active' : '');
    chip.innerHTML = esc(catLabel(c.id)) + ' <span class="chip-count">' + count + '</span>';
    chip.addEventListener('click', function () {
      // single-select: pick this topic, or click the active one again to clear back to "All"
      selectedCat = (selectedCat === c.id) ? null : c.id;
      renderEpisodeList();
    });
    bar.appendChild(chip);
  });
}
function renderEpisodeList() {
  renderFilterBar();
  var grid = document.getElementById('episode-grid');
  grid.innerHTML = '';
  var shown = EPISODES.filter(episodeMatchesFilter);
  shown.forEach(function (ep) {
    var tags = (ep.categories || []).map(function (c) {
      return '<span class="cat-tag">' + esc(catLabel(c)) + '</span>';
    }).join('');
    var card = document.createElement('div');
    card.className = 'ep-list-card';
    card.innerHTML =
      '<div class="ep-list-badge">' + esc(epNumber(ep)) + '</div>' +
      '<div class="ep-list-title">' + esc(epField(ep, 'title')) + '</div>' +
      '<div class="ep-list-desc">' + esc(epField(ep, 'description')) + '</div>' +
      '<div class="cat-tags">' + tags + '</div>' +
      '<button class="btn ep-list-btn">' + esc(t('btn_listen_quiz')) + '</button>';
    card.querySelector('button').addEventListener('click', function () { selectEpisode(ep.id); });
    grid.appendChild(card);
  });
  var cnt = document.getElementById('filter-count');
  if (cnt) cnt.textContent = t('eps_count', { n: shown.length, total: EPISODES.length });
}

// ── Select episode ───────────────────────────────────────
function selectEpisode(id) {
  selectedEpisode = EPISODES.find(function (e) { return e.id === id; });
  renderEpisodeDetail();
  showScreen('screen-episode');
}

// ── Episode detail (player + transcript + topics) ────────
function renderEpisodeDetail() {
  var ep = selectedEpisode;
  if (!ep) return;
  document.getElementById('ep-badge').textContent = epNumber(ep);
  document.getElementById('ep-title').textContent = epField(ep, 'title');
  document.getElementById('ep-description').textContent = epField(ep, 'description');

  // Audio for the current language (falls back to English when no native track exists).
  var audio = document.getElementById('ep-audio');
  var newSrc = audioForLang(ep);
  if (audio.getAttribute('data-src') !== newSrc) {
    audio.pause();
    audio.src = newSrc;
    audio.setAttribute('data-src', newSrc);
    audio.load();
  }

  updateLangButtons();
  renderTranscript();

  // Topics
  var chips = document.getElementById('ep-topics');
  chips.innerHTML = '';
  epTopics(ep).forEach(function (tp) {
    var c = document.createElement('div');
    c.className = 'topic-chip';
    c.textContent = tp;
    chips.appendChild(c);
  });
}

// ── Transcript (always the chosen UI language) ───────────
function segmentsForScript(ep) {
  if (currentLang === 'fr' && ep.segments_fr) return ep.segments_fr;
  if (currentLang === 'de' && ep.segments_de) return ep.segments_de;
  return ep.segments;
}
function updateLangButtons() {
  document.querySelectorAll('#lang-switch-global .lang-btn').forEach(function (b) {
    b.classList.toggle('active', b.getAttribute('data-lang') === currentLang);
  });
}
function renderTranscript() {
  var ep = selectedEpisode;
  var audio = document.getElementById('ep-audio');
  var segs = segmentsForScript(ep);
  var synced = isScriptSynced(ep);   // can we karaoke-highlight against the current audio?
  var tw = document.getElementById('transcript');
  tw.innerHTML = '';
  tw.scrollTop = 0;
  segEls = [];
  segTimes = [];
  activeSeg = -1;
  var lastSpeaker = null;
  segs.forEach(function (seg, i) {
    var line = document.createElement('button');
    line.className = 't-line';
    line.type = 'button';
    var speakerTag = '';
    if (seg.speaker !== lastSpeaker) {
      speakerTag = '<span class="t-speaker ' + seg.speaker + '">' + esc(seg.speaker) + '</span>';
      lastSpeaker = seg.speaker;
    }
    line.innerHTML = speakerTag + '<span class="t-text">' + esc(seg.text) + '</span>';
    if (synced) {
      line.addEventListener('click', function () {
        audio.currentTime = seg.t + 0.01;
        audio.play();
        userScrolling = false;
        setActiveSeg(i, true);
      });
      segTimes.push(seg.t);
    } else {
      // Reading-only view (script differs from the spoken language): no seeking, no highlight.
      line.style.cursor = 'default';
    }
    tw.appendChild(line);
    segEls.push(line);
  });
  // Re-sync highlight to the current audio position (only when synced).
  if (synced) setActiveSeg(findSegIndex(audio.currentTime), true);
}
// Header switcher: site language drives UI, audio, quiz, content AND the transcript.
function setSiteLang(lang) {
  if (lang === currentLang) return;
  currentLang = lang;
  applyLang();
}

// ── Karaoke highlighting ─────────────────────────────────
function findSegIndex(time) {
  var lo = 0, hi = segTimes.length - 1, res = 0;
  if (hi < 0) return -1;
  while (lo <= hi) {
    var mid = (lo + hi) >> 1;
    if (segTimes[mid] <= time) { res = mid; lo = mid + 1; }
    else { hi = mid - 1; }
  }
  return res;
}
function setActiveSeg(i, forceScroll) {
  if (i === activeSeg && !forceScroll) return;
  if (activeSeg >= 0 && segEls[activeSeg]) {
    segEls[activeSeg].classList.remove('active');
    segEls[activeSeg].classList.add('spoken');
  }
  segEls.forEach(function (el, k) {
    if (k < i) el.classList.add('spoken'); else el.classList.remove('spoken');
  });
  activeSeg = i;
  if (i < 0 || !segEls[i]) return;
  segEls[i].classList.remove('spoken');
  segEls[i].classList.add('active');
  var follow = document.getElementById('follow-chk').checked;
  if (follow && (!userScrolling || forceScroll)) {
    centerLine(segEls[i]);
  }
}
function centerLine(el) {
  var tw = document.getElementById('transcript');
  if (!tw || !el) return;
  var cRect = tw.getBoundingClientRect();
  var eRect = el.getBoundingClientRect();
  var target = tw.scrollTop + (eRect.top - cRect.top) - (tw.clientHeight / 2 - el.clientHeight / 2);
  if (target < 0) target = 0;
  tw.scrollTo({ top: target, behavior: 'smooth' });
}
function onTimeUpdate() {
  var audio = document.getElementById('ep-audio');
  var i = findSegIndex(audio.currentTime);
  if (i !== activeSeg) setActiveSeg(i, false);
}

// ── Quiz ─────────────────────────────────────────────────
function setQuizLabel() {
  document.getElementById('q-label').textContent = epNumber(selectedEpisode) + ' – Biergerpakt Podcast';
}
function startQuiz() {
  answers = new Array(epQuestions(selectedEpisode).length).fill(-1);
  wrongIndices = [];
  curIndex = 0;
  isRetry = false;
  setQuizLabel();
  document.getElementById('ep-audio').pause();
  showScreen('screen-quiz');
  renderQuestion(0);
}
function renderQuestion(idx) {
  var qs = epQuestions(selectedEpisode);
  var q = qs[idx];
  var total = qs.length;
  document.getElementById('q-counter').textContent = t('q_counter', { n: idx + 1, total: total });
  document.getElementById('q-eyebrow').textContent = t('q_word') + ' ' + (idx + 1);
  document.getElementById('q-text').textContent = q.text;
  document.getElementById('q-progress').style.width = (((idx + 1) / total) * 100) + '%';

  var optWrap = document.getElementById('q-options');
  optWrap.innerHTML = '';
  var letters = ['A', 'B', 'C', 'D'];
  q.options.forEach(function (text, i) {
    var div = document.createElement('div');
    div.className = 'option';
    div.innerHTML = '<div class="opt-letter">' + letters[i] + '</div><div class="opt-text">' + esc(text) + '</div>';
    div.addEventListener('click', function () { selectAnswer(i); });
    optWrap.appendChild(div);
  });
  var fb = document.getElementById('q-feedback');
  fb.className = 'feedback';
  fb.textContent = '';
  var nb = document.getElementById('btn-next');
  nb.textContent = t('btn_next');
  hide('btn-next');
}
function selectAnswer(chosen) {
  if (!document.getElementById('btn-next').classList.contains('hidden')) return;
  var q = epQuestions(selectedEpisode)[curIndex];
  answers[curIndex] = chosen;

  document.querySelectorAll('.option').forEach(function (el) {
    el.style.cursor = 'default';
    el.replaceWith(el.cloneNode(true));
  });
  document.querySelectorAll('.option').forEach(function (el, i) {
    if (i === q.correct) el.classList.add('correct');
    if (i === chosen && i !== q.correct) el.classList.add('wrong');
  });

  var fb = document.getElementById('q-feedback');
  if (chosen === q.correct) {
    fb.className = 'feedback show ok';
    fb.innerHTML = '<strong>' + t('fb_ok') + '</strong> ' + esc(q.explanation);
  } else {
    fb.className = 'feedback show fail';
    fb.innerHTML = '<strong>' + t('fb_fail_prefix') + '</strong> ' + t('fb_fail_mid') + ' <strong>' +
      esc(q.options[q.correct]) + '</strong>. ' + esc(q.explanation);
  }
  show('btn-next');
}
function nextQuestion() {
  if (isRetry) {
    retryPos++;
    if (retryPos < retryIndices.length) { curIndex = retryIndices[retryPos]; renderQuestion(curIndex); }
    else { showResults(); }
  } else {
    curIndex++;
    if (curIndex < epQuestions(selectedEpisode).length) { renderQuestion(curIndex); }
    else { showResults(); }
  }
}

// ── Results ──────────────────────────────────────────────
function showResults() {
  var qs = epQuestions(selectedEpisode);
  wrongIndices = [];
  answers.forEach(function (ans, i) {
    if (ans !== qs[i].correct) wrongIndices.push(i);
  });
  var total = qs.length;
  var nCorrect = total - wrongIndices.length;

  document.getElementById('score-n').textContent = nCorrect;
  document.getElementById('score-d').textContent = t('of_word') + ' ' + total;
  var ring = document.getElementById('score-ring');

  if (nCorrect === total) {
    ring.style.background = 'var(--green)';
    document.getElementById('score-title').textContent = t('res_all_title');
    document.getElementById('score-msg').textContent = t('res_all_msg');
    hide('retry-card');
    show('success-banner');
  } else {
    ring.style.background = 'var(--orange)';
    document.getElementById('score-title').textContent = t('res_partial_title', { n: nCorrect, total: total });
    document.getElementById('score-msg').textContent = t('res_partial_msg');
    var list = document.getElementById('wrong-list');
    list.innerHTML = wrongIndices.map(function (i) {
      return '<div class="wrong-item"><strong>' + t('q_word') + ' ' + (i + 1) + ':</strong> ' + esc(qs[i].text) + '</div>';
    }).join('');
    show('retry-card');
    hide('success-banner');
  }
  showScreen('screen-results');
}
function retryWrong() {
  isRetry = true;
  retryIndices = wrongIndices.slice();
  retryPos = 0;
  curIndex = retryIndices[0];
  retryIndices.forEach(function (i) { answers[i] = -1; });
  showScreen('screen-quiz');
  renderQuestion(curIndex);
}

// ── Certificate ──────────────────────────────────────────
function showCertificate() {
  document.getElementById('cert-name-out').textContent = user.firstName + ' ' + user.lastName;
  document.getElementById('cert-episode-out').textContent = epNumber(selectedEpisode) + ': ' + epField(selectedEpisode, 'title');
  var emailLine = document.getElementById('cert-email-line');
  emailLine.innerHTML = user.email ? ('<strong>' + t('cert_email_label') + '</strong> ' + esc(user.email) + '<br>') : '';
  document.getElementById('cert-date-out').textContent = new Date().toLocaleDateString(DATE_LOCALE[currentLang] || 'en-GB', {
    day: '2-digit', month: 'long', year: 'numeric'
  });
  showScreen('screen-certificate');
}

// ── Wire up ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('btn-register').addEventListener('click', doRegister);
  ['inp-first', 'inp-last', 'inp-email'].forEach(function (id) {
    document.getElementById(id).addEventListener('keydown', function (e) { if (e.key === 'Enter') doRegister(); });
  });
  document.getElementById('btn-start-quiz').addEventListener('click', startQuiz);
  document.getElementById('btn-next').addEventListener('click', nextQuestion);
  document.getElementById('btn-retry').addEventListener('click', retryWrong);
  document.getElementById('btn-show-cert').addEventListener('click', showCertificate);
  document.getElementById('btn-print').addEventListener('click', function () { window.print(); });
  document.getElementById('btn-back-episode').addEventListener('click', function () { showScreen('screen-episode'); });
  document.getElementById('btn-back-episodes').addEventListener('click', function () {
    document.getElementById('ep-audio').pause(); showScreen('screen-episodes');
  });
  document.getElementById('btn-back-episodes-result').addEventListener('click', function () { showScreen('screen-episodes'); });

  // Header switcher → site language (drives UI, audio, quiz, content and transcript).
  document.querySelectorAll('#lang-switch-global .lang-btn').forEach(function (b) {
    b.addEventListener('click', function () { setSiteLang(b.getAttribute('data-lang')); });
  });

  // Audio sync
  var audio = document.getElementById('ep-audio');
  audio.addEventListener('timeupdate', onTimeUpdate);
  audio.addEventListener('seeked', onTimeUpdate);

  document.getElementById('follow-chk').addEventListener('change', function () {
    if (this.checked) {
      userScrolling = false;
      if (activeSeg >= 0 && segEls[activeSeg]) centerLine(segEls[activeSeg]);
    }
  });

  var tw = document.getElementById('transcript');
  tw.addEventListener('wheel', markUserScroll, { passive: true });
  tw.addEventListener('touchmove', markUserScroll, { passive: true });
  function markUserScroll() {
    userScrolling = true;
    clearTimeout(userScrollTimer);
    userScrollTimer = setTimeout(function () {
      userScrolling = false;
      if (document.getElementById('follow-chk').checked && activeSeg >= 0 && segEls[activeSeg]) {
        centerLine(segEls[activeSeg]);
      }
    }, 4000);
  }

  // Apply initial language (sets active states + static strings).
  applyLang();
});
