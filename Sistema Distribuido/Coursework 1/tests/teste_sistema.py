#!/usr/bin/env python3
import argparse
import os
import re
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


RAIZ_PROJETO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_PROJETO / "src"))

from rpc_utils import criar_proxy  # noqa: E402


URL_BALANCEADOR_PADRAO = "http://127.0.0.1:8000"
PADRAO_URL_ENCURTADA = re.compile(r"^sddin\.uem/[A-Za-z0-9]{8}$")


def verificar(condicao, mensagem):
    if not condicao:
        raise AssertionError(mensagem)
    print(f"  [OK] {mensagem}")


def testar_ping(cliente):
    print("\n[1/7] Conexão e disponibilidade")
    resposta = cliente.ping()
    verificar(resposta.get("status") == "ok", "balanceador respondeu ao ping")
    servidores = resposta.get("servidores", [])
    verificar(len(servidores) == 3, "balanceador conhece exatamente 3 servidores")
    verificar(
        all(item.get("disponivel") for item in servidores),
        "os 3 servidores estão disponíveis",
    )


def testar_encurtamento_e_resolucao(cliente, marcador):
    print("\n[2/7] Encurtamento e formato")
    url_original = f"https://example.com/teste/{marcador}"
    resposta = cliente.encurtar(url_original)
    verificar(resposta.get("status") == "sucesso", "URL inédita foi encurtada")
    url_encurtada = resposta.get("url_encurtada", "")
    verificar(
        PADRAO_URL_ENCURTADA.fullmatch(url_encurtada) is not None,
        "URL encurtada segue sddin.uem/ + 8 caracteres alfanuméricos",
    )

    print("\n[3/7] Resolução")
    resolucao = cliente.resolver(url_encurtada)
    verificar(resolucao.get("status") == "sucesso", "URL encurtada foi resolvida")
    verificar(
        resolucao.get("url_original") == url_original,
        "resolução devolveu a URL original correta",
    )
    return url_original, url_encurtada


def testar_duplicidade(cliente, url_original, url_encurtada):
    print("\n[4/7] URL duplicada")
    repetida = cliente.encurtar(url_original)
    verificar(repetida.get("status") == "existente", "duplicidade foi notificada")
    verificar(
        repetida.get("url_encurtada") == url_encurtada,
        "URL repetida manteve o mesmo código",
    )


def testar_erros(cliente, marcador):
    print("\n[5/7] Entradas inválidas e código inexistente")
    invalida = cliente.encurtar("isto-nao-e-uma-url")
    verificar(invalida.get("status") == "erro", "URL original inválida foi rejeitada")

    codigo_inexistente = f"sddin.uem/{marcador[:8]}"
    inexistente = cliente.resolver(codigo_inexistente)
    verificar(
        inexistente.get("status") == "erro",
        "código inexistente retornou erro",
    )


def testar_round_robin(cliente, marcador):
    print("\n[6/7] Round-Robin")
    ids = []
    for indice in range(6):
        resposta = cliente.encurtar(
            f"https://round-robin.example/{marcador}/{indice}"
        )
        verificar(
            resposta.get("status") == "sucesso",
            f"requisição Round-Robin {indice + 1} foi processada",
        )
        ids.append(resposta.get("servidor_id"))

    inicio = ids[0]
    esperado = [(inicio + deslocamento) % 3 for deslocamento in range(6)]
    verificar(ids == esperado, f"sequência observada {ids} segue Round-Robin")


def testar_concorrencia(endereco, timeout, marcador):
    print("\n[7/7] Clientes concorrentes")

    def enviar(indice):
        with criar_proxy(endereco, timeout) as cliente:
            return cliente.encurtar(
                f"https://concorrencia.example/{marcador}/{indice}"
            )

    with ThreadPoolExecutor(max_workers=12) as executor:
        respostas = list(executor.map(enviar, range(24)))

    verificar(
        all(resposta.get("status") == "sucesso" for resposta in respostas),
        "24 requisições concorrentes foram processadas",
    )
    urls_encurtadas = {resposta.get("url_encurtada") for resposta in respostas}
    verificar(len(urls_encurtadas) == 24, "os códigos concorrentes são únicos")
    servidores = {resposta.get("servidor_id") for resposta in respostas}
    verificar(servidores == {0, 1, 2}, "as três instâncias atenderam clientes")


def criar_parser():
    parser = argparse.ArgumentParser(description="Testes integrados do encurtador")
    parser.add_argument(
        "--servidor",
        default=os.getenv("ENCURTADOR_URL", URL_BALANCEADOR_PADRAO),
        help="URL local ou URL pública do ngrok",
    )
    parser.add_argument("--timeout", type=float, default=10.0)
    return parser


def main():
    argumentos = criar_parser().parse_args()
    marcador = uuid.uuid4().hex
    endereco = argumentos.servidor.rstrip("/")
    cliente = criar_proxy(endereco, argumentos.timeout)

    print("=" * 60)
    print("TESTES INTEGRADOS - ENCURTADOR DISTRIBUÍDO")
    print("=" * 60)

    try:
        testar_ping(cliente)
        url_original, url_encurtada = testar_encurtamento_e_resolucao(
            cliente, marcador
        )
        testar_duplicidade(cliente, url_original, url_encurtada)
        testar_erros(cliente, marcador)
        testar_round_robin(cliente, marcador)
        testar_concorrencia(endereco, argumentos.timeout, marcador)
    except Exception as erro:
        print(f"\n[ERRO] TESTE FALHOU: {erro}")
        return 1
    finally:
        cliente.close()

    print("\n[OK] TODOS OS TESTES PASSARAM")
    return 0


if __name__ == "__main__":
    sys.exit(main())
