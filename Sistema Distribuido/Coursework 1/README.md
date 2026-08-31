# Encurtador de Links Distribuído

Serviço distribuído de encurtamento de URLs desenvolvido para o Trabalho Prático 1 de DIN9929 — Sistemas Distribuídos. A comunicação utiliza XML-RPC e o balanceador distribui as requisições entre exatamente três servidores com Round-Robin.

## Arquitetura

```text
Cliente de terminal
        |
        | XML-RPC pela URL pública do ngrok
        v
Balanceador centralizado (127.0.0.1:8000)
        |
        +-- Servidor 0 (127.0.0.1:9000)
        +-- Servidor 1 (127.0.0.1:9001)
        +-- Servidor 2 (127.0.0.1:9002)
                    |
                    v
              data/urls.db
```

Os servidores e o balanceador devem executar no mesmo computador. O cliente pode executar em outro computador e conhece apenas a URL pública do balanceador.

## Requisitos

- Python 3.7 ou superior.
- ngrok instalado e autenticado no computador do balanceador.
- Nenhuma biblioteca Python externa: são usadas apenas bibliotecas da distribuição padrão.

## Execução obrigatória com ngrok

No computador que executará o balanceador e os servidores, abra cinco terminais.

1. Inicie os três servidores:

   ```bash
   python src/servidor_encurtador.py 0
   python src/servidor_encurtador.py 1
   python src/servidor_encurtador.py 2
   ```

2. Inicie o balanceador:

   ```bash
   python src/balanceador_carga.py
   ```

3. Publique somente a porta do balanceador:

   ```bash
   ngrok http 8000
   ```

4. Copie a URL HTTPS exibida pelo ngrok, por exemplo `https://exemplo.ngrok-free.app`.

No computador do cliente, execute:

```bash
python src/cliente_encurtador.py --servidor https://exemplo.ngrok-free.app
```

A URL também pode ser fornecida pela variável de ambiente `ENCURTADOR_URL`.

## Execução local para desenvolvimento

Para testar tudo no mesmo computador, inicie os servidores e o balanceador como acima e execute:

```bash
python src/cliente_encurtador.py
```

O endereço local padrão é `http://127.0.0.1:8000`.

## Scripts auxiliares

No Windows:

```text
scripts\windows\iniciar_servidores.bat
scripts\windows\iniciar_balanceador.bat
scripts\windows\iniciar_cliente.bat --servidor URL_DO_NGROK
```

No Linux ou macOS:

```bash
chmod +x scripts/unix/*.sh
./scripts/unix/iniciar_servidores.sh
./scripts/unix/iniciar_balanceador.sh
./scripts/unix/iniciar_cliente.sh --servidor URL_DO_NGROK
```

Se necessário, defina `PYTHON_BIN=python` ou `PYTHON_BIN=python3` antes de executar os scripts Unix.

## Operações

### `encurtar(url)`

- Aceita uma URL completa com protocolo HTTP ou HTTPS.
- Gera oito caracteres alfanuméricos aleatórios.
- Retorna o formato `sddin.uem/Ab12Cd34`.
- Se a URL já existir, retorna o mesmo código com status `existente`.

### `resolver(url_encurtada)`

- Aceita `sddin.uem/Ab12Cd34` ou somente `Ab12Cd34`.
- Retorna a URL original quando o código existe.
- Retorna status `erro` para formato inválido ou código inexistente.

## Persistência e concorrência

Os dados ficam em `data/urls.db`, criado automaticamente. SQLite fornece transações e restrições únicas tanto para a URL original quanto para o código. Isso evita a perda de atualizações que ocorreria se três processos reescrevessem simultaneamente um único arquivo JSON.

O banco, seus arquivos temporários e os caches do Python estão ignorados pelo Git.

## Balanceamento e falhas

O índice Round-Robin é protegido contra acesso concorrente. Para cada nova requisição, o balanceador escolhe o próximo servidor na sequência 0, 1, 2, 0, 1, 2. Se o escolhido estiver indisponível, a mesma requisição tenta os demais servidores, mantendo o balanceador operacional enquanto houver pelo menos uma instância ativa.

As chamadas possuem timeout configurável. O balanceador trata a requisição como caixa preta: identifica o método RPC permitido, escolhe um destino e encaminha os argumentos sem executar lógica de encurtamento.

## Logs

Cada servidor imprime a operação recebida e o endereço do cliente encaminhado pelo balanceador:

```text
[SERVIDOR 1] Requisição recebida: encurtar
[SERVIDOR 1] Cliente: 203.0.113.10
```

Quando existe `X-Forwarded-For`, como no acesso via ngrok, o balanceador o utiliza. Caso contrário, registra o endereço da conexão TCP.

## Testes integrados

Com os três servidores e o balanceador em execução:

```bash
python tests/teste_sistema.py
```

Para testar pela URL pública:

```bash
python tests/teste_sistema.py --servidor https://exemplo.ngrok-free.app
```

Os testes verificam disponibilidade das três instâncias, formato do código, persistência, resolução, duplicidade, entradas inválidas, sequência Round-Robin e 24 requisições concorrentes.

## Estrutura

```text
.
├── src/                         Código principal
│   ├── servidor_encurtador.py
│   ├── balanceador_carga.py
│   ├── cliente_encurtador.py
│   └── rpc_utils.py
├── tests/                       Testes integrados
├── scripts/
│   ├── windows/
│   └── unix/
├── data/                        Banco criado em execução
├── docs/                        Especificação e arquivos históricos
├── GUIA_RAPIDO.md
└── README.md
```

Os arquivos de `docs/archive/` são preservados apenas como referência e não fazem parte da entrega mínima. Os exemplos antigos de calculadora RPC/REST foram removidos por não pertencerem a este trabalho.

## Opções úteis

```bash
python src/servidor_encurtador.py --help
python src/balanceador_carga.py --help
python src/cliente_encurtador.py --help
python tests/teste_sistema.py --help
```

A especificação original convertida para Markdown está em [docs/DIN9929 - Trabalho Prático 1 - Especificação.md](docs/DIN9929%20-%20Trabalho%20Prático%201%20-%20Especificação.md).
