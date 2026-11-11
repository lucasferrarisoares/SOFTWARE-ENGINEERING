# Revisão final e testes manuais

Etapa 06 **reexecutada em 11/11/2026 após a refatoração para o padrão da Prática 4**, no Windows, com Python 3.13.2, PLY 3.11 incluído no projeto e MEPA original em português. Todas as execuções desta revisão usaram uma cópia isolada com os sete módulos atuais, incluindo `definicoes.py`. As saídas abaixo foram observadas ao executar a CLI e o interpretador, separadamente da suíte `unittest`.

## Como reproduzir

Na raiz do trabalho, no PowerShell:

```powershell
$codaPython = 'C:\Users\Lukinhaa\AppData\Local\Programs\Python\Python313\python.exe'
$codaSaida = Join-Path $env:TEMP 'coda-demonstracao.mepa'
& $codaPython -B main.py testes/manuais/integracao.coda -o $codaSaida
'5 1' | & $codaPython -B mepa/mepa_pt.py --progfile $codaSaida --silent
'0 0' | & $codaPython -B mepa/mepa_pt.py --progfile $codaSaida --silent
```

Em outra instalação, ajuste apenas o caminho do Python (requer Python 3.10 ou superior). Não é necessário instalar PLY pela rede.

O programa `integracao.coda` combina recursão direta com variável local preservada, recursão mútua, chamada antecipada, função `void`, alteração de global, parâmetro que oculta uma global, passagem por valor e descarte de resultado em laço. A entrada `n` desta demonstração deve ser não negativa.

## Resultados observados

Cada número da coluna de saída é impresso em uma linha. A MEPA também informa a quantidade de instruções em `stderr`. As dez execuções abaixo foram conferidas na cópia isolada, usando `-E -s -B` no compilador e no interpretador.

| Fonte | Entrada | Saída observada e esperada | Instruções executadas |
|---|---|---|---|
| `testes/validos/fatorial.coda` | — | `120` | 91 |
| `testes/coda/ok_08_recursao_fatorial.coda` | — | `120` | 91 |
| `testes/validos/parametro_por_valor.coda` | — | `7, 100` | 2535 |
| `testes/coda/ok_05_entrada_saida.coda` | `-8 0` | `-8, 0, -7` | 16 |
| `testes/coda/ok_05_entrada_saida.coda` | `4 1` | `4, 1, 5` | 16 |
| `testes/manuais/integracao.coda` | `5 1` | `15, 0, 1, 0, 5, 15, 5` | 416 |
| `testes/manuais/integracao.coda` | `0 0` | `0, 1, 0, 1, 0, 10, 0` | 76 |
| `testes/validos/soma.coda` | — | `6` | 64 |
| `testes/coda/ok_03_condicional.coda` | — | `9` | 23 |
| `testes/coda/ok_36_unarios_encadeados.coda` | — | `-3, 1, 5` | 24 |

As duas execuções da integração usaram `--debug` e confirmaram `s=-1` na instrução `PARA`: locais, argumentos, resultados descartados e globais foram liberados. Com `0 0`, o laço não executa. `--verificar` para o mesmo fonte retornou status 0, sem saída. O programa de soma também foi compilado em `stdout`; essa saída foi gravada e executada na MEPA, produzindo `6`, sem mensagens extras misturadas às instruções.

## Erros pela CLI

Os sete casos abaixo foram compilados com `-o` apontando para um arquivo que já continha `conteudo anterior`. Todos retornaram **status 1**, `stdout` vazio, diagnóstico em `stderr` e preservaram o conteúdo anterior.

| Caso | Diagnóstico observado |
|---|---|
| `testes/invalidos/caractere_invalido.coda` | Erro léxico na linha 2: símbolo `@` |
| `program P { print(); }` | Erro sintático na linha 1: `)` inesperado |
| `testes/invalidos/tipo_incompativel.coda` | Erro semântico na linha 3: esperado `int`, recebido `bool` |
| `testes/invalidos/retorno_parcial.coda` | Erro semântico na linha 2: `positivo` pode chegar ao fim sem executar `return` |
| `program P { fun f() -> void {} print(f()); }` | Erro semântico na linha 1: função `void` não produz valor em expressão |
| `program P { fun f(int x) -> int { return x; } print(f()); }` | Erro semântico na linha 1: esperado 1 argumento, recebido 0 |
| Caminho de fonte inexistente | Erro de leitura de arquivo |

