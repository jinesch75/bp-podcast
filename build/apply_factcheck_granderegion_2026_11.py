# Fact-check episode 12 House of the Greater Region (10 Nov 2026). Usage: python3 build/apply_factcheck_granderegion_2026_11.py [--dry]
# Each edit = (turn, lang, old substring, new substring); the turn's full new text is built from the current script,
# then written with lib_factcheck.apply (idempotent: an edit whose new text is already present is skipped).
import sys, os, re; sys.path.insert(0, os.path.dirname(__file__)); from lib_factcheck import apply, SFX, TURN
KEY = "granderegion"
E = {}  # turn -> lang -> [(old, new)]
def e(turn, lang, old, new): E.setdefault(turn, {}).setdefault(lang, []).append((old, new))

# 1. population (turns 8, 9)
e(8, "en", "over eleven point eight million people", "almost twelve million people")
e(8, "fr", "de plus de onze virgule huit millions de personnes", "de près de douze millions de personnes")
e(8, "de", "über elf Komma acht Millionen Menschen", "fast zwölf Millionen Menschen")
e(8, "lb", "an iwwer eelef Komma aacht Milliounen Leit", "a bal zwielef Milliounen Leit")
e(9, "en", "Eleven point eight million.", "Almost twelve million.")
e(9, "fr", "Onze virgule huit millions.", "Près de douze millions.")
e(9, "de", "Elf Komma acht Millionen.", "Fast zwölf Millionen.")
e(9, "lb", "Eelef Komma aacht Milliounen.", "Bal zwielef Milliounen.")
# 2. commuters (turn 12)
e(12, "en", "about half of those commuters live in France, and around three-quarters of all of them come to work in Luxembourg.", "more than half of them live in France, and more than four out of five come to work in Luxembourg.")
e(12, "fr", "environ la moitié de ces frontaliers vivent en France, et à peu près les trois quarts d'entre eux viennent travailler au Luxembourg.", "plus de la moitié d'entre eux vivent en France, et plus de quatre sur cinq viennent travailler au Luxembourg.")
e(12, "de", "etwa die Hälfte dieser Grenzgänger lebt in Frankreich, und ungefähr drei Viertel von ihnen kommen zum Arbeiten nach Luxemburg.", "mehr als die Hälfte von ihnen lebt in Frankreich, und mehr als vier von fünf kommen zum Arbeiten nach Luxemburg.")
e(12, "lb", "ongeféier d'Halschent vun dëse Frontalieren wunnt a Frankräich, a ronn dräi Véierel vun hinnen all kommen zu Lëtzebuerg schaffen.", "méi wéi d'Halschent vun hinnen wunnt a Frankräich, a méi wéi véier vu fënnef kommen zu Lëtzebuerg schaffen.")
# 3. the House: in Esch since 2015, shared office in Luxembourg City since 1999 (turns 18, 19, 20, 64, 84)
e(18, "en", "It opened in twenty fifteen.", "It's been in Esch since twenty fifteen. Before that, from nineteen ninety-nine, it was a smaller shared office in Luxembourg City.")
e(18, "fr", "Elle a ouvert en deux mille quinze.", "Elle est à Esch depuis deux mille quinze. Avant cela, depuis mille neuf cent quatre-vingt-dix-neuf, c'était un bureau commun plus petit, à Luxembourg-Ville.")
e(18, "de", "Es wurde zweitausendfünfzehn eröffnet.", "Seit zweitausendfünfzehn ist es in Esch. Davor, seit neunzehnhundertneunundneunzig, war es ein kleineres gemeinsames Büro in Luxemburg-Stadt.")
e(18, "lb", "Et huet am Joer zweedausendfofzéng opgemaach.", "Zënter zweedausendfofzéng ass et zu Esch. Virdrun, zënter nonzénghonnertnénganonzeg, war et e méi klengt gemeinsamt Büro an der Stad Lëtzebuerg.")
e(19, "en", "So it's quite young — about ten years old.", "So the idea is older than the building.")
e(19, "fr", "Donc elle est assez jeune — environ dix ans.", "Donc l'idée est plus ancienne que le bâtiment.")
e(19, "de", "Es ist also ziemlich jung — etwa zehn Jahre alt.", "Die Idee ist also älter als das Gebäude.")
e(19, "lb", "Also ass et nach zimmlech jonk — ongeféier zéng Joer al.", "D'Iddi ass also méi al wéi d'Gebai.")
e(20, "en", "Young, yes. It was created", "Exactly. It was created")
e(20, "fr", "Jeune, oui. Elle a été créée", "Exactement. Elle a été créée")
e(20, "de", "Jung, ja. Es wurde", "Genau. Es wurde")
e(20, "lb", "Jonk, jo. Et gouf", "Genee. Et gouf")
e(64, "en", "it got its physical home", "it got its bigger home")
e(64, "fr", "il a obtenu son foyer physique", "il a obtenu un foyer plus grand")
e(64, "de", "bekam es sein physisches Zuhause", "bekam es sein größeres Zuhause")
e(64, "lb", "huet et säi physescht Doheem kritt", "huet et säi gréissert Doheem kritt")
e(84, "en", "in Esch-sur-Alzette, which opened in twenty fifteen and hosts", "in Esch-sur-Alzette since twenty fifteen, which hosts")
e(84, "fr", "à Esch-sur-Alzette, qui a ouvert en deux mille quinze et accueille", "installée à Esch-sur-Alzette depuis deux mille quinze, qui accueille")
e(84, "de", "in Esch-sur-Alzette, das zweitausendfünfzehn eröffnet wurde und das Gipfelsekretariat", "das seit zweitausendfünfzehn in Esch-sur-Alzette ist und das Gipfelsekretariat")
e(84, "lb", "zu Esch-sur-Alzette, dat am Joer zweedausendfofzéng opgemaach huet an", "dat zënter zweedausendfofzéng zu Esch-sur-Alzette ass an")
# 4. who sits at the Summit (turns 26, 27)
e(26, "en", "the Prime Minister of Luxembourg, the Minister-Presidents of the German regions, of Wallonia, the leaders from the French side", "a member of the Luxembourg government, the Minister-Presidents of the German regions and of Wallonia, representatives from the French side")
e(26, "fr", "le Premier ministre du Luxembourg, les Ministres-présidents des régions allemandes, de la Wallonie, les dirigeants du côté français", "un membre du gouvernement luxembourgeois, les Ministres-présidents des régions allemandes et de la Wallonie, des représentants du côté français")
e(26, "de", "der Premierminister von Luxemburg, die Ministerpräsidenten der deutschen Regionen, der Wallonie, die Spitzen von der französischen Seite", "ein Mitglied der luxemburgischen Regierung, die Ministerpräsidenten der deutschen Regionen und der Wallonie, Vertreter von der französischen Seite")
e(26, "lb", "de Premierminister vu Lëtzebuerg, d'Ministerpresidente vun den däitsche Regiounen, vun der Wallonie, d'Cheffe vun der franséischer Säit", "e Member vun der Lëtzebuerger Regierung, d'Ministerpresidente vun den däitsche Regiounen a vun der Wallonie, Vertrieder vun der franséischer Säit")
e(27, "en", "So the actual heads of government, around one table.", "So the top political leaders, around one table.")
e(27, "fr", "Donc les véritables chefs de gouvernement, autour d'une même table.", "Donc les plus hauts responsables politiques, autour d'une même table.")
e(27, "de", "Also die tatsächlichen Regierungschefs, an einem Tisch.", "Also die obersten politischen Spitzen, an einem Tisch.")
e(27, "lb", "Also déi richteg Regierungschefen, ronderëm ee Dësch.", "Also déi héchst politesch Cheffen, ronderëm ee Dësch.")
# 5. emergency teams across the border (turn 50)
e(50, "en", "If you have an accident, the closest ambulance comes — not the closest ambulance in your own country.", "And in some places, if you have an accident, the emergency team from across the border can come, if it's closer.")
e(50, "fr", "Si tu as un accident, c'est l'ambulance la plus proche qui vient — pas l'ambulance la plus proche dans ton propre pays.", "Et à certains endroits, si tu as un accident, l'équipe d'urgence de l'autre côté de la frontière peut venir, si elle est plus proche.")
e(50, "de", "Wenn du einen Unfall hast, kommt der nächste Krankenwagen — nicht der nächste Krankenwagen in deinem eigenen Land.", "Und an manchen Orten kann bei einem Unfall das Rettungsteam von der anderen Seite der Grenze kommen, wenn es näher ist.")
e(50, "lb", "Wann s du en Accident hues, kënnt déi noost Ambulanz — net déi noost Ambulanz an dengem eegene Land.", "An op verschiddene Plazen, wann s du en Accident hues, kann d'Noutfallequipe vun der anerer Säit vun der Grenz kommen, wann se méi no ass.")
# 6. Biergerpakt on granderegion.net (turn 82)
e(82, "en", "in Esch-sur-Alzette.", "in Esch-sur-Alzette. And in the Discover section, you'll even find the Biergerpakt.")
e(82, "fr", "à Esch-sur-Alzette.", "à Esch-sur-Alzette. Et dans la rubrique Découvrir, vous trouverez même le Biergerpakt.")
e(82, "de", "in Esch-sur-Alzette.", "in Esch-sur-Alzette. Und in der Rubrik Entdecken findest du sogar den Biergerpakt.")
e(82, "lb", "zu Esch-sur-Alzette.", "zu Esch-sur-Alzette. An an der Rubrik Entdecken fënns du souguer de Biergerpakt.")

