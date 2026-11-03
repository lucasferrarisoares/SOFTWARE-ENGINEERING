"""Expectativas léxicas extraídas da especificação Coda."""

import io
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import unittest

from lexer import CodaLexer


CASOS = Path(__file__).parent


class TestCodaLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = CodaLexer()

    def tokens(self, texto):
        self.lexer.input(texto)
        return [(t.type, t.value, t.lineno) for t in iter(self.lexer.token, None)]

    def test_programa_completo_e_reinicio_da_linha(self):
        texto = (CASOS / "validos/lexer_basico.coda").read_text(encoding="utf-8")
        esperado = [
            ("PROGRAM", "program", 1), ("ID", "P", 1), ("LBRACE", "{", 1),
            ("INT", "int", 2), ("ID", "Valor_1", 2), ("SEMI", ";", 2),
            ("ID", "Valor_1", 4), ("ASSIGN", "=", 4), ("MINUS", "-", 4),
            ("NUM", 42, 4), ("SEMI", ";", 4),
            ("PRINT", "print", 5), ("LPAREN", "(", 5), ("ID", "Valor_1", 5),
            ("RPAREN", ")", 5), ("SEMI", ";", 5), ("RBRACE", "}", 6),
        ]
        self.assertEqual(self.tokens(texto), esperado)
        self.assertEqual(self.tokens(texto), esperado)

    def test_operadores_e_delimitadores(self):
        pares = [
            ("(", "LPAREN"), (")", "RPAREN"), ("{", "LBRACE"), ("}", "RBRACE"),
            (",", "COMMA"), (";", "SEMI"), ("=", "ASSIGN"), ("==", "EQ"),
            ("!", "NOT"), ("!=", "NE"), ("<", "LT"), ("<=", "LE"),
            (">", "GT"), (">=", "GE"), ("-", "MINUS"), ("->", "ARROW"),
            ("+", "PLUS"), ("*", "TIMES"), ("/", "DIVIDE"),
            ("&&", "AND"), ("||", "OR"),
        ]
        self.assertEqual(
            self.tokens(" ".join(simbolo for simbolo, _ in pares)),
            [(tipo, simbolo, 1) for simbolo, tipo in pares],
        )
        self.assertEqual(self.tokens("a->b!=c&&d<=e||!f"), [
            ("ID", "a", 1), ("ARROW", "->", 1), ("ID", "b", 1),
            ("NE", "!=", 1), ("ID", "c", 1), ("AND", "&&", 1),
            ("ID", "d", 1), ("LE", "<=", 1), ("ID", "e", 1),
            ("OR", "||", 1), ("NOT", "!", 1), ("ID", "f", 1),
        ])

    def test_todas_as_reservadas(self):
        palavras = "program fun int bool if else void while return read print true false"
        tipos = ["PROGRAM", "FUN", "INT", "BOOL", "IF", "ELSE", "VOID",
                 "WHILE", "RETURN", "READ", "PRINT", "TRUE", "FALSE"]
        self.assertEqual(self.tokens(palavras), [
            (tipo, palavra, 1) for tipo, palavra in zip(tipos, palavras.split())
        ])

    def test_identificadores_e_case_sensitive(self):
        self.assertEqual(self.tokens("program Program programador A a Z0 a_b__9"), [
            ("PROGRAM", "program", 1), ("ID", "Program", 1),
            ("ID", "programador", 1), ("ID", "A", 1), ("ID", "a", 1),
            ("ID", "Z0", 1), ("ID", "a_b__9", 1),
        ])

    def test_inteiros_decimais_e_sinal_separado(self):
        self.assertEqual(self.tokens("0 0042 -42 1tempo"), [
            ("NUM", 0, 1), ("NUM", 42, 1), ("MINUS", "-", 1),
            ("NUM", 42, 1), ("NUM", 1, 1), ("ID", "tempo", 1),
        ])

    def test_comentarios_divisao_e_quebras_de_linha(self):
        for quebra in ("\n", "\r\n", "\r"):
            with self.subTest(quebra=repr(quebra)):
                texto = f"// @ é ignorado{quebra}\t8/2// comentário{quebra}{quebra}true// fim"
                self.assertEqual(self.tokens(texto), [
                    ("NUM", 8, 2), ("DIVIDE", "/", 2), ("NUM", 2, 2),
                    ("TRUE", "true", 4),
                ])

    def test_entradas_sem_tokens(self):
        for texto in ("", " \t\r\n", "// comentário no fim"):
            with self.subTest(texto=texto):
                self.assertEqual(self.tokens(texto), [])

    def test_simbolos_invalidos(self):
        for texto, simbolo in (("_nome", "_"), ("10.5", "."), ("@", "@"),
                               ("&", "&"), ("|", "|"), ("ação", "ç"), ("١", "١")):
            with self.subTest(texto=texto):
                with self.assertRaises(ValueError) as erro:
                    self.tokens("\n" + texto)
                self.assertEqual(str(erro.exception),
                                 f"Erro léxico na linha 2: símbolo inválido {simbolo!r}")

    def test_erro_interrompe_sem_imprimir(self):
        texto = (CASOS / "invalidos/caractere_invalido.coda").read_text(encoding="utf-8")
        saida, erros = io.StringIO(), io.StringIO()
        with redirect_stdout(saida), redirect_stderr(erros):
            with self.assertRaisesRegex(ValueError, "linha 2.*'@'"):
                self.tokens(texto)
        self.assertEqual(saida.getvalue(), "")
        self.assertEqual(erros.getvalue(), "")
        # O símbolo inválido não é pulado silenciosamente após a exceção.
        with self.assertRaisesRegex(ValueError, "linha 2.*'@'"):
            self.lexer.token()
        self.assertEqual(self.tokens("int x;"), [
            ("INT", "int", 1), ("ID", "x", 1), ("SEMI", ";", 1),
        ])


if __name__ == "__main__":
    unittest.main()
