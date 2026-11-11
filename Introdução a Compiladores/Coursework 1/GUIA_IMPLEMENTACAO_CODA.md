# Planejamento de implementação do compilador Coda

Planejamento consolidado em **03/11/2026**, com base na [especificação](especifica_o_coda.md) e nos materiais locais. Este documento descreve trabalho futuro; não comprova implementação nem execução do compilador.

**Atualização da implementação em 09/11:** etapas 00 a 05 implementadas e verificadas, incluindo funções, parâmetros por valor e recursão na MEPA recebida. São 75 testes aprovados na suíte completa. A CLI gera código por padrão, grava com `-o` e mantém `--verificar`. O [README do projeto](README.md) registra ambiente, comandos, convenção de chamadas e a decisão adicional do usuário de rejeitar, na compilação, funções que possam terminar sem retorno. A etapa 06, de revisão final de integração, continua planejada.

## 1. Objetivo e situação atual

Implementar em Python com PLY o fluxo **fonte Coda → análise léxica → parser e AST → análise semântica → código MEPA**, acessível pela linha de comando.

O diretório contém a especificação, os seis módulos próprios do compilador, o PLY local, a máquina em `mepa/`, práticas de referência e casos recebidos em `testes/coda/`. O roteiro detalhado está em [planejamento_ia/README.md](planejamento_ia/README.md); essa pasta e `referencias/` estão ignoradas pelo Git, portanto não acompanham um clone comum.

O prazo informado no enunciado é **29/11/2026, às 23h59**. Não fazem parte do escopo otimizações, outros destinos de compilação ou uma implementação própria da MEPA.

## 2. Preparação do ambiente

1. Localizar um interpretador Python e registrar seu caminho e versão. Se mantido `field(kw_only=True)` das práticas, usar Python 3.10 ou superior; caso contrário, adequar as classes ao interpretador escolhido.
2. Usar a cópia **PLY 3.11** de `referencias/Pratica 1/ply/`, conforme a decisão já registrada no roteiro. Copiar o pacote para `ply/` na raiz do trabalho, mantendo os avisos de autoria e licença. Não misturar essa versão com `ply-master`.
3. Confirmar a importação local de `ply`, `ply.lex` e `ply.yacc`, registrando versão e caminho efetivamente importados.
4. Criar os casos de teste junto com cada funcionalidade. Não criar módulos vazios para representar progresso.

Na inspeção de 03/11, `python --version` falhou por comando não encontrado, e `Get-Command py,python3` não encontrou esses comandos. Isso não prova ausência de instalação fora do PATH. A versão 3.11 do PLY foi confirmada pela leitura de seu `__init__.py`, sem execução.

## 3. Arquitetura e contratos

| Módulo previsto | Responsabilidade e contrato |
|---|---|
| `lexer.py` | `CodaLexer`: expõe `tokens`, `input(texto)` e `token()`; reinicia a linha a cada entrada |
| `nos_ast.py` | Classes de dados para declarações, comandos e expressões, com localização |
| `parser.py` | `CodaParser.parse(texto, lexer)` devolve `Programa`; constrói a AST sem verificar tipos nem emitir MEPA |
| `semantico.py` | `analisar(programa)` valida e devolve `{'global': tabela_global, 'locais': tabelas_por_funcao}` |
| `gerador_mepa.py` | `gerar(programa, tabelas)` consulta as tabelas e devolve uma lista de instruções textuais |
| `main.py` | Lê o arquivo, coordena as fases e escreve a saída somente depois do sucesso completo |

Esses nomes são decisões do projeto. Cada compilação terá estado novo, sem carregar linhas, símbolos ou rótulos da anterior. Erros esperados de compilação serão `ValueError` com fase, localização disponível e motivo. A CLI tratará esses erros e falhas de leitura (`OSError`), usando `stderr` e código de saída diferente de zero. Defeitos internos não serão escondidos por captura genérica de exceções.

## 4. Análise léxica

