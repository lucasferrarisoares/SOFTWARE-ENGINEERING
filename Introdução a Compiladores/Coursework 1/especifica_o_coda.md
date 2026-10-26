# Disciplina: 11927 - Introdução à Compilação
**Profa. Valéria**
**Trabalho Prático**
**Implementação de um compilador para a linguagem Coda**

## Especificação geral

Esta atividade propõe a construção de um compilador para uma linguagem de programação experimental denominada Coda. A linguagem foi desenvolvida especificamente para este trabalho e possui um conjunto reduzido de construções, incluindo declaração de variáveis, funções, comandos de atribuição, estruturas de controle, operações de entrada e saída e expressões aritméticas, relacionais e lógicas.

O compilador deverá realizar as três etapas de análise: léxica, sintática e semântica. Após as análises, o compilador deverá gerar código para ser interpretado pela máquina MEPA (Kowaltowski, 1983). Uma implementação dessa máquina será disponibilizada juntamente com os arquivos de apoio ao trabalho.

O trabalho deverá ser desenvolvido em Python, utilizando a ferramenta de geração automática de scanners e parsers PLY¹.

É requisito deste trabalho que uma Árvore Sintática Abstrata (AST) seja produzida pelo parser. A construção de uma AST explícita, em vez da realização direta da tradução por meio das ações semânticas do parser, tem como objetivo proporcionar uma implementação mais organizada e modular. A AST servirá como representação intermediária do programa e será utilizada nas etapas posteriores de análise semântica e geração de código.

O compilador deverá ser executado a partir da linha de comando, recebendo como argumento o arquivo contendo o código-fonte em Coda. O código MEPA gerado poderá ser impresso na saída padrão ou redirecionado para um arquivo.

## Normas para desenvolvimento e entrega do trabalho

O trabalho deverá ser desenvolvido em duplas. A submissão do trabalho deverá ser feita exclusivamente pelo Classroom. O prazo final para a entrega será até às 23h59min do dia 29/11/2026.

## Avaliação do trabalho

O código-fonte do compilador será avaliado de acordo com sua organização, correção e atendimento aos requisitos especificados. Para isso, será utilizado um conjunto de programas escritos em Coda para verificar o funcionamento das diferentes etapas do compilador e os requisitos que foram cumpridos pela equipe.

A entrega de uma implementação funcional do compilador não determinará, por si só, a nota de cada integrante da equipe. A avaliação será complementada por uma apresentação, na qual os integrantes deverão demonstrar conhecimento sobre o compilador desenvolvido, explicar as principais decisões de implementação e responder a questões relacionadas ao funcionamento do código e aos conceitos envolvidos.

A nota será atribuída individualmente, considerando o desempenho de cada integrante durante a apresentação. Dessa forma, integrantes de uma mesma equipe poderão receber notas diferentes, de acordo com o domínio demonstrado sobre o trabalho desenvolvido. Durante a apresentação, poderão ser solicitadas explicações sobre trechos específicos do código, estruturas de dados utilizadas, regras de análise léxica, sintática ou semântica, construção e travessia da AST e geração de código MEPA.

O uso deliberado de IA generativa para produzir partes do trabalho, quando detectado, acarretará redução substancial da nota.

¹ https://ply.readthedocs.io/en/latest/index.html

---

## Características da linguagem

Coda é uma linguagem experimental de propósito geral, case-sensitive e com tipagem estática. A seguir são descritas as principais características da linguagem.

### Palavras reservadas

`program`, `fun`, `int`, `bool`, `if`, `else`, `void`, `while`, `return`, `read`, `print`, `true`, `false`

### Símbolos especiais

`(`, `)`, `{`, `->`, `}`, `=`, `==`, `!=`, `<`, `>`, `>=`, `<=`, `+`, `& &`, `/`, `!`

O símbolo `=` representa o operador de atribuição, enquanto `==` e `!=` representam, respectivamente, os operadores de igualdade e diferença.

Os operadores `+`, `-`, `*` e `/` são utilizados em expressões aritméticas. O operador `/` representa a divisão inteira, uma vez que Coda não suporta números reais.

Os operadores `<`, `<=`, `>`, `>=`, `==` e `!=` são utilizados em comparações, enquanto `& &`, `| |` e `!` representam, respectivamente, as operações lógicas de conjunção, disjunção e negação.

### Tipagem

