def busca_e_atualiza():
    NOME_ARQ = input("Qual nome do arquivo: ")

    ARQ = open(NOME_ARQ, "r + b")

    if not NOME_ARQ:
        ARQ = open(NOME_ARQ, "w + r")
        TOTAL_REG = 0
        ARQ.write(4)
    else:
        ARQ = open(NOME_ARQ, "r + b",)
        TOTAL_REG = ARQ.read(4)
    
    while True:
        print()
        print('\nMenu:')
        print('1. Inserir novo registro;')
        print('2. Bucar um registro por RRN para alterações;')
        print('3; Finalizar.')

        opcao = input('Olá, seja bem-vindo, qual opção deseja selecionar? ')

        if opcao == '1':
            a
        elif opcao == '2':
            a
        elif opcao == '3':     
            print()
            print("Fechando o modo operação.")
            print()
            break
        else:
            print("Opção inválida. Tente novamente.")



