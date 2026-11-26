"""Zesumme Vereinfachen, partner feedback (Steve, Zesumme Vereinfachen team, Ministry for Digitalisation, 25-26 Nov 2026):
"less focus on the digital component, more on administrative steps in general" + use the example of the
Guichet de proximite (multi-channel consultation -> Guichet.lu on tour bus) or of the water plan (AGE, PDG4).

Rebuilds podcast_script_zesumme{,_fr,_de,_lb}.md from the current files:
- the MyGuichet-app example (old turns 35-38) is replaced by the Guichet.lu bus story (Tom explains) and the
  4th water management plan (Anna explains);
- two new exchanges: "not only apps and websites" and "taking part offline";
- "..." pauses removed in the body (standard intro/outro untouched);
- recap / practical tips / header length / sources updated.
Unchanged turns are copied byte for byte (so their cached audio is reused).
Runs once: aborts if the old turn count (61) is not found.
"""
import re, sys

TURN = re.compile(r"^\*\*(ANNA|TOM)\s?:\*\*\s?(.*)$")

# New sequence: int = old turn number (1-based) kept as is; (speaker, {lang: text}) = new/changed turn.
def N(spk, en, fr, de, lb):
    return (spk, {"": en, "_fr": fr, "_de": de, "_lb": lb})

