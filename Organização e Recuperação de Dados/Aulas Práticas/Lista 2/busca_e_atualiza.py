def busca_e_atualiza():
    NOME_ARQ = input("Qual nome do arquivo: ")

    try:
        ARQ = open(NOME_ARQ, 'rb+')
    except:
        ARQ = open(NOME_ARQ, 'wb+')
        TOTAL_REG = 0
        TOTAL_REG = TOTAL_REG.to_bytes(4)
        ARQ.write(TOTAL_REG)
    
    TOTAL_REG = ARQ.read(4)
    TOTAL_REG = int.from_bytes(TOTAL_REG)


    opcao = int(escolhaopcao())

    while opcao != 3:
        if opcao == 1:
            print()
            SOBRENOME = input('Sobrenome: ')
            NOME = input('Nome: ')
            RUA = input('Rua: ')
            CIDADE = input('Cidade: ')
            ESTADO = input('Estado: ')
            CEP = input('CEP: ')

            REG = f'{SOBRENOME}|{NOME}|{RUA}|{CIDADE}|{ESTADO}|{CEP}|'
            REG = REG.encode()
            REG = REG.ljust(64, b'\0')

            TOTAL_REG += 1
            OFFSET = TOTAL_REG * 64 + 4
            ARQ.seek(OFFSET)
            ARQ.write(REG)
            TOTAL_REG += 1             
        elif opcao == 2:
            RRN = int(input('Qual o RRN: '))
                
            if RRN > TOTAL_REG:
                    print()
                    print('Erro!')
                    print()
            else:
                OFFSET = RRN * 64 + 4
                ARQ.seek(OFFSET)
                REG = ARQ.read(64)
                REG = REG.decode()
                REG = REG.replace('\0', '')
                for campo in REG.split(sep='|')[:-1]:
                    print(campo)

            ALTERAR = input('Deseja alterar o registro?(S/N) ')
            if ALTERAR.upper() == "S":
                SOBRENOME = input('Sobrenome: ')
                NOME = input('Nome: ')
                RUA = input('Rua: ')
                CIDADE = input('Cidade: ')
                ESTADO = input('Estado: ')
                CEP = input('CEP: ')
                    
                REG = f'{SOBRENOME}|{NOME}|{CIDADE}|{ESTADO}|{CEP}|'
                REG = REG.encode()
                REG = REG.ljust(64, b'\0')

                ARQ.seek(OFFSET)
                ARQ.write(REG)            
        elif opcao == 3:     
            print()
            print("Fechando o modo operação.")
            print()                
            break
        else:
            print("Opção inválida. Tente novamente.")  
        opcao = int(escolhaopcao())
            
                    
    ARQ.seek(0)
    TOTAL_REG = TOTAL_REG.to_bytes(4)
    ARQ.write(TOTAL_REG)
    ARQ.close()


def escolhaopcao() -> int:
        print()
        print('\nMenu:')
        print('1. Inserir novo registro;')
        print('2. Bucar um registro por RRN para alterações;')
        print('3; Finalizar.')
        print()

        opcao = input('Olá, seja bem-vindo, qual opção deseja selecionar? ')

        return opcao




busca_e_atualiza()



