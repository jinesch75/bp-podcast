#!/usr/bin/env python3
"""Fact-check Klima-Agence (9 Nov 2026): Klimabonus renewed for 2026-2030 (Wunnen until 2030, Mobilitéit until
30.06.2030), PV/batteries + subsidy deducted from invoice by participating companies; full ministry names."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from lib_factcheck import apply
C = {
11: {"en": "Several ministries stand behind it... the Ministry of the Economy, the Ministry of the Environment, Climate and Biodiversity, and the Ministry of Housing and Spatial Planning.",
     "fr": "Plusieurs ministères se trouvent derrière elle... le Ministère de l'Économie, le Ministère de l'Environnement, du Climat et de la Biodiversité, et le Ministère du Logement et de l'Aménagement du territoire.",
     "lb": "Verschidde Ministèren stinn dohannert... de Wirtschaftsministère, de Ministère fir Ëmwelt, Klima a Biodiversitéit, an de Ministère fir Wunnengsbau a Landesplanung."},
49: {"en": "The Klimabonus supports things like energy-efficient renovation, renewable heating such as heat pumps, solar panels and batteries, electric vehicles, and charging stations. And it was renewed in 2026, for most projects until 2030.",
     "fr": "Le Klimabonus soutient des choses comme la rénovation énergétique, le chauffage renouvelable comme les pompes à chaleur, les panneaux solaires et les batteries, les véhicules électriques, et les bornes de recharge. Et il a été renouvelé en 2026, pour la plupart des projets jusqu'en 2030.",
     "de": "Der Klimabonus unterstützt Dinge wie energieeffiziente Renovierung, erneuerbares Heizen wie Wärmepumpen, Solarmodule und Batterien, Elektrofahrzeuge und Ladestationen. Und er wurde 2026 erneuert, für die meisten Projekte bis 2030.",
     "lb": "De Klimabonus ënnerstëtzt Saache wéi energieeffizient Renovatioun, erneierbar Heizung wéi Wäermepompelen, Solarpanneauen a Batterien, elektresch Gefierer, a Luetstatiounen. An en ass 2026 erneiert ginn, fir déi meescht Projete bis 2030."},
50: {"en": "So it really covers most of the projects we just talked about. And for solar panels, some companies can even take the subsidy straight off your bill.",
     "fr": "Donc il couvre vraiment la plupart des projets dont nous venons de parler. Et pour les panneaux solaires, certaines entreprises peuvent même déduire la subvention directement de votre facture.",
     "de": "Er deckt also wirklich die meisten der Projekte ab, über die wir gerade gesprochen haben. Und bei Solarmodulen können manche Firmen den Zuschuss sogar direkt von der Rechnung abziehen.",
     "lb": "Et deckt also wierklech déi meescht vun de Projeten, iwwer déi mir just geschwat hunn. A bei Solarpanneauen kënnen e puer Firmen de Subsid souguer direkt vun der Rechnung ofzéien."},
}
N = {"en": "Update: Klimabonus Wunnen renewed for 2026–2030 (some works until 2035), Klimabonus Mobilitéit extended until 30 June 2030; PV pre-financing where the participating company deducts the subsidy from the invoice (klima-agence.lu, gouvernement.lu 31.12.2025 and 20.03.2026). Fact-checked 9 November 2026.",
     "fr": "Mise à jour : Klimabonus Wunnen renouvelé pour 2026–2030, Klimabonus Mobilitéit prolongé jusqu'au 30 juin 2030 ; préfinancement photovoltaïque avec subvention déduite de la facture (klima-agence.lu, gouvernement.lu). Vérifié le 9 novembre 2026.",
     "de": "Aktualisierung: Klimabonus Wunnen für 2026–2030 erneuert, Klimabonus Mobilitéit bis 30. Juni 2030 verlängert; PV-Vorfinanzierung mit Abzug des Zuschusses von der Rechnung (klima-agence.lu, gouvernement.lu). Geprüft am 9. November 2026.",
     "lb": "Aktualiséierung: Klimabonus Wunnen 2026–2030, Klimabonus Mobilitéit bis den 30. Juni 2030; PV-Virfinanzéierung (klima-agence.lu). Iwwerpréift den 9. November 2026."}
apply("klima", C, N)