- Reconhecer as 13 palavras reservadas da especificação, distinguindo maiúsculas de minúsculas.
- Identificadores: letra ASCII inicial, seguida de letras ASCII, dígitos ou `_`. Números: sequência de dígitos decimais, convertida em inteiro; o sinal é um token independente.
- Reconhecer todos os delimitadores e operadores do Apêndice I, incluindo vírgula, ponto e vírgula, `->`, `&&` e `||`. A lista resumida de símbolos contém omissões e espaços tipográficos; a gramática e as regras semânticas explicitam esses tokens.
- Ignorar espaços, tabulações, quebras de linha e comentários `//`, mantendo a contagem de linhas. Cobrir arquivos com LF e CRLF e comentário sem quebra final.
- Garantir distinção entre operadores compostos e prefixos, além de comentário e divisão. Interromper no primeiro caractere inválido.

Adaptações das práticas: não aceitar números reais; ampliar o identificador para maiúsculas e sublinhas internas; substituir impressão/continuação após erro pelo contrato de diagnóstico.

## 5. AST e parser

Estruturas propostas, todas com linha de origem:

| Nó | Campos principais, além da linha |
|---|---|
| `Programa` | `nome`, `globais`, `funcoes`, `comandos` |
| `Funcao` | `nome`, `parametros`, `tipo_retorno`, `locais`, `comandos` |
| `DeclaracaoVariavel`, `Parametro` | `nome`, `tipo` |
| `Atribuicao` | `destino` como identificador, `expressao` |
| `Condicional` | `condicao`, `entao`, `senao` opcional |
| `Repeticao` | `condicao`, `comandos` |
| `Retorno` | `expressao` |
| `Leitura`, `Escrita` | Lista de identificadores; lista de expressões, respectivamente |
| `ChamadaComando` | `chamada`, permitindo distinguir o descarte do resultado |
| `Chamada` | `nome`, `argumentos` |
| `OperacaoBinaria`, `OperacaoUnaria` | Operador e operandos |
| `Identificador` | `nome` |
| `Inteiro`, `Booleano` | `valor` |

Blocos serão listas de comandos, sem novos escopos. Parênteses e separadores não viram nós; parênteses preservam o agrupamento da árvore. Fixar os nomes concretos na etapa 02 antes de implementar seus consumidores.

Converter repetições EBNF para listas BNF, preferindo recursão à esquerda; opções terão alternativas vazias explícitas. Apenas declarações, comandos, parâmetros de função e argumentos de chamada admitem as ausências previstas na gramática. `read` e `print` exigem pelo menos um item.

As produções de expressões usarão diretamente os tokens de operadores, para que o PLY determine a precedência. Ordem crescente:

| Operadores | Associatividade |
|---|---|
| `||` | Esquerda |
| `&&` | Esquerda |
| `==`, `!=` | Não associativos |
| `<`, `<=`, `>`, `>=` | Não associativos |
| `+`, `-` binário | Esquerda |
| `*`, `/` | Esquerda |
| `-` unário, `!` | Direita |

Usar precedência específica para o menos unário. Verificar conflitos do parser, agrupamento da AST, erros em delimitadores e fim inesperado do arquivo. Declarações precedem comandos; funções só aparecem no global, depois das variáveis.

## 6. Análise semântica

Primeiro instalar variáveis globais e assinaturas de todas as funções; depois verificar os corpos e os comandos principais. Essa ordem atende à visibilidade global em todo o programa e permite resolver chamadas antes da posição textual da definição, além da recursão direta exigida.

Uma tabela global usa nível 0. Cada função tem uma tabela de nível 1 compartilhada por parâmetros e variáveis locais. Pesquisar primeiro no local e depois no global. Duplicidades no mesmo escopo geram erro sem substituir a declaração anterior; sombreamento do global é permitido. O símbolo encontrado determina a categoria: não procurar outra função global quando uma variável local oculta seu nome.

Símbolos guardam nome, categoria, tipo, nível e localização; funções também guardam a assinatura ordenada. Preservar as tabelas locais para a geração. Uma eventual pilha de escopos contém referências a essas tabelas, e não valores de execução da MEPA.

