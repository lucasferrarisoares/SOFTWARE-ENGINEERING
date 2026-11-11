"""Validação da AST Coda e construção das tabelas de símbolos."""

import nos_ast as ast


def analisar(programa):
    """Devolve as tabelas global e locais, ou lança o primeiro erro semântico.

    Cada chamada cria tabelas novas. A AST não é modificada e as tabelas locais
    continuam disponíveis para a futura geração de código.
    """
    return _AnaliseSemantica().analisar(programa)


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


class _AnaliseSemantica:
    def __init__(self):
        self.global_ = {}
        self.locais = {}

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

    def analisar(self, programa):
        for variavel in programa.globais:
            self._instalar(self.global_, variavel, "variavel", 0, "global")
        # Todas as assinaturas ficam visíveis antes da verificação dos corpos.
        for funcao in programa.funcoes:
            self._instalar(self.global_, funcao, "funcao", 0, "global")

        for funcao in programa.funcoes:
            local = {}
            self.locais[funcao.nome] = local
            for parametro in funcao.parametros:
                self._instalar(local, parametro, "parametro", 1, funcao.nome)
            for variavel in funcao.locais:
                self._instalar(local, variavel, "variavel", 1, funcao.nome)
            tem_retorno = self._comandos(funcao.comandos, local, funcao)
            if funcao.tipo_retorno != "void" and not tem_retorno:
                _erro(funcao, f"função {funcao.nome!r} do tipo {funcao.tipo_retorno} "
                      "deve possuir pelo menos um return")
            # Convenção adicional escolhida pelo usuário em 09/11/2026.
            if funcao.tipo_retorno != "void" and _pode_chegar_ao_fim(funcao.comandos):
                _erro(funcao, f"função {funcao.nome!r} pode chegar ao fim sem executar return")

        self._comandos(programa.comandos, {}, None)
        return {"global": self.global_, "locais": self.locais}

    def _resolver(self, nome, no, local):
        if nome in local:
            return local[nome]
        if nome in self.global_:
            return self.global_[nome]
        _erro(no, f"identificador {nome!r} não declarado")

    def _variavel(self, identificador, local):
        simbolo = self._resolver(identificador.nome, identificador, local)
        if simbolo["categoria"] not in ("variavel", "parametro"):
            _erro(identificador, f"{identificador.nome!r} não é variável nem parâmetro")
        return simbolo["tipo"]

    def _chamada(self, chamada, local):
        simbolo = self._resolver(chamada.nome, chamada, local)
        if simbolo["categoria"] != "funcao":
            _erro(chamada, f"{chamada.nome!r} não é função")
        parametros = simbolo["parametros"]
        if len(chamada.argumentos) != len(parametros):
            _erro(chamada, f"chamada de {chamada.nome!r}: esperados {len(parametros)} "
                  f"argumentos, recebidos {len(chamada.argumentos)}")
        for indice, (argumento, esperado) in enumerate(zip(chamada.argumentos, parametros), 1):
            recebido = self._expressao(argumento, local)
            _exigir_tipo(argumento, recebido, esperado,
                         f"argumento {indice} de {chamada.nome!r}")
        return simbolo["tipo"]

    def _expressao(self, expressao, local):
        if isinstance(expressao, ast.Inteiro):
            return "int"
        if isinstance(expressao, ast.Booleano):
            return "bool"
        if isinstance(expressao, ast.Identificador):
            return self._variavel(expressao, local)
        if isinstance(expressao, ast.Chamada):
            tipo = self._chamada(expressao, local)
            if tipo == "void":
                _erro(expressao, f"função void {expressao.nome!r} não produz valor em expressão")
            return tipo
        if isinstance(expressao, ast.OperacaoUnaria):
            operador = expressao.operador
            if operador not in ("-", "!"):
                raise TypeError(f"Operador unário desconhecido: {operador!r}")
            esperado = "int" if operador == "-" else "bool"
            recebido = self._expressao(expressao.operando, local)
            _exigir_tipo(expressao, recebido, esperado, f"operador {operador!r}")
            return esperado
        if isinstance(expressao, ast.OperacaoBinaria):
            esquerdo = self._expressao(expressao.esquerdo, local)
            direito = self._expressao(expressao.direito, local)
            operador = expressao.operador
            if operador in ("==", "!="):
                _exigir_tipo(expressao, direito, esquerdo,
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
            _exigir_tipo(expressao, esquerdo, esperado, f"operando esquerdo de {operador!r}")
            _exigir_tipo(expressao, direito, esperado, f"operando direito de {operador!r}")
            return resultado
        raise TypeError(f"Nó de expressão desconhecido: {type(expressao).__name__}")

    def _comandos(self, comandos, local, funcao):
        """Verifica todos os comandos e informa se algum contém return válido."""
        tem_retorno = False
        for comando in comandos:
            if isinstance(comando, ast.Atribuicao):
                esperado = self._variavel(comando.destino, local)
                recebido = self._expressao(comando.expressao, local)
                _exigir_tipo(comando, recebido, esperado,
                             f"atribuição a {comando.destino.nome!r}")
            elif isinstance(comando, ast.Condicional):
                tipo = self._expressao(comando.condicao, local)
                _exigir_tipo(comando.condicao, tipo, "bool", "condição de if")
                if self._comandos(comando.entao, local, funcao):
                    tem_retorno = True
                if comando.senao is not None:
                    if self._comandos(comando.senao, local, funcao):
                        tem_retorno = True
            elif isinstance(comando, ast.Repeticao):
                tipo = self._expressao(comando.condicao, local)
                _exigir_tipo(comando.condicao, tipo, "bool", "condição de while")
                if self._comandos(comando.comandos, local, funcao):
                    tem_retorno = True
            elif isinstance(comando, ast.Retorno):
                if funcao is None:
                    _erro(comando, "return fora de função")
                if funcao.tipo_retorno == "void":
                    _erro(comando, f"função void {funcao.nome!r} não permite return")
                recebido = self._expressao(comando.expressao, local)
                _exigir_tipo(comando, recebido, funcao.tipo_retorno,
                             f"return de {funcao.nome!r}")
                tem_retorno = True
            elif isinstance(comando, ast.Leitura):
                for identificador in comando.identificadores:
                    self._variavel(identificador, local)
            elif isinstance(comando, ast.Escrita):
                for expressao in comando.expressoes:
                    self._expressao(expressao, local)
            elif isinstance(comando, ast.ChamadaComando):
                self._chamada(comando.chamada, local)
            else:
                raise TypeError(f"Nó de comando desconhecido: {type(comando).__name__}")
        return tem_retorno
