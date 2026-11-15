from engine import *

R = random.Random(7)
S = []

# 1 — intro ---------------------------------------------------------------
def logo(c, lt):
    c.drawCircle(960, 285, 78, P(ORANGE)); icon(c, 'podcast', 960, 285, 84, WHITE)
e = [El(0.15, logo, 960, 285, T[3] - 0.25, 'pop'),
     Tx(0.5, 'BIERGERPAKT PODCAST', 960, 410, 30, 'x', ORANGE, T[3] - 0.25),
     Tx(0.9, 'Lëtz prepare', 960, 530, 160, 'x', NAVY, T[3] - 0.25),
     Tx(1.6, 'Ready for 72 hours', 960, 670, 62, 's', ORANGE, T[3] - 0.25),
     Tx(2.3, 'Episode 43', 960, 760, 32, 'm', MUTED, T[3] - 0.25),
     Tx(T[3] + 0.1, 'Part of the Biergerpakt', 960, 210, 80, 'x', NAVY),
     Tx(T[4] + 0.3, 'A programme of living together in Luxembourg', 960, 310, 42, 's', ORANGE),
     TB(T[4] + 3.2, 'Organised by the Ministry of Family Affairs, Solidarity, Living Together and Reception of Refugees',
        960, 400, 28, 'm', MUTED, 1300)]
for k, (ph, ic, lb) in enumerate([('residents', 'house-user', 'Residents'), ('cross-border', 'briefcase', 'Cross-border workers'),
                                  ('discover', 'compass', 'Discover Luxembourg'), ('meet', 'users', 'Meet new people')]):
    e.append(Tile(at(5, ph), 960 + (k - 1.5) * 400, 650, 360, 270, ic, lb, ORANGE if k > 1 else NAVY))
S.append(Scene(0, 6, 'Welcome', e))

