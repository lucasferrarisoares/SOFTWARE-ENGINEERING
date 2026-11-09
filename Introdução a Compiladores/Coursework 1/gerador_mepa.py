"""Geração para a MEPA em português fornecida com o trabalho.

Esta etapa suporta programas sem funções, usando globais no nível léxico 0.
Recebe uma AST e tabelas já aprovadas pela análise semântica.
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

    Acrescenta `endereco` aos símbolos globais existentes. Funções ficam para
    a etapa seguinte e produzem um diagnóstico, sem gerar programa parcial.
    """
    if programa.funcoes:
        funcao = programa.funcoes[0]
        raise ValueError(
            f"Erro de geração na linha {funcao.linha}: função {funcao.nome!r} "
            "ainda não suportada na geração MEPA (etapa 05)"
        )
    return _Gerador(tabelas).gerar(programa)


class _Gerador:
    def __init__(self, tabelas):
        self.globais = tabelas["global"]
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
        quantidade = len(programa.globais)
        self._emitir("INPP")
        if quantidade:
            self._emitir("AMEM", quantidade)
        self._comandos(programa.comandos)
        if quantidade:
            self._emitir("DMEM", quantidade)
        self._emitir("PARA")
        self._emitir("FIM")
        return self.codigo

    def _acessar(self, instrucao, nome):
        simbolo = self.globais[nome]
        self._emitir(instrucao, simbolo["nivel"], simbolo["endereco"])

    def _expressao(self, expressao):
        if isinstance(expressao, ast.Inteiro):
            self._emitir("CRCT", expressao.valor)
        elif isinstance(expressao, ast.Booleano):
            self._emitir("CRCT", int(expressao.valor))
        elif isinstance(expressao, ast.Identificador):
            self._acessar("CRVL", expressao.nome)
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
