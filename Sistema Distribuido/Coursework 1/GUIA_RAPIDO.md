# Guia rápido de execução

## 1. Computador dos servidores

No Windows, execute nesta ordem:

```text
scripts\windows\iniciar_servidores.bat
scripts\windows\iniciar_balanceador.bat
```

No Linux ou macOS:

```bash
chmod +x scripts/unix/*.sh
./scripts/unix/iniciar_servidores.sh
./scripts/unix/iniciar_balanceador.sh
```

Confirme que os servidores aparecem como disponíveis no terminal do balanceador.

## 2. Publicar o balanceador

Em outro terminal do mesmo computador:

```bash
ngrok http 8000
```

Copie a URL HTTPS mostrada pelo ngrok. Somente o balanceador deve ser publicado; não crie túneis para as portas 9000, 9001 ou 9002.

## 3. Computador do cliente

Substitua a URL do exemplo pela fornecida pelo ngrok:

```bash
python src/cliente_encurtador.py --servidor https://exemplo.ngrok-free.app
```

No Windows também é possível usar:

```text
scripts\windows\iniciar_cliente.bat --servidor https://exemplo.ngrok-free.app
```

Para um teste totalmente local, omita `--servidor`.

## 4. Testar

Com o sistema em execução:

```bash
python tests/teste_sistema.py
```

Ou pela URL pública:

```bash
python tests/teste_sistema.py --servidor https://exemplo.ngrok-free.app
```

O resultado esperado termina com:

```text
[OK] TODOS OS TESTES PASSARAM
```

Consulte o [README.md](README.md) para configuração, arquitetura e solução de problemas.
