"""Gera os cards do README (atividade e linguagens) como SVG, sem depender de serviços externos.

Roda dentro do GitHub Actions (workflow snake.yml) e salva os arquivos em dist/,
que é publicado na branch `output` junto com a cobrinha.

Uso local para testar sem rede:  python cards.py --mock
"""
import json
import os
import sys
import urllib.request
from collections import OrderedDict
from datetime import date

USER = os.environ.get("GITHUB_USER", "tamiresvferreira")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("OUT_DIR", "dist")

# Paleta rosa do perfil
BG, BORDER, TEXT, MUTED, PINK, PINK_SOFT = "#0d1117", "#30363d", "#c9d1d9", "#8b949e", "#ff5fa2", "#ffc2e0"
FONT = "font-family=\"Segoe UI, Ubuntu, Helvetica, Arial, sans-serif\""
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

# Cores das linguagens (as mesmas que o GitHub usa)
LANG_COLORS = {
    "Python": "#3572A5", "Jupyter Notebook": "#DA5B0B", "R": "#198CE7", "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6", "HTML": "#e34c26", "CSS": "#663399", "C++": "#f34b7d", "C": "#555555",
    "Java": "#b07219", "Shell": "#89e051", "SQL": "#e38c00", "PLpgSQL": "#336790", "Dockerfile": "#384d54",
}


NOMES_CURTOS = {"Jupyter Notebook": "Jupyter"}
LANG_COLORS["Jupyter"] = LANG_COLORS["Jupyter Notebook"]


def api(url, payload=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "cards-readme"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def contribuicoes_por_dia():
    """Contribuições do último ano (inclui as privadas, se o perfil permitir)."""
    q = """query($login:String!){ user(login:$login){ contributionsCollection{
             contributionCalendar{ weeks{ contributionDays{ date contributionCount }}}}}}"""
    res = api("https://api.github.com/graphql", {"query": q, "variables": {"login": USER}})
    semanas = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return {d["date"]: d["contributionCount"] for w in semanas for d in w["contributionDays"]}


def linguagens():
    """Soma os bytes por linguagem dos repositórios públicos (sem forks)."""
    total = {}
    for repo in api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner"):
        if repo.get("fork") or repo.get("private"):
            continue
        for lang, n in api(repo["languages_url"]).items():
            total[lang] = total.get(lang, 0) + n
    return total


def por_mes(dias):
    """Agrupa as contribuições nos últimos 12 meses (o mês atual por último)."""
    hoje = date.today()
    meses = OrderedDict()
    for i in range(11, -1, -1):
        m, a = hoje.month - i, hoje.year
        while m <= 0:
            m, a = m + 12, a - 1
        meses[(a, m)] = 0
    for d, n in dias.items():
        a, m = int(d[:4]), int(d[5:7])
        if (a, m) in meses:
            meses[(a, m)] += n
    return meses


def card_atividade(meses):
    w, h = 900, 260
    left, right, top, bottom = 50, 25, 62, 40
    cw, ch = w - left - right, h - top - bottom
    maximo = max(max(meses.values()), 1)
    total = sum(meses.values())
    n = len(meses)
    slot = cw / n
    bw = slot * 0.56
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="Contribuições por mês no último ano: {total}">',
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="8" fill="{BG}" stroke="{BORDER}"/>',
        f'<text x="{left}" y="36" {FONT} font-size="18" font-weight="600" fill="{PINK}">Atividade no GitHub</text>',
        f'<text x="{w-right}" y="36" {FONT} font-size="13" fill="{MUTED}" text-anchor="end">'
        f'{total} contribuições nos últimos 12 meses</text>',
    ]
    # linhas de grade
    for frac in (0, 0.5, 1):
        y = top + ch - ch * frac
        partes.append(f'<line x1="{left}" y1="{y:.1f}" x2="{w-right}" y2="{y:.1f}" stroke="{BORDER}" stroke-dasharray="3 4"/>')
        partes.append(f'<text x="{left-10}" y="{y+4:.1f}" {FONT} font-size="11" fill="{MUTED}" text-anchor="end">'
                      f'{round(maximo*frac)}</text>')
    for i, ((a, m), v) in enumerate(meses.items()):
        x = left + i * slot + (slot - bw) / 2
        bh = ch * v / maximo
        y = top + ch - bh
        cor = PINK if v else BORDER
        if v:
            partes.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(bh,2):.1f}" rx="4" fill="{cor}">'
                          f'<title>{MESES[m-1]}/{a}: {v}</title></rect>')
            partes.append(f'<text x="{x+bw/2:.1f}" y="{y-6:.1f}" {FONT} font-size="11" fill="{PINK_SOFT}" '
                          f'text-anchor="middle">{v}</text>')
        else:
            partes.append(f'<rect x="{x:.1f}" y="{top+ch-2:.1f}" width="{bw:.1f}" height="2" rx="1" fill="{cor}"/>')
        rotulo = MESES[m - 1] + (f" {str(a)[2:]}" if m == 1 or i == 0 else "")
        partes.append(f'<text x="{x+bw/2:.1f}" y="{h-16}" {FONT} font-size="12" fill="{MUTED}" '
                      f'text-anchor="middle">{rotulo}</text>')
    partes.append("</svg>")
    return "\n".join(partes)


