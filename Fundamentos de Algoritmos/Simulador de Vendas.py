from enum import Enum
from dataclasses import dataclass

class Tipos(Enum):
    CHAPA = 1
    PAINEL = 2
    BOBINA = 3

@dataclass
class Pedido:
    produto: Tipos
    quantidade: int

@dataclass
class Totalizacao:
    chapa: int = 0
    painel: int = 0
    bobina: int = 0

def totaliza_pedidos(pedidos: list[Pedido]) -> Totalizacao:
    '''
    Produz uma estrutura que totaliza a demanda de cada produto a partir de *pedidos*
    >>> totaliza_pedidos([Pedido(Tipos.CHAPA, 70), Pedido(Tipos.CHAPA, 30), Pedido(Tipos.PAINEL, 50)])
    Totalizacao(chapa=100, painel=50, bobina=0)
    >>> totaliza_pedidos([Pedido(Tipos.CHAPA, 20), Pedido(Tipos.BOBINA, 70), Pedido(Tipos.PAINEL, 200)])
    Totalizacao(chapa=20, painel=200, bobina=70)
    '''

    totalizacao = Totalizacao()

    for pedido in pedidos:
        if pedido.produto == Tipos.CHAPA:
            totalizacao.chapa = pedido.quantidade + totalizacao.chapa
        elif pedido.produto == Tipos.PAINEL:
            totalizacao.painel = pedido.quantidade + totalizacao.painel
        elif pedido.produto == Tipos.BOBINA:
            totalizacao.bobina = pedido.quantidade + totalizacao.bobina

    return totalizacao


def ha_ruptura(estoque: Totalizacao, demanda: Totalizacao)  -> list[Tipos]:
    ''' Gera a partir do *estoque* e *demanda*, uma lista com os tipos de produtos com ruptura no estoque.
    >>> ha_ruptura(Totalizacao(chapa=20, painel=200, bobina=70), Totalizacao(chapa=30, painel=150, bobina=50))
    [<Tipos.CHAPA: 1>]
    >>> ha_ruptura(Totalizacao(chapa=20, painel=200, bobina=70), Totalizacao(chapa=10, painel=300, bobina=50))
    [<Tipos.PAINEL: 2>]
    >>> ha_ruptura(Totalizacao(chapa=20, painel=200, bobina=70), Totalizacao(chapa=10, painel=150, bobina=100))
    [<Tipos.BOBINA: 3>]
    '''
    
    ruptura = Totalizacao()
    rupturaprodutos = []

    ruptura.chapa = estoque.chapa - demanda.chapa
    ruptura.painel = estoque.painel - demanda.painel
    ruptura.bobina = estoque.bobina - demanda.bobina

    if ruptura.chapa < 0:
        rupturaprodutos.append(Tipos.CHAPA)
    if ruptura.painel < 0:
        rupturaprodutos.append(Tipos.PAINEL)
    if ruptura.bobina < 0:
        rupturaprodutos.append(Tipos.BOBINA)

    return rupturaprodutos

class Tipos2(Enum):
    PAPEL = 1
    PAPELAO = 2
    PAINEIS = 3

class Vendedores(Enum):
    VENDEDOR1 = 1
    VENDEDOR2 = 2
    VENDEDOR3 = 3
    VENDEDOR4 = 4    

@dataclass
class Vendas:
    vendedor: Vendedores
    produto: Tipos2
    quantidade: int
    valor: float

@dataclass
class Lucro:
    vendedor: Vendedores
    lucro: float

@dataclass
class Financeiro:
    receita: float = 0
    lliquido: float = 0

def lucro(lista: list) -> Financeiro:
    '''Receber uma lista com com as vendas, e devolver a receita e lucro liquido   
    >>> lucro([Vendas(Vendedores.VENDEDOR1, Tipos2.PAINEIS, 200, 90)])
    Financeiro(receita=18000, lliquido=3000)
    >>> lucro([Vendas(Vendedores.VENDEDOR1, Tipos2.PAPEL, 100, 60), Vendas(Vendedores.VENDEDOR1, Tipos2.PAPELAO, 100, 48), Vendas(Vendedores.VENDEDOR3, Tipos2.PAINEIS, 100, 90)])
    Financeiro(receita=19800, lliquido=3300)
    '''

    financeiro = Financeiro()
                

    for vendas in lista:
        financeiro.receita = financeiro.receita + (vendas.valor * vendas.quantidade)
        if vendas.produto == Tipos2.PAPEL:
            financeiro.lliquido = (vendas.quantidade * 50) + financeiro.lliquido
        
        if vendas.produto == Tipos2.PAPELAO:
              financeiro.lliquido = (vendas.quantidade * 40) + financeiro.lliquido
        
        if vendas.produto == Tipos2.PAINEIS:
            financeiro.lliquido  = (vendas.quantidade * 75) + financeiro.lliquido

    financeiro.lliquido = financeiro.receita - financeiro.lliquido

    return financeiro


def vendedor(lista: list) -> list:
    '''Receber uma lista com as vendas do mes, e devolver o top3 dos vendedores que geraram mais lucro para empresa.
    >>> vendedor([Lucro(Vendedores.VENDEDOR1, 10000), Lucro(Vendedores.VENDEDOR2, 20000), Lucro(Vendedores.VENDEDOR3, 9000), Lucro(Vendedores.VENDEDOR4, 15000)])
    [Lucro(vendedor=<Vendedores.VENDEDOR2: 2>, lucro=20000), Lucro(vendedor=<Vendedores.VENDEDOR4: 4>, lucro=15000), Lucro(vendedor=<Vendedores.VENDEDOR1: 1>, lucro=10000), Lucro(vendedor=<Vendedores.VENDEDOR3: 3>, lucro=9000)]
    >>> vendedor([Lucro(Vendedores.VENDEDOR1, 9000), Lucro(Vendedores.VENDEDOR2, 30000), Lucro(Vendedores.VENDEDOR3, 25000), Lucro(Vendedores.VENDEDOR4, 35000)])
    [Lucro(vendedor=<Vendedores.VENDEDOR4: 4>, lucro=35000), Lucro(vendedor=<Vendedores.VENDEDOR2: 2>, lucro=30000), Lucro(vendedor=<Vendedores.VENDEDOR3: 3>, lucro=25000), Lucro(vendedor=<Vendedores.VENDEDOR1: 1>, lucro=9000)]
    '''
    top3vendedores = []  
    top3lucros = [0, 0, 0]  

    for lucro in lista:
        if lucro.lucro > top3lucros[0]:
            top3lucros[2] = top3lucros[1]
            top3lucros[1] = top3lucros[0]
            top3lucros[0] = lucro.lucro
            top3vendedores.insert(0, lucro)
        elif lucro.lucro > top3lucros[1]:
            top3lucros[2] = top3lucros[1]
            top3lucros[1] = lucro.lucro
            top3vendedores.insert(1, lucro)
        elif lucro.lucro > top3lucros[2]:
            top3lucros[2] = lucro.lucro
            top3vendedores.insert(2, lucro)

    return top3vendedores
