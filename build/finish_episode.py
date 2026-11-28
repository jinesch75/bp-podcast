#!/usr/bin/env python3
"""Finish an episode with ONE command, so no step can be forgotten:

  record (ElevenLabs, from the cache when nothing changed) + listening check
  -> pitch check (voice_qc.py, EN/FR/DE in parallel)
  -> retakes of the lines that sound off (best_take.py), outside the standard intro/outro
  -> rebuild + second pitch check
  -> put live (inject_<key>.js for a new episode, replace_audio_elevenlabs.js)
  -> version bump, review page, partner Word file
  -> report: durations, what is left to check by ear, review link, git push commands

Usage (from the project root):

  python3 build/finish_episode.py <key> [en,fr,de] [options]

  --new             new episode: runs build/inject_<key>.js first if the key is not in episodes_data.js yet,
                    and marks it pending: it waits for Jacques's validation in the admin space before it is public;
                    and evens out the quiz answers (balance_quiz_answers.js --write)
  --no-retakes      pitch check, no retakes (no credits for retakes); still puts a changed recording live
  --check-only      pitch + listening check and report only: no retakes, nothing put live, nothing changed
  --max-retakes N   at most N retaken sentences per language (default 15; ~250 credits each)
  --budget S        stop cleanly after S seconds and print RUN AGAIN (default 160 = fits the 180 s
                    shell limit in Cowork). 0 = no limit (on the Mac / in Claude Code).
  --from STEP       redo from a step: record, qc1, pick, retake, rebuild, qc2, golive, publish, report
  --reset           forget the saved progress of this key and start again
  -m "message"      commit message for the push commands in the report

Run the same command again until it prints FINISHED. It is safe to stop at any point: progress is kept
in <work>/finish_state.json. The work folder is $FINISH_DIR, else /tmp/fin_<key>; it holds EL_TMP,
EL_STATE and EL_ASR_FILE for this run, so parallel sessions do not overwrite each other's files.
Best-take choices are re-applied to the shared build/el_cache/reseed.json before the rebuild
(another session writing that file at the same time can no longer drop them).

Use it for: a new episode (after the scripts and build/inject_<key>.js are written), any script change
(after the .md files are edited), or a plain pitch check of a live episode (text unchanged: the recording
comes from the cache, 0 credits apart from the retakes).
Added 26 Nov 2026 (Jacques: "I have to repeat a lot what you have to do, e.g. check the pitch").
"""
import glob, hashlib, json, math, os, re, shutil, subprocess, sys, time

ROOT = os.getcwd()
if not os.path.exists(os.path.join(ROOT, "episodes_data.js")):
    sys.exit("Run this from the project root (the folder with episodes_data.js).")
PY = sys.executable
SITE = "https://bp-podcast-production.up.railway.app"
STEPS = ["setup", "record", "qc1", "pick", "retake", "rebuild", "qc2", "golive", "publish", "report"]
QC_LANGS = ("en", "fr", "de")

# ---------- arguments ----------
args = sys.argv[1:]
def opt(name, default=None, flag=False):
    if name not in args: return default
    i = args.index(name)
    if flag: del args[i]; return True
    v = args[i + 1]; del args[i:i + 2]; return v
NEW = opt("--new", False, True)
NO_RETAKES = opt("--no-retakes", False, True)
CHECK_ONLY = opt("--check-only", False, True)
NO_RETAKES = NO_RETAKES or CHECK_ONLY
RESET = opt("--reset", False, True)
MAX_RETAKES = int(opt("--max-retakes", "15"))
BUDGET = float(opt("--budget", "160"))
FROM = opt("--from")
MSG = opt("-m")
if not args: sys.exit(__doc__)
KEY = args[0]
LANGS = [l for l in (args[1] if len(args) > 1 else "en,fr,de").split(",") if l]
bad = [l for l in LANGS if l not in QC_LANGS]
if bad: sys.exit(f"Only en, fr, de can be finished with this script (got {bad}).")
if FROM and FROM not in STEPS: sys.exit(f"--from must be one of {', '.join(STEPS)}")

T0 = time.time()
def left(): return math.inf if BUDGET <= 0 else BUDGET - (time.time() - T0)
def big(x): return 10 ** 7 if x == math.inf else max(1, int(x))

# ---------- work folder + state ----------
W = os.environ.get("FINISH_DIR") or f"/tmp/fin_{KEY}"
if os.path.exists(W) and not os.access(W, os.W_OK):
    W = f"/tmp/fin_{KEY}_{os.getuid()}"
os.makedirs(W, exist_ok=True)
SP = os.path.join(W, "finish_state.json")
if RESET:   # a new pass: also forget the recorder's "done" state and the old pitch measurements, otherwise a
            # changed script is not re-recorded (LAR ep, 2026-11-26). Unchanged sentences come from the cache (0 credits).
    for f in [SP, os.path.join(W, "rec_state.json"), os.path.join(W, "rebuild_state.json")] + glob.glob(f"{W}/voice_qc_{KEY}_*.json"):
        if os.path.exists(f): os.remove(f)
S = json.load(open(SP)) if os.path.exists(SP) else {}
if S.get("langs") and S["langs"] != LANGS and not RESET and not FROM:
    sys.exit(f"Saved progress is for languages {S['langs']}. Use the same languages, or --reset.")
S.setdefault("step", "setup"); S["langs"] = LANGS; S["new"] = NEW or S.get("new", False)
if FROM:
    S["step"] = FROM
    if STEPS.index(FROM) <= STEPS.index("record"):
        for f in ("rec_state.json", "rebuild_state.json"):
            if os.path.exists(os.path.join(W, f)): os.remove(os.path.join(W, f))
    if STEPS.index(FROM) <= STEPS.index("qc1"):
        for l in LANGS:
            for p in glob.glob(f"{W}/voice_qc_{KEY}_{l}*.json"): os.remove(p)
def save(): json.dump(S, open(SP + ".part", "w"), ensure_ascii=False, indent=1); os.replace(SP + ".part", SP)
LOG = open(os.path.join(W, "log.txt"), "a")
def log(s): LOG.write(s + "\n"); LOG.flush()

def again(why=""):
    save()
    print(f"\n▶ RUN AGAIN (same command) — {why or 'time budget used'}. Next step: {S['step']}.")
    sys.exit(0)
def die(msg):
    save(); print(f"\n✖ STOPPED at step '{S['step']}': {msg}"); sys.exit(1)
def run(cmd, env, timeout=None):
    """Run a command; returns (returncode or None on timeout, output)."""
    try:
        r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True,
                           timeout=None if timeout in (None, math.inf) else max(5, timeout))
        out = (r.stdout or "") + (r.stderr or ""); code = r.returncode
    except subprocess.TimeoutExpired as e:
        o = e.stdout or b""; o = o.decode(errors="replace") if isinstance(o, bytes) else o
        out, code = o, None
    log(f"$ {' '.join(cmd)}\n{out[-4000:]}")
    return code, out

sfx = lambda l: "" if l == "en" else "_" + l
seg_dir = lambda l: f"{W}/{KEY}{sfx(l)}_el_seg"
qc_file = lambda l: f"{W}/voice_qc_{KEY}_{l}.json"

# ---------- step: setup (python packages for the listening + pitch checks) ----------
def env_ok(env):
    code, _ = run([PY, "-c", "import faster_whisper, librosa"], env, 120)
    return code == 0
def setup():
    env = dict(os.environ, EL_TMP=W, EL_STATE=f"{W}/rec_state.json", EL_ASR_FILE=f"{W}/asr.json",
               NUMBA_CACHE_DIR=f"{W}/numba", PYTHONUNBUFFERED="1")
    if not env_ok(env):
        for d in sorted(glob.glob("/tmp/*/py")) + [f"{W}/py"]:
            if os.path.isdir(d) and env_ok(dict(env, PYTHONUSERBASE=d)):
                env["PYTHONUSERBASE"] = d; break
        else:
            if left() < 150: again("installing the listening-check packages needs a fresh call")
            env["PYTHONUSERBASE"] = f"{W}/py"
            print("Installing faster-whisper + librosa (once per computer/session)…")
            code, out = run([PY, "-m", "pip", "install", "--user", "--quiet", "--break-system-packages",
                             "faster-whisper", "librosa"], env, left() - 10)
            if code is None: again("still installing packages")
            if code != 0 or not env_ok(env): die("could not install faster-whisper/librosa:\n" + out[-800:])
        if env.get("PYTHONUSERBASE"): env["PATH"] = env["PYTHONUSERBASE"] + "/bin:" + env.get("PATH", "")
    # whisper models: reuse a cache that already has them (read-only caches work offline)
    if "HF_HOME" not in os.environ and not glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--Systran--faster-whisper-small")):
        for hf in sorted(glob.glob("/tmp/*/hf")):
            if glob.glob(f"{hf}/hub/models--Systran--faster-whisper-small") and glob.glob(f"{hf}/hub/models--Systran--faster-whisper-base"):
                env["HF_HOME"] = hf
                if not os.access(f"{hf}/hub", os.W_OK): env["HF_HUB_OFFLINE"] = "1"
                break
        else:
            env["HF_HOME"] = f"{W}/hf"
    # start the private listening-check cache from the shared one (saves re-transcribing unchanged sentences)
    shared_asr = os.path.join(ROOT, "build", "el_cache", "asr.json")
    if not os.path.exists(env["EL_ASR_FILE"]) and os.path.exists(shared_asr):
        shutil.copy(shared_asr, env["EL_ASR_FILE"])
    keep = ("EL_TMP", "EL_STATE", "EL_ASR_FILE", "NUMBA_CACHE_DIR", "PYTHONUSERBASE", "PATH", "HF_HOME", "HF_HUB_OFFLINE")
    S["env"] = {k: env[k] for k in keep if k in env}
    S["step"] = "record"

def ENV(**extra):
    e = dict(os.environ, PYTHONUNBUFFERED="1"); e.update(S.get("env", {})); e.update({k: str(v) for k, v in extra.items()}); return e

# ---------- steps: record / rebuild (el_run_batch.py, resumable) ----------
def batch(langs, state_file, label):
    if left() < 30: again()
    code, out = run([PY, "build/el_run_batch.py", KEY, ",".join(langs), "--budget", str(big(left() - 8))],
                    ENV(EL_STATE=f"{W}/{state_file}"), left() - 3)
    for l in out.splitlines():
        if "listening check" in l or "check manually" in l or "still cut" in l or "assembled" in l or "generated" in l:
            print("  " + l.strip())
    if "DONE ALL" in out: return True
    if "quota_exceeded" in out:
        die("the ElevenLabs key has no credits left (quota_exceeded). Raise its limit in ElevenLabs "
            "(Developers → API keys), then run the same command again — nothing recorded so far is lost.")
    if "FAILED" in out: die(f"{label} failed:\n" + out[-1500:])
    again(f"{label} in progress")

