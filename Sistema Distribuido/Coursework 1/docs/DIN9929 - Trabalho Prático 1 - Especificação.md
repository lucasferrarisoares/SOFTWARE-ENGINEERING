## UNIVERSIDADE ESTADUAL DE MARINGÁ DEPARTAMENTO DE INFORMÁTICA CENTRO DE TECNOLOGIA

## Disciplina: DIN9929 - Sistemas Distribuídos Bacharelado em Engenharia de Software Professor Dr. Alisson Renan Svaigen [URL 🔗](mailto:arsvaigen@uem.br)

\_____________________________________________

## Implementação de um Serviço Distribuído de “Encurtador de Links” utilizando RPC e Balanceamento de Carga Trabalho Prático 1

\_____________________________________________

## Especificação Geral

Este trabalho tem como objetivo utilizar os conceitos teóricos de comunicação entre

processos e balanceamento de carga em Sistemas Distribuídos para desenvolver um serviço simplificado de “encurtamento” de URLs. Para a comunicação entre processos, deve ser utilizado um modelo de Remote Procedure Call (RPC). Já para o balanceamento de carga, deve ser implementada a estratégia Round-Robin (RR). O serviço deverá ser executado por meio de 3 instâncias de servidores, permitindo que diferentes requisições sejam distribuídas entre essas instâncias por um balanceador de carga.

A arquitetura geral do sistema deverá considerar três tipos de componentes:

- Cliente RPC: aplicação responsável pela interação com o usuário e pela realização das chamadas remotas. O sistema deve ser capaz de suportar o maior número possível de clientes.

- Balanceador de carga: componente intermediário responsável por receber as requisições dos clientes e encaminhá-las para uma das instâncias disponíveis do serviço (servidores). O sistema deve considerar um único serviço de balanceamento de carga, atuando de maneira centralizada;

- Servidores RPC: múltiplas instâncias do serviço de encurtamento de URLs, responsáveis por efetivamente processar as chamadas RPC. Para este trabalho em específico, devem ser considerados exatamente 3 servidores.

Devido às limitações de infraestrutura para execução do trabalho utilizando, no

mínimo, 5 dispositivos computacionais distintos (ao menos 1 cliente, 1 balanceador e 3 servidores), a execução do sistema poderá ser realizada por meio de, no mínimo, dois dispositivos computacionais: ao menos 1 dispositivo executando as tarefas do cliente; e


## UNIVERSIDADE ESTADUAL DE MARINGÁ DEPARTAMENTO DE INFORMÁTICA CENTRO DE TECNOLOGIA

obrigatoriamente 1 dispositivo executando as tarefas do balanceador e dos servidores. A Figura 1 apresenta a arquitetura conceitual do SD a ser desenvolvido no trabalho.

De modo geral, a arquitetura segue o padrão cliente x servidor, considerando um

balanceador centralizado. No entanto, todos os 3 servidores devem executar localmente, no mesmo dispositivo que o balanceador de carga. Desse modo, o balanceador de carga irá distribuir as requisições para o mesmo dispositivo, de maneira local.

De modo a facilitar questões relacionadas ao roteamento, acesso e liberação de

portas nos dispositivos, é obrigatória a utilização da ferramenta ngrok1. Esta ferramenta deve ser utilizada apenas como mecanismo de acesso externo ao balanceador. Não é necessário, nem desejável, utilizar uma instância do ngrok para cada servidor RPC.

## Implementação dos componentes

- Cliente RPC: O cliente deverá fornecer uma interface simples, obrigatoriamente via terminal, para interação com o usuário e deverá realizar chamadas remotas ao serviço. O cliente não deverá conhecer diretamente os endereços das diferentes


## UNIVERSIDADE ESTADUAL DE MARINGÁ DEPARTAMENTO DE INFORMÁTICA CENTRO DE TECNOLOGIA

instâncias dos servidores RPC. Para o cliente, deverá existir apenas um ponto de acesso ao serviço: o endereço público disponibilizado pelo ngrok e associado ao balanceador. A interface deverá permitir as seguintes operações:

- “encurtar”: solicitar o encurtamento de uma URL;

- “resolver”: solicitar a resolução de uma URL já encurtada;

- “sair”: encerrar a aplicação.

- Serviço RPC: Deverá ser implementado um serviço de encurtamento de URLs que disponibiliza as seguintes operações remotas listadas a seguir. Independentemente da operação, o servidor deve gerar um print de qual requisição foi recebida, e qual é o endereço do cliente que fez a requisição.

- encurtar(url): recebe uma URL e gera um código correspondente à URL encurtada, retornando-a como resposta. Caso a URL já tenha sido encurtada anteriormente, deve retornar uma notificação informando que a URL já possui um código encurtado associado;

- Política de geração de URL encurtada:

- O par (URL original, URL encurtada) deve ser persistida no sistema, independente do meio de persistência utilizado, por exemplo, utilização de um banco de dados ou de um arquivo.

- A URL gerada deve seguir o seguinte padrão:

- sddin.uem/[caracteres]

Na qual [caracteres] representam, obrigatoriamente, 8

