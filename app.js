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
    filter_heading: 'Topic',
    filter_all: 'All topics',
    eps_count: '{n} of {total} episodes',
    view_by_topic: 'Show episodes by topic',
    view_map: 'Show the topic map',
    map_hint: 'Each circle is a topic and each number an episode. Choose a topic to filter the list below, or a number to open the episode.',
    map_tap_again: 'Tap again to open',
    map_label: 'Map of the episodes by topic',
    view_full_list: 'Show the full list',
    topics_count: '{n} topics · {total} episodes',
    btn_all_episodes: '← All episodes',
    listen_title: '🎧 Listen to this episode',
    player_hint: 'Press play and the script below will highlight along with the audio. Click any line to jump to that point.',
    script_title: '📝 Episode script',
    autoscroll: 'Auto-scroll with audio',
    lang_note_tmpl: 'The audio is in {lang}. This script is shown for reading along.',
    status_in_progress: 'In progress',
    in_progress_note: 'This episode is still in progress: the audio and the script are not final yet and may still change.',
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
    cert_generic_name: 'Biergerpakt Participant',
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
    filter_heading: 'Sujet',
    filter_all: 'Tous les sujets',
    eps_count: '{n} sur {total} épisodes',
    view_by_topic: 'Afficher les épisodes par sujet',
    view_map: 'Afficher la carte des sujets',
    map_hint: 'Chaque cercle est un sujet et chaque numéro un épisode. Choisissez un sujet pour filtrer la liste ci-dessous, ou un numéro pour ouvrir l\'épisode.',
    map_tap_again: 'Touchez à nouveau pour ouvrir',
    map_label: 'Carte des épisodes par sujet',
    view_full_list: 'Afficher la liste complète',
    topics_count: '{n} sujets · {total} épisodes',
    btn_all_episodes: '← Tous les épisodes',
    listen_title: '🎧 Écouter cet épisode',
    player_hint: 'Appuyez sur lecture et le script ci-dessous se surlignera au rythme de l’audio. Cliquez sur une ligne pour y accéder directement.',
    script_title: '📝 Script de l’épisode',
    autoscroll: 'Défilement automatique avec l’audio',
    lang_note_tmpl: 'L’audio est en {lang}. Ce script est affiché pour suivre la lecture.',
    status_in_progress: 'En cours',
    in_progress_note: 'Cet épisode est encore en cours de préparation : l’audio et le script ne sont pas encore définitifs et peuvent encore changer.',
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
    cert_generic_name: 'Participant(e) au Biergerpakt',
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
    filter_heading: 'Thema',
    filter_all: 'Alle Themen',
    eps_count: '{n} von {total} Folgen',
    view_by_topic: 'Folgen nach Thema anzeigen',
    view_map: 'Themenkarte anzeigen',
    map_hint: 'Jeder Kreis ist ein Thema und jede Zahl eine Folge. Wählen Sie ein Thema, um die Liste darunter zu filtern, oder eine Zahl, um die Folge zu öffnen.',
    map_tap_again: 'Zum Öffnen erneut tippen',
    map_label: 'Karte der Folgen nach Thema',
    view_full_list: 'Ganze Liste anzeigen',
    topics_count: '{n} Themen · {total} Folgen',
    btn_all_episodes: '← Alle Folgen',
    listen_title: '🎧 Diese Folge anhören',
    player_hint: 'Drücken Sie auf Wiedergabe, und das Skript unten wird im Takt des Audios hervorgehoben. Klicken Sie auf eine Zeile, um direkt dorthin zu springen.',
    script_title: '📝 Skript der Folge',
    autoscroll: 'Automatisch mit dem Audio scrollen',
    lang_note_tmpl: 'Das Audio ist auf {lang}. Dieses Skript dient zum Mitlesen.',
    status_in_progress: 'In Bearbeitung',
    in_progress_note: 'Diese Folge ist noch in Bearbeitung: Audio und Skript sind noch nicht endgültig und können sich noch ändern.',
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
    cert_generic_name: 'Biergerpakt-Teilnehmer(in)',
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
    filter_heading: 'Thema',
    filter_all: 'All Themen',
    eps_count: '{n} vu(n) {total} Episoden',
    view_by_topic: 'Episoden no Thema weisen',
    view_map: 'Themekaart weisen',
    view_full_list: 'Ganz Lëscht weisen',
    topics_count: '{n} Themen · {total} Episoden',
    btn_all_episodes: '← All Episoden',
    listen_title: '🎧 Dës Episode lauschteren',
    player_hint: 'Dréckt op Play an de Skript hei ënnen gëtt am Takt vum Audio ervirgehuewen. Klickt op eng Zeil fir direkt dohinner ze sprangen.',
    script_title: '📝 Skript vun der Episode',
    autoscroll: 'Automatesch mam Audio scrollen',
    lang_note_tmpl: 'Den Audio ass op {lang}. Dëse Skript gëtt fir matzelauschteren ugewisen.',
    status_in_progress: 'Am Gaang',
    in_progress_note: 'Dës Episod ass nach a Bearbechtung: den Audio an de Skript sinn nach net definitiv a kënne sech nach änneren.',
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
    cert_generic_name: 'Biergerpakt-Participant(in)',
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
  { id: 'agriculture', en: 'Agriculture & food',        fr: 'Agriculture & alimentation',  de: 'Landwirtschaft & Ernährung' },
  { id: 'culture',     en: 'Culture & arts',            fr: 'Culture & arts',              de: 'Kultur & Kunst' },
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
// Broad themes. The detailed categories above are regrouped into a few families; these are what
// the dropdown, the "by topic" view and the topic map show. Every category id must be listed
// in exactly one theme (an episode tagged only with an unlisted category would not be grouped).
const THEMES = [
  { id: 'digital', color: '#1A3C5E', cats: ['digital'],
    en: 'Digital services', fr: 'Services en ligne', de: 'Online-Dienste' },
  { id: 'social', color: '#B8430A', cats: ['social', 'inclusion'],
    en: 'Social support & inclusion', fr: 'Aides sociales & inclusion', de: 'Soziale Hilfen & Inklusion' },
  { id: 'family', color: '#8E2A6B', cats: ['family', 'health', 'seniors'],
    en: 'Family, health & seniors', fr: 'Famille, santé & seniors', de: 'Familie, Gesundheit & Senioren' },
  { id: 'work', color: '#1F6F78', cats: ['work', 'research'],
    en: 'Work & innovation', fr: 'Travail & innovation', de: 'Arbeit & Innovation' },
  { id: 'living', color: '#2A7A3B', cats: ['housing', 'energy', 'agriculture'],
    en: 'Housing & environment', fr: 'Logement & environnement', de: 'Wohnen & Umwelt' },
  { id: 'civic', color: '#5B4BA8', cats: ['civic', 'culture', 'crossborder'],
    en: 'Civic life, culture & Greater Region', fr: 'Vie citoyenne, culture & Grande Région', de: 'Bürgerleben, Kultur & Großregion' },
  { id: 'safety', color: '#B02A2A', cats: ['safety'],
    en: 'Safety & emergencies', fr: 'Sécurité & urgences', de: 'Sicherheit & Notfälle' }
];
function themeById(id) { return THEMES.find(function (x) { return x.id === id; }); }
function themeLabel(th) { return th[currentLang] || th.en; }
function epInTheme(ep, th) {
  return (ep.categories || []).some(function (c) { return th.cats.indexOf(c) >= 0; });
}
function themeEpisodes(th) { return EPISODES.filter(function (e) { return epInTheme(e, th); }); }
let selectedCat = null;   // single active theme filter (a THEMES id); null = show all
let showMap = false;      // topic map (bubbles) above the list; off by default
// List view: false = one row per episode (default); true = grouped by topic, an episode appears under each of its topics
let viewByTopic = false;   // the site always opens on the full list

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
// ?v=<duration> busts browser caches: a re-recorded mp3 keeps its file name but always gets a new duration.
function audioForLang(ep) {
  var l = audioLangFor(ep);
  var src = l === 'en' ? ep.audio : ep['audio_' + l];
  var dur = l === 'en' ? ep.duration : ep['duration_' + l];
  return (src && dur) ? src + '?v=' + dur : src;
}
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
  plRefreshUI();   // playlist: header counter, + buttons, playlist screen, player bar
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
  var th = selectedCat && themeById(selectedCat);
  return th ? epInTheme(ep, th) : true;
}
function renderFilterBar() {
  // Topic filter = one compact dropdown (single-select; "All topics" clears it).
  var sel = document.getElementById('filter-select');
  if (!sel) return;
  sel.innerHTML = '';
  var all = document.createElement('option');
  all.value = '';
  all.textContent = t('filter_all');
  sel.appendChild(all);
  THEMES.forEach(function (c) {
    var count = themeEpisodes(c).length;
    if (!count) return;   // hide themes with no episodes yet
    var opt = document.createElement('option');
    opt.value = c.id;
    opt.textContent = themeLabel(c) + ' (' + count + ')';
    sel.appendChild(opt);
  });
  sel.value = selectedCat || '';
  sel.classList.toggle('active', !!selectedCat);
  sel.onchange = function () { selectedCat = sel.value || null; renderEpisodeList(); };
}
function episodeRow(ep) {
  // One compact row per episode: number · title · arrow. The whole row is the button.
  var row = document.createElement('button');
  var inProgress = ep.status === 'in_progress';
  row.type = 'button';
  row.className = 'ep-row' + (inProgress ? ' in-progress' : '');
  row.title = epField(ep, 'description');   // full description on hover
  row.setAttribute('aria-label', epNumber(ep) + ': ' + epField(ep, 'title'));
  row.innerHTML =
    '<span class="ep-row-num">' + esc(String(ep.number).replace(/\D/g, '')) + '</span>' +
    '<span class="ep-row-title">' + esc(epField(ep, 'title')) + '</span>' +
    (inProgress ? '<span class="ep-status-badge">' + esc(t('status_in_progress')) + '</span>' : '') +
    '<span class="ep-row-go" aria-hidden="true">&rsaquo;</span>';
  row.addEventListener('click', function () { selectEpisode(ep.id); });
  return plWrapRow(row, ep);   // adds the "+ playlist" button (row unchanged where playlists are off)
}
function renderViewToggle() {
  // Tick box "Show episodes by topic" (unticked = full list, the default).
  var box = document.getElementById('view-toggle');
  if (!box) return;
  var lab = document.getElementById('view-toggle-label');
  if (lab) lab.textContent = t('view_by_topic');
  box.checked = viewByTopic;
  box.onchange = function () { viewByTopic = box.checked; renderEpisodeList(); };
  // Second tick box: "Show the topic map".
  var mbox = document.getElementById('map-toggle');
  if (!mbox) return;
  var mlab = document.getElementById('map-toggle-label');
  if (mlab) mlab.textContent = t('view_map');
  mbox.checked = showMap;
  mbox.onchange = function () { showMap = mbox.checked; renderEpisodeList(); };
}

