"""montar_slides.py - monta o .pptx da aula a partir de um JSON.

Uso:  python montar_slides.py slides.json aula.pptx
JSON: {"cor": "#2563EB", "slides": [ {"tipo": ..., "notas": "fala do professor"}, ... ]}
Tipos: capa(titulo, subtitulo) | topicos(titulo, itens<=5) | codigo(titulo, imagem, legenda?)
       pergunta(texto) | secao(titulo)
Caminhos de imagem sao relativos ao JSON.
"""
import json, os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

spec_path, saida = sys.argv[1], sys.argv[2]
spec = json.load(open(spec_path, encoding="utf-8"))
base = os.path.dirname(os.path.abspath(spec_path))
COR = RGBColor.from_string(spec.get("cor", "#2563EB").lstrip("#"))
ESCURO, CINZA = RGBColor(0x1F, 0x29, 0x37), RGBColor(0x6B, 0x72, 0x80)
FONTE = "Calibri"
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = prs.slide_width, prs.slide_height

def caixa(sl, x, y, w, h, txt, tam, cor=ESCURO, neg=False, alin=PP_ALIGN.LEFT, meio=False):
    tf = sl.shapes.add_textbox(x, y, w, h).text_frame
    tf.word_wrap = True
    if meio: tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, linha in enumerate(txt if isinstance(txt, list) else [txt]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = alin; p.space_after = Pt(14)
        r = p.add_run(); r.text = linha
        r.font.size, r.font.bold, r.font.name = Pt(tam), neg, FONTE
        r.font.color.rgb = cor
    return tf

def barra(sl, y=Inches(1.25)):
    s = sl.shapes.add_shape(1, Inches(0.6), y, Inches(1.2), Inches(0.08))
    s.fill.solid(); s.fill.fore_color.rgb = COR; s.line.fill.background()

def titulo(sl, t):
    caixa(sl, Inches(0.6), Inches(0.35), W - Inches(1.2), Inches(0.9), t, 36, neg=True); barra(sl)

for n, s in enumerate(spec["slides"], 1):
    sl = prs.slides.add_slide(prs.slide_layouts[6]); tipo = s["tipo"]
    if tipo == "capa":
        caixa(sl, Inches(0.8), Inches(2.3), W - Inches(1.6), Inches(1.6), s["titulo"], 48, neg=True)
        barra(sl, Inches(3.95))
        caixa(sl, Inches(0.8), Inches(4.2), W - Inches(1.6), Inches(1.2), s.get("subtitulo", ""), 24, CINZA)
    elif tipo == "secao":
        fundo = sl.background.fill; fundo.solid(); fundo.fore_color.rgb = COR
        caixa(sl, Inches(0.8), 0, W - Inches(1.6), H, s["titulo"], 44, RGBColor(255, 255, 255), True, meio=True)
    elif tipo == "topicos":
        titulo(sl, s["titulo"])
        caixa(sl, Inches(0.8), Inches(1.7), W - Inches(1.6), H - Inches(2.2), ["•  " + i for i in s["itens"][:5]], 28)
    elif tipo == "pergunta":
        caixa(sl, Inches(1.2), 0, W - Inches(2.4), H, s["texto"], 40, COR, True, PP_ALIGN.CENTER, True)
    elif tipo == "codigo":
        titulo(sl, s["titulo"])
        img = os.path.join(base, s["imagem"]); iw, ih = Image.open(img).size
        topo = Inches(1.6); leg = Inches(0.7) if s.get("legenda") else 0
        max_w, max_h = W - Inches(1.2), H - topo - Inches(0.35) - leg
        esc = min(max_w / iw, max_h / ih, 11000)  # limite: fonte do print ~26 pt, nunca gigante
        w, h = int(iw * esc), int(ih * esc)
        sl.shapes.add_picture(img, int((W - w) / 2), topo, w, h)
        if leg:
            caixa(sl, Inches(0.6), topo + h + Inches(0.1), W - Inches(1.2), leg, s["legenda"], 20, CINZA, alin=PP_ALIGN.CENTER)
    else:
        sys.exit(f"Tipo desconhecido no slide {n}: {tipo}")
    if tipo not in ("capa", "secao"):
        caixa(sl, W - Inches(1.2), H - Inches(0.55), Inches(0.8), Inches(0.4), str(n), 14, CINZA, alin=PP_ALIGN.RIGHT)
    sl.notes_slide.notes_text_frame.text = s.get("notas", "")

prs.save(saida); print(f"OK: {saida} ({len(spec['slides'])} slides)")
