# Fact-check episodes 32-36 (9 Nov 2026). Usage: python3 build/apply_factcheck_eps32-36_2026_11.py [--dry]
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from lib_factcheck import apply
DATE = {"en": "Fact-checked 9 November 2026.", "fr": "Vérifié le 9 novembre 2026.", "de": "Geprüft am 9. November 2026.", "lb": "Iwwerpréift den 9. November 2026."}
def note(en, fr, de, lb): return {"en": en + " " + DATE["en"], "fr": fr + " " + DATE["fr"], "de": de + " " + DATE["de"], "lb": lb + " " + DATE["lb"]}

apply("geoportail", {
 22: {"en": "Since late 2025, a new 3D viewer even lets you explore the country in 3D, with a virtual model of the buildings.",
      "fr": "Depuis fin 2025, une nouvelle visionneuse 3D vous permet même d'explorer le pays en 3D, avec un modèle virtuel des bâtiments.",
      "de": "Seit Ende 2025 können Sie mit einem neuen 3D-Viewer sogar das Land in 3D erkunden, mit einem virtuellen Modell der Gebäude.",
      "lb": "Zënter Enn 2025 kënnt Dir mat engem neien 3D-Viewer souguer d'Land an 3D entdecken, mat engem virtuelle Modell vun de Gebaier."},
}, note("New 3D viewer (3d.geoportail.lu) since December 2025.", "Nouvelle visionneuse 3D (3d.geoportail.lu) depuis décembre 2025.", "Neuer 3D-Viewer (3d.geoportail.lu) seit Dezember 2025.", "Neien 3D-Viewer (3d.geoportail.lu) zënter Dezember 2025."))

apply("govcert", {
 12: {"en": "The information systems of the State and of critical infrastructure operators. Since a new law in 2026, other companies and the communes turn to its sister team, CIRCL.",
      "fr": "Les systèmes d'information de l'État et des opérateurs d'infrastructures critiques. Depuis une nouvelle loi en 2026, les autres entreprises et les communes s'adressent à son équipe sœur, le CIRCL.",
      "de": "Die Informationssysteme des Staates und der Betreiber kritischer Infrastrukturen. Seit einem neuen Gesetz von 2026 wenden sich andere Unternehmen und die Gemeinden an das Schwesterteam CIRCL.",
      "lb": "D'Informatiounssystemer vum Staat a vun de Betreiber vu kritteschen Infrastrukturen. Zënter engem neie Gesetz vun 2026 wenden aner Betriber an d'Gemengen sech un d'Schwësterequipe CIRCL."},
}, note("Under the NIS2 law of 5 May 2026, GOVCERT.LU (part of the HCPN) is the CSIRT for the public sector and critical entities, and CIRCL for the private sector, communes and non-governmental entities; the ILR is the competent authority.",
        "Selon la loi NIS2 du 5 mai 2026, le GOVCERT.LU (rattaché au HCPN) est le CSIRT du secteur public et des entités critiques, et le CIRCL celui du secteur privé, des communes et des entités non gouvernementales ; l'ILR est l'autorité compétente.",
        "Nach dem NIS2-Gesetz vom 5. Mai 2026 ist GOVCERT.LU (beim HCPN) das CSIRT für den öffentlichen Sektor und kritische Einrichtungen, CIRCL für den Privatsektor, die Gemeinden und nichtstaatliche Einrichtungen; das ILR ist die zuständige Behörde.",
        "No dem NIS2-Gesetz vum 5. Mee 2026 ass GOVCERT.LU (beim HCPN) den CSIRT fir den ëffentleche Secteur an d'kritesch Entitéiten, an de CIRCL fir de private Secteur, d'Gemengen an déi net-staatlech Entitéiten; den ILR ass déi zoustänneg Autoritéit."))