// ── Topic map: one bubble per theme (sized by its number of episodes), one dot per episode ──
function tmMix(hex, share) {   // colour mixed with white; share = part of the colour (0..1)
  var n = parseInt(hex.slice(1), 16), c = [n >> 16 & 255, n >> 8 & 255, n & 255];
  return 'rgb(' + c.map(function (v) { return Math.round(255 - (255 - v) * share); }).join(',') + ')';
}
function tmDotLayout(n, d) {
  // Sunflower arrangement of n dots of diameter d, centred on (0,0); returns the points and the bubble radius.
  var c = (d + 5) / 1.72, pts = [], i;
  for (i = 0; i < n; i++) {
    var rad = n === 1 ? 0 : c * Math.sqrt(i + 0.5), ang = i * 2.399963;
    pts.push({ x: rad * Math.cos(ang), y: rad * Math.sin(ang) });
  }
  // A few relaxation passes so that no two dots touch.
  for (var it = 0; it < 60; it++) {
    for (i = 0; i < n; i++) for (var j = i + 1; j < n; j++) {
      var dx = pts[j].x - pts[i].x, dy = pts[j].y - pts[i].y, dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
      if (dist < d + 4) {
        var push = (d + 4 - dist) / 2;
        pts[i].x -= dx / dist * push; pts[i].y -= dy / dist * push;
        pts[j].x += dx / dist * push; pts[j].y += dy / dist * push;
      }
    }
  }
  var cx = 0, cy = 0, far = 0;
  pts.forEach(function (p) { cx += p.x / n; cy += p.y / n; });
  pts.forEach(function (p) { p.x -= cx; p.y -= cy; far = Math.max(far, Math.sqrt(p.x * p.x + p.y * p.y)); });
  return { pts: pts, r: Math.max(48, far + d / 2 + 12) };
}
function tmPack(nodes, W, gap) {
  // Place the bubbles side by side without overlap, pulled towards the middle of the available width.
  nodes.forEach(function (n, i) {
    var a = i * 2.4, rad = 60 * Math.sqrt(i);
    n.x = W / 2 + Math.cos(a) * rad * 2; n.y = Math.sin(a) * rad;
  });
  for (var it = 0; it < 500; it++) {
    if (it < 440) nodes.forEach(function (n) { n.x += (W / 2 - n.x) * 0.012; n.y += -n.y * 0.05; });
    for (var i = 0; i < nodes.length; i++) for (var j = i + 1; j < nodes.length; j++) {
      // Vertical distances count for less, so bubbles sit further apart vertically: room for the label chips.
      var a2 = nodes[i], b = nodes[j], dx = b.x - a2.x, dy = (b.y - a2.y) * 0.8;
      var dist = Math.sqrt(dx * dx + dy * dy) || 0.01, min = a2.r + b.r + gap;
      if (dist < min) {
        var push = (min - dist) / 2;
        a2.x -= dx / dist * push; a2.y -= dy / dist * push;
        b.x += dx / dist * push; b.y += dy / dist * push;
      }
    }
    nodes.forEach(function (n) { n.x = Math.min(Math.max(n.x, n.r + 4), Math.max(W - n.r - 4, n.r + 4)); });
  }
  var top = Infinity, bottom = -Infinity;
  nodes.forEach(function (n) { top = Math.min(top, n.y - n.r); bottom = Math.max(bottom, n.y + n.r); });
  nodes.forEach(function (n) { n.y += 26 - top; });
  return bottom - top + 34;
}
var tmTipFor = null;   // on touch screens: the dot whose title is showing (a second tap opens it)
function renderTopicMap() {
  var wrap = document.getElementById('topic-map-wrap');
  if (!wrap) return;
  wrap.hidden = !showMap;
  if (!showMap) return;
  var map = document.getElementById('topic-map');
  map.innerHTML = '';
  map.setAttribute('aria-label', t('map_label'));
  document.getElementById('topic-map-hint').textContent = t('map_hint');
  var W = map.clientWidth || 860;
  var d = W < 520 ? 32 : 36;
  var noHover = !!(window.matchMedia && window.matchMedia('(hover: none)').matches);
  tmTipFor = null;

  var nodes = [];
  THEMES.forEach(function (th) {
    var eps = themeEpisodes(th);
    if (!eps.length) return;
    var lay = tmDotLayout(eps.length, d);
    nodes.push({ th: th, eps: eps, pts: lay.pts, r: lay.r });
  });
  map.style.height = Math.ceil(tmPack(nodes, W, 18)) + 'px';

  var tip = document.createElement('div');
  tip.className = 'tm-tip';
  tip.hidden = true;
  function showTip(node, p, ep) {
    tip.innerHTML = '<span class="tm-tip-num">' + esc(epNumber(ep)) + '</span>' + esc(epField(ep, 'title')) +
      (noHover ? '<span class="tm-tip-more">' + esc(t('map_tap_again')) + '</span>' : '');
    tip.hidden = false;
    var half = Math.min(120, W / 2 - 4);
    tip.style.left = Math.min(Math.max(node.x + p.x, half + 4), W - half - 4) + 'px';
    tip.style.top = (node.y + p.y - d / 2 - 8) + 'px';
  }
  function hideTip() { tip.hidden = true; }
  function pickTheme(id) { selectedCat = selectedCat === id ? null : id; renderEpisodeList(); }

  nodes.forEach(function (node) {
    var th = node.th, on = selectedCat === th.id;
    var b = document.createElement('div');
    b.className = 'tm-bubble' + (on ? ' selected' : (selectedCat ? ' dimmed' : ''));
    b.style.cssText = 'left:' + (node.x - node.r) + 'px;top:' + (node.y - node.r) + 'px;width:' + (2 * node.r) +
      'px;height:' + (2 * node.r) + 'px;--c:' + th.color + ';background:' + tmMix(th.color, 0.09) +
      ';border-color:' + tmMix(th.color, 0.4);
    b.addEventListener('click', function () { pickTheme(th.id); });

    var chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'tm-chip';
    chip.style.maxWidth = Math.round(2 * node.r) + 'px';
    chip.setAttribute('aria-pressed', on ? 'true' : 'false');
    chip.innerHTML = esc(themeLabel(th)) + ' <span class="tm-chip-n">' + node.eps.length + '</span>';
    chip.addEventListener('click', function (e) { e.stopPropagation(); pickTheme(th.id); });
    b.appendChild(chip);

    node.eps.forEach(function (ep, i) {
      var p = node.pts[i];
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'tm-dot' + (ep.status === 'in_progress' ? ' in-progress' : '');
      dot.style.cssText = 'left:' + (node.r + p.x) + 'px;top:' + (node.r + p.y) + 'px;width:' + d + 'px;height:' + d +
        'px;margin:' + (-d / 2) + 'px 0 0 ' + (-d / 2) + 'px';
      dot.textContent = String(ep.number).replace(/\D/g, '');
      dot.setAttribute('aria-label', epNumber(ep) + ': ' + epField(ep, 'title'));
      dot.addEventListener('mouseenter', function () { showTip(node, p, ep); });
      dot.addEventListener('focus', function () { showTip(node, p, ep); });
      dot.addEventListener('mouseleave', hideTip);
      dot.addEventListener('blur', hideTip);
      dot.addEventListener('click', function (e) {
        e.stopPropagation();
        var key = th.id + ':' + ep.id;
        if (noHover && tmTipFor !== key) { tmTipFor = key; showTip(node, p, ep); return; }
        selectEpisode(ep.id);
      });
      b.appendChild(dot);
    });
    map.appendChild(b);
  });
  map.appendChild(tip);
}
var tmResizeTimer = null;
window.addEventListener('resize', function () {
  if (!showMap) return;
  clearTimeout(tmResizeTimer);
  tmResizeTimer = setTimeout(renderTopicMap, 150);
});
function renderEpisodeList() {
  renderFilterBar();
  renderViewToggle();
  renderTopicMap();
  var grid = document.getElementById('episode-grid');
  grid.innerHTML = '';
  grid.classList.toggle('by-topic', viewByTopic);
  var shown = EPISODES.filter(episodeMatchesFilter);
  var cnt = document.getElementById('filter-count');
  if (!viewByTopic) {
    shown.forEach(function (ep) { grid.appendChild(episodeRow(ep)); });
    if (cnt) cnt.textContent = t('eps_count', { n: shown.length, total: EPISODES.length });
    return;
  }
  // Grouped view: one section per theme (in THEMES order); episodes with several themes are repeated.
  var groups = 0;
  THEMES.forEach(function (c) {
    if (selectedCat && selectedCat !== c.id) return;
    var eps = themeEpisodes(c);
    if (!eps.length) return;
    groups++;
    var sec = document.createElement('section');
    sec.className = 'topic-group';
    var h = document.createElement('h2');
    h.className = 'topic-group-head';
    h.innerHTML = '<span class="topic-group-dot" style="background:' + c.color + '"></span>' + esc(themeLabel(c)) + ' <span class="topic-group-count">' + eps.length + '</span>';
    sec.appendChild(h);
    eps.forEach(function (ep) { sec.appendChild(episodeRow(ep)); });
    grid.appendChild(sec);
  });
  if (cnt) cnt.textContent = selectedCat ? t('eps_count', { n: shown.length, total: EPISODES.length })
                                         : t('topics_count', { n: groups, total: shown.length });
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
  // Episodes not finalised yet (status: 'in_progress') show a notice for reviewers/listeners.
  var note = document.getElementById('ep-status-note');
  if (note) {
    note.hidden = ep.status !== 'in_progress';
    note.textContent = ep.status === 'in_progress' ? '⏳ ' + t('in_progress_note') : '';
  }

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
  plPaintDetailBtn();
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
  plOnLangChange();   // playlist track follows the site language
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
  // Registration is disabled for now: fall back to a generic name on the certificate.
  document.getElementById('cert-name-out').textContent =
    (user.firstName ? user.firstName + ' ' + user.lastName : t('cert_generic_name'));
  document.getElementById('cert-episode-out').textContent = epNumber(selectedEpisode) + ': ' + epField(selectedEpisode, 'title');
  var emailLine = document.getElementById('cert-email-line');
  emailLine.innerHTML = user.email ? ('<strong>' + t('cert_email_label') + '</strong> ' + esc(user.email) + '<br>') : '';
  document.getElementById('cert-date-out').textContent = new Date().toLocaleDateString(DATE_LOCALE[currentLang] || 'en-GB', {
    day: '2-digit', month: 'long', year: 'numeric'
  });
  showScreen('screen-certificate');
}

