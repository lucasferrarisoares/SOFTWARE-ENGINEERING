def leia_reg(fd) -> str:
    tam = int.from_bytes(fd.read(2))
    if tam > 0:
        s = fd.read(tam)
        return s.decode()
    return ''

def busca_seq():

    try:
        NOME_ARQ = input('Qual nome do arquivo: ')
        ENTRADA = open(NOME_ARQ, 'rb')

        CHAVE = str(input('Qual sobrenome deve ser buscado:'))
        ACHOU = False
        REG = leia_reg(ENTRADA)  

        while REG != "" and ACHOU == False:
            SOBRENOME = REG.split(sep='|')[0]

            if SOBRENOME == CHAVE:
                ACHOU = True
            else:
                REG = leia_reg(ENTRADA)
        if ACHOU == True:
            REG = REG.split(sep='|')

            for x in REG:
                print(x)
        else:
            TypeError("Errouw")


    except FileNotFoundError:
        print('Não foi possível abrir o arquivo')
        exit()


busca_seq()