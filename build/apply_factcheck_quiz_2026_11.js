#!/usr/bin/env node
// Quiz updates from the LuxTrust fact-check of 2 Nov 2026, validated by Jacques.
// Usage: node build/apply_factcheck_quiz_2026_11.js [--write]
// Each edit replaces one substring in one quiz field; re-running is safe.
const fs = require('fs');
const path = require('path');
const FILE = path.join(__dirname, '..', 'episodes_data.js');

const Q = []; // [key, field, questionIndex(0-based), part ('text'|'explanation'|optionIndex), old, new]
const q = (...a) => Q.push(a);

// LuxTrust Q1: 'qualified' provider instead of 'European-certified'
q('luxtrust', 'questions', 0, 'explanation', 'provided by a European-certified Certificate Authority and trust service provider.', "provided by a Certificate Authority and trust service provider officially recognised as 'qualified' in the European Union.");
q('luxtrust', 'questions_fr', 0, 'explanation', 'fournie par une autorité de certification et un prestataire de services de confiance certifiés au niveau européen.', 'fournie par une autorité de certification et un prestataire de services de confiance officiellement reconnu comme « qualifié » dans l\'Union européenne.');
q('luxtrust', 'questions_de', 0, 'explanation', 'bereitgestellt von einer europäisch zertifizierten Zertifizierungsstelle und einem Vertrauensdiensteanbieter.', 'bereitgestellt von einer Zertifizierungsstelle und einem Vertrauensdiensteanbieter, der in der Europäischen Union offiziell als „qualifiziert" anerkannt ist.');
// LuxTrust Q4: where you can be identified in person (correct option kept short so it is not the longest)