| Construção | Regra de validação |
|---|---|
| Variável e parâmetro | Tipo `int` ou `bool`; declaração visível; parâmetros podem receber atribuição |
| Atribuição | Destino variável/parâmetro; expressão do mesmo tipo |
| `+`, `-`, `*`, `/` e menos unário | Operandos `int`, resultado `int` |
| `<`, `<=`, `>`, `>=` | Operandos `int`, resultado `bool` |
| `==`, `!=` | Operandos do mesmo tipo primitivo, resultado `bool` |
| `&&`, `||`, `!` | Operandos `bool`, resultado `bool` |
| `if`, `while` | Condição `bool` |
| `read` | Identificadores de variáveis/parâmetros `int` ou `bool` |
| `print` | Expressões `int` ou `bool` |
| Chamada | Símbolo função; quantidade, ordem e tipos dos argumentos compatíveis |
| Uso de chamada | `void` apenas como comando; retorno `int`/`bool` também pode ser descartado |
| `return` | Expressão compatível em função `int`/`bool`; rejeitar em `void` e no principal |
| Função `int`/`bool` | Pelo menos um `return` válido; por convenção adicional do usuário, rejeitar fluxo que possa chegar ao fim sem retornar |

O parser aceita a construção sintática de retorno; a restrição ao contexto de função é verificada nesta fase. Analisar todos os comandos, sem dispensar verificações de tipos por parecerem inalcançáveis.

A regra de fluxo foi solicitada pelo usuário em 09/11/2026 e é mais restritiva que o enunciado, que exigia apenas a presença de `return`. Após validar os tipos, a análise verifica a continuação dos blocos: `return` encerra o fluxo; `if` não literal considera ambos os ramos; laços podem executar zero vezes, salvo `while (true)`, que não termina normalmente. Booleanos literais são reconhecidos; não há avaliação de expressões constantes, propagação de valores ou prova de condições correlacionadas. Os detalhes e exemplos estão no README.

## 7. Geração MEPA

A máquina recebida está em `mepa/`; a versão portuguesa é executada com `python mepa/mepa_pt.py --progfile programa.mepa --silent`. As etapas 04 e 05 usam os formatos e instruções de seu código original, preservado. A convenção de chamadas foi derivada de `call`, `entproc` e `retproc` em `mepa_interp.py` e está documentada no README.

Implementar em duas entregas:

1. Programa sem funções, concluído: início/fim, alocação global, constantes, operadores, atribuições, entrada/saída, condicionais e laços.
2. Funções, concluído: desvio sobre corpos, parâmetros por valor, locais, acesso ao global, chamadas, retorno antecipado, descarte de resultados e recursão.

O gerador percorre a AST e reutiliza os símbolos já validados, acrescentando endereços e rótulos quando necessário. Não repete a análise semântica. Cada expressão com valor deixa um resultado na pilha; comandos preservam o equilíbrio esperado. Ativações recursivas devem manter parâmetros e locais independentes.

Não fixar offsets, instruções ou comportamento de casos omissos por analogia com outra versão de MEPA. Código textual gerado não comprova execução correta.

## 8. Sequência de entregas

As datas abaixo são uma proposta de organização, ajustável à disponibilidade da dupla e do material MEPA.

| Período proposto | Entrega | Critério de conclusão |
|---|---|---|
| 03–05/11 | 00: ambiente e dependência | Python localizado e importação local do PLY executada |
| 06–08/11 | 01: lexer | Tokens, valores, linhas e erros conferidos |
| 09–12/11 | 02: AST e parser | Todas as construções e precedências verificadas |
| 13–17/11 | 03: semântica | Tipos, escopos, chamadas e retornos cobertos |
| 18–21/11 | 04: MEPA básica | Programas sem funções executados na máquina fornecida |
| 22–25/11 | 05: funções MEPA | Chamadas, recursão e equilíbrio da pilha verificados |
| 26–28/11 | 06: integração e revisão | CLI e execução final reproduzíveis; apresentação preparada |
| 29/11 | Reserva para entrega | Revisão do pacote antes do prazo de 23h59 |

A máquina foi recebida em 09/11. A CLI já gera programas com funções; a conclusão da entrega ainda depende da revisão de integração da etapa 06 e dos esclarecimentos de casos omissos registrados abaixo.

## 9. Matriz mínima de validação

