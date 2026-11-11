"""Análise léxica da Coda usando PLY 3.11."""

import ply.lex as lex


class CodaLexer:
    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Palavras reservadas
    reserved = {
        "program": "PROGRAM",
        "fun": "FUN",
        "int": "INT",
        "bool": "BOOL",
        "if": "IF",
        "else": "ELSE",
        "void": "VOID",
        "while": "WHILE",
        "return": "RETURN",
        "read": "READ",
        "print": "PRINT",
        "true": "TRUE",
        "false": "FALSE",
    }

    # Tokens nomeados
    tokens = (
        "ID", "NUM",
        "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COMMA", "SEMI",
        "ARROW", "ASSIGN", "EQ", "NE", "LT", "LE", "GT", "GE",
        "PLUS", "MINUS", "TIMES", "DIVIDE", "AND", "OR", "NOT",
    ) + tuple(reserved.values())

    # Operadores e delimitadores
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACE = r"\{"
    t_RBRACE = r"\}"
    t_COMMA = r","
    t_SEMI = r";"
    t_ARROW = r"->"
    t_ASSIGN = r"="
    t_EQ = r"=="
    t_NE = r"!="
    t_LT = r"<"
    t_LE = r"<="
    t_GT = r">"
    t_GE = r">="
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_AND = r"&&"
    t_OR = r"\|\|"
    t_NOT = r"!"

    # Espaços e tabulações
    t_ignore = " \t"

    # Comentários: devem ser reconhecidos antes do operador de divisão.
    def t_COMMENT(self, t):
        r"//[^\r\n]*"
        pass

    # Quebras de linha
    def t_newline(self, t):
        r"\r\n|\r|\n"
        t.lexer.lineno += 1

    # Números inteiros; o sinal é reconhecido separadamente.
    def t_NUM(self, t):
        r"[0-9]+"
        t.value = int(t.value)
        return t

    # Identificadores e palavras reservadas
    def t_ID(self, t):
        r"[a-zA-Z][a-zA-Z0-9_]*"
        t.type = self.reserved.get(t.value, "ID")
        return t

    # Erros léxicos
    def t_error(self, t):
        raise ValueError(
            f"Erro léxico na linha {t.lineno}: símbolo inválido {t.value[0]!r}"
        )

    # Entrada do programa-fonte
    def input(self, texto):
        self.lexer.lineno = 1
        self.lexer.input(texto)

    # Retorna o próximo token.
    def token(self):
        return self.lexer.token()
