#!/usr/bin/env python3
"""A/B listening test for new French host voices (Jacques, 27 Nov 2026: Lucie/Marcel sound boxy and hurried).
Same two lines from the MyGuichet FR script, read by each candidate with the project's normal settings.
-> build/el_test/fr_voices/<role>_<nn>_<name>.mp3 (each levelled to -20 LUFS) + ANNA_all.mp3 / TOM_all.mp3 + rates.txt"""
import hashlib, importlib.util, json, os, re, subprocess
spec = importlib.util.spec_from_file_location("el", "build/tts_elevenlabs.py"); el = importlib.util.module_from_spec(spec); spec.loader.exec_module(el)
el.load_env(); key = os.environ["ELEVENLABS_API_KEY"].strip()
ANNA_TXT = ("Ce podcast fait partie du Biergerpakt. C'est un programme du vivre-ensemble au Luxembourg, organisé par le "
            "Ministère de la Famille, des Solidarités, du Vivre ensemble et de l'Accueil. L'idée est d'aider les résidents, "
            "et aussi les frontaliers, à découvrir le Luxembourg, ou peut-être à le redécouvrir, et à rencontrer de nouvelles personnes.")
TOM_TXT = ("Bien sûr que vous pouvez. Mais les bureaux sont ouverts en journée, quand beaucoup d'entre nous sont au travail. "
           "MyGuichet.lu est ouvert vingt-quatre heures sur vingt-quatre, sept jours sur sept. Vous gagnez du temps : pas de file, "
           "pas d'attente. Et tout reste au même endroit.")
CAND = {
 "ANNA": [("Lucie (current)", "YxrwjAKoUKULGd0g8K9Y"), ("Victoria - Warm and calm", "WeAAwKYcS06VmXw086yZ"),
          ("Jeanne - Narrator", "txtf1EDouKke753vN8SL"), ("Marie Alice - Soft, Calm", "tMyQcCxfGDdIt7wJ2RQw"),
          ("Anais - Instructor", "5OnMHwgTFgvPVwE8jP6B"), ("Koraly - Credible and Professional", "MNKK2Wl2wbbsEPQTHZGt"),
          ("Caroline - Warm, Sweet and Soft", "kwhMCf63M8O3rCfnQ3oQ")],
 "TOM":  [("Marcel (current)", "kENkNtk0xyzG09WW40xE"), ("Nicolas - Narrator", "aQROLel5sQbj1vuIVi6B"),
          ("Clement - Calm and Neutral", "jUHQdLfy668sllNiNTSW"), ("Martin Dupont - Podcast Narrator", "FNOttooGMYDRXmqkQ0Fz"),
          ("Adrien Clairon - Podcast Narrator", "c365oriviHmAhyLhpuN6"), ("Guillaume - Narrator", "Qrl71rx6Yg8RvyPYRGCQ"),
          ("Celian - Documentary Narrator", "DGTOOUoGpoP6UZ9uSWfA")]}
import sys
D = "build/el_test/fr_voices"; os.makedirs(f"{D}/raw", exist_ok=True)
TAG = ""
if len(sys.argv) > 2:   # python3 build/fr_voice_ab.py <ROLE> <tag> "Name=voice_id" ...  (second round)
    role, TAG = sys.argv[1].upper(), "_" + sys.argv[2]
    CAND = {role: [tuple(a.split("=", 1)) for a in sys.argv[3:]]}
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout)
def speech_dur(p):   # duration without leading/trailing silence
    out = subprocess.run(["ffmpeg","-i",p,"-af","silencedetect=n=-40dB:d=0.25","-f","null","-"],capture_output=True,text=True).stderr
    t = dur(p); st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    lead = en[0] if st and st[0] < 0.05 and en else 0.0
    tail = t - st[-1] if st and (len(st) > len(en)) else 0.0
    pauses = sum(e - s for s, e in zip(st, en) if s > 0.05)
    return t - lead - tail, pauses
rates = []
for role, cands in CAND.items():
    txt = ANNA_TXT if role == "ANNA" else TOM_TXT
    spoken = el.spoken(txt, "fr"); parts = []
    for i, (name, vid) in enumerate(cands):
        body = {"text": spoken, "model_id": "eleven_multilingual_v2", "voice_settings": el.VOICE_SETTINGS, "seed": 1234}
        h = hashlib.sha1(json.dumps([vid, body], sort_keys=True).encode()).hexdigest()[:16]; raw = f"{D}/raw/{h}.mp3"
        if not os.path.exists(raw):
            open(raw, "wb").write(el.request("POST", f"/text-to-speech/{vid}", key, body, query="?output_format=mp3_44100_128"))
        slug = re.sub(r"[^A-Za-z]+", "_", name.split(" - ")[0].split(" (")[0]).strip("_")
        out = f"{D}/{role}{TAG}_{i:02d}_{slug}{'_CURRENT' if 'current' in name else ''}.mp3"
        subprocess.run(["ffmpeg","-y","-v","error","-i",raw,"-af","loudnorm=I=-20:TP=-1.5","-ar","44100","-b:a","128k",out], check=True)
        sd, pa = speech_dur(out); words = len(txt.split())
        rates.append(f"{role:4} {name:38} {sd:5.1f}s  {words/sd*60:5.0f} words/min  pauses {pa:4.1f}s")
        parts.append(out)
    n = len(parts); ins = sum((["-i", p] for p in parts), [])
    filt = "".join(f"[{j}:a]apad=pad_dur=1.5[a{j}];" for j in range(n)) + "".join(f"[a{j}]" for j in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    subprocess.run(["ffmpeg","-y","-v","error",*ins,"-filter_complex",filt,"-map","[o]","-b:a","128k",f"{D}/{role}{TAG}_all.mp3"], check=True)
    t = 0.0; lines = []
    for j, (name, _) in enumerate(cands):
        lines.append(f"  {int(t//60)}:{t%60:04.1f}  {chr(65+j)}  {name}"); t += dur(parts[j]) + 1.5
    rates.append(f"{role}{TAG}_all.mp3 order:\n" + "\n".join(lines))
open(f"{D}/rates{TAG}.txt", "w").write("\n".join(rates) + "\n"); print("\n".join(rates))
