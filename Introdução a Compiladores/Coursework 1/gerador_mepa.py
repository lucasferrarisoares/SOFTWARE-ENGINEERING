"""Geração para a MEPA em português fornecida com o trabalho.

Globais usam nível 0; parâmetros e locais usam nível 1. Recebe uma AST e
tabelas já aprovadas pela análise semântica.
"""

import nos_ast as ast
from definicoes import Visitador


BINARIOS = {
    "+": "SOMA", "-": "SUBT", "*": "MULT", "/": "DIVI",
    "<": "CMME", "<=": "CMEG", ">": "CMMA", ">=": "CMAG",
    "==": "CMIG", "!=": "CMDG", "&&": "CONJ", "||": "DISJ",
}
UNARIOS = {"-": "INVR", "!": "NEGA"}


def gerar(programa, tabelas):
    """Devolve instruções completas, sem imprimir ou repetir a semântica.

    Acrescenta endereços e rótulos aos símbolos existentes. As ativações de
    funções são criadas pela MEPA em execução, não pela tabela de símbolos.
    """
    return GeradorMEPA(tabelas).gerar(programa)


class GeradorMEPA(Visitador):
    def __init__(self, tabelas):
        self.globais = tabelas["global"]
        self.locais = tabelas["locais"]
        self.local = {}
        self.funcao = None
        self.codigo = []
        self.proximo_rotulo = 0

    def gerar(self, programa: ast.Programa):
        self.local = {}
        self.funcao = None
        self.codigo = []
        self.proximo_rotulo = 0
        self.visita(programa)
        return self.codigo

    def _emitir(self, instrucao, *argumentos):
        parametros = ",".join(str(argumento) for argumento in argumentos)
        self.codigo.append(instrucao + (" " + parametros if parametros else ""))

    def _rotulo(self):
        rotulo = f"L{self.proximo_rotulo}"
        self.proximo_rotulo += 1
        return rotulo

    def _marcar(self, rotulo):
        self._emitir(f"{rotulo}: NADA")

    # Programa e funções
    def visita_Programa(self, no: ast.Programa):
        for endereco, declaracao in enumerate(no.globais):
            self.globais[declaracao.nome]["endereco"] = endereco
        # Todos os rótulos existem antes dos corpos, inclusive para recursão mútua.
        for funcao in no.funcoes:
            simbolo = self.globais[funcao.nome]
            simbolo["rotulo"] = self._rotulo()
            simbolo["rotulo_saida"] = self._rotulo()
            quantidade_parametros = len(funcao.parametros)
            local = self.locais[funcao.nome]
            for indice, parametro in enumerate(funcao.parametros):
                local[parametro.nome]["endereco"] = indice - quantidade_parametros - 4
            for endereco, variavel in enumerate(funcao.locais):
                local[variavel.nome]["endereco"] = endereco
            if funcao.tipo_retorno != "void":
                simbolo["endereco_retorno"] = -quantidade_parametros - 5
        quantidade = len(no.globais)
        self._emitir("INPP")
        if quantidade:
            self._emitir("AMEM", quantidade)
        if no.funcoes:
            principal = self._rotulo()
            self._emitir("DSVS", principal)
            for funcao in no.funcoes:
                self.visita(funcao)
            self._marcar(principal)
        self._comandos(no.comandos)
        if quantidade:
            self._emitir("DMEM", quantidade)
        self._emitir("PARA")
        self._emitir("FIM")

    def visita_Funcao(self, no: ast.Funcao):
        self.funcao = self.globais[no.nome]
        self.local = self.locais[no.nome]
        self._marcar(self.funcao["rotulo"])
        self._emitir("ENPR", 1)
        if no.locais:
            self._emitir("AMEM", len(no.locais))
        self._comandos(no.comandos)
        # return desvia para este epílogo; funções void chegam a ele pelo fim
        # do corpo. A semântica rejeita término sem return em funções com valor.
        self._marcar(self.funcao["rotulo_saida"])
        if no.locais:
            self._emitir("DMEM", len(no.locais))
        self._emitir("RTPR", len(no.parametros))
        self.funcao = None
        self.local = {}

    # Acesso a símbolos
    def _resolver(self, nome):
        return self.local[nome] if nome in self.local else self.globais[nome]

    def _acessar(self, instrucao, nome):
        simbolo = self._resolver(nome)
        self._emitir(instrucao, simbolo["nivel"], simbolo["endereco"])

    # Expressões: cada visita deixa o resultado na pilha da MEPA.
    def visita_Chamada(self, no: ast.Chamada):
        funcao = self._resolver(no.nome)
        if funcao["tipo"] != "void":
            self._emitir("AMEM", 1)
        for argumento in no.argumentos:
            self.visita(argumento)
        # CHPR salva três células; ENPR acrescenta a quarta e define D[1].
        # O nível é o da função chamada, pois RTPR restaura D[1] ao retornar.
        self._emitir("CHPR", funcao["rotulo"], 1)

    def visita_Inteiro(self, no: ast.Inteiro):
        self._emitir("CRCT", no.valor)

    def visita_Booleano(self, no: ast.Booleano):
        self._emitir("CRCT", int(no.valor))

    def visita_Identificador(self, no: ast.Identificador):
        self._acessar("CRVL", no.nome)

    def visita_OperacaoUnaria(self, no: ast.OperacaoUnaria):
        self.visita(no.operando)
        self._emitir(UNARIOS[no.operador])

    def visita_OperacaoBinaria(self, no: ast.OperacaoBinaria):
        # Avaliação da esquerda para a direita, seguida da operação nativa.
        self.visita(no.esquerdo)
        self.visita(no.direito)
        self._emitir(BINARIOS[no.operador])

    # Comandos
    def _comandos(self, comandos):
        for comando in comandos:
            self.visita(comando)

    def visita_Atribuicao(self, no: ast.Atribuicao):
        self.visita(no.expressao)
        self._acessar("ARMZ", no.destino.nome)

    def visita_Leitura(self, no: ast.Leitura):
        for identificador in no.identificadores:
            self._emitir("LEIT")
            self._acessar("ARMZ", identificador.nome)

    def visita_Escrita(self, no: ast.Escrita):
        for expressao in no.expressoes:
            self.visita(expressao)
            self._emitir("IMPR")

    def visita_ChamadaComando(self, no: ast.ChamadaComando):
        self.visita(no.chamada)
        if self._resolver(no.chamada.nome)["tipo"] != "void":
            self._emitir("DMEM", 1)

    def visita_Retorno(self, no: ast.Retorno):
        self.visita(no.expressao)
        self._emitir("ARMZ", 1, self.funcao["endereco_retorno"])
        self._emitir("DSVS", self.funcao["rotulo_saida"])

    def visita_Condicional(self, no: ast.Condicional):
        alternativo = self._rotulo()
        self.visita(no.condicao)
        self._emitir("DSVF", alternativo)
        self._comandos(no.entao)
        if no.senao is None:
            self._marcar(alternativo)
        else:
            fim = self._rotulo()
            self._emitir("DSVS", fim)
            self._marcar(alternativo)
            self._comandos(no.senao)
            self._marcar(fim)

    def visita_Repeticao(self, no: ast.Repeticao):
        inicio, fim = self._rotulo(), self._rotulo()
        self._marcar(inicio)
        self.visita(no.condicao)
        self._emitir("DSVF", fim)
        self._comandos(no.comandos)
        self._emitir("DSVS", inicio)
        self._marcar(fim)