// ── Playlist ─────────────────────────────────────────────
// Listeners pick episodes and hear them one after the other (e.g. in the car).
//  - A second <audio id="pl-audio"> sits in the fixed player bar, so the playlist keeps playing on every
//    screen. The episode page keeps its own player (#ep-audio, with the read-along script).
//    Only one of the two plays at a time.
//  - The list (and where you stopped) is kept on the device only (localStorage) – nothing is sent anywhere.
//  - Media Session: title + previous/next on the lock screen, Bluetooth, CarPlay and Android Auto.
//  - Switched off on single-episode pages (partner review links) and on pages generated before this
//    feature existed (no #pl-audio in the HTML).
Object.assign(I18N.en, {
  pl_button: 'My playlist',
  pl_h1: 'My playlist',
  pl_intro: 'Choose the episodes you want to hear in a row – in the car, on the train or on a walk. They play one after the other.',
  pl_add: 'Add to my playlist',
  pl_added: '✓ In my playlist',
  pl_remove: 'Remove from my playlist',
  pl_empty: 'Your playlist is empty. Use the + button next to an episode to add it.',
  pl_play_all: '▶ Play all',
  pl_clear: 'Empty the playlist',
  pl_clear_confirm: 'Tap again to empty',
  pl_summary: '{n} episodes · {time}',
  pl_summary_one: '1 episode · {time}',
  pl_up: 'Move up', pl_down: 'Move down',
  pl_play_this: 'Play this episode',
  pl_car_hint: 'In the car: connect your phone by Bluetooth, CarPlay or Android Auto, start the playlist before you drive, and use the buttons of your car to pause or to skip to the next episode. The audio is streamed, so it uses mobile data.',
  pl_storage_note: 'Your playlist is saved only on this device. Nothing is sent anywhere.',
  pl_prev: 'Previous episode', pl_next: 'Next episode', pl_play: 'Play', pl_pause: 'Pause',
  pl_close: 'Close the player', pl_seek: 'Position in the episode'
});
Object.assign(I18N.fr, {
  pl_button: 'Ma playlist',
  pl_h1: 'Ma playlist',
  pl_intro: 'Choisissez les épisodes que vous voulez écouter à la suite – en voiture, dans le train ou en promenade. Ils s’enchaînent automatiquement.',
  pl_add: 'Ajouter à ma playlist',
  pl_added: '✓ Dans ma playlist',
  pl_remove: 'Retirer de ma playlist',
  pl_empty: 'Votre playlist est vide. Utilisez le bouton + à côté d’un épisode pour l’ajouter.',
  pl_play_all: '▶ Tout écouter',
  pl_clear: 'Vider la playlist',
  pl_clear_confirm: 'Appuyez encore pour vider',
  pl_summary: '{n} épisodes · {time}',
  pl_summary_one: '1 épisode · {time}',
  pl_up: 'Monter', pl_down: 'Descendre',
  pl_play_this: 'Écouter cet épisode',
  pl_car_hint: 'En voiture : connectez votre téléphone par Bluetooth, CarPlay ou Android Auto, lancez la playlist avant de démarrer, puis utilisez les touches de votre voiture pour mettre en pause ou passer à l’épisode suivant. L’écoute se fait en streaming et utilise donc vos données mobiles.',
  pl_storage_note: 'Votre playlist est enregistrée uniquement sur cet appareil. Rien n’est envoyé.',
  pl_prev: 'Épisode précédent', pl_next: 'Épisode suivant', pl_play: 'Lecture', pl_pause: 'Pause',
  pl_close: 'Fermer le lecteur', pl_seek: 'Position dans l’épisode'
});
Object.assign(I18N.de, {
  pl_button: 'Meine Playlist',
  pl_h1: 'Meine Playlist',
  pl_intro: 'Wählen Sie die Folgen aus, die Sie nacheinander hören möchten – im Auto, im Zug oder beim Spazierengehen. Sie werden automatisch nacheinander abgespielt.',
  pl_add: 'Zu meiner Playlist hinzufügen',
  pl_added: '✓ In meiner Playlist',
  pl_remove: 'Aus meiner Playlist entfernen',
  pl_empty: 'Ihre Playlist ist leer. Mit der Schaltfläche + neben einer Folge fügen Sie sie hinzu.',
  pl_play_all: '▶ Alle abspielen',
  pl_clear: 'Playlist leeren',
  pl_clear_confirm: 'Zum Leeren erneut tippen',
  pl_summary: '{n} Folgen · {time}',
  pl_summary_one: '1 Folge · {time}',
  pl_up: 'Nach oben', pl_down: 'Nach unten',
  pl_play_this: 'Diese Folge abspielen',
  pl_car_hint: 'Im Auto: Verbinden Sie Ihr Telefon über Bluetooth, CarPlay oder Android Auto, starten Sie die Playlist vor der Fahrt und nutzen Sie die Tasten Ihres Autos, um zu pausieren oder zur nächsten Folge zu springen. Die Wiedergabe erfolgt per Streaming und verbraucht mobile Daten.',
  pl_storage_note: 'Ihre Playlist wird nur auf diesem Gerät gespeichert. Es wird nichts übertragen.',
  pl_prev: 'Vorherige Folge', pl_next: 'Nächste Folge', pl_play: 'Abspielen', pl_pause: 'Pause',
  pl_close: 'Player schließen', pl_seek: 'Position in der Folge'
});

