#!/usr/bin/env python3
"""Run ElevenLabs generation + assembly for many episodes/languages, resumable.

  python3 build/el_run_batch.py <key1,key2,...> <en,fr,de> [--budget SECONDS]

Works through every key x language: tts_elevenlabs.py (--yes, parallel requests via
EL_CONCURRENCY, default 6) then `TEMPO=1.0 LOUDNORM=-20 rebuild.py`. Stops cleanly before
--budget seconds (default 160) so it fits in a short shell call; just run it again to
continue — finished pairs are remembered in /tmp/el_batch_state.json and the sentence cache
makes restarts free. Prints DONE ALL when every pair is assembled.
"""
import json, os, subprocess, sys, time
ROOT = os.getcwd()
STATE = "/tmp/el_batch_state.json"
t0 = time.time()
keys, langs = sys.argv[1].split(","), sys.argv[2].split(",")
budget = float(sys.argv[sys.argv.index("--budget") + 1]) if "--budget" in sys.argv else 160.0
state = json.load(open(STATE)) if os.path.exists(STATE) else {}
env = dict(os.environ, EL_CONCURRENCY=os.environ.get("EL_CONCURRENCY", "6"), PYTHONUNBUFFERED="1")
left = lambda: budget - (time.time() - t0)
for key in keys:
    for lang in langs:
        tag = f"{key}:{lang}"
        if state.get(tag) == "done":
            continue
        sfx = "" if lang == "en" else "_" + lang
        work = f"/tmp/{key}{sfx}_el_seg"
        if state.get(tag) != "generated":
            if left() < 20:
                print("budget used — run again to continue"); sys.exit(0)
            try:
                r = subprocess.run([sys.executable, "build/tts_elevenlabs.py", key, lang, "--yes"], env=env,
                                   capture_output=True, text=True, timeout=left() - 5)
            except subprocess.TimeoutExpired:
                print(f"{tag}: generating… (partial, cached) — run again"); sys.exit(0)
            out = r.stdout + r.stderr
            if "ALL SEGMENTS DONE" not in out:
                print(f"{tag}: FAILED\n{out[-1500:]}"); sys.exit(1)
            state[tag] = "generated"; json.dump(state, open(STATE, "w"))
            print(f"{tag}: generated ({[l for l in out.splitlines() if l.startswith('sentences:')][0]})")
            for l in out.splitlines():
                if "listening check" in l or "check manually" in l or "still cut" in l:
                    print("   " + l.strip())
                    if "check manually" in l:
                        open("/tmp/el_check_by_ear.txt", "a").write(f"{tag}  {l.strip()}\n")
        if left() < 40:
            print("budget used — run again to continue"); sys.exit(0)
        try:
            r = subprocess.run([sys.executable, "build/rebuild.py", work, f"{work}/podcast_{key}{sfx}.mp3"],
                               env=dict(env, TEMPO="1.0", LOUDNORM="-20", CLEAN="1", OUT_SR="44100"), capture_output=True, text=True,
                               timeout=left() - 3)
        except subprocess.TimeoutExpired:
            print(f"{tag}: assembling… — run again"); sys.exit(0)
        if r.returncode != 0:
            print(f"{tag}: REBUILD FAILED\n{(r.stdout + r.stderr)[-1500:]}"); sys.exit(1)
        state[tag] = "done"; json.dump(state, open(STATE, "w"))
        print(f"{tag}: assembled — {r.stdout.strip().splitlines()[0].split(': ', 1)[1]}")
print("DONE ALL")
