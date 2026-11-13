"""Gera assets/banner-neon.svg — banner pixel neon animado do perfil.

Tudo é desenhado em código (pixel art com <rect>) e animado só com CSS,
que é o que o GitHub aceita dentro de um SVG exibido como <img>.

Uso:  python .github/scripts/gerar_banner_neon.py
"""
import math
from pathlib import Path

W, H = 1000, 280
OUT = Path(__file__).resolve().parents[2] / "assets" / "banner-neon.svg"

BG = "#110a14"
PINK = "#ff5fa2"
PINK_L = "#ff9ccf"
WHITE = "#f6e9f2"

parts = []  # pedaços de SVG
CSS_EXTRA = []  # keyframes gerados no meio do desenho
add = parts.append


# ---------------------------------------------------------------- utilidades
def darken(hex_color, f=0.45):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


class Grid:
    """Grade de pixels; cada célula guarda uma cor (ou None)."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.c = [[None] * w for _ in range(h)]

    def set(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.c[y][x] = col

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.c[y][x]
        return None

    def rect(self, x0, y0, x1, y1, col):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, col)

    def ellipse(self, cx, cy, rx, ry, col, cond=None):
        for y in range(self.h):
            for x in range(self.w):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    if cond is None or cond(x, y):
                        self.set(x, y, col)

    def outline(self, col=None):
        add_cells = []
        for y in range(self.h):
            for x in range(self.w):
                if self.c[y][x] is None:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        n = self.get(x + dx, y + dy)
                        if n is not None:
                            add_cells.append((x, y, col or darken(n)))
                            break
        for x, y, c in add_cells:
            self.c[y][x] = c

    def svg(self, ox, oy, s):
        """Converte em <rect>s, juntando pixels vizinhos da mesma cor."""
        out = []
        for y in range(self.h):
            x = 0
            while x < self.w:
                col = self.c[y][x]
                if col is None:
                    x += 1
                    continue
                x2 = x
                while x2 + 1 < self.w and self.c[y][x2 + 1] == col:
                    x2 += 1
                out.append(f'<rect x="{ox + x * s}" y="{oy + y * s}" width="{(x2 - x + 1) * s}" height="{s}" fill="{col}"/>')
                x = x2 + 1
        return "".join(out)


# ---------------------------------------------------------------- fonte 5x7
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "&": [".##..", "#..#.", ".##..", ".##.#", "#..#.", "#..#.", ".##.#"],
    ">": ["#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."],
    " ": ["....."] * 7,
}


def glyph(ch, x, y, p, fill, gap=1, rx=0):
    out = []
    for r, row in enumerate(FONT[ch]):
        for c, v in enumerate(row):
            if v == "#":
                out.append(f'<rect x="{x + c * p}" y="{y + r * p}" width="{p - gap}" height="{p - gap}" rx="{rx}" fill="{fill}"/>')
    return "".join(out)


def text_width(s, p):
    return len(s) * 6 * p - p


# ---------------------------------------------------------------- estilos
CSS = """
.tw{animation:tw 3s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes tw{0%,100%{opacity:.15;transform:scale(.6)}50%{opacity:1;transform:scale(1)}}
.ch{opacity:0;animation:show .01s linear forwards}
@keyframes show{to{opacity:1}}
.cur{opacity:0;animation:show .01s linear forwards,blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.drop{opacity:0;animation:drop .5s cubic-bezier(.2,1.6,.4,1) forwards}
@keyframes drop{from{opacity:0;transform:translateY(-30px)}to{opacity:1;transform:translateY(0)}}
.wave{animation:wave 3.2s ease-in-out infinite}
@keyframes wave{0%,100%{opacity:1}50%{opacity:.55}}
.neon{animation:neon 7s linear 3s infinite}
@keyframes neon{0%,86%,90%,94%,100%{opacity:1}88%,92%{opacity:.35}}
.fade{opacity:0;animation:fade .8s ease-out forwards}
@keyframes fade{to{opacity:1}}
.lineL{transform-box:fill-box;transform-origin:right;transform:scaleX(0);animation:grow .7s ease-out forwards}
.lineR{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:grow .7s ease-out forwards}
@keyframes grow{to{transform:scaleX(1)}}
.tag{animation:tag 4.5s ease-in-out infinite}
@keyframes tag{0%,100%{fill:#cdbdcb}12%,22%{fill:#ff7ab8}}
.beat{transform-box:fill-box;transform-origin:center;animation:beat 1.2s ease-in-out infinite}
@keyframes beat{0%,100%{transform:scale(1)}15%{transform:scale(1.3)}30%{transform:scale(1)}45%{transform:scale(1.18)}}
.bob{animation:bob 2.6s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.blink{opacity:0;animation:eyes 4.2s steps(1) infinite}
@keyframes eyes{0%,90%{opacity:0}91%,95%{opacity:1}96%,100%{opacity:0}}
.typeL{animation:typ .32s steps(1) infinite}
.typeR{animation:typ .32s steps(1) .16s infinite}
@keyframes typ{0%{transform:translateY(0)}50%{transform:translateY(-3px)}}
.screen{animation:scr 2s ease-in-out infinite}
@keyframes scr{0%,100%{opacity:.75}50%{opacity:1}}
.ph{animation:ph 2s ease-in-out infinite}
@keyframes ph{0%,100%{opacity:1}50%{opacity:.6}}
.tail{transform-box:fill-box;transform-origin:left bottom;animation:tail 2.4s ease-in-out infinite}
@keyframes tail{0%,100%{transform:rotate(0)}50%{transform:rotate(-14deg)}}
.ear{transform-box:fill-box;transform-origin:bottom;animation:ear 5s ease-in-out infinite}
@keyframes ear{0%,88%,100%{transform:rotate(0)}91%{transform:rotate(-18deg)}94%{transform:rotate(0)}}
.breath{transform-box:fill-box;transform-origin:bottom;animation:breath 3s ease-in-out infinite}
@keyframes breath{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.05)}}
.z{opacity:0;animation:z 3.6s ease-out infinite}
@keyframes z{0%{opacity:0;transform:translate(0,0)}20%{opacity:1}100%{opacity:0;transform:translate(14px,-26px)}}
.float{animation:float 5s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 3.4s ease-in-out infinite}
@keyframes spin{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.15)}}
.bar{transform-box:fill-box;transform-origin:bottom;animation:bar 2.8s ease-in-out infinite}
@keyframes bar{0%,100%{transform:scaleY(.35)}50%{transform:scaleY(1)}}
.pulse{stroke-dasharray:14 400;animation:pulse 4s linear infinite}
@keyframes pulse{from{stroke-dashoffset:414}to{stroke-dashoffset:0}}
.node{animation:node 2s ease-in-out infinite}
@keyframes node{0%,100%{opacity:.35}50%{opacity:1}}
.floor{animation:floor 1.6s linear infinite}
@keyframes floor{from{transform:translateY(0)}to{transform:translateY(10px)}}
.frame{animation:frame 4s ease-in-out infinite}
@keyframes frame{0%,100%{stroke-opacity:.45}50%{stroke-opacity:.95}}
"""

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
    f'aria-label="Hello world! I am Tamires — AI &amp; Data Science">')
STYLE_AT = len(parts)
add("")
add('<defs>'
    '<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.4" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    '<filter id="glow2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    f'<clipPath id="r"><rect width="{W}" height="{H}" rx="16"/></clipPath>'
    '<clipPath id="floorclip"><rect x="0" y="236" width="1000" height="44"/></clipPath>'
    '<radialGradient id="bgl" cx="70%" cy="55%" r="55%"><stop offset="0" stop-color="#3a1233" stop-opacity=".55"/>'
    '<stop offset="1" stop-color="#3a1233" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5fa2" stop-opacity="0"/>'
    '<stop offset="1" stop-color="#ff5fa2" stop-opacity=".55"/></linearGradient>'
    '<mask id="floormask"><rect x="0" y="236" width="1000" height="44" fill="url(#fl)"/></mask>'
    '</defs>')
add('<g clip-path="url(#r)">')
add(f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#bgl)"/>')

# ---------------------------------------------------------------- piso em grade
fl = ['<g clip-path="url(#floorclip)"><g mask="url(#floormask)" stroke="#ff5fa2" stroke-width="1.2" fill="none">']
vx, vy = 640, 150
for i in range(-14, 15):
    bx = vx + i * 70
    fl.append(f'<line x1="{vx}" y1="{vy}" x2="{bx}" y2="{H + 40}"/>')
fl.append('<g class="floor">')
for y in range(226, 300, 10):
    fl.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
fl.append('</g></g></g>')
add("".join(fl))

# ---------------------------------------------------------------- circuitos (esquerda)
circ = [
    "M0 70 H30 L45 85 V120",
    "M0 100 H18 L30 112 V150 L44 164",
    "M0 190 H22 L36 176 H58",
    "M0 225 H40 L52 213 H74",
]
for i, d in enumerate(circ):
    add(f'<path d="{d}" stroke="#5c2048" stroke-width="2" fill="none"/>')
    add(f'<path class="pulse" d="{d}" stroke="{PINK}" stroke-width="2.4" fill="none" filter="url(#glow)" '
        f'style="animation-delay:{i * 0.9:.1f}s"/>')
for i, (x, y) in enumerate([(45, 124), (44, 168), (62, 176), (78, 213)]):
    add(f'<circle class="node" cx="{x}" cy="{y}" r="4" fill="none" stroke="{PINK}" stroke-width="2" '
        f'style="animation-delay:{i * 0.5:.1f}s"/>')

# ---------------------------------------------------------------- estrelinhas
def sparkle(x, y, size, col, delay, dur):
    s = size
    g = (f'<rect x="{-s}" y="{-s * 3}" width="{s * 2}" height="{s * 6}" fill="{col}"/>'
         f'<rect x="{-s * 3}" y="{-s}" width="{s * 6}" height="{s * 2}" fill="{col}"/>')
    return (f'<g transform="translate({x} {y})"><g class="tw" style="animation-delay:{delay}s;animation-duration:{dur}s">'
            f'{g}</g></g>')


stars = [(70, 40, 3, "#ff8a7a", 0, 2.6), (95, 62, 2, "#ff8a7a", .8, 3.1), (150, 28, 1, WHITE, 1.2, 2.4),
         (250, 18, 1, WHITE, .3, 3.3), (420, 22, 1, WHITE, 2.0, 2.8), (520, 92, 1, WHITE, 1.5, 3.0),
         (585, 150, 1, PINK_L, .6, 2.5), (620, 200, 2, PINK_L, 1.9, 3.4), (700, 30, 1, WHITE, .9, 2.7),
         (770, 110, 1, WHITE, 2.3, 3.2), (960, 30, 2, WHITE, .4, 2.9), (975, 200, 1, PINK_L, 1.1, 2.6),
         (830, 110, 1, WHITE, 1.7, 3.0), (30, 255, 1, WHITE, 2.5, 2.8), (330, 262, 1, PINK_L, .2, 3.1)]
for st in stars:
    add(sparkle(*st))
for i, (x, y) in enumerate([(200, 60), (300, 150), (470, 160), (560, 40), (640, 250), (930, 245), (820, 20)]):
    add(f'<rect class="tw" x="{x}" y="{y}" width="2" height="2" fill="{WHITE}" style="animation-delay:{i * 0.45:.2f}s"/>')

# ---------------------------------------------------------------- textos
CX = 330  # centro do bloco de texto
t = 0.4   # relógio da animação de entrada

# linha 1: "> HELLO WORLD! I AM" digitando
p1 = 4
l1 = "HELLO WORLD! I AM"
full = "> " + l1
x0 = CX - text_width(full, p1) // 2
y1 = 54
add(f'<g filter="url(#glow)">{glyph(">", x0, y1, p1, PINK, rx=1)}</g>')
xs = x0 + 2 * 6 * p1
add('<g filter="url(#glow)">')
for i, ch in enumerate(l1):
    if ch != " ":
        add(f'<g class="ch" style="animation-delay:{t + i * 0.09:.2f}s">{glyph(ch, xs + i * 6 * p1, y1, p1, WHITE, rx=1)}</g>')
add('</g>')
t_end1 = t + len(l1) * 0.09
add(f'<rect class="cur" x="{xs + len(l1) * 6 * p1 + 2}" y="{y1 - 2}" width="5" height="{7 * p1 + 4}" fill="{PINK}" '
    f'style="animation-delay:{t_end1:.2f}s,{t_end1:.2f}s"/>')

# linha 2: TAMIRES em letreiro neon
p2 = 10
l2 = "TAMIRES"
x2 = CX - text_width(l2, p2) // 2
y2 = 100
t2 = t_end1 + 0.15
add('<g class="neon" filter="url(#glow2)">')
for i, ch in enumerate(l2):
    add(f'<g class="drop" style="animation-delay:{t2 + i * 0.12:.2f}s"><g class="wave" style="animation-delay:{i * 0.22:.2f}s">'
        f'{glyph(ch, x2 + i * 6 * p2, y2, p2, "#ff7ab8", gap=1, rx=1)}</g></g>')
add('</g>')
t5 = t2 + len(l2) * 0.12 + 0.4

# linha 3: tags acendendo em sequência
tags = [("AI", 20), ("PYTHON", 60), ("DATA SCIENCE", 120), ("MACHINE LEARNING", 160)]
gapt = 32
xt = CX - (sum(w for _, w in tags) + gapt * (len(tags) - 1)) // 2
add(f'<g class="fade" style="animation-delay:{t5:.2f}s" font-family="\'Courier New\',Courier,monospace" font-size="14" '
    f'font-weight="bold">')
for i, (tg, w) in enumerate(tags):
    add(f'<text class="tag" x="{xt}" y="214" fill="#cdbdcb" textLength="{w}" lengthAdjust="spacingAndGlyphs" '
        f'style="animation-delay:{i * 1.1:.1f}s">{tg}</text>')
    xt += w
    if i < len(tags) - 1:
        add(f'<rect class="node" x="{xt + gapt // 2 - 3}" y="205" width="5" height="5" fill="{PINK}" '
            f'style="animation-delay:{i * 0.5:.1f}s"/>')
        xt += gapt
add('</g>')

# ---------------------------------------------------------------- gema
gem = Grid(11, 11)
for y in range(11):
    for x in range(11):
        if abs(x - 5) + abs(y - 5) <= 5:
            gem.set(x, y, "#b8306f" if x < 5 else ("#e2508f" if y < 5 else "#8c2054"))
gem.set(3, 3, "#ff9ccf"); gem.set(4, 2, "#ff9ccf"); gem.set(3, 4, "#ff9ccf")
add(f'<g class="float" style="animation-duration:4s"><g class="spin" filter="url(#glow)">{gem.svg(590, 34, 4)}</g></g>')

# ---------------------------------------------------------------- janela com gráfico
wx, wy = 846, 20
add(f'<g class="float" style="animation-duration:6s;animation-delay:1s" filter="url(#glow)">'
    f'<rect x="{wx}" y="{wy}" width="96" height="62" rx="3" fill="#1a0e1c" stroke="{PINK}" stroke-width="2.5"/>'
    f'<rect x="{wx}" y="{wy}" width="96" height="11" rx="3" fill="#3a1233"/>'
    + "".join(f'<rect x="{wx + 6 + i * 7}" y="{wy + 4}" width="4" height="4" fill="{PINK_L}"/>' for i in range(3)))
for i, (h, d) in enumerate([(12, 0), (22, .4), (18, .8), (32, 1.2), (26, 1.6), (40, 2.0)]):
    add(f'<rect class="bar" x="{wx + 10 + i * 13}" y="{wy + 56 - h}" width="8" height="{h}" fill="{PINK if i % 2 else PINK_L}" '
        f'style="animation-delay:{d}s"/>')
add('</g>')


def line_cells(g, x0, y0, x1, y1, col, thick=3):
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n)
        y = round(y0 + (y1 - y0) * i / n)
        for dx in range(thick):
            g.set(x + dx - thick // 2, y, col)


# ---------------------------------------------------------------- avatar
HAIR, HAIR_S, HAIR_L = "#f2cf78", "#d3a24a", "#fff1bd"
SKIN, SKIN_S = "#ffdcc8", "#f0b49a"
PH, PH_S = "#ff7ab8", "#c2386f"
TOP, TOP_S = "#b83a7c", "#86285a"
JEANS, JEANS_S = "#3b3656", "#2a2642"
LAP, LAP_S = "#ffa8d6", "#d95f9b"
LASH, IRIS, IRIS_L, PUPIL = "#3a1f2c", "#8a5236", "#c4865a", "#2b1626"

av = Grid(42, 48)
# cabelo de trás (comprido e ondulado)
av.ellipse(21, 14, 12, 12, HAIR)
for y in range(14, 37):
    wv = round(math.sin(y / 2.2))
    av.rect(8 + wv, y, 13 + wv, y, HAIR)
    av.rect(29 - wv, y, 34 - wv, y, HAIR)
    av.set(9 + wv, y, HAIR_S); av.set(33 - wv, y, HAIR_S)
# pernas cruzadas
av.ellipse(21, 41, 16, 4.6, JEANS)
av.rect(6, 44, 36, 44, None)
for x in range(7, 36):
    if av.get(x, 43):
        av.set(x, 43, JEANS_S)
# tênis
av.rect(3, 39, 7, 42, "#f4eef4"); av.rect(3, 42, 7, 42, PH)
av.rect(35, 39, 39, 42, "#f4eef4"); av.rect(35, 42, 39, 42, PH)
# moletom
for y in range(24, 37):
    half = 6 + (y - 24) // 2
    av.rect(21 - half, y, 21 + half, y, TOP)
    av.set(21 - half, y, TOP_S); av.set(21 + half, y, TOP_S)
# mechas da frente sobre os ombros
for y in range(18, 35):
    wv = round(math.sin(y / 2.0 + 1))
    av.rect(10 + wv, y, 12 + wv, y, HAIR)
    av.rect(30 - wv, y, 32 - wv, y, HAIR)
    if y % 4 == 0:
        av.set(11 + wv, y, HAIR_L); av.set(31 - wv, y, HAIR_L)
# braços indo até o teclado
line_cells(av, 14, 26, 13, 34, TOP_S, 3)
line_cells(av, 28, 26, 20, 36, TOP_S, 3)
# pescoço e rosto (mais arredondado, estilo chibi)
av.rect(19, 22, 23, 24, SKIN_S)
av.ellipse(21, 15.5, 8.6, 8.0, SKIN)
# franja com repartido de lado
av.ellipse(21, 13, 10.5, 10, HAIR, cond=lambda x, y: y <= 10)
for x in range(12, 21):
    av.set(x, 11, HAIR)
for x in (12, 13, 14, 15, 16):
    av.set(x, 12, HAIR)
for x in (12, 13):
    av.set(x, 13, HAIR)
for x in (24, 25, 27, 28, 29, 30):
    av.set(x, 11, HAIR)
for x in (29, 30):
    av.set(x, 12, HAIR)
for (x, y) in ((22, 9), (22, 10), (21, 10)):
    av.set(x, y, HAIR_S)                       # risca do cabelo
for (x, y) in ((15, 6), (16, 5), (17, 5), (26, 6), (27, 7), (14, 9), (15, 9)):
    av.set(x, y, HAIR_L)
# olhos grandes e redondos com brilho (olhando para a tela, à esquerda)
for ex in (15, 25):
    av.rect(ex, 14, ex + 2, 14, LASH)          # cílios
    av.rect(ex - 1, 15, ex + 2, 18, IRIS)
    av.rect(ex - 1, 15, ex, 17, PUPIL)
    av.set(ex - 1, 15, "#ffffff")              # brilho
    av.set(ex + 1, 18, IRIS_L); av.set(ex + 2, 18, IRIS_L)
    av.set(ex + 2, 15, LASH)
av.rect(13, 19, 14, 19, "#ff9bb5"); av.rect(28, 19, 29, 19, "#ff9bb5")
av.set(20, 21, "#d2477f"); av.set(21, 21, "#d2477f"); av.set(19, 20, "#e98aa9"); av.set(22, 20, "#e98aa9")
# fone de ouvido
for y in range(av.h):
    for x in range(av.w):
        d = math.hypot(x - 21, y - 13)
        if 11.6 <= d <= 12.8 and y <= 9:
            av.set(x, y, PH)
av.rect(7, 11, 10, 18, PH); av.rect(8, 12, 9, 17, PH_S)
av.rect(32, 11, 35, 18, PH); av.rect(33, 12, 34, 17, PH_S)
av.outline()

# pálpebras (piscar)
lids = Grid(42, 48)
for ex in (15, 25):
    lids.rect(ex - 1, 14, ex + 2, 17, SKIN)
    lids.rect(ex - 1, 18, ex + 2, 18, LASH)

AX, AY, AS = 640, 22, 5
add(f'<g class="bob">{av.svg(AX, AY, AS)}<g class="blink">{lids.svg(AX, AY, AS)}</g>')

# notebook em 3/4: tela à esquerda, teclado na frente dela
SX, SY, SW, SH, SK = 658, 126, 74, 54, 0.28   # canto, largura, altura, inclinação
add(f'<g transform="matrix(1 {SK} 0 1 {SX} {SY})">'
    f'<rect x="0" y="0" width="{SW}" height="{SH}" rx="2" fill="{LAP}" stroke="#7a2350" stroke-width="2"/>'
    f'<rect x="4" y="4" width="{SW - 8}" height="{SH - 8}" fill="#170c1a"/>')
code = [(8, 9, 26, PINK_L), (8, 16, 44, "#7ee0c3"), (15, 23, 34, WHITE), (15, 30, 46, "#ffd27a"),
        (15, 37, 22, PINK_L), (8, 44, 36, "#7ee0c3")]
n = len(code)
for i, (x, y, w, col) in enumerate(code):
    a, b = 5 + i * 12, 5 + i * 12 + 9
    CSS_EXTRA.append(f".c{i}{{transform-box:fill-box;transform-origin:left;animation:c{i} 6s steps(6) infinite}}"
                     f"@keyframes c{i}{{0%,{a}%{{transform:scaleX(0)}}{b}%,90%{{transform:scaleX(1);opacity:1}}"
                     f"96%,100%{{transform:scaleX(1);opacity:0}}}}")
    add(f'<rect class="c{i}" x="{x}" y="{y}" width="{w}" height="4" fill="{col}"/>')
add(f'<rect class="cur" x="48" y="44" width="5" height="4" fill="{PINK}" style="animation-delay:0s,0s"/>'
    f'</g>')
# base/teclado: matriz leva o quadrado unitário ao paralelogramo da base
u = (SW, SW * SK)
v = (24, 22)
bx, by = SX, SY + SH
add(f'<polygon points="{bx},{by} {bx + u[0]},{by + u[1]} {bx + u[0] + v[0]},{by + u[1] + v[1]} {bx + v[0]},{by + v[1]}" '
    f'fill="#f7d3e8" stroke="#7a2350" stroke-width="2" stroke-linejoin="round"/>')
keys = []
for r in range(3):
    for c in range(7):
        keys.append(f'<rect x="{0.08 + c * 0.125:.3f}" y="{0.15 + r * 0.22:.3f}" width="0.09" height="0.14" fill="{LAP_S}"/>')
add(f'<g transform="matrix({u[0]} {u[1]} {v[0]} {v[1]} {bx} {by})">{"".join(keys)}</g>')
# mãos digitando por cima do teclado
hand = lambda x, y: (f'<rect x="{x - 1}" y="{y - 1}" width="14" height="9" rx="2" fill="#a0605a"/>'
                     f'<rect x="{x}" y="{y}" width="12" height="7" rx="2" fill="{SKIN}"/>')
add(f'<g class="typeL">{hand(700, 196)}</g><g class="typeR">{hand(732, 206)}</g>')
add('</g>')  # fim do bob

# ---------------------------------------------------------------- gato preto dormindo (à esquerda da avatar)
CAT, WHT = "#1d1722", "#f4eef4"
CAT_MAP = [
    "..........................",
    "..........................",
    ".BBBBBBB..................",
    "BBBBBBBBB....BBBBBBBB.....",
    "BBPPBBPPBBBBBBBBBBBBBBB...",
    "BBBBBBBBBBBBBBBBBBBBBBBB..",
    "BWWWpWWWBBBBBBkkkkBBBBBBB.",
    "BWWWWWWWBBBBBBBBBBBBBBBBB.",
    ".BWWWWWBBBBBBBBBBBBBBBBBB.",
    ".BBWWWBBBBBBBBBBBBBBBBBBB.",
    "..BBBBBBBBBBBBBBBBBBBBBB..",
    ".WWWW.WWWWBBBBBBBBBBBBB...",
    ".WWWW.WWWW................",
]
EARS_MAP = ["..B...B...", ".BPB.BPB..", ".BBBBBBB.."]
TAIL_MAP = ["......BB", ".....BWB", "....BB..", "...BB...", "..BB....", ".BB.....", "BB......"]
COLS = {"B": CAT, "W": WHT, "P": "#ff9ccf", "p": "#ff7ab8", "k": "#3a2f44",
        "O": "#c9763c", "o": "#8f4c26", "C": "#f3d3b0", "A": "#f0a92e", "E": "#1d1722", "N": "#ff8fae"}


def from_map(rows):
    g = Grid(max(len(r) for r in rows), len(rows))
    for y, row in enumerate(rows):
        for x, v in enumerate(row):
            if v in COLS:
                g.set(x, y, COLS[v])
    g.outline("#5a3352")
    return g


cat, ears, tail = from_map(CAT_MAP), from_map(EARS_MAP), from_map(TAIL_MAP)
CX0, CY0, CS = 548, 222, 3.6
add(f'<g class="breath">{cat.svg(CX0, CY0, CS)}</g>'
    f'<g class="ear">{ears.svg(CX0, CY0, CS)}</g>'
    f'<g class="tail">{tail.svg(round(CX0 + 23 * CS, 1), round(CY0 - 1 * CS, 1), CS)}</g>')
for i in range(3):
    add(f'<g transform="translate({CX0 + 30 + i * 6} {CY0 + 2})"><text class="z" x="0" y="0" '
        f'font-family="\'Courier New\',monospace" font-weight="bold" font-size="{11 + i * 3}" fill="{PINK_L}" '
        f'style="animation-delay:{i * 1.2:.1f}s">z</text></g>')

# ---------------------------------------------------------------- gatinha escaminha brincando com Júpiter
TORT = [
    "..B...........B...",
    ".BBB.........BBB..",
    ".BPBB.......BBPB..",
    ".BBBBBBBBCBBBBBB..",
    "BBBOBBBBBCBBBBOBB.",
    "BBBBBBBBBCCBBBBBB.",
    "BBAAAEBBBCCBAAAEB.",
    "BBAAEEBBCCCBAAEEB.",
    "BBBBBBBCCNCCBBBBB.",
    ".BBBBBBBCCCBBBBB..",
    "..BBBBBBBBBBBBB...",
    "...BBBBOBBBBBB....",
    "..BBBBBOOBBBBBB...",
    "..BBBBCCBBBBOBBB..",
    ".BBBBBCCBBBBBBBBB.",
    ".BBOBBBBBBBBBOBBB.",
    ".BBBBBBBBBBBBBBBB.",
    ".BBBBBBBBOBBBBBBB.",
    "..BBB...BBB..BBBB.",
    "..BBB...BBB.......",
]
tort = from_map(TORT)
TAILT = ["..BB", ".BOB", ".BB.", "BB..", "BB..", "BBB."]
tailt = from_map(TAILT)
ARM = ["BBB", "BBB", "BOB", "BBB", "BBB", "BBB", "BBB", "BOB", "BBB", "BBB", "CCC"]
arm = from_map(ARM)
TX, TY, TS = 902, 196, 3.4
add(f'<g class="breath">{tort.svg(TX, TY, TS)}</g>'
    f'<g class="tail" style="animation-duration:1.6s">{tailt.svg(round(TX + 16 * TS, 1), round(TY + 12 * TS, 1), TS)}</g>')
# patinha: gira em torno do ombro para cima e bate no Júpiter
pvx, pvy = TX + 2 * TS, TY + 11 * TS
CSS_EXTRA.append(f".paw{{transform-origin:{pvx + 1.5 * TS:.1f}px {pvy:.1f}px;animation:paw 3.2s ease-in-out infinite}}"
                 "@keyframes paw{0%,62%,100%{transform:rotate(0)}70%{transform:rotate(140deg)}74%{transform:rotate(152deg)}84%{transform:rotate(0)}}")
add(f'<g class="paw">{arm.svg(round(pvx, 1), round(pvy, 1), TS)}</g>')

# Júpiter: faixas em tons quentes + grande mancha vermelha
JUP = {"a": "#fbe3c6", "b": "#e8b48a", "c": "#c9785a", "d": "#9a4f3e", "s": "#d0473f"}
pl = Grid(17, 17)
pl.ellipse(8, 8, 8, 8, JUP["a"])
for y in range(17):
    for x in range(17):
        if pl.get(x, y):
            band = "a"
            if y in (3, 4, 11):
                band = "b"
            if y in (6, 7, 13):
                band = "c"
            if y in (9, 14):
                band = "d"
            pl.set(x, y, JUP[band])
for (x, y) in ((10, 9), (11, 9), (10, 10), (11, 10), (12, 10)):
    pl.set(x, y, JUP["s"])
pl.outline("#6a3348")
PS = 3.4
PCX, PCY = TX - 2 * TS, 170
half = 8.5 * PS
CSS_EXTRA.append(".bat{animation:bat 3.2s ease-in-out infinite}"
                 "@keyframes bat{0%,70%,100%{transform:translateY(0)}78%{transform:translateY(-30px)}"
                 "86%{transform:translateY(-34px)}94%{transform:translateY(-6px)}97%{transform:translateY(-2px)}}"
                 ".roll{transform-box:fill-box;transform-origin:center;animation:roll 3.2s ease-in-out infinite}"
                 "@keyframes roll{0%,70%{transform:rotate(0)}96%,100%{transform:rotate(360deg)}}"
                 ".orbit{transform-box:fill-box;transform-origin:center;animation:orbit 3.2s ease-in-out infinite}"
                 "@keyframes orbit{0%,70%{transform:rotate(-18deg)}96%,100%{transform:rotate(342deg)}}")
add(f'<g class="bat"><g class="float" style="animation-duration:5s">'
    f'<g class="orbit"><ellipse cx="{PCX}" cy="{PCY}" rx="{half + 16}" ry="9" fill="none" stroke="#ff9ccf" '
    f'stroke-width="3" stroke-dasharray="6 5" filter="url(#glow)"/></g>'
    f'<g class="roll">{pl.svg(round(PCX - half, 1), round(PCY - half, 1), PS)}</g>'
    f'</g></g>')

# ---------------------------------------------------------------- moldura
add('</g>')
add(f'<rect class="frame" x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="15" fill="none" stroke="{PINK}" '
    f'stroke-width="2" filter="url(#glow)"/>')
add("</svg>")
parts[STYLE_AT] = "<style>" + CSS + "".join(CSS_EXTRA) + "</style>"

OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"ok: {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")
