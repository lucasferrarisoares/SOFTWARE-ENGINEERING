# Guia de implementação da Coda

Base: especificação da disciplina e materiais locais das práticas. Revisão: 27/10/2026.

Este documento orienta a implementação pela dupla. Os módulos descritos são uma proposta; o compilador ainda não foi implementado nem testado. A especificação continua sendo a fonte dos requisitos. As escolhas de organização abaixo procuram atender ao feedback recebido em Sistemas Distribuídos: código funcional, mas complexo demais para o problema solicitado.

**Direção escolhida:** módulos por etapa, classes simples para os nós da AST, funções diretas para percorrê-la e geração de MEPA a partir da AST validada. Cada estrutura deve atender a um requisito atual ou tornar uma parte concreta do código mais clara.

## 1. Material disponível e como aproveitá-lo

Os caminhos desta tabela são relativos a este guia. `referencias/` é material local ignorado pelo Git; seus links não estarão disponíveis em um clone que não contenha essa pasta.

| Material | O que fornece | Uso na Coda |
|---|---|---|
| [Especificação Coda](especifica_o_coda.md) | Requisitos léxicos, sintáticos, semânticos, AST e destino MEPA | Fonte principal; prevalece sobre os exemplos de outras linguagens |
| [Prática 1](<referencias/Pratica 1>) | Dois programas RoboDIN e a biblioteca PLY 3.11 | Modelo de entradas válidas/inválidas e cópia da biblioteca usada nas práticas; essa pasta não contém o lexer da atividade |
| [posfixo.py](<referencias/Pratica 2/posfixo.py>) e [posfixo1.py](<referencias/Pratica 2/posfixo1.py>) | Tradução de expressões para texto pós-fixo; a segunda versão acrescenta `b` | Entender produções, `p[0]` e propagação de resultados |
| [posfixo2.py](<referencias/Pratica 2/posfixo2.py>) | Operadores `and` e `or`, organizados em níveis da gramática | Estudar precedência; adaptar para os operadores e a tabela do PLY exigidos pela Coda |
| [posfixo3.py](<referencias/Pratica 2/posfixo3.py>) | Verificação de tipos nas ações do parser, com `a: int` e `b: bool` | Referência conceitual de tipos; na Coda, verificar a AST depois do parser |
| [robo_lexer.py](<referencias/Pratica 3/robo_lexer.py>) | Reservadas, tokens, comentários, contagem de linhas e estado de erro | Principal referência para organizar o lexer, substituindo as regras da RoboDIN |
| [robo_ast.py](<referencias/Pratica 3/robo_ast.py>) | Classes de dados, nós de comando/expressão e atributo `linha` | Principal referência de representação da AST |
| [robo_parser.py](<referencias/Pratica 3/robo_parser.py>) | Produções e listas com recursão à esquerda | Esqueleto didático: as ações principais ainda têm `pass` e não constroem a AST |
| [robo_ast_utils.py](<referencias/Pratica 3/robo_ast_utils.py>) | Impressão recursiva da árvore | Auxílio opcional de desenvolvimento |
| [Documentação local do PLY](ply-master/doc/ply.md) | AST, precedência, associatividade e localização dos tokens | Consulta técnica para as regras do parser |

O comentário de `posfixo3.py`, linhas 37–38, avisa expressamente que a verificação semântica do trabalho não será feita no parser. Ele concorda com a especificação Coda: primeiro construir a AST, depois analisá-la.

Não foi encontrada MEPA nos arquivos adicionados. Os tradutores pós-fixos produzem texto; não implementam a máquina que executará o resultado do compilador. O arquivo `entradaOk`, mencionado no PDF de pós-fixo discutido anteriormente, também não veio no material. Isso não impede usar os exemplos do README da prática. `parsetab.py`, `parser.out` e `__pycache__` são arquivos gerados, não códigos-base faltando.

## 2. Arquitetura proporcional ao trabalho

Fluxo obrigatório: arquivo Coda → lexer PLY → parser PLY → AST → análise semântica → geração MEPA.

A proposta inicial tem seis módulos próprios. Classes pequenas para encapsular lexer ou parser, como nas práticas, são aceitáveis; não é necessário transformar toda etapa em uma hierarquia de classes.

