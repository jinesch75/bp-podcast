"""Fact-check MyGuichet (ep 1), 2 Nov 2026 — approved by Jacques ("all three").
1) business part: VAT returns are filed on eCDF, not MyGuichet -> staff/social security, VAT account, business permit
2) help: new AI assistant on Guichet.lu (gouvernement.lu, 6 July 2026)
3) eID card: can be used with a smartphone via the GouvID app (ctie.gouvernement.lu)
Turn counts unchanged (text added inside existing turns). Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[
 ("for things like tax and VAT declarations, social security declarations for their staff, or applying for permits and licences.",
  "for things like declaring their staff to social security, checking their VAT account, or applying for a business permit."),
 ("with the certificates activated. Or, and this",
  "with the certificates activated. And you can even use it with your smartphone, through the government's GouvID app. Or, and this"),
 ("many tutorials are available, and a helpdesk.",
  "many tutorials are available, and a helpdesk. And on Guichet.lu there's now an AI assistant: you type your question in your own words, in your own language, and it helps you find the right procedure."),
],
"fr":[
 ("pour des choses comme les déclarations d'impôts et de TVA, les déclarations de sécurité sociale pour leur personnel, ou les demandes de permis et d'autorisations.",
  "pour des choses comme déclarer leur personnel à la sécurité sociale, consulter leur compte TVA, ou demander une autorisation d'établissement."),
 ("avec les certificats activés. Ou alors",
  "avec les certificats activés. Et vous pouvez même l'utiliser avec votre smartphone, grâce à l'application GouvID de l'État. Ou alors"),
 ("ainsi qu'un service d'assistance.",
  "ainsi qu'un service d'assistance. Et sur Guichet.lu, il y a maintenant un assistant d'intelligence artificielle : vous tapez votre question avec vos propres mots, dans votre langue, et il vous aide à trouver la bonne démarche."),
],
"de":[
 ("für Dinge wie Steuer- und Mehrwertsteuererklärungen, Sozialversicherungserklärungen für ihr Personal, oder die Beantragung von Genehmigungen und Lizenzen.",
  "für Dinge wie die Anmeldung ihres Personals bei der Sozialversicherung, den Blick auf ihr Mehrwertsteuerkonto, oder den Antrag auf eine Niederlassungsgenehmigung."),
 ("mit aktivierten Zertifikaten haben. Oder, und das",
  "mit aktivierten Zertifikaten haben. Und Sie können ihn sogar mit Ihrem Smartphone nutzen, über die App GouvID des Staates. Oder, und das"),
 ("gibt es viele Tutorials, und einen Helpdesk.",
  "gibt es viele Tutorials, und einen Helpdesk. Und auf Guichet.lu gibt es jetzt einen KI-Assistenten: Sie tippen Ihre Frage in Ihren eigenen Worten ein, in Ihrer Sprache, und er hilft Ihnen, das richtige Verfahren zu finden."),
],
"lb":[
 ("fir Saache wéi Steier- an TVA-Deklaratiounen, Sozialversécherungsdeklaratioune fir hir Mataarbechter, oder fir Autorisatiounen a Lizenzen ze froen.",
  "fir Saache wéi hir Mataarbechter bei der Sozialversécherung unzemellen, hire TVA-Kont ze kucken, oder eng Autorisation d'établissement ze froen."),
 ("mat aktivéierten Zertifikater hutt. Oder, an dat",
  "mat aktivéierten Zertifikater hutt. An Dir kënnt se souguer mat Ärem Smartphone benotzen, iwwer d'App GouvID vum Staat. Oder, an dat"),
 ("gëtt et vill Tutorialen, an en Helpdesk.",
  "gëtt et vill Tutorialen, an en Helpdesk. An op Guichet.lu gëtt et elo en KI-Assistent: Dir tippt Är Fro an Ären eegene Wierder, an Ärer Sprooch, an hien hëlleft Iech, déi richteg Prozedur ze fannen."),
],
}
SRC={"en":"*Source: guichet.public.lu/en/citoyens/myguichet.html and the MyGuichet.lu help pages.*"}
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_myguichet"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new in s: continue
        assert s.count(old)==1,(lang,old)
        s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en" and "ctie.gouvernement.lu" not in s:
        s=s.replace(SRC["en"],"*Sources: guichet.public.lu/en/citoyens/myguichet.html and the MyGuichet.lu help pages; guichet.public.lu (VAT return via eCDF, CCSS employer services, business permit); gouvernement.lu (AI on Guichet.lu, 6 July 2026); ctie.gouvernement.lu (GouvID). Fact-checked 2 November 2026.*")
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