apply("culture", {
 27: {"en": "It's part of a bigger effort to develop culture in Luxembourg, guided by a cultural development plan that runs until 2028.",
      "fr": "Il fait partie d'un effort plus large pour développer la culture au Luxembourg, guidé par un plan de développement culturel qui court jusqu'en 2028.",
      "de": "Es ist Teil eines größeren Bestrebens, die Kultur in Luxemburg zu entwickeln, geleitet von einem Kulturentwicklungsplan, der bis 2028 läuft.",
      "lb": "Et ass Deel vun engem méi grousse Beméien, fir d'Kultur zu Lëtzebuerg z'entwéckelen, op Basis vum Kulturentwécklungsplang, deen bis 2028 leeft."},
 28: {"en": "And a national action plan, launched in 2026, works to make culture more accessible, more inclusive, and more present in every region.",
      "fr": "Et un plan d'action national, lancé en 2026, vise à rendre la culture plus accessible, plus inclusive et plus présente dans chaque région.",
      "de": "Und ein nationaler Aktionsplan, 2026 gestartet, soll Kultur zugänglicher, inklusiver und in jeder Region präsenter machen.",
      "lb": "An en nationalen Aktiounsplang, deen 2026 lancéiert gouf, soll d'Kultur méi zougänglech, méi inklusiv a méi präsent an all Regioun maachen."},
 36: {"en": "And much of it is affordable, or even free, if you know where to look. With the Kulturpass, people on low incomes can enjoy many venues for free.",
      "fr": "Et une grande partie est abordable, voire gratuite, si vous savez où chercher. Avec le Kulturpass, les personnes à faibles revenus profitent gratuitement de nombreux lieux.",
      "de": "Und vieles davon ist erschwinglich oder sogar kostenlos, wenn Sie wissen, wo Sie suchen müssen. Mit dem Kulturpass können Menschen mit geringem Einkommen viele Häuser kostenlos besuchen.",
      "lb": "A vill dovun ass bezuelbar, oder souguer gratis, wann Dir wësst, wou Der musst kucken. Mam Kulturpass kënne Leit mat engem klengen Akommes vill Haiser gratis besichen."},
}, note("Cultural development plan (Kulturentwécklungsplang) 2018–2028; national action plan 'Access to culture' presented in April 2026 (2026–2030), including the Kulturpass; culture.lu portal announced May 2026.",
        "Plan de développement culturel (Kulturentwécklungsplang) 2018-2028 ; plan d'action national « Accès à la culture » présenté en avril 2026 (2026-2030), y compris le Kulturpass ; portail culture.lu annoncé en mai 2026.",
        "Kulturentwicklungsplan (Kulturentwécklungsplang) 2018–2028; nationaler Aktionsplan „Zugang zur Kultur“, vorgestellt im April 2026 (2026–2030), einschließlich Kulturpass; Portal culture.lu im Mai 2026 angekündigt.",
        "Kulturentwécklungsplang 2018–2028; nationalen Aktiounsplang „Zougang zur Kultur“, am Abrëll 2026 virgestallt (2026–2030), mam Kulturpass; Portal culture.lu am Mee 2026 ugekënnegt."))

apply("demenz", {
 26: {"en": "It can point you to more than a hundred services, support groups, and partners across the country.",
      "fr": "Il peut vous orienter vers plus d'une centaine de services, des groupes de soutien, et des partenaires partout dans le pays.",
      "de": "Es kann Sie zu mehr als hundert Diensten, Selbsthilfegruppen, und Partnern im ganzen Land weiterleiten.",
      "lb": "Et kann Iech bei méi wéi honnert Servicer, Selbsthëllefsgruppen, a Partner am ganze Land weiderleeden."},
 30: {"en": "The centre runs talks, events and awareness campaigns, and there's a national dementia prevention programme too.",
      "fr": "Le centre organise des conférences, des événements et des campagnes de sensibilisation, et il existe aussi un programme national de prévention de la démence.",
      "de": "Das Zentrum veranstaltet Vorträge, Veranstaltungen und Sensibilisierungskampagnen, und es gibt auch ein nationales Demenz-Präventionsprogramm.",
      "lb": "D'Zentrum organiséiert Virträg, Veranstaltungen a Sensibiliséierungscampagnen, an et gëtt och en nationaalt Programm fir Demenz-Preventioun."},
 34: {"en": "And contacting the centre is simple... by phone, by email, through their website, or in person in Luxembourg City, and sometimes in other towns.",
      "fr": "Et contacter le centre est simple... par téléphone, par e-mail, via leur site internet, ou sur place à Luxembourg-Ville, et parfois dans d'autres villes.",
      "de": "Und das Zentrum zu kontaktieren ist einfach... telefonisch, per E-Mail, über ihre Webseite, oder vor Ort in Luxemburg-Stadt, und manchmal auch in anderen Städten.",
      "lb": "An d'Zentrum ze kontaktéieren ass einfach... iwwer Telefon, iwwer E-Mail, iwwer hir Websäit, oder op der Plaz an der Stad, an heiansdo och an anere Stied."},
}, note("Website demenz.lu lists more than 100 services; campaigns 'VergiessMechNet' and 'Mäi Liewen mat Demenz'; Programme Démence Prévention (pdp.lu); monthly consultations also held in Esch-sur-Alzette.",
        "Le site demenz.lu répertorie plus de 100 services ; campagnes « VergiessMechNet » et « Mäi Liewen mat Demenz » ; Programme Démence Prévention (pdp.lu) ; permanences mensuelles aussi à Esch-sur-Alzette.",
        "Die Website demenz.lu listet mehr als 100 Dienste; Kampagnen „VergiessMechNet“ und „Mäi Liewen mat Demenz“; Programme Démence Prévention (pdp.lu); monatliche Sprechstunden auch in Esch-sur-Alzette.",
        "D'Websäit demenz.lu weist méi wéi 100 Servicer; Campagnen „VergiessMechNet“ an „Mäi Liewen mat Demenz“; Programme Démence Prévention (pdp.lu); all Mount Sprechstonnen och zu Esch-Uelzecht."))