var PL_KEY = 'bp_playlist_v1';
var PL_ICONS = {
  play:  '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 5v14l11-7z"/></svg>',
  pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>',
  plus:  '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" d="M12 5v14M5 12h14"/></svg>',
  check: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  up:    '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" d="M6 15l6-6 6 6"/></svg>',
  down:  '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" d="M6 9l6 6 6-6"/></svg>',
  remove:'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" d="M6 6l12 12M18 6L6 18"/></svg>'
};
var playlist = [];          // episode ids, in listening order
var plCurId = null;         // episode loaded in the player bar (null = bar closed)
var plLang = null;          // language of the loaded track
var plPendingSeek = null;   // position to jump to once the audio has loaded (resume / language switch)
var plSeeking = false;      // the listener is dragging the position slider
var plLastStore = 0;
var plClearTimer = null;

function plAudio() { return document.getElementById('pl-audio'); }
function plEnabled() { return EPISODES.length > 1 && !!plAudio(); }
function plEp(id) { return EPISODES.find(function (e) { return e.id === id; }); }
function plHas(id) { return playlist.indexOf(id) >= 0; }
function plIndex() { return plCurId == null ? -1 : playlist.indexOf(plCurId); }
function plDurIn(ep, lang) { return (lang === 'en' ? ep.duration : ep['duration_' + lang]) || ep.duration || 0; }
function plDur(ep) { return plDurIn(ep, audioLangFor(ep)); }
function plPos() { var a = plAudio(); return plPendingSeek != null ? plPendingSeek : ((a && a.currentTime) || 0); }
function plScreenActive() { var s = document.getElementById('screen-playlist'); return !!s && s.classList.contains('active'); }
function fmtTime(s) {
  s = Math.max(0, Math.round(s || 0));
  var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
  return (h ? h + ':' + (m < 10 ? '0' : '') : '') + m + ':' + (x < 10 ? '0' : '') + x;
}