def card_linguagens(langs, max_itens=5):
    w, h = 350, 195
    # raiz quadrada dos bytes: evita que notebooks (que guardam saídas) engulam o resto
    itens = sorted(((NOMES_CURTOS.get(k, k), v ** 0.5) for k, v in langs.items()), key=lambda kv: kv[1], reverse=True)
    total = sum(v for _, v in itens) or 1
    principais = itens[:max_itens]
    resto = sum(v for _, v in itens[max_itens:])
    if resto:
        principais.append(("Outras", resto))
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="Linguagens que mais uso">',
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="8" fill="{BG}" stroke="{BORDER}"/>',
        f'<text x="25" y="38" {FONT} font-size="18" font-weight="600" fill="{PINK}">Linguagens que mais uso</text>',
    ]
    # barra empilhada
    x, bar_w = 25.0, w - 50
    partes.append(f'<clipPath id="c"><rect x="25" y="58" width="{bar_w}" height="10" rx="5"/></clipPath><g clip-path="url(#c)">')
    for nome, v in principais:
        largura = bar_w * v / total
        partes.append(f'<rect x="{x:.2f}" y="58" width="{largura+0.5:.2f}" height="10" '
                      f'fill="{LANG_COLORS.get(nome, MUTED)}"/>')
        x += largura
    partes.append("</g>")
    # legenda em duas colunas
    for i, (nome, v) in enumerate(principais):
        col, lin = i % 2, i // 2
        lx, ly = 25 + col * 165, 98 + lin * 28
        pct = 100 * v / total
        partes.append(f'<circle cx="{lx+5}" cy="{ly-4}" r="5" fill="{LANG_COLORS.get(nome, MUTED)}"/>')
        partes.append(f'<text x="{lx+16}" y="{ly}" {FONT} font-size="12.5" fill="{TEXT}">{nome} '
                      f'<tspan fill="{MUTED}">{pct:.1f}%</tspan></text>')
    if not principais:
        partes.append(f'<text x="25" y="110" {FONT} font-size="13" fill="{MUTED}">Sem repositórios públicos ainda</text>')
    partes.append("</svg>")
    return "\n".join(partes)


def main():
    if "--mock" in sys.argv:
        dias = {"2026-03-23": 1, "2026-03-24": 1, "2026-05-19": 3, "2026-06-01": 7, "2026-06-02": 2,
                "2026-08-19": 1, "2026-09-28": 35, "2026-10-27": 3, "2026-10-29": 1, "2026-11-10": 2, "2026-11-11": 5}
        langs = {"Jupyter Notebook": 420000, "Python": 9800, "R": 4300}
    else:
        dias, langs = contribuicoes_por_dia(), linguagens()
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "atividade.svg"), "w", encoding="utf-8") as f:
        f.write(card_atividade(por_mes(dias)))
    with open(os.path.join(OUT, "linguagens.svg"), "w", encoding="utf-8") as f:
        f.write(card_linguagens(langs))
    print("Cards gerados em", OUT)


if __name__ == "__main__":
    main()
