#!/usr/bin/env python3
"""Fact-check episodes 22-26 (9 Nov 2026): fondseuropeens, zesumme, cgdis, statec, environnement. EN/FR/DE/LB."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from lib_factcheck import apply
DATE = {"en": "Fact-checked 9 November 2026.", "fr": "Vérifié le 9 novembre 2026.", "de": "Geprüft am 9. November 2026.", "lb": "Iwwerpréift den 9. November 2026."}
def note(en, fr, de, lb): return {"en": en + " " + DATE["en"], "fr": fr + " " + DATE["fr"], "de": de + " " + DATE["de"], "lb": lb + " " + DATE["lb"]}

apply("fondseuropeens", {
 14: {"en": "For Luxembourg, in the current period from 2021 to 2027, this fund is around twenty-one million euros. And the next period, from 2028, is already being prepared at European level.",
      "fr": "Pour le Luxembourg, dans la période actuelle de 2021 à 2027, ce fonds représente environ vingt et un millions d'euros. Et la prochaine période, à partir de 2028, est déjà en préparation au niveau européen.",
      "de": "Für Luxemburg beläuft sich dieser Fonds im aktuellen Zeitraum von 2021 bis 2027 auf etwa einundzwanzig Millionen Euro. Und der nächste Zeitraum, ab 2028, wird auf europäischer Ebene schon vorbereitet.",
      "lb": "Fir Lëtzebuerg beleeft sech dëse Fong an der aktueller Period vu 2021 bis 2027 op ongeféier eenanzwanzeg Milliounen Euro. An déi nächst Period, ab 2028, gëtt op europäeschem Niveau schonn virbereet."},
 20: {"en": "There are also funds for internal security and for managing borders. And there is Interreg, which supports cross-border projects with our neighbours... for example in the Greater Region.",
      "fr": "Il existe aussi des fonds pour la sécurité intérieure et pour la gestion des frontières. Et il y a Interreg, qui soutient des projets transfrontaliers avec nos voisins... par exemple dans la Grande Région.",
      "de": "Es gibt auch Fonds für die innere Sicherheit und für die Verwaltung der Grenzen. Und es gibt Interreg, das grenzüberschreitende Projekte mit unseren Nachbarn unterstützt... zum Beispiel in der Großregion.",
      "lb": "Et gëtt och Fongen fir déi bannenzeg Sécherheet a fir d'Verwaltung vun de Grenzen. An et gëtt Interreg, dat grenziwwerschreidend Projeten mat eisen Noperen ënnerstëtzt... zum Beispill an der Groussregioun."},
}, note("Update: Interreg (incl. Interreg Grande Région small-projects calls 2026) added; programmes 2021–2027 with FEDER, FSE+, AMIF, ISF, BMVI, Interreg (fonds-europeens.public.lu, 2026).",
        "Mise à jour : Interreg ajouté (fonds-europeens.public.lu, 2026).", "Aktualisierung: Interreg ergänzt (fonds-europeens.public.lu, 2026).", "Aktualiséierung: Interreg derbäi."))

apply("zesumme", {
 22: {"en": "And then the work happens in a participatory, co-creative way... together with the people who proposed it. Ministries and administrations can also post their own projects there, to ask for people's opinions.",
      "fr": "Et ensuite, le travail se déroule de manière participative et co-créative... avec les personnes qui l'ont proposé. Les ministères et les administrations peuvent aussi y publier leurs propres projets, pour demander l'avis des gens.",
      "de": "Und dann erfolgt die Arbeit auf partizipative, ko-kreative Weise... gemeinsam mit denen, die den Vorschlag gemacht haben. Ministerien und Verwaltungen können dort auch eigene Projekte veröffentlichen, um die Meinung der Menschen einzuholen.",
      "lb": "An dann passéiert d'Aarbecht op eng participativ, ko-kreativ Manéier... zesummen mat de Leit déi et virgeschloen hunn. Ministèren an Administratiounen kënnen do och hir eege Projeten publizéieren, fir d'Meenung vun de Leit ze froen."},
}, note("Update: ministries and administrations can also submit projects for stakeholder feedback; platform managed by the Council for Simplification (mindigital.gouvernement.lu).",
        "Mise à jour : les ministères et administrations peuvent aussi y soumettre des projets (mindigital.gouvernement.lu).", "Aktualisierung: Ministerien und Verwaltungen können ebenfalls Projekte einreichen.", "Aktualiséierung: Ministèren kënnen och Projeten areechen."))

apply("cgdis", {
 39: {"en": "Thousands of volunteer firefighters. About nine in ten firefighters are volunteers.",
      "fr": "Des milliers de pompiers volontaires. Environ neuf pompiers sur dix sont des volontaires.",
      "de": "Tausende freiwillige Feuerwehrleute. Etwa neun von zehn Feuerwehrleuten sind Freiwillige.",
      "lb": "Dausende fräiwëlleg Pompjeeën. Ongeféier néng vun zéng Pompjeeë sinn Fräiwëlleger."},
 40: {"en": "Nine in ten! So most of the people who rush to help you are volunteers.",
      "fr": "Neuf sur dix ! Donc la plupart des personnes qui se précipitent pour vous secourir sont des bénévoles.",
      "de": "Neun von zehn! Die meisten Menschen, die zu Ihrer Hilfe eilen, sind also Freiwillige.",
      "lb": "Néng vun zéng! Also déi meeschte Leit, déi sech beeilen, fir Iech ze hëllefen, sinn Fräiwëlleger."},
}, note("Update: CGDIS annual report 2025 (presented 16 July 2026): 6,890 volunteer and 694 professional firefighters; 75,814 interventions; 258,036 emergency calls — the script now says 'about nine in ten firefighters are volunteers'.",
        "Mise à jour : rapport annuel 2025 du CGDIS : 6 890 pompiers volontaires et 694 professionnels.", "Aktualisierung: CGDIS-Jahresbericht 2025: 6 890 freiwillige und 694 Berufsfeuerwehrleute.", "Aktualiséierung: CGDIS-Joresbericht 2025: 6 890 Fräiwëlleger, 694 Beruffspompjeeën."))

apply("statec", {}, note("Checked: motto 'Nous comptons car vous comptez !', simulators (inflation, indexation), index tranche of 1 June 2026, index system unchanged by the June 2026 tripartite agreement (statistiques.public.lu, gouvernement.lu).",
        "Vérifié : devise, simulateurs, tranche indiciaire du 1er juin 2026, système d'indexation inchangé.", "Geprüft: Motto, Simulatoren, Indextranche vom 1. Juni 2026, Indexsystem unverändert.", "Iwwerpréift: Motto, Simulateuren, Index."))

apply("environnement", {
 6: {"en": "It is the environment portal of Luxembourg. Its friendly name is emwelt dot lu... which takes you to environnement dot public dot lu.",
     "fr": "C'est le portail de l'environnement du Luxembourg. Son nom familier est emwelt point lu... qui vous mène à environnement point public point lu.",
     "de": "Es ist das Umweltportal Luxemburgs. Sein vertrauter Name ist emwelt Punkt lu... das Sie zu environnement Punkt public Punkt lu führt.",
     "lb": "Et ass d'Ëmweltportal vu Lëtzebuerg. Säi vertraute Numm ass emwelt Punkt lu... deen Iech op environnement Punkt public Punkt lu féiert."},
 18: {"en": "And there is a real-time air-quality service, with the app Meng Loft, so you can see live measurements.",
      "fr": "Et il existe un service de qualité de l'air en temps réel, avec l'application Meng Loft, qui vous permet de voir les mesures en direct.",
      "de": "Und es gibt einen Echtzeit-Dienst zur Luftqualität, mit der App Meng Loft, sodass Sie die Messungen live sehen können.",
      "lb": "An et gëtt e Service fir d'Loftqualitéit an Echtzäit, mat der App Meng Loft, sou datt Dir d'Moossunge live gesi kënnt."},
 20: {"en": "Luxembourg has a national energy and climate plan, and a new strategy to adapt to a warming world, adopted in 2026.",
      "fr": "Le Luxembourg dispose d'un plan national énergie et climat, et d'une nouvelle stratégie pour s'adapter à un monde qui se réchauffe, adoptée en 2026.",
      "de": "Luxemburg hat einen nationalen Energie- und Klimaplan und eine neue Strategie, um sich an eine wärmer werdende Welt anzupassen, die 2026 verabschiedet wurde.",
      "lb": "Lëtzebuerg huet en nationalen Energie- a Klimaplang, an eng nei Strategie, fir sech un eng méi waarm Welt unzepassen, déi 2026 ugeholl gouf."},
 23: {"en": "There's even an app, Mäin Offall, to help you know what goes in which bin.",
      "fr": "Il existe même une application, Mäin Offall, pour vous aider à savoir ce qui va dans quelle poubelle.",
      "de": "Es gibt sogar eine App, Mäin Offall, die Ihnen hilft zu wissen, was in welche Tonne gehört.",
      "lb": "Et gëtt souguer eng App, Mäin Offall, déi Iech hëlleft ze wëssen, wat an déi wéi eng Tonn gehéiert."},
 42: {"en": "The portal also shares the country's latest plans... for example a new national plan to restore nature.",
      "fr": "Le portail présente aussi les derniers plans du pays... par exemple un nouveau plan national pour restaurer la nature.",
      "de": "Das Portal stellt auch die neuesten Pläne des Landes vor... zum Beispiel einen neuen nationalen Plan zur Wiederherstellung der Natur.",
      "lb": "D'Portal stellt och déi neiste Pläng vum Land vir... zum Beispill en neien nationale Plang fir d'Natur ze restauréieren."},
}, note("Update: emwelt.lu redirects to environnement.public.lu; apps 'Meng Loft' (air) and 'Mäin Offall' (waste); national climate adaptation strategy 2025–2035 adopted 22 April 2026; national nature restoration plan (Sept 2026); no 'calls for projects for nature in towns' found on the portal.",
        "Mise à jour : emwelt.lu mène à environnement.public.lu ; applis Meng Loft et Mäin Offall ; stratégie d'adaptation 2025–2035 (22.04.2026) ; plan national de restauration de la nature (sept. 2026).",
        "Aktualisierung: emwelt.lu führt zu environnement.public.lu; Apps Meng Loft und Mäin Offall; Anpassungsstrategie 2025–2035 (22.04.2026); nationaler Wiederherstellungsplan (Sept. 2026).",
        "Aktualiséierung: emwelt.lu → environnement.public.lu; Meng Loft, Mäin Offall; Adaptatiounsstrategie 2026; Restauratiounsplang."))
