from urllib.request import urlopen
from urllib.parse import urlencode
import json

ENDERECO = "127.0.0.1"
PORTA= "8000"

while True:

    print("--- Realizando operações matemáticas elementares com REST")
    print("1 - Somar")
    print("2 - Multiplicar")
    print("3 - Subtrair")
    print("4 - Dividir")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")
    print("\n")

    if opcao == "0":
        break

    if opcao == "1" or opcao == "2" or opcao == "3" or opcao == "4":

        try:
            a = float(input("Digite o primeiro número: "))
            b = float(input("Digite o segundo número: "))

            if opcao == "4" and b == 0:
                print("Erro: não é possível dividir por zero.")
                input("Pressione Enter para continuar...")
                print("\n" * 3)
                continue

            if opcao == "1":
                operacao = "sum"
            if opcao == "2":
                operacao = "mult"
            if opcao == "3":
                operacao = "sub"
            if opcao == "4":
                operacao = "div"

            params = urlencode({"a": a, "b": b})
            url = f"http://{ENDERECO}:{PORTA}/{operacao}?{params}"

            response = urlopen(url)
            result = json.loads(response.read().decode("utf-8"))
            print(f"Resultado: {result}")
            input("Pressione Enter para continuar...")
            print("\n" * 3)

        except Exception as erro:
            print("Erro ao comunicar com o servidor:")
            print(erro)

    else:
        print("Opção inválida.")