| Área | Casos e resultado esperado |
|---|---|
| Lexer | Reservadas versus identificadores, todos os operadores, `-42` em dois tokens, comentários e reinício da linha; rejeitar `@`, `_nome`, `10.5` |
| Sintaxe | Programa vazio, listas, blocos e chamadas; rejeitar `read()`, `print()`, `return;`, funções aninhadas e declaração com inicialização |
| Precedência | `2 + 3 * 4` agrupa multiplicação; `10 - 3 - 2` agrupa à esquerda; `!true && false` agrupa negação |
| Não associação | Rejeitar `1 < 2 < 3` e `true == false == true`; aceitar sintaticamente `1 < 2 == true` |
| Nomes e tipos | Sombreamento válido; duplicidade, nome ausente, função usada como variável e condição inteira rejeitados |
| Funções | Assinaturas, parâmetros, chamada antecipada, recursão, retorno incompatível/ausente, chamada `void` em expressão |
| Semântica do retorno | Pela convenção do usuário, rejeitar retorno parcial; aceitar ambos os ramos com retorno ou retorno final; rejeitar retorno em `void` e no principal |
| MEPA básica | Caso soma da etapa 04 imprime `6`; variante sem iterações imprime `0` |
| MEPA com funções | Fatorial imprime `120`; caso de passagem por valor da etapa 05 imprime `7` e `100` |
| CLI | Erros léxicos, sintáticos, semânticos e de leitura: status não zero, diagnóstico em `stderr`, `stdout` vazio |
| Isolamento | Compilações sucessivas sem estado residual; pacote executável sem as pastas ignoradas |

Casos de AST verificam a estrutura, não só a existência de uma raiz. Resultados numéricos exigem execução na MEPA. A etapa 04 cobre entrada booleana 0/1, divisão negativa e lógicos conforme as operações nativas recebidas; eventuais exigências diferentes da linguagem permanecem sujeitas a esclarecimento.

## 10. Pendências e decisões a confirmar

| Pendência | Impacto e próximo passo |
|---|---|
| Ambiente Python | Resolvido: Python 3.13.2 localizado e importação local do PLY verificada |
| Máquina MEPA | Recebida e executada: versão 5.0 em `mepa/mepa_pt.py`; convenção de chamadas documentada e validada na etapa 05 |
| Booleanos em entrada/saída | Adotados 0/1; `LEIT`/`IMPR` operam com inteiros. Confirmar eventual exigência de validação de outros valores de entrada |
| Divisão com operandos negativos | Implementada conforme `DIVI`, que usa `//` e arredonda para baixo; confirmar se a disciplina exige regra distinta |
| Avaliação de `&&` e `||` | Implementada da esquerda para a direita, sem curto-circuito, por `CONJ`/`DISJ`; confirmar eventual exigência diferente da Coda |
| Caminho de função sem executar `return` | Resolvido por decisão do usuário em 09/11: erro semântico na compilação quando a análise conservadora identificar possibilidade de chegar ao fim; sem retorno padrão e sem alterar a MEPA |
| Variável lida antes de atribuição | Confirmar comportamento; não inventar análise obrigatória de inicialização |
| Nome do programa na tabela | Confirmar se participa do espaço de nomes; a especificação explicita instalação de variáveis, funções e parâmetros |

Casos omissos devem ser esclarecidos com a professora, conforme o enunciado. Registrar respostas e refletir mudanças nos testes e documentos afetados.

## 11. Integração e entrega

Interface disponível para programas com e sem funções: `python main.py caminho/programa.coda`, com saída MEPA em `stdout`, ou `-o programa.mepa` para gravar UTF-8. `--verificar` executa somente as três análises. Diagnósticos usam `stderr`. Use o comando Python efetivamente localizado.

Executar a matriz em uma cópia contendo os módulos próprios, o PLY local e os casos necessários. Documentar ambiente, comandos e resultados observados. Não depender das práticas ou deste planejamento em tempo de execução.

A dupla deverá conseguir explicar construção da AST, precedência, resolução de nomes, regras de tipos, chamadas e recursão. A conclusão exige testes na máquina fornecida e revisão dos requisitos; preparação de documentação não equivale a etapa implementada. Submissão e publicação ficam fora deste planejamento.
