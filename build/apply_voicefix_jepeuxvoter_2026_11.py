#!/usr/bin/env python3
"""Voice fix, I can vote (20 Nov 2026): very short lines flagged by voice_qc.py ("Not in all three.",
"There are three of them.", "There are two ways.", "They are.") joined to the next sentence, EN/FR/DE/LB.
Turn counts unchanged. Idempotent. Run from the project root."""
R = {
 "": [
  ("There are three main ones. The municipal elections, for the council of your commune. The European elections, for the European Parliament. And the national elections, for the Chamber of Deputies.",
   "There are three main ones: the municipal elections, for the council of your commune, the European elections, for the European Parliament, and the national elections, for the Chamber of Deputies."),
  ("Not in all three. The national elections are only", "Not in all three, because the national elections are only"),
  ("There are three of them. You are at least eighteen on election day. You live in Luxembourg. And you have not lost",
   "There are three conditions: you are at least eighteen on election day, you live in Luxembourg, and you have not lost"),
  ("There are two ways. The first one is online,", "There are two ways, and the first one is online,"),
  ("They are. You can simply go", "They are, and you can simply go"),
 ],
 "_fr": [
  ("Il y en a trois principales. Les élections communales, pour le conseil de votre commune. Les élections européennes, pour le Parlement européen. Et les élections nationales, pour la Chambre des députés.",
   "Il y en a trois principales : les élections communales, pour le conseil de votre commune, les élections européennes, pour le Parlement européen, et les élections nationales, pour la Chambre des députés."),
  ("Pas aux trois. Les élections nationales sont réservées", "Pas aux trois, car les élections nationales sont réservées"),
  ("Il y en a trois. Vous avez au moins dix-huit ans le jour des élections. Vous habitez au Luxembourg. Et vous n'avez pas perdu",
   "Il y a trois conditions : vous avez au moins dix-huit ans le jour des élections, vous habitez au Luxembourg, et vous n'avez pas perdu"),
  ("Il y a deux possibilités. La première, c'est en ligne,", "Il y a deux possibilités, et la première, c'est en ligne,"),
  ("Oui, elles le sont. Vous pouvez simplement", "Oui, et vous pouvez simplement"),
 ],
 "_de": [
  ("Es gibt drei wichtige Wahlen. Die Gemeindewahlen, für den Rat Ihrer Gemeinde. Die Europawahlen, für das Europäische Parlament. Und die Nationalwahlen, für die Abgeordnetenkammer.",
   "Es gibt drei wichtige Wahlen: die Gemeindewahlen, für den Rat Ihrer Gemeinde, die Europawahlen, für das Europäische Parlament, und die Nationalwahlen, für die Abgeordnetenkammer."),
  ("Nicht bei allen drei. Die Nationalwahlen sind nur", "Nicht bei allen drei, denn die Nationalwahlen sind nur"),
  ("Es sind drei. Sie sind am Wahltag mindestens achtzehn Jahre alt. Sie wohnen in Luxemburg. Und Sie haben Ihr Wahlrecht",
   "Es sind drei Bedingungen: Sie sind am Wahltag mindestens achtzehn Jahre alt, Sie wohnen in Luxemburg, und Sie haben Ihr Wahlrecht"),
  ("Es gibt zwei Wege. Der erste ist online,", "Es gibt zwei Wege, und der erste ist online,"),
  ("Ja, das sind sie. Sie können einfach hingehen", "Ja, und Sie können einfach hingehen"),
 ],
 "_lb": [
  ("Et ginn dräi wichteg Walen. D'Gemengewalen, fir de Rot vun Ärer Gemeng. D'Europawalen, fir d'Europaparlament. An d'Nationalwalen, fir d'Chamber.",
   "Et ginn dräi wichteg Walen: d'Gemengewalen, fir de Rot vun Ärer Gemeng, d'Europawalen, fir d'Europaparlament, an d'Nationalwalen, fir d'Chamber."),
  ("Net bei allen dräi. D'Nationalwale sinn nëmme", "Net bei allen dräi, well d'Nationalwale sinn nëmme"),
  ("Et sinn der dräi. Dir hutt um Waldag op d'mannst uechtzéng Joer. Dir wunnt zu Lëtzebuerg. An Dir hutt Äert Walrecht",
   "Et sinn dräi Konditiounen: Dir hutt um Waldag op d'mannst uechtzéng Joer, Dir wunnt zu Lëtzebuerg, an Dir hutt Äert Walrecht"),
  ("Et ginn zwou Méiglechkeeten. Déi éischt ass online,", "Et ginn zwou Méiglechkeeten, an déi éischt ass online,"),
  ("Jo, dat si se. Dir kënnt einfach higoen", "Jo, an Dir kënnt einfach higoen"),
 ],
}
for sfx, pairs in R.items():
    p = f"podcast_script_jepeuxvoter{sfx}.md"; s = open(p, encoding="utf-8").read(); n = 0
    for a, b in pairs:
        if a in s: s = s.replace(a, b); n += 1
        elif b not in s: raise SystemExit(f"{p}: not found: {a[:50]}")
    open(p, "w", encoding="utf-8").write(s); print(p, n, "changed")
