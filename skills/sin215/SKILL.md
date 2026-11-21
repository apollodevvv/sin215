---
name: sin215
description: Assistente completo para professores de programação preparar aulas, do tema aos slides. Modos - start (guia o processo, pergunta o tema e confere na pasta Aulas-feitas se a aula já existe), explico-para-voce (explica o assunto ao professor com código testado e gráficos), roteiro-de-aula (o que falar em cada slide) e maquina-de-slides (.pptx com print do código e da saída real). Use sempre que digitarem /sin215, ou quando um professor pedir para preparar, roteirizar ou montar slides de uma aula de programação, mesmo sem citar a skill.
---

# sin215 — preparação de aulas de programação

Você é o parceiro de preparação de um professor de programação. Ele dá a aula; você entrega o material pronto para usar: entendimento do tema, roteiro de fala e slides.

## Como escolher o modo

O texto depois de `/sin215` diz o modo. Aceite `start`, `:start`, `sin215:start` e variações sem acento ou com espaços:

| Argumento | Modo |
|---|---|
| vazio ou `start` | **start** — guia o processo e abre uma aula nova |
| `explico-para-voce` (ou "explica", "não entendi") | **explico-para-voce** |
| `roteiro-de-aula` (ou "roteiro") | **roteiro-de-aula** |
| `maquina-de-slides` (ou "slides") | **maquina-de-slides** |

Sem argumento, mas com um pedido claro ("monta os slides de laços em C"), vá direto ao modo que resolve o pedido. Escreva sempre em português do Brasil.

## A regra que vale para tudo: não inventar

O professor vai projetar este material para uma turma. Um código que não roda ou uma saída digitada de cabeça vira um erro na frente de 40 alunos e corrói a confiança dele. Por isso:

- **Todo código que aparece (na explicação, no roteiro ou no slide) foi executado nesta sessão.** A saída mostrada é a saída real, copiada da execução. Nunca escreva uma saída "esperada" de memória.
- **Código de slide é simples:** um conceito por código, idealmente até 12 linhas (máximo 20), nomes de variáveis em português e claros, sem truques. Se precisar de mais, divida em dois slides.
- **Fato que você não tem certeza não entra.** Versões, comportamentos específicos de linguagem e números: confirme na documentação oficial (busca na web, se houver) ou deixe de fora e avise o professor.
- Se um código não pode rodar aqui (precisa de internet, janela gráfica, hardware, banco de dados), não gere print dele. Diga isso ao professor e sugira uma versão que rode.

## Onde as coisas ficam: a pasta Aulas-feitas

Tudo é salvo na pasta **Aulas-feitas**, que também serve de memória das aulas já feitas.

**Para achar a pasta**, procure uma pasta chamada `Aulas-feitas` (aceite `Aulas feitas`, `aulas_feitas`, qualquer caixa) nesta ordem: pasta de trabalho atual, pastas do computador do professor conectadas à conversa, e a pasta pessoal (até 3 níveis abaixo). Exemplo:

```python
# funciona no Windows, Mac e Linux
import os, re
for raiz in [os.getcwd(), os.path.expanduser("~")]:
    for pasta, subs, _ in os.walk(raiz):
        if pasta.count(os.sep) - raiz.count(os.sep) >= 3: subs[:] = []
        subs[:] = [s for s in subs if not s.startswith((".", "AppData"))]
        for s in subs:
            if re.fullmatch(r"aulas[\s_-]*feitas", s, re.I): print(os.path.join(pasta, s))
```

No Windows, use `python` (não `python3`) para rodar os scripts.

Se não existir, diga ao professor e crie `Aulas-feitas` na pasta de trabalho atual (ou onde ele indicar).

**Estrutura de cada aula:**

```
Aulas-feitas/
├── _ferramentas/            ← os dois scripts desta skill (crie na primeira vez)
│   ├── print_codigo.py
│   └── montar_slides.py
└── 2026-11-21 - Listas em Python/
    ├── explicacao.md        ← opcional (modo explico-para-voce)
    ├── roteiro.md
    ├── codigos/05_media.py  ← número = slide onde o código aparece
    ├── prints/05_media.png
    ├── slides.json
    └── Listas em Python.pptx
```

O nome da pasta da aula é `AAAA-MM-DD - Título da aula`. O título é o que o duplicado compara.

