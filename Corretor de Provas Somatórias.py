from dataclasses import dataclass

def somatorio_alternativas(s: int) -> list[int]:
    '''
    Calcula a lista de alternativas que somadas gera o somátorio *s*.
    Cada alternativa pode ser um dos valores: 1, 2, 4, 8, 16.
    Requer que *s* esteja no entre 0 e 31.
    Exemplos
    '''
    alternativas = []
    alternativa = 1

    while s > 0:
        # verifica se alternativa faz parte do somatório s
        if s % 2 == 1:
            alternativas.append(alternativa)
            # divide todas as alternativas que compõe /o somatório s por 2
        s = s // 2
        # procura a próxima alternativa
        alternativa = alternativa * 2

    return alternativas


@dataclass
class Provas:
    Codigo: int
    Redacao: float
    Respostas: list

@dataclass
class Notas_Finais:
    Codigo: int
    Nota: float

def Selecao_haptos(lista: list[Provas]) -> list:
    '''Receber uma lista de provas, verificar quais candidatos nao foram desqualificados por zerarem a redacao, e devolver uma lista com os qualificados
    >>> Selecao_haptos([Provas(3211, 80, [4, 10, 4, 16, 10]), Provas(7102, 0, [1, 2, 3, 4, 5]), Provas(1234, 90, [21, 8, 8, 8, 14]), Provas(5812, 32, [20, 0, 8, 16, 1]), Provas(9123, 0,[5, 4, 3, 2, 1])])
    [Notas_Finais(Codigo=1234, Nota=109.5), Notas_Finais(Codigo=3211, Nota=97.0), Notas_Finais(Codigo=5812, Nota=49.5)]
    '''

    lista_haptos = []
    lista_final = []
    Gabarito = [21, 10, 8, 16, 15]
    Matriz_Gabarito = []

    #adiciona os qualificados para a lista_haptos
    for i in lista:
        if i.Redacao != 0:
            lista_haptos.append(i)

    #coloca os qualificados na lista_final com sua nota parcial.
    for Provas in lista_haptos:
        Final = Notas_Finais(0, 0)
        Final.Codigo = Provas.Codigo
        Final.Nota = Provas.Redacao + Final.Nota
        lista_final.append(Final)

    #Calcula quais alternativas fazem parte da resposta.
    for i in Gabarito:
        Matriz_Gabarito.append(somatorio_alternativas(i))
    for x in lista_haptos:
        Matriz_Respostas = []
        for i in x.Respostas:
            Matriz_Respostas.append(somatorio_alternativas(i))
        for z in lista_final:
            if x.Codigo == z.Codigo:
                z.Nota = corrigir_alternativas(Matriz_Respostas, Matriz_Gabarito) + z.Nota

    
    lista_final = melhoresnotas(lista_final)

    return lista_final


def corrigir_alternativas(resp: list, Gabarito: list) -> float:
    # começa com a nota da alternativa zerada
    nota = 0 
    
    # olha resposta por resposta
    for i in range(0, len(Gabarito)):
        if len(resp[i]) <= len(Gabarito[i]):
            for x in resp[i]:
                if len(Gabarito[i]) == 5:
                    if x in Gabarito[i]:
                        nota += 1.2
                    else:
                        nota = 0
                        break
                elif len(Gabarito[i]) == 4:
                    if x in Gabarito[i]:
                        nota += 1.5
                    else:
                        nota = 0
                        break
                elif len(Gabarito[i]) == 3:
                    if x in Gabarito[i]:
                        nota += 2
                    else:
                        nota = 0
                        break
                elif len(Gabarito[i]) == 2:
                    if x in Gabarito[i]:
                        nota += 3
                    else:
                        nota = 0
                        break
                elif len(Gabarito[i]) == 1:
                    if x in Gabarito[i]:
                        nota += 6  
                            
    return nota


def melhoresnotas(lista: list) -> list:

    Notas = []

    for x in lista:
        Notas.append(x.Nota)
    Notas.sort()
    Notas.reverse()

    for x in range(0, len(Notas)):
        for i in lista:
            if Notas[x] == i.Nota:
                lista.remove(i)
                lista.insert(x, i)
                

    return lista
                