// Storage (private browsing or blocked storage simply means the list is not remembered).
function plStore() {
  plLastStore = Date.now();
  try {
    localStorage.setItem(PL_KEY, JSON.stringify({ ids: playlist, cur: plCurId, t: plCurId != null ? Math.floor(plPos()) : 0 }));
  } catch (e) {}
}
function plRestore() {
  try {
    var d = JSON.parse(localStorage.getItem(PL_KEY) || 'null');
    if (!d || !Array.isArray(d.ids)) return;
    var seen = {};
    playlist = d.ids.filter(function (id) { if (seen[id] || !plEp(id)) return false; seen[id] = 1; return true; });
    if (d.cur != null && plHas(d.cur)) plLoadTrack(d.cur, false, d.t || 0);   // bar comes back paused where you stopped
  } catch (e) {}
}

// Player
function plLoadTrack(id, autoplay, startAt) {
  var ep = plEp(id), a = plAudio();
  if (!ep || !a) return;
  plCurId = id;
  plLang = audioLangFor(ep);
  plPendingSeek = startAt > 0 ? startAt : null;
  a.src = audioForLang(ep);
  if (plPendingSeek != null) { try { a.currentTime = plPendingSeek; } catch (e) {} }
  plShowBar(true);
  plMediaSession(true);
  plUpdateBar();
  if (plScreenActive()) renderPlaylist();
  if (autoplay) plPlay();
  plStore();
}
function plPlay() {
  var a = plAudio();
  if (!a || plCurId == null) return;
  var p = a.play();
  if (p && p.catch) p.catch(function () { plUpdateBar(); });
}
function plTogglePlay() { var a = plAudio(); if (!a || plCurId == null) return; if (a.paused) plPlay(); else a.pause(); }
function plPlayAt(i) { if (i >= 0 && i < playlist.length) plLoadTrack(playlist[i], true, 0); }
function plNext() { var i = plIndex(); if (i >= 0 && i < playlist.length - 1) plPlayAt(i + 1); }
function plPrev() {
  var a = plAudio(), i = plIndex();
  if (!a || i < 0) return;
  if (plPos() > 5 || i === 0) { plSeekTo(0); }   // like a car radio: first press goes back to the start
  else plPlayAt(i - 1);
}
function plSeekTo(sec) {
  var a = plAudio();
  if (!a || plCurId == null) return;
  sec = Math.max(0, sec);
  if (a.readyState === 0) plPendingSeek = sec; else plPendingSeek = null;
  try { a.currentTime = sec; } catch (e) {}
  plUpdateBar();
}
function plOnEnded() {
  var i = plIndex();
  if (i >= 0 && i < playlist.length - 1) plPlayAt(i + 1);
  else if (playlist.length) plLoadTrack(playlist[0], false, 0);   // end of the list: back to the first episode, paused
}
function plClose() {
  var a = plAudio();
  if (a) { a.pause(); a.removeAttribute('src'); a.load(); }
  plCurId = null; plPendingSeek = null;
  plShowBar(false);
  plMediaSession(false);
  plStore();
  if (plScreenActive()) renderPlaylist();
}
function plShowBar(on) {
  var bar = document.getElementById('pl-bar');
  if (bar) bar.hidden = !on;
  document.body.classList.toggle('pl-bar-on', !!on);
}
function plUpdateBar() {
  var a = plAudio(), ep = plCurId != null && plEp(plCurId);
  if (!a || !ep) return;
  var i = plIndex();
  var dur = (isFinite(a.duration) && a.duration > 0) ? a.duration : plDur(ep);
  var cur = Math.min(plPos(), dur);
  document.getElementById('pl-bar-count').textContent = (i + 1) + '/' + playlist.length;
  document.getElementById('pl-bar-name').textContent = epField(ep, 'title');
  var seek = document.getElementById('pl-seek');
  seek.max = Math.floor(dur);
  if (!plSeeking) {
    seek.value = Math.floor(cur);
    document.getElementById('pl-cur').textContent = fmtTime(cur);
  }
  seek.style.setProperty('--p', (dur ? (seek.value / dur) * 100 : 0) + '%');
  seek.setAttribute('aria-label', t('pl_seek'));
  seek.setAttribute('aria-valuetext', fmtTime(seek.value) + ' / ' + fmtTime(dur));
  document.getElementById('pl-dur').textContent = fmtTime(dur);
  var tg = document.getElementById('pl-toggle');
  var want = a.paused ? 'play' : 'pause';
  if (tg.getAttribute('data-state') !== want) { tg.innerHTML = PL_ICONS[want]; tg.setAttribute('data-state', want); }
  tg.setAttribute('aria-label', t(a.paused ? 'pl_play' : 'pl_pause'));
  document.getElementById('pl-prev').setAttribute('aria-label', t('pl_prev'));
  var nx = document.getElementById('pl-next');
  nx.setAttribute('aria-label', t('pl_next'));
  nx.disabled = i >= playlist.length - 1;
  document.getElementById('pl-close').setAttribute('aria-label', t('pl_close'));
  document.getElementById('pl-bar-title').setAttribute('aria-label', t('pl_button') + ': ' + epField(ep, 'title'));
}

