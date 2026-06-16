import os, subprocess, json, sys
SR=24000; GAP=0.14; TEMPO=1.08; ENC_DELAY=0.05  # constant compensation for encoder delay + slight lag bias
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
            p=subprocess.run(["ffmpeg","-v","error","-i",WORK+"/"+f,"-f","s16le","-ac","1","-ar",str(SR),"-"],capture_output=True)
            out.write(p.stdout); pos+=len(p.stdout)
            out.write(gap_bytes); pos+=len(gap_bytes)
    # encode once with tempo
    subprocess.run(["ffmpeg","-y","-f","s16le","-ar",str(SR),"-ac","1","-i",pcm_path,
                    "-filter:a",f"atempo={TEMPO}","-acodec","libmp3lame","-b:a","96k",out_mp3],capture_output=True)
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