| Módulo proposto | Responsabilidade |
|---|---|
| `main.py` | Receber o caminho do arquivo, ler a entrada, coordenar as etapas e apresentar o resultado ou erro |
| `lexer.py` | Reconhecer tokens e guardar a linha de cada um |
| `parser.py` | Reconhecer a gramática e construir a AST |
| `nos_ast.py` | Declarar os nós e seus campos |
| `semantico.py` | Manter a tabela de símbolos, resolver nomes e verificar tipos, chamadas e retornos |
| `gerador_mepa.py` | Percorrer a AST validada e emitir instruções compatíveis com a MEPA fornecida |

A tabela de símbolos pode começar em `semantico.py`. Só vale separá-la se isso melhorar a leitura. O número de arquivos não é uma meta de avaliação.

**Limites escolhidos para a implementação:**

- Usar classes de dados e funções recursivas, sem fábricas, registradores, visitantes genéricos ou hierarquias profundas.
- Representar os dois níveis de escopo que Coda possui, sem infraestrutura para aninhamento arbitrário.
- Gerar MEPA diretamente da AST validada, sem uma representação intermediária adicional.
- Implementar apenas a linguagem especificada, sem otimizações, interface gráfica, servidor ou suporte a outros destinos.
- Começar com interrupção no primeiro erro. Recuperação para acumular vários erros é opcional.
- Manter verificações obrigatórias, mensagens claras e testes por requisito. Simplificar a estrutura não reduz a cobertura da linguagem.

## 3. Dependência PLY e execução

Há duas versões locais: `referencias/Pratica 1/ply` declara **3.11** e `ply-master/src/ply` declara **2022.10.27**. Não devem ser misturadas. Há diferenças de API: por exemplo, as opções `write_tables` e `tabmodule` de `yacc()` existem na cópia 3.11, mas não na assinatura da cópia de `ply-master`.

**Decisão sugerida:** começar com a cópia 3.11 fornecida na prática, para acompanhar os exemplos. Na implementação, colocar uma única pasta `ply/`, com seus avisos originais, ao lado dos módulos do compilador, fora de `referencias/`. A existência de `ply-master/src/ply` não torna automaticamente `import ply` disponível. A entrega deve funcionar sem a pasta ignorada e documentar as versões de Python e PLY efetivamente usadas.

Se forem mantidas as `dataclasses` de RoboDIN, conferir o suporte do Python escolhido aos recursos usados, especialmente `field(kw_only=True)`, antes de iniciar a adaptação.

A interface final prevista é `python main.py programa.coda`, com possibilidade de redirecionar a saída para um arquivo MEPA. É uma interface a implementar, não um comando disponível hoje. Usar `stdout` apenas para o código gerado e `stderr` para diagnósticos; terminar com código diferente de zero em caso de erro. A impressão da AST e mensagens como “análise concluída” não devem acompanhar a saída normal.

## 4. Lexer: adaptar as regras da RoboDIN

| Aspecto | Base das práticas | Regra para Coda |
|---|---|---|
| Identificador | RoboDIN exige inicial minúscula e não aceita `_` | `[a-zA-Z][a-zA-Z0-9_]*`, conforme as letras do Apêndice I |
| Número | RoboDIN converte decimais para `float` | `[0-9]+`, convertido para `int`; sem parte decimal |
| Número negativo | Não está coberto pelos exemplos pós-fixos | Reconhecer `-` e o número separadamente; o parser constrói o operador unário |
| Reservadas | Vocabulário do robô | `program`, `fun`, `int`, `bool`, `if`, `else`, `void`, `while`, `return`, `read`, `print`, `true`, `false` |
| Atribuição | `<-` | `=`; distinguir de `==` |
| Operadores lógicos | `and` e `or` nas práticas pós-fixas | Usar os símbolos de Coda: conjunção, disjunção e `!` |
| Comentários | RoboDIN já reconhece `//` até o fim da linha | Aproveitar a estratégia |
| Linhas | Pós-fixo ignora `\n` sem contabilizar | Contar quebras, como em `robo_lexer.py`, e guardar a linha dos tokens |

Definir também chaves, parênteses, vírgula, ponto e vírgula, `->` e todos os operadores da gramática. Usar regras apropriadas para os operadores compostos: `==`, `!=`, `<=`, `>=`, `&&` e `||` não podem ser separados em tokens menores. Comentários precisam ser distinguidos da divisão.

Consultar o dicionário de reservadas na regra de identificadores, como em RoboDIN. Coda diferencia maiúsculas de minúsculas: `program` é reservada e `Program` pode ser identificador.

