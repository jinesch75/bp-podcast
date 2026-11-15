import skia, json, math, random
import numpy as np

W, H, FPS = 1920, 1080, 30
D = json.load(open('segs.json')); SEG = D['segments']; DUR = D['duration']
T = [s['t'] for s in SEG] + [DUR]
FA = json.load(open('fa.json'))

BG, NAVY, ORANGE, DARK, MUTED, WHITE = '#F6F6F4', '#1A3C5E', '#E84600', '#111111', '#666666', '#FFFFFF'
GREEN, RED, TOM, BORDER, NIGHT, OLIGHT = '#2A7A3B', '#C0392B', '#b8430a', '#E2E2E0', '#0E2238', '#FFF4EE'
YELLOW = '#FFD166'


def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def col(h, a=1.0):
    r, g, b = rgb(h) if isinstance(h, str) else h
    return skia.Color(int(r), int(g), int(b), int(max(0, min(1, a)) * 255))


def mix(h1, h2, k):
    a, b = rgb(h1), rgb(h2); k = max(0, min(1, k))
    return tuple(a[i] + (b[i] - a[i]) * k for i in range(3))


INTER = '/usr/share/fonts/opentype/inter/Inter-%s.otf'
TFS = {k: skia.Typeface.MakeFromFile(INTER % v) for k, v in
       dict(r='Regular', m='Medium', s='SemiBold', b='Bold', x='ExtraBold').items()}
TFI = skia.Typeface.MakeFromFile('fa-solid.ttf')
_fc = {}


def fnt(w, size):
    k = (w, round(size, 1))
    if k not in _fc:
        f = skia.Font(TFI if w == 'i' else TFS[w], size); f.setSubpixel(True); _fc[k] = f
    return _fc[k]


def P(color, a=1.0, stroke=None):
    p = skia.Paint(AntiAlias=True, Color=col(color, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def eoc(p): p = clamp(p); return 1 - (1 - p) ** 3
def eob(p):
    p = clamp(p); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2
def eio(p): p = clamp(p); return 3 * p * p - 2 * p ** 3


def tw(s, size, w='b'): return fnt(w, size).measureText(s)


def text(c, s, x, y, size, w='b', color=NAVY, align='c', a=1.0):
    f = fnt(w, size); m = f.measureText(s)
    if align == 'c': x -= m / 2
    elif align == 'r': x -= m
    c.drawString(s, x, y + size * 0.35, f, P(color, a))
    return m


def wrap(s, size, w, maxw):
    out = []
    for para in s.split('\n'):
        line = ''
        for word in para.split(' '):
            t = (line + ' ' + word).strip()
            if tw(t, size, w) <= maxw or not line: line = t
            else: out.append(line); line = word
        out.append(line)
    return out


def textbox(c, s, x, y, size, w='b', color=NAVY, maxw=1000, align='c', lh=1.22, a=1.0):
    lines = wrap(s, size, w, maxw); n = len(lines)
    for i, l in enumerate(lines):
        text(c, l, x, y + (i - (n - 1) / 2) * size * lh, size, w, color, align, a)
    return n


def icon(c, name, x, y, size, color=NAVY, a=1.0):
    ch = chr(int(FA[name], 16)); f = fnt('i', size); m = f.measureText(ch)
    c.drawString(ch, x - m / 2, y + size * 0.36, f, P(color, a))


def rrect(c, x, y, w, h, r, color, a=1.0, stroke=None):
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), r, r, P(color, a, stroke))


def card(c, x, y, w, h, r=28, fill=WHITE, border=BORDER):
    rrect(c, x, y + 7, w, h, r, '#000000', 0.06)
    rrect(c, x, y, w, h, r, fill)
    if border: rrect(c, x, y, w, h, r, border, 1, 2)


class El:
    def __init__(s, t0, fn, cx=960, cy=490, t1=None, anim='up', dur=0.45):
        s.t0, s.fn, s.cx, s.cy, s.t1, s.anim, s.dur = t0, fn, cx, cy, t1, anim, dur

    def draw(s, c, t):
        if t < s.t0: return
        lt = t - s.t0; p = min(lt / s.dur, 1); a = min(p * 1.8, 1)
        if s.t1 is not None:
            if t > s.t1 + 0.3: return
            if t > s.t1: a *= 1 - (t - s.t1) / 0.3
        c.save()
        if s.anim == 'pop' and p < 1:
            k = eob(p); c.translate(s.cx, s.cy); c.scale(k, k); c.translate(-s.cx, -s.cy)
        elif s.anim == 'up' and p < 1:
            c.translate(0, (1 - eoc(p)) * 36)
        layer = a < 0.995
        if layer: c.saveLayerAlpha(None, int(a * 255))
        s.fn(c, lt)
        if layer: c.restore()
        c.restore()