q('luxtrust', 'questions', 3, 'explanation', 'face-to-face with an agent or remotely by video identification.', 'in person (at LuxTrust, at a partner such as your bank, or at a notary) or remotely by video identification.');
q('luxtrust', 'questions_fr', 3, 'explanation', 'en face à face avec un agent ou à distance par identification vidéo.', 'en personne (chez LuxTrust, chez un partenaire comme votre banque, ou chez un notaire) ou à distance par identification vidéo.');
q('luxtrust', 'questions_de', 3, 'explanation', 'persönlich bei einem Agenten oder aus der Ferne per Video-Identifikation.', 'persönlich (bei LuxTrust, bei einem Partner wie Ihrer Bank oder bei einem Notar) oder aus der Ferne per Video-Identifikation.');
q('luxtrust', 'questions', 3, 3, 'in person with an agent, or remotely', 'in person, or remotely');
q('luxtrust', 'questions_fr', 3, 3, 'en personne avec un agent, ou à distance', 'en personne, ou à distance');
q('luxtrust', 'questions_de', 3, 3, 'persönlich bei einem Agenten oder aus der Ferne', 'persönlich oder aus der Ferne');
// Digital Inclusion Q3 (2 Nov 2026): conditions from the main application page, 12+ rule
q('digitalinclusion', 'questions', 2, 'explanation', null, "You must live in Luxembourg and meet one condition – for example your household receives the cost-of-living allowance (allocation de vie chère), you are in a collective debt settlement procedure, you hold a 'vie privée' residence permit, or you are an asylum seeker, an unaccompanied minor or under temporary protection. Each household member aged 12 or older can get their own computer, as long as donations allow. See digital-inclusion.lu for the current conditions and waiting time.");
q('digitalinclusion', 'questions_fr', 2, 'explanation', null, "Vous devez vivre au Luxembourg et remplir une condition – par exemple votre ménage perçoit l'allocation de vie chère (AVC), vous bénéficiez d'un règlement collectif des dettes, vous avez un titre de séjour « vie privée », ou vous êtes demandeur d'asile, mineur non accompagné ou sous protection temporaire. Chaque membre du ménage âgé de 12 ans ou plus peut recevoir son propre ordinateur, tant que les dons le permettent. Consultez digital-inclusion.lu pour les conditions et le délai d'attente actuels.");
q('digitalinclusion', 'questions_de', 2, 'explanation', null, "Sie müssen in Luxemburg leben und eine Bedingung erfüllen – zum Beispiel bezieht Ihr Haushalt die Teuerungszulage (allocation de vie chère), Sie sind in einem kollektiven Schuldenregulierungsverfahren, Sie haben eine Aufenthaltserlaubnis „Privatleben“ (vie privée), oder Sie sind Asylsuchender, unbegleiteter Minderjähriger oder stehen unter vorübergehendem Schutz. Jedes Haushaltsmitglied ab 12 Jahren kann einen eigenen Computer bekommen, solange die Spenden reichen. Die aktuellen Bedingungen und die Wartezeit finden Sie auf digital-inclusion.lu.");
// Work in Luxembourg Q3 (2 Nov 2026): '11,000 candidates' no longer published -> pre-screened by ADEM
q('workinluxembourg', 'questions', 2, 0 + 2, 'and around 11,000 pre-selected candidates', 'and candidates pre-screened by ADEM');
q('workinluxembourg', 'questions', 2, 'explanation', 'and the pool already holds around 11,000 candidates pre-selected by ADEM.', 'and every candidate profile is pre-screened by ADEM. The board focuses on shortage occupations.');
q('workinluxembourg', 'questions_fr', 2, 0 + 2, 'et environ 11 000 candidats présélectionnés', "et des candidats présélectionnés par l'ADEM");
q('workinluxembourg', 'questions_fr', 2, 'explanation', "et le vivier compte déjà environ 11 000 candidats présélectionnés par l'ADEM.", "et chaque profil de candidat est présélectionné par l'ADEM. Le Job Board se concentre sur les métiers en pénurie.");
q('workinluxembourg', 'questions_de', 2, 0 + 2, 'und rund 11 000 vorausgewählten Kandidaten', 'und von ADEM vorab geprüften Kandidaten');
q('workinluxembourg', 'questions_de', 2, 'explanation', 'und der Pool umfasst bereits rund 11 000 von ADEM vorausgewählte Kandidaten.', 'und jedes Kandidatenprofil wird von ADEM vorab geprüft. Das Job Board konzentriert sich auf Mangelberufe.');
// DSP-CNS (9 Nov 2026): no 'about half' figure; DSP also opens in the MyGuichet eSpace
q('dsp_cns', 'questions', 2, 'explanation', 'About half of doctors now use immediate direct payment:', 'More and more doctors and dentists use immediate direct payment:');
q('dsp_cns', 'questions_fr', 2, 'explanation', 'Environ la moitié des médecins utilisent désormais le paiement immédiat direct :', 'De plus en plus de médecins et de dentistes utilisent le paiement immédiat direct :');
q('dsp_cns', 'questions_de', 2, 'explanation', 'Etwa die Hälfte der Ärzte nutzt inzwischen die sofortige Direktzahlung:', 'Immer mehr Ärzte und Zahnärzte nutzen die sofortige Direktzahlung:');
q('dsp_cns', 'questions_lb', 2, 'explanation', "Ongeféier d'Hallschent vun den Dokteren benotzt elo den direkte Paiement:", 'Ëmmer méi Dokteren an Zänndokteren benotzen den direkte Paiement:');
q('dsp_cns', 'questions', 4, 'explanation', 'you log in through the eSanté portal — or use', 'you open it in your MyGuichet eSpace or on the eSanté portal — or use');
q('dsp_cns', 'questions_fr', 4, 'explanation', 'vous vous connectez via le portail eSanté — ou', 'vous l\'ouvrez dans votre eSpace MyGuichet ou sur le portail eSanté — ou');
q('dsp_cns', 'questions_de', 4, 'explanation', 'melden Sie sich über das eSanté-Portal an — oder', 'öffnen Sie es in Ihrem MyGuichet-eSpace oder auf dem eSanté-Portal — oder');
q('dsp_cns', 'questions_lb', 4, 'explanation', 'loggt Dir Iech iwwer den eSanté-Portal an — oder', 'maacht Dir en an Ärem MyGuichet-eSpace oder um eSanté-Portal op — oder');
// LU-Alert (9 Nov 2026): no 'cannot opt out'; sirens warn of serious danger locally or nationwide (lu-alert.lu Sirens page)
q('lualert', 'questions', 1, 'explanation', 'you do not sign up – and cannot really opt out.', 'you do not sign up.');
q('lualert', 'questions_fr', 1, 'explanation', 'vous ne vous inscrivez pas – et vous ne pouvez pas vraiment vous y soustraire.', 'vous ne vous inscrivez pas.');
q('lualert', 'questions_de', 1, 'explanation', 'melden Sie sich nicht an – und können sich auch nicht wirklich abmelden.', 'melden Sie sich nicht an.');
q('lualert', 'questions_lb', 1, 'explanation', 'schreift Dir Iech net an – an Dir kënnt Iech och net wierklech ofmellen.', 'schreift Dir Iech net an.');
q('lualert', 'questions', 3, 2, null, 'To warn of a serious danger');
q('lualert', 'questions_fr', 3, 2, null, "Pour avertir d'un danger grave");
q('lualert', 'questions_de', 3, 2, null, 'Um vor einer ernsten Gefahr zu warnen');
q('lualert', 'questions_lb', 3, 2, null, 'Fir virun enger eeschter Gefor ze warnen');
q('lualert', 'questions', 3, 'explanation', null, 'Sirens warn the population of a serious danger – in one area or across the whole country. A long, steady tone means: get to safety and follow the news; a rising and falling tone means: go into a solid building and close doors and windows. Most alerts reach you by phone (Cell Broadcast and SMS), the app, websites and the media. The sirens are tested on the first Monday of each month, around noon.');
q('lualert', 'questions_fr', 3, 'explanation', null, "Les sirènes avertissent la population d'un danger grave – dans une zone ou dans tout le pays. Un son long et continu veut dire : mettez-vous en sécurité et suivez les informations ; un son montant et descendant veut dire : entrez dans un bâtiment solide et fermez portes et fenêtres. La plupart des alertes vous atteignent par téléphone (Cell Broadcast et SMS), l'application, les sites internet et les médias. Les sirènes sont testées le premier lundi de chaque mois, vers midi.");
q('lualert', 'questions_de', 3, 'explanation', null, 'Sirenen warnen die Bevölkerung vor einer ernsten Gefahr – in einem Gebiet oder im ganzen Land. Ein langer, gleichbleibender Ton heißt: in Sicherheit bringen und die Nachrichten verfolgen; ein auf- und abschwellender Ton heißt: in ein festes Gebäude gehen und Türen und Fenster schließen. Die meisten Warnungen erreichen Sie über das Telefon (Cell Broadcast und SMS), die App, Websites und die Medien. Die Sirenen werden am ersten Montag jedes Monats gegen Mittag getestet.');
q('lualert', 'questions_lb', 3, 'explanation', null, "D'Sirene warnen d'Bevëlkerung virun enger eeschter Gefor – an enger Regioun oder am ganze Land. E laangen, gläichméissegen Toun heescht: a Sécherheet goen an d'Noriichte verfollegen; en op- an ofschwellenden Toun heescht: an e feste Gebai goen an Dieren a Fënsteren zoumaachen. Déi meescht Alarmer erreechen Iech iwwer den Handy (Cell Broadcast an SMS), d'App, d'Websäiten an d'Medien. D'Sirene ginn den éischte Méindeg vun all Mount géint Mëtteg getest.");
// Maison de l'Orientation (9 Nov 2026): Espace orientation 10:00-17:00 (page of 31.08.2026)
q('maison_orientation', 'questions', 1, 'explanation', 'Monday to Friday, 8:00–17:00', 'Monday to Friday, 10:00–17:00');
q('maison_orientation', 'questions_fr', 1, 'explanation', 'du lundi au vendredi, de 8h00 à 17h00', 'du lundi au vendredi, de 10h00 à 17h00');
q('maison_orientation', 'questions_de', 1, 'explanation', 'Montag bis Freitag, 8:00–17:00 Uhr', 'Montag bis Freitag, 10:00–17:00 Uhr');