A lista inicial de símbolos do enunciado tem omissões e espaços em `& &`/`| |`; o Apêndice I e a seção de precedência usam `&&`/`||`. Seguir essas formas na proposta e levar a inconsistência à professora se houver dúvida.

Um caso como `1tempo` pode produzir número seguido de identificador; não se deve presumir que todo identificador escrito incorretamente será um único erro léxico. O programa completo ainda deve ser rejeitado na etapa apropriada. Ao detectar um erro léxico, impedir a geração de MEPA mesmo que o analisador consiga continuar lendo tokens.

## 5. AST e parser

A base de RoboDIN é suficiente como estilo: uma classe `No` com linha, categorias simples de expressão/comando e campos nomeados. A tabela abaixo sugere as informações necessárias; nomes e agrupamentos são decisões da dupla.

| Construção | Informações a preservar |
|---|---|
| Programa | Nome, variáveis globais, funções e comandos principais |
| Declaração de variável / parâmetro | Nome, tipo e linha; preservar a ordem dos parâmetros |
| Função | Nome, parâmetros, tipo de retorno, variáveis locais e comandos |
| Atribuição | Identificador de destino e expressão |
| Condicional | Condição, lista de comandos do ramo verdadeiro e ramo alternativo opcional |
| Repetição | Condição e lista de comandos do corpo |
| Retorno | Expressão e linha |
| Leitura / escrita | Lista de identificadores / lista de expressões |
| Chamada | Nome e argumentos; distinguir uso como expressão de uso como comando |
| Expressão binária / unária | Operador e operandos |
| Identificador / literal | Nome / valor inteiro ou booleano |

Representar os blocos por listas de comandos é suficiente. Delimitadores e parênteses não precisam virar nós. Uma chamada como comando pode envolver o mesmo nó de chamada usado em expressões, com uma indicação clara de que seu resultado será descartado.

Trocar `Num.valor: float` por inteiro e representar booleanos explicitamente. Nas verificações, usar os tipos da linguagem, sem depender de comparações entre valores Python para distinguir `int` e `bool`.

**Conversão da gramática:**

- Transformar repetições EBNF em listas com produção vazia e recursão à esquerda; transformar opcionais em alternativas com e sem o elemento.
- Permitir listas vazias onde o enunciado permite: declarações, comandos, parâmetros e argumentos de chamada.
- Manter `read` e `print` com pelo menos um argumento.
- Preservar a ordem: variáveis globais → funções → comandos; dentro de função, variáveis locais → comandos.
- Blocos de `if`/`else`/`while` contêm apenas comandos; funções não podem ser aninhadas.
- Declarações de variável não incluem inicialização.

Nas ações do parser, construir o nó em `p[0]` ou propagar um nó já construído. Guardar a linha a partir de um terminal relevante com `p.lineno(i)`; para nós propagados, preservar sua própria linha. Não presumir que um não terminal tenha localização automática. Não calcular expressões, verificar declarações nem emitir MEPA nessas ações.

O parser RoboDIN contém `pass` nas ações principais e pode imprimir “AST construída” mesmo que o resultado seja `None`. Para concluir esta etapa, uma entrada válida precisa retornar uma raiz com todos os nós esperados, não apenas terminar sem erro de sintaxe.

**Precedência de Coda, da menor para a maior:**

1. `||`: à esquerda.
2. `&&`: à esquerda.
3. `==` e `!=`: não associativos.
4. `<`, `<=`, `>` e `>=`: não associativos.
5. `+` e `-`: à esquerda.
6. `*` e `/`: à esquerda.
7. `-` unário e `!`: à direita.

Usar a tabela `precedence` do PLY, como exige o enunciado, e `%prec UMINUS` para diferenciar o menos unário. Os exemplos de RoboDIN e pós-fixo embutem precedência em níveis como expressão/termo/fator; servem para estudar o conceito, mas a Coda exige o mecanismo indicado acima.

Não transcrever literalmente a produção `expressao : expressao operador_binario expressao` para uma única regra PLY esperando que a tabela funcione. A precedência vem do terminal mais à direita da produção. Explicitar alternativas com os tokens de cada operador, por exemplo `expressao PLUS expressao`, permite atribuir a precedência correta. Comparações e igualdades precisam de dois grupos `nonassoc` distintos.

## 6. Análise semântica depois da AST