# ---------- steps: qc1 / qc2 (voice_qc.py, all languages in parallel) ----------
def n_sent(l): return len(json.load(open(f"{seg_dir(l)}/meta.json"))["meta"])
def qc_done(l): return os.path.exists(qc_file(l)) and len(json.load(open(qc_file(l)))) >= n_sent(l)
def qc(langs):
    todo = [l for l in langs if not qc_done(l)]
    if not todo: return True
    if left() < 60: again()
    os.makedirs(f"{W}/numba", exist_ok=True)
    cold = not os.listdir(f"{W}/numba")       # a cold numba cache + several runs at once can crash: warm with one
    run_now = todo[:1] if cold else todo
    budget = big(left() - 25)
    procs = [subprocess.Popen([PY, "build/voice_qc.py", KEY, l], cwd=ROOT,
                              env=ENV(BUDGET=budget, OMP_NUM_THREADS=1 if len(run_now) > 1 else 2),
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) for l in run_now]
    for l, p in zip(run_now, procs):
        try:
            out, _ = p.communicate(timeout=None if left() == math.inf else max(5, left() - 5))
        except subprocess.TimeoutExpired:
            p.kill(); out, _ = p.communicate()
        log(f"$ voice_qc.py {KEY} {l}\n{(out or '')[-3000:]}")
        if p.returncode not in (0, None, -9) and "Traceback" in (out or ""):
            print(f"  voice_qc {l}: error (see {W}/log.txt), will retry")
    for l in langs:
        if os.path.exists(qc_file(l)):
            print(f"  pitch check {l.upper()}: {len(json.load(open(qc_file(l))))} / {n_sent(l)} sentences measured")
    if all(qc_done(l) for l in langs): return True
    again("pitch check in progress")

