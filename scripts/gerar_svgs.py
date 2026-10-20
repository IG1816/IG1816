"""Gera os SVGs do README do perfil com a identidade do portfólio (igordeaguiar.vercel.app).

Fundo #09090a, destaque limão #d4ff3f, títulos em Instrument Serif e rótulos em Geist Mono.
As fontes vão embutidas (só os glifos usados), porque o GitHub não carrega fonte externa em SVG.

Uso:
    pip install fonttools brotli
    npm pack @fontsource/instrument-serif @fontsource/geist-mono   # e extrair os .tgz
    python scripts/gerar_svgs.py <pasta-com-os-woff2>
"""

import base64
import io
import pathlib
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

FONTES = {
    "serif": "instrument-serif-latin-400-normal.woff2",
    "serif-italic": "instrument-serif-latin-400-italic.woff2",
    "mono": "geist-mono-latin-400-normal.woff2",
}

TEMAS = {
    "dark": {
        "bg": "#09090a", "elev": "#111113", "line": "rgba(255,255,255,0.10)",
        "fg": "#ecebe6", "muted": "#8d8c86", "accent": "#d4ff3f", "glow": "rgba(212,255,63,0.16)",
        "grain": 0.07,
    },
    "light": {
        "bg": "#f4f3ee", "elev": "#ffffff", "line": "rgba(0,0,0,0.10)",
        "fg": "#141413", "muted": "#62615b", "accent": "#4c6a00", "glow": "rgba(76,106,0,0.12)",
        "grain": 0.05,
    },
}

STACK = ["Python", "FastAPI", "PostgreSQL", "Next.js", "React", "TypeScript",
         "Supabase", "Tailwind", "three.js", "Node.js", "WebSocket", "Vercel"]

SECOES = [
    ("01", "Sobre", "sobre"),
    ("02", "Experiência", "experiencia"),
    ("03", "Projetos", "projetos"),
    ("04", "Vamos construir", "contato"),  # o resto ("algo juntos?") vai em itálico
]


def fonte_b64(pasta, chave, texto):
    """Subconjunto da fonte só com os caracteres de `texto`, em woff2 base64."""
    font = TTFont(pasta / FONTES[chave])
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    sub = subset.Subsetter(opts)
    sub.populate(text=texto + " ")
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def estilo(pasta, textos):
    regras = []
    for chave, familia, italico in [("serif", "S", False), ("serif-italic", "S", True), ("mono", "M", False)]:
        texto = textos.get(chave, "")
        if not texto:
            continue
        regras.append(
            f"@font-face{{font-family:'{familia}';font-style:{'italic' if italico else 'normal'};"
            f"src:url(data:font/woff2;base64,{fonte_b64(pasta, chave, texto)}) format('woff2');}}"
        )
    return "\n".join(regras)


def grao(t):
    return (
        '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>'
        '<feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 1 0"/></filter>'
        f'<rect width="100%" height="100%" filter="url(#grain)" opacity="{t["grain"]}"/>'
    )


