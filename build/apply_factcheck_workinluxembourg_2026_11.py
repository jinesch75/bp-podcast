"""Fact-check Work in Luxembourg (ep 6), 2 Nov 2026 — Jacques: "apply all".
1 'Live here' = safety & stability, healthcare, education, family, culture & lifestyle (housing is under 'Get started')
2 '~11,000 candidates' no longer published -> profiles pre-screened by ADEM (adem.public.lu wil-emp, 16.01.2026)
3 Job Board focuses on shortage occupations; other jobs -> EURES (workinluxembourg.com/get-started/job-search)
4 durable figures (Jacques: no numbers that go stale): three quarters / more than 200,000 / 'among the safest' / 'among the very best'
5 shortage jobs: no local search first, ADEM green light within a few days (gouvernement.lu 27.03.2026: 5 working days)
Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[
 ("Housing, family, education, healthcare, culture, leisure — and","Safety and stability, healthcare, education, family life, culture and leisure — and"),
 ("apply directly to vacancies.","apply directly to vacancies. It focuses on the professions where Luxembourg most needs people. For jobs in all other sectors, the site points you to the European job portal, EURES."),
 ("In fact, the platform already has around eleven thousand candidates from all over the world, pre-selected by ADEM.","Every profile is pre-screened by ADEM, and employers search the database and contact candidates directly."),
 ("**ANNA:** Eleven thousand. So","**ANNA:** Pre-screened by ADEM. So"),
 ("can mean faster immigration procedures.","can mean faster immigration procedures. The employer doesn't first have to look for someone locally, so ADEM gives the green light within a few days."),
 ("according to the Legatum Prosperity Index, Luxembourg is ranked the number one safest country for expats. According to the IMD World Talent Ranking, it's second in the world for attracting talent.",
  "the Legatum Prosperity Index ranks Luxembourg among the safest countries for expats. And the IMD World Talent Ranking puts it among the very best in the world for attracting talent."),
 ("That around seventy-four percent of Luxembourg's workforce","That around three quarters of Luxembourg's workforce"),
 ("And more than two hundred and twenty-eight thousand people","And more than two hundred thousand people"),
 ("**ANNA:** Seventy-four percent. So","**ANNA:** Three quarters. So"),
],
"fr":[
 ("Le logement, la famille, l'éducation, la santé, la culture, les loisirs — et","La sécurité et la stabilité, la santé, l'éducation, la vie de famille, la culture et les loisirs — et"),
 ("postuler directement aux offres.","postuler directement aux offres. Il se concentre sur les métiers où le Luxembourg a le plus besoin de personnes. Pour les emplois dans tous les autres secteurs, le site vous renvoie vers le portail européen de l'emploi, EURES."),
 ("En fait, la plateforme compte déjà environ onze mille candidats venus du monde entier, présélectionnés par l'ADEM.","Chaque profil est présélectionné par l'ADEM, et les employeurs consultent la base de données et contactent directement les candidats."),
 ("**ANNA :** Onze mille. Donc","**ANNA :** Présélectionnés par l'ADEM. Donc"),
 ("des démarches d'immigration plus rapides.","des démarches d'immigration plus rapides. L'employeur n'a pas d'abord à chercher quelqu'un sur place, donc l'ADEM donne son feu vert en quelques jours."),
 ("selon le Legatum Prosperity Index, le Luxembourg est classé pays le plus sûr au monde pour les expatriés. Selon l'IMD World Talent Ranking, il est deuxième au monde pour attirer les talents.",
  "le Legatum Prosperity Index classe le Luxembourg parmi les pays les plus sûrs pour les expatriés. Et l'IMD World Talent Ranking le place parmi les meilleurs au monde pour attirer les talents."),
 ("Qu'environ soixante-quatorze pour cent de la population active","Qu'environ trois quarts de la population active"),
 ("Et plus de deux cent vingt-huit mille personnes","Et plus de deux cent mille personnes"),
 ("**ANNA :** Soixante-quatorze pour cent. Donc","**ANNA :** Trois quarts. Donc"),
],
"de":[
 ("Wohnen, Familie, Bildung, Gesundheitsversorgung, Kultur, Freizeit — und","Sicherheit und Stabilität, Gesundheitsversorgung, Bildung, Familienleben, Kultur und Freizeit — und"),
 ("direkt auf offene Stellen bewerben.","direkt auf offene Stellen bewerben. Es konzentriert sich auf die Berufe, in denen Luxemburg am dringendsten Menschen braucht. Für Jobs in allen anderen Branchen verweist die Website auf das europäische Jobportal EURES."),
 ("Tatsächlich hat die Plattform bereits rund elftausend Kandidatinnen und Kandidaten aus aller Welt, die von ADEM vorausgewählt wurden.","Jedes Profil wird von ADEM vorab geprüft, und Arbeitgeber durchsuchen die Datenbank und kontaktieren Kandidaten direkt."),
 ("**ANNA:** Elftausend. Es ist","**ANNA:** Von ADEM vorab geprüft. Es ist"),
 ("schnellere Einwanderungsverfahren bedeuten.","schnellere Einwanderungsverfahren bedeuten. Der Arbeitgeber muss nicht zuerst vor Ort nach jemandem suchen, und so gibt ADEM innerhalb weniger Tage grünes Licht."),
 ("laut dem Legatum Prosperity Index ist Luxemburg das sicherste Land für Expats, auf Platz eins. Laut dem IMD World Talent Ranking ist es weltweit das zweitbeste Land, wenn es darum geht, Talente anzuziehen.",
  "der Legatum Prosperity Index zählt Luxemburg zu den sichersten Ländern für Expats. Und das IMD World Talent Ranking zählt es weltweit zu den besten Ländern, wenn es darum geht, Talente anzuziehen."),
 ("Dass rund vierundsiebzig Prozent der","Dass rund drei Viertel der"),
 ("Und mehr als zweihundertachtundzwanzigtausend Menschen","Und mehr als zweihunderttausend Menschen"),
 ("**ANNA:** Vierundsiebzig Prozent. In","**ANNA:** Drei Viertel. In"),
],
"lb":[
 ("Wunnen, Famill, Schoul, Gesondheet, Kultur, Fräizäit — an","Sécherheet a Stabilitéit, Gesondheet, Schoul, Familljeliewen, Kultur a Fräizäit — an"),
 ("dech direkt op fräi Stellen umellen.","dech direkt op fräi Stellen umellen. Et konzentréiert sech op d'Beruffer, wou Lëtzebuerg am meeschte Leit brauch. Fir Jobs an allen anere Secteuren verweist de Site op den europäesche Jobportal EURES."),
 ("Tatsächlech huet d'Plattform schonn ongeféier eelefdausend Kandidaten aus der ganzer Welt, virausgewielt vun der ADEM.","All Profil gëtt vun der ADEM virdrun iwwerpréift, an d'Patronen duerchsichen d'Datebank a kontaktéieren d'Kandidaten direkt."),
 ("**ANNA:** Eelefdausend. Also","**ANNA:** Vun der ADEM iwwerpréift. Also"),
 ("méi séier Immigratiounsprozeduren bedeiten.","méi séier Immigratiounsprozeduren bedeiten. De Patron muss net fir d'éischt hei am Land no engem sichen, an esou gëtt d'ADEM bannent e puer Deeg gréng Luucht."),
 ("laut dem Legatum Prosperity Index ass Lëtzebuerg als dat séchersst Land fir Expats op der Nummer eent gerankt. Laut dem IMD World Talent Ranking ass et weltwäit op der zweeter Plaz, fir Talenter unzéien.",
  "de Legatum Prosperity Index zielt Lëtzebuerg zu de sécherste Länner fir Expats. An den IMD World Talent Ranking zielt et weltwäit zu de beschten, fir Talenter unzéien."),
 ("Datt ongeféier véieransiwwenzeg Prozent vun de","Datt ongeféier dräi Véierel vun de"),
 ("A méi wéi zweehonnertaachtanzwanzegdausend Leit","A méi wéi zweehonnertdausend Leit"),
 ("**ANNA:** Véieransiwwenzeg Prozent. Also","**ANNA:** Dräi Véierel. Also"),
],
}
SRC_OLD="(around 11,000 candidates pre-selected by ADEM; vacancies updated daily)"
SRC_NEW="(all profiles pre-screened by ADEM; vacancies updated daily; it focuses on shortage occupations, other jobs via EURES)"
FIG_OLD="Selected figures as published on the site:"
FIG_NEW="Figures are given in rounded, durable form (fact-checked 2 November 2026). As published on the site then:"
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_workinluxembourg"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new in s: continue
        assert s.count(old)==1,(lang,old); s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en":
        if SRC_NEW not in s: assert s.count(SRC_OLD)==1; s=s.replace(SRC_OLD,SRC_NEW)
        if FIG_NEW not in s: assert s.count(FIG_OLD)==1; s=s.replace(FIG_OLD,FIG_NEW)
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
