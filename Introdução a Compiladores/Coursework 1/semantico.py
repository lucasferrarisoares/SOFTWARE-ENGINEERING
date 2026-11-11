"""Validação da AST Coda e construção das tabelas de símbolos."""

import nos_ast as ast
from definicoes import Visitador


def analisar(programa):
    """Devolve as tabelas global e locais, ou lança o primeiro erro semântico.

    Cada chamada cria tabelas novas. A AST não é modificada e as tabelas locais
    continuam disponíveis para a futura geração de código.
    """
    return AnalisadorSemantico().analisar(programa)


def _erro(no, mensagem):
    raise ValueError(f"Erro semântico na linha {no.linha}: {mensagem}")


def _exigir_tipo(no, recebido, esperado, contexto):
    if recebido != esperado:
        _erro(no, f"{contexto}: esperado {esperado}, recebido {recebido}")


def _pode_chegar_ao_fim(comandos):
    """Análise conservadora do fluxo, após verificar tipos de todos os comandos.

    Reconhece condições booleanas literais. Outras condições podem ser
    verdadeiras ou falsas; laços podem executar zero vezes. Não há break
    na Coda, portanto while (true) não chega ao comando seguinte.
    """
    for comando in comandos:
        if isinstance(comando, ast.Retorno):
            return False
        if isinstance(comando, ast.Condicional):
            senao = comando.senao if comando.senao is not None else []
            if isinstance(comando.condicao, ast.Booleano):
                ramo = comando.entao if comando.condicao.valor else senao
                continua = _pode_chegar_ao_fim(ramo)
            else:
                continua = (_pode_chegar_ao_fim(comando.entao)
                            or _pode_chegar_ao_fim(senao))
            if not continua:
                return False
        if isinstance(comando, ast.Repeticao):
            if isinstance(comando.condicao, ast.Booleano) and comando.condicao.valor:
                return False
    return True