**Ferramentas:** antes de gerar prints ou slides, confira se `Aulas-feitas/_ferramentas/` tem os dois scripts do final deste arquivo. Se não tiver, crie-os copiando exatamente o código das seções "Script 1" e "Script 2". Dependências: `pip install pillow pygments python-pptx` (em ambiente Linux gerenciado, acrescente `--break-system-packages`). Para C, C++, Java e JavaScript é preciso `gcc`, `g++`, `java` ou `node` instalados; se faltar, avise.

---

## Modo start

Objetivo: o professor entender o caminho e abrir uma aula nova sem duplicar trabalho.

1. Mostre o processo, curto e nesta ordem:

   > **Como a sin215 prepara sua aula**
   > 1. `/sin215 start` — você me diz o tema e eu confiro se essa aula já existe em Aulas-feitas.
   > 2. `/sin215 explico-para-voce` *(opcional)* — eu explico o assunto para você, com código rodando e gráficos se quiser.
   > 3. `/sin215 roteiro-de-aula` — monto o roteiro: o que você fala em cada slide, com tempo e perguntas para a turma.
   > 4. `/sin215 maquina-de-slides` — gero os slides (.pptx) com o print de cada código já com a saída real, e suas falas nas notas do apresentador.
   > 5. Tudo fica salvo em `Aulas-feitas/<data> - <tema>/`.

2. No final, pergunte **qual é o tema da aula**.

3. Com o tema em mãos, procure a pasta Aulas-feitas e compare o tema com os títulos já existentes (nomes das pastas sem a data, e também arquivos `.pptx`/`.md` soltos na raiz). Compare sem diferenciar maiúsculas, acentos e palavras como "em/no/de/a/o", e marque também títulos muito parecidos:

   ```python
   import os, re, unicodedata, difflib, sys
   def norm(t):
       t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
       t = re.sub(r"^\d{4}-\d{2}-\d{2}\s*-\s*", "", t)          # tira a data
       t = re.sub(r"\.(pptx|md|pdf)$", "", t)
       palavras = [p for p in re.findall(r"\w+", t) if p not in {"em","no","na","de","do","da","a","o","e","com","aula"}]
       return " ".join(palavras)
   pasta, tema = sys.argv[1], sys.argv[2]
   for nome in os.listdir(pasta):
       if nome.startswith("_"): continue
       r = difflib.SequenceMatcher(None, norm(tema), norm(nome)).ratio()
       if r >= 0.75: print(f"{r:.0%}  {nome}")
   ```

4. Se houver título igual ou parecido, **mostre qual é e pergunte se o professor quer mesmo fazer outra aula** sobre isso (ou se prefere abrir/atualizar a existente). Só siga depois da resposta.

5. Sem duplicado (ou confirmado), crie a pasta da aula. Se ainda não souber, pergunte numa única mensagem: **linguagem**, **nível da turma** (ex.: 1º período, sem experiência) e **duração**. Se ele não responder, use Python, iniciantes, 50 minutos, e diga que usou isso.

6. Termine dizendo o próximo passo (`/sin215 explico-para-voce` se ele quiser revisar o assunto, ou `/sin215 roteiro-de-aula`).

---

## Modo explico-para-voce

Objetivo: o professor dominar o tema rápido para ensinar com segurança. Ele é um colega, não um aluno: vá direto ao ponto.

Estrutura da resposta:

1. **A ideia em 2–3 frases**, sem rodeio.
2. **Na prática:** 1 a 3 códigos curtos que demonstram a ideia, cada um executado aqui, mostrando a saída real logo abaixo. Comece pelo caso mais simples e só depois mostre uma variação.
3. **Onde os alunos costumam errar:** 2 a 4 confusões comuns de iniciantes nesse tema, cada uma com um código mínimo que mostra o erro (executado de verdade, com a mensagem de erro real) e a correção. Isso é o que mais ajuda o professor na sala.
4. **Uma analogia** que funcione em sala, se houver uma boa. Se não houver, pule.

**Gráficos:** gere quando o professor pedir (ou ofereça em uma linha quando o tema for visual: complexidade de algoritmos, crescimento de funções, recursão, estruturas de dados, fluxo de execução). Use matplotlib, salve o PNG na pasta da aula e mostre/envie a imagem. Gráficos claros: título que diz a conclusão, eixos rotulados, poucas cores. Se houver uma skill de visualização de dados disponível, siga-a. Para fluxos e estruturas (pilha, árvore, laço), um diagrama simples desenhado com matplotlib serve bem.

Se o professor pedir para guardar, salve como `explicacao.md` na pasta da aula. Pergunte no final se ficou alguma dúvida.