Coda possui dois tipos primitivos, `int` e `bool`, além do tipo especial `void`:
*   `int`: representa valores numéricos inteiros;
*   `bool`: representa valores lógicos, representados pelas constantes `false` e `true`;
*   `void`: tipo especial que pode ser utilizado exclusivamente como tipo de retorno de funções.

Coda não permite a definição de novos tipos pelo programador.

### Funções

Coda possui uma única construção para definição de sub-rotinas, denominada função, introduzida pela palavra reservada `fun` e com um tipo de retorno.

As funções devem ser declaradas no escopo global do programa, não sendo permitido o aninhamento de funções. No programa, as declarações de variáveis devem preceder as declarações de funções e ambas devem aparecer antes dos comandos. No corpo de uma função, as declarações de variáveis devem aparecer antes dos comandos. As regras detalhadas de escopo e visibilidade serão apresentadas na especificação semântica.

### Declaração de variáveis

A declaração de uma variável não permite a atribuição de um valor inicial.

### Estruturas de controle

Coda possui duas estruturas de controle: o comando condicional `$if/el$ else` e o comando de repetição `while`.

## Interfaces de entrada e saída

Coda disponibiliza os comandos `read` e `print` para entrada e saída de dados. O comando `read` permite realizar a leitura de uma ou mais variáveis pela interface de entrada padrão, enquanto `print` permite exibir os valores de uma ou mais expressões na interface de saída padrão.

## Especificação léxica

### Identificadores
Identificadores são nomes definidos pelo programador e utilizados para representar entidades da linguagem, como programas, variáveis, funções e parâmetros. Um identificador deve iniciar com uma letra e pode ser seguido por qualquer combinação de letras, dígitos ou sublinhas (`_`).

Palavras reservadas da linguagem não podem ser utilizadas como identificadores.

### Números
Coda suporta apenas números inteiros, representados na base decimal por uma sequência de um ou mais dígitos entre 0 e 9.

O sinal de um número negativo não faz parte do elemento léxico correspondente ao número. Dessa forma, por exemplo, `-42` é reconhecido como dois símbolos distintos: o operador `-` e o número `42`. A interpretação de `-` como operador unário de negação aritmética será realizada durante a análise sintática.

### Valores booleanos
Os valores booleanos são representados pelas palavras reservadas `true` e `false`, correspondentes, respectivamente, aos valores lógicos verdadeiro e falso.

### Comentários e símbolos a serem ignorados
Coda permite comentários de uma única linha, iniciados pela sequência `//`. Todo o conteúdo compreendido entre `//` e o final da linha deve ser ignorado pelo analisador léxico.

Espaços em branco, tabulações e quebras de linha não possuem significado sintático e devem ser ignorados pelo analisador léxico. Entretanto, as quebras de linha devem ser contabilizadas para possibilitar a indicação da linha em que eventuais erros forem encontrados.

Caso seja encontrado um caractere ou uma sequência de caracteres que não possa ser reconhecida como um elemento léxico válido da linguagem, o analisador léxico deverá emitir uma mensagem de erro indicando, pelo menos, a linha em que o erro ocorreu.

## Especificação sintática

A sintaxe de Coda é definida pela gramática apresentada no Apêndice I desta especificação. A gramática utiliza a notação EBNF (Extended Backus-Naur Form), na qual são utilizadas, entre outras, as seguintes construções:
*   `{a}` para indicar que `a` pode ocorrer zero ou mais vezes;
*   `[a]` para indicar que `a` é opcional; e
*   `|` para indicar alternativas.

A notação EBNF utilizada no Apêndice I não corresponde diretamente ao formato das produções aceitas pelo PLY. Dessa forma, as construções EBNF deverão ser convertidas em produções equivalentes em BNF para a implementação do parser. Em particular, as construções de repetição e opção deverão ser transformadas em produções equivalentes. Se a transformação introduzir recursão nas produções, procure utilizar recursão à esquerda, pois ela é mais adequada para parsers LR.

### Construção da Árvore Sintática Abstrata
Além de verificar se o programa está de acordo com a gramática de Coda e emitir mensagens apropriadas para eventuais erros sintáticos, o parser deverá construir uma Árvore Sintática Abstrata (AST).

A AST deverá representar as construções relevantes do programa, abstraindo elementos utilizados apenas para sua organização sintática, como delimitadores, parênteses e pontos e vírgulas.

A organização concreta das classes ou estruturas utilizadas para representar os nós da AST é uma decisão de implementação da equipe. Entretanto, a árvore construída deverá conter as informações necessárias para permitir que as etapas posteriores de análise semântica e geração de código MEPA sejam realizadas por meio de travessias da AST.

