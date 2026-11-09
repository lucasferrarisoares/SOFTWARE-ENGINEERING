# Compilador Coda

Trabalho de Introdução à Compilação, conforme a [especificação](especifica_o_coda.md).

## Estado da implementação

O lexer está implementado em `lexer.py`. Reconhece reservadas, identificadores, inteiros, operadores e delimitadores; ignora comentários e espaços; preserva linhas e interrompe no primeiro erro léxico com `ValueError`.

O parser está implementado em `parser.py`, com nós da AST em `nos_ast.py`. Reconhece todas as construções do Apêndice I, respeita a precedência dos operadores e devolve uma árvore com linhas de origem. Erros sintáticos, incluindo fim inesperado do arquivo, interrompem a análise com `ValueError`.

A análise semântica está implementada em `semantico.py`. Valida declarações, escopos, tipos, chamadas e retornos, preservando as tabelas global e locais para a futura geração de código. `main.py` integra as três análises no modo `--verificar`.

`gerador_mepa.py` gera código executável para programas sem funções: globais, expressões, atribuições, entrada/saída, condicionais e laços. A geração de funções e a integração final continuam pendentes. A sequência de trabalho está no [guia](GUIA_IMPLEMENTACAO_CODA.md).

## Ambiente e testes

Materiais adicionados em 09/11/2026:

- `testes/coda/`: 19 programas recebidos originalmente em `testes-coda/`, com nomes e conteúdo preservados. Esses casos ficam separados dos testes automatizados `testes/test_*.py` e dos exemplos locais em `testes/validos/` e `testes/invalidos/`.
- `mepa/`: oito arquivos originais do interpretador MEPA, mantidos juntos para preservar seus imports. A etapa 04 foi validada com `mepa/mepa_pt.py`, versão 5.0, sem modificar a máquina.

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

Os testes usam `unittest`, da biblioteca padrão. Verificam as três análises e a CLI, além de compilar programas sem funções e executar o código na MEPA recebida. A geração é verificada por saídas reais e pelo rastreamento da pilha da máquina.

Validação em 09/11/2026: **59 testes aprovados** (9 do lexer, 12 da AST/parser, 17 da semântica, 9 da CLI e 12 da geração/execução MEPA) no Python 3.13.2 com PLY 3.11 local. A construção das tabelas LALR também foi inspecionada na etapa 02: nenhum aviso ou conflito pendente. O parser não grava tabelas ou relatórios no diretório do projeto durante o uso normal.

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

Erros semânticos lançam `ValueError` com linha e motivo. A análise não imprime mensagens nem executa o programa. As convenções de execução adotadas na geração estão descritas abaixo.

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

`--verificar` executa somente as análises e também aceita programas com funções semanticamente válidas. Para conferir um erro semântico, use `testes/invalidos/tipo_incompativel.coda`; o diagnóstico aponta a atribuição incompatível na linha 3.

## Compilação e execução MEPA

Sem `--verificar`, a CLI gera código MEPA. Use `-o` para gravar um arquivo UTF-8, inclusive no PowerShell:

```text
python main.py testes/validos/soma.coda -o programa.mepa
python mepa/mepa_pt.py --progfile programa.mepa --silent
```

Nesta máquina, substitua `python` pelo caminho já indicado:

```powershell
& 'C:\Users\Lukinhaa\AppData\Local\Programs\Python\Python313\python.exe' -B main.py testes/validos/soma.coda -o programa.mepa
& 'C:\Users\Lukinhaa\AppData\Local\Programs\Python\Python313\python.exe' -B mepa/mepa_pt.py --progfile programa.mepa --silent
```

O programa imprime **6**. Sem `-o`, o compilador escreve apenas as instruções em `stdout`. `--verificar` e `-o` são mutuamente exclusivos. A geração termina antes de escrever a saída; erros de análise ou funcionalidades ainda não suportadas preservam um arquivo de saída existente. O destino não pode ser o próprio arquivo-fonte.

`gerar(programa, tabelas)` devolve uma lista de instruções e acrescenta `endereco` aos símbolos globais já existentes, sem repetir a semântica. As posições começam em zero e são acessadas com nível léxico 0. O programa usa `INPP`, reserva/libera globais com `AMEM`/`DMEM`, termina a execução com `PARA` e encerra o arquivo com `FIM`. Rótulos são alfanuméricos, como `L0: NADA`; argumentos de memória usam vírgula sem espaços, como `CRVL 0,1`.

Convenções desta implementação, baseadas nas operações da MEPA recebida:

- Booleanos: `false = 0` e `true = 1`. Para `read` de booleanos, forneça `0` ou `1`; `print` escreve um número por linha. `LEIT` aceita inteiros e não valida o domínio booleano; valores diferentes de 0/1 não são normalizados pelo compilador.
- Divisão: `DIVI` aplica `//`, arredondando para baixo. Assim, `-7 / 3` resulta em `-3` nesta máquina.
- Lógicos: `&&` e `||` usam `CONJ` e `DISJ`, com avaliação da esquerda para a direita e **sem curto-circuito**. Ambos os operandos são avaliados, inclusive se o segundo provocar erro de execução. Essa é a convenção adotada com as operações nativas; o enunciado não especifica curto-circuito. Confirmar com a professora se a linguagem exige comportamento diferente.
- Variáveis: `AMEM` reserva espaço sem inicialização implícita. Atribua ou leia um valor antes de usá-lo.

O interpretador lê números da entrada padrão, separados por espaços ou linhas; termine a entrada com quebra de linha, conforme seu leitor. `--infile dados.txt` permite usar um arquivo de entrada. Os limites padrão são 500 instruções de programa, 500 posições configuradas de pilha e 10.000 instruções executadas, ajustáveis pelas opções da máquina.

Mesmo com `--silent`, a MEPA escreve a contagem de instruções executadas em `stderr`. A versão recebida captura `SystemExit` e pode retornar status 0 após um diagnóstico de erro; os testes exigem também a mensagem de término e a saída esperada.

Limitação atual: programas que declaram funções são rejeitados na geração com diagnóstico da etapa 05 e sem saída MEPA parcial. Funções, parâmetros e recursão continuam disponíveis nas três análises, mas ainda não na geração. Os casos recebidos que divergem da gramática foram preservados; a execução desta etapa inclui os casos compatíveis `ok_03`, `ok_05` e `ok_36`.