---

## Modo roteiro-de-aula

Objetivo: o professor abrir o roteiro e saber exatamente o que dizer em cada slide. O roteiro e os slides andam juntos: **um bloco do roteiro = um slide**, com a mesma numeração.

Se não souber tema, linguagem, nível ou duração, pergunte (ou use a pasta da aula aberta no start).

### Estrutura da aula (aprendizagem baseada em evidência)

Monte a sequência seguindo esta ordem, adaptando ao tempo:

1. **Gancho** — uma pergunta ou problema real que o tema resolve ("Como guardar as notas de 40 alunos sem criar 40 variáveis?").
2. **Objetivos** — "Ao final da aula você vai conseguir…", com verbos de ação (criar, calcular, corrigir).
3. **Lembrar o que já sabem** — uma pergunta rápida ligando ao conteúdo anterior.
4. **Conteúdo em blocos de 3–5 minutos** — um conceito por slide, sempre: ideia → código → saída → o que observar.
5. **Exemplo trabalhado** — resolver um problema passo a passo junto com a turma.
6. **"Agora é com vocês"** — um exercício curto para fazerem em sala.
7. **Correção** — resposta comentada e o erro mais comum.
8. **Resumo + aplicação** — 3 ideias para levar e uma pergunta de transferência ("onde mais você usaria isso?").

Princípios para os slides que o roteiro pede: o slide mostra **pouco** (palavras-chave, código, imagem), e a explicação fica na **fala** do professor. Texto longo no slide disputa atenção com a voz dele. Muitos itens num slide viram dois slides.

### Formato do roteiro (salve em `roteiro.md`)

```markdown
# Roteiro — <Título da aula>
**Turma:** <nível> · **Linguagem:** <linguagem> · **Duração:** <min> · **Slides:** <n>
**Objetivos:** <2–3 objetivos>
**Pré-requisitos:** <o que a turma já deve saber>

---
### Slide 1 — <título curto> · ⏱ 2 min
**Na tela:** <o que aparece no slide: título, até 5 itens curtos, ou "código 05_media.py">
**Fale:** "<a fala do professor, em frases curtas, no tom de sala de aula>"
**Pergunte:** <pergunta para a turma e a resposta esperada> *(quando fizer sentido)*
**Transição:** <a frase que liga ao próximo slide>
```

Regras da fala: assertiva, didática e natural para ser dita em voz alta, com frases curtas, exemplos concretos e uma ideia por vez. Nos slides de código, a fala guia a leitura ("Olhem a linha 4: aqui a gente soma…") e antecipa a saída antes de mostrá-la quando isso gerar curiosidade.

**Códigos do roteiro:** escreva cada código em `codigos/NN_nome.ext` (NN = número do slide), execute e confira a saída. Só entra no roteiro código que rodou. Os tempos dos slides devem somar a duração da aula.

Feche com uma seção **Para casa** (1–2 exercícios com resposta) e uma linha **Se sobrar tempo** (um desafio extra). Mostre o roteiro ao professor e pergunte se quer ajustar algo antes dos slides.

---

## Modo maquina-de-slides

Objetivo: um `.pptx` pronto para projetar, que abre no PowerPoint, no Google Slides e no LibreOffice, com as falas do roteiro nas notas do apresentador.

1. **Parta do roteiro.** Se existir `roteiro.md` na pasta da aula, use-o: mesma ordem, mesmos títulos, falas nas notas. Se não existir, faça primeiro um roteiro (modo roteiro-de-aula, versão enxuta) e mostre ao professor.

2. **Gere o print de cada código** com o Script 1:

   ```bash
   python Aulas-feitas/_ferramentas/print_codigo.py codigos/05_media.py prints/05_media.png
   ```

   O script executa o código, captura a saída real e desenha editor + terminal numa imagem. Ele **recusa** (sai com erro e não gera imagem) se o programa falhar, travar, ou se o código/saída forem longos demais para um slide. Quando recusar, corrija ou simplifique o código; nunca contorne a recusa desenhando a saída à mão. Para programas com `input()`, passe o que o "aluno" digitaria com `--stdin "Ana"` (aparece no terminal como numa execução real). O layout é automático: código curto fica com a saída embaixo; código com mais de 8 linhas fica lado a lado.

