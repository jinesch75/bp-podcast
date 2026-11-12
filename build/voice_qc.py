#!/usr/bin/env python3
"""Voice quality check for one recorded episode (ElevenLabs sentences in /tmp/<key>[_<lang>]_el_seg).
python3 build/voice_qc.py <key> <lang>  -> /tmp/voice_qc_<key>_<lang>.json (resumable) + a list of outliers.
Per sentence: speaking rate, pitch (median, spread, end-of-sentence movement), loudness, and a
whisper re-transcription with its confidence. Outliers are judged per speaker (robust z-score), so
it flags sentences that sound unlike the rest of that voice: strange melody, too fast/slow, mumbled."""
import json, os, re, sys, time
import numpy as np, librosa
sys.path.insert(0, "build")
from pronunciation import spoken
key, lang = sys.argv[1], sys.argv[2]
seg = f"/tmp/{key}_el_seg" if lang == "en" else f"/tmp/{key}_{lang}_el_seg"
meta = json.load(open(os.path.join(seg, "meta.json")))["meta"]
out = f"/tmp/voice_qc_{key}_{lang}.json"
res = json.load(open(out)) if os.path.exists(out) else {}
t0 = time.time(); budget = float(os.environ.get("BUDGET", 150))
from faster_whisper import WhisperModel
wm = WhisperModel("base", device="cpu", compute_type="int8")
for i, m in enumerate(meta):
    if str(i) in res: continue
    if time.time() - t0 > budget: print("budget used, run again"); break
    p = os.path.join(seg, f"seg_{i:04d}.mp3")
    y, sr = librosa.load(p, sr=16000)
    yt, _ = librosa.effects.trim(y, top_db=35)
    dur = len(yt) / sr
    f0, vf, _ = librosa.pyin(yt, fmin=70, fmax=420, sr=sr, frame_length=1024)
    f = f0[~np.isnan(f0)]
    st = 12 * np.log2(f / np.median(f)) if len(f) > 5 else np.array([0.0])
    tail = st[-max(3, len(st) // 6):]
    segs, info = wm.transcribe(p, language=lang, beam_size=1)
    segs = list(segs)
    lp = float(np.mean([s.avg_logprob for s in segs])) if segs else -5.0
    heard = " ".join(s.text.strip() for s in segs)
    txt = spoken(m["text"], lang)
    res[str(i)] = dict(speaker=m["speaker"], text=m["text"], dur=round(dur, 2),
        rate=round(len(re.sub(r"\W", "", txt)) / max(dur, 0.1), 2),
        f0=round(float(np.median(f)), 1) if len(f) else 0, spread=round(float(np.std(st)), 2),
        tail=round(float(np.mean(tail) - np.median(st)), 2), voiced=round(len(f) / max(len(f0), 1), 2),
        rms=round(float(20 * np.log10(np.sqrt(np.mean(yt ** 2)) + 1e-9)), 1), logprob=round(lp, 2), heard=heard)
    json.dump(res, open(out, "w"), ensure_ascii=False)
print(len(res), "/", len(meta), "done")
if len(res) == len(meta):
    rows = [dict(i=int(k), **v) for k, v in res.items()]
    flags = {}
    for spk in {r["speaker"] for r in rows}:
        rs = [r for r in rows if r["speaker"] == spk]
        for fld in ("rate", "f0", "spread", "rms", "voiced"):
            a = np.array([r[fld] for r in rs]); med = np.median(a); mad = np.median(np.abs(a - med)) * 1.4826 + 1e-6
            for r in rs:
                z = (r[fld] - med) / mad
                if abs(z) > 3.5: flags.setdefault(r["i"], []).append(f"{fld} {r[fld]} (z {z:+.1f})")
    for r in rows:
        if r["logprob"] < -0.8: flags.setdefault(r["i"], []).append(f"unclear (whisper {r['logprob']}: '{r['heard']}')")
    for i in sorted(flags):
        r = res[str(i)]; print(f"#{i} {r['speaker']} [{r['dur']}s] {r['text'][:70]!r}\n     " + "; ".join(flags[i]))
