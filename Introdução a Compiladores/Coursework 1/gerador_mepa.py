"""Geração para a MEPA em português fornecida com o trabalho.

Globais usam nível 0; parâmetros e locais usam nível 1. Recebe uma AST e
tabelas já aprovadas pela análise semântica.
"""

import nos_ast as ast


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
    return _Gerador(tabelas).gerar(programa)


class _Gerador:
    def __init__(self, tabelas):
        self.globais = tabelas["global"]
        self.locais = tabelas["locais"]
        self.local = {}
        self.funcao = None
        self.codigo = []
        self.proximo_rotulo = 0

    def _emitir(self, instrucao, *argumentos):
        parametros = ",".join(str(argumento) for argumento in argumentos)
        self.codigo.append(instrucao + (" " + parametros if parametros else ""))

    def _rotulo(self):
        rotulo = f"L{self.proximo_rotulo}"
        self.proximo_rotulo += 1
        return rotulo

    def _marcar(self, rotulo):
        self._emitir(f"{rotulo}: NADA")

    def gerar(self, programa):
        for endereco, declaracao in enumerate(programa.globais):
            self.globais[declaracao.nome]["endereco"] = endereco
        # Todos os rótulos existem antes dos corpos, inclusive para recursão mútua.
        for funcao in programa.funcoes:
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
        quantidade = len(programa.globais)
        self._emitir("INPP")
        if quantidade:
            self._emitir("AMEM", quantidade)
        if programa.funcoes:
            principal = self._rotulo()
            self._emitir("DSVS", principal)
            for funcao in programa.funcoes:
                self._gerar_funcao(funcao)
            self._marcar(principal)
        self._comandos(programa.comandos)
        if quantidade:
            self._emitir("DMEM", quantidade)
        self._emitir("PARA")
        self._emitir("FIM")
        return self.codigo

    def _gerar_funcao(self, funcao):
        self.funcao = self.globais[funcao.nome]
        self.local = self.locais[funcao.nome]
        self._marcar(self.funcao["rotulo"])
        self._emitir("ENPR", 1)
        if funcao.locais:
            self._emitir("AMEM", len(funcao.locais))
        self._comandos(funcao.comandos)
        # return desvia para este epílogo; funções void chegam a ele pelo fim
        # do corpo. A semântica rejeita término sem return em funções com valor.
        self._marcar(self.funcao["rotulo_saida"])
        if funcao.locais:
            self._emitir("DMEM", len(funcao.locais))
        self._emitir("RTPR", len(funcao.parametros))
        self.funcao = None
        self.local = {}

    def _resolver(self, nome):
        return self.local[nome] if nome in self.local else self.globais[nome]

    def _acessar(self, instrucao, nome):
        simbolo = self._resolver(nome)
        self._emitir(instrucao, simbolo["nivel"], simbolo["endereco"])

    def _chamada(self, chamada):
        funcao = self._resolver(chamada.nome)
        if funcao["tipo"] != "void":
            self._emitir("AMEM", 1)
        for argumento in chamada.argumentos:
            self._expressao(argumento)
        # CHPR salva três células; ENPR acrescenta a quarta e define D[1].
        # O nível é o da função chamada, pois RTPR restaura D[1] ao retornar.
        self._emitir("CHPR", funcao["rotulo"], 1)

    def _expressao(self, expressao):
        if isinstance(expressao, ast.Inteiro):
            self._emitir("CRCT", expressao.valor)
        elif isinstance(expressao, ast.Booleano):
            self._emitir("CRCT", int(expressao.valor))
        elif isinstance(expressao, ast.Identificador):
            self._acessar("CRVL", expressao.nome)
        elif isinstance(expressao, ast.Chamada):
            self._chamada(expressao)
        elif isinstance(expressao, ast.OperacaoUnaria):
            self._expressao(expressao.operando)
            self._emitir(UNARIOS[expressao.operador])
        elif isinstance(expressao, ast.OperacaoBinaria):
            # Avaliação da esquerda para a direita, seguida da operação nativa.
            self._expressao(expressao.esquerdo)
            self._expressao(expressao.direito)
            self._emitir(BINARIOS[expressao.operador])
        else:
            raise TypeError(f"Expressão não suportada pelo gerador: {type(expressao).__name__}")

    def _comandos(self, comandos):
        for comando in comandos:
            if isinstance(comando, ast.Atribuicao):
                self._expressao(comando.expressao)
                self._acessar("ARMZ", comando.destino.nome)
            elif isinstance(comando, ast.Leitura):
                for identificador in comando.identificadores:
                    self._emitir("LEIT")
                    self._acessar("ARMZ", identificador.nome)
            elif isinstance(comando, ast.Escrita):
                for expressao in comando.expressoes:
                    self._expressao(expressao)
                    self._emitir("IMPR")
            elif isinstance(comando, ast.ChamadaComando):
                self._chamada(comando.chamada)
                if self._resolver(comando.chamada.nome)["tipo"] != "void":
                    self._emitir("DMEM", 1)
            elif isinstance(comando, ast.Retorno):
                self._expressao(comando.expressao)
                self._emitir("ARMZ", 1, self.funcao["endereco_retorno"])
                self._emitir("DSVS", self.funcao["rotulo_saida"])
            elif isinstance(comando, ast.Condicional):
                alternativo = self._rotulo()
                self._expressao(comando.condicao)
                self._emitir("DSVF", alternativo)
                self._comandos(comando.entao)
                if comando.senao is None:
                    self._marcar(alternativo)
                else:
                    fim = self._rotulo()
                    self._emitir("DSVS", fim)
                    self._marcar(alternativo)
                    self._comandos(comando.senao)
                    self._marcar(fim)
            elif isinstance(comando, ast.Repeticao):
                inicio, fim = self._rotulo(), self._rotulo()
                self._marcar(inicio)
                self._expressao(comando.condicao)
                self._emitir("DSVF", fim)
                self._comandos(comando.comandos)
                self._emitir("DSVS", inicio)
                self._marcar(fim)
            else:
                raise TypeError(f"Comando não suportado pelo gerador: {type(comando).__name__}")
