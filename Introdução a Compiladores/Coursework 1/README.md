# Compilador Coda

Trabalho de Introdução à Compilação, conforme a [especificação](especifica_o_coda.md).

## Estado da implementação

O lexer está implementado em `lexer.py`. Reconhece reservadas, identificadores, inteiros, operadores e delimitadores; ignora comentários e espaços; preserva linhas e interrompe no primeiro erro léxico com `ValueError`.

O parser está implementado em `parser.py`, com nós da AST em `nos_ast.py`. Reconhece todas as construções do Apêndice I, respeita a precedência dos operadores e devolve uma árvore com linhas de origem. Erros sintáticos, incluindo fim inesperado do arquivo, interrompem a análise com `ValueError`.

Análise semântica, geração MEPA e CLI ainda não foram implementadas. A sequência de trabalho está no [guia](GUIA_IMPLEMENTACAO_CODA.md).

## Ambiente e testes

Python localizado nesta máquina: **3.13.2**, em `C:\Users\Lukinhaa\AppData\Local\Programs\Python\Python313\python.exe`. O pacote **PLY 3.11** está incluído em `ply/`, copiado da prática da disciplina, com autoria e licença preservadas nos arquivos. Não é necessário instalar dependências externas para executar os testes.

Na raiz deste trabalho, com Python disponível no PATH:

```text
python -B -m unittest discover -s testes -v
```

Nesta máquina, pelo PowerShell:

```powershell
& 'C:\Users\Lukinhaa\AppData\Local\Programs\Python\Python313\python.exe' -B -m unittest discover -s testes -v
```

Os testes usam `unittest`, da biblioteca padrão. Verificam tokens, valores, linhas, comentários e erros léxicos; também comparam a estrutura da AST, precedência e associatividade, listas, funções, comandos, rejeição de sintaxe inválida e reutilização após erros. Os arquivos `.coda` em `testes/` são casos de análise; não há execução de programas.

Validação em 03/11/2026: **21 testes aprovados** (9 do lexer e 12 da AST/parser) no Python 3.13.2 com PLY 3.11 local. A construção das tabelas LALR também foi inspecionada: nenhum aviso ou conflito pendente. O parser não grava tabelas ou relatórios no diretório do projeto durante o uso normal.

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

O parser verifica a sintaxe e constrói a árvore. Tipos incompatíveis, nomes não declarados, chamadas `void` em expressões e retornos fora de função serão verificados na próxima etapa, de análise semântica. Uma AST construída não comprova que o programa seja semanticamente válido ou executável.