Os três fontes escritos diretamente na tabela foram criados em arquivos temporários. Para repetir um caso persistente:

```powershell
Set-Content -Encoding ASCII -LiteralPath $codaSaida -Value 'conteudo anterior'
& $codaPython -B main.py testes/invalidos/retorno_parcial.coda -o $codaSaida
$LASTEXITCODE
Get-Content -LiteralPath $codaSaida
```

## Revisão dos 19 exemplos recebidos

Todos foram novamente executados pela CLI com `--verificar`: quatro aceitos e quinze rejeitados, com os mesmos motivos da revisão anterior. O prefixo do nome não substitui a gramática do enunciado.

| Casos em `testes/coda/` | Resultado |
|---|---|
| `ok_03`, `ok_05`, `ok_08`, `ok_36` | Aceitos e executados na MEPA, conforme tabela acima |
| `ok_01`, `ok_02`, `ok_04`, `ok_14` | Rejeitados: declaração de variável depois de comandos (linhas 4, 4, 4 e 5) |
| `ok_06` | Rejeitado: função declarada depois de uma atribuição, linha 5 |
| `ok_07` | Rejeitado: `return;` não pertence à gramática; funções `void` não têm `return`, linha 4 |
| `ok_17` | Rejeitado: declaração com vírgula, linha 2; a gramática declara uma variável por comando |
| `erro_lexico_01`, `erro_lexico_03` | Erros léxicos de `@` e decimal, linhas 4 e 3 |
| `erro_sintatico_01`, `erro_sintatico_05` | Erros sintáticos, linhas 2 e 3 |
| `erro_semantico_01`, `erro_semantico_03` | Nome não declarado e atribuição incompatível, linhas 2 e 3 |
| `erro_semantico_09`, `erro_semantico_12` | Aridade e retorno incompatível, linhas 6 e 3 |

Os exemplos e a MEPA recebidos não foram alterados. A aceitação dos sete `ok_` divergentes exige esclarecimento da professora sobre a gramática, e não foi incorporada como extensão silenciosa.

## Validação isolada

Foi criada uma pasta temporária contendo apenas os sete módulos do compilador, `ply/`, `mepa/` e `testes/`. Não foram copiados `referencias/`, `planejamento_ia/`, `ply-master/`, caches Python ou metadados Git. A importação confirmou PLY 3.11 (`ply`, `ply.lex` e `ply.yacc`) e `definicoes.py` dentro dessa cópia. Os 53 arquivos copiados tiveram seu conteúdo conferido por SHA-256 antes e depois da execução, sem alterações no original ou na cópia durante a validação.

Executado a partir da cópia, com variáveis `PYTHON*` herdadas removidas do processo de revisão e `PYTHONNOUSERSITE=1` para seus subprocessos. O processo inicial também usou `-E -s` para desabilitar a influência dessas variáveis e dos pacotes do usuário:

```powershell
& $codaPython -E -s -B -m unittest discover -s testes -v
```

Resultado: **75 testes aprovados em 6,679 segundos** (9 do lexer, 12 do parser, 20 da semântica, 10 da CLI e 24 da geração/execução MEPA). A suíte e os programas de teste permaneceram inalterados. Não foram gerados `__pycache__`, `parsetab.py` ou `parser.out` na cópia. Nenhuma correção adicional no compilador foi necessária; a documentação do pacote foi corrigida para incluir `definicoes.py`.

O pacote mínimo de execução contém `main.py`, `lexer.py`, `parser.py`, `nos_ast.py`, **`definicoes.py`**, `semantico.py`, `gerador_mepa.py`, `ply/` e `mepa/`. Para revisão e demonstração, incluir também os testes, README, especificação, guia, comparação com a Prática 4 e roteiro de apresentação. Preserve os avisos de autoria e licença das dependências.

## Convenções e limites

Permanecem as convenções documentadas no README: booleanos em entrada/saída como 0/1, divisão negativa conforme `DIVI`, operadores lógicos sem curto-circuito e variáveis sem inicialização implícita. A análise conservadora de retorno é uma exigência adicional escolhida pelo usuário. Eventual orientação diferente da professora pode exigir ajustes. A validação foi feita no Windows com Python 3.13.2; não comprova testes em outros sistemas ou versões.
