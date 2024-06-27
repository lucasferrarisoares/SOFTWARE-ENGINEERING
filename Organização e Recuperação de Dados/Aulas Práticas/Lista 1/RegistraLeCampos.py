def escreve_campos(NOME_ARQ: str):

    arq = open(NOME_ARQ, 'w')
    
    SOBRENOME = str(input('Qual sobrenome? '))
    separa = str('|')
    quebra = str('\n')
    

    while SOBRENOME != "":
        NOME = str(input('Qual nome? '))
        ENDERECO = str(input('Qual endereço? '))
        CIDADE = str(input('Qual cidade? '))
        ESTADO = str(input('Qual o estado? '))
        CEP = str(input('Qual CEP? '))

        arq.write(SOBRENOME) 
        arq.write(separa) 
        arq.write(NOME) 
        arq.write(separa) 
        arq.write(ENDERECO) 
        arq.write(separa) 
        arq.write(CIDADE) 
        arq.write(separa) 
        arq.write(ESTADO) 
        arq.write(separa) 
        arq.write(CEP) 
        arq.write(quebra)

        SOBRENOME = str(input('Qual sobrenome? '))
        if SOBRENOME == "":
            arq.close()
            ValueError("O campo do sobrenome está vázio")
    
    print('O campo do sobrenome está vázio.')
    arq.close()

def leia_campo(fd) -> str:
    campo = ''
    c = fd.read(1)
    while c and c != '|':
        campo += c
        c = fd.read(1)
    return campo


def le_campo() -> None:
    nomeArq = input('Digite o nome do arquivo a ser aberto: ')
    try:
        fd = open(nomeArq, 'r')
        contaCampo = 1
        campo = leia_campo(fd)
        while campo:
            print(f'\tCampo #{contaCampo}: {campo}')
            contaCampo += 1
            campo = leia_campo(fd)
        fd.close()
    except FileNotFoundError:
        print('Não foi possível abrir o arquivo')
        exit()






NOME_ARQ = str(input('Qual Nome do arquivo: '))
escreve_campos(NOME_ARQ)
le_campo()


# Há alguns pontos no seu código que precisam ser corrigidos para evitar erros e garantir que ele funcione conforme o esperado. Vou listar as correções necessárias:
# No método leia_campo, você está inicializando CAMPO como str, que é a classe string, e não uma string vazia.
# A condição while C != "" and "|" está incorreta. A comparação correta seria while C != "" and C != "|".
# Na função le_campos, você está tentando fechar arq, mas o arquivo aberto é ENTRADA. Isso causará um erro porque arq não está definido no escopo da função le_campos.
# O ValueError na função escreve_campos não deve ser utilizado como está. Você deve levantar a exceção com raise ValueError.
# Aqui está a versão corrigida do seu código:
