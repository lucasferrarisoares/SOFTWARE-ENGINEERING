"""Validação estrutural da AST e da gramática Coda, sem executar programas."""

import io
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import unittest

from lexer import CodaLexer
from parser import CodaParser
import nos_ast as ast


class TestCodaParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = CodaParser()

    def setUp(self):
        self.lexer = CodaLexer()

    def parse(self, texto):
        return self.parser.parse(texto, self.lexer)

    def expressao(self, texto):
        return self.parse(f"program P {{ print({texto}); }}").comandos[0].expressoes[0]

    def forma(self, no):
        """Forma compacta para comparar agrupamentos sem omitir operandos."""
        if isinstance(no, ast.OperacaoBinaria):
            return (no.operador, self.forma(no.esquerdo), self.forma(no.direito))
        if isinstance(no, ast.OperacaoUnaria):
            return (no.operador, self.forma(no.operando))
        if isinstance(no, ast.Identificador):
            return no.nome
        return no.valor

    def test_programa_vazio(self):
        self.assertEqual(self.parse("program P {}"), ast.Programa("P", [], [], [], linha=1))

    def test_programa_completo(self):
        texto = (Path(__file__).parent / "validos/parser_completo.coda").read_text(encoding="utf-8")
        raiz = self.parse(texto)
        self.assertEqual((raiz.nome, raiz.linha), ("P", 1))
        self.assertEqual(raiz.globais, [ast.DeclaracaoVariavel("x", "int", linha=2)])
        self.assertEqual(raiz.funcoes, [ast.Funcao(
            "dobro", [ast.Parametro("n", "int", linha=3)], "int", [],
            [ast.Retorno(ast.OperacaoBinaria(
                "*", ast.Identificador("n", linha=4), ast.Inteiro(2, linha=4), linha=4
            ), linha=4)], linha=3,
        )])
        self.assertEqual(raiz.comandos, [
            ast.Atribuicao(ast.Identificador("x", linha=6), ast.Chamada("dobro", [
                ast.OperacaoBinaria("+", ast.Inteiro(2, linha=6),
                    ast.OperacaoBinaria("*", ast.Inteiro(3, linha=6), ast.Inteiro(4, linha=6), linha=6),
                    linha=6)
            ], linha=6), linha=6),
            ast.Condicional(
                ast.OperacaoBinaria(">", ast.Identificador("x", linha=7), ast.Inteiro(0, linha=7), linha=7),
                [ast.Escrita([ast.Identificador("x", linha=7)], linha=7)],
                [ast.Escrita([ast.Inteiro(0, linha=7)], linha=7)], linha=7,
            ),
            ast.Repeticao(
                ast.OperacaoBinaria(">", ast.Identificador("x", linha=8), ast.Inteiro(0, linha=8), linha=8),
                [ast.Atribuicao(ast.Identificador("x", linha=8),
                    ast.OperacaoBinaria("-", ast.Identificador("x", linha=8), ast.Inteiro(1, linha=8), linha=8),
                    linha=8)], linha=8,
            ),
        ])

    def test_precedencia_associatividade_e_parenteses(self):
        casos = {
            "2 + 3 * 4": ("+", 2, ("*", 3, 4)),
            "10 - 3 - 2": ("-", ("-", 10, 3), 2),
            "8 / 2 * 3": ("*", ("/", 8, 2), 3),
            "-2 + 3": ("+", ("-", 2), 3),
            "-2 * 3": ("*", ("-", 2), 3),
            "--2": ("-", ("-", 2)),
            "!!true": ("!", ("!", True)),
            "!-a": ("!", ("-", "a")),
            "!true && false": ("&&", ("!", True), False),
            "true || false && false": ("||", True, ("&&", False, False)),
            "a || b || c": ("||", ("||", "a", "b"), "c"),
            "a && b && c": ("&&", ("&&", "a", "b"), "c"),
            "1 < 2 == true": ("==", ("<", 1, 2), True),
            "a < b + c": ("<", "a", ("+", "b", "c")),
            "a == b && c": ("&&", ("==", "a", "b"), "c"),
            "(2 + 3) * 4": ("*", ("+", 2, 3), 4),
            "1 < (2 < 3)": ("<", 1, ("<", 2, 3)),
            "(true == false) == true": ("==", ("==", True, False), True),
        }
        for texto, esperado in casos.items():
            with self.subTest(texto=texto):
                self.assertEqual(self.forma(self.expressao(texto)), esperado)

    def test_todos_operadores_binarios(self):
        for operador in ("+", "-", "*", "/", "<", "<=", ">", ">=", "==", "!=", "&&", "||"):
            with self.subTest(operador=operador):
                self.assertEqual(self.forma(self.expressao(f"a {operador} b")), (operador, "a", "b"))

    def test_nao_associativos_rejeitam_encadeamento(self):
        for grupo in (("<", "<=", ">", ">="), ("==", "!=")):
            for primeiro in grupo:
                for segundo in grupo:
                    with self.subTest(primeiro=primeiro, segundo=segundo):
                        with self.assertRaisesRegex(ValueError, "Erro sintático"):
                            self.expressao(f"a {primeiro} b {segundo} c")

    def test_funcoes_listas_e_chamadas(self):
        raiz = self.parse("""program P {
  bool ok;
  int x;
  fun nada() -> void {}
  fun escolher(int n, bool b) -> bool {
    int local;
    bool ativo;
    read(local, ativo);
    return b;
  }
  nada();
  print(escolher(2, true), false, nada());
}""")
        self.assertEqual([d.nome for d in raiz.globais], ["ok", "x"])
        self.assertEqual(raiz.funcoes[0], ast.Funcao("nada", [], "void", [], [], linha=4))
        funcao = raiz.funcoes[1]
        self.assertEqual(funcao.parametros, [ast.Parametro("n", "int", linha=5), ast.Parametro("b", "bool", linha=5)])
        self.assertEqual(funcao.locais, [ast.DeclaracaoVariavel("local", "int", linha=6), ast.DeclaracaoVariavel("ativo", "bool", linha=7)])
        self.assertEqual(funcao.tipo_retorno, "bool")
        self.assertEqual(funcao.comandos[0], ast.Leitura([
            ast.Identificador("local", linha=8), ast.Identificador("ativo", linha=8)
        ], linha=8))
        self.assertEqual(funcao.comandos[1], ast.Retorno(ast.Identificador("b", linha=9), linha=9))
        self.assertEqual(raiz.comandos[0], ast.ChamadaComando(ast.Chamada("nada", [], linha=11), linha=11))
        self.assertEqual(raiz.comandos[1], ast.Escrita([
            ast.Chamada("escolher", [ast.Inteiro(2, linha=12), ast.Booleano(True, linha=12)], linha=12),
            ast.Booleano(False, linha=12), ast.Chamada("nada", [], linha=12)
        ], linha=12))
        chamada = self.expressao("f(g(), h(1, 2))")
        self.assertEqual(chamada, ast.Chamada("f", [ast.Chamada("g", [], linha=1),
            ast.Chamada("h", [ast.Inteiro(1, linha=1), ast.Inteiro(2, linha=1)], linha=1)], linha=1))

    def test_blocos_vazios_e_else_aninhado(self):
        raiz = self.parse("program P { if (true) {} if (false) {} else {} while (true) {} }")
        self.assertEqual(raiz.comandos[0], ast.Condicional(ast.Booleano(True, linha=1), [], None, linha=1))
        self.assertEqual(raiz.comandos[1], ast.Condicional(ast.Booleano(False, linha=1), [], [], linha=1))
        self.assertEqual(raiz.comandos[2], ast.Repeticao(ast.Booleano(True, linha=1), [], linha=1))
        externo = self.parse("program P { if (true) { if (false) {} else {} } }").comandos[0]
        self.assertIsNone(externo.senao)
        self.assertEqual(externo.entao[0].senao, [])

    def test_linhas_dos_nos_em_expressao_multilinha(self):
        raiz = self.parse("program P {\r\nprint(\r\n(1\r\n+\r\n-2));\r\n}")
        escrita = raiz.comandos[0]
        soma = escrita.expressoes[0]
        self.assertEqual(escrita.linha, 2)
        self.assertEqual(soma.linha, 4)
        self.assertEqual(soma.esquerdo.linha, 3)
        self.assertEqual(soma.direito.linha, 5)
        self.assertEqual(soma.direito.operando.linha, 5)
        self.assertEqual(self.expressao("((true))"), ast.Booleano(True, linha=1))

    def test_rejeita_construcoes_fora_da_gramatica(self):
        corpos = [
            "read();", "print();", "return;", "int x = 1;", "print(1); int x;",
            "fun f() -> void {} int x;", "fun f() -> void { fun g() -> void {} }",
            "if (true) { int x; }", "while (true) { bool x; }", "{ print(1); }",
            "void x;", "fun f(void x) -> void {}", "fun f() {}", "fun f() -> void { print(1); int x; }",
            "if (true) print(1);", "else {}", "read(1);", "read(x + 1);",
            "print(1,);", "f(,1);", "f(1,);", "fun f(int a,) -> int {}",
            "int a, b;", "x = ;", "x = 1", "print((1);", "1 + 2;",
        ]
        for corpo in corpos:
            with self.subTest(corpo=corpo):
                with self.assertRaisesRegex(ValueError, "Erro sintático"):
                    self.parse(f"program P {{ {corpo} }}")
        for texto in ("P {}", "program {}", "program P {} program Q {}", "program P {} ;"):
            with self.subTest(texto=texto):
                with self.assertRaisesRegex(ValueError, "Erro sintático"):
                    self.parse(texto)

    def test_nao_antecipa_analise_semantica(self):
        raiz = self.parse("""program P {
            int x; int x;
            fun f() -> void { return true; }
            fun g() -> int {}
            x = true;
            if (1) { desconhecida(); }
            print(f());
            return 2;
        }""")
        self.assertIsInstance(raiz, ast.Programa)
        self.assertEqual(len(raiz.comandos), 4)

    def test_erros_com_localizacao_e_sem_impressao(self):
        saida, erros = io.StringIO(), io.StringIO()
        with redirect_stdout(saida), redirect_stderr(erros):
            with self.assertRaisesRegex(ValueError, r"Erro sintático na linha 2:.*';'"):
                self.parse("program P {\nx = ;\n}")
            with self.assertRaisesRegex(ValueError, "Erro sintático na linha 3: fim inesperado"):
                self.parse("program P {\nprint(1);\n")
            with self.assertRaisesRegex(ValueError, "Erro sintático na linha 1: fim inesperado"):
                self.parse("")
            with self.assertRaisesRegex(ValueError, "Erro léxico na linha 2:.*'@'"):
                self.parse("program P {\nprint(@); }")
        self.assertEqual(saida.getvalue(), "")
        self.assertEqual(erros.getvalue(), "")

    def test_reutilizacao_apos_sucesso_e_erros(self):
        anterior = self.parse("program Primeiro {\nprint(1);\n}")
        for invalido in ("program P { print(1)", "program P { print(@); }"):
            with self.assertRaises(ValueError):
                self.parse(invalido)
            self.assertEqual(self.parse("program Novo {}"), ast.Programa("Novo", [], [], [], linha=1))
        novo = self.parse("program Novo { print(false); }")
        self.assertEqual(novo.comandos[0], ast.Escrita([ast.Booleano(False, linha=1)], linha=1))
        self.assertEqual(anterior.comandos[0], ast.Escrita([ast.Inteiro(1, linha=2)], linha=2))


if __name__ == "__main__":
    unittest.main()