def hero(pasta, t):
    w, h = 1200, 460
    pill = "Aberto a vagas · Içara/SC · híbrido na região ou remoto"
    nome, sobrenome = "Igor de ", "Aguiar"
    sub1, sub2 = "Construo produtos web de ponta a ponta, ", "do banco de dados ao pixel."
    topo_esq, topo_dir = "IG1816 / FULL STACK", "IGORDEAGUIAR.VERCEL.APP"
    linha = "  ·  ".join(STACK) + "  ·  "

    css = estilo(pasta, {
        "serif": nome + sub1,
        "serif-italic": sobrenome + sub2,
        "mono": pill + topo_esq + topo_dir + linha,
    })

    # Faixa da stack: dois blocos iguais lado a lado, a animação desliza um bloco inteiro.
    passo = len(linha) * 16 * (0.6 + 0.08)  # Geist Mono: avanço de 0,6em + letter-spacing de 0,08em
    faixa = "".join(
        f'<text x="{i * passo:.0f}" y="0" class="mono" font-size="16" fill="{t["muted"]}">{linha}</text>'
        for i in range(4)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Igor de Aguiar · Desenvolvedor full stack">
<style>
{css}
.serif{{font-family:'S',Georgia,serif}}
.mono{{font-family:'M',ui-monospace,monospace;letter-spacing:.08em}}
.dot{{animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{50%{{opacity:.25}}}}
.marquee{{animation:mq 38s linear infinite}}
@keyframes mq{{to{{transform:translateX(-{passo:.0f}px)}}}}
</style>
<defs>
<radialGradient id="g1" cx="85%" cy="15%" r="60%"><stop offset="0" stop-color="{t["glow"]}"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx="0%" cy="100%" r="45%"><stop offset="0" stop-color="{t["glow"]}"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>
<clipPath id="c"><rect width="{w}" height="{h}" rx="20"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="{w}" height="{h}" fill="{t["bg"]}"/>
<rect width="{w}" height="{h}" fill="url(#g1)"/>
<rect width="{w}" height="{h}" fill="url(#g2)"/>
{grao(t)}
<text x="56" y="58" class="mono" font-size="13" fill="{t["muted"]}">{topo_esq}</text>
<text x="{w - 56}" y="58" text-anchor="end" class="mono" font-size="13" fill="{t["muted"]}">{topo_dir}</text>

<g>
<rect x="56" y="98" width="{len(pill) * 8.2 + 50:.0f}" height="34" rx="17" fill="{t["bg"]}" fill-opacity=".5" stroke="{t["line"]}"/>
<circle class="dot" cx="76" cy="115" r="3.5" fill="{t["accent"]}"/>
<text x="90" y="120" class="mono" font-size="13" fill="{t["muted"]}" style="letter-spacing:.02em">{pill}</text>
</g>

<text x="50" y="262" class="serif" font-size="138" fill="{t["fg"]}" style="letter-spacing:-.02em">{nome}<tspan font-style="italic" fill="{t["accent"]}">{sobrenome}</tspan></text>
<text x="56" y="322" class="serif" font-size="38" fill="{t["muted"]}">{sub1}<tspan font-style="italic" fill="{t["fg"]}">{sub2}</tspan></text>

<line x1="0" y1="{h - 70}" x2="{w}" y2="{h - 70}" stroke="{t["line"]}"/>
<g transform="translate(56 {h - 30})"><g class="marquee">{faixa}</g></g>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="19.5" fill="none" stroke="{t["line"]}"/>
</svg>
"""


def secao(pasta, t, num, titulo):
    w, h = 1200, 120
    rotulo = f"({num})"
    italico = " algo juntos?" if num == "04" else ""
    css = estilo(pasta, {"serif": titulo, "serif-italic": italico, "mono": rotulo})
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{titulo}{italico}">
<style>
{css}
.serif{{font-family:'S',Georgia,serif}}
.mono{{font-family:'M',ui-monospace,monospace;letter-spacing:.08em}}
</style>
<text x="2" y="84" class="mono" font-size="15" fill="{t["accent"]}">{rotulo}</text>
<text x="56" y="88" class="serif" font-size="76" fill="{t["fg"]}" style="letter-spacing:-.02em">{titulo}<tspan font-style="italic" fill="{t["accent"]}">{italico}</tspan></text>
<line x1="0" y1="{h - 1}" x2="{w}" y2="{h - 1}" stroke="{t["line"]}"/>
</svg>
"""


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    pasta = pathlib.Path(sys.argv[1])
    saida = pathlib.Path(__file__).resolve().parent.parent / "assets"
    saida.mkdir(exist_ok=True)
    for nome_tema, t in TEMAS.items():
        (saida / f"hero-{nome_tema}.svg").write_text(hero(pasta, t), encoding="utf-8")
        for num, titulo, slug in SECOES:
            (saida / f"secao-{slug}-{nome_tema}.svg").write_text(secao(pasta, t, num, titulo), encoding="utf-8")
    print("SVGs gerados em", saida)


if __name__ == "__main__":
    main()
