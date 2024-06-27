mensagens: str = [
    "                                   Nome: ",
    "                               Endereco: ",
    "                                 Cidade: ",
    "                                 Estado: ",
    "                                    CEP: "
]

def concatena_campo(buffer: str, campo: str) -> str:
    return buffer + campo + '|'
    

def main() -> None:
    nomeArq = input('Digite o nome do arquivo a ser criado: ')
    fd = open(nomeArq, 'wb')

    campo = input("Digite o sobrenome ou <ENTER> para sair: ")

    while campo:
        buffer = ''
        buffer = concatena_campo(buffer, campo)
        for m in mensagens:
            campo = input(m)
            buffer = concatena_campo(buffer, campo)
        ''' caracteres especiais vão ocupar mais de um byte depois de decodificados, 
        por isso precisa decodificar antes de calcular o tamanho '''
        
        buffer = buffer.encode()
        lenBuffer = len(buffer)
        fd.write(lenBuffer.to_bytes(2))
        fd.write(buffer)
        campo = input("Digite o sobrenome ou <ENTER> para sair: ")
    
    fd.close()


if __name__ == '__main__':
    main()