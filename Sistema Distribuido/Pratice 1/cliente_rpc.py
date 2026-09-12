import xmlrpc.client

ENDERECO = "127.0.0.1"
PORTA= "8000"

cliente = xmlrpc.client.ServerProxy(f"http://{ENDERECO}:{PORTA}")

while True:

    print("--- Realizando operações matemáticas elementares com RPC")
    print("1 - Somar")
    print("2 - Multiplicar")
    print("3 - Subtrair")
    print("4 - Dividir")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "0":
        print("Encerrando cliente...")
        break

    if opcao in ("1", "2", "3", "4"):

        try:
            a = float(input("Digite o primeiro número: "))
            b = float(input("Digite o segundo número: "))

            if opcao == "1":
                result = cliente.somar(a, b)
            if opcao == "2":
                result = cliente.multiplicar(a, b)
            if opcao == "3":
                result = cliente.subtrair(a, b)
            if opcao == "4":
                result = cliente.dividir(a, b)

            print(f"Resultado: {result}")
            input("Pressione Enter para continuar...")
            print("\n" * 3)

        except xmlrpc.client.Fault as erro:
            if "Nao e possivel dividir por zero" in erro.faultString:
                print("Erro: nao e possivel dividir por zero.")
            else:
                print("Erro retornado pelo servidor:")
                print(erro)
        except Exception as erro:
            print("Erro ao comunicar com o servidor:")
            print(erro)

    else:
        print("Opção inválida.")