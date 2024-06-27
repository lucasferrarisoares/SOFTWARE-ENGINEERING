import os

def busca_rrn():
    NOME_ARQ = input('Qual nome do arquivo: ')

    ENTRADA = open(NOME_ARQ, 'rb')

    CAB = ENTRADA.read(4)
    TOTAL_REG = int.from_bytes(CAB, byteorder='big')

    RRN = int(input('Qual registro deve ser acessado: '))

    if RRN >= TOTAL_REG:
        raise TypeError('Errouw')
    
    OFFSET = ((RRN * 64) + 4)
    ENTRADA.seek(OFFSET)
    REG = ENTRADA.read(64)
    REG = REG.decode()
    REG = REG.split(sep="|")
    

    for CAMPO in REG:
        print(CAMPO)


busca_rrn()