# ---------- which sentences sound off (same measures as voice_qc.py / voice_qc_rank.py) ----------
def outliers(l):
    q = json.load(open(qc_file(l))); n = n_sent(l)
    std = set(range(0, 6)) | set(range(n - 5, n))          # standard intro/outro, shared by all episodes
    z = {}
    for spk in {v["speaker"] for v in q.values()}:
        ids = [k for k, v in q.items() if v["speaker"] == spk]
        for f in ("f0", "spread", "rate", "rms", "voiced", "tail"):
            pool = [k for k in ids if f != "tail" or q[k]["text"].rstrip().endswith(".")]
            a = sorted(q[k][f] for k in pool)
            if not a: continue
            med = a[len(a) // 2]; mad = sorted(abs(x - med) for x in a)[len(a) // 2] * 1.4826 or 1.0
            for k in pool: z.setdefault(k, {})[f] = (q[k][f] - med) / mad
    res, ear = [], []
    for k, v in q.items():
        i = int(k)
        if i in std: continue
        zz = z.get(k, {}); why = []
        if abs(zz.get("f0", 0)) >= 2.5: why.append(f"pitch {'high' if zz['f0'] > 0 else 'low'} ({v['f0']:.0f} Hz)")
        if abs(zz.get("spread", 0)) >= 2.6: why.append("melody " + ("too lively" if zz["spread"] > 0 else "flat"))
        if zz.get("tail", 0) >= 2.2: why.append("rising end on a statement")
        if abs(zz.get("rate", 0)) > 3.5: why.append("too " + ("fast" if zz["rate"] > 0 else "slow"))
        if abs(zz.get("rms", 0)) > 3.5: why.append("too " + ("loud" if zz["rms"] > 0 else "soft"))
        if abs(zz.get("voiced", 0)) > 3.5: why.append("breathy/creaky")
        score = max([abs(zz.get("f0", 0)), abs(zz.get("spread", 0)) * 0.8 / 1.04, zz.get("tail", 0) * 0.7 / 0.62,
                     abs(zz.get("rate", 0)) * 0.7, abs(zz.get("rms", 0)) * 0.7, abs(zz.get("voiced", 0)) * 0.7])
        if why: res.append(dict(i=i, speaker=v["speaker"], text=v["text"], why=why, score=round(score, 1)))
        if v.get("logprob", 0) < -0.8:
            ear.append(dict(i=i, speaker=v["speaker"], text=v["text"], heard=v.get("heard", "")))
    res.sort(key=lambda r: -r["score"])
    return res, ear

def pick():
    S["retake"] = {}; S["pass1"] = {}
    for l in LANGS:
        off, ear = outliers(l)
        S["pass1"][l] = {"off": off, "unclear": ear}
        S["retake"][l] = [] if NO_RETAKES else [r["i"] for r in off[:MAX_RETAKES]]
        print(f"  {l.upper()}: {len(off)} line(s) sound off" + ("" if NO_RETAKES else f" → retaking {len(S['retake'][l])}"))
    S["retake_pos"] = {l: 0 for l in LANGS}; S["chosen"] = {}; S["new_takes"] = {l: 0 for l in LANGS}; S["credits"] = 0

# ---------- step: retake (best_take.py, one language at a time, 3 sentences per call) ----------
RESEED = os.path.join(ROOT, "build", "el_cache", "reseed.json")
def read_reseed(): return json.load(open(RESEED)) if os.path.exists(RESEED) else {}
def retake():
    for l in LANGS:
        ids = S["retake"].get(l, [])
        while S["retake_pos"][l] < len(ids):
            if left() < 100: again("retakes in progress")
            chunk = ids[S["retake_pos"][l]:S["retake_pos"][l] + 3]
            before = read_reseed()
            code, out = run([PY, "build/best_take.py", KEY, l, ",".join(map(str, chunk))], ENV(), left() - 5)
            after = read_reseed()
            for b in set(before) | set(after):                    # remember our choices, to re-apply later
                if before.get(b) != after.get(b): S["chosen"][b] = after.get(b, b)
            for line in out.splitlines():
                if line.startswith("#"): print(f"  {l.upper()} {line.strip()[:120]}")
            S["new_takes"][l] += out.count("-> NEW take")
            m = re.search(r"≈ (\d+) credits", out); S["credits"] += int(m.group(1)) if m else 0
            if code is None: again("retakes in progress")      # partial: takes are cached, redoing the chunk is free
            if code != 0:
                if "quota_exceeded" in out:
                    die("the ElevenLabs key has no credits left (quota_exceeded). Raise its limit, then run again.")
                die(f"best_take.py failed for {l} {chunk}:\n" + out[-1200:])
            S["retake_pos"][l] += len(chunk); save()
    # re-apply our choices (another session may have rewritten the shared reseed.json meanwhile)
    cur = read_reseed(); fixed = 0
    for b, c in S["chosen"].items():
        want = None if c == b else c
        if cur.get(b) != want:
            fixed += 1
            if want is None: cur.pop(b, None)
            else: cur[b] = want
    if fixed:
        json.dump(cur, open(RESEED + ".part", "w"), indent=1); os.replace(RESEED + ".part", RESEED)
        print(f"  re-applied {fixed} best-take choice(s) that another session had overwritten")
    S["changed_langs"] = [l for l in LANGS if S["new_takes"].get(l)]

# ---------- step: golive ----------
NODE_EP = ("const fs=require('fs');const s=fs.readFileSync('episodes_data.js','utf8');"
           "const E=new Function(s.slice(s.indexOf('const EPISODES'))+'\\nreturn EPISODES;')();"
           "const e=E.find(x=>x.key===process.argv[1]);"
           "console.log(JSON.stringify(e?{number:e.number,title:e.title,duration:e.duration,duration_fr:e.duration_fr,"
           "duration_de:e.duration_de,audio:e.audio,audio_fr:e.audio_fr,audio_de:e.audio_de,status:e.status,pending:!!e.pending}:null))")
def episode():
    out = subprocess.run(["node", "-e", NODE_EP, KEY], cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0: die("could not read episodes_data.js:\n" + out.stderr[-800:])
    return json.loads(out.stdout.strip() or "null")
def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def golive():
    ep = episode()
    if ep is None:
        inj = f"build/inject_{KEY}.js"
        if not os.path.exists(inj):
            die(f"'{KEY}' is not in episodes_data.js yet. Write {inj} (title, description, topics, quiz in EN/FR/DE, "
                f"see build/inject_simpa.js), then run again with --from golive.")
        code, out = run(["node", inj], ENV(), 120)
        print("  " + "\n  ".join(out.strip().splitlines()[-3:]))
        if code != 0: die(f"{inj} failed:\n" + out[-1200:])
        S["injected"] = True
    if S.get("injected") and not (episode() or {}).get("pending"):
        # Every new episode waits for Jacques's validation in the admin space before it is on the public list.
        code, out = run(["node", "build/mark_pending.js", KEY], ENV(), 60)
        if code != 0: die("build/mark_pending.js failed:\n" + out[-800:])
        print("  waiting for validation in the admin space (not on the public list yet)")
    todo = []
    for l in LANGS:
        rec = f"{seg_dir(l)}/podcast_{KEY}{sfx(l)}.mp3"; live = os.path.join(ROOT, f"podcast_{KEY}{sfx(l)}.mp3")
        if not os.path.exists(live) or md5(rec) != md5(live): todo.append(l)
    if not todo:
        print("  the recording is identical to what is live — nothing to replace"); S["went_live"] = []; return
    code, out = run(["node", "build/replace_audio_elevenlabs.js", KEY, ",".join(todo)], ENV(), 300)
    for line in out.strip().splitlines(): print("  " + line)
    if code != 0: die("replace_audio_elevenlabs.js refused (the recording does not match the current scripts?):\n" + out[-1500:])
    S["went_live"] = todo

# ---------- step: publish ----------
def publish():
    steps = []
    if S.get("new"): steps.append(["node", "build/balance_quiz_answers.js", "--write"])
    changed = bool(S.get("went_live")) or S.get("injected")
    if changed: steps.append(["node", "build/bump_version.js"])
    steps += [["node", "build/make_review.js", KEY], ["node", "build/make_review_doc.js", KEY], ["node", "--check", "app.js"]]
    for cmd in steps:
        code, out = run(cmd, ENV(), 300)
        if code != 0: die(f"{' '.join(cmd)} failed:\n" + out[-1200:])
        print(f"  ✓ {' '.join(cmd[1:])}")
    # sanity check: durations in episodes_data.js match the mp3 files
    ep = episode(); S["durations"] = {}
    for l in LANGS:
        d = ep.get("duration" + sfx(l)); a = ep.get("audio" + sfx(l))
        try:
            real = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a],
                                        cwd=ROOT, capture_output=True, text=True).stdout.strip())
        except Exception:
            real = None
        S["durations"][l] = d
        if real is not None and d is not None and abs(real - float(d)) > 1.5:
            die(f"{l}: duration in episodes_data.js ({d}) does not match {a} ({real:.1f} s)")

