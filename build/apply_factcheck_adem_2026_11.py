"""Fact-check ADEM (ep 13), 9 Nov 2026 — Jacques: "apply all".
1 scams: fake e-mails / social-media accounts, phishing for personal details (ADEM alerts 02.10.2026, 09.09.2026)
2 login: LuxTrust or Luxembourg eID (guichet.lu)
3 unemployment benefit: letter from ADEM, then complete the application on MyGuichet.lu (adem.public.lu 10.11.2025)
4 Youth Guarantee: monthly meeting with counsellor in the first six months (adem.public.lu)
5 Club Emploi: CV and cover letter, CV photo, group workshops (adem.public.lu)
Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[
 ("like a LuxTrust product.","like a LuxTrust product, or your Luxembourg electronic ID card."),
 ("There you can use computers and get help preparing your CV.","There you can use computers, get help with your CV and cover letter, even have a photo taken for your CV, and join group workshops."),
 ("Recently, applying for unemployment benefit became fully online.","If you meet the conditions, ADEM sends you a letter, and you complete your application online, on MyGuichet.lu."),
 ("within four months of registering with ADEM.","within four months of registering with ADEM. And during the first six months, you meet your personal counsellor every month."),
 ("Sometimes scammers send fake emails pretending to be ADEM, and they ask for money for a job or a visa.","Sometimes scammers send fake emails or create fake social-media accounts pretending to be ADEM. They ask for money for a job or a visa — or they ask you to click a link and confirm your personal details."),
 ("If anyone asks you for payment in ADEM's name, it is a scam. Don't pay, and don't share your details.","If anyone asks you for payment or personal details in ADEM's name, it is a scam. Don't pay, don't click, and check ADEM's official channels on its website."),
],
"fr":[
 ("comme un produit LuxTrust.","comme un produit LuxTrust, ou votre carte d'identité électronique luxembourgeoise."),
 ("Là, vous pouvez utiliser des ordinateurs et recevoir de l'aide pour préparer votre CV.","Là, vous pouvez utiliser des ordinateurs, recevoir de l'aide pour votre CV et votre lettre de motivation, même faire prendre une photo pour votre CV, et participer à des ateliers en groupe."),
 ("Récemment, la demande d'indemnité de chômage est devenue entièrement en ligne.","Si vous remplissez les conditions, l'ADEM vous envoie un courrier, et vous complétez votre demande en ligne, sur MyGuichet.lu."),
 ("dans les quatre mois suivant l'inscription à l'ADEM.","dans les quatre mois suivant l'inscription à l'ADEM. Et pendant les six premiers mois, vous rencontrez votre conseiller personnel tous les mois."),
 ("Parfois, des escrocs envoient de faux courriels en se faisant passer pour l'ADEM, et ils demandent de l'argent pour un emploi ou un visa.","Parfois, des escrocs envoient de faux courriels ou créent de faux comptes sur les réseaux sociaux en se faisant passer pour l'ADEM. Ils demandent de l'argent pour un emploi ou un visa — ou ils vous demandent de cliquer sur un lien et de confirmer vos données personnelles."),
 ("Si quelqu'un vous demande un paiement au nom de l'ADEM, c'est une arnaque. Ne payez pas, et ne communiquez pas vos données.","Si quelqu'un vous demande un paiement ou des données personnelles au nom de l'ADEM, c'est une arnaque. Ne payez pas, ne cliquez pas, et vérifiez les canaux officiels de l'ADEM sur son site."),
],
"de":[
 ("wie ein LuxTrust-Produkt.","wie ein LuxTrust-Produkt, oder Ihren luxemburgischen elektronischen Personalausweis."),
 ("Dort können Sie Computer nutzen und Hilfe bei der Erstellung Ihres Lebenslaufs bekommen.","Dort können Sie Computer nutzen, Hilfe bei Lebenslauf und Anschreiben bekommen, sogar ein Foto für Ihren Lebenslauf machen lassen, und an Gruppenworkshops teilnehmen."),
 ("Seit Kurzem ist der Antrag auf Arbeitslosengeld vollständig online.","Wenn Sie die Bedingungen erfüllen, schickt Ihnen die ADEM einen Brief, und Sie vervollständigen Ihren Antrag online, auf MyGuichet.lu."),
 ("innerhalb von vier Monaten nach der Anmeldung bei der ADEM.","innerhalb von vier Monaten nach der Anmeldung bei der ADEM. Und in den ersten sechs Monaten treffen Sie Ihren persönlichen Berater jeden Monat."),
 ("Manchmal senden Betrüger gefälschte E-Mails und geben vor, die ADEM zu sein, und sie verlangen Geld für einen Job oder ein Visum.","Manchmal senden Betrüger gefälschte E-Mails oder erstellen gefälschte Konten in sozialen Netzwerken und geben vor, die ADEM zu sein. Sie verlangen Geld für einen Job oder ein Visum — oder sie bitten Sie, auf einen Link zu klicken und Ihre persönlichen Daten zu bestätigen."),
 ("Wenn jemand Sie im Namen der ADEM um eine Zahlung bittet, ist das Betrug. Zahlen Sie nicht und geben Sie Ihre Daten nicht weiter.","Wenn jemand Sie im Namen der ADEM um eine Zahlung oder persönliche Daten bittet, ist das Betrug. Zahlen Sie nicht, klicken Sie nicht, und prüfen Sie die offiziellen Kanäle der ADEM auf ihrer Website."),
],
"lb":[
 ("wéi e LuxTrust-Produkt.","wéi e LuxTrust-Produkt, oder deng Lëtzebuerger elektronesch Identitéitskaart."),
 ("Do kanns du Computere benotzen an Hëllef kréien, fir däi CV virzebereeden.","Do kanns du Computere benotzen, Hëllef bei dengem CV an dengem Motivatiounsbréif kréien, souguer eng Foto fir de CV maache loossen, an u Gruppenworkshoppen deelhuelen."),
 ("Zënter kuerzem ass d'Ufro fir d'Aarbechtslosegeld komplett online.","Wann s du d'Konditiounen erfëlls, schéckt d'ADEM der e Bréif, an du fëlls deng Demande online aus, op MyGuichet.lu."),
 ("bannent véier Méint nodeems s du dech bei der ADEM ugemellt hues.","bannent véier Méint nodeems s du dech bei der ADEM ugemellt hues. An an den éischte sechs Méint gesäis du däi perséinleche Beroder all Mount."),
 ("Heiansdo schécken Escroke falsch E-Maile, déi virgewen, d'ADEM ze sinn, a si froen no Suen fir e Job oder e Visa.","Heiansdo schécken Escroke falsch E-Mailen oder maache falsch Konten op de soziale Netzwierker, déi virgi, d'ADEM ze sinn. Si froen no Suen fir e Job oder e Visa — oder si froen dech, op e Link ze klicken an deng perséinlech Donnéeën ze bestätegen."),
 ("Wann iech iergendeen am Numm vun der ADEM no enger Bezuelung freet, ass et e Bedruch. Bezuelt net, an deelt Är Donnéeën net.","Wann iergendeen dech am Numm vun der ADEM no enger Bezuelung oder no perséinlechen Donnéeë freet, ass et e Bedruch. Bezuel net, klick net, a kuck d'offiziell Kanäl vun der ADEM op hirer Websäit no."),
],
}
SRC_OLD="General information only — for your personal situation"
SRC_ADD="Fact-checked 9 November 2026 (ADEM phishing alert 02.10.2026 and fake social-media accounts 09.09.2026; unemployment benefit application via MyGuichet.lu after ADEM's letter; Youth Guarantee monthly counsellor meetings; Club Emploi; login with LuxTrust or eID per Guichet.lu). "
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_adem"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new in s: continue
        assert s.count(old)==1,(lang,old); s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en" and SRC_ADD not in s:
        assert s.count(SRC_OLD)==1; s=s.replace(SRC_OLD,SRC_ADD+SRC_OLD)
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