Usar um dicionário global e um dicionário local por função. Procurar primeiro no local e depois no global. Guardar categoria, tipo, escopo/nível e, para funções, assinatura. Endereços e rótulos podem ser acrescentados quando a convenção MEPA estiver definida. Parâmetros pertencem ao escopo local e funcionam como variáveis passadas por valor.

**Pilha de escopos opcional:** uma lista pode guardar referências aos dicionários ativos: `[global]` no programa e `[global, local_da_funcao]` ao analisar uma função. A consulta percorre a lista do topo para a base. Ao terminar a função, retirar apenas a referência da pilha e preservar seu dicionário em `locais[nome_da_funcao]`, para uso posterior pelo gerador. `if`, `else` e `while` não empilham novos escopos. Como existem apenas dois níveis, consultar diretamente o local e o global continua sendo uma alternativa suficiente.

Essa pilha pertence ao compilador e organiza a visibilidade dos nomes. A pilha de execução da MEPA guarda valores e informações das ativações durante as chamadas; recursão não exige reconstruir a tabela local da função a cada chamada.

Uma organização simples da análise:

1. Cadastrar variáveis globais e assinaturas das funções, rejeitando duplicidades no mesmo escopo sem substituir a declaração anterior.
2. Para cada função, cadastrar parâmetros e variáveis locais, depois verificar seu corpo.
3. Verificar os comandos principais no escopo global.

Pré-cadastrar assinaturas é a leitura adotada para a regra de que identificadores globais são visíveis em todo o programa. Isso permite resolver chamadas sem depender da ordem de análise dos corpos e atende à recursão direta exigida. Coletar declarações/assinaturas e depois verificar os corpos são subetapas complementares; isso não significa executar duas análises semânticas completas.

O sombreamento deve valer também para a categoria do nome: se uma variável local oculta uma função global, uma chamada com esse nome deve falhar. A busca não deve ignorar o símbolo local para encontrar uma função no global. `if`, `else` e `while` não criam novos escopos.

| Construção | Verificação obrigatória |
|---|---|
| Uso de nome | Declarado, visível e com categoria adequada |
| Atribuição | Destino é variável; expressão tem o mesmo tipo |
| Operadores aritméticos e menos unário | Operand(os) `int`; resultado `int` |
| Comparações de ordem | Dois `int`; resultado `bool` |
| Igualdade/diferença | Dois operandos do mesmo tipo, `int` ou `bool`; resultado `bool` |
| Operadores lógicos | Operand(os) `bool`; resultado `bool` |
| `if` e `while` | Condição `bool` |
| `read` | Cada argumento é variável visível `int` ou `bool` |
| `print` | Cada expressão produz `int` ou `bool` |
| Chamada | Nome resolve para função; quantidade, ordem e tipos dos argumentos coincidem |
| Chamada `void` | Permitida como comando; proibida como valor de expressão |
| Chamada `int`/`bool` como comando | Permitida; o gerador deverá descartar o resultado |
| `return` | Contexto de função com retorno `int`/`bool`; expressão com o tipo declarado |
| Função `int`/`bool` | Pelo menos um `return` com expressão adequada; verificar também os demais retornos existentes |
| Função `void` | Não possui comando `return` |

Uma função recursiva de análise de expressão pode retornar seu tipo. A análise de comandos usa essa informação e o contexto da função atual. É suficiente devolver as tabelas de símbolos ao gerador, com os mesmos escopos; não é obrigatório criar uma segunda árvore tipada ou um sistema genérico de passes.

**Construção única por compilação:** `analisar(programa)` constrói as tabelas durante a análise semântica e as devolve após a validação. Uma nova compilação começa com suas próprias tabelas. `gerar(programa, tabelas)` recebe as tabelas da compilação atual e consulta os símbolos existentes. Não deve recadastrar declarações, reconstruir tabelas nem chamar novamente a análise semântica. Pode acrescentar os endereços e rótulos necessários à geração. Consultar tipo, categoria e assinatura para escolher instruções não equivale a repetir as validações semânticas.

A análise semântica percorre a AST para verificar o programa, e o gerador faz outra travessia para emitir instruções. Evitar repetir a análise semântica significa reutilizar seus resultados na geração; não significa eliminar a travessia semântica da AST nem exigir uma única passagem por toda a estrutura.