// Zukunftskeess (9 Nov 2026): law 8746 in force 1 Jan 2027 – durable amounts, no cents
q('zukunftskeess', 'questions', 1, 'text', '(about €1,740)', '(more than €1,700)');
q('zukunftskeess', 'questions_fr', 1, 'text', '(environ 1 740 €)', '(plus de 1 700 €)');
q('zukunftskeess', 'questions_de', 1, 'text', '(etwa 1.740 €)', '(mehr als 1.700 €)');
q('zukunftskeess', 'questions', 1, 0, 'of about €580', 'of nearly €600');
q('zukunftskeess', 'questions_fr', 1, 0, "d'environ 580 €", 'de près de 600 €');
q('zukunftskeess', 'questions_de', 1, 0, 'von etwa 580 €', 'von fast 600 €');
q('zukunftskeess', 'questions', 1, 'explanation', null, 'The birth allowance totals more than €1,700, paid in three independent instalments of nearly €600 – prenatal, birth and postnatal – each tied to completing the medical examinations for mother and baby. From January 2027 it rises with the cost of living.');
q('zukunftskeess', 'questions_fr', 1, 'explanation', null, "L'allocation de naissance s'élève au total à plus de 1 700 €, payée en trois tranches indépendantes de près de 600 € – prénatale, de naissance et postnatale – chacune liée à la réalisation des examens médicaux pour la mère et le bébé. À partir de janvier 2027, elle suit le coût de la vie.");
q('zukunftskeess', 'questions_de', 1, 'explanation', null, 'Die Geburtszulage beträgt insgesamt mehr als 1.700 €, gezahlt in drei unabhängigen Raten von fast 600 € – vorgeburtlich, Geburt und nachgeburtlich – jede gebunden an die ärztlichen Untersuchungen für Mutter und Baby. Ab Januar 2027 steigt sie mit den Lebenshaltungskosten.');
q('zukunftskeess', 'questions', 3, 'explanation', '(around €115 for ages 6–11 and €235 for 12 and over)', '(from 2027: more than €175 for ages 6–11 and more than €325 for 12 and over)');
q('zukunftskeess', 'questions_fr', 3, 'explanation', '(environ 115 € pour les 6-11 ans et 235 € pour les 12 ans et plus)', '(à partir de 2027 : plus de 175 € pour les 6-11 ans et plus de 325 € pour les 12 ans et plus)');
q('zukunftskeess', 'questions_de', 3, 'explanation', '(etwa 115 € für 6- bis 11-Jährige und 235 € für 12 Jahre und älter)', '(ab 2027: mehr als 175 € für 6- bis 11-Jährige und mehr als 325 € für 12 Jahre und älter)');