## Especificação semântica

Após a construção da AST, deverá ser realizada a análise semântica do programa. Essa etapa tem como objetivo verificar se as construções sintaticamente válidas estão sendo utilizadas de acordo com as regras da linguagem Coda.

A análise semântica deverá utilizar uma tabela de símbolos para armazenar informações sobre os identificadores declarados no programa, como categoria, tipo, escopo, nível léxico e demais atributos necessários às etapas posteriores da compilação.

A seguir, são apresentadas as regras semânticas das principais construções da linguagem.

### Programa, escopos e visibilidade
O programa define o escopo global, correspondente ao nível léxico 0. Cada função define um escopo local, correspondente ao nível léxico 1. Blocos associados aos comandos `if`, `else` e `while` não definem novos escopos.

Coda utiliza escopo léxico. Um identificador declarado no escopo global é visível em todo o programa, exceto quando ocultado por uma declaração de mesmo nome no escopo local de uma função. Dessa forma, Coda permite o sombreamento (ocultação) de identificadores globais por identificadores declarados no escopo local de uma função.

### Declarações
As declarações de variáveis, funções e parâmetros deverão instalar na tabela de símbolos os identificadores correspondentes e as informações necessárias para as etapas posteriores da compilação.

Antes de instalar um novo identificador, deverá ser verificado se já existe uma declaração com o mesmo nome no escopo corrente. Caso exista, deverá ser emitido um erro semântico e a nova declaração não deverá substituir a declaração anterior.

### Funções e chamadas
Uma função possui um identificador, uma lista de parâmetros e um tipo de retorno, o qual pode ser `int`, `bool` ou `void`.

Uma função pode chamar a si mesma, permitindo recursão direta.

Para que uma chamada seja semanticamente válida, o identificador utilizado deverá corresponder a uma função declarada e visível no escopo da chamada.

O número de argumentos fornecidos na chamada deverá coincidir com o número de parâmetros da função. Além disso, o tipo de cada argumento deverá coincidir com o tipo do parâmetro correspondente, respeitando a mesma ordem.

Todos os parâmetros de Coda são passados por valor.

Uma função cujo tipo de retorno seja `void` não produz um valor. Portanto, uma chamada a uma função `void` pode ser utilizada como comando, mas não como parte de uma expressão.

O valor produzido por uma função dos tipos `int` ou `bool` pode ser utilizado em uma expressão. Uma chamada a uma função desses tipos também pode ser utilizada como comando, caso o valor retornado seja descartado.

### Retorno de funções
Funções dos tipos `int` e `bool` devem possuir pelo menos um comando `return` seguido de uma expressão, cujo tipo deverá coincidir com o tipo de retorno declarado para a função. Não é necessário verificar se todos os possíveis caminhos de execução levam a um `return`.

Funções do tipo `void` não possuem comando `return`.

### Comandos

**Atribuição:**
O identificador à esquerda do operador `=` deverá corresponder a uma variável declarada e visível no escopo atual.
A expressão à direita deve ser semanticamente válida e possuir o mesmo tipo da variável à esquerda.

**Condicional e repetição:**
A expressão utilizada como condição de um comando `if` ou `while` deverá ser semanticamente válida e possuir tipo `bool`.

**Entrada e saída:**
*   No comando `read`, cada argumento deverá corresponder a uma variável declarada e visível no escopo atual. As variáveis utilizadas como argumentos podem possuir os tipos `int` ou `bool`.
*   No comando `print`, cada argumento deverá ser uma expressão semanticamente válida e produzir um valor do tipo `int` ou `bool`.

**Expressões:**
As expressões deverão ser verificadas de acordo com os tipos de seus operandos e os operadores utilizados.
*   **Expressões aritméticas:** os operadores binários `+`, `-`, `*` e `/` exigem operandos do tipo `int` e produzem resultado do tipo `int`. O operador unário `-` também exige um operando do tipo `int` e produz resultado do tipo `int`.
*   **Expressões relacionais:** os operadores `<`, `<=`, `>` e `>=` exigem operandos do tipo `int` e produzem resultado do tipo `bool`.
*   **Expressões de igualdade e diferença:** os operadores `==` e `!=` exigem operandos do mesmo tipo. Os operandos podem ser dos tipos `int` ou `bool`, e o resultado da operação é do tipo `bool`.
*   **Expressões lógicas:** os operadores binários `&&` e `||` exigem operandos do tipo `bool` e produzem resultado do tipo `bool`. O operador unário `!` exige um operando do tipo `bool` e produz resultado do tipo `bool`.
*   **Constantes:** uma constante numérica possui tipo `int`. As constantes `true` e `false` possuem tipo `bool`.
*   **Uso de variável:** o identificador deverá corresponder a uma variável declarada e visível. O tipo resultante será o tipo declarado para a variável.
*   **Chamada de função:** seu tipo será o tipo de retorno da função chamada.

