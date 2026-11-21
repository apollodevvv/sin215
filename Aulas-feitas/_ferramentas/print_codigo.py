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