# ---------- step: report ----------
def mmss(s):
    try: s = float(s); return f"{int(s // 60)}:{int(round(s % 60)):02d}"
    except Exception: return "?"
def report():
    ep = episode() or {}
    tok = {}
    try: tok = json.load(open(os.path.join(ROOT, "build", "review_tokens.json")))
    except Exception: pass
    L = [f"# {KEY} — finished {time.strftime('%Y-%m-%d %H:%M')}", ""]
    if ep:
        num = str(ep.get("number", ""))
        L.append(f"{num if num.lower().startswith('episode') else 'Episode ' + num}: {ep.get('title')}")
    L.append("Durations: " + ", ".join(f"{l.upper()} {mmss(ep.get('duration' + sfx(l)))}" for l in LANGS))
    nt = S.get("new_takes", {})
    L.append("Pitch check: " + ", ".join(f"{l.upper()} {len(S.get('pass1', {}).get(l, {}).get('off', []))} off → "
                                         f"{nt.get(l, 0)} new take(s)" for l in LANGS)
             + f" (≈ {S.get('credits', 0)} credits for retakes; standard intro/outro not checked)")
    L.append("Went live: " + ("— (check only)" if CHECK_ONLY else
                              (", ".join(x.upper() for x in S.get("went_live", [])) or "nothing changed")))
    ear_file = os.path.join(W, "el_check_by_ear.txt")
    ear_lines = [x.strip() for x in open(ear_file)] if os.path.exists(ear_file) else []
    still = {}
    for l in LANGS:
        if os.path.exists(qc_file(l)):
            off, unclear = outliers(l); still[l] = (off, unclear)
    L += ["", "## Still worth a listen (after retakes)"]
    any_left = False
    for l in LANGS:
        off, unclear = still.get(l, ([], []))
        for r in off[:8]:
            any_left = True; L.append(f"- {l.upper()} #{r['i']} {r['speaker']}: “{r['text'][:90]}” — {', '.join(r['why'])}")
        for r in unclear[:5]:
            any_left = True; L.append(f"- {l.upper()} #{r['i']} {r['speaker']}: “{r['text'][:90]}” — recogniser unsure (heard “{r['heard'][:60]}”)")
    for x in ear_lines:
        any_left = True; L.append(f"- listening check: {x}")
    if not any_left: L.append("- nothing flagged")
    L.append("  (A short line that stays off in every take: join it to the next sentence, in all four languages.)")
    if KEY in tok: L += ["", f"Review page: {SITE}/review/{KEY}-{tok[KEY]}/"]
    if ep.get("pending"):
        L.append(f"Not on the public list yet: waiting for your validation at {SITE}/admin/#validation (once pushed)")
    L.append(f"Word file for the partner: Relecture partenaires/Biergerpakt_Capsule_{KEY}_relecture.docx")
    if CHECK_ONLY:
        txt = "\n".join(L); open(os.path.join(W, "report.md"), "w").write(txt + "\n")
        print("\n" + txt + f"\n\n✅ FINISHED (check only, nothing changed). {W}/report.md"); return
    msg = MSG or (f"Add episode {ep.get('number')}: {KEY}" if S.get("injected") else f"{KEY}: recording + pitch check, review page and Word file updated")
    L += ["", "## Push to GitHub (in your terminal, in the project folder)", "```"]
    if os.path.exists(os.path.join(ROOT, ".git", "index.lock")): L.append("rm -f .git/index.lock")
    L += ["git add -A", f'git commit -m "{msg}"', "git push", "```"]
    txt = "\n".join(L)
    open(os.path.join(W, "report.md"), "w").write(txt + "\n")
    print("\n" + txt + f"\n\n✅ FINISHED ({W}/report.md). Run with --reset to start a new pass on this episode.")

