import os, subprocess, json, sys
SR=int(os.environ.get("OUT_SR", "24000")); ENC_DELAY=0.05  # constant compensation for encoder delay + slight lag bias
# CLEAN=1 (ElevenLabs): tidy every sentence before joining —
#  * drop short stray sounds at the very start/end that are separated from the speech by a pause
#    (ElevenLabs sometimes starts the next word, or ends the previous one, because of the context text);
#  * trim leading/trailing silence to a fixed margin, with short fades so no edge clicks;
#  * even pauses: GAP_SAME between sentences of one turn, GAP_TURN when the speaker changes;
#  * LEAD_IN seconds of silence before the first word (players/Bluetooth fade in the first moment).
CLEAN=os.environ.get("CLEAN")=="1"
GAP_SAME=float(os.environ.get("GAP_SAME","0.28")); GAP_TURN=float(os.environ.get("GAP_TURN","0.42"))
LEAD_IN=float(os.environ.get("LEAD_IN","0.6")) if CLEAN else 0.0
def clean_pcm(raw):
    import numpy as np
    x=np.frombuffer(raw,np.int16).astype(np.float32)
    if len(x) < SR//10: return raw
    w=int(SR*0.01); n=len(x)//w
    env=20*np.log10(np.sqrt((x[:n*w].reshape(n,w)**2).mean(1))/32768+1e-9)
    on=env > -42
    if not on.any(): return raw
    # speech regions (in 10 ms frames), small holes (<60 ms) filled
    regs=[]; i=0
    while i<n:
        if on[i]:
            j=i
            while j<n and on[j]: j+=1
            if regs and i-regs[-1][1] < 6: regs[-1][1]=j
            else: regs.append([i,j])
            i=j
        else: i+=1
    # stray fragment at the end: short (<250 ms), after a pause of >=120 ms, and near the end
    while len(regs)>1 and regs[-1][1]-regs[-1][0] < 25 and regs[-1][0]-regs[-2][1] >= 12 and n-regs[-1][1] < 8:
        regs.pop()
    while len(regs)>1 and regs[0][1]-regs[0][0] < 25 and regs[1][0]-regs[0][1] >= 12 and regs[0][0] < 8:
        regs.pop(0)
    a=max(0,regs[0][0]*w-int(SR*0.03)); b=min(len(x),regs[-1][1]*w+int(SR*0.12))
    y=x[a:b].copy()
    fi=min(len(y),int(SR*0.008)); fo=min(len(y),int(SR*0.04))
    y[:fi]*=np.linspace(0,1,fi); y[len(y)-fo:]*=np.linspace(1,0,fo)
    return np.clip(y,-32768,32767).astype(np.int16).tobytes()
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
    def decode(f):  # gain + decode one sentence (independent, so it can run in parallel)
        g=seg_gain(WORK+"/"+f)
        return subprocess.run(["ffmpeg","-v","error","-i",WORK+"/"+f,*([] if g==0.0 else ["-af",f"volume={g:.2f}dB"]),"-f","s16le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=int(os.environ.get("REBUILD_JOBS","4"))) as pool:
        pcms=list(pool.map(decode, segs))  # results come back in sentence order
    if CLEAN:
        pcms=[clean_pcm(p) for p in pcms]
    with open(pcm_path,"wb") as out:
        pos=0
        if LEAD_IN:
            lead=b"\x00\x00"*int(SR*LEAD_IN); out.write(lead); pos+=len(lead)
        for k,pcm in enumerate(pcms):
            offsets.append(pos/2/SR)  # pre-tempo start seconds
            out.write(pcm); pos+=len(pcm)
            if CLEAN:
                nxt=meta[k+1]["speaker"] if k+1<len(meta) else None
                g=b"\x00\x00"*int(SR*(GAP_TURN if nxt and nxt!=meta[k]["speaker"] else GAP_SAME))
            else:
                g=gap_bytes
            out.write(g); pos+=len(g)
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
