import xmlrpc.client

ENDERECO = "127.0.0.1"
PORTA= "8000"

cliente = xmlrpc.client.ServerProxy(f"http://{ENDERECO}:{PORTA}")


while True:

    print("--- Realizando operações matemáticas elementares com RPC")
    print("1 - Somar")
    print("2 - Multiplicar")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "0":
        print("Encerrando cliente...")
        break

    if opcao == "1" or opcao == "2":

        try:
            a = float(input("Digite o primeiro número: "))
            b = float(input("Digite o segundo número: "))

            #implementar o restante em aula

        except Exception as erro:
            print("Erro ao comunicar com o servidor:")
            print(erro)

    else:
        print("Opção inválida.")