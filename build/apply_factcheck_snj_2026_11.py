#!/usr/bin/env python3
"""Fact-check SNJ (9 Nov 2026): 'more than sixty years'; youth monitoring since 2022 with the OEJQS -> national
youth report every five years feeds the Youth Pact 2026-2030 (published by the SNJ); sixth youth centre in Esch."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from lib_factcheck import apply
C = {
8: {"en": "It is a public service of the State, created back in 1964. So it has been supporting young people for more than sixty years.",
    "fr": "C'est un service public de l'État, créé en 1964. Il soutient donc les jeunes depuis plus de soixante ans.",
    "de": "Es ist ein öffentlicher Dienst des Staates, gegründet im Jahr 1964. Er unterstützt junge Menschen also seit mehr als sechzig Jahren.",
    "lb": "Et ass en ëffentlechen Déngscht vum Staat, gegrënnt am Joer 1964. Hie stëtzt jonk Leit also zanter méi wéi sechzeg Joer."},
52: {"en": "The SNJ listens to young people, through surveys and discussion groups.",
     "fr": "Le SNJ écoute les jeunes, à travers des enquêtes et des groupes de discussion.",
     "de": "Der SNJ hört jungen Menschen zu, durch Umfragen und Gesprächsgruppen.",
     "lb": "De SNJ lauschtert de jonke Leit no, duerch Ëmfroen an Diskussiounsgruppen."},
53: {"en": "And every five years, there is a big national report on youth. It is the basis for the national plan for young people, the Youth Pact. The newest one runs from 2026 to 2030, and the SNJ helped to prepare it.",
     "fr": "Et tous les cinq ans, il y a un grand rapport national sur la jeunesse. C'est la base du plan national pour les jeunes, le Pacte pour la jeunesse. Le plus récent va de 2026 à 2030, et le SNJ a aidé à le préparer.",
     "de": "Und alle fünf Jahre gibt es einen großen nationalen Jugendbericht. Er ist die Grundlage für den nationalen Plan für junge Menschen, den Jugendpakt. Der neueste läuft von 2026 bis 2030, und der SNJ hat geholfen, ihn vorzubereiten.",
     "lb": "An all fënnef Joer gëtt et e grousse nationale Rapport iwwer d'Jugend. En ass d'Basis fir den nationale Plang fir jonk Leit, de Jugendpakt. Dee neiste leeft vun 2026 bis 2030, an de SNJ huet gehollef, en virzebereeden."},
60: {"en": "The SNJ has five educational centres, with a new one coming in Esch-sur-Alzette, and local youth antennas across the country for individual support.",
     "fr": "Le SNJ a cinq centres éducatifs, avec un nouveau centre à Esch-sur-Alzette, et des antennes locales pour la jeunesse dans tout le pays pour un accompagnement individuel.",
     "de": "Der SNJ hat fünf Bildungszentren, dazu kommt ein neues in Esch-sur-Alzette, und lokale Jugendantennen im ganzen Land für die individuelle Begleitung.",
     "lb": "De SNJ huet fënnef Bildungszentren, dobäi kënnt en neit zu Esch-Uelzecht, a lokal Jugendantennen am ganze Land fir déi individuell Begleedung."},
}
N = {"en": "Update: national youth report every five years (2025 edition) and Youth Pact 2026–2030, published by the SNJ (gouvernement.lu, Oct 2026); monitoring of youth with the OEJQS since 2022; five youth centres (Marienthal, Hollenfels, Cinqfontaines, Forum Geesseknäppchen, Lultzhausen water-sports base) plus Esch-sur-Alzette from end 2026 (snj.public.lu). Fact-checked 9 November 2026.",
     "fr": "Mise à jour : rapport national sur la jeunesse tous les cinq ans et Pacte pour la jeunesse 2026–2030, édité par le SNJ ; cinq centres + Esch-sur-Alzette fin 2026 (snj.public.lu). Vérifié le 9 novembre 2026.",
     "de": "Aktualisierung: nationaler Jugendbericht alle fünf Jahre und Jugendpakt 2026–2030, herausgegeben vom SNJ; fünf Zentren + Esch-sur-Alzette ab Ende 2026 (snj.public.lu). Geprüft am 9. November 2026.",
     "lb": "Aktualiséierung: Jugendrapport all fënnef Joer a Jugendpakt 2026–2030; fënnef Zentren + Esch-Uelzecht (snj.public.lu). Iwwerpréift den 9. November 2026."}
apply("snj", C, N)
