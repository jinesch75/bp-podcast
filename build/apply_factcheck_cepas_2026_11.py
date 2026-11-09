#!/usr/bin/env python3
"""Fact-check CePAS (9 Nov 2026): 'more than sixty years'; financial help made concrete (SMFR low-income subsidy
via the school's SePAS, free Kulturpass) + planned complément vie chère (bill 8716) hedged."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from lib_factcheck import apply
C = {
40: {"en": "CePAS also handles financial help for pupils from low-income families... a yearly subsidy for school materials and activities, which you ask for through the school's psycho-social service. The government plans to fold it into a new single cost-of-living help from 2027, so ask at the school what applies.",
     "fr": "Le CePAS gère aussi une aide financière pour les élèves de familles à faible revenu... une subvention annuelle pour le matériel et les activités scolaires, que l'on demande via le service psycho-social de l'école. Le gouvernement prévoit de l'intégrer dans une nouvelle aide unique contre la vie chère à partir de 2027, alors renseignez-vous à l'école.",
     "de": "CePAS kümmert sich auch um eine finanzielle Hilfe für Schüler aus Familien mit geringem Einkommen... einen jährlichen Zuschuss für Schulmaterial und Aktivitäten, den man über den psycho-sozialen Dienst der Schule beantragt. Die Regierung plant, ihn ab 2027 in eine neue, einzige Teuerungshilfe einzugliedern, fragen Sie also an der Schule nach, was gilt.",
     "lb": "De CePAS këmmert sech och ëm eng finanziell Hëllef fir Schüler aus Famillje mat engem klengen Akommes... e jäerleche Subsid fir Schoulmaterial an Aktivitéiten, deen een iwwer de psycho-soziale Service vun der Schoul freet. D'Regierung plangt, en ab 2027 an eng nei, eenzeg Hëllef géint d'Liewensdeierung ze integréieren, also frot an der Schoul no, wat gëllt."},
55: {"en": "First... it is a psycho-social and school support centre, helping young people's wellbeing at school for more than sixty years.",
     "fr": "Premièrement... c'est un centre de soutien psycho-social et scolaire, qui aide au bien-être des jeunes à l'école depuis plus de soixante ans.",
     "de": "Erstens... es ist ein psycho-soziales und schulisches Unterstützungszentrum, das seit mehr als sechzig Jahren dem Wohlergehen junger Menschen in der Schule dient.",
     "lb": "Éischtens... et ass e psycho-sozialt a schoulescht Ënnerstëtzungszentrum, dat zanter méi wéi sechzeg Joer dem Wuelbefanne vu jonke Leit an der Schoul déngt."},
}
N = {"en": "Update: CePAS grants the low-income household subsidy (SMFR) and the school-retention subsidy through the lycées' SePAS (cepas.public.lu); bill 8716 (complément vie chère, still in committee, planned 1 January 2027) would replace the SMFR. Fact-checked 9 November 2026.",
     "fr": "Mise à jour : le CePAS octroie la subvention pour ménages à faible revenu (SMFR) via les SePAS ; le projet de loi 8716 (complément vie chère, prévu au 1er janvier 2027, encore en commission) la remplacerait. Vérifié le 9 novembre 2026.",
     "de": "Aktualisierung: CePAS gewährt den Zuschuss für Haushalte mit geringem Einkommen (SMFR) über die SePAS; Gesetzentwurf 8716 (complément vie chère, geplant ab 1. Januar 2027, noch im Ausschuss) würde ihn ersetzen. Geprüft am 9. November 2026.",
     "lb": "Aktualiséierung: SMFR iwwer d'SePAS; Gesetzesprojet 8716 (complément vie chère) géif se ersetzen. Iwwerpréift den 9. November 2026."}
apply("cepas", C, N)