# ---------- main loop ----------
print(f"finish_episode {KEY} [{','.join(LANGS)}] — work folder {W}")
while True:
    step = S["step"]
    if step == "setup": setup()
    elif step == "record":
        print("• recording + listening check"); batch(LANGS, "rec_state.json", "recording"); S["step"] = "qc1"
    elif step == "qc1":
        print("• pitch check"); qc(LANGS); S["step"] = "pick"
    elif step == "pick":
        pick(); S["step"] = "retake"
    elif step == "retake":
        if any(S.get("retake", {}).get(l) for l in LANGS): print("• retakes")
        retake(); S["step"] = "rebuild"
    elif step == "rebuild":
        ch = S.get("changed_langs", [])
        if ch:
            print("• rebuilding " + ",".join(ch))
            if not S.get("pass1_moved"):
                for l in ch:
                    if os.path.exists(qc_file(l)): os.replace(qc_file(l), qc_file(l).replace(".json", ".pass1.json"))
                S["pass1_moved"] = True; save()
            batch(ch, "rebuild_state.json", "rebuild")
        S["step"] = "qc2"
    elif step == "qc2":
        ch = S.get("changed_langs", [])
        if ch: print("• second pitch check"); qc(ch)
        S["step"] = "report" if CHECK_ONLY else "golive"
    elif step == "golive":
        print("• putting it live"); golive(); S["step"] = "publish"
    elif step == "publish":
        print("• version bump, review page, Word file"); publish(); S["step"] = "report"
    elif step == "report":
        report(); S["step"] = "done"; save(); break
    elif step == "done":
        print("Already FINISHED for this key. Report: " + os.path.join(W, "report.md") + " — use --reset for a new pass.")
        if os.path.exists(os.path.join(W, "report.md")): print(open(os.path.join(W, "report.md")).read())
        break
    save()
