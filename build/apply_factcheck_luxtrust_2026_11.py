"""Fact-check LuxTrust (ep 2) + MyGuichet wording, 2 Nov 2026 — approved by Jacques ("make all changes").
1 data centres in the EU (luxtrust.com/en/security) · 2 summary safety line = line 121 (no 'access your devices')
3 'qualified' provider, since 2005 (luxtrust.com certifications / who-we-are) + summary wording
4 exact prices (order-product-private-use: app 47, Scan from 105, SmartCard from 129, 3 years)
5 identification in person at LuxTrust, a partner (bank) or notary, or by video (luxtrust.com/en/app)
6 app activation about 5 minutes (luxtrust.com activate) · 7 'most popular' -> 'simplest' (not on official pages), also MyGuichet
Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LT={
"en":[
 ("They are certified by the European Union, and they have been doing this for about twenty years.",
  "And they are officially recognised in the European Union as a 'qualified' provider. They have been doing this for more than twenty years — since 2005."),
 ("stored in data centres here, in Luxembourg.","stored in secure data centres in the European Union."),
 ("The first, and today the most popular — the LuxTrust Mobile app.","The first, and the simplest — the LuxTrust Mobile app."),
 ("As a rough idea, the app starts at around fifty euros for three years, and the physical devices cost a bit more.",
  "Right now, the app costs forty-seven euros for three years. The Scan starts at a hundred and five euros, and the SmartCard at a hundred and twenty-nine euros."),
 ("You can do this face-to-face, with one of their agents.","You can do this in person — at LuxTrust, at a partner such as your bank, or at a notary."),
 ("you activate it directly on your smartphone, following the guide.","you activate it directly on your smartphone, following the guide — it takes about five minutes."),
 ("from a European-certified provider.","from a provider recognised at European level."),
 ("never calls for sensitive data, never asks to access your devices.","never calls for sensitive data, and never comes to your home."),
],
"fr":[
 ("Ils sont certifiés par l'Union européenne, et ils font ça depuis une vingtaine d'années.",
  "Et ils sont officiellement reconnus dans l'Union européenne comme prestataire « qualifié ». Ils font ça depuis plus de vingt ans — depuis 2005."),
 ("stockées dans des centres de données ici, au Luxembourg.","stockées dans des centres de données sécurisés dans l'Union européenne."),
 ("Le premier, et aujourd'hui le plus populaire — l'appli LuxTrust Mobile.","Le premier, et le plus simple — l'appli LuxTrust Mobile."),
 ("Pour donner une idée, l'appli commence autour de cinquante euros pour trois ans, et les dispositifs physiques coûtent un peu plus.",
  "En ce moment, l'appli coûte quarante-sept euros pour trois ans. Le Scan commence à cent cinq euros, et la SmartCard à cent vingt-neuf euros."),
 ("Vous pouvez le faire en personne, avec un de leurs agents.","Vous pouvez le faire en personne — chez LuxTrust, chez un partenaire comme votre banque, ou chez un notaire."),
 ("vous l'activez directement sur votre smartphone, en suivant le guide.","vous l'activez directement sur votre smartphone, en suivant le guide — ça prend environ cinq minutes."),
 ("d'un prestataire certifié au niveau européen.","d'un prestataire reconnu au niveau européen."),
 ("n'appelle jamais pour des données sensibles, ne demande jamais à accéder à vos appareils.","n'appelle jamais pour des données sensibles, et ne vient jamais chez vous."),
],
"de":[
 ("Sie sind von der Europäischen Union zertifiziert, und sie machen das seit etwa zwanzig Jahren.",
  "Und sie sind in der Europäischen Union offiziell als „qualifizierter\" Anbieter anerkannt. Sie machen das seit mehr als zwanzig Jahren — seit 2005."),
 ("in Rechenzentren hier in Luxemburg gespeichert.","in sicheren Rechenzentren in der Europäischen Union gespeichert."),
 ("Das erste, und heute das beliebteste — die LuxTrust-Mobile-App.","Das erste, und das einfachste — die LuxTrust-Mobile-App."),
 ("Als grobe Vorstellung: Die App beginnt bei etwa fünfzig Euro für drei Jahre, und die physischen Geräte kosten ein bisschen mehr.",
  "Im Moment kostet die App siebenundvierzig Euro für drei Jahre. Der Scan beginnt bei hundertfünf Euro, und die SmartCard bei hundertneunundzwanzig Euro."),
 ("Das können Sie persönlich machen, mit einem ihrer Mitarbeiter.","Das können Sie persönlich machen — bei LuxTrust, bei einem Partner wie Ihrer Bank, oder bei einem Notar."),
 ("indem Sie der Anleitung folgen.","indem Sie der Anleitung folgen — das dauert etwa fünf Minuten."),
 ("von einem europäisch zertifizierten Anbieter.","von einem europaweit anerkannten Anbieter."),
 ("ruft niemals wegen sensibler Daten an, fragt niemals nach Zugang zu Ihren Geräten.","ruft niemals wegen sensibler Daten an, und kommt niemals zu Ihnen nach Hause."),
],
"lb":[
 ("Si sinn vun der Europäescher Unioun zertifizéiert, a si maachen dat scho ronn zwanzeg Joer.",
  "A si sinn an der Europäescher Unioun offiziell als \"qualifizéierte\" Provider unerkannt. Si maachen dat scho méi wéi zwanzeg Joer — zënter 2005."),
 ("gespäichert an Datenzentren hei, zu Lëtzebuerg.","gespäichert a sécheren Datenzentren an der Europäescher Unioun."),
 ("Dat éischt, an haut dat populärst — d'LuxTrust Mobile App.","Dat éischt, an dat einfachst — d'LuxTrust Mobile App."),
 ("Als groff Iddi, d'App fänkt bei ronn fofzeg Euro fir dräi Joer un, an déi physesch Apparater kaschten e bësse méi.",
  "Momentan kascht d'App siwenavéierzeg Euro fir dräi Joer. De Scan fänkt bei honnertfënnef Euro un, an d'SmartCard bei honnertnénganzwanzeg Euro."),
 ("Dir kënnt dat vis-à-vis maachen, mat engem vun hiren Agenten.","Dir kënnt dat perséinlech maachen — bei LuxTrust, bei engem Partner wéi Ärer Bank, oder bei engem Notaire."),
 ("andeem Dir dem Guide follegt.","andeem Dir dem Guide follegt — dat dauert ongeféier fënnef Minutten."),
 ("vun engem europäesch zertifizéierte Provider.","vun engem op europäeschem Niveau unerkannte Provider."),
 ("rifft ni un fir sensibel Donnéeën, freet ni fir Zougang zu Ären Apparater.","rifft ni un fir sensibel Donnéeën, a kënnt ni bei Iech heem."),
],
}
MG={"en":[("The most popular product is LuxTrust Mobile","The simplest product is LuxTrust Mobile")],
    "fr":[("Le produit le plus populaire est LuxTrust Mobile","Le produit le plus simple est LuxTrust Mobile")],
    "de":[("Das beliebteste Produkt ist LuxTrust Mobile","Das einfachste Produkt ist LuxTrust Mobile")],
    "lb":[("Dat populäerst Produkt ass LuxTrust Mobile","Dat einfachst Produkt ass LuxTrust Mobile")]}
SRC_OLD="General information only"
SRC_ADD="Also: luxtrust.com/en/security, /certifications, /about-us/who-we-are, /app, /order-product-private-use (prices checked 2 November 2026). "
def apply(key,table):
    for lang,reps in table.items():
        p=os.path.join(ROOT,f"podcast_script_{key}"+("" if lang=="en" else "_"+lang)+".md")
        s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
        for old,new in reps:
            if new in s: continue
            assert s.count(old)==1,(key,lang,old)
            s=s.replace(old,new)
        assert s.count("\n**")==n0
        if key=="luxtrust" and lang=="en" and SRC_ADD not in s:
            assert s.count(SRC_OLD)==1; s=s.replace(SRC_OLD,SRC_ADD+SRC_OLD)
        open(p,"w",encoding="utf-8").write(s); print("ok",key,lang)
apply("luxtrust",LT); apply("myguichet",MG)