// Episode descriptions: [key, field, old, new]
const D = [];
D.push(['zukunftskeess', 'description', 'can last to 25 for students', 'can last to 25 for pupils still in secondary school']);
D.push(['zukunftskeess', 'description_fr', "peut durer jusqu'à 25 ans pour les étudiants", "peut durer jusqu'à 25 ans pour les élèves du secondaire"]);
D.push(['zukunftskeess', 'description_de', 'für Studierende bis 25 dauern kann', 'für Schülerinnen und Schüler der Sekundarstufe bis 25 dauern kann']);

// FNS (9 Nov 2026): no MyGuichet procedure for FNS benefits
D.push(['fns', 'description', 'Apply on fns.lu or MyGuichet.lu', 'Forms and an online calculator are on fns.lu']);
D.push(['fns', 'description_fr', 'Faites votre demande sur fns.lu ou MyGuichet.lu', 'Formulaires et calculateur en ligne sur fns.lu']);
D.push(['fns', 'description_de', 'Stellen Sie Ihren Antrag auf fns.lu oder MyGuichet.lu', 'Formulare und Online-Rechner auf fns.lu']);

// ONIS (9 Nov 2026): ADEM profiles first, refers people far from work to ONIS
q('onis', 'questions', 1, 'explanation', 'while ONIS handles the inclusion side, helping the person move back toward work and society.', 'while the inclusion side is handled by ADEM for people ready to look for work, and by ONIS for people who are still far from work, helping them move back toward work and society.');
q('onis', 'questions_fr', 1, 'explanation', "tandis que l'ONIS s'occupe du volet inclusion, en aidant la personne à se rapprocher à nouveau du travail et de la société.", "tandis que le volet inclusion est assuré par l'ADEM pour les personnes prêtes à chercher un emploi, et par l'ONIS pour celles qui sont encore éloignées du travail, en les aidant à se rapprocher à nouveau du travail et de la société.");
q('onis', 'questions_de', 1, 'explanation', 'während ONIS sich um die Eingliederungsseite kümmert und der Person hilft, sich wieder der Arbeit und der Gesellschaft anzunähern.', 'während die Eingliederungsseite für Menschen, die bereit sind, Arbeit zu suchen, von der ADEM übernommen wird, und für Menschen, die noch weit von der Arbeit entfernt sind, von ONIS – das ihnen hilft, sich wieder der Arbeit und der Gesellschaft anzunähern.');
q('onis', 'questions', 3, 'explanation', 'You are invited to a meeting,', 'If ADEM refers you to ONIS, you are invited to an information meeting,');
q('onis', 'questions_fr', 3, 'explanation', 'Vous êtes invité à un entretien,', "Si l'ADEM vous oriente vers l'ONIS, vous êtes invité à une réunion d'information,");
q('onis', 'questions_de', 3, 'explanation', 'Sie werden zu einem Gespräch eingeladen,', 'Wenn die ADEM Sie an ONIS verweist, werden Sie zu einer Informationsversammlung eingeladen,');
D.push(['onis', 'description', 'ONIS helps people furthest from work move forward', 'ONIS helps people furthest from work – referred by ADEM – move forward']);
D.push(['onis', 'description_fr', "l'ONIS aide les personnes les plus éloignées de l'emploi à avancer", "l'ONIS aide les personnes les plus éloignées de l'emploi – orientées par l'ADEM – à avancer"]);
D.push(['onis', 'description_de', 'hilft ONIS den Menschen, die am weitesten von der Arbeit entfernt sind, voranzukommen', 'hilft ONIS den Menschen, die am weitesten von der Arbeit entfernt sind – von der ADEM verwiesen –, voranzukommen']);

