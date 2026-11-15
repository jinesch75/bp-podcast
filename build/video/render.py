import sys, os, subprocess
from engine import *
from scenes import S

arr = np.zeros((H, W, 4), np.uint8)
surf = skia.Surface(arr)
cv = surf.getCanvas()


def shot(t, path):
    frame(cv, t, S); surf.flushAndSubmit()
    skia.Image.fromarray(arr.copy()).save(path)


def render_scene(k):
    sc = S[k]; f0 = int(round(sc.start * FPS)); f1 = int(round(sc.end * FPS))
    if k == len(S) - 1: f1 = int(math.ceil(DUR * FPS))
    out = f'out/s{k:02d}.mp4'; tmp = f'out/tmp_s{k:02d}.mp4'
    if os.path.exists(out): return
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS),
                          '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
                          '-threads', '1', tmp], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        frame(cv, f / FPS, S); surf.flushAndSubmit(); p.stdin.write(arr.tobytes())
    p.stdin.close()
    if p.wait() == 0: os.rename(tmp, out); print('done', k, f1 - f0, flush=True)
    else: print('FAILED', k, flush=True)


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True); os.makedirs('prev', exist_ok=True)
    if sys.argv[1] == 'shot':
        for t in sys.argv[2:]: shot(float(t), f'prev/f_{float(t):07.2f}.png')
    else:
        for k in sys.argv[2:]: render_scene(int(k))