apply("ess", {
 22: {"en": "It lets you create a real business whose official purpose is social impact, recognised by law since 2016 and approved by the Ministry of Labour.",
      "fr": "Il permet de créer une véritable entreprise dont l'objet officiel est l'impact social, reconnu par la loi depuis 2016 et agréé par le ministère du Travail.",
      "de": "Sie erlaubt es, ein echtes Unternehmen zu gründen, dessen offizieller Zweck die soziale Wirkung ist, gesetzlich anerkannt seit 2016 und vom Arbeitsministerium zugelassen.",
      "lb": "Et erlaabt et, eng richteg Entreprise ze grënnen, deem säin offiziellen Zweck de soziale Impakt ass, zënter 2016 vum Gesetz unerkannt a vum Aarbechtsministère zougelooss."},
 25: {"en": "The portal, run by the Ministry of Labour, explains the social and solidarity economy and how to create this kind of company. And the ministry's social business incubator offers free support to get started.",
      "fr": "Le portail, géré par le ministère du Travail, explique l'économie sociale et solidaire et comment créer ce type d'entreprise. Et l'incubateur du ministère accompagne gratuitement les porteurs de projet.",
      "de": "Das Portal des Arbeitsministeriums erklärt die Sozial- und Solidarwirtschaft und wie man ein solches Unternehmen gründet. Und der Inkubator des Ministeriums begleitet Gründer kostenlos.",
      "lb": "De Portal vum Aarbechtsministère erkläert d'Sozial- a Solidarwirtschaft a wéi ee sou eng Entreprise grënnt. An den Inkubator vum Ministère begleet Grënner gratis."},
}, note("SIS created by the law of 12 December 2016; approval by the Ministry of Labour (department of the social and solidarity economy), which runs the portal and the free Social Business Incubator; guide 'How to get started' updated January 2026; ULESS became Entrepreneurs d'Impact Luxembourg (EIL) in September 2025.",
        "SIS créée par la loi du 12 décembre 2016 ; agrément par le ministère du Travail (département de l'économie sociale et solidaire), qui gère le portail et le Social Business Incubator gratuit ; « Guide de l'entrepreneur social » mis à jour en janvier 2026 ; l'ULESS est devenue Entrepreneurs d'Impact Luxembourg (EIL) en septembre 2025.",
        "SIS durch das Gesetz vom 12. Dezember 2016 geschaffen; Zulassung durch das Arbeitsministerium (Abteilung Sozial- und Solidarwirtschaft), das das Portal und den kostenlosen Social Business Incubator betreibt; Leitfaden für Sozialunternehmer im Januar 2026 aktualisiert; die ULESS wurde im September 2025 zu Entrepreneurs d'Impact Luxembourg (EIL).",
        "SIS duerch d'Gesetz vum 12. Dezember 2016 geschaf; Zouloossung duerch den Aarbechtsministère (Departement Sozial- a Solidarwirtschaft), deen de Portal an de gratis Social Business Incubator bedreift; Guide fir sozial Entrepreneuren am Januar 2026 aktualiséiert; d'ULESS gouf am September 2025 zu Entrepreneurs d'Impact Luxembourg (EIL)."))
