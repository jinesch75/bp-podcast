import os, subprocess, json, sys
SR=24000; ENC_DELAY=0.05  # constant compensation for encoder delay + slight lag bias
# GAP (silence between sentences) and TEMPO (speed-up) default to the edge-tts values.
# ElevenLabs voices are already paced naturally: run with TEMPO=1.0 (tts_elevenlabs.py prints the command).
GAP=float(os.environ.get("GAP", "0.14")); TEMPO=float(os.environ.get("TEMPO", "1.08"))
# LOUDNORM=<LUFS> (e.g. -20): bring every sentence to the same loudness before joining, so the two
# hosts sound equally loud. Gain only (no time change), so timestamps stay sample-accurate.
# Gain is capped so the sentence's true peak stays below PEAK_MAX dBTP. Off by default (edge-tts episodes).
LOUDNORM=os.environ.get("LOUDNORM"); PEAK_MAX=float(os.environ.get("PEAK_MAX", "-1.5"))
import re
def seg_gain(path):
    if not LOUDNORM: return 0.0
    err=subprocess.run(["ffmpeg","-hide_banner","-nostats","-i",path,"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
    try:
        I=float(re.findall(r"I:\s+(-?[\d.]+) LUFS",err)[-1]); pk=float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS",err)[-1])
    except (IndexError, ValueError):
        return 0.0
    if I < -70: return 0.0  # silence / too short to measure
    return min(float(LOUDNORM)-I, PEAK_MAX-pk)
def rebuild(WORK, out_mp3):
    segs=sorted(f for f in os.listdir(WORK) if f.startswith("seg_") and f.endswith(".mp3"))
    if os.path.exists(WORK+"/meta.json"):
        meta=json.load(open(WORK+"/meta.json"))["meta"]
    else:
        meta=json.load(open(WORK+"/segdata.json"))["segments"]
    assert len(meta)==len(segs),(len(meta),len(segs))
    gap_bytes=b"\x00\x00"*int(SR*GAP)
    pcm_path=WORK+"/full.pcm"
    offsets=[]
    with open(pcm_path,"wb") as out:
        pos=0
        for f in segs:
            offsets.append(pos/2/SR)  # pre-tempo start seconds
            g=seg_gain(WORK+"/"+f)
            p=subprocess.run(["ffmpeg","-v","error","-i",WORK+"/"+f,*([] if g==0.0 else ["-af",f"volume={g:.2f}dB"]),"-f","s16le","-ac","1","-ar",str(SR),"-"],capture_output=True)
            out.write(p.stdout); pos+=len(p.stdout)
            out.write(gap_bytes); pos+=len(gap_bytes)
    # encode once with tempo
    subprocess.run(["ffmpeg","-y","-f","s16le","-ar",str(SR),"-ac","1","-i",pcm_path,
                    *([] if TEMPO == 1.0 else ["-filter:a", f"atempo={TEMPO}"]),"-acodec","libmp3lame","-b:a","96k",out_mp3],capture_output=True)
    def dur(f):
        r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True)
        return float(r.stdout.strip())
    fd=dur(out_mp3)
    data=[{"speaker":meta[i]["speaker"],"text":meta[i]["text"],"t":round(offsets[i]/TEMPO+ENC_DELAY,2)} for i in range(len(segs))]
    json.dump({"duration":round(fd,2),"segments":data}, open(WORK+"/segdata_fixed.json","w"), ensure_ascii=False)
    return fd, data[-1]["t"], len(data)

if __name__=="__main__":
    WORK=sys.argv[1]; out=sys.argv[2]
    fd,last,n=rebuild(WORK,out)
    print(f"{WORK}: final_dur={fd:.2f} last_ts={last:.2f} segs={n}")
    print(f"  last_ts vs dur gap = {fd-last:.2f}s (should be small & positive)")