NOTES = {
 "en": "Fact-checked 10 November 2026: 11.8 million inhabitants on 1 January 2023 (spoken as 'almost twelve million'); 276,360 cross-border workers in 2024 (IBA-OIE), about 230,000 of them working in Luxembourg (STATEC, Q4 2024); the House began in 1999 as a shared office in Luxembourg City and moved to Esch-sur-Alzette on 17 June 2015; Luxembourg is currently represented at the Summit by a member of the government; cross-border emergency medical aid in some border areas (Franco-Belgian convention 2007); the Biergerpakt is presented on granderegion.net (Discover).",
 "fr": "Vérifié le 10 novembre 2026 : 11,8 millions d'habitants au 1er janvier 2023 (dit « près de douze millions ») ; 276 360 frontaliers en 2024 (IBA-OIE), dont environ 230 000 travaillent au Luxembourg (STATEC, 4e trimestre 2024) ; la Maison était depuis 1999 un bureau commun à Luxembourg-Ville et a déménagé à Esch-sur-Alzette le 17 juin 2015 ; le Luxembourg est actuellement représenté au Sommet par un membre du gouvernement ; aide médicale urgente transfrontalière dans certaines zones (convention franco-belge de 2007) ; le Biergerpakt est présenté sur granderegion.net (Découvrir).",
 "de": "Geprüft am 10. November 2026: 11,8 Millionen Einwohner am 1. Januar 2023 (gesprochen „fast zwölf Millionen“); 276.360 Grenzgänger im Jahr 2024 (IBA-OIE), davon rund 230.000 in Luxemburg beschäftigt (STATEC, 4. Quartal 2024); das Haus war seit 1999 ein gemeinsames Büro in Luxemburg-Stadt und zog am 17. Juni 2015 nach Esch-sur-Alzette; Luxemburg ist beim Gipfel derzeit durch ein Regierungsmitglied vertreten; grenzüberschreitende Notfallhilfe in manchen Grenzgebieten (französisch-belgisches Abkommen 2007); der Biergerpakt wird auf granderegion.net vorgestellt (Entdecken).",
 "lb": "Iwwerpréift den 10. November 2026: 11,8 Milliounen Awunner den 1. Januar 2023 (gesot „bal zwielef Milliounen“); 276.360 Frontalieren am Joer 2024 (IBA-OIE), dovun ronn 230.000 zu Lëtzebuerg (STATEC, 4. Trimester 2024); d'Haus war zënter 1999 e gemeinsamt Büro an der Stad an ass de 17. Juni 2015 op Esch-sur-Alzette geplënnert; Lëtzebuerg ass beim Sommet de Moment duerch e Member vun der Regierung vertrueden; grenziwwerschreidend Noutfallhëllef a verschiddene Grenzgebidder (franséisch-belsch Konventioun 2007); de Biergerpakt gëtt op granderegion.net virgestallt (Entdecken).",
}

CHANGES = {}
for lang, sfx in SFX.items():
    turns = [m.group(2) for m in TURN.finditer(open(f"podcast_script_{KEY}{sfx}.md", encoding="utf-8").read())]
    for t, by in E.items():
        txt = turns[t]
        for old, new in by.get(lang, []):
            if new in txt: continue
            assert txt.count(old) == 1, (lang, t, old)
            txt = txt.replace(old, new)
        CHANGES.setdefault(t, {})[lang] = txt
apply(KEY, CHANGES, NOTES)
