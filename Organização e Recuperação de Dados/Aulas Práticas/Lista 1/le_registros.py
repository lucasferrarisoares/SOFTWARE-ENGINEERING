def leia_reg(fd) -> str:
    tam = int.from_bytes(fd.read(2))
    if tam > 0:
        s = fd.read(tam)
        return s.decode()
    return ''

def main() -> None:
    try:
        nomeArq = input('Digite o nome do arquivo a ser aberto: ')
        fd = open(nomeArq, 'rb')
        contaReg = 1

        buffer = leia_reg(fd)
        
        while buffer:
            print(f"\nRegistro #{contaReg} (Tam = {len(buffer)}):")
            contaCampo = 1
            for campo in buffer.split(sep='|'):
                if campo:
                    print(f"Campo #{contaCampo}: {campo}")
                    contaCampo += 1
            contaReg += 1
            buffer = leia_reg(fd)
        print()
        fd.close()
    except FileNotFoundError:
        print('Não foi possível abrir o arquivo')
        exit()


if __name__ == '__main__':
    main()