**Não acrescentar análise de retorno em todos os caminhos:** o enunciado dispensa essa verificação. Também não exigir inicialização de toda variável antes do uso, nem introduzir coerções entre `int` e `bool`; essas regras não foram pedidas.

## 7. Geração MEPA: parte dependente do material faltante

Ainda faltam a implementação da máquina e os slides com sua especificação, prometidos nas seções “Especificação geral” e “Geração de código para a máquina MEPA”. As práticas recebidas não suprem essa dependência. Não é necessário desenvolver uma máquina virtual própria.

É possível planejar o gerador com uma lista de instruções e um contador de rótulos. Para defini-lo corretamente, obter primeiro:

- Formato do arquivo aceito, instruções, operandos e sintaxe de rótulos.
- Endereçamento de globais, parâmetros e variáveis locais.
- Convenção de chamada, armazenamento do retorno e limpeza da pilha.
- Representação e entrada/saída de booleanos; comportamento da divisão inteira.

Depois disso, implementar progressivamente: literais e operações → variáveis e entrada/saída → desvios e laços → funções, parâmetros e recursão. A geração de uma expressão deve produzir seu valor; comandos devem manter a pilha equilibrada, com os ajustes previstos na convenção da máquina. Uma chamada usada como comando não pode acumular resultados na pilha.

Ao percorrer os corpos das funções para gerar código, selecionar as tabelas locais preservadas pela análise semântica e consultar o global quando necessário. Essa seleção não recria escopos nem repete as verificações de tipos e declarações.

Funções recursivas exigem espaço próprio para cada ativação; não basta reservar uma única área fixa para todas as execuções de uma função. O fluxo inicial precisa chegar aos comandos principais sem executar corpos de funções por acidente. Um `return` deve encerrar a execução da função e respeitar sua limpeza de pilha.

Não fixar neste guia nomes de instruções, offsets de parâmetros ou formato de prólogo sem a versão usada pela disciplina. A conclusão da etapa exige executar o código gerado nessa MEPA e conferir o comportamento.

## 8. Sequência de implementação e critérios de avanço

| Etapa | Entrega verificável | Complexidade estimada |
|---|---|---|
| 1. Ambiente e entrada | PLY importável fora de `referencias/`; leitura de arquivo por argumento | Baixa |
| 2. Lexer | Tokens, valores e linhas corretos; erros léxicos detectados | Baixa–média |
| 3. Parser e AST | Programa completo representado; precedência e listas verificadas | Média |
| 4. Semântica | Regras da seção 6 cobertas por casos válidos e inválidos | Média–alta |
| 5. MEPA básica | Expressões, variáveis, entrada/saída e controle executados na máquina fornecida | Média–alta |
| 6. Funções MEPA | Parâmetros por valor, retornos, descarte de resultado e recursão funcionando | Alta |
| 7. Integração | Execução pela CLI, saída limpa e demonstração compreendida pela dupla | Média |

Esses níveis estimam esforço de implementação, não desempenho assintótico. A parte difícil continua sendo funções e convenções de execução; a estrutura simples reduz trabalho auxiliar.

Enquanto a MEPA não chega, avançar até a análise semântica e manter seus testes independentes. Não classificar o compilador como completo apenas porque essas etapas funcionam.

Para dividir o trabalho, uma pessoa pode iniciar lexer/parser e a outra AST/casos semânticos. Combinar os campos dos nós antes de trabalhar em paralelo. Revisar juntos a integração e a geração de funções, pois a avaliação individual exige compreender o conjunto.

## 9. Casos de teste suficientes para orientar a implementação

Criar pequenos arquivos `.coda` organizados em válidos e inválidos, com a saída ou categoria de erro esperada. Os trechos abaixo precisam ser inseridos em programas completos e com as declarações indicadas. Começar com execução simples; um executor de testes pequeno só se justifica quando a repetição manual atrapalhar.