// Episodes 17-21 (9 Nov 2026)
q('habitat', 'questions', 3, 'explanation', 'the Observatoire does not publish detailed house prices.', 'the Observatoire does not publish detailed house prices. For houses, STATEC publishes a general price index instead.');
q('habitat', 'questions_fr', 3, 'explanation', "l'Observatoire ne diffuse pas de prix détaillés des maisons.", "l'Observatoire ne diffuse pas de prix détaillés des maisons. Pour les maisons, le STATEC publie plutôt un indice général des prix.");
q('habitat', 'questions_de', 3, 'explanation', 'gibt das Observatoire keine detaillierten Hauspreise heraus.', 'gibt das Observatoire keine detaillierten Hauspreise heraus. Für Häuser veröffentlicht der STATEC stattdessen einen allgemeinen Preisindex.');
q('klima', 'questions', 3, 'explanation', null, 'The Klimabonus is the national state grant scheme. It supports energy-efficient renovation, renewable heating such as heat pumps, solar panels and batteries, electric vehicles and charging stations. It was renewed in 2026, for most projects until 2030. Klima-Agence helps you find which grants apply.');
q('klima', 'questions_fr', 3, 'explanation', null, "Le Klimabonus est le régime national d'aides de l'État. Il soutient la rénovation énergétique, le chauffage renouvelable comme les pompes à chaleur, les panneaux photovoltaïques et les batteries, les véhicules électriques et les bornes de recharge. Il a été renouvelé en 2026, pour la plupart des projets jusqu'en 2030. La Klima-Agence vous aide à trouver les aides qui s'appliquent.");
q('klima', 'questions_de', 3, 'explanation', null, 'Der Klimabonus ist das nationale staatliche Förderprogramm. Es unterstützt energetische Sanierung, erneuerbares Heizen wie Wärmepumpen, Photovoltaikanlagen und Batterien, Elektrofahrzeuge und Ladestationen. Es wurde 2026 erneuert, für die meisten Projekte bis 2030. Die Klima-Agence hilft Ihnen, die passenden Beihilfen zu finden.');

// Episodes 22-26 (9 Nov 2026): CGDIS volunteer share without a stale number
q('cgdis', 'questions', 2, 'explanation', null, "Thousands of volunteers make up around 90% of the CGDIS's firefighters (CGDIS annual report 2025). They have ordinary jobs but drop everything to help when the alarm sounds.");
q('cgdis', 'questions_fr', 2, 'explanation', "Plus de 3 900 pompiers volontaires représentent environ 90 % de l'effectif opérationnel du CGDIS.", "Des milliers de volontaires représentent environ 90 % des pompiers du CGDIS (rapport annuel 2025).");
q('cgdis', 'questions_de', 2, 'explanation', 'Mehr als 3 900 freiwillige Feuerwehrleute machen rund 90 % der einsatzfähigen Belegschaft des CGDIS aus.', 'Tausende Freiwillige machen rund 90 % der Feuerwehrleute des CGDIS aus (Jahresbericht 2025).');

