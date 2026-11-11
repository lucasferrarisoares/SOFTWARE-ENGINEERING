"""Parser LALR da Coda: valida a sintaxe e constrói a AST explícita."""

import ply.yacc as yacc

from lexer import CodaLexer
import nos_ast as ast


class CodaParser:
    tokens = CodaLexer.tokens
    start = "programa"
    precedence = (
        ("left", "OR"),
        ("left", "AND"),
        ("nonassoc", "EQ", "NE"),
        ("nonassoc", "LT", "LE", "GT", "GE"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "UMINUS", "NOT"),
    )

    def __init__(self):
        self._lexer = None
        self.parser = yacc.yacc(module=self, write_tables=False, debug=False)

    # Programa e declarações
    def p_programa(self, p):
        "programa : PROGRAM ID LBRACE declaracoes_variaveis declaracoes_funcoes comandos RBRACE"
        p[0] = ast.Programa(
            nome=p[2],
            globais=p[4],
            funcoes=p[5],
            comandos=p[6],
            linha=p.lineno(1)
        )

    def p_declaracoes_variaveis(self, p):
        """declaracoes_variaveis : declaracoes_variaveis declaracao_variavel
                                 | vazio"""
        if len(p) == 3:
            p[1].append(p[2])
            p[0] = p[1]
        else:
            p[0] = []

    def p_declaracao_variavel(self, p):
        "declaracao_variavel : tipo ID SEMI"
        p[0] = ast.DeclaracaoVariavel(
            nome=p[2],
            tipo=p[1],
            linha=p.lineno(2)
        )

    def p_tipo(self, p):
        """tipo : INT
                | BOOL"""
        p[0] = p[1]

    def p_tipo_retorno(self, p):
        """tipo_retorno : tipo
                        | VOID"""
        p[0] = p[1]

    def p_declaracoes_funcoes(self, p):
        """declaracoes_funcoes : declaracoes_funcoes declaracao_funcao
                              | vazio"""
        if len(p) == 3:
            p[1].append(p[2])
            p[0] = p[1]
        else:
            p[0] = []

    def p_declaracao_funcao(self, p):
        "declaracao_funcao : FUN ID LPAREN parametros_opcionais RPAREN ARROW tipo_retorno LBRACE declaracoes_variaveis comandos RBRACE"
        p[0] = ast.Funcao(
            nome=p[2],
            parametros=p[4],
            tipo_retorno=p[7],
            locais=p[9],
            comandos=p[10],
            linha=p.lineno(1)
        )

    def p_parametros_opcionais(self, p):
        """parametros_opcionais : lista_parametros
                                | vazio"""
        p[0] = p[1] if p[1] is not None else []

    def p_lista_parametros(self, p):
        """lista_parametros : lista_parametros COMMA parametro
                            | parametro"""
        if len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        else:
            p[0] = [p[1]]

    def p_parametro(self, p):
        "parametro : tipo ID"
        p[0] = ast.Parametro(nome=p[2], tipo=p[1], linha=p.lineno(2))

    # Comandos
    def p_comandos(self, p):
        """comandos : comandos comando
                    | vazio"""
        if len(p) == 3:
            p[1].append(p[2])
            p[0] = p[1]
        else:
            p[0] = []

    def p_comando(self, p):
        """comando : atribuicao
                   | condicional
                   | repeticao
                   | retorno
                   | leitura
                   | escrita
                   | chamada_comando"""
        p[0] = p[1]

    def p_atribuicao(self, p):
        "atribuicao : ID ASSIGN expressao SEMI"
        p[0] = ast.Atribuicao(
            destino=ast.Identificador(nome=p[1], linha=p.lineno(1)),
            expressao=p[3],
            linha=p.lineno(1)
        )

    def p_condicional(self, p):
        """condicional : IF LPAREN expressao RPAREN bloco
                       | IF LPAREN expressao RPAREN bloco ELSE bloco"""
        senao = p[7] if len(p) == 8 else None
        p[0] = ast.Condicional(
            condicao=p[3],
            entao=p[5],
            senao=senao,
            linha=p.lineno(1)
        )

    def p_repeticao(self, p):
        "repeticao : WHILE LPAREN expressao RPAREN bloco"
        p[0] = ast.Repeticao(
            condicao=p[3],
            comandos=p[5],
            linha=p.lineno(1)
        )

    def p_bloco(self, p):
        "bloco : LBRACE comandos RBRACE"
        p[0] = p[2]

    def p_retorno(self, p):
        "retorno : RETURN expressao SEMI"
        p[0] = ast.Retorno(expressao=p[2], linha=p.lineno(1))

    def p_leitura(self, p):
        "leitura : READ LPAREN lista_identificadores RPAREN SEMI"
        p[0] = ast.Leitura(identificadores=p[3], linha=p.lineno(1))

    def p_lista_identificadores(self, p):
        """lista_identificadores : lista_identificadores COMMA ID
                                 | ID"""
        if len(p) == 4:
            p[1].append(ast.Identificador(nome=p[3], linha=p.lineno(3)))
            p[0] = p[1]
        else:
            p[0] = [ast.Identificador(nome=p[1], linha=p.lineno(1))]

    def p_escrita(self, p):
        "escrita : PRINT LPAREN lista_expressoes RPAREN SEMI"
        p[0] = ast.Escrita(expressoes=p[3], linha=p.lineno(1))

    def p_lista_expressoes(self, p):
        """lista_expressoes : lista_expressoes COMMA expressao
                            | expressao"""
        if len(p) == 4:
            p[1].append(p[3])
            p[0] = p[1]
        else:
            p[0] = [p[1]]

    def p_chamada_comando(self, p):
        "chamada_comando : chamada SEMI"
        p[0] = ast.ChamadaComando(chamada=p[1], linha=p[1].linha)

    def p_chamada(self, p):
        "chamada : ID LPAREN argumentos_opcionais RPAREN"
        p[0] = ast.Chamada(
            nome=p[1],
            argumentos=p[3],
            linha=p.lineno(1)
        )

    def p_argumentos_opcionais(self, p):
        """argumentos_opcionais : lista_expressoes
                                | vazio"""
        p[0] = p[1] if p[1] is not None else []

    # Expressões
    def p_expressao_binaria(self, p):
        """expressao : expressao PLUS expressao
                     | expressao MINUS expressao
                     | expressao TIMES expressao
                     | expressao DIVIDE expressao
                     | expressao LT expressao
                     | expressao LE expressao
                     | expressao GT expressao
                     | expressao GE expressao
                     | expressao EQ expressao
                     | expressao NE expressao
                     | expressao AND expressao
                     | expressao OR expressao"""
        p[0] = ast.OperacaoBinaria(
            operador=p[2],
            esquerdo=p[1],
            direito=p[3],
            linha=p.lineno(2)
        )

    def p_expressao_unaria(self, p):
        """expressao : MINUS expressao %prec UMINUS
                     | NOT expressao"""
        p[0] = ast.OperacaoUnaria(
            operador=p[1],
            operando=p[2],
            linha=p.lineno(1)
        )

    def p_expressao_parenteses(self, p):
        "expressao : LPAREN expressao RPAREN"
        p[0] = p[2]

    def p_expressao_numero(self, p):
        "expressao : NUM"
        p[0] = ast.Inteiro(valor=p[1], linha=p.lineno(1))

    def p_expressao_booleano(self, p):
        """expressao : TRUE
                     | FALSE"""
        p[0] = ast.Booleano(valor=p[1] == "true", linha=p.lineno(1))

    def p_expressao_identificador(self, p):
        "expressao : ID"
        p[0] = ast.Identificador(nome=p[1], linha=p.lineno(1))

    def p_expressao_chamada(self, p):
        "expressao : chamada"
        p[0] = p[1]

    # Produção vazia
    def p_vazio(self, p):
        "vazio :"
        p[0] = None

    # Erros sintáticos
    def p_error(self, token):
        if token is None:
            linha = self._lexer.lexer.lineno
            raise ValueError(f"Erro sintático na linha {linha}: fim inesperado do arquivo")
        raise ValueError(
            f"Erro sintático na linha {token.lineno}: token inesperado {token.value!r} ({token.type})"
        )

    # Inicia a análise sintática.
    def parse(self, texto, lexer):
        """Devolve Programa ou propaga o primeiro erro léxico/sintático."""
        self._lexer = lexer
        # O PLY chama input(texto), que reinicia a linha no CodaLexer.
        return self.parser.parse(texto, lexer=lexer)