SEQ = [1, 2, 3,
 N("T", "And today we have a topic that, honestly, almost everyone has feelings about: paperwork.",
        "Et aujourd'hui, nous avons un sujet qui, honnêtement, touche presque tout le monde : la paperasse.",
        "Und heute haben wir ein Thema, zu dem ehrlich gesagt fast jeder etwas zu sagen hat: der Papierkram.",
        "A haut hu mir en Thema, dat éierlech gesot bal jiddereen ugeet: de Pabeierkrom."),
 N("A", "Yes! Forms, procedures, administrative steps. Sometimes they are simple. And sometimes, they are not.",
        "Oui ! Les formulaires, les procédures, les démarches administratives. Parfois, ils sont simples. Et parfois, ils ne le sont pas.",
        "Ja! Formulare, Verfahren, behördliche Schritte. Manchmal sind sie einfach. Und manchmal sind sie es nicht.",
        "Jo! Formulairen, Prozeduren, administrativ Schrëtt. Heiansdo sinn se einfach. An heiansdo sinn se et net."),
 N("T", "We have all had that moment. A form that asks the same thing twice. A step that makes you think: why is this so complicated?",
        "Nous avons tous vécu ce moment. Un formulaire qui demande deux fois la même chose. Une étape qui vous fait penser : pourquoi est-ce si compliqué ?",
        "Wir alle kennen diesen Moment. Ein Formular, das dasselbe zweimal abfragt. Ein Schritt, bei dem man denkt: Warum ist das so kompliziert?",
        "Mir hunn all dee Moment scho gehat. E Formulaire dee zweemol no derselwechter Saach freet. E Schrëtt deen Iech denke léisst: firwat ass dat esou komplizéiert?"),
 7, 8, 9, 10,
 N("A", "It is a participation platform where citizens and businesses can help make the State's procedures, and administrative steps in general, simpler.",
        "C'est une plateforme participative où les citoyens et les entreprises peuvent aider à rendre plus simples les procédures de l'État, et les démarches administratives en général.",
        "Es ist eine Beteiligungsplattform, auf der Bürger und Unternehmen dabei helfen können, die Verfahren des Staates und die Verwaltungsschritte im Allgemeinen einfacher zu gestalten.",
        "Et ass eng Plattform fir matzemaachen, wou Bierger an Entreprisen kënnen hëllefen, dem Staat seng Prozeduren, an d'administrativ Schrëtt am Allgemengen, méi einfach ze maachen."),
 12,
 N("A", "Exactly. Its slogan says it beautifully: public services that make your daily life easier.",
        "Exactement. Son slogan le dit magnifiquement : des services publics qui vous facilitent la vie au quotidien.",
        "Genau. Der Slogan bringt es wunderbar auf den Punkt: öffentliche Dienste, die Ihren Alltag einfacher machen.",
        "Genee. Säi Slogan seet et wonnerbar: ëffentlech Servicer déi Iech den Alldag méi einfach maachen."),
 14, 15, 16,
 N("A", "That bigger effort even has its own name: \"Einfach Lëtzebuerg\", which means \"Simply Luxembourg\".",
        "Cet effort plus large a même son propre nom : « Einfach Lëtzebuerg », qui signifie « Le Luxembourg en toute simplicité ».",
        "Diese größere Anstrengung hat sogar einen eigenen Namen: „Einfach Lëtzebuerg\", was „Einfach Luxemburg\" bedeutet.",
        "Dee méi groussen Effort huet souguer säin eegenen Numm: „Einfach Lëtzebuerg\"."),
 N("T", "With a Ministry for Digitalisation behind it, I would expect it to be all about apps and websites.",
        "Avec le Ministère de la Digitalisation derrière, je m'attendrais à ce que tout tourne autour des applications et des sites internet.",
        "Mit dem Ministerium für Digitalisierung dahinter würde ich erwarten, dass sich alles um Apps und Websites dreht.",
        "Mam Ministère fir Digitaliséierung dohannert géif ech mengen, datt et nëmmen ëm Appen a Websäiten geet."),
 N("A", "Many people think that, but it goes much wider. It is about administrative steps in general: forms, offices, counters, and how close public services are to the people who use them.",
        "Beaucoup de gens le pensent, mais c'est bien plus large. Il s'agit des démarches administratives en général : les formulaires, les bureaux, les guichets, et la proximité des services publics avec les personnes qui les utilisent.",
        "Das denken viele, aber es geht viel weiter. Es geht um Verwaltungsschritte im Allgemeinen: Formulare, Ämter, Schalter, und darum, wie nah die öffentlichen Dienste an den Menschen sind, die sie nutzen.",
        "Dat mengen der vill, mä et geet vill méi wäit. Et geet ëm administrativ Schrëtt am Allgemengen: Formulairen, Büroen, Guichetën, a wéi no d'ëffentlech Servicer bei de Leit sinn, déi se benotzen."),
 18, 19, 20, 21, 22,
 N("A", "And then the work happens in a participatory, co-creative way, together with the people who proposed it. Ministries and administrations can also post their own projects there, to ask for people's opinions.",
        "Et ensuite, le travail se déroule de manière participative et co-créative, avec les personnes qui l'ont proposé. Les ministères et les administrations peuvent aussi y publier leurs propres projets, pour demander l'avis des gens.",
        "Und dann erfolgt die Arbeit auf partizipative, ko-kreative Weise, gemeinsam mit denen, die den Vorschlag gemacht haben. Ministerien und Verwaltungen können dort auch eigene Projekte veröffentlichen, um die Meinung der Menschen einzuholen.",
        "An dann passéiert d'Aarbecht op eng participativ, ko-kreativ Manéier, zesumme mat de Leit déi et virgeschloen hunn. Ministèren an Administratiounen kënnen do och hir eege Projeten publizéieren, fir d'Meenung vun de Leit ze froen."),
 24, 25, 26, 27, 28,
 N("A", "And the platform welcomes everyone, in all four of our languages: Luxembourgish, German, French, and English.",
        "Et la plateforme accueille tout le monde, dans nos quatre langues : le luxembourgeois, l'allemand, le français et l'anglais.",
        "Und die Plattform heißt alle willkommen, in allen vier unserer Sprachen: Luxemburgisch, Deutsch, Französisch und Englisch.",
        "An d'Plattform begréisst jiddereen, an all eise véier Sproochen: Lëtzebuergesch, Däitsch, Franséisch an Englesch."),
 30,
 N("A", "And what about people who do not use the internet much? Can they take part too?",
        "Et les personnes qui utilisent peu internet ? Peuvent-elles participer aussi ?",
        "Und was ist mit Menschen, die das Internet kaum nutzen? Können sie auch mitmachen?",
        "A wat ass mat Leit, déi kaum den Internet benotzen? Kënne si och matmaachen?"),
 N("T", "Yes, they can, because in some projects people could also give their opinion on paper, in workshops, at stands, or at round tables. We will hear two real examples in a moment.",
        "Oui, tout à fait, car dans certains projets, on pouvait aussi donner son avis sur papier, lors d'ateliers, à des stands ou lors de tables rondes. Nous allons entendre deux exemples concrets dans un instant.",
        "Ja, das können sie, denn bei manchen Projekten konnte man seine Meinung auch auf Papier abgeben, in Workshops, an Ständen oder an runden Tischen. Gleich hören wir zwei echte Beispiele.",
        "Jo, dat kënne si, well bei verschiddene Projete konnt een seng Meenung och op Pabeier ginn, an Atelieren, bei Stänn oder bei Ronnen Dëscher. Mir héieren elo gläich zwee richteg Beispiller."),
 31, 32, 33, 34,
 # --- Example 1: Guichet.lu on tour (Tom explains) ---
 N("A", "Those are good ideas. But has the platform already changed something real?",
        "Ce sont de bonnes idées. Mais la plateforme a-t-elle déjà changé quelque chose de concret ?",
        "Das sind gute Ideen. Aber hat die Plattform schon etwas Konkretes verändert?",
        "Dat si gutt Iddien. Mä huet d'Plattform schonn eppes Konkretes verännert?"),
 N("T", "It has, and my favourite example is about meeting the administration face to face. For a long time, if you wanted help with a procedure in person, you went to the Guichet.lu reception desk in Luxembourg City.",
        "Oui, et mon exemple préféré concerne le contact en personne avec l'administration. Pendant longtemps, si vous vouliez de l'aide en personne pour une démarche, vous alliez au guichet d'accueil de Guichet.lu, à Luxembourg-Ville.",
        "Ja, und mein Lieblingsbeispiel handelt vom persönlichen Kontakt mit der Verwaltung. Lange Zeit musste man, wenn man persönlich Hilfe bei einem Verfahren wollte, zum Empfangsschalter von Guichet.lu in Luxemburg-Stadt gehen.",
        "Jo, a mäi Liblingsbeispill geet ëm de perséinleche Kontakt mat der Administratioun. Laang Zäit ass een, wann een perséinlech Hëllef bei enger Prozedur wollt, bei de Guichet vu Guichet.lu an der Stad gaangen."),
 N("A", "That can be a long trip for some people, depending on where they live.",
        "Cela peut faire un long trajet pour certaines personnes, selon l'endroit où elles habitent.",
        "Das kann für manche Menschen ein weiter Weg sein, je nachdem, wo sie wohnen.",
        "Dat ka fir verschidde Leit e wäite Wee sinn, jee nodeem wou se wunnen."),
 N("T", "Exactly. The government had promised more reception desks in the regions. So the Ministry for Digitalisation asked people what they would need from a reception desk close to home.",
        "Exactement. Le gouvernement avait promis d'autres guichets d'accueil dans les régions. Alors le Ministère de la Digitalisation a demandé aux gens ce dont ils auraient besoin dans un guichet proche de chez eux.",
        "Genau. Die Regierung hatte weitere Empfangsschalter in den Regionen versprochen. Also fragte das Ministerium für Digitalisierung die Menschen, was sie von einem Schalter in ihrer Nähe brauchen würden.",
        "Genee. D'Regierung hat weider Guichetën an de Regiounen versprach. Dofir huet de Ministère fir Digitaliséierung d'Leit gefrot, wat si vun engem Guichet no bei hinnen doheem bräichten."),
 N("A", "And how did they ask people: only online, or in other ways too?",
        "Et comment a-t-on interrogé les gens : seulement en ligne, ou autrement aussi ?",
        "Und wie wurden die Menschen gefragt: nur online, oder auch anders?",
        "A wéi goufen d'Leit gefrot: nëmmen online, oder och anescht?"),
 N("T", "Not only online, and that is the interesting part. People could answer on the platform, on a paper form, in workshops, and at stands.",
        "Pas seulement en ligne, et c'est cela qui est intéressant. On pouvait répondre sur la plateforme, sur un formulaire papier, lors d'ateliers et à des stands.",
        "Nicht nur online, und das ist das Interessante daran. Man konnte auf der Plattform antworten, auf einem Papierformular, in Workshops und an Ständen.",
        "Net nëmmen online, an dat ass dat Interessant. Ee konnt op der Plattform äntweren, op engem Pabeierformulaire, an Atelieren a bei Stänn."),
 N("A", "So even people who rarely go online could give their opinion.",
        "Donc même les personnes qui vont rarement sur internet ont pu donner leur avis.",
        "Also konnten auch Menschen, die selten online sind, ihre Meinung sagen.",
        "Also konnten och Leit, déi selten online sinn, hir Meenung soen."),
 N("T", "That's right. In the end, nearly eight thousand people took part.",
        "C'est exact. Au final, près de huit mille personnes ont participé.",
        "Richtig. Am Ende haben fast achttausend Menschen mitgemacht.",
        "Dat stëmmt. Um Enn hu bal aachtdausend Leit matgemaach."),
 N("A", "That is a lot of voices. And what did all those people tell the State?",
        "Cela fait beaucoup de voix. Et qu'est-ce que toutes ces personnes ont dit à l'État ?",
        "Das sind viele Stimmen. Und was haben all diese Menschen dem Staat gesagt?",
        "Dat si vill Stëmmen. A wat hunn all déi Leit dem Staat gesot?"),
 N("T", "The results clearly showed one need: public services should be closer to people, especially to those who find it hard to do their procedures online.",
        "Les résultats ont clairement montré un besoin : les services publics doivent être plus proches des gens, surtout de ceux qui ont du mal à faire leurs démarches en ligne.",
        "Die Ergebnisse zeigten deutlich einen Bedarf: Die öffentlichen Dienste sollen näher bei den Menschen sein, vor allem bei denen, denen es schwerfällt, ihre Verfahren online zu erledigen.",
        "D'Resultater hunn däitlech e Besoin gewisen: d'ëffentlech Servicer solle méi no bei de Leit sinn, virun allem bei deenen, deenen et schwéier fält, hir Prozeduren online ze maachen."),
 N("A", "And what came out of it in the end?",
        "Et qu'est-ce qui en est sorti, finalement ?",
        "Und was ist am Ende dabei herausgekommen?",
        "A wat ass um Enn dobäi erauskomm?"),
 N("T", "A bus! It is called Guichet.lu on tour. It is a fully electric bus, fitted out like a reception desk, and it travels to the different regions of the country.",
        "Un bus ! Il s'appelle Guichet.lu on tour. C'est un bus cent pour cent électrique, aménagé comme un guichet d'accueil, et il se déplace dans les différentes régions du pays.",
        "Ein Bus! Er heißt Guichet.lu on tour. Es ist ein vollelektrischer Bus, eingerichtet wie ein Empfangsschalter, und er fährt in die verschiedenen Regionen des Landes.",
        "E Bus! En heescht Guichet.lu on tour. Et ass e ganz elektresche Bus, ageriicht wéi e Guichet, an e fiert an déi verschidde Regioune vum Land."),
 N("A", "So the counter comes to you. And what can you do on board?",
        "Donc c'est le guichet qui vient à vous. Et que peut-on faire à bord ?",
        "Der Schalter kommt also zu Ihnen. Und was kann man an Bord machen?",
        "De Guichet kënnt also bei Iech. A wat kann een u Bord maachen?"),
 N("T", "You can get help with a procedure, or with using MyGuichet.lu. You can find the right service for your question, or apply for a Luxembourg identity card or driving licence.",
        "Vous pouvez recevoir de l'aide pour une démarche, ou pour utiliser MyGuichet.lu. Vous pouvez trouver le bon service pour votre question, ou demander une carte d'identité ou un permis de conduire luxembourgeois.",
        "Sie können Hilfe bei einem Verfahren bekommen, oder bei der Nutzung von MyGuichet.lu. Sie können die richtige Stelle für Ihre Frage finden, oder einen luxemburgischen Personalausweis oder Führerschein beantragen.",
        "Dir kritt Hëllef bei enger Prozedur, oder fir MyGuichet.lu ze benotzen. Dir fannt de richtege Service fir Är Fro, oder Dir kënnt eng lëtzebuergesch Identitéitskaart oder e Führerschäin ufroen."),
 N("A", "I really like that. People's ideas did not lead to a new app, but to a real bus, with real people to help you.",
        "J'aime beaucoup cela. Les idées des gens n'ont pas mené à une nouvelle application, mais à un vrai bus, avec de vraies personnes pour vous aider.",
        "Das gefällt mir sehr. Die Ideen der Menschen haben nicht zu einer neuen App geführt, sondern zu einem echten Bus, mit echten Menschen, die Ihnen helfen.",
        "Dat gefält mer immens. D'Iddie vun de Leit hunn net zu enger neier App gefouert, mä zu engem richtege Bus, mat richtege Leit, déi Iech hëllefen."),
 # --- Example 2: 4th water management plan (Anna explains) ---
 N("T", "Is there also an example where a ministry asks for people's opinion on a bigger plan?",
        "Y a-t-il aussi un exemple où un ministère demande l'avis des gens sur un plan plus important ?",
        "Gibt es auch ein Beispiel, bei dem ein Ministerium die Menschen zu einem größeren Plan befragt?",
        "Gëtt et och e Beispill, wou e Ministère d'Leit zu engem gréissere Plang freet?"),
 N("A", "Yes, and it is about water. Every six years, Luxembourg updates its plan for managing its water, as a European directive requires.",
        "Oui, et il concerne l'eau. Tous les six ans, le Luxembourg met à jour son plan de gestion de l'eau, comme l'exige une directive européenne.",
        "Ja, und es geht um Wasser. Alle sechs Jahre aktualisiert Luxemburg seinen Plan für die Bewirtschaftung seiner Gewässer, wie es eine europäische Richtlinie verlangt.",
        "Jo, an et geet ëm d'Waasser. All sechs Joer aktualiséiert Lëtzebuerg säi Plang fir d'Gestioun vu sengem Waasser, esou wéi eng europäesch Direktiv et verlaangt."),
 N("T", "And what is in a plan like that, exactly?",
        "Et que contient un tel plan, exactement ?",
        "Und was steht in so einem Plan genau drin?",
        "A wat steet genee an esou engem Plang?"),
 N("A", "It describes the state of our waters, the main issues, and the measures planned to protect and restore them.",
        "Il décrit l'état de nos eaux, les principaux enjeux, et les mesures prévues pour les protéger et les restaurer.",
        "Er beschreibt den Zustand unserer Gewässer, die wichtigsten Herausforderungen und die geplanten Maßnahmen, um sie zu schützen und wiederherzustellen.",
        "E beschreift den Zoustand vun eise Gewässer, déi wichtegst Erausfuerderungen, an d'Moossname fir se ze schützen an ze restauréieren."),
 N("T", "And who prepares this plan, and with whom?",
        "Et qui prépare ce plan, et avec qui ?",
        "Und wer bereitet diesen Plan vor, und mit wem?",
        "A wie preparéiert dëse Plang, a mat wiem?"),
 N("A", "The Water Management Administration is preparing the fourth plan, for 2027 to 2033. It is preparing it together with citizens, communes, businesses and experts.",
        "L'Administration de la gestion de l'eau prépare le quatrième plan, pour les années 2027 à 2033. Elle le prépare avec les citoyens, les communes, les entreprises et des experts.",
        "Das Wasserwirtschaftsamt bereitet den vierten Plan vor, für die Jahre 2027 bis 2033. Es bereitet ihn gemeinsam mit Bürgern, Gemeinden, Unternehmen und Fachleuten vor.",
        "D'Waasserwirtschaftsamt preparéiert de véierte Plang, fir d'Joren 2027 bis 2033. Et preparéiert en zesumme mat Bierger, Gemengen, Entreprisen an Experten."),
 N("T", "And how can ordinary people join in?",
        "Et comment les citoyens peuvent-ils y participer ?",
        "Und wie können die Menschen mitmachen?",
        "A wéi kënnen d'Leit matmaachen?"),
 N("A", "Through public consultations, and through round tables, seminars and workshops in different places. You can follow all of it on the platform.",
        "Par des consultations publiques, et par des tables rondes, des séminaires et des ateliers dans différents lieux. Vous pouvez tout suivre sur la plateforme.",
        "Über öffentliche Konsultationen, und über runde Tische, Seminare und Workshops an verschiedenen Orten. Sie können alles auf der Plattform verfolgen.",
        "Iwwer ëffentlech Konsultatiounen, an iwwer Ronn Dëscher, Seminairen an Atelieren op verschiddenen Plazen. Dir kënnt alles op der Plattform verfollegen."),
 N("T", "So simplifying together is not only about forms. It is also about shaping public decisions together, online, on paper, or around a table.",
        "Donc simplifier ensemble, ce n'est pas seulement une affaire de formulaires. C'est aussi construire ensemble des décisions publiques, en ligne, sur papier, ou autour d'une table.",
        "Gemeinsam vereinfachen heißt also nicht nur Formulare. Es heißt auch, öffentliche Entscheidungen gemeinsam zu gestalten, online, auf Papier oder an einem Tisch.",
        "Zesumme vereinfachen heescht also net nëmme Formulairen. Et heescht och, ëffentlech Decisiounen zesummen ze gestalten, online, op Pabeier, oder ronderëm en Dësch."),
 39, 40, 41, 42, 43,
 N("T", "And that fits the spirit of the Biergerpakt perfectly: citizens and the State, working together.",
        "Et cela correspond parfaitement à l'esprit du Biergerpakt : les citoyens et l'État, travaillant ensemble.",
        "Und das passt perfekt zum Geist des Biergerpakt: Bürger und Staat, die zusammenarbeiten.",
        "An dat passt perfekt zum Geescht vum Biergerpakt: Bierger an de Staat, déi zesummeschaffen."),
 45, 46, 47,
 N("T", "First, next time a procedure frustrates you, write the idea down instead of just sighing.",
        "D'abord, la prochaine fois qu'une procédure vous frustre, notez l'idée au lieu de simplement soupirer.",
        "Erstens: Wenn Sie das nächste Mal ein Verfahren frustriert, schreiben Sie die Idee auf, anstatt nur zu seufzen.",
        "Éischtens, d'nächst Kéier wann eng Prozedur Iech frustréiert, schreift d'Iddi op anstatt nëmmen ze sëfzen."),
 N("A", "Second, visit the platform and share your suggestion in your own language, or join a workshop or a round table when a project offers one.",
        "Ensuite, rendez-vous sur la plateforme Zesumme Vereinfachen et partagez votre suggestion dans votre propre langue, ou participez à un atelier ou à une table ronde quand un projet en propose.",
        "Zweitens: Besuchen Sie die Plattform Zesumme Vereinfachen und teilen Sie Ihren Vorschlag in Ihrer eigenen Sprache, oder machen Sie bei einem Workshop oder einem runden Tisch mit, wenn ein Projekt das anbietet.",
        "Zweetens, besicht d'Plattform Zesumme Vereinfachen an deelt Äre Virschlag an Ärer eegener Sprooch, oder maacht bei engem Atelier oder engem Ronnen Dësch mat, wann e Projet dat ubitt."),
 N("T", "Third, if you like, follow it through one or more phases, and help co-create the solution.",
        "Troisièmement, si vous le souhaitez, suivez-la à travers une ou plusieurs phases, et aidez à co-créer la solution.",
        "Drittens: Wenn Sie möchten, begleiten Sie sie durch eine oder mehrere Phasen und helfen Sie, die Lösung mitzugestalten.",
        "Drëttens, wann Dir wëllt, verfollegt en duerch eng oder méi Phasen, an hëlleft d'Léisung mat ze gestalten."),
 N("A", "And fourth, remember: even a small idea can make a real difference for many people.",
        "Et quatrièmement, rappelez-vous : même une petite idée peut faire une réelle différence pour de nombreuses personnes.",
        "Und viertens: Denken Sie daran, selbst eine kleine Idee kann für viele Menschen einen echten Unterschied machen.",
        "A véiertens, denkt drun: souguer eng kleng Iddi kann e richtegen Ënnerscheed fir vill Leit maachen."),
 52,
 N("A", "First, it is a platform where citizens and businesses help simplify the State's procedures, online and offline.",
        "Premièrement, c'est une plateforme où les citoyens et les entreprises aident à simplifier les procédures de l'État, en ligne et hors ligne.",
        "Erstens: Es ist eine Plattform, auf der Bürger und Unternehmen helfen, die Verfahren des Staates zu vereinfachen, online und offline.",
        "Éischtens, et ass eng Plattform wou Bierger an Entreprisen hëllefen, dem Staat seng Prozeduren ze vereinfachen, online an offline."),
 N("T", "Second, it is run by the Ministry for Digitalisation, and launched in 2022, as part of \"Einfach Lëtzebuerg\".",
        "Deuxièmement, elle est gérée par le Ministère de la Digitalisation, et lancée en 2022, dans le cadre d'« Einfach Lëtzebuerg ».",
        "Zweitens: Sie wird vom Ministerium für Digitalisierung betrieben und wurde 2022 gestartet, als Teil von „Einfach Lëtzebuerg\".",
        "Zweetens, si gëtt vum Ministère fir Digitaliséierung gefouert, a gouf 2022 lancéiert, als Deel vun „Einfach Lëtzebuerg\"."),
 N("A", "Third, you can submit ideas, join one phase or many, in any of the four languages.",
        "Troisièmement, vous pouvez soumettre des idées, participer à une seule phase ou à plusieurs, dans n'importe laquelle des quatre langues.",
        "Drittens: Sie können Ideen einreichen, an einer oder mehreren Phasen teilnehmen, in jeder der vier Sprachen.",
        "Drëttens, Dir kënnt Iddien araichen, un enger Phas oder ville matmaachen, an all eenzel vun de véier Sproochen."),
 N("T", "And fourth, it has already helped change real services, like the Guichet.lu bus that brings the counter closer to people.",
        "Et quatrièmement, elle a déjà aidé à changer de vrais services, comme le bus de Guichet.lu, qui rapproche le guichet des gens.",
        "Und viertens: Sie hat bereits geholfen, echte Dienste zu verändern, wie den Bus von Guichet.lu, der den Schalter näher zu den Menschen bringt.",
        "A véiertens, si huet schonn gehollef richteg Servicer ze veränneren, wéi de Bus vu Guichet.lu, deen de Guichet méi no bei d'Leit bréngt."),
 57,
 N("T", "So the next time something feels too complicated, remember: your voice can help fix it.",
        "Alors, la prochaine fois que quelque chose vous semble trop compliqué, rappelez-vous : votre voix peut aider à y remédier.",
        "Wenn sich also das nächste Mal etwas zu kompliziert anfühlt, denken Sie daran: Ihre Stimme kann helfen, es zu verbessern.",
        "Also d'nächst Kéier wann eppes ze komplizéiert schéngt, denkt drun: Är Stëmm kann hëllefen, et ze verbesseren."),
 59, 60, 61]