# ---- element builders -------------------------------------------------
def Tx(t0, s, x, y, size, w='b', color=NAVY, t1=None, align='c'):
    return El(t0, lambda c, lt: text(c, s, x, y, size, w, color, align), x, y, t1)


def TB(t0, s, x, y, size, w='b', color=NAVY, maxw=1200, t1=None):
    return El(t0, lambda c, lt: textbox(c, s, x, y, size, w, color, maxw), x, y, t1)


def IC(t0, name, x, y, size, color=NAVY, t1=None):
    return El(t0, lambda c, lt: icon(c, name, x, y, size, color), x, y, t1, 'pop')


def Tile(t0, x, y, w, h, ic, label, color=NAVY, t1=None, lsize=None):
    lsize = lsize or (30 if w >= 340 else 26)
    def fn(c, lt):
        card(c, x, y, w, h)
        r = min(w, h) * 0.24; iy = y - h * 0.15
        c.drawCircle(x, iy, r, P(color, 0.10))
        icon(c, ic, x, iy, r * 1.05, color)
        textbox(c, label, x, y + h * 0.29, lsize, 's', NAVY, w - 40)
    return El(t0, fn, x, y, t1, 'pop')


def Row(t0, x, y, w, h, ic, label, color=NAVY, t1=None, num=None, size=36):
    def fn(c, lt):
        card(c, x, y, w, h, r=h * 0.3)
        cx = x - w / 2 + h * 0.62; r = h * 0.34
        c.drawCircle(cx, y, r, P(color))
        if num is not None: text(c, str(num), cx, y, r * 1.1, 'x', WHITE)
        else: icon(c, ic, cx, y, r * 1.0, WHITE)
        lx = x - w / 2 + h * 1.25
        lines = wrap(label, size, 's', w - h * 1.25 - (h * 1.1 if num is not None and ic else 40))
        for i, l in enumerate(lines):
            text(c, l, lx, y + (i - (len(lines) - 1) / 2) * size * 1.2, size, 's', NAVY, 'l')
        if num is not None and ic: icon(c, ic, x + w / 2 - h * 0.6, y, h * 0.4, color, 0.35)
    return El(t0, fn, x, y, t1, 'up')


def Pill(t0, s, x, y, size, bg=NAVY, fg=WHITE, ic=None, t1=None):
    def fn(c, lt):
        m = tw(s, size, 'b'); iw = size * 1.5 if ic else 0
        w = m + iw + size * 1.6; h = size * 1.9
        rrect(c, x, y, w, h, h / 2, bg)
        if bg in (WHITE, OLIGHT): rrect(c, x, y, w, h, h / 2, '#F3C9B5' if bg == OLIGHT else BORDER, 1, 2)
        if ic: icon(c, ic, x - w / 2 + size * 1.25, y, size * 0.95, fg)
        text(c, s, x - w / 2 + size * 0.8 + iw, y, size, 'b', fg, 'l')
    return El(t0, fn, x, y, t1, 'pop')


def Cu(t0, fn, t1=None, anim='fade', cx=960, cy=490):
    return El(t0, fn, cx, cy, t1, anim)


def at(i, phrase):
    s = SEG[i]['text']; k = s.find(phrase)
    if k < 0: raise ValueError(f'{phrase!r} not in seg {i}: {s}')
    return T[i] + (k / len(s)) * max(T[i + 1] - T[i] - 0.4, 0.5)


class Scene:
    def __init__(s, i0, i1, chapter, els, dark=False):
        s.start = 0.0 if i0 == 0 else T[i0]; s.end = T[i1]; s.chapter = chapter; s.els = els; s.dark = dark