caracteres gerados de maneira aleatória. Os caracteres podem ser numéricos ou alfabéticos. Deve ser verificado se a URL encurtada gerada já não existe. Se existir, deve-se gerar URLs até que se encontre uma válida.

- resolver(url): recebe uma URL já encurtada, verifica se existe na base de dados e retorna a URL encurtada como resposta. Caso contrário, deve retornar uma mensagem de erro informando que a URL não consta na base de dados.

- Balanceador de carga: Deverá ser implementado um balanceador de carga responsável por receber as requisições provenientes dos clientes e encaminhá-las para uma das instâncias do servidor RPC. É importante frisar que a requisição deverá


UNIVERSIDADE ESTADUAL DE MARINGÁ

CENTRO DE TECNOLOGIA

DEPARTAMENTO DE INFORMÁTICA

ser tratada como uma caixa preta: o balanceador deve receber a requisição, selecionar o servidor de destino, encaminhar a requisição e retornar ao cliente a resposta recebida do servidor. Dessa maneira, a lógica relacionada ao serviço de encurtamento de URLs deverá permanecer exclusivamente nos servidores RPC. O balanceador deverá seguir, obrigatoriamente, a estratégia Round Robin.

## Linguagens de Programação e bibliotecas permitidas para implementação

Este trabalho pode ser implementado nas seguintes linguagens de programação:

Python, C, C++ ou Java. Não serão aceitas implementações em quaisquer outras linguagens além das quatro listadas. Para a comunicação RPC, pode se utilizar qualquer biblioteca da linguagem escolhida (seja ela uma biblioteca nativa ou uma dependência). No entanto, não é permitido a utilização de bibliotecas ou softwares próprios de balanceamento de carga, por exemplo, o NGINX.

## Casos omissos

Quaisquer casos omissos relacionados ao desenvolvimento deste trabalho que não

foram esclarecidos nesta descrição deverão ser arguidas diretamente com o professor de maneira pública, por meio de comentários públicos na área de instruções e de submissão deste trabalho, exclusivamente via Google Classroom.

## Normas para desenvolvimento e entrega do Trabalho Prático

O trabalho prático deve ser desenvolvido por uma equipe de, no mínimo, UM aluno

matriculado na disciplina e, no máximo, CINCO alunos matriculados na disciplina.

A submissão do trabalho prático será feita exclusivamente via Classroom, na página

correspondente à disciplina. Não serão aceitos trabalhos entregues após o prazo final e também não serão aceitos trabalhos submetidos por outros locais (email, whatsapp, etc.).

Os seguintes documentos devem ser entregues:

- Código fonte do ambiente de simulação desenvolvido; Arquivo no estilo “README” apresentando qual a versão da linguagem de programação utilizada, como compilar (se for o caso) e executar o sistema. Caso seja necessário utilizar alguma biblioteca adicional, identificar nesse arquivo.

4


## UNIVERSIDADE ESTADUAL DE MARINGÁ DEPARTAMENTO DE INFORMÁTICA CENTRO DE TECNOLOGIA

Prazo final: 04/10/2026 às 23:59.

Observação: O tempo estipulado para realização deste trabalho é menor do que o prazo final determinado. Mais especificamente, este trabalho possui uma duração estimada de duas semanas e meia para ser completamente desenvolvido. Dessa maneira, alunos atendidos pelo PROPAE já estão contemplados com 50% a mais do tempo necessário para desenvolvimento do trabalho.

## Apresentações do Trabalho Prático

- As apresentações irão ocorrer nos dias 06 e 08 de outubro de 2026, preferencialmente no horário de aula. Caso o número de equipes ultrapasse o quantitativo adequado para apresentação em horário de aula, o professor se reserva ao direito de combinar outros horários de apresentação com cada equipe.

- O cronograma de apresentação será definido unilateralmente pelo professor, sendo divulgado na véspera do primeiro dia de apresentações (ou antes, conforme disponibilidade do professor).

- O professor fornecerá 2 dispositivos computacionais para execução do sistema.

- A apresentação consistirá na demonstração de execução do sistema. Durante a demonstração, o professor se reserva ao direito de:

- Solicitar que a equipe proceda com a execução do sistema;

- Realizar perguntas para a equipe, ou individualmente, relacionadas à implementação do código e ao comportamento do sistema;

- Realizar perguntas para a equipe, ou individualmente, relacionadas à fundamentação teórica vista em sala de aula, desde que esteja alinhada ao desenvolvimento do trabalho prático.

## Considerações Finais

- A apresentação do trabalho é mandatória para toda a equipe.

- A performance individual e em equipe na apresentação possui caráter de pontuação eliminatório, ou seja: caso o professor avalie que o indivíduo, ou a equipe, não demonstram conhecimento sobre o desenvolvimento do trabalho, toda a nota pode ser zerada, mesmo que o trabalho tenha sido implementado e entregue.

- É por meio da apresentação que o professor da disciplina se certificará de que todos os membros da equipe contribuíram para a realização do trabalho prático!

- Se for utilizar ferramentas de IA, utilize com responsabilidade, e saiba aquilo que você está fazendo 🙂
