import argparse
import os
import sys
from urllib.parse import urlparse

from rpc_utils import criar_proxy


URL_BALANCEADOR_PADRAO = "http://127.0.0.1:8000"


def validar_url(url):
    analisada = urlparse(url.strip())
    return analisada.scheme in {"http", "https"} and bool(analisada.netloc)


def criar_parser():
    parser = argparse.ArgumentParser(description="Cliente do encurtador de URLs")
    parser.add_argument(
        "--servidor",
        default=os.getenv("ENCURTADOR_URL", URL_BALANCEADOR_PADRAO),
        help="URL local ou URL pública HTTPS fornecida pelo ngrok",
    )
    parser.add_argument("--timeout", type=float, default=10.0)
    return parser


def main():
    argumentos = criar_parser().parse_args()
    endereco = argumentos.servidor.rstrip("/")

    print("\n" + "=" * 60)
    print("SERVIÇO DISTRIBUÍDO DE ENCURTADOR DE LINKS")
    print("=" * 60)

    cliente = criar_proxy(endereco, argumentos.timeout)
    try:
        resposta_ping = cliente.ping()
        if resposta_ping.get("status") != "ok":
            raise ConnectionError("o balanceador não respondeu corretamente")
        print(f"\n[OK] Conectado ao balanceador em {endereco}\n")
    except Exception as erro:
        print(f"\n[ERRO] Erro ao conectar ao balanceador: {erro}")
        print("Confira a URL, o ngrok e se o balanceador está em execução.")
        cliente.close()
        return 1

    try:
        while True:
            print("\n" + "-" * 60)
            print("MENU PRINCIPAL")
            print("-" * 60)
            print("1 - Encurtar URL")
            print("2 - Resolver URL encurtada")
            print("0 - Sair")
            print("-" * 60)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "0":
                print("\n[OK] Encerrando cliente...")
                break

            if opcao == "1":
                print("\n--- ENCURTAR URL ---")
                url = input("Digite a URL a ser encurtada: ").strip()
                if not validar_url(url):
                    print("[ERRO] URL inválida! Exemplo: https://example.com")
                    continue

                try:
                    resultado = cliente.encurtar(url)
                    if resultado.get("status") == "sucesso":
                        print("\n[OK] URL encurtada com sucesso!")
                        print(f"  URL original: {resultado['url_original']}")
                        print(f"  URL encurtada: {resultado['url_encurtada']}")
                    elif resultado.get("status") == "existente":
                        print("\n[AVISO] Esta URL já foi encurtada!")
                        print(f"  URL original: {resultado['url_original']}")
                        print(f"  URL encurtada: {resultado['url_encurtada']}")
                    else:
                        print(f"\n[ERRO] {resultado.get('mensagem', 'Erro desconhecido')}")
                except Exception as erro:
                    print(f"\n[ERRO] Erro ao comunicar com o serviço: {erro}")
                continue

            if opcao == "2":
                print("\n--- RESOLVER URL ---")
                url_encurtada = input(
                    "Digite a URL encurtada (ex: sddin.uem/abc12345): "
                ).strip()
                if not url_encurtada:
                    print("[ERRO] URL inválida!")
                    continue

                try:
                    resultado = cliente.resolver(url_encurtada)
                    if resultado.get("status") == "sucesso":
                        print("\n[OK] URL encontrada!")
                        print(f"  Código: {resultado['codigo']}")
                        print(f"  URL original: {resultado['url_original']}")
                    else:
                        print(f"\n[ERRO] {resultado.get('mensagem', 'Erro desconhecido')}")
                except Exception as erro:
                    print(f"\n[ERRO] Erro ao comunicar com o serviço: {erro}")
                continue

            print("\n[ERRO] Opção inválida!")
    finally:
        cliente.close()

    print("\n" + "=" * 60)
    print("Até logo!")
    print("=" * 60 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