# 2 — blackout ------------------------------------------------------------
BLD = []
x = 60
while x < 1860:
    bw = R.choice([110, 140, 170, 200]); bh = R.randint(160, 380)
    wins = [(x + 18 + cxi * 34, 850 - bh + 22 + ryi * 44, T[7] + 1.0 + R.random() * 4.2)
            for cxi in range(int((bw - 30) // 34)) for ryi in range(int((bh - 30) // 44)) if R.random() < 0.8]
    BLD.append((x, bw, bh, wins)); x += bw + 14
def skyline(c, lt):
    t = lt + T[6]
    for (bx, bw, bh, wins) in BLD:
        c.drawRect(skia.Rect.MakeXYWH(bx, 850 - bh, bw, bh), P('#17344F'))
        for (wx, wy, off) in wins:
            k = clamp((t - off) / 0.25)
            c.drawRect(skia.Rect.MakeXYWH(wx, wy, 18, 24), P(mix(YELLOW, '#213F5C', k)))
def candle(c, lt):
    fl = 1 + 0.06 * math.sin(lt * 9)
    c.drawCircle(760, 330, 120 * fl, P(YELLOW, 0.10)); c.drawCircle(760, 330, 70 * fl, P(YELLOW, 0.14))
    icon(c, 'fire', 760, 330, 110, YELLOW); text(c, 'A few candles', 760, 440, 36, 's', WHITE)
def biscuit(c, lt):
    icon(c, 'cookie-bite', 1160, 330, 110, '#E0A458'); text(c, 'Half a packet of biscuits', 1160, 440, 36, 's', WHITE)
S.append(Scene(6, 12, 'Are you ready?', [
    Cu(T[6], skyline),
    Tx(T[6] + 0.1, 'A question to start', 960, 230, 54, 's', '#C9D3DD', T[7] - 0.1),
    Tx(T[7] + 0.2, 'The power goes off tonight', 960, 210, 76, 'x', WHITE, T[8] - 0.2),
    Pill(at(7, 'three days'), 'and stays off for 3 days', 960, 330, 44, ORANGE, WHITE, 'clock', T[8] - 0.2),
    Tx(T[8], 'Would you be ready?', 960, 270, 120, 'x', WHITE, T[9] - 0.1),
    El(at(9, 'candles'), candle, 760, 330, T[10] - 0.2, 'pop'),
    El(at(9, 'half'), biscuit, 1160, 330, T[10] - 0.2, 'pop'),
    Tx(T[10] + 0.1, 'Then this episode is for you', 960, 250, 64, 's', WHITE, T[11] - 0.1),
    Tx(T[11] + 0.6, 'Lëtz prepare', 960, 280, 170, 'x', ORANGE)], dark=True))

# 3 — the name ------------------------------------------------------------
def wcard(x, big, small, color):
    def fn(c, lt):
        card(c, x, 540, 580, 210); text(c, big, x, 515, 84, 'x', color); text(c, small, x, 600, 32, 'm', MUTED)
    return fn
S.append(Scene(12, 16, 'Lëtz prepare', [
    Tx(T[12], 'Lëtz prepare', 960, 215, 130, 'x', NAVY),
    Tx(T[12] + 1.6, "Luxembourg's National Resilience Strategy", 960, 335, 50, 's', ORANGE),
    El(at(13, 'like'), wcard(610, 'Lëtz', 'like Lëtzebuerg', NAVY), 610, 540, None, 'pop'),
    Tx(at(13, 'English') - 0.3, '+', 960, 540, 90, 'x', MUTED),
    El(at(13, 'English'), wcard(1310, "let's prepare", 'in English', ORANGE), 1310, 540, None, 'pop'),
    Pill(T[14] + 0.6, 'letzprepare.lu', 610, 760, 46, NAVY, WHITE, 'globe'),
    Pill(T[15] + 1.0, '“Together, for our protection.”', 1310, 760, 38, ORANGE, WHITE, 'shield-halved')]))

# 4 — resilience ----------------------------------------------------------
GP = [(330, 520), (720, 520), (790, 690), (860, 700), (960, 640), (1080, 570), (1220, 525), (1400, 505), (1590, 495)]
def graph(c, lt):
    c.drawLine(330, 520, 1590, 520, P(BORDER, 1, 3))
    p = clamp(lt / 5.0); tot = GP[-1][0] - GP[0][0]; xe = GP[0][0] + tot * p
    path = skia.Path(); path.moveTo(*GP[0]); last = GP[0]
    for a, b in zip(GP, GP[1:]):
        if xe >= b[0]: path.lineTo(*b); last = b
        elif xe > a[0]:
            k = (xe - a[0]) / (b[0] - a[0]); last = (xe, a[1] + (b[1] - a[1]) * k); path.lineTo(*last); break
    pt = P(ORANGE, 1, 10); pt.setPathEffect(skia.CornerPathEffect.Make(30)); c.drawPath(path, pt)
    c.drawCircle(last[0], last[1], 14, P(ORANGE)); c.drawCircle(last[0], last[1], 6, P(WHITE))
    if xe > 730:
        k = eob((xe - 730) / 90); c.save(); c.translate(745, 420); c.scale(k, k)
        c.drawCircle(0, 0, 50, P(RED)); icon(c, 'bolt', 0, 0, 52, WHITE); c.restore()
S.append(Scene(16, 20, 'Resilience', [
    Tx(T[16] + 0.5, 'Resilience', 960, 200, 120, 'x', NAVY),
    Tx(T[17], 'What does it mean?', 960, 310, 40, 'm', MUTED, T[18]),
    Cu(T[18] + 0.3, graph),
    Pill(at(18, 'resist'), 'Resist a shock', 520, 790, 38, NAVY, WHITE, 'shield-halved'),
    Pill(at(18, 'adapt'), 'Adapt', 880, 790, 38, NAVY, WHITE, 'rotate'),
    Pill(at(18, 'get back'), 'Back to normal, quickly', 1340, 790, 38, GREEN, WHITE, 'arrow-trend-up'),
    Pill(T[19] + 0.5, 'For a country', 760, 310, 34, OLIGHT, TOM, 'landmark'),
    Pill(T[19] + 1.8, 'For each one of us', 1170, 310, 34, OLIGHT, TOM, 'user')]))

# 5 — risks ---------------------------------------------------------------
RK = [('Extreme', 'cloud-showers-heavy', 'Extreme weather & floods'), ('a long power', 'plug-circle-xmark', 'A long power cut'),
      ('cyberattacks', 'laptop-code', 'Cyberattacks'), ('a pandemic', 'virus-covid', 'A pandemic'),
      ('an industrial', 'radiation', 'Industrial or nuclear accident'), ('a terrorist', 'triangle-exclamation', 'A terrorist threat'),
      ('and even', 'shield-halved', 'Armed conflict')]
e = [Tx(T[20] + 0.2, 'What kind of shocks?', 960, 185, 72, 'x', NAVY, T[21] - 0.1),
     Tx(T[21] + 0.2, 'All kinds of risks, together', 960, 185, 72, 'x', NAVY, T[24] - 0.2)]
for k, (ph, ic, lb) in enumerate(RK):
    x, y = (960 + (k - 1.5) * 410, 400) if k < 4 else (960 + (k - 5) * 410, 670)
    e.append(Tile(at(22, ph), x, y, 380, 240, ic, lb, NAVY if k % 2 == 0 else ORANGE))
e += [Cu(T[24] - 0.1, lambda c, lt: c.drawRect(skia.Rect.MakeXYWH(0, 110, W, 750), P(BG, 0.975))),
      Tx(T[24] + 0.1, 'The idea is not to frighten anyone', 960, 300, 68, 'x', NAVY),
      Tx(T[25], "It's the opposite", 960, 400, 44, 's', ORANGE),
      Pill(at(26, 'you stay'), 'Prepared, you stay calmer', 960, 560, 50, GREEN, WHITE, 'circle-check'),
      Pill(at(26, 'and you can'), 'and you can help others', 960, 690, 50, GREEN, WHITE, 'hand-holding-heart')]
S.append(Scene(20, 27, 'The risks', e))

# 6a — who ----------------------------------------------------------------
S.append(Scene(27, 30, 'The strategy', [
    Tx(T[27] + 0.2, 'Who is behind the strategy?', 960, 190, 68, 'x', NAVY),
    Tile(T[28] + 0.1, 560, 440, 560, 290, 'landmark', 'The Government', NAVY, lsize=38),
    Tile(at(28, 'High'), 1360, 440, 560, 290, 'building-shield', 'High Commission for National Protection', ORANGE, lsize=32),
    Tx(at(28, 'together'), 'together with a group of ministries', 960, 645, 34, 'm', MUTED),
    Pill(T[29] + 0.6, "Luxembourg's first National Resilience Strategy", 960, 730, 38, NAVY, WHITE, 'flag'),
    Pill(at(29, 'launched'), 'Launched in 2025', 960, 818, 36, ORANGE, WHITE, 'calendar-check')]))

# 6b — pillars ------------------------------------------------------------
PL = ['Democracy &\nthe State', 'A resilient\nsociety', 'Essential\nservices', 'A resilient\neconomy',
      'Strategic\nresources', 'Cyber\nresilience', 'Civil\ndefence', 'Military\ndefence']
def pillars(c, lt):
    t = lt + T[30]; step = (T[32] - T[31] - 3.0) / 8
    hi = eio((t - T[32]) / 0.6)
    for i, lb in enumerate(PL):
        x = 960 + (i - 3.5) * 205; r0 = T[31] + 1.0 + i * step
        if t < r0: continue
        k = eoc((t - r0) / 0.7); hgt = 330 * k; base = 710
        cc = mix(NAVY, ORANGE, hi) if i == 1 else NAVY; al = 1.0 if i == 1 else 1 - 0.6 * hi
        rrect(c, x, base + 12, 170, 24, 6, cc, al)
        c.drawRect(skia.Rect.MakeXYWH(x - 58, base - hgt, 116, hgt), P(cc, al))
        for q in (-36, -12, 12, 36):
            c.drawRect(skia.Rect.MakeXYWH(x + q - 3, base - hgt + 6, 6, max(hgt - 12, 0)), P(WHITE, 0.18 * al))
        rrect(c, x, base - hgt - 14, 160, 28, 6, cc, al)
        text(c, str(i + 1), x, base - hgt - 62, 46, 'x', cc, 'c', al * k)
        for j, l in enumerate(lb.split('\n')):
            text(c, l, x, 765 + j * 30, 24, 's', cc if i == 1 else NAVY, 'c', al * k)
S.append(Scene(30, 34, 'The strategy', [
    Tx(T[30] + 0.2, 'Built on eight pillars', 960, 185, 72, 'x', NAVY),
    Cu(T[30], pillars),
    Pill(T[33] + 0.3, 'This pillar is about us', 960, 840, 32, ORANGE, WHITE, 'users')]))

# 7a — households ---------------------------------------------------------
HS = [(400 + cxi * 160, 370 + ryi * 135) for ryi in range(3) for cxi in range(8)]
NEED = [5, 10, 19]; ORD = list(range(24)); R.shuffle(ORD)
def houses(c, lt):
    t = lt + T[34]; th = at(36, 'the helpers')
    for i, (x, y) in enumerate(HS):
        k = clamp((t - (T[36] + 0.4 + ORD[i] * 0.13)) / 0.35)
        if i in NEED:
            pu = 1 + 0.08 * math.sin(t * 6) * k
            icon(c, 'house', x, y, 76 * pu, mix('#9AA7B4', ORANGE, k))
        else:
            icon(c, 'house', x, y, 76, mix('#9AA7B4', GREEN, k))
            if k > 0: c.drawCircle(x + 34, y - 30, 17 * eob(k), P(WHITE)); icon(c, 'circle-check', x + 34, y - 30, 30 * eob(k), GREEN)
    stops = [(T[34] + 0.3, HS[1]), (T[34] + 2.0, HS[14]), (T[34] + 4.0, HS[7]), (T[34] + 6.2, HS[16]), (T[36], HS[3]),
             (th, HS[NEED[0]]), (th + 1.3, HS[NEED[1]]), (th + 2.6, HS[NEED[2]]), (th + 9, HS[NEED[2]])]
    pos = stops[0][1]
    for (ta, pa), (tb, pb) in zip(stops, stops[1:]):
        if t >= ta:
            k = eio((t - ta) / min(tb - ta, 1.1)); pos = (pa[0] + (pb[0] - pa[0]) * k, pa[1] + (pb[1] - pa[1]) * k)
    c.drawCircle(pos[0], pos[1] - 62, 44, P(RED)); icon(c, 'truck-medical', pos[0], pos[1] - 62, 44, WHITE)
S.append(Scene(34, 37, '72 hours', [
    Tx(T[34] + 0.3, 'Emergency services cannot be everywhere at once', 960, 185, 58, 'x', NAVY),
    Cu(T[34], houses),
    Tx(T[36] + 0.3, 'Most households manage on their own for a few days', 960, 795, 40, 's', GREEN, at(36, 'the helpers') - 0.2),
    Tx(at(36, 'the helpers'), 'Helpers can focus on the people who need them most', 960, 795, 40, 's', ORANGE)]))

# 7b — campaign -----------------------------------------------------------
S.append(Scene(37, 40, '72 hours', [
    Pill(T[37] + 0.4, 'October 2026  ·  National campaign', 960, 215, 38, NAVY, WHITE, 'bullhorn'),
    Tx(at(37, 'Bass'), 'Bass du prett?', 960, 410, 190, 'x', ORANGE),
    Tx(T[38] + 0.7, '“Are you ready?”', 960, 560, 64, 's', NAVY),
    Row(T[39] + 2.2, 960, 735, 1060, 150, 'book-open', 'My guide to 72 hours of self-sufficiency', NAVY, size=44)]))

# 7c — 72 hours -----------------------------------------------------------
def counter(c, lt):
    v = int(round(72 * eoc(lt / 1.6)))
    text(c, str(v), 640, 440, 300, 'x', ORANGE); text(c, 'hours', 640, 610, 60, 's', ORANGE)
def day(i):
    x = 960 + (i - 1) * 330
    def fn(c, lt):
        rrect(c, x, 745, 300, 90, 24, NAVY); text(c, f'Day {i + 1}', x, 745, 40, 'b', WHITE)
    return El(T[41] + 1.0 + i * 0.3, fn, x, 745, None, 'pop')
S.append(Scene(40, 43, '72 hours', [
    Tx(T[40] + 0.1, 'Why 72 hours?', 960, 185, 68, 'x', NAVY),
    Cu(T[40] + 0.7, counter),
    Tx(T[41] + 0.7, '= 3 days', 1260, 460, 130, 'x', NAVY),
    day(0), day(1), day(2),
    Tx(T[42] + 0.6, 'Every household, on its own, for the first three days of a crisis', 960, 835, 34, 's', MUTED)]))

# 7d — four parts ---------------------------------------------------------
e = [Tx(T[43] + 0.1, 'The guide has four parts', 960, 185, 68, 'x', NAVY)]
for k, (ic, lb) in enumerate([('triangle-exclamation', 'Understand the risks'), ('tower-broadcast', 'Know how to react'),
                              ('list-check', 'Prepare with a checklist'), ('file-lines', 'Write a personal emergency plan')]):
    e.append(Row(T[44 + k], 960, 325 + k * 132, 1100, 112, ic, lb, ORANGE if k % 2 else NAVY, num=k + 1, size=42))
S.append(Scene(43, 48, '72 hours', e))

# 8a — LU-Alert -----------------------------------------------------------
def phone(c, lt):
    t = lt + T[48] + 0.4; sh = 0
    if T[51] < t < T[51] + 0.9: sh = 7 * math.sin((t - T[51]) * 45) * (1 - (t - T[51]) / 0.9)
    x = 520 + sh
    rrect(c, x, 570, 300, 530, 44, NAVY); rrect(c, x, 570, 268, 480, 26, '#EEF2F6'); rrect(c, x, 322, 90, 10, 5, '#0F2740')
    for j in range(4): rrect(c, x, 520 + j * 62, 220, 40, 10, '#DCE3EA')
    if t > T[51]:
        k = eob((t - T[51]) / 0.5); c.save(); c.translate(x, 400); c.scale(k, k)
        rrect(c, 0, 0, 252, 110, 18, ORANGE); icon(c, 'triangle-exclamation', -88, 0, 44, WHITE)
        text(c, 'LU-Alert', -50, -18, 28, 'x', WHITE, 'l'); rrect(c, 28, 16, 150, 10, 5, WHITE, 0.8); rrect(c, 8, 36, 110, 10, 5, WHITE, 0.6)
        c.restore()
        for j in range(3):
            q = ((t - T[51]) * 0.8 + j / 3) % 1; c.drawCircle(x, 400, 140 + q * 60, P(ORANGE, 0.22 * (1 - q), 5))
e = [Tx(T[48] + 0.1, 'How to react', 960, 175, 68, 'x', NAVY),
     Tx(T[49] + 0.1, 'How do I know that something serious is happening?', 960, 255, 36, 'm', MUTED, T[50] - 0.1),
     Tx(T[50] + 0.2, 'LU-Alert  ·  the national warning system', 960, 255, 40, 's', ORANGE),
     Cu(T[48] + 0.4, phone)]
for k, (ph, ic, lb) in enumerate([('app', 'mobile-screen-button', 'The app'), ('website', 'globe', 'The website'),
                                  ('the media', 'newspaper', 'The media'), ('the sirens', 'bullhorn', 'The sirens')]):
    e.append(Tile(at(52, ph), 1090 + (k % 2) * 330, 440 + (k // 2) * 235, 300, 210, ic, lb, NAVY if k in (0, 3) else ORANGE))
e.append(Pill(T[53] + 0.5, 'More in our LU-Alert episode', 1255, 815, 28, OLIGHT, TOM, 'headphones'))
S.append(Scene(48, 54, 'How to react', e))

# 8b — colours ------------------------------------------------------------
def lvl(i, name, mean, bg, fg):
    y = 320 + i * 132
    def fn(c, lt):
        card(c, 960, y, 1300, 112, 26); rrect(c, 960 - 650 + 170, y, 340, 112, 26, bg)
        text(c, name, 960 - 650 + 170, y, 44, 'x', fg); text(c, mean, 960 - 650 + 390, y, 42, 's', NAVY, 'l')
    return El(T[55 + i], fn, 960, y, None, 'up')
S.append(Scene(54, 59, 'How to react', [
    Tx(T[54] + 0.1, 'The warnings use colours', 960, 185, 68, 'x', NAVY),
    lvl(0, 'Yellow', 'Be aware', '#F2C200', DARK), lvl(1, 'Orange', 'Be careful', '#F28C00', WHITE),
    lvl(2, 'Red', 'Utmost vigilance', '#D62828', WHITE), lvl(3, 'Purple', 'Imminent danger: act immediately', '#7B2CBF', WHITE)]))

# 8c — radio --------------------------------------------------------------
def radio(c, lt):
    for j in range(3):
        q = (lt * 0.6 + j / 3) % 1; c.drawCircle(960, 360, 90 + q * 130, P(ORANGE, 0.3 * (1 - q), 5))
    c.drawCircle(960, 360, 100, P(NAVY)); icon(c, 'radio', 960, 360, 96, WHITE)
S.append(Scene(59, 63, 'How to react', [
    Tx(T[59] + 0.1, 'The radio is very important', 960, 180, 68, 'x', NAVY),
    El(T[59] + 0.5, radio, 960, 360, None, 'pop'),
    Tx(T[60] + 0.5, 'No power, no internet? A radio still works.', 960, 535, 40, 's', ORANGE),
    Tile(at(60, 'a radio with'), 560, 715, 370, 210, 'battery-full', 'Battery radio'),
    Tile(T[61] + 0.2, 960, 715, 370, 210, 'rotate', 'Wind-up radio', ORANGE),
    Tile(T[62] + 0.3, 1360, 715, 370, 210, 'car', 'Car radio')]))

# 8d — numbers ------------------------------------------------------------
def num(x, n, lb, ic, color):
    def fn(c, lt):
        card(c, x, 450, 620, 390); text(c, n, x, 400, 210, 'x', color)
        icon(c, ic, x - tw(lb, 36, 's') / 2 - 36, 580, 36, color); text(c, lb, x + 22, 580, 36, 's', NAVY)
    return fn
S.append(Scene(63, 66, 'How to react', [
    Tx(T[63] + 0.1, 'The emergency numbers stay the same', 960, 180, 60, 'x', NAVY),
    El(at(63, '112'), num(610, '112', 'Fire and rescue services', 'fire-extinguisher', ORANGE), 610, 450, None, 'pop'),
    El(at(63, 'and 1-1-3'), num(1310, '113', 'Police', 'shield-halved', NAVY), 1310, 450, None, 'pop'),
    Pill(T[64] + 0.2, 'Only for a real emergency', 610, 760, 38, RED, WHITE, 'triangle-exclamation'),
    Pill(T[65] + 0.8, 'Keep calls short, keep lines free', 1310, 760, 36, NAVY, WHITE, 'phone')]))

# 8e — check info ---------------------------------------------------------
S.append(Scene(66, 68, 'How to react', [
    Tx(T[66] + 0.6, 'Check information before you share it', 960, 190, 64, 'x', NAVY),
    Tile(T[67] + 0.1, 610, 480, 600, 320, 'circle-check', 'Trust the official sources', GREEN, lsize=38),
    Pill(at(67, 'infocrise'), 'infocrise.lu', 610, 740, 44, NAVY, WHITE, 'globe'),
    Tile(at(67, "and don't"), 1310, 480, 600, 320, 'comment-slash', "Don't pass on rumours", RED, lsize=38)]))

# 9a — water --------------------------------------------------------------
def bottles(c, lt):
    for j in range(3):
        x = 440 + j * 120; k = eio((lt - j * 0.45) / 0.8)
        rrect(c, x, 372, 34, 30, 6, NAVY); rrect(c, x, 510, 92, 240, 22, NAVY, 1, 6)
        hh = 228 * k
        if hh > 2:
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 40, 396, 80, 228), 16, 16), True)
            c.drawRect(skia.Rect.MakeXYWH(x - 40, 624 - hh, 80, hh), P('#2E86C1')); c.restore()
        text(c, '1 L', x, 520, 30, 'x', WHITE if k > 0.6 else NAVY)
    text(c, 'At least 3 litres', 560, 690, 44, 'x', NAVY); text(c, 'per person, per day', 560, 745, 34, 'm', MUTED)
def w9(c, lt):
    text(c, '× 3 days', 1010, 430, 48, 's', MUTED)
def fam(c, lt):
    for j in range(4): icon(c, 'user', 1500 + (j - 1.5) * 62, 430, 54, ORANGE)
S.append(Scene(68, 73, 'The checklist', [
    Tx(T[68] + 0.1, 'My 72-hour checklist', 960, 180, 72, 'x', NAVY),
    Tx(T[69] + 0.1, 'What should I have at home?', 960, 265, 38, 'm', MUTED, T[70] - 0.1),
    Tx(T[70] + 0.1, 'First: water', 960, 265, 42, 's', ORANGE),
    Cu(at(70, 'at least') - 0.3, bottles),
    Cu(T[71] + 0.8, w9), Tx(at(71, 'nine'), '9 litres', 1010, 540, 110, 'x', NAVY), Tx(at(71, 'nine') + 0.3, 'for each person', 1010, 640, 34, 'm', MUTED),
    Cu(T[72] + 0.3, fam), Tx(at(72, 'thirty'), '36 litres', 1500, 540, 110, 'x', ORANGE), Tx(at(72, 'thirty') + 0.3, 'for a family of four', 1500, 640, 34, 'm', MUTED)]))

# 9b/c — checklist grid ---------------------------------------------------
CK = [(T[73] - 0.0, 'bottle-water', 'Water'), (T[73] + 0.9, 'jar', 'Food that keeps'), (T[75] + 0.9, 'utensils', 'Tin opener'),
      (T[76] + 0.5, 'paw', 'Pet food'), (T[77] + 0.3, 'fire-burner', 'Small gas stove'),
      (at(81, 'A torch'), 'lightbulb', 'Torch & spare batteries'), (at(81, 'candles'), 'fire', 'Candles & matches'),
      (at(81, 'and blankets'), 'bed', 'Blankets, sleeping bags'), (at(82, 'a first'), 'kit-medical', 'First aid kit'),
      (at(82, 'and the medicines'), 'pills', 'Regular medicines'), (at(83, 'toilet'), 'toilet-paper', 'Hygiene products'),
      (at(84, 'the radio'), 'radio', 'Radio'), (at(84, 'and a power'), 'battery-full', 'Power bank'),
      (T[85] + 1.6, 'money-bill-wave', 'Cash'), (at(87, 'keep copies'), 'id-card', 'Copies of documents')]
GXY = [(960 + (k % 5 - 2) * 345, 320 + (k // 5) * 222) for k in range(15)]
MISS = [4, 7, 12, 13]
e = [Tx(T[73] + 0.1, 'My 72-hour checklist', 960, 165, 48, 'x', NAVY, T[88] - 0.2)]
for k, (t0, ic, lb) in enumerate(CK):
    e.append(Tile(t0 + 0.25, GXY[k][0], GXY[k][1], 325, 200, ic, lb, ORANGE if k % 2 else NAVY))
def warn(c, lt):
    c.drawRect(skia.Rect.MakeXYWH(0, 110, W, 750), P(BG, 0.9))
    rrect(c, 960, 480, 1400, 300, 40, RED); icon(c, 'triangle-exclamation', 400, 480, 130, WHITE)
    textbox(c, 'Never use a barbecue or a generator inside the house', 1090, 440 if lt > T[79] - T[78] else 480, 52, 'x', WHITE, 1050)
    if lt > T[79] - T[78]: text(c, 'The fumes can kill.', 1090, 570, 40, 's', '#FFE3DE', 'c', clamp((lt - (T[79] - T[78])) / 0.3))
def ticks(c, lt):
    t = lt + T[88]; n = 0
    for k, (x, y) in enumerate(GXY):
        bx, by = x + 130, y - 72
        if k in MISS:
            q = eob((t - T[91] - 0.3 - MISS.index(k) * 0.15) / 0.4)
            if t > T[91] + 0.3 + MISS.index(k) * 0.15:
                rrect(c, x, y, 325, 200, 28, ORANGE, 1, 6); c.drawCircle(bx, by, 26 * q, P(ORANGE)); text(c, '?', bx, by, 34 * q, 'x', WHITE)
        else:
            t0 = T[90] + 0.8 + n * 0.16; n += 1
            if t > t0:
                q = eob((t - t0) / 0.4); c.drawCircle(bx, by, 26 * q, P(WHITE)); icon(c, 'circle-check', bx, by, 50 * q, GREEN)
e += [El(T[78] + 0.1, warn, 960, 480, T[80] - 0.3, 'fade'),
      Tx(T[88] + 0.1, 'A long list?', 960, 165, 48, 'x', NAVY, T[90] - 0.1),
      Tx(T[90] + 0.3, 'You probably have many of these things already', 960, 165, 48, 'x', GREEN, T[91] - 0.1),
      Tx(T[91] + 0.1, 'The checklist shows what is missing', 960, 165, 48, 'x', ORANGE, T[92] - 0.1),
      Cu(T[88], ticks),
      Pill(T[92] + 0.3, 'Check your kit at least twice a year', 960, 165, 40, NAVY, WHITE, 'calendar-check')]
S.append(Scene(73, 93, 'The checklist', e))

# 10a — the plan ----------------------------------------------------------
FL = [('Who', 'Household members'), ('phone', 'Phone numbers'), ('allergies', 'Allergies'), ('regular', 'Regular medication')]
def paper(c, lt):
    t = lt + T[94]
    card(c, 520, 545, 560, 580, 24); rrect(c, 520, 300, 560, 90, 24, ORANGE); c.drawRect(skia.Rect.MakeXYWH(240, 310, 560, 36), P(ORANGE))
    icon(c, 'file-lines', 300, 300, 40, WHITE); text(c, 'Personal emergency plan', 340, 300, 32, 'x', WHITE, 'l')
    for j, (ph, lb) in enumerate(FL):
        y = 420 + j * 105; text(c, lb, 280, y - 22, 26, 's', MUTED, 'l')
        rrect(c, 520, y + 22, 480, 44, 10, '#F0F2F4')
        k = eoc((t - at(97, ph)) / 1.2)
        if k > 0: c.drawRoundRect(skia.Rect.MakeXYWH(292, y + 14, 380 * k * (0.75 + 0.25 * ((j * 37) % 5) / 4), 16), 8, 8, P(NAVY))
S.append(Scene(93, 98, 'The emergency plan', [
    Tx(T[93] + 0.2, 'My personal emergency plan', 960, 175, 70, 'x', NAVY),
    Cu(T[94], paper),
    Row(T[95] + 0.6, 1340, 430, 860, 150, 'users', 'Fill it in together with the people you live with', NAVY, size=36),
    Row(at(95, 'and that you share'), 1340, 620, 860, 150, 'share-nodes', 'Share it with family and friends', ORANGE, size=36)]))

# 10b — at home -----------------------------------------------------------
e = [Tx(T[98] + 0.1, 'At home: where is everything?', 960, 185, 66, 'x', NAVY)]
for k, (ic, lb) in enumerate([('faucet-drip', 'Main water valve'), ('toggle-off', 'Circuit breaker'),
                              ('fire-extinguisher', 'Fire extinguisher'), ('warehouse', 'Garage door without electricity')]):
    e.append(Tile(T[99 + k] + 0.2, 960 + (k - 1.5) * 415, 470, 385, 300, ic, lb, ORANGE if k % 2 else NAVY))
def qm(c, lt):
    w = 1 + 0.08 * math.sin(lt * 7); c.drawCircle(1740, 320, 48 * w, P(RED)); text(c, '?', 1740, 320, 64 * w, 'x', WHITE)
e += [El(T[103] + 0.3, qm, 1740, 320, None, 'pop'),
      Pill(T[104] + 0.2, 'Find out now, not in the dark', 960, 760, 46, NAVY, WHITE, 'lightbulb')]
S.append(Scene(98, 105, 'The emergency plan', e))

# 10c — meeting places ----------------------------------------------------
def mp(c, lt):
    t = lt + T[105] + 0.6
    card(c, 560, 530, 760, 500, 30); c.save(); c.clipRect(skia.Rect.MakeXYWH(190, 290, 740, 480))
    for (x1, y1, x2, y2) in [(180, 420, 940, 480), (180, 650, 940, 600), (380, 280, 440, 790), (700, 280, 660, 790), (180, 540, 520, 300)]:
        c.drawLine(x1, y1, x2, y2, P('#E6EAEE', 1, 26))
    c.restore()
    for j, (x, y) in enumerate([(410, 450), (720, 610)]):
        t0 = T[106] + 0.4 + j * 0.7
        if t > t0:
            k = eob((t - t0) / 0.5); dy = (1 - eoc((t - t0) / 0.4)) * -120
            c.drawOval(skia.Rect.MakeXYWH(x - 24 * k, y + 2, 48 * k, 14), P('#000000', 0.15))
            icon(c, 'location-dot', x, y - 50 + dy, 100, ORANGE if j == 0 else NAVY)
            text(c, f'Meeting place {j + 1}', x, y + 46, 26, 'b', NAVY, 'c', clamp((t - t0 - 0.3) / 0.3))
S.append(Scene(105, 109, 'The emergency plan', [
    Tx(T[105] + 0.2, 'Where do we meet if we cannot go home?', 960, 185, 60, 'x', NAVY),
    Cu(T[105] + 0.6, mp),
    Row(T[107] + 0.2, 1400, 430, 760, 170, 'school', 'Who collects the children from school?', ORANGE, size=36),
    Row(T[108] + 0.2, 1400, 640, 760, 170, 'person-walking', 'How do I get home without a car or public transport?', NAVY, size=34)]))

# 10d — neighbourhood -----------------------------------------------------
HX = [960 + (i - 2) * 310 for i in range(5)]
def nb(c, lt):
    t = lt + T[109]
    def arrow(x1, x2, y, color, k):
        if k <= 0: return
        xe = x1 + (x2 - x1) * eoc(k); c.drawLine(x1, y, xe, y, P(color, 1, 9)); d = 1 if x2 > x1 else -1
        pa = skia.Path(); pa.moveTo(xe + d * 22, y); pa.lineTo(xe - d * 6, y - 18); pa.lineTo(xe - d * 6, y + 18); pa.close(); c.drawPath(pa, P(color))
    arrow(HX[1] + 90, HX[2] - 100, 470, GREEN, (t - T[110]) / 0.7); arrow(HX[3] - 90, HX[2] + 100, 470, GREEN, (t - T[110] - 0.3) / 0.7)
    arrow(HX[2] - 95, HX[1] + 95, 560, ORANGE, (t - T[111] - 0.3) / 0.7); arrow(HX[2] + 95, HX[3] - 95, 560, ORANGE, (t - T[111] - 0.5) / 0.7)
    for i, x in enumerate(HX):
        k = eob((t - T[109] - 0.3 - abs(i - 2) * 0.2) / 0.5)
        if t < T[109] + 0.3 + abs(i - 2) * 0.2: continue
        c.save(); c.translate(x, 520); c.scale(k, k); icon(c, 'house-chimney', 0, 0, 150, ORANGE if i == 2 else NAVY)
        if i == 2: text(c, 'Me', 0, 110, 32, 'x', ORANGE)
        c.restore()
def badge(x, ic, lb, color):
    def fn(c, lt):
        c.drawCircle(x, 385, 46, P(color)); icon(c, ic, x, 385, 46, WHITE); text(c, lb, x, 640, 30, 's', color)
    return fn
S.append(Scene(109, 116, 'The emergency plan', [
    Tx(T[109] + 0.1, 'The neighbourhood', 960, 180, 70, 'x', NAVY),
    Cu(T[109], nb),
    Tx(T[110] + 0.1, 'Who could help me?', 960, 285, 46, 's', GREEN, T[111] - 0.1),
    Tx(T[111] + 0.1, 'And who might need my help?', 960, 285, 46, 's', ORANGE, T[114] - 0.2),
    El(T[112] + 0.3, badge(HX[1], 'kit-medical', 'Knows first aid', GREEN), HX[1], 385, None, 'pop'),
    El(T[113] + 0.5, badge(HX[3], 'person-cane', 'Lives alone', ORANGE), HX[3], 385, None, 'pop'),
    Pill(T[114] + 0.2, "That's very Biergerpakt", 960, 285, 40, ORANGE, WHITE, 'handshake'),
    Tx(T[115] + 0.2, 'When we know our neighbours, everyone is stronger', 960, 780, 46, 'x', NAVY)]))

# 10e — on paper ----------------------------------------------------------
S.append(Scene(116, 118, 'The emergency plan', [
    Tx(T[116] + 0.1, 'Keep the plan on paper too', 960, 190, 70, 'x', NAVY),
    Tile(T[116] + 0.6, 620, 500, 540, 340, 'file-circle-check', 'On paper', GREEN, lsize=40),
    Tile(at(116, 'not only'), 1300, 500, 540, 340, 'mobile-screen-button', 'Not only on your phone', NAVY, lsize=40),
    Pill(T[117] + 0.2, 'A battery can run out', 1300, 760, 40, RED, WHITE, 'battery-empty')]))

# 11 — where --------------------------------------------------------------
e = [Tx(T[118] + 0.1, 'Where can you find all this?', 960, 165, 56, 'x', NAVY),
     Pill(T[119] + 0.2, 'letzprepare.lu', 960, 275, 64, NAVY, WHITE, 'globe')]
for k, (ph, ic, lb) in enumerate([('the guide', 'book-open', 'The guide'), ('the checklist', 'list-check', 'The checklist'),
                                  ('and the emergency', 'file-lines', 'The emergency plan')]):
    e.append(Tile(at(120, ph), 960 + (k - 1) * 370, 475, 345, 215, ic, lb, ORANGE if k == 1 else NAVY))
e.append(Pill(at(120, 'for free'), 'Free', 1650, 475, 40, GREEN, WHITE, 'download'))
for k, (ph, lb) in enumerate([('Luxembourgish', 'Lëtzebuergesch'), ('French', 'Français'), ('German', 'Deutsch'), ('English', 'English'), ('Portuguese', 'Português')]):
    e.append(Pill(at(121, ph), lb, 960 + (k - 2) * 300, 655, 34, OLIGHT, TOM))
e += [Pill(at(122, 'infocrise') - 1.0, 'infocrise.lu', 430, 790, 46, ORANGE, WHITE, 'globe'),
      Pill(at(122, 'a power'), 'Power cut', 840, 790, 32, WHITE, NAVY, 'plug-circle-xmark'),
      Pill(at(122, 'a flood'), 'Flood', 1130, 790, 32, WHITE, NAVY, 'house-flood-water'),
      Pill(at(122, 'a nuclear'), 'Nuclear alert', 1440, 790, 32, WHITE, NAVY, 'circle-radiation')]
S.append(Scene(118, 123, 'Where to find it', e))

# 12 — recap --------------------------------------------------------------
e = [Tx(T[123] + 0.1, 'What to remember', 960, 175, 68, 'x', NAVY, T[130] - 0.3)]
for k, (i, ic, lb) in enumerate([(125, 'shield-halved', "Lëtz prepare: Luxembourg's National Resilience Strategy"),
                                 (127, 'clock', 'Every household: on its own for 72 hours'),
                                 (128, 'list-check', 'Water, food, light, a radio, medicines, cash, documents'),
                                 (129, 'people-roof', 'Fill in your emergency plan, and talk to your neighbours')]):
    e.append(Row(T[i] + 0.2, 960, 310 + k * 135, 1500, 112, ic, lb, ORANGE if k % 2 else NAVY, T[130] - 0.3, num=k + 1, size=38))
e += [Tx(T[130] + 0.1, 'A little preparation today', 960, 370, 92, 'x', NAVY),
      Tx(T[130] + 1.3, 'makes a big difference tomorrow.', 960, 490, 92, 'x', ORANGE),
      Tx(T[131] + 0.2, 'Together, we are stronger.', 960, 680, 60, 's', NAVY)]
S.append(Scene(123, 132, 'To remember', e))

# 13 — outro --------------------------------------------------------------
tb = T[135] - 0.3; ty = T[138] - 0.2
e = [Tx(T[132] + 0.2, 'That was our episode about Lëtz prepare', 960, 420, 64, 'x', NAVY, T[133] - 0.2),
     Tx(T[133] + 0.2, 'Biergerpakt', 960, 215, 130, 'x', ORANGE, ty),
     Tx(T[133] + 1.6, 'Living together in Luxembourg: discover the country, meet new people', 960, 325, 38, 's', NAVY, ty)]
for k, (ph, ic, lb) in enumerate([('guided visits', 'map-location-dot', 'Guided visits'), ('online information', 'laptop', 'Online information sessions'),
                                  ('a language', 'language', 'Language learning app'), ('creative', 'palette', 'Creative workshops'),
                                  ('training', 'graduation-cap', 'Training sessions')]):
    e.append(Tile(at(134, ph), 960 + (k - 2) * 345, 530, 325, 250, ic, lb, ORANGE if k % 2 else NAVY, tb))
e += [Pill(at(134, 'simply head'), 'biergerpakt.lu', 960, 775, 60, NAVY, WHITE, 'globe', ty),
      Row(T[135] + 0.2, 960, 465, 1200, 120, 'users', 'Open to all residents and to cross-border workers', NAVY, ty, size=40),
      Row(T[136] + 0.2, 960, 615, 1200, 120, 'gift', 'All activities are free of charge', ORANGE, ty, size=40),
      El(T[138] + 0.1, logo, 960, 285, None, 'pop'),
      Tx(T[138] + 0.3, 'Thank you for listening!', 960, 480, 100, 'x', NAVY),
      Tx(T[139] + 0.2, 'See you next time', 960, 600, 52, 's', ORANGE),
      Pill(T[139] + 0.8, 'biergerpakt.lu', 960, 745, 54, NAVY, WHITE, 'globe')]
S.append(Scene(132, 141, 'Biergerpakt', e))
