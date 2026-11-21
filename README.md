# sin215 — skill de preparação de aulas de programação

Uma skill para o Claude (Claude.ai e Claude Code) feita para professores de programação. Ela leva a aula do tema aos slides:

| Comando | O que faz |
|---|---|
| `/sin215 start` | Mostra o passo a passo, pergunta o tema e confere na pasta `Aulas-feitas` se já existe uma aula com título igual ou parecido. Se existir, pede confirmação antes de criar outra. |
| `/sin215 explico-para-voce` | Explica o assunto para o professor de forma objetiva, com códigos executados (saída real), erros comuns dos alunos e gráficos quando pedido. |
| `/sin215 roteiro-de-aula` | Roteiro slide a slide: o que fica na tela, o que falar, pergunta para a turma, transição e tempo. |
| `/sin215 maquina-de-slides` | Gera o `.pptx` com o print de cada código já com a saída real, e as falas do roteiro nas notas do apresentador. |

## A regra principal: não inventar

Todo código que aparece foi executado. O script `print_codigo.py` roda o código, captura a saída de verdade e só então desenha a imagem. Ele recusa (não gera imagem) se o código der erro, travar ou for longo demais para um slide. Funciona com Python, JavaScript, C, C++ e Java.

## Estrutura

```
sin215/
├── skills/sin215/SKILL.md        ← a skill
├── Aulas-feitas/                 ← pasta onde as aulas são salvas
│   └── _ferramentas/
│       ├── print_codigo.py       ← print do código + saída real
│       └── montar_slides.py      ← monta o .pptx a partir de um JSON
└── exemplo/                      ← uma aula de exemplo (Listas em Python)
```

Cada aula nova vira uma pasta `Aulas-feitas/AAAA-MM-DD - Título/` com `roteiro.md`, `codigos/`, `prints/`, `slides.json` e o `.pptx`.

## Como instalar

**Claude Code:** copie a pasta `skills/sin215` para `~/.claude/skills/sin215` (no Windows, `C:\Users\<você>\.claude\skills\sin215`). Ou, com o Skills CLI:

```bash
npx skills add apollodevvv/sin215
```

**Claude.ai:** compacte a pasta `skills/sin215` em um `.zip` e envie em Configurações → Capacidades → Skills.

Depois, deixe a pasta `Aulas-feitas` no lugar onde você trabalha (ou na sua pasta pessoal). Se ela não existir, a skill cria.

## Requisitos

- Python 3.9+ com `pip install pillow pygments python-pptx`
- Para outras linguagens: `node`, `gcc`/`g++` ou `java` instalados
- Opcional: LibreOffice, para a skill conferir os slides renderizados antes de entregar

## Créditos e referências

As ideias de didática vieram de skills públicas que foram estudadas e adaptadas:
[educational-presentation](https://github.com/guia-matthieu/clawfu-skills) (estrutura de aula de Gagné, princípios de Mayer),
[canva-classroom-helper](https://github.com/canva-sdks/canva-skills) (falas nas notas do apresentador) e
[teach](https://github.com/mattpocock/skills) (prática de recuperação e foco no objetivo da turma).

## Licença

MIT