// Lock screen / car display. Only claimed while the playlist is the active player, so the episode
// page's own player keeps the browser's default behaviour.
function plMediaSession(on) {
  if (!('mediaSession' in navigator)) return;
  var ms = navigator.mediaSession, a = plAudio();
  var ep = on && plCurId != null && plEp(plCurId);
  var handlers = {
    play: function () { plPlay(); },
    pause: function () { if (a) a.pause(); },
    previoustrack: function () { plPrev(); },
    nexttrack: function () { plNext(); },
    seekbackward: function (d) { plSeekTo(plPos() - ((d && d.seekOffset) || 15)); },
    seekforward: function (d) { plSeekTo(plPos() + ((d && d.seekOffset) || 30)); },
    seekto: function (d) { if (d && d.seekTime != null) plSeekTo(d.seekTime); }
  };
  Object.keys(handlers).forEach(function (k) {
    try { ms.setActionHandler(k, ep ? handlers[k] : null); } catch (e) {}
  });
  try {
    ms.metadata = ep ? new MediaMetadata({
      title: epField(ep, 'title'),
      artist: t('podcast_name'),
      album: epNumber(ep),
      artwork: [
        { src: 'podcast-cover-192.png', sizes: '192x192', type: 'image/png' },
        { src: 'podcast-cover-512.png', sizes: '512x512', type: 'image/png' }
      ]
    }) : null;
  } catch (e) {}
}
function plPositionState() {
  var a = plAudio();
  if (!a || !('mediaSession' in navigator) || !navigator.mediaSession.setPositionState) return;
  if (!isFinite(a.duration) || a.duration <= 0) return;
  try { navigator.mediaSession.setPositionState({ duration: a.duration, playbackRate: a.playbackRate || 1, position: Math.min(a.currentTime, a.duration) }); } catch (e) {}
}