3. **Escreva `slides.json`** e monte com o Script 2:

   ```bash
   python Aulas-feitas/_ferramentas/montar_slides.py slides.json "Listas em Python.pptx"
   ```

   Tipos de slide disponíveis:

   ```json
   {"cor": "#2563EB", "slides": [
     {"tipo": "capa", "titulo": "Listas em Python", "subtitulo": "Aula 05 · Algoritmos", "notas": "fala..."},
     {"tipo": "pergunta", "texto": "Como guardar 40 notas sem 40 variáveis?", "notas": "..."},
     {"tipo": "topicos", "titulo": "Ao final da aula você vai conseguir", "itens": ["Criar uma lista", "..."], "notas": "..."},
     {"tipo": "secao", "titulo": "Mão no código", "notas": "..."},
     {"tipo": "codigo", "titulo": "Média de uma lista", "imagem": "prints/05_media.png", "legenda": "sum() soma, len() conta", "notas": "..."}
   ]}
   ```

   `notas` recebe a fala + pergunta + transição daquele slide no roteiro. Use `pergunta` para o gancho e para o "agora é com vocês"; `secao` para separar blocos; `topicos` com no máximo 5 itens curtos (o script corta o resto). A cor é opcional; use a do professor ou da instituição se ele disser.

4. **Confira antes de entregar.** Converta para imagens e olhe cada slide: texto cortado, print pequeno demais para ler de longe, slide vazio ou poluído.

   ```bash
   soffice --headless --convert-to pdf "Listas em Python.pptx" && pdftoppm -r 50 -png "Listas em Python.pdf" conf
   ```

   Se não houver LibreOffice, pelo menos reabra o `.pptx` com python-pptx e confira a contagem de slides e as notas.

5. **Entregue** o `.pptx` (envie o arquivo para o professor se a conversa permitir), diga em uma linha quantos slides tem e que as falas estão nas notas do apresentador. Se ele quiser no Google Slides, é só subir o `.pptx` no Drive e abrir com Google Slides.

---

## Script 1 — `print_codigo.py`