# ---- captions ---------------------------------------------------------
def _split(s, lim=92):
    if len(s) <= lim: return [s]
    best = None
    for sep in (', ', ': ', ' — ', '. ', '? '):
        k = s.find(sep)
        while k > 0:
            cut = k + len(sep.rstrip()) if sep != ' — ' else k
            d = abs(cut - len(s) / 2)
            if cut > 20 and len(s) - cut > 20 and (best is None or d < best[0]): best = (d, cut)
            k = s.find(sep, k + 1)
    if not best:
        k = s.rfind(' ', 0, len(s) // 2 + 10); best = (0, k)
    a, b = s[:best[1]].strip(), s[best[1]:].strip(' —')
    return _split(a, lim) + _split(b, lim)


CAPS = []
for i, sg in enumerate(SEG):
    import re as _re
    _t = _re.sub(r'(\w+) dot l-u', r'\1.lu', sg['text']).replace('1-1-3', '113')
    parts = _split(_t); tot = sum(len(p) for p in parts); t = T[i]; span = T[i + 1] - T[i]
    for p in parts:
        d = span * len(p) / tot; CAPS.append((t, t + d, sg['speaker'], p)); t += d

pcm = np.frombuffer(open('audio.pcm', 'rb').read(), dtype=np.int16).astype(np.float32)
n = int(len(pcm) / 8000 * FPS); spf = 8000 / FPS
ENV = np.array([np.sqrt(np.mean(pcm[int(i * spf):int((i + 1) * spf)] ** 2) + 1) for i in range(n)])
ENV = np.clip(ENV / np.percentile(ENV, 95), 0, 1.2)


def caption(c, t):
    f = int(t * FPS)
    cap = None
    for cp in CAPS:
        if cp[0] <= t < cp[1]: cap = cp; break
    card(c, 960, 958, 1760, 150, r=36)
    if not cap: return
    spk = cap[2]; cc = NAVY if spk == 'Anna' else TOM
    c.drawCircle(160, 958, 44, P(cc)); text(c, spk[0], 160, 958, 44, 'x', WHITE)
    text(c, spk.upper(), 225, 940, 24, 'b', cc, 'l')
    for k in range(6):
        e = ENV[max(0, min(len(ENV) - 1, f - k))]; hh = 6 + 26 * e * (0.6 + 0.4 * math.sin(k * 1.7 + 1))
        rrect(c, 229 + k * 11, 978, 6, hh, 3, cc, 0.85)
    a = clamp((t - cap[0]) / 0.15)
    size = 38; lines = wrap(cap[3], size, 'm', 1440)
    if len(lines) > 2: size = 32; lines = wrap(cap[3], size, 'm', 1440)
    for i, l in enumerate(lines):
        text(c, l, 345, 958 + (i - (len(lines) - 1) / 2) * size * 1.25, size, 'm', DARK, 'l', a)


def darkness(t, scenes):
    d = 0.0
    for s in scenes:
        if s.dark: d = max(d, clamp(min((t - s.start) / 0.5, (s.end - t) / 0.5)))
    return d


def frame(c, t, scenes):
    d = darkness(t, scenes)
    c.clear(col(mix(BG, NIGHT, d)))
    sc = next((s for s in scenes if s.start <= t < s.end), scenes[-1])
    hc = mix(NAVY, WHITE, d)
    text(c, 'BIERGERPAKT PODCAST', 80, 62, 24, 'x', ORANGE if d < 0.5 else YELLOW, 'l')
    text(c, 'Episode 43  ·  Lëtz prepare', 392, 62, 24, 'm', mix(MUTED, '#C9D3DD', d), 'l')
    text(c, sc.chapter, 1840, 62, 26, 's', hc, 'r')
    c.drawRect(skia.Rect.MakeXYWH(80, 92, 1760, 2), P(mix(BORDER, '#2a4866', d)))
    a = clamp(min((t - sc.start) / 0.3, (sc.end - t) / 0.3)) if sc.start > 0 else clamp((sc.end - t) / 0.3)
    if sc is scenes[-1]: a = clamp((t - sc.start) / 0.3)
    layer = a < 0.995
    if layer: c.saveLayerAlpha(None, int(a * 255))
    for e in sc.els: e.draw(c, t)
    if layer: c.restore()
    caption(c, t)
    c.drawRect(skia.Rect.MakeXYWH(0, 1068, W, 12), P(mix(BORDER, '#2a4866', d)))
    c.drawRect(skia.Rect.MakeXYWH(0, 1068, W * t / DUR, 12), P(ORANGE))