// Changes to the list
function plToggle(id) {
  var i = playlist.indexOf(id);
  if (i >= 0) plRemoveAt(i); else { playlist.push(id); plChanged(); }
}
function plRemoveAt(i) {
  var a = plAudio(), wasCur = playlist[i] === plCurId, wasPlaying = !!a && !a.paused;
  playlist.splice(i, 1);
  if (wasCur) {
    if (playlist.length) plLoadTrack(playlist[Math.min(i, playlist.length - 1)], wasPlaying && i < playlist.length, 0);
    else plClose();
  }
  plChanged();
}
function plMove(i, d) {
  var j = i + d;
  if (j < 0 || j >= playlist.length) return;
  var x = playlist[i]; playlist[i] = playlist[j]; playlist[j] = x;
  plChanged({ index: j, act: d < 0 ? 'up' : 'down' });
}
function plClear() { playlist = []; plClose(); plChanged(); }
function plChanged(focus) { plStore(); plRefreshUI(focus); }

// Buttons that add / remove an episode
function plPaintAddBtn(b) {
  var ep = plEp(Number(b.getAttribute('data-id')));
  if (!ep) return;
  var added = plHas(ep.id);
  var want = added ? 'check' : 'plus';
  if (b.getAttribute('data-state') !== want) { b.innerHTML = PL_ICONS[want]; b.setAttribute('data-state', want); }
  b.classList.toggle('added', added);
  b.setAttribute('aria-pressed', added ? 'true' : 'false');
  b.title = t(added ? 'pl_remove' : 'pl_add');
  b.setAttribute('aria-label', t(added ? 'pl_remove' : 'pl_add') + ': ' + epField(ep, 'title'));
}
function plWrapRow(row, ep) {
  if (!plEnabled()) return row;   // review pages etc.: the row exactly as before
  var wrap = document.createElement('div');
  wrap.className = 'ep-row-wrap';
  var b = document.createElement('button');
  b.type = 'button';
  b.className = 'ep-row-add';
  b.setAttribute('data-id', ep.id);
  b.addEventListener('click', function () { plToggle(ep.id); });
  plPaintAddBtn(b);
  wrap.appendChild(row);
  wrap.appendChild(b);
  return wrap;
}
function plPaintDetailBtn() {
  var b = document.getElementById('btn-pl-toggle');
  if (!b) return;
  if (!plEnabled() || !selectedEpisode) { b.hidden = true; return; }
  var added = plHas(selectedEpisode.id);
  b.hidden = false;
  b.textContent = added ? t('pl_added') : '+ ' + t('pl_add');
  b.classList.toggle('added', added);
  b.setAttribute('aria-pressed', added ? 'true' : 'false');
  b.title = added ? t('pl_remove') : '';
}
function plRefreshUI(focus) {
  if (!plEnabled()) return;
  var hb = document.getElementById('btn-playlist');
  if (hb) {
    hb.hidden = false;
    document.getElementById('pl-head-count').textContent = playlist.length;
    hb.classList.toggle('has-items', playlist.length > 0);
    hb.setAttribute('aria-label', t('pl_button') + ' (' + playlist.length + ')');
  }
  document.querySelectorAll('.ep-row-add').forEach(plPaintAddBtn);
  plPaintDetailBtn();
  if (plScreenActive()) renderPlaylist(focus);
  plUpdateBar();
  if (plCurId != null && 'mediaSession' in navigator && navigator.mediaSession.metadata) plMediaSession(true);   // title in the new language
}

