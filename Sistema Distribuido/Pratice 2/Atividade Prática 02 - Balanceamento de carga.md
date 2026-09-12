## UNIVERSIDADE ESTADUAL DE MARINGÁ DEPARTAMENTO DE INFORMÁTICA CENTRO DE TECNOLOGIA

Disciplina 9929- Sistemas Distribuídos (Ano letivo de 2026, 2º Semestre)

Bacharelado em Engenharia de Software

[Alisson Renan Svaigen](mailto:arsvaigen@uem.br)

Professor Dr.

## Atividade Prática 02: Balanceamento de carga

Objetivo da aula prática: aplicar o conhecimento teórico obtido no Módulo 03 (Balanceamento de Carga) de maneira prática, por meio da implementação de diferentes algoritmos de balanceamento de carga.

Linguagem de programação a ser utilizada: Python 3.x

SO a ser utilizado: qualquer distribuição com um ambiente Python instalado.

## Algoritmos a serem implementados

Nessa atividade prática, a proposta é implementar 3 diferentes algoritmos de

balanceamento de carga, especificamente relacionados à arquiteturas centralizadas de balanceamento de tráfego:

- Randômico (Rand): Cada requisição é enviada aleatoriamente para um servidor que está disponível.

- Round-Robin (RR): As requisições são encaminhadas de forma sequencial e cíclica para cada servidor disponível.

- Least Connections (LC): Cada nova requisição é enviada para o servidor com o menor número de conexões ativas no momento. Para tanto, o balanceador precisa manter uma contagem de conexões ativas para cada servidor. Para este exercício, considere que cada nova requisição representa uma nova conexão criada. O servidor, ao concluir o processamento de uma requisição, deve informar ao balanceador que concluiu uma requisição. Caso haja empate na decisão de balanceamento, faça um sorteio para decidir qual servidor receberá.

## Cenário de operação

Os algoritmos a serem implementados devem operar num balanceador de carga de

um sistema distribuído que opera em um nó centralizado. O balanceador recebe as requisições e as distribui para três servidores: A, B e C. A comunicação entre balanceador e servidores é realizada por meio de sockets UDP.


Cada servidor, por sua vez, ao receber uma requisição, deverá considerar um certo

intervalo de tempo para realizar o seu “processamento”, visto que esta atividade baseia-se numa simulação experimental, seguindo as informações presentes na própria requisição (será descrito na próxima seção).

Considerando a implementação a ser realizada, as requisições serão “submetidas”

para o balanceador por meio de um arquivo de entrada (discutido na próxima seção), que simulará a interação dos clientes com o sistema distribuído. Cada requisição do arquivo de entrada deve ser tratada pelo balanceador em intervalos de 10 milissegundos.

A arquitetura geral do sistema é similar a vista em sala de aula, na qual pode-se

abstrair o cenário para o apresentado na figura abaixo:

## Formato do arquivo de entrada

Por padrão, o balanceador de carga deve carregar um arquivo de entrada que possui

a descrição de todas as requisições que serão distribuídas para os três servidores. Cada linha do arquivo de entrada é composto pelas seguintes informações:

ID requisição;tempo de execução (em milissegundos inteiros)

Um exemplo de arquivo de entrada é apresentado a seguir:

r0;200

r1;110

r2;150

r3;500


## Saída esperada

A cada requisição que o balanceador trata, após o envio para o servidor escolhido, o

balanceador deve preencher um arquivo de log com o número de requisições sendo tratadas em cada servidor. Cada linha do arquivo de log deve ter o seguinte formato:

```
#req. servidor A; #req. servidor B; #req. servidor C
```

Um exemplo de saída é apresentado a seguir, considerando o algoritmo RR:

```
1;0;0
1;1;0
1;1;1
2;1;1
1;1;1 /*nesse momento o server A finalizou uma requisição*/
...
```

## ENTREGAS NO GOOGLE CLASSROOM (Pontuação extra)

- O conjunto de arquivos .py implementados;

- Um arquivo .py que contenha uma implementação para gerar uma análise gráfica considerando 3 arquivos de log: um para cada algoritmo implementado, a fim de comparar os algoritmos implementados para uma mesma entrada.

- Data final da entrega: 23h59min do dia 15 de Setembro de 2026, exclusivamente via Google Classroom
