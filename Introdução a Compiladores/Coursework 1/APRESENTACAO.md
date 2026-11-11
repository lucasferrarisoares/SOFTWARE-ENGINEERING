# Roteiro de demonstração do compilador Coda

Material para estudo e demonstração pela dupla. A execução técnica está verificada; cada integrante deve praticar as explicações e executar os exemplos antes da apresentação.

## 1. Mostrar o fluxo completo

`arquivo.coda → lexer → parser/AST → semântica/tabelas → gerador → arquivo.mepa → interpretador`

| Arquivo | O que explicar |
|---|---|
| `lexer.py` | PLY reconhece tokens; palavra reservada não vira identificador; sinal negativo é separado do número; comentários são ignorados e linhas preservadas |
| `nos_ast.py` | Nós representam declarações, comandos e expressões; linhas permitem localizar erros; delimitadores não precisam de nós |
| `parser.py` | Repetições EBNF viram listas com recursão à esquerda; precedência resolve expressões; o parser constrói a AST sem traduzir diretamente para MEPA |
| `semantico.py` | Tabelas dos níveis 0 e 1, duplicidades, resolução local antes da global, validação de tipos e assinaturas |
| `gerador_mepa.py` | Travessia da AST, endereços e rótulos, saltos, chamadas e equilíbrio da pilha |
| `main.py` | Leitura UTF-8, ordem das etapas, `--verificar`, `-o` e diagnóstico com status de erro |

## 2. Executar programas

Na raiz do projeto, ajustar o caminho do Python conforme a instalação:

```powershell
$codaPython = 'C:\Users\Lukinhaa\AppData\Local\Programs\Python\Python313\python.exe'
$codaSaida = Join-Path $env:TEMP 'coda-apresentacao.mepa'
& $codaPython -B main.py testes/validos/fatorial.coda -o $codaSaida
Get-Content -LiteralPath $codaSaida
& $codaPython -B mepa/mepa_pt.py --progfile $codaSaida --silent
& $codaPython -B main.py testes/manuais/integracao.coda -o $codaSaida
'5 1' | & $codaPython -B mepa/mepa_pt.py --progfile $codaSaida --silent
& $codaPython -B main.py --verificar testes/invalidos/retorno_parcial.coda
$LASTEXITCODE
```

Fatorial imprime `120`. A integração imprime `15, 0, 1, 0, 5, 15, 5`, um valor por linha. O último comando rejeita o retorno parcial com status 1. Os [testes manuais](testes/manuais/README.md) apresentam outros casos e resultados.

## 3. Explicar as decisões no código

- **Precedência:** em `2 + 3 * 4`, a multiplicação é a subárvore direita da soma. Parênteses alteram o agrupamento; comparações do mesmo nível não podem ser encadeadas.
- **Visibilidade:** todas as assinaturas são instaladas antes de analisar os corpos. Isso permite chamadas antecipadas e recursão. Parâmetros e locais compartilham uma tabela; blocos não criam escopo.
- **Passagem por valor:** alterar um parâmetro muda sua célula na ativação da função, sem modificar a variável do chamador. Uma função ainda pode modificar globais visíveis por nome.
- **Chamadas MEPA:** o chamador reserva o resultado, se houver, e empilha argumentos. `CHPR`/`ENPR` estabelecem a ativação; `RTPR` restaura a anterior. Locais recursivas têm posições próprias em cada ativação.
- **Retorno:** o resultado ocupa `-(n+5)` em relação a `D[1]`; parâmetros ocupam `i-n-4` e locais começam em zero. `return` salta para um epílogo comum. O README detalha as quatro células de controle.
- **Descarte:** uma chamada com valor usada como comando emite `DMEM 1`, evitando acumular resultados em laços.
- **Erros:** as fases levantam `ValueError`; a CLI apresenta o diagnóstico em `stderr` e só escreve código após a análise completa.
- **Retorno parcial:** a regra adicional solicitada rejeita caminhos que possam chegar ao fim. A análise é conservadora e reconhece booleanos literais, sem provar expressões ou relações entre condições.

## 4. Preparar respostas e entrega

Cada integrante deve conseguir localizar no código uma resolução de nome, uma produção do parser, uma verificação de tipo e uma chamada recursiva. Explicar por que as tabelas não guardam os valores das ativações em execução.

Apresentar as convenções de booleanos, divisão negativa e operadores lógicos documentadas no README. Explicar as divergências dos exemplos `ok_` usando a gramática original. Confirmar com a professora eventuais regras diferentes antes da submissão.

A revisão técnica passou nos 75 testes em cópia isolada e nas demonstrações manuais. A apresentação oral e a submissão ao Classroom são atividades dos integrantes e não foram realizadas por este roteiro.
