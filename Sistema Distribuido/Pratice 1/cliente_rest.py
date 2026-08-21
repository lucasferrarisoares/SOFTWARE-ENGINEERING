from urllib.request import urlopen
from urllib.parse import urlencode
import json

ENDERECO = "127.0.0.1"
PORTA= "8000"


while True:

    print("--- Realizando operações matemáticas elementares com REST")
    print("1 - Somar")
    print("2 - Multiplicar")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "0":
        break

    if opcao == "1" or opcao == "2":

        try:
            a = float(input("Digite o primeiro número: "))
            b = float(input("Digite o segundo número: "))

            if opcao == "1":
                operacao = "somar"
            else:
                operacao = "multiplicar"

            #implementar em aula

        except Exception as erro:
            print("Erro ao comunicar com o servidor:")
            print(erro)

    else:
        print("Opção inválida.")