// "My playlist" screen
function renderPlaylist(focus) {
  var list = document.getElementById('pl-list');
  if (!list) return;
  var a = plAudio(), cur = plIndex(), total = 0;
  list.innerHTML = '';
  playlist.forEach(function (id, i) {
    var ep = plEp(id);
    total += plDur(ep);
    var item = document.createElement('div');
    var isCur = i === cur;
    item.className = 'pl-item' + (isCur ? ' current' : '') + (isCur && a && !a.paused ? ' playing' : '');
    item.innerHTML =
      '<span class="pl-pos">' + (i + 1) + '</span>' +
      '<button type="button" class="pl-item-main" data-act="play" title="' + esc(t('pl_play_this')) + '">' +
        '<span class="pl-item-title">' + esc(epField(ep, 'title')) + '</span>' +
        '<span class="pl-item-meta">' + esc(epNumber(ep)) + ' · ' + fmtTime(plDur(ep)) + '</span>' +
      '</button>' +
      '<button type="button" class="pl-ic pl-sm" data-act="up" aria-label="' + esc(t('pl_up')) + '" title="' + esc(t('pl_up')) + '"' + (i === 0 ? ' disabled' : '') + '>' + PL_ICONS.up + '</button>' +
      '<button type="button" class="pl-ic pl-sm" data-act="down" aria-label="' + esc(t('pl_down')) + '" title="' + esc(t('pl_down')) + '"' + (i === playlist.length - 1 ? ' disabled' : '') + '>' + PL_ICONS.down + '</button>' +
      '<button type="button" class="pl-ic pl-sm pl-rm" data-act="remove" aria-label="' + esc(t('pl_remove')) + '" title="' + esc(t('pl_remove')) + '">' + PL_ICONS.remove + '</button>';
    item.querySelectorAll('[data-act]').forEach(function (b) {
      b.addEventListener('click', function () {
        var act = b.getAttribute('data-act');
        if (act === 'play') { if (i === plIndex()) plTogglePlay(); else plPlayAt(i); }
        else if (act === 'up') plMove(i, -1);
        else if (act === 'down') plMove(i, 1);
        else if (act === 'remove') plRemoveAt(i);
      });
    });
    list.appendChild(item);
  });
  var has = playlist.length > 0;
  document.getElementById('pl-empty').hidden = has;
  document.getElementById('pl-actions').hidden = !has;
  list.hidden = !has;
  document.getElementById('pl-summary').textContent = has
    ? t(playlist.length === 1 ? 'pl_summary_one' : 'pl_summary', { n: playlist.length, time: fmtTime(total) }) : '';
  // Keep the keyboard focus on the arrow that was just used (or its neighbour at the end of the list).
  if (focus && list.children[focus.index]) {
    var fb = list.children[focus.index].querySelector('[data-act="' + focus.act + '"]');
    if (fb && fb.disabled) fb = list.children[focus.index].querySelector('[data-act="' + (focus.act === 'up' ? 'down' : 'up') + '"]');
    if (fb) fb.focus();
  }
}
function openPlaylist() { renderPlaylist(); showScreen('screen-playlist'); }

// Language switch while a playlist track is loaded: same episode, other language, about the same place.
function plOnLangChange() {
  if (!plEnabled() || plCurId == null) return;
  var ep = plEp(plCurId), a = plAudio();
  var lang = audioLangFor(ep);
  if (lang === plLang) return;
  var oldDur = (isFinite(a.duration) && a.duration > 0) ? a.duration : plDurIn(ep, plLang);
  var ratio = oldDur ? plPos() / oldDur : 0;
  plLoadTrack(plCurId, !a.paused, Math.floor(ratio * plDur(ep)));
}

function plInit() {
  if (!plEnabled()) return;
  var a = plAudio(), epA = document.getElementById('ep-audio');
  a.addEventListener('play', function () {
    if (epA) epA.pause();
    plMediaSession(true);
    plUpdateBar();
    if (plScreenActive()) renderPlaylist();
  });
  a.addEventListener('pause', function () { plUpdateBar(); plStore(); if (plScreenActive()) renderPlaylist(); });
  a.addEventListener('ended', plOnEnded);
  a.addEventListener('loadedmetadata', function () {
    if (plPendingSeek != null) {
      if (Math.abs(a.currentTime - plPendingSeek) > 1) { try { a.currentTime = plPendingSeek; } catch (e) {} }
      plPendingSeek = null;
    }
    plUpdateBar();
    plPositionState();
  });
  a.addEventListener('timeupdate', function () {
    plUpdateBar();
    if (Date.now() - plLastStore > 5000) { plStore(); plPositionState(); }
  });
  a.addEventListener('seeked', function () { plUpdateBar(); plPositionState(); });
  // One player at a time: starting the episode page's player pauses the playlist.
  if (epA) epA.addEventListener('play', function () { a.pause(); plMediaSession(false); });
  window.addEventListener('pagehide', plStore);

  document.getElementById('pl-toggle').addEventListener('click', plTogglePlay);
  document.getElementById('pl-prev').addEventListener('click', plPrev);
  document.getElementById('pl-next').addEventListener('click', plNext);
  document.getElementById('pl-close').addEventListener('click', plClose);
  document.getElementById('pl-bar-title').addEventListener('click', openPlaylist);
  var seek = document.getElementById('pl-seek');
  seek.addEventListener('input', function () {
    plSeeking = true;
    document.getElementById('pl-cur').textContent = fmtTime(seek.value);
    seek.style.setProperty('--p', (seek.max > 0 ? (seek.value / seek.max) * 100 : 0) + '%');
  });
  seek.addEventListener('change', function () { plSeeking = false; plSeekTo(Number(seek.value)); });

  document.getElementById('btn-playlist').addEventListener('click', openPlaylist);
  document.getElementById('btn-back-episodes-pl').addEventListener('click', function () { showScreen('screen-episodes'); });
  document.getElementById('pl-play-all').addEventListener('click', function () { plPlayAt(0); });
  var clr = document.getElementById('pl-clear');
  clr.addEventListener('click', function () {   // two taps, so a slip of the finger does not empty the list
    if (plClearTimer) { clearTimeout(plClearTimer); plClearTimer = null; clr.textContent = t('pl_clear'); plClear(); return; }
    clr.textContent = t('pl_clear_confirm');
    plClearTimer = setTimeout(function () { plClearTimer = null; clr.textContent = t('pl_clear'); }, 4000);
  });
  var db = document.getElementById('btn-pl-toggle');
  if (db) db.addEventListener('click', function () { if (selectedEpisode) plToggle(selectedEpisode.id); });
  // The quiz is taken without audio in the background.
  document.getElementById('btn-start-quiz').addEventListener('click', function () { a.pause(); });

  plRestore();
}

// ── Wire up ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  // Registration screen is disabled for now - go straight to the catalogue.
  showScreen('screen-episodes');
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

  plInit();   // playlist (restores the saved list)

  // Apply initial language (sets active states + static strings).
  applyLang();
});
