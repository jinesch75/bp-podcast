#!/usr/bin/env python3
"""Fact-check episodes 27-31 (9 Nov 2026): syvicol, research, agriculture, amenagement, aaa. EN/FR/DE/LB."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from lib_factcheck import apply
DATE = {"en": "Fact-checked 9 November 2026.", "fr": "Vérifié le 9 novembre 2026.", "de": "Geprüft am 9. November 2026.", "lb": "Iwwerpréift den 9. November 2026."}
def note(en, fr, de, lb): return {"en": en + " " + DATE["en"], "fr": fr + " " + DATE["fr"], "de": de + " " + DATE["de"], "lb": lb + " " + DATE["lb"]}

apply("syvicol", {
 11: {"en": "It is the organisation that brings together all of Luxembourg's communes into one common voice. It was founded in 1986.",
      "fr": "C'est l'organisation qui réunit toutes les communes du Luxembourg en une seule voix commune. Elle a été fondée en 1986.",
      "de": "Es ist die Organisation, die alle Gemeinden Luxemburgs zu einer gemeinsamen Stimme zusammenführt. Sie wurde 1986 gegründet.",
      "lb": "Et ass d'Organisatioun, déi all d'Gemenge vu Lëtzebuerg zu enger gemeinsamer Stëmm zesummebréngt. Si gouf 1986 gegrënnt."},
}, note("Checked: 100 communes (since the 2023 mergers); SYVICOL founded 1986 as a syndicate of communes; opinions on draft laws (e.g. bill 8723, May 2026).",
        "Vérifié : 100 communes ; SYVICOL fondé en 1986.", "Geprüft: 100 Gemeinden; SYVICOL 1986 gegründet.", "Iwwerpréift: 100 Gemengen; SYVICOL 1986."))

apply("research", {}, note("Checked: six members (University of Luxembourg, LIST, LIH, LISER, FNR, Luxinnovation), supported by the Ministry of Higher Education and Research; Belval Innovation Campus; career and PhD pages (researchluxembourg.org).",
        "Vérifié : six membres, ministère de l'Enseignement supérieur et de la Recherche (researchluxembourg.org).", "Geprüft: sechs Mitglieder, Hochschulministerium (researchluxembourg.org).", "Iwwerpréift: sechs Memberen."))

apply("agriculture", {
 20: {"en": "And there is an administration that looks after animal health and welfare, and the safety of our food. It is called ALVA, and it was created in 2022.",
      "fr": "Et il y a une administration qui veille sur la santé et le bien-être des animaux, et sur la sécurité de notre alimentation. Elle s'appelle l'ALVA, et elle a été créée en 2022.",
      "de": "Und es gibt eine Verwaltung, die über die Gesundheit und das Wohl der Tiere wacht, und über die Sicherheit unserer Lebensmittel. Sie heißt ALVA und wurde 2022 gegründet.",
      "lb": "An et gëtt eng Verwaltung, déi iwwer d'Gesondheet an d'Wuelbefannen vun den Déieren waacht, an iwwer d'Sécherheet vun eisem Iessen. Si heescht ALVA, a si gouf 2022 gegrënnt."},
 24: {"en": "Luxembourg has a plan, called PAN-Bio, to grow the share of organic farming in the country. The newest one runs from 2026 to 2030.",
      "fr": "Le Luxembourg a un plan, appelé PAN-Bio, pour augmenter la part de l'agriculture biologique dans le pays. Le plus récent va de 2026 à 2030.",
      "de": "Luxemburg hat einen Plan, genannt PAN-Bio, um den Anteil der biologischen Landwirtschaft im Land zu erhöhen. Der neueste läuft von 2026 bis 2030.",
      "lb": "Lëtzebuerg huet e Plang, genannt PAN-Bio, fir den Undeel vun der Bio-Landwirtschaft am Land ze erhéijen. Dee neiste leeft vun 2026 bis 2030."},
 56: {"en": "Second... specialised bodies support it... ASTA for technical services, the wine institute in Remich, and ALVA for animal welfare and food safety.",
      "fr": "Ensuite... des organismes spécialisés le soutiennent... l'ASTA pour les services techniques, l'institut du vin à Remich, et l'ALVA pour le bien-être animal et la sécurité alimentaire.",
      "de": "Zweitens... spezialisierte Stellen unterstützen es... die ASTA für die technischen Dienste, das Weininstitut in Remich, und die ALVA für das Tierwohl und die Lebensmittelsicherheit.",
      "lb": "Zweetens... spezialiséiert Stellen ënnerstëtzen et... d'ASTA fir déi technesch Déngschter, de Wäininstitut zu Remich, an d'ALVA fir den Déiereschutz an d'Liewensmëttelsécherheet."},
}, note("Update: Administration luxembourgeoise vétérinaire et alimentaire (ALVA), law of 8 September 2022; PAN-Bio 2030 (2026–2030), presented December 2025.",
        "Mise à jour : ALVA (loi du 8 septembre 2022) ; PAN-Bio 2030 (2026–2030).", "Aktualisierung: ALVA (Gesetz vom 8. September 2022); PAN-Bio 2030 (2026–2030).", "Aktualiséierung: ALVA (2022); PAN-Bio 2030."))

apply("amenagement", {
 17: {"en": "The first is the master programme, a big strategic vision for how the whole country should develop. The current one was adopted in 2023, and looks ahead to 2035.",
      "fr": "Le premier est le programme directeur, une grande vision stratégique de la façon dont l'ensemble du pays devrait se développer. L'actuel a été adopté en 2023, et regarde jusqu'en 2035.",
      "de": "Das erste ist das Leitprogramm, eine große strategische Vision dafür, wie sich das ganze Land entwickeln soll. Das aktuelle wurde 2023 verabschiedet und blickt bis 2035.",
      "lb": "Dat éischt ass de Leitprogramm, eng grouss strategesch Visioun dervun, wéi d'ganzt Land sech entwéckele soll. Den aktuellen ass 2023 ugeholl ginn, a kuckt bis 2035."},
}, note("Update: Programme directeur d'aménagement du territoire (PDAT) approved by the Government in Council on 21 June 2023, orientations to 2035; four sectoral master plans in force since 1 March 2021.",
        "Mise à jour : PDAT approuvé le 21 juin 2023, horizon 2035 ; plans directeurs sectoriels en vigueur depuis le 1er mars 2021.", "Aktualisierung: PDAT vom 21. Juni 2023, Horizont 2035; sektorielle Leitpläne seit 1. März 2021.", "Aktualiséierung: PDAT 2023, bis 2035."))

apply("aaa", {
 8: {"en": "It is the body that runs Luxembourg's insurance against accidents at work, and occupational diseases. It was created back in 1902.",
     "fr": "C'est l'organisme qui gère l'assurance du Luxembourg contre les accidents du travail et les maladies professionnelles. Elle a été créée dès 1902.",
     "de": "Sie ist die Einrichtung, die Luxemburgs Versicherung gegen Arbeitsunfälle und Berufskrankheiten verwaltet. Sie wurde schon 1902 gegründet.",
     "lb": "Et ass déi Instanz, déi Lëtzebuerg seng Versécherung géint Aarbechtsaccidenter a Beruffskrankheeten verwalt. Si gouf schonn 1902 gegrënnt."},
 36: {"en": "And this can now be done electronically, through MyGuichet, which we covered in an earlier episode... both for accidents at work and for school accidents.",
      "fr": "Et cela peut désormais se faire par voie électronique, via MyGuichet, dont nous avons parlé dans un épisode précédent... aussi bien pour les accidents du travail que pour les accidents scolaires.",
      "de": "Und das kann jetzt elektronisch erledigt werden, über MyGuichet, worüber wir in einer früheren Folge gesprochen haben... sowohl für Arbeitsunfälle als auch für Schulunfälle.",
      "lb": "An dat kann elo elektronesch gemaach ginn, iwwer MyGuichet, doriwwer hu mir an enger fréierer Episod geschwat... souwuel fir Aarbechtsaccidenter wéi och fir Schoulaccidenter."},
 38: {"en": "It's also worth knowing the AAA is there to answer questions, with a contact service and a counter... and you can even book an appointment online.",
      "fr": "Il est aussi bon de savoir que l'AAA est là pour répondre aux questions, avec un service de contact et un guichet... et on peut même prendre rendez-vous en ligne.",
      "de": "Es ist auch gut zu wissen, dass die AAA da ist, um Fragen zu beantworten, mit einem Kontaktservice und einem Schalter... und man kann sogar online einen Termin buchen.",
      "lb": "Et ass och gutt ze wëssen, datt d'AAA do ass, fir Froen ze beäntweren, mat engem Kontaktservice an engem Schalter... an et ka souguer online e Rendez-vous huelen."},
}, note("Update: AAA created in 1902; electronic declaration of work/commuting and school accidents via MyGuichet.lu since 30 September 2024; online appointments via MyGuichet.lu (aaa.public.lu, guichet.public.lu).",
        "Mise à jour : AAA créée en 1902 ; déclaration électronique via MyGuichet.lu depuis le 30 septembre 2024 ; rendez-vous en ligne.", "Aktualisierung: AAA 1902 gegründet; elektronische Unfallmeldung über MyGuichet.lu seit 30. September 2024; Online-Termine.", "Aktualiséierung: AAA 1902; MyGuichet.lu zënter 2024."))
