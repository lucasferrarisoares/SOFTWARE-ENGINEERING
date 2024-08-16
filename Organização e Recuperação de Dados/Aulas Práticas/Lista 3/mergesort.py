import io

#CONSTANTES
VALOR_BAIXO = ""
VALOR_ALTO = "~"

def inicialize () -> tuple[str, str, io.TextIOWrapper, io.TextIOWrapper,
                           io.TextIOWrapper, bool]:
    
    ant1 = VALOR_BAIXO
    ant2 = VALOR_BAIXO

    arql1 = open("lista1.txt", "r")
    arql2 = open("lista2.txt", "r")
    saida = open("saida.txt", "w")

    existem_mais_nomes = True

    return ant1, ant2, arql1, arql2, saida, existem_mais_nomes


def leia_nomes(lista: io.TextIOWrapper, nome_ant: str, nome_outra_lista: str,
existem_mais_nomes: bool) -> tuple[str, str, bool]:
    
    NOME = lista.readline().strip()

    if not NOME:
        if nome_outra_lista == VALOR_ALTO:
            existem_mais_nomes = False
        else:
            NOME = VALOR_ALTO
    else:
        if NOME <= nome_ant:
            ValueError("Erro de sequência")
    nome_ant = NOME

    return NOME, nome_ant, existem_mais_nomes

def merge() -> None:
    
    ant1, ant2, lista1, lista2, saida, existem_mais_nomes = inicialize()

    nome1, ant1, existem_mais_nomes = leia_nomes(lista1, ant1, "", existem_mais_nomes)
    nome2, ant2, existem_mais_nomes = leia_nomes(lista2, ant2, "", existem_mais_nomes)

    while existem_mais_nomes:
        if nome1 < nome2:
            saida.write(nome1 + '\n') 
            nome1, ant1, existem_mais_nomes = leia_nomes(lista1, ant1, ant2, existem_mais_nomes)
        elif nome1 > nome2:
            saida.write(nome2 + '\n')
            nome2, ant2, existem_mais_nomes = leia_nomes(lista2, ant2, ant1, existem_mais_nomes)
        else:
            saida.write(nome1 + '\n')
            nome1, ant1, existem_mais_nomes = leia_nomes(lista1, ant1, ant2, existem_mais_nomes)
            nome2, ant2, existem_mais_nomes = leia_nomes(lista2, ant2, ant1, existem_mais_nomes)

    lista1.close()
    lista2.close()
    saida.close()

if __name__ == '__main__':
    merge()


    