// Episodes 32-36 (9 Nov 2026): GOVCERT.LU and CIRCL under the NIS2 law; SIS since 2016, Ministry of Labour
q('govcert', 'questions', 1, 'explanation', null, "GOVCERT.LU is the central contact point for IT incidents affecting the information systems of the State and of critical infrastructure operators — the systems a country cannot function without. Since Luxembourg's 2026 NIS2 law, other companies and the communes turn to its sister team, CIRCL.");
q('govcert', 'questions_fr', 1, 'explanation', null, "Le GOVCERT.LU est le point de contact central pour les incidents informatiques touchant les systèmes d'information de l'État et des opérateurs d'infrastructures critiques — les systèmes sans lesquels un pays ne peut pas fonctionner. Depuis la loi NIS2 luxembourgeoise de 2026, les autres entreprises et les communes s'adressent à son équipe sœur, le CIRCL.");
q('govcert', 'questions_de', 1, 'explanation', null, "GOVCERT.LU ist die zentrale Anlaufstelle für IT-Vorfälle, die die Informationssysteme des Staates und der Betreiber kritischer Infrastrukturen betreffen – die Systeme, ohne die ein Land nicht funktionieren kann. Seit dem luxemburgischen NIS2-Gesetz von 2026 wenden sich andere Unternehmen und die Gemeinden an das Schwesterteam CIRCL.");
q('ess', 'questions', 2, 'explanation', null, "Luxembourg created a legal status, the societal impact company (société d'impact sociétal, SIS), which lets you build a real business whose official purpose is social impact. It has been recognised by law since 2016, and companies are approved by the Ministry of Labour.");
q('ess', 'questions_fr', 2, 'explanation', null, "Le Luxembourg a créé un statut légal, la société d'impact sociétal (SIS), qui permet de bâtir une véritable entreprise dont l'objet officiel est l'impact social. Il est reconnu par la loi depuis 2016, et les sociétés sont agréées par le ministère du Travail.");
q('ess', 'questions_de', 2, 'explanation', null, "Luxemburg hat einen rechtlichen Status geschaffen, die Gesellschaft mit gesellschaftlicher Wirkung (société d'impact sociétal, SIS), mit der man ein echtes Unternehmen aufbauen kann, dessen offizieller Zweck die soziale Wirkung ist. Er ist seit 2016 gesetzlich anerkannt, und die Unternehmen werden vom Arbeitsministerium zugelassen.");

// Episodes 37-41 (9 Nov 2026): language leave is for Luxembourgish
q('lll', 'questions', 3, 'explanation', 'or language leave)', 'or language leave to learn Luxembourgish)');
q('lll', 'questions_fr', 3, 'explanation', 'ou le congé linguistique)', 'ou le congé linguistique pour apprendre le luxembourgeois)');
q('lll', 'questions_de', 3, 'explanation', 'oder den Sprachurlaub)', 'oder den Sprachurlaub für Luxemburgisch)');

// House of the Greater Region (10 Nov 2026): almost 12 million, commuter shares, in Esch since 2015
q('granderegion', 'questions', 0, 'explanation', 'with 11.8 million inhabitants', 'with almost 12 million inhabitants');
q('granderegion', 'questions_fr', 0, 'explanation', "avec 11,8 millions d'habitants", "avec près de 12 millions d'habitants");
q('granderegion', 'questions_de', 0, 'explanation', '11,8 Millionen Einwohnern', 'fast 12 Millionen Einwohnern');
q('granderegion', 'questions', 1, 'explanation', 'Around half live in France and roughly three-quarters work in Luxembourg.', 'More than half live in France and more than four out of five work in Luxembourg.');
q('granderegion', 'questions_fr', 1, 'explanation', 'La moitié environ vit en France et à peu près les trois quarts travaillent au Luxembourg.', 'Plus de la moitié vivent en France et plus de quatre sur cinq travaillent au Luxembourg.');
q('granderegion', 'questions_de', 1, 'explanation', 'Rund die Hälfte lebt in Frankreich und etwa drei Viertel arbeiten in Luxemburg.', 'Mehr als die Hälfte lebt in Frankreich, und mehr als vier von fünf arbeiten in Luxemburg.');
q('granderegion', 'questions', 2, 2, '(opened 2015)', '(since 2015)');
q('granderegion', 'questions_fr', 2, 2, '(ouvert en 2015)', '(depuis 2015)');
q('granderegion', 'questions_de', 2, 2, '(2015 eröffnet)', '(seit 2015)');
q('granderegion', 'questions', 2, 'explanation', 'Opened in 2015 in Esch-sur-Alzette, the House', 'In Esch-sur-Alzette since 2015 (and a shared office in Luxembourg City since 1999), the House');
q('granderegion', 'questions_fr', 2, 'explanation', 'Ouverte en 2015 à Esch-sur-Alzette, la Maison', 'Installée à Esch-sur-Alzette depuis 2015 (et bureau commun à Luxembourg-Ville depuis 1999), la Maison');
q('granderegion', 'questions_de', 2, 'explanation', 'Das 2015 in Esch an der Alzette eröffnete Haus der Großregion ist', 'Das Haus der Großregion – seit 2015 in Esch an der Alzette, davor seit 1999 ein gemeinsames Büro in Luxemburg-Stadt – ist');
D.push(['granderegion', 'description', '11.8 million people', 'almost 12 million people']);
D.push(['granderegion', 'description', 'in Esch-sur-Alzette, opened in 2015, which hosts', 'in Esch-sur-Alzette (there since 2015), which hosts']);
D.push(['granderegion', 'description_fr', "11,8 millions d'habitants", "près de 12 millions d'habitants"]);
D.push(['granderegion', 'description_fr', 'à Esch-sur-Alzette, ouverte en 2015, qui accueille', 'à Esch-sur-Alzette (installée depuis 2015), qui accueille']);
D.push(['granderegion', 'description_de', '11,8 Millionen Menschen', 'fast 12 Millionen Menschen']);
D.push(['granderegion', 'description_de', 'in Esch an der Alzette, das 2015 eröffnet wurde und', 'in Esch an der Alzette, das seit 2015 dort ansässig ist und']);

// --only=key1,key2 limits the run to those episodes (older entries may no longer match after balance_quiz_answers reshuffled options)
const ONLY = ((process.argv.find(a => a.startsWith('--only=')) || '').slice(7)).split(',').filter(Boolean);
if (ONLY.length) { for (const L of [Q, D]) { const keep = L.filter(x => ONLY.includes(x[0])); L.length = 0; L.push(...keep); } }
const src = fs.readFileSync(FILE, 'utf8');
const i = src.indexOf('const EPISODES');
const banner = src.slice(0, i);
const E = new Function(src + ';return EPISODES;')();
const ser = (data) => banner + 'const EPISODES = ' + JSON.stringify(data, null, 1) + ';\n';
if (ser(E) !== src) { console.error('Round-trip check failed – file format differs, aborting.'); process.exit(1); }

let applied = 0, skipped = 0; const problems = [];
for (const [key, field, qi, part, oldS, newS] of Q) {
  const ep = E.find(e => e.key === key);
  const qq = ep && ep[field] && ep[field][qi];
  if (!qq) { problems.push(`${key} ${field} Q${qi + 1}: not found`); continue; }
  const get = () => (typeof part === 'number' ? qq.options[part] : qq[part]);
  const set = (v) => { if (typeof part === 'number') qq.options[part] = v; else qq[part] = v; };
  const cur = get();
  if (oldS === null) { if (cur === newS) skipped++; else { set(newS); applied++; } continue; }
  if (cur.includes(newS)) { skipped++; continue; } // new text may contain the old one
  const n = cur.split(oldS).length - 1;
  if (n === 0 && cur.includes(newS)) { skipped++; continue; }
  if (n !== 1) { problems.push(`${key} ${field} Q${qi + 1} ${part}: found ${n}x "${oldS}"`); continue; }
  set(cur.replace(oldS, newS)); applied++;
}

for (const [key, field, oldS, newS] of D) {
  const ep = E.find(e => e.key === key); const cur = ep && ep[field];
  if (!cur) { problems.push(`${key} ${field}: not found`); continue; }
  if (cur.includes(newS)) { skipped++; continue; }
  if (cur.split(oldS).length - 1 !== 1) { problems.push(`${key} ${field}: "${oldS}" not found once`); continue; }
  ep[field] = cur.replace(oldS, newS); applied++;
}
problems.forEach(p => console.log('PROBLEM', p));
console.log(`quiz edits: ${applied} applied, ${skipped} already done, ${problems.length} problems`);
if (problems.length) process.exit(1);

// sanity: every question still has 4 distinct options and a valid answer
let bad = 0;
for (const e of E) for (const f of ['questions', 'questions_fr', 'questions_de', 'questions_lb']) (e[f] || []).forEach((x, n) => {
  if (x.options.length !== 4 || new Set(x.options).size !== 4 || !(x.correct >= 0 && x.correct < 4)) { bad++; console.log('BAD', e.key, f, n + 1); }
});
if (bad) process.exit(1);
if (process.argv.includes('--write')) { fs.writeFileSync(FILE, ser(E)); console.log('written', FILE); }