| Grupo | Casos a verificar | Resultado esperado |
|---|---|---|
| Léxico | Nomes como `X`, `valor_1`; reservadas; comentário seguido de erro | Identificadores corretos e linha exata no diagnóstico |
| Léxico inválido | `_x`, `10.5`, caractere `@` | Rejeição sem geração de código |
| Tokens compostos | `=`, `==`, `!=`, `<=`, `>=`, `->`, `&&`, `\|\|` | Reconhecimento sem divisão incorreta |
| Estrutura mínima | `program P { }` | AST de programa com listas vazias |
| Declarações | Inicialização na declaração; variável após comandos; declaração dentro de `if`; função aninhada | Erro sintático |
| Listas | Função e chamada sem argumentos; vários argumentos em `read`/`print`; `read()` e `print()` | Aceitar os casos permitidos e rejeitar as listas vazias de leitura/escrita |
| Precedência | `2 + 3 * 4`, `(2 + 3) * 4`, `10 - 3 - 2`, `-2 * 3`, `-2 + 3`, `!!true` | AST correta; posteriormente resultados 14, 20, 5, -6, 1 e verdadeiro; conferir também o agrupamento do menos unário na árvore |
| Precedência lógica | `true \|\| false && false`; `!true && false`; `1 + 2 < 4 == true` | Agrupar conjunção antes de disjunção, negação antes de conjunção e soma antes de comparação; resultados verdadeiro, falso e verdadeiro |
| Não associatividade | `1 < 2 < 3`; `true == false == true` | Erro sintático |
| Sintaxe inválida | Falta de `;`, chave ausente, fim de arquivo inesperado, `return;` | Rejeição com mensagem compreensível |
| Símbolos | Nome não declarado; declaração duplicada; parâmetro e variável local com mesmo nome | Erro semântico; declaração anterior preservada |
| Sombreamento | Variável local com nome de global; variável local ocultando função chamada | Usar o símbolo local; rejeitar a chamada à variável |
| Tipos | Atribuir booleano a inteiro; `true + 1`; `!1`; `1 && true`; igualdade entre `int` e `bool`; condição inteira | Erro semântico |
| Entrada/saída | Ler variáveis `int`/`bool`; imprimir expressões; ler função ou nome ausente | Aceitar apenas usos válidos |
| Chamadas | Quantidade ou tipo incorreto; função `void` em expressão; chamada sem argumentos | Verificar assinatura e contexto |
| Retornos | Tipo errado; ausência de retorno em função não `void`; retorno em `void` ou no principal | Erro semântico |
| Retorno condicional | Função `int` com `return` adequado somente dentro de um `if` | Aceitar semanticamente; não exigir retorno em todos os caminhos |
| Controle | `if` com/sem `else`, `while`, estruturas aninhadas | Seleção dos ramos e término corretos na MEPA |
| Funções | Recursão direta com caso-base; parâmetros por valor; acesso a globais e locais | Resultados corretos e ativações independentes |
| Pilha | Chamada `int`/`bool` como comando dentro de laço; chamadas usadas em expressões | Descarte de resultados e equilíbrio da pilha |
| Interface | Arquivo ausente; erro em cada etapa; redirecionamento de programa válido | Erros em `stderr`; `stdout` sem mensagens extras e sem MEPA parcial em caso de erro |

Uma condição como `1 < 2 == true` combina níveis distintos de precedência e pode ser válida. Não rejeitar toda expressão com mais de uma comparação: aplicar os grupos de não associatividade exatamente como especificados.

## 10. Pontos a confirmar com a professora

| Ponto | Por que importa |
|---|---|
| Implementação e slides MEPA | São necessários para compatibilidade e testes finais |
| Curto-circuito de `&&`/`\|\|` | O enunciado define tipos, mas não a estratégia de avaliação; chamadas podem ter efeitos observáveis |
| Formato de booleanos em `read`/`print` | Não está definido se a interface usa números ou palavras |
| Divisão inteira com valores negativos | Confirmar truncamento/arredondamento usado pela máquina |
| Caminho que termina função não `void` sem executar `return` | É permitido pela verificação exigida, mas o comportamento em execução não foi definido |

Não transformar essas dúvidas em novas restrições da linguagem. Registrar a orientação recebida e atualizar somente a parte afetada do guia.

## 11. Critérios de conclusão

- O compilador usa Python e PLY, recebe arquivo pela linha de comando e constrói uma AST explícita.
- Todas as construções de Coda estão representadas e as regras semânticas foram verificadas depois do parser.
- A geração só ocorre após as análises válidas, sem mistura de diagnósticos com MEPA.
- Os testes cobrem erros e programas válidos, incluindo recursão, sombreamento e descarte de retorno.
- O código gerado foi executado na MEPA da disciplina.
- A execução funciona sem `referencias/` e a dupla consegue explicar cada módulo, nó e regra implementada.

O guia define um caminho de implementação. Até a chegada da MEPA, a verificação de execução final permanece pendente.