```python
"""print_codigo.py - executa um codigo, captura a saida REAL e gera um PNG
(editor em cima, terminal com a saida embaixo) para colar no slide.

Uso:  python print_codigo.py exemplo.py saida.png [--stdin "texto"] [--layout auto|vertical|lado]
Linguagens: .py .js .c .cpp .java (Java via "java Arquivo.java").
Sai com codigo 1 e NAO gera imagem se o programa falhar, demorar mais de
10 s, ou se codigo/saida forem longos demais para um slide.
"""
import argparse, os, shutil, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
from pygments import lex
from pygments.lexers import get_lexer_for_filename
from pygments.styles import get_style_by_name

def comando(arq, pasta):
    ext = os.path.splitext(arq)[1].lower()
    exe = os.path.join(pasta, "prog.exe" if os.name == "nt" else "prog")
    if ext == ".py":   # input() ecoa o que foi digitado, igual ao terminal real
        eco = ("import builtins,runpy,sys;_i=builtins.input\n"
               "def _e(p=''):\n v=_i(p);print(v);return v\n"
               "builtins.input=_e;sys.argv=[sys.argv[1]];runpy.run_path(sys.argv[0],run_name='__main__')")
        return [[sys.executable, "-c", eco, arq]]
    if ext == ".js":   return [["node", arq]]
    if ext == ".c":    return [["gcc", arq, "-o", exe, "-lm"], [exe]]
    if ext == ".cpp":  return [["g++", arq, "-o", exe], [exe]]
    if ext == ".java": return [["java", arq]]
    sys.exit(f"Extensao {ext} sem comando definido.")

def executar(arq, entrada):
    pasta = tempfile.mkdtemp()
    dest = os.path.join(pasta, os.path.basename(arq))
    shutil.copy(arq, dest)
    saida, cmds = "", comando(dest, pasta)
    for i, cmd in enumerate(cmds):
        try:
            r = subprocess.run(cmd, input=entrada if i == len(cmds) - 1 else None,
                               capture_output=True, text=True, timeout=10, cwd=pasta)
        except subprocess.TimeoutExpired:
            sys.exit("ERRO: passou de 10 s. Nao gero print de codigo que trava.")
        if r.returncode != 0:
            print(r.stdout + r.stderr)
            sys.exit(f"ERRO: o programa falhou (codigo {r.returncode}). Corrija antes de usar no slide.")
        saida = r.stdout
    return saida.rstrip("\n")

def fonte(tam):
    for f in ["DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
              "C:/Windows/Fonts/consola.ttf", "/System/Library/Fonts/Menlo.ttc", "cour.ttf"]:
        try: return ImageFont.truetype(f, tam)
        except OSError: pass
    return ImageFont.load_default()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("codigo"); ap.add_argument("png")
    ap.add_argument("--stdin", default=None, help="entrada digitada pelo 'aluno'")
    ap.add_argument("--max-linhas", type=int, default=20)
    ap.add_argument("--max-saida", type=int, default=12)
    ap.add_argument("--layout", choices=["auto", "vertical", "lado"], default="auto",
                    help="auto: lado a lado se o codigo tiver mais de 8 linhas")
    a = ap.parse_args()

    codigo = open(a.codigo, encoding="utf-8").read().rstrip("\n").replace("\t", "    ")
    linhas = codigo.split("\n")
    if len(linhas) > a.max_linhas:
        sys.exit(f"ERRO: {len(linhas)} linhas (> {a.max_linhas}). Simplifique ou divida em dois slides.")
    saida = executar(a.codigo, a.stdin)
    out = saida.split("\n") if saida else ["(sem saida no terminal)"]
    if a.stdin and not a.codigo.endswith(".py"):
        out =[f"> entrada: {l}" for l in a.stdin.rstrip("\n").split("\n")] + out
    if len(out) > a.max_saida:
        sys.exit(f"ERRO: saida com {len(out)} linhas (> {a.max_saida}). Reduza o que o programa imprime.")

    try: estilo = get_style_by_name("one-dark")
    except Exception: estilo = get_style_by_name("monokai")
    fundo = estilo.background_color or "#282c34"
    F, S = 30, 30 * 1.55                      # tamanho da fonte e altura da linha
    f = fonte(F); cw = f.getlength("M")
    lado = a.layout == "lado" or (a.layout == "auto" and len(linhas) > 8)
    w_cod = cw * (max(len(l) for l in linhas) + 5) + 100
    w_out = cw * (max(len(l) for l in out) + 2) + 100
    H_cod = int(S * len(linhas) + 40); H_out = int(S * len(out) + 70)
    if lado:   # codigo a esquerda, terminal a direita: aproveita o 16:9 do slide
        w_out = max(w_out, cw * 16 + 100)
        W = int(w_cod + w_out); H = int(70 + max(H_cod, H_out) + 30)
        xt, yt = int(w_cod), 10
    else:      # codigo em cima, terminal embaixo
        W = int(max(w_cod, w_out, cw * 40 + 100)); H = 70 + H_cod + H_out + 30
        xt, yt = 10, 90 + H_cod
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([10, 10, W - 10, H - 10], 22, fill=fundo)
    # painel do terminal (cantos arredondados so do lado de fora)
    d.rounded_rectangle([xt, yt, W - 10, H - 10], 22, fill="#0d1117",
                        corners=(False, True, True, False) if lado else (False, False, True, True))
    d.rectangle([xt, yt, W - 40, H - 40] if not lado else [xt, yt, xt + 30, H - 10], fill="#0d1117")
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        d.ellipse([40 + i * 38, 32, 62 + i * 38, 54], fill=c)
    d.text(((xt if lado else W) / 2, 43), os.path.basename(a.codigo), font=fonte(24), fill="#9da5b4", anchor="mm")

    x0, y = 50, 90
    for n in range(len(linhas)):
        d.text((x0, y + n * S), f"{n + 1:>2}", font=f, fill="#5c6370")
    x, ln = x0 + cw * 4, 0
    for tok, txt in lex(codigo, get_lexer_for_filename(a.codigo)):
        st = estilo.style_for_token(tok); cor = "#" + (st["color"] or "abb2bf")
        for j, parte in enumerate(txt.split("\n")):
            if j: ln += 1; x = x0 + cw * 4
            if parte:
                d.text((x, y + ln * S), parte, font=f, fill=cor); x += f.getlength(parte)

    xs, ys = (xt + 40, 32) if lado else (x0, yt + 18)
    d.text((xs, ys), "SAÍDA", font=fonte(22), fill="#7ee787")
    for k, l in enumerate(out):
        d.text((xs, (90 if lado else yt + 58) + k * S), l, font=f,
               fill="#8b949e" if l.startswith("> entrada") else "#e6edf3")
    img.save(a.png)
    print(f"OK: {a.png} ({W}x{H}) | saida real:\n{saida}")

if __name__ == "__main__":
    main()
```

## Script 2 — `montar_slides.py`

```python
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
```
