# Pratica 1: Comunicacao entre Processos

## Versao em portugues

### Objetivo

Nesta primeira atividade pratica, serao implementados e executados exemplos de comunicacao entre processos utilizando dois modelos:

- **RPC (Remote Procedure Call);**
- **REST (Representational State Transfer).**

A atividade utiliza a linguagem de programacao **Python**.

### Contexto de execucao

A atividade sera realizada inicialmente no laboratorio. Devido as limitacoes de comunicacao entre maquinas distintas impostas pela legislacao da UEM, os experimentos serao executados em uma arquitetura local e centralizada.

Dessa forma, o funcionamento da comunicacao entre processos em Sistemas Distribuidos sera simulado localmente.

### Atividade

1. Baixe e extraia os arquivos fornecidos em anexo.
2. Siga as instrucoes do professor para implementar a comunicacao entre processos.
3. Implemente, inicialmente, as seguintes operacoes matematicas basicas:
	- soma;
	- multiplicacao.
4. Implemente as operacoes adicionais:
	- subtracao;
	- divisao.
5. Realize os testes utilizando os modelos RPC e REST.

### Ordem de execucao

Para cada modelo de comunicacao:

1. Abra um terminal e inicie o **servidor**.
2. Abra outro terminal e inicie o **cliente** somente depois que o servidor estiver em execucao.
3. Teste as operacoes de soma, multiplicacao, subtracao e divisao.

#### RPC

- Servidor: `servidor_rpc.py`
- Cliente: `cliente_rpc.py`

#### REST

- Servidor: `servidor_rest.py`
- Cliente: `cliente_rest.py`

---

## English version

### Objective

In this first practical activity, examples of inter-process communication will be implemented and executed using two models:

- **RPC (Remote Procedure Call);**
- **REST (Representational State Transfer).**

The activity uses the **Python** programming language.

### Execution context

The activity will initially be carried out in the laboratory. Due to the communication limitations between different machines imposed by UEM regulations, the experiments will be executed in a local and centralized architecture.

Therefore, the operation of inter-process communication in Distributed Systems will be simulated locally.

### Activity

1. Download and extract the files provided in the attachment.
2. Follow the professor's instructions to implement the inter-process communication.
3. Initially implement the following basic mathematical operations:
	- addition;
	- multiplication.
4. Implement the additional operations:
	- subtraction;
	- division.
5. Run tests using both the RPC and REST models.

### Execution order

For each communication model:

1. Open a terminal and start the **server**.
2. Open another terminal and start the **client** only after the server is running.
3. Test the addition, multiplication, subtraction, and division operations.

#### RPC

- Server: `servidor_rpc.py`
- Client: `cliente_rpc.py`

#### REST

- Server: `servidor_rest.py`
- Client: `cliente_rest.py`