LENGTH = {"": ("**Length:** about 14 minutes", "**Length:** about 9 minutes"),
          "_fr": ("**Durée :** environ 14 minutes", "**Durée :** environ 9 minutes"),
          "_de": ("**Länge:** etwa 14 Minuten", "**Länge:** etwa 9 Minuten"),
          "_lb": ("**Längt:** ongeféier 14 Minutten", "**Längt:** ongeféier 9 Minutten")}

SOURCES = {
 "": "*Sources: \"Zesumme Vereinfachen\" platform, zesumme-vereinfachen.lu, and the Ministry for Digitalisation (mindigital.gouvernement.lu) — the participatory administrative-simplification platform managed by the Simplification Council, launched in 2022 as part of the \"Einfach Lëtzebuerg\" programme; citizens and businesses can submit ideas and take part in one or several project phases, in Luxembourgish, German, French or English; ministries and administrations can also submit projects for stakeholder feedback. Example 1: project \"Local reception desk\" (guichet de proximité) on zesumme-vereinfachen.lu — public consultation by the Ministry for Digitalisation (online, on paper, in workshops and at stands, about 8,000 participants), followed by a call by the Government IT Centre (CTIE) for a mobile reception desk serving every region; press conference of 1 October 2024 (gouvernement.lu); \"Guichet.lu on tour\" (guichet.public.lu). Example 2: project \"4e plan de gestion des ressources en eau au Luxembourg (2027–2033)\" on zesumme-vereinfachen.lu (Administration de la gestion de l'eau, Water Framework Directive). The remark that a trip to Luxembourg City can be long for some people is an illustration by the hosts. General information only. Revised on 26 November 2026 after feedback from the Zesumme Vereinfachen team (Ministry for Digitalisation).*",
 "_fr": "*Sources : plateforme « Zesumme Vereinfachen », zesumme-vereinfachen.lu, et le Ministère de la Digitalisation (mindigital.gouvernement.lu) — la plateforme participative de simplification administrative gérée par le Conseil de simplification, lancée en 2022 dans le cadre du programme « Einfach Lëtzebuerg » ; les citoyens et les entreprises peuvent soumettre des idées et prendre part à une ou plusieurs phases de projet, en luxembourgeois, allemand, français ou anglais ; les ministères et administrations peuvent aussi y soumettre des projets. Exemple 1 : projet « Guichet de proximité » sur zesumme-vereinfachen.lu — consultation publique du Ministère de la Digitalisation (en ligne, sur papier, lors d'ateliers et de stands, environ 8 000 participants), suivie d'un appel du Centre des technologies de l'information de l'État (CTIE) pour un guichet mobile desservant chaque région ; conférence de presse du 1er octobre 2024 (gouvernement.lu) ; « Guichet.lu on tour » (guichet.public.lu). Exemple 2 : projet « 4e plan de gestion des ressources en eau au Luxembourg (2027–2033) » sur zesumme-vereinfachen.lu (Administration de la gestion de l'eau, directive-cadre sur l'eau). La remarque sur la longueur du trajet vers Luxembourg-Ville est une illustration des animateurs. Informations générales uniquement. Révisé le 26 novembre 2026 après les remarques de l'équipe Zesumme Vereinfachen (Ministère de la Digitalisation).*",
 "_de": "*Quellen: Plattform „Zesumme Vereinfachen\", zesumme-vereinfachen.lu, und das Ministerium für Digitalisierung (mindigital.gouvernement.lu) — die partizipative Plattform zur Verwaltungsvereinfachung, verwaltet vom Vereinfachungsrat, gestartet 2022 als Teil des Programms „Einfach Lëtzebuerg\"; Bürger und Unternehmen können Ideen einreichen und an einer oder mehreren Projektphasen teilnehmen, auf Luxemburgisch, Deutsch, Französisch oder Englisch; Ministerien und Verwaltungen können ebenfalls Projekte einreichen. Beispiel 1: Projekt „Guichet de proximité\" auf zesumme-vereinfachen.lu — öffentliche Konsultation des Ministeriums für Digitalisierung (online, auf Papier, in Workshops und an Ständen, rund 8.000 Teilnehmende), danach ein Aufruf des Zentrums für Informationstechnologien des Staates (CTIE) für einen mobilen Schalter, der jede Region bedient; Pressekonferenz vom 1. Oktober 2024 (gouvernement.lu); „Guichet.lu on tour\" (guichet.public.lu). Beispiel 2: Projekt „4e plan de gestion des ressources en eau au Luxembourg (2027–2033)\" auf zesumme-vereinfachen.lu (Wasserwirtschaftsamt, Wasserrahmenrichtlinie). Die Bemerkung zum weiten Weg nach Luxemburg-Stadt ist eine Illustration der Moderatoren. Nur allgemeine Informationen. Überarbeitet am 26. November 2026 nach Rückmeldung des Teams von Zesumme Vereinfachen (Ministerium für Digitalisierung).*",
 "_lb": "*Quellen: Plattform „Zesumme Vereinfachen\", zesumme-vereinfachen.lu, an de Ministère fir Digitaliséierung (mindigital.gouvernement.lu) — déi participativ Plattform fir d'Verwaltungsvereinfachung, geréiert vum Vereinfachungsrot, lancéiert 2022 als Deel vum Programm „Einfach Lëtzebuerg\"; Bierger an Entreprisen kënnen Iddien araichen an un enger oder méi Projetsphasen deelhuelen, op Lëtzebuergesch, Däitsch, Franséisch oder Englesch; Ministèren kënnen och Projeten areechen. Beispill 1: Projet „Guichet de proximité\" op zesumme-vereinfachen.lu — ëffentlech Consultatioun vum Ministère fir Digitaliséierung (online, op Pabeier, an Atelieren a bei Stänn, ongeféier 8.000 Participanten), duerno en Opruff vum CTIE fir e mobille Guichet fir all Regioun; Pressekonferenz vum 1. Oktober 2024 (gouvernement.lu); „Guichet.lu on tour\" (guichet.public.lu). Beispill 2: Projet „4e plan de gestion des ressources en eau au Luxembourg (2027–2033)\" op zesumme-vereinfachen.lu (Administration de la gestion de l'eau, Waasserrahmendirektiv). Nëmmen allgemeng Informatiounen. Iwwerschafft den 26. November 2026 no der Réckmeldung vun der Ekipp vu Zesumme Vereinfachen (Ministère fir Digitaliséierung).*",
}

