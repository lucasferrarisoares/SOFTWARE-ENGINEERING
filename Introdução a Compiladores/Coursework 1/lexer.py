"""Análise léxica da Coda usando PLY 3.11."""

from ply import lex


class CodaLexer:
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

    tokens = (
        "ID", "NUM",
        "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COMMA", "SEMI",
        "ARROW", "ASSIGN", "EQ", "NE", "LT", "LE", "GT", "GE",
        "PLUS", "MINUS", "TIMES", "DIVIDE", "AND", "OR", "NOT",
    ) + tuple(reserved.values())

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

    t_ignore = " \t"

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def input(self, texto):
        self.lexer.lineno = 1
        self.lexer.input(texto)

    def token(self):
        return self.lexer.token()

    def t_COMMENT(self, token):
        r"//[^\r\n]*"
        # Comentários são descartados antes de reconhecer o operador de divisão.
        pass

    def t_newline(self, token):
        r"\r\n|\r|\n"
        token.lexer.lineno += 1

    def t_NUM(self, token):
        r"[0-9]+"
        token.value = int(token.value)
        return token

    def t_ID(self, token):
        r"[a-zA-Z][a-zA-Z0-9_]*"
        token.type = self.reserved.get(token.value, "ID")
        return token

    def t_error(self, token):
        raise ValueError(
            f"Erro léxico na linha {token.lineno}: símbolo inválido {token.value[0]!r}"
        )
