# Comparação de estilo: Prática 4 e Coda

Análise e refatoração realizadas em **11/11/2026**, usando os arquivos Python da pasta `OneDrive/Área de Trabalho/Pratica4`. A referência implementa partes do compilador RoboDIN. O objetivo foi aproximar a organização do código da Coda, preservando o comportamento existente.

## O padrão encontrado

A prática separa lexer, parser, AST, definições compartilhadas, semântica e execução em módulos. Usa classes PLY, nomes em português, `dataclass` para os nós, argumentos nomeados ao construir a árvore e comentários curtos para identificar os grupos de regras. O `Visitador` escolhe o método `visita_<NomeDoNo>` por meio de `getattr`; a semântica reserva um método para cada construção.

O arquivo `robo_semantico.py` é um esqueleto com métodos ainda contendo `pass`. Além disso, `robo.py` importa `robo_semantico_gabarito`, ausente da pasta. Portanto, esses arquivos permitem comparar a estrutura proposta, mas não fornecem uma implementação semântica completa para usar como referência de funcionamento. A pasta também não contém um gerador MEPA.

## Comparação e alterações

| Parte | Prática 4 | Coda antes | Coda após a refatoração |
|---|---|---|---|
| Lexer | Classe com `module=self`, regras `t_...`, comentários por grupo e parâmetro `t` | Mesma estrutura PLY, outra disposição dos métodos | Construtor no início, grupos comentados, parâmetro `t` e entrada/token no final |
| Parser | Métodos `p_...` constroem nós usando argumentos nomeados | Nós construídos principalmente com argumentos posicionais | Campos explícitos, como `nome=`, `expressao=` e `linha=` |
| AST | Classes base agrupadas, `dataclass`, `linha` nomeada e `Literal` para operadores | Já usava `dataclass` e `linha`, com bases distribuídas no arquivo | Bases agrupadas, comentários por família de nós e operadores anotados com `Literal` |
| Travessia | `Visitador` em `robo_defs.py` | Seleção do nó por sequências de `isinstance` na semântica e no gerador | `Visitador` compartilhado em `definicoes.py` |
| Semântica | `AnalisadorSemantico(Visitador)` com métodos `visita_...` | Classe interna com `_expressao` e `_comandos` concentrando as regras | `AnalisadorSemantico(Visitador)` com uma visita por construção analisada |
| Geração | Não consta da referência | Classe interna com seleção de expressões e comandos por `isinstance` | `GeradorMEPA(Visitador)` aplica o mesmo padrão às instruções MEPA |

As funções públicas `analisar(programa)` e `gerar(programa, tabelas)` continuam disponíveis. O visitador organiza a seleção dos métodos; as verificações de tipos e as instruções emitidas permanecem nas respectivas fases. A análise de fluxo de retorno continua em sua função específica.

## Diferenças mantidas e seus motivos

- **Linguagem:** Coda mantém seus identificadores, inteiros, booleanos, declarações, funções, escopos e operadores. Não incorpora números reais, atribuição `<-` ou comandos de movimento de RoboDIN.
- **Tokens e precedência:** os tokens continuam nomeados. A precedência continua declarada em `precedence`, como exige a especificação da Coda, em vez da separação `expressao/termo/fator` usada pela prática.
- **Listas do parser:** continuam usando recursão à esquerda e `append`, preservando a ordem sem copiar toda a lista a cada redução.
- **Símbolos:** continuam em dicionários com categoria, tipo, nível, escopo e informações das funções. O `Simbolo` de RoboDIN tem apenas `nome` e `atribuida`; transplantá-lo não atenderia às informações necessárias à Coda. A AST continua sem receber vínculos mutáveis com os símbolos.
- **Erros:** as fases continuam interrompendo no primeiro erro com `ValueError`; a CLI continua emitindo o diagnóstico em `stderr`. A recuperação com `tem_erro` e produções `error` da prática não foi incorporada.
- **Interface:** a Coda continua recebendo o caminho do arquivo e oferecendo `--verificar` e `-o`. A prática usa entrada padrão e mensagens de sucesso, enquanto a saída padrão da Coda deve servir ao código MEPA.
- **Retornos:** foi preservada a convenção já documentada que rejeita funções com possibilidade de terminar sem retorno. Ela é mais restritiva que o enunciado original e não foi introduzida nesta refatoração.

## Verificação

Os **75 testes existentes passaram antes e depois**, sem alteração dos testes. A suíte cobre as análises, a CLI e a execução na MEPA, incluindo escopos, recursão, ordem de avaliação e equilíbrio da pilha.

Também foi feita uma comparação automática dos **29 arquivos `.coda`** de `testes/`: tokens, estrutura da AST, tabelas de símbolos, endereços/rótulos, instruções MEPA e diagnósticos foram idênticos aos registrados antes da refatoração, nas etapas alcançadas por cada arquivo. Essa comparação verifica os exemplos disponíveis; não substitui uma prova formal para todos os programas possíveis.