class AnalisadorSemantico(Visitador):
    def __init__(self):
        self.global_ = {}
        self.locais = {}
        self.local = {}
        self.funcao = None

    def analisar(self, programa: ast.Programa):
        # Cada análise começa com tabelas e contexto próprios.
        self.global_ = {}
        self.locais = {}
        self.local = {}
        self.funcao = None
        return self.visita(programa)

    def _instalar(self, tabela, declaracao, categoria, nivel, escopo):
        nome = declaracao.nome
        if nome in tabela:
            _erro(declaracao, f"identificador {nome!r} já declarado neste escopo "
                  f"(linha {tabela[nome]['linha']})")
        simbolo = {
            "nome": nome,
            "categoria": categoria,
            "tipo": declaracao.tipo_retorno if categoria == "funcao" else declaracao.tipo,
            "nivel": nivel,
            "escopo": escopo,
            "linha": declaracao.linha,
        }
        if categoria == "funcao":
            simbolo["parametros"] = [parametro.tipo for parametro in declaracao.parametros]
        tabela[nome] = simbolo

    def visita_Programa(self, no: ast.Programa):
        for variavel in no.globais:
            self._instalar(self.global_, variavel, "variavel", 0, "global")
        # Todas as assinaturas ficam visíveis antes da verificação dos corpos.
        for funcao in no.funcoes:
            self._instalar(self.global_, funcao, "funcao", 0, "global")

        for funcao in no.funcoes:
            self.visita(funcao)

        self._comandos(no.comandos)
        return {"global": self.global_, "locais": self.locais}

    def visita_Funcao(self, no: ast.Funcao):
        self.local = {}
        self.locais[no.nome] = self.local
        self.funcao = no
        try:
            for parametro in no.parametros:
                self._instalar(self.local, parametro, "parametro", 1, no.nome)
            for variavel in no.locais:
                self._instalar(self.local, variavel, "variavel", 1, no.nome)
            tem_retorno = self._comandos(no.comandos)
            if no.tipo_retorno != "void" and not tem_retorno:
                _erro(no, f"função {no.nome!r} do tipo {no.tipo_retorno} "
                      "deve possuir pelo menos um return")
            # Convenção adicional escolhida pelo usuário em 09/11/2026.
            if no.tipo_retorno != "void" and _pode_chegar_ao_fim(no.comandos):
                _erro(no, f"função {no.nome!r} pode chegar ao fim sem executar return")
        finally:
            self.local = {}
            self.funcao = None

    # Consulta de símbolos e validação de chamadas
    def _resolver(self, nome, no):
        if nome in self.local:
            return self.local[nome]
        if nome in self.global_:
            return self.global_[nome]
        _erro(no, f"identificador {nome!r} não declarado")

    def visita_Identificador(self, no: ast.Identificador) -> str:
        simbolo = self._resolver(no.nome, no)
        if simbolo["categoria"] not in ("variavel", "parametro"):
            _erro(no, f"{no.nome!r} não é variável nem parâmetro")
        return simbolo["tipo"]

    def _chamada(self, chamada):
        simbolo = self._resolver(chamada.nome, chamada)
        if simbolo["categoria"] != "funcao":
            _erro(chamada, f"{chamada.nome!r} não é função")
        parametros = simbolo["parametros"]
        if len(chamada.argumentos) != len(parametros):
            _erro(chamada, f"chamada de {chamada.nome!r}: esperados {len(parametros)} "
                  f"argumentos, recebidos {len(chamada.argumentos)}")
        for indice, (argumento, esperado) in enumerate(zip(chamada.argumentos, parametros), 1):
            recebido = self.visita(argumento)
            _exigir_tipo(argumento, recebido, esperado,
                         f"argumento {indice} de {chamada.nome!r}")
        return simbolo["tipo"]

    # Expressões: cada visita devolve o tipo resultante.
    def visita_Inteiro(self, no: ast.Inteiro) -> str:
        return "int"

    def visita_Booleano(self, no: ast.Booleano) -> str:
        return "bool"

    def visita_Chamada(self, no: ast.Chamada) -> str:
        tipo = self._chamada(no)
        if tipo == "void":
            _erro(no, f"função void {no.nome!r} não produz valor em expressão")
        return tipo

    def visita_OperacaoUnaria(self, no: ast.OperacaoUnaria) -> str:
        operador = no.operador
        if operador not in ("-", "!"):
            raise TypeError(f"Operador unário desconhecido: {operador!r}")
        esperado = "int" if operador == "-" else "bool"
        recebido = self.visita(no.operando)
        _exigir_tipo(no, recebido, esperado, f"operador {operador!r}")
        return esperado

    def visita_OperacaoBinaria(self, no: ast.OperacaoBinaria) -> str:
        esquerdo = self.visita(no.esquerdo)
        direito = self.visita(no.direito)
        operador = no.operador
        if operador in ("==", "!="):
            _exigir_tipo(no, direito, esquerdo,
                         f"operandos de {operador!r} devem ter o mesmo tipo")
            return "bool"
        if operador in ("+", "-", "*", "/"):
            esperado, resultado = "int", "int"
        elif operador in ("<", "<=", ">", ">="):
            esperado, resultado = "int", "bool"
        elif operador in ("&&", "||"):
            esperado, resultado = "bool", "bool"
        else:
            raise TypeError(f"Operador binário desconhecido: {operador!r}")
        _exigir_tipo(no, esquerdo, esperado, f"operando esquerdo de {operador!r}")
        _exigir_tipo(no, direito, esperado, f"operando direito de {operador!r}")
        return resultado

    # Comandos: True indica a presença de um return válido no comando.
    def _comandos(self, comandos):
        """Verifica todos os comandos e informa se algum contém return válido."""
        tem_retorno = False
        for comando in comandos:
            if self.visita(comando):
                tem_retorno = True
        return tem_retorno

    def visita_Atribuicao(self, no: ast.Atribuicao):
        esperado = self.visita(no.destino)
        recebido = self.visita(no.expressao)
        _exigir_tipo(no, recebido, esperado, f"atribuição a {no.destino.nome!r}")

    def visita_Condicional(self, no: ast.Condicional) -> bool:
        tipo = self.visita(no.condicao)
        _exigir_tipo(no.condicao, tipo, "bool", "condição de if")
        tem_retorno = self._comandos(no.entao)
        if no.senao is not None:
            if self._comandos(no.senao):
                tem_retorno = True
        return tem_retorno

    def visita_Repeticao(self, no: ast.Repeticao) -> bool:
        tipo = self.visita(no.condicao)
        _exigir_tipo(no.condicao, tipo, "bool", "condição de while")
        return self._comandos(no.comandos)

    def visita_Retorno(self, no: ast.Retorno) -> bool:
        if self.funcao is None:
            _erro(no, "return fora de função")
        if self.funcao.tipo_retorno == "void":
            _erro(no, f"função void {self.funcao.nome!r} não permite return")
        recebido = self.visita(no.expressao)
        _exigir_tipo(no, recebido, self.funcao.tipo_retorno,
                     f"return de {self.funcao.nome!r}")
        return True

    def visita_Leitura(self, no: ast.Leitura):
        for identificador in no.identificadores:
            self.visita(identificador)

    def visita_Escrita(self, no: ast.Escrita):
        for expressao in no.expressoes:
            self.visita(expressao)

    def visita_ChamadaComando(self, no: ast.ChamadaComando):
        # Como comando, a chamada também pode ter retorno void.
        self._chamada(no.chamada)
