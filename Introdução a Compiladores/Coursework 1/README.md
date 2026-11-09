# Compilador Coda

Trabalho de Introdução à Compilação, conforme a [especificação](especifica_o_coda.md).

## Estado da implementação

O lexer está implementado em `lexer.py`. Reconhece reservadas, identificadores, inteiros, operadores e delimitadores; ignora comentários e espaços; preserva linhas e interrompe no primeiro erro léxico com `ValueError`.

O parser está implementado em `parser.py`, com nós da AST em `nos_ast.py`. Reconhece todas as construções do Apêndice I, respeita a precedência dos operadores e devolve uma árvore com linhas de origem. Erros sintáticos, incluindo fim inesperado do arquivo, interrompem a análise com `ValueError`.

A análise semântica está implementada em `semantico.py`. Valida declarações, escopos, tipos, chamadas e retornos, preservando as tabelas global e locais para a futura geração de código. `main.py` integra as três análises no modo `--verificar`.

A geração MEPA e a integração final com a máquina ainda estão pendentes. A sequência de trabalho está no [guia](GUIA_IMPLEMENTACAO_CODA.md).

## Ambiente e testes

Materiais adicionados em 09/11/2026:

- `testes/coda/`: 19 programas recebidos originalmente em `testes-coda/`, com nomes e conteúdo preservados. Esses casos ficam separados dos testes automatizados `testes/test_*.py` e dos exemplos locais em `testes/validos/` e `testes/invalidos/`.
- `mepa/`: oito arquivos originais do interpretador MEPA, mantidos juntos para preservar seus imports. A presença da máquina não significa que a geração MEPA já esteja implementada ou validada.

Os prefixos dos casos recebidos foram preservados, mas não comprovam aceitação pela especificação atual. Há arquivos `ok_` com declarações após comandos, declaração de múltiplas variáveis ou `return;`, construções ausentes da gramática vigente. A compatibilidade desses exemplos será tratada separadamente; esta organização não modifica o compilador nem os programas recebidos.

Python localizado nesta máquina: **3.13.2**, em `C:\Users\Lukinhaa\AppData\Local\Programs\Python\Python313\python.exe`. O pacote **PLY 3.11** está incluído em `ply/`, copiado da prática da disciplina, com autoria e licença preservadas nos arquivos. Não é necessário instalar dependências externas para executar os testes.

Na raiz deste trabalho, com Python disponível no PATH:

```text
python -B -m unittest discover -s testes -v
```

Nesta máquina, pelo PowerShell:

```powershell
& 'C:\Users\Lukinhaa\AppData\Local\Programs\Python\Python313\python.exe' -B -m unittest discover -s testes -v
```

Os testes usam `unittest`, da biblioteca padrão. Verificam tokens, estrutura da AST, precedência, sintaxe, tabelas de símbolos, tipos, escopos, chamadas e retornos. Também exercitam a CLI em processos separados, conferindo status e canais de saída. Os arquivos `.coda` em `testes/` são casos de análise; não há execução de programas Coda.

Validação em 03/11/2026: **43 testes aprovados** (9 do lexer, 12 da AST/parser, 17 da semântica e 5 da CLI) no Python 3.13.2 com PLY 3.11 local. A construção das tabelas LALR também foi inspecionada na etapa 02: nenhum aviso ou conflito pendente. O parser não grava tabelas ou relatórios no diretório do projeto durante o uso normal.

## Uso do lexer em Python

```python
from lexer import CodaLexer

lexer = CodaLexer()
lexer.input("program P { print(-42); }")
for token in iter(lexer.token, None):
    print(token.type, token.value, token.lineno)
```

`input()` reinicia a linha em 1. `token()` retorna um token PLY ou `None` ao terminar. Números têm valor Python `int`; demais tokens mantêm o texto original. O menos é separado do número, e o parser converte `true`/`false` para valores booleanos na AST. O lexer não imprime diagnósticos por conta própria.

## Uso do parser em Python

```python
from pathlib import Path
from pprint import pprint

from lexer import CodaLexer
from parser import CodaParser

texto = Path("testes/validos/parser_completo.coda").read_text(encoding="utf-8")
arvore = CodaParser().parse(texto, CodaLexer())
pprint(arvore)
```

O resultado é `Programa(nome, globais, funcoes, comandos, linha=...)`. Funções guardam parâmetros, tipo de retorno, declarações locais e comandos. Blocos são listas; `Condicional.senao` vale `None` quando não há `else` e uma lista quando há. `ChamadaComando` distingue uma chamada usada como comando de uma chamada dentro de expressão.

Todos os nós guardam `linha`: palavras-chave localizam programa, função e comandos; identificadores localizam declarações, parâmetros, destinos e chamadas; operadores localizam operações. Parênteses apenas alteram o agrupamento, sem criar um nó próprio.

O parser verifica a sintaxe e constrói a árvore. Tipos incompatíveis, nomes não declarados, chamadas `void` em expressões e retornos fora de função são verificados separadamente pela análise semântica. Uma AST construída não comprova que o programa seja semanticamente válido ou executável.

## Análise semântica

Depois de obter `arvore` com o parser:

```python
from semantico import analisar

tabelas = analisar(arvore)
pprint(tabelas)
```

`analisar()` devolve `{'global': tabela_global, 'locais': tabelas_por_nome_de_funcao}`. Cada tabela é um dicionário indexado pelo nome do identificador. Cada símbolo guarda `nome`, `categoria` (`variavel`, `parametro` ou `funcao`), `tipo`, `nivel`, `escopo` e `linha`. Em funções, `tipo` representa o retorno e `parametros` contém os tipos dos parâmetros na ordem da declaração.

O escopo global tem nível 0; parâmetros e variáveis locais compartilham o nível 1 de cada função. Blocos não criam escopos. A resolução procura primeiro no local, permitindo sombreamento, e depois no global. Todas as assinaturas são cadastradas antes dos corpos, permitindo recursão e chamadas antecipadas. As tabelas locais permanecem disponíveis após a verificação, sem modificar a AST ou compartilhar estado entre chamadas de `analisar()`.

Funções `int` e `bool` precisam conter pelo menos um `return` compatível, inclusive dentro de `if` ou `while`; não se exige retorno em todos os caminhos. Todos os comandos são verificados, inclusive após um retorno. Funções `void` não podem conter `return` nem produzir valor em uma expressão. Chamadas de qualquer tipo podem ser usadas como comando.

Erros semânticos lançam `ValueError` com linha e motivo. A análise não imprime mensagens, não executa o programa e não decide comportamentos ainda pendentes da MEPA, como divisão negativa ou curto-circuito.

## Verificação pela linha de comando

Com Python no PATH, execute na raiz do trabalho:

```text
python main.py --verificar testes/validos/semantica_escopos.coda
```

Nesta máquina, pelo PowerShell:

```powershell
& 'C:\Users\Lukinhaa\AppData\Local\Programs\Python\Python313\python.exe' -B main.py --verificar testes/validos/semantica_escopos.coda
$LASTEXITCODE
```

Sucesso retorna status **0**, sem saída. Erros de leitura ou de análise retornam **1**, com diagnóstico em `stderr` e `stdout` vazio. Argumentos inválidos retornam **2**. O arquivo-fonte deve estar em UTF-8.

Por enquanto, `--verificar` é obrigatório: a compilação para MEPA ainda não está disponível. Para conferir um erro semântico, use `testes/invalidos/tipo_incompativel.coda`; o diagnóstico aponta a atribuição incompatível na linha 3.
