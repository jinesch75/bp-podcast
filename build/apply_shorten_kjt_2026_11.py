#!/usr/bin/env python3
"""KJT episode shortened to about 10 minutes (Jacques, 26 Nov 2026): 78 -> 50 body lines in build/kjt_src/<lang>.txt.
Lines kept by their old number; the lines in NEW replace the old text. Runs once (does nothing when a file already has 50 lines).
Then: python3 build/make_scripts_kjt.py"""
KEEP = [1,2,3,6,7,8,9,12,13,14,15,16,19,20,21,22,25,26,27,30,31,32,33,34,39,40,41,44,45,46,47,50,51,52,53,54,59,60,63,68,69,70,71,72,73,74,75,76,77,78]
NEW = {
"en": {
 3: "T: The KJT was founded in 1992, in connection with the United Nations Convention on the Rights of the Child. The idea was simple: every child and every young person should have the chance to be heard. Today, the KJT is a service of a non-profit association called CJF Lëtzebuerg, and it is financed through an agreement with the National Youth Service, which comes under the Ministry of Education, Children and Youth.",
 6: "A: What does the KJT actually do when someone gets in touch?",
 9: "T: No, and that is one of the five principles of the KJT. It is called self-determination: after the conversation, each person decides alone which steps to take. The other principles are anonymity, confidentiality, tolerance and respect, and openness to any question and any subject.",
 16: "A: No, the line is not open around the clock. It is open in the afternoon and in the evening, from Monday to Saturday. The exact hours are on the website, and so are the times when you can call in English.",
 20: "A: For them, there is the Online Help. You write your question or your worry on the website of the KJT, in Luxembourgish, German, French or English, and a counsellor sends you a written answer within a few days.",
 27: "T: No, and that is what makes the chat special. The website describes it as peer-to-peer, because the chat counsellors are young people themselves. They have been trained, and they also bring in their own experience. The chat is open at fixed times in the evening, which you find on the website.",
 34: "A: You can expect counselling, orientation and information. The counsellors do not step in and act in your place. They help you to see more clearly, they give practical suggestions, and they can tell you which other services in Luxembourg could help. The service is free, anonymous and confidential, and the hours are on the website.",
 41: "T: It is for every citizen, of any age. You can call with questions about safety on the internet and in digital media. The team gives individual advice, and if necessary it points you to a specialised service. The calls are free, anonymous and confidential. And here is one detail for cross-border workers: the website says that this number can only be reached from the Luxembourg network.",
 47: "T: There are three kinds: images that show the sexual abuse of minors, content that is racist, revisionist or discriminatory, which includes hate speech, and content linked to terrorism. The Stopline analyses each report and passes it on to the competent services of the Grand Ducal Police, and it does not store data that could identify you.",
 60: "A: There is a form on the website for people who are interested, and there is an information evening before each new training.",
 63: "T: The website kjt dot l-u is worth a visit, also for adults. It exists in German, French and English. There are pages on subjects that matter to young people, such as friendship, conflicts in the family, cyberbullying and mental health, and also on very serious subjects, such as violence, sexual abuse and suicide. There is also a toolbox with tips, videos and a page that helps you to find counselling centres in Luxembourg.",
},
"fr": {
 3: "T: Le KJT a été fondé en 1992, dans le cadre de la Convention des Nations Unies relative aux droits de l'enfant. L'idée était simple : chaque enfant et chaque jeune doit avoir la possibilité d'être écouté. Aujourd'hui, le KJT est un service d'une association sans but lucratif qui s'appelle CJF Lëtzebuerg, et il est financé dans le cadre d'une convention avec le Service national de la jeunesse, qui dépend du Ministère de l'Éducation nationale, de l'Enfance et de la Jeunesse.",
 6: "A: Que fait concrètement le KJT quand quelqu'un le contacte ?",
 9: "T: Non, et c'est justement un des cinq principes du KJT. Il s'appelle l'autodétermination : après l'entretien, chaque personne décide elle-même des étapes à suivre. Les autres principes sont l'anonymat, la confidentialité, la tolérance et le respect, et l'ouverture à toutes les questions et à tous les sujets.",
 16: "A: Non, la ligne n'est pas ouverte en permanence. Elle est ouverte l'après-midi et le soir, du lundi au samedi. Les horaires exacts se trouvent sur le site, tout comme les moments où l'on peut appeler en anglais.",
 20: "A: Pour eux, il y a l'Online Help. Vous écrivez votre question ou votre souci sur le site du KJT, en luxembourgeois, en allemand, en français ou en anglais, et un conseiller vous envoie une réponse écrite en quelques jours.",
 27: "T: Non, et c'est ce qui rend le chat particulier. Le site le décrit comme un service de pair à pair, car les conseillers du chat sont eux-mêmes des jeunes. Ils ont suivi une formation, et ils apportent aussi leur propre expérience. Le chat est ouvert à des heures fixes en soirée, que vous trouvez sur le site.",
 34: "A: Vous pouvez attendre de l'écoute, des conseils et des informations. Les conseillers n'interviennent pas à votre place. Ils vous aident à y voir plus clair, ils font des suggestions pratiques, et ils peuvent vous dire quels autres services au Luxembourg pourraient vous aider. Le service est gratuit, anonyme et confidentiel, et les horaires se trouvent sur le site.",
 41: "T: Elle est ouverte à tout citoyen, de tout âge. Vous pouvez appeler pour des questions sur la sécurité sur Internet et dans les médias numériques. L'équipe donne des conseils individuels et, si nécessaire, elle vous oriente vers un service spécialisé. Les appels sont gratuits, anonymes et confidentiels. Et voici un détail pour les frontaliers : le site précise que ce numéro est joignable uniquement depuis le réseau luxembourgeois.",
 47: "T: Il y en a trois : les représentations d'abus sexuels sur des mineurs, les contenus racistes, révisionnistes ou discriminatoires, y compris les discours de haine, et les contenus liés au terrorisme. La Stopline analyse chaque signalement et le transmet aux services compétents de la Police grand-ducale, et elle n'enregistre pas de données qui permettraient de vous identifier.",
 60: "A: Il y a un formulaire sur le site pour les personnes intéressées, et une soirée d'information a lieu avant chaque nouvelle formation.",
 63: "T: Le site kjt point l-u vaut une visite, aussi pour les adultes. Il existe en allemand, en français et en anglais. Il y a des pages sur des sujets qui comptent pour les jeunes, comme l'amitié, les conflits dans la famille, le cyberharcèlement et la santé mentale, et aussi sur des sujets très graves, comme la violence, les abus sexuels et le suicide. Il y a aussi une boîte à outils avec des conseils, des vidéos et une page qui vous aide à trouver des centres de consultation au Luxembourg.",
},
"de": {
 3: "T: Das KJT wurde 1992 gegründet, im Rahmen der Kinderrechtskonvention der Vereinten Nationen. Die Idee war einfach: Jedes Kind und jeder Jugendliche soll die Möglichkeit haben, gehört zu werden. Heute ist das KJT ein Dienst einer Vereinigung ohne Gewinnzweck mit dem Namen CJF Lëtzebuerg, und es wird im Rahmen einer Konvention mit dem Service National de la Jeunesse finanziert, der zum Ministerium für Bildung, Kinder und Jugend gehört.",
 6: "A: Was macht das KJT konkret, wenn sich jemand meldet?",
 9: "T: Nein, und das ist eines der fünf Prinzipien des KJT. Es heißt Selbstbestimmung: Nach dem Gespräch entscheidet jede Person selbst, welche Schritte sie geht. Die anderen Prinzipien sind die Anonymität, die Schweigepflicht, Toleranz und Respekt, und die Offenheit für jede Frage und jedes Thema.",
 16: "A: Nein, die Leitung ist nicht rund um die Uhr besetzt. Sie ist nachmittags und abends erreichbar, von Montag bis Samstag. Die genauen Zeiten stehen auf der Website, und dort steht auch, wann man auf Englisch anrufen kann.",
 20: "A: Für sie gibt es die Online Help. Man schreibt seine Frage oder seine Sorge auf der Website des KJT, auf Luxemburgisch, Deutsch, Französisch oder Englisch, und ein Berater schickt innerhalb weniger Tage eine schriftliche Antwort.",
 27: "T: Nein, und genau das macht den Chat besonders. Die Website beschreibt ihn als Peer-to-Peer-Angebot, denn die Chatberater sind selbst junge Menschen. Sie haben eine Ausbildung gemacht, und sie bringen auch ihre eigenen Erfahrungen mit. Der Chat ist zu festen Zeiten am Abend geöffnet, die Sie auf der Website finden.",
 34: "A: Sie können Beratung, Orientierung und Information erwarten. Die Berater greifen nicht an Ihrer Stelle ein. Sie helfen Ihnen, klarer zu sehen, sie geben praktische Anregungen, und sie können Ihnen sagen, welche anderen Stellen in Luxemburg helfen könnten. Das Angebot ist kostenlos, anonym und vertraulich, und die Zeiten stehen auf der Website.",
 41: "T: Sie ist für jeden Bürger jeden Alters da. Sie können mit Fragen zur Sicherheit im Internet und in den digitalen Medien anrufen. Das Team berät Sie individuell und verweist Sie, wenn nötig, an eine spezialisierte Stelle. Die Anrufe sind kostenlos, anonym und vertraulich. Und hier ist ein Hinweis für Grenzgänger: Laut der Website ist diese Nummer nur aus dem luxemburgischen Netz erreichbar.",
 47: "T: Es gibt drei Arten: Darstellungen von sexuellem Missbrauch von Minderjährigen, rassistische, revisionistische oder diskriminierende Inhalte, wozu auch Hassrede gehört, und Inhalte, die mit Terrorismus zu tun haben. Die Stopline analysiert jede Meldung und leitet sie an die zuständigen Dienste der Großherzoglichen Polizei weiter, und sie speichert keine Daten, mit denen man Sie erkennen könnte.",
 60: "A: Auf der Website gibt es ein Formular für Interessierte, und vor jeder neuen Ausbildung gibt es einen Informationsabend.",
 63: "T: Die Website kjt Punkt l-u lohnt einen Besuch, auch für Erwachsene. Es gibt sie auf Deutsch, Französisch und Englisch. Es gibt Seiten zu Themen, die Jugendliche beschäftigen, wie Freundschaft, Konflikte in der Familie, Cybermobbing und psychische Gesundheit, und auch zu sehr ernsten Themen, wie Gewalt, sexuellem Missbrauch und Suizid. Es gibt auch eine Toolbox mit Tipps, Videos und einer Seite, die Ihnen hilft, Beratungsstellen in Luxemburg zu finden.",
},
"lb": {
 3: "T: De KJT gouf 1992 gegrënnt, am Kader vun der Kannerrechtskonventioun vun de Vereenten Natiounen. D'Iddi war einfach: all Kand an all Jugendleche soll d'Méiglechkeet hunn, gehéiert ze ginn. Haut ass de KJT e Service vun enger Associatioun ouni Gewënnzweck mam Numm CJF Lëtzebuerg, an e gëtt am Kader vun enger Konventioun mam Service National de la Jeunesse finanzéiert, deen zum Ministère fir Educatioun, Kanner a Jugend gehéiert.",
 6: "A: Wat mécht de KJT konkret, wann ee sech mellt?",
 9: "T: Nee, an dat ass ee vun de fënnef Prinzippie vum KJT. Et heescht Selbstbestëmmung: nom Gespréich decidéiert all Persoun selwer, wéi eng Schrëtt si mécht. Déi aner Prinzippie sinn d'Anonymitéit, d'Schweigepflicht, Toleranz a Respekt, an d'Offenheet fir all Fro an all Thema.",
 16: "A: Nee, d'Linn ass net ronderëm d'Auer besat. Si ass nomëttes an owes ze erreechen, vu Méindes bis Samschdes. Déi genau Zäite stinn um Site, an do steet och, wéini een op Englesch uruffe kann.",
 20: "A: Fir si gëtt et d'Online Help. Et schreift ee seng Fro oder seng Suerg um Site vum KJT, op Lëtzebuergesch, Däitsch, Franséisch oder Englesch, an e Beroder schéckt bannent e puer Deeg eng schrëftlech Äntwert.",
 27: "T: Nee, a genau dat mécht de Chat besonnesch. De Site beschreift en als Peer-to-Peer-Offer, well d'Chatberoder si selwer jonk Leit. Si hunn eng Formatioun gemaach, a si bréngen och hir eegen Erfarunge mat. De Chat ass zu feste Zäiten owes op, déi Dir um Site fannt.",
 34: "A: Dir kënnt Berodung, Orientéierung an Informatioun erwaarden. D'Beroder gräifen net op Ärer Plaz an. Si hëllefen Iech, méi kloer ze gesinn, si ginn Iech praktesch Iddien, a si kënnen Iech soen, wéi eng aner Servicer zu Lëtzebuerg hëllefe kéinten. D'Offer ass gratis, anonym a vertraulech, an d'Zäite stinn um Site.",
 41: "T: Si ass fir all Bierger an all Alter do. Dir kënnt mat Froen iwwer d'Sécherheet am Internet an an den digitale Medien uruffen. D'Equipe beréit Iech individuell a weist Iech, wann néideg, un e spezialiséierte Service weider. D'Uriff si gratis, anonym a vertraulech. An hei ass en Hiweis fir Grenzgänger: laut dem Site ass dës Nummer nëmmen aus dem lëtzebuergeschen Netz ze erreechen.",
 47: "T: Et ginn dräi Zorten: Duerstellunge vu sexuellem Mëssbrauch vu Mannerjäregen, rassistesch, revisionistesch oder diskriminéierend Inhalter, wouzou och Haassried gehéiert, an Inhalter, déi mat Terrorismus ze dinn hunn. D'Stopline analyséiert all Meldung a gëtt se un déi zoustänneg Servicer vun der Groussherzoglecher Police weider, a si späichert keng Donnéeën, mat deenen een Iech erkenne kéint.",
 60: "A: Um Site gëtt et e Formulaire fir Interesséierter, a virun all neier Ausbildung gëtt et en Informatiounsowend.",
 63: "T: De Site kjt Punkt l-u ass eng Visitt wäert, och fir Erwuessener. Et gëtt en op Däitsch, Franséisch an Englesch. Et gi Säiten iwwer Themen, déi Jugendlecher beschäftegen, wéi Frëndschaft, Konflikter an der Famill, Cybermobbing a psychesch Gesondheet, an och iwwer ganz eescht Themen, wéi Gewalt, sexuelle Mëssbrauch a Suizid. Et gëtt och eng Toolbox mat Tipps, Videoen an enger Säit, déi Iech hëlleft, Berodungsstellen zu Lëtzebuerg ze fannen.",
},
}
ADD54 = {"en": " There is also an internship at the side of experienced counsellors, and afterwards regular supervision.",
         "fr": " Il y a aussi un stage aux côtés de conseillers expérimentés, et ensuite une supervision régulière.",
         "de": " Dazu kommen ein Praktikum an der Seite von erfahrenen Beratern und danach regelmäßige Supervision.",
         "lb": " Dozou kommen e Stage un der Säit vun erfuerene Beroder an duerno reegelméisseg Supervisioun."}
for lang in ("en", "fr", "de", "lb"):
    p = f"build/kjt_src/{lang}.txt"
    old = [l.rstrip("\n") for l in open(p, encoding="utf-8") if l.strip()]
    if len(old) == 50: print(lang, "already short"); continue
    assert len(old) == 78, (lang, len(old))
    out = []
    for n in KEEP:
        line = NEW[lang].get(n, old[n - 1]) + (ADD54[lang] if n == 54 else "")
        assert line[:1] == old[n - 1][:1], (lang, n)   # same speaker as before
        out.append(line)
    open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(lang, len(out), "lines")
