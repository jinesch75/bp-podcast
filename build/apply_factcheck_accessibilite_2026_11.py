"""Fact-check Accessibility (ep 11), 9 Nov 2026 — Jacques: "apply all".
1 complaint procedure: organisation first (contact in accessibility declaration), then SIP (answers within a month) or Ombudsman (accessibilite.public.lu/fr/tools/reclamations.html)
2 OSAPS reporting also by phone, e-mail, WhatsApp photo (accessibilite-produits-services.public.lu signaler) — no numbers
3 aid: plan compliance check first; works finished by 1 July 2031 (accessibilite-infrastructure; guichet.lu)
4 new collective housing: 10% of homes accessible (guichet.lu)
Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[
 ("Every site must give you a way to report a barrier. They have to answer you, normally within one month. And if you're not satisfied, you can turn to the State information service, or even the ombudsman — the médiateur.",
  "First, you contact the organisation, using the contact details in its accessibility declaration. If that doesn't help, you can turn to the State information and press service, the SIP, which checks accessibility and answers within a month — or to the ombudsman, the médiateur."),
 ("and collective housing — buildings with many homes inside.","and collective housing — in new apartment buildings, one home in ten must be accessible."),
 ("if you apply before July 2028.","if you apply before July 2028. The plans need a compliance check first, and the works must be finished by July 2031."),
 ("And you can even do it without logging in, if you prefer.","And you can even do it without logging in, if you prefer. Or by phone, or by email — or you can simply send a photo by WhatsApp, for example of a ticket machine that doesn't work for you."),
],
"fr":[
 ("Chaque site doit vous donner un moyen de signaler un obstacle. Ils doivent vous répondre, normalement dans un délai d'un mois. Et si vous n'êtes pas satisfait, vous pouvez vous tourner vers le service information de l'État, ou même vers l'ombudsman — le médiateur.",
  "D'abord, vous contactez l'organisme, avec les coordonnées indiquées dans sa déclaration d'accessibilité. Si ça n'aide pas, vous pouvez vous tourner vers le Service information et presse de l'État, le SIP, qui contrôle l'accessibilité et répond dans un délai d'un mois — ou vers l'ombudsman, le médiateur."),
 ("et le logement collectif — les immeubles avec beaucoup d'habitations à l'intérieur.","et le logement collectif — dans les nouveaux immeubles d'habitation, un logement sur dix doit être accessible."),
 ("si vous faites la demande avant juillet 2028.","si vous faites la demande avant juillet 2028. Les plans doivent d'abord passer un contrôle de conformité, et les travaux doivent être terminés avant juillet 2031."),
 ("Et vous pouvez même le faire sans vous connecter, si vous préférez.","Et vous pouvez même le faire sans vous connecter, si vous préférez. Ou par téléphone, ou par e-mail — ou vous pouvez simplement envoyer une photo par WhatsApp, par exemple d'un distributeur de billets qui ne fonctionne pas pour vous."),
],
"de":[
 ("Jede Seite muss Ihnen eine Möglichkeit geben, ein Hindernis zu melden. Sie müssen Ihnen antworten, normalerweise innerhalb eines Monats. Und wenn Sie nicht zufrieden sind, können Sie sich an den Informationsdienst des Staates wenden, oder sogar an den Ombudsmann — den Mediateur.",
  "Zuerst wenden Sie sich an die Stelle selbst, mit den Kontaktdaten aus ihrer Barrierefreiheitserklärung. Wenn das nicht hilft, können Sie sich an den Informations- und Pressedienst des Staates wenden, den SIP, der die Barrierefreiheit kontrolliert und innerhalb eines Monats antwortet — oder an den Ombudsmann, den Mediateur."),
 ("und kollektiven Wohnraum — Gebäude mit vielen Wohnungen darin.","und kollektiven Wohnraum — in neuen Mehrfamilienhäusern muss jede zehnte Wohnung barrierefrei sein."),
 ("wenn Sie den Antrag vor Juli 2028 stellen.","wenn Sie den Antrag vor Juli 2028 stellen. Die Pläne müssen vorher auf Konformität geprüft werden, und die Arbeiten müssen bis Juli 2031 fertig sein."),
 ("Und Sie können es sogar ohne Anmeldung tun, wenn Sie möchten.","Und Sie können es sogar ohne Anmeldung tun, wenn Sie möchten. Oder per Telefon, oder per E-Mail — oder Sie schicken einfach ein Foto per WhatsApp, zum Beispiel von einem Fahrkartenautomaten, der für Sie nicht funktioniert."),
],
"lb":[
 ("All Säit muss der eng Manéier ginn, fir en Hindernis ze mellen. Si mussen der äntweren, normalerweis bannent engem Mount. A wann s du net zefridde bass, kanns du dech un den Informatiounsdéngscht vum Staat wenden, oder souguer un den Ombudsman — de Mediateur.",
  "Fir d'éischt kontaktéiers du d'Organisatioun selwer, mat de Kontaktdaten aus hirer Accessibilitéitserklärung. Wann dat net hëlleft, kanns du dech un den Informatiouns- a Pressedéngscht vum Staat wenden, de SIP, deen d'Accessibilitéit kontrolléiert a bannent engem Mount äntwert — oder un den Ombudsman, de Mediateur."),
 ("a Kollektivwunnengen — Gebaier mat ville Wunnengen dran.","a Kollektivwunnengen — an neie Residenzen muss all zéngt Wunneng accessibel sinn."),
 ("wann s du den Demande virum Juli 2028 mëss.","wann s du den Demande virum Juli 2028 mëss. D'Pläng mussen éischt op Konformitéit gepréift ginn, an d'Aarbechte mussen bis Juli 2031 fäerdeg sinn."),
 ("An du kanns et souguer maachen, ouni dech anzelaggen, wann s du léiwer wëlls.","An du kanns et souguer maachen, ouni dech anzelaggen, wann s du léiwer wëlls. Oder per Telefon, oder per E-Mail — oder du schécks einfach eng Foto iwwer WhatsApp, zum Beispill vun engem Billjeesautomat, deen net fir dech funktionéiert."),
],
}
SRC_OLD="General information only — check accessibilite.lu"
SRC_ADD="Fact-checked 9 November 2026 (complaint procedure: organisation first, then SIP — reply within one month — or Ombudsman; OSAPS reporting by MyGuichet.lu, form, phone, e-mail, WhatsApp, post; financial aid: 50%, max. EUR 24,000, apply by 1 July 2028, works by 1 July 2031, plan compliance check first; 10% of homes in new collective buildings accessible). "
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_accessibilite"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new in s: continue
        assert s.count(old)==1,(lang,old); s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en" and SRC_ADD not in s:
        assert s.count(SRC_OLD)==1; s=s.replace(SRC_OLD,SRC_ADD+SRC_OLD)
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
