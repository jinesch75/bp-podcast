"""Fact-check Volunteering (ep 3), 2 Nov 2026 — approved by Jacques ("all three").
1 smart matching also sends suggestions by email (benevolat.lu news 01.06.2026)
2 add the 12th field 'Association board' (benevolat.lu field list; board-participation campaign)
3 EN: 'International Volunteer Day' (UN name). Turn counts unchanged. Idempotent."""
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R={
"en":[("missions that could be of interest to you.","missions that could be of interest to you — it even sends them to you by email."),
      ("Animals. Emergency relief. For example,","Animals. Emergency relief. And even helping to run an association, by joining its board. For example,"),
      ("an International Volunteering Day every year","an International Volunteer Day every year")],
"fr":[("des missions qui pourraient vous intéresser.","des missions qui pourraient vous intéresser — il vous les envoie même par e-mail."),
      ("Les secours d'urgence. Par exemple,","Les secours d'urgence. Et même aider à faire tourner une association, en entrant dans son conseil d'administration. Par exemple,")],
"de":[("Einsätze vor, die Sie interessieren könnten.","Einsätze vor, die Sie interessieren könnten — es schickt sie Ihnen sogar per E-Mail."),
      ("Tiere. Nothilfe. Zum Beispiel:","Tiere. Nothilfe. Und sogar mithelfen, einen Verein zu führen, indem man in seinen Vorstand geht. Zum Beispiel:")],
"lb":[("Missiounen, déi Iech kéinten interesséieren.","Missiounen, déi Iech kéinten interesséieren — e schéckt Iech se souguer per E-Mail."),
      ("Déieren. Noutfallhëllef. Zum Beispill:","Déieren. Noutfallhëllef. An och hëllefen, e Veräin ze féieren, andeem een a säi Comité geet. Zum Beispill:")],
}
SRC_ADD=" Fact-checked 2 November 2026 (benevolat.lu smart matching 01.06.2026, field list; STATEC Regards 10/24)."
for lang,reps in R.items():
    p=os.path.join(ROOT,"podcast_script_benevolat"+("" if lang=="en" else "_"+lang)+".md")
    s=open(p,encoding="utf-8").read(); n0=s.count("\n**")
    for old,new in reps:
        if new in s: continue
        assert s.count(old)==1,(lang,old); s=s.replace(old,new)
    assert s.count("\n**")==n0
    if lang=="en" and SRC_ADD not in s:
        s=s.rstrip("\n"); assert s.endswith("volontaires.lu.*"); s=s[:-1]+SRC_ADD+"*\n"
    open(p,"w",encoding="utf-8").write(s); print("ok",lang)