dry = "--dry" in sys.argv
for sfx in ["", "_fr", "_de", "_lb"]:
    p = f"podcast_script_zesumme{sfx}.md"
    lines = open(p, encoding="utf-8").read().split("\n")
    tidx = [i for i, l in enumerate(lines) if TURN.match(l)]
    assert len(tidx) == 61, (p, len(tidx), "already applied?")
    old = [lines[i] for i in tidx]
    fmt = {"A": None, "T": None}
    for l in old:  # keep the file's own label style (with or without space before the colon)
        m = re.match(r"^(\*\*(ANNA|TOM)\s?:\*\*\s?)", l)
        fmt["A" if m.group(2) == "ANNA" else "T"] = m.group(1)
    new = []
    for item in SEQ:
        if isinstance(item, int):
            new.append(old[item - 1])
        else:
            spk, texts = item
            t = texts[sfx]
            assert "..." not in t and "…" not in t, t
            new.append(fmt[spk] + t)
    # speakers must alternate except where the old file already had the same speaker twice
    spk = [re.match(r"^\*\*(ANNA|TOM)", l).group(1) for l in new]
    for a, b in zip(spk, spk[1:]):
        assert a != b, (p, "same speaker twice")
    out = lines[:tidx[0]] + new + lines[tidx[-1] + 1:]
    s = "\n".join(out)
    a, b = LENGTH[sfx]; assert s.count(a) == 1, (p, a); s = s.replace(a, b)
    src = [l for l in s.split("\n") if l.startswith("*Sources") or l.startswith("*Quellen")]
    assert len(src) == 1, (p, src); s = s.replace(src[0], SOURCES[sfx])
    if sfx == "":
        body = [l for l in new]
        assert "\n".join(body).count("Zesumme Vereinfachen") == 1  # EN: name said once only
    print(p, len(tidx), "->", len(new), "turns")
    if not dry:
        open(p, "w", encoding="utf-8").write(s)