### Precedência e associatividade dos operadores
A gramática de expressões apresentada no Apêndice I é ambígua em relação à precedência e à associatividade dos operadores. Esses conflitos deverão ser resolvidos no parser por meio das regras de precedência e associatividade fornecidas pelo PLY.

Os operadores possuem os seguintes níveis de precedência, do menor para o maior:
*   `||`: associativo à esquerda;
*   `&&`: associativo à esquerda;
*   `==` e `!=`: não associativos;
*   `<`, `<=`, `>` e `>=`: não associativos;
*   `+` e `-`: associativos à esquerda;
*   `*` e `/`: associativos à esquerda;
*   `-` unário e `!`: associativos à direita.

Operadores não associativos não podem ser encadeados dentro do mesmo nível de precedência.

## Geração de código para a máquina MEPA
A especificação da máquina MEPA (KOWALTOWSKI, 1983) e seu código serão apresentados durante as aulas e, portanto, estarão nos slides de aula a serem disponibilizados.

## Casos omissos
Quaisquer casos relacionados ao desenvolvimento deste trabalho que não foram esclarecidos nesta especificação deverão ser arguidos diretamente com a professora.

## Referências
KOWALTOWSKI, T. Implementação de Linguagens de Programação. Rio de Janeiro: Guanabara Dois, 1983.

---

## Apêndice I
### Gramática EBNF da linguagem Coda

```ebnf
<programa> ::= 'program' <identificador> '{'
               <declaracoes-variaveis>
               <declaracoes-funcoes>
               <comandos>
               '}'

<declaracoes-funcoes> ::= { <declaracao-funcao> }

<declaracao-funcao> ::= 'fun' <identificador>
                        '('[ <lista-parametros>] ')' '->' <tipo-retorno> '{'
                        <declaracoes-variaveis>
                        <comandos>
                        '}'

<lista-parametros> ::= <parametro> { ',' <parametro> }

<parametro> ::= <tipo> <identificador>

<declaracoes-variaveis> ::= { <declaracao-variavel> }

<declaracao-variavel> ::= <tipo> <identificador> ';'

<tipo> ::= 'int' | 'bool'

<tipo-retorno> ::= 'int' | 'bool' | 'void'

<comandos> ::= { <comando> }

<comando> ::= <atribuicao>
            | <condicional>
            | <repeticao>
            | <retorno>
            | <leitura>
            | <escrita>
            | <chamada-comando>

<atribuicao> ::= <identificador> '=' <expressao> ';'

<condicional> ::= 'if' '('<expressao> ')' <bloco> [ 'else' <bloco> ]

<repeticao> ::= 'while' '(' <expressao> ')' <bloco>

<bloco> ::= '{' <comandos> '}'

<retorno> ::= 'return' <expressao> ';'

<leitura> ::= 'read' '('<lista-identificadores> ')' ';'

<lista-identificadores> ::= <identificador> { ',' <identificador> }

<escrita> ::= 'print' '(' <lista-expressoes> ')' ';'

<lista-expressoes> ::= <expressao> { ',' <expressao> }

<chamada-comando> ::= <chamada> ';'

<chamada> ::= <identificador> '(' [ <lista-expressoes> ] ')'

<expressao> ::= <expressao> <operador-binario> <expressao>
              | <operador-unario> <expressao>
              | <numero>
              | <booleano>
              | <identificador>
              | <chamada>
              | '(' <expressao> ')'

<operador-binario> ::= '+' | '-' | '*' | '/' | '<' | '<=' | '==' | '!=' | '>' | '>=' | '&&' | '||'

<operador-unario> ::= '-' | '!'

<numero> ::= <digito> { <digito> }

<digito> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

<booleano> ::= 'true' | 'false'

<identificador> ::= <letra> { <letra> | <digito> | "_" }

<letra> ::= 'a' | 'b' | ... | 'z' | 'A' | 'B' | ... | 'Z'
```