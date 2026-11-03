"""Regras semânticas verificadas a partir de programas Coda completos."""

from copy import deepcopy
from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import unittest

from lexer import CodaLexer
from parser import CodaParser
from semantico import analisar


CASOS = Path(__file__).parent


class TestSemantico(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = CodaParser()

    def arvore(self, texto):
        return self.parser.parse(texto, CodaLexer())

    def analisar_corpo(self, corpo):
        return analisar(self.arvore(f"program P {{ {corpo} }}"))

    def rejeitar(self, corpo, mensagem):
        # A construção da AST precisa passar antes da expectativa de erro semântico.
        programa = self.arvore(f"program P {{ {corpo} }}")
        with self.assertRaisesRegex(ValueError, f"Erro semântico na linha [0-9]+:.*{mensagem}"):
            analisar(programa)

    def test_programa_vazio(self):
        self.assertEqual(self.analisar_corpo(""), {"global": {}, "locais": {}})

    def test_aceitacao_e_atributos_dos_simbolos(self):
        texto = (CASOS / "validos/semantica_escopos.coda").read_text(encoding="utf-8")
        tabelas = analisar(self.arvore(texto))
        self.assertEqual(tabelas, {
            "global": {
                "x": {"nome": "x", "categoria": "variavel", "tipo": "int", "nivel": 0,
                      "escopo": "global", "linha": 2},
                "soma": {"nome": "soma", "categoria": "funcao", "tipo": "int", "nivel": 0,
                         "escopo": "global", "linha": 3, "parametros": ["int", "bool"]},
            },
            "locais": {"soma": {
                "x": {"nome": "x", "categoria": "parametro", "tipo": "int", "nivel": 1,
                      "escopo": "soma", "linha": 3},
                "ok": {"nome": "ok", "categoria": "parametro", "tipo": "bool", "nivel": 1,
                       "escopo": "soma", "linha": 3},
            }},
        })

    def test_tabelas_locais_preservadas_e_sombreamento(self):
        tabelas = self.analisar_corpo("""
            int x;
            fun a(int p) -> int {
                bool x;
                x = true;
                p = p + 1;
                read(p, x);
                if (x) { while (false) { x = false; } }
                return p;
            }
            fun b() -> bool { bool x; x = false; return x; }
            x = a(1);
            print(x, b());
        """)
        self.assertEqual(tabelas["global"]["x"]["tipo"], "int")
        self.assertEqual(tabelas["locais"]["a"]["x"]["tipo"], "bool")
        self.assertEqual(tabelas["locais"]["b"]["x"]["nivel"], 1)
        self.assertEqual(set(tabelas["locais"]["a"]), {"p", "x"})
        self.assertIsNot(tabelas["locais"]["a"], tabelas["locais"]["b"])
        self.assertIsNot(tabelas["locais"]["a"]["x"], tabelas["locais"]["b"]["x"])
        self.analisar_corpo("int x; fun f() -> void { x = 2; } f(); print(x);")

    def test_duplicidades_no_mesmo_escopo(self):
        casos = [
            "int x; bool x;",
            "int f; fun f() -> void {}",
            "fun f() -> void {} fun f() -> int { return 1; }",
            "fun f(int p, bool p) -> void {}",
            "fun f(int p) -> void { int p; }",
            "fun f() -> void { int x; bool x; }",
        ]
        for corpo in casos:
            with self.subTest(corpo=corpo):
                self.rejeitar(corpo, "já declarado neste escopo")

    def test_nomes_nao_declarados_e_escopos_isolados(self):
        casos = [
            "x = 1;", "read(x);", "print(x);", "f();",
            "if (x) {}", "while (x) {}",
            "fun f(int p) -> void {} print(p);",
            "fun f() -> void { int x; } fun g() -> void { print(x); }",
            "fun f() -> int { return x; }",
        ]
        for corpo in casos:
            with self.subTest(corpo=corpo):
                self.rejeitar(corpo, "não declarado")

    def test_categorias_e_funcoes_ocultadas(self):
        for comando in ("f = 1;", "read(f);", "print(f);", "print(f + 1);"):
            with self.subTest(comando=comando):
                self.rejeitar("fun f() -> int { return 1; } " + comando, "não é variável")
        for corpo in (
            "int f; f();",
            "fun f() -> void {} fun g() -> void { int f; f(); }",
            "fun f() -> void {} fun g(int f) -> void { f(); }",
            "fun f(int f) -> int { return f(1); }",
        ):
            with self.subTest(corpo=corpo):
                self.rejeitar(corpo, "não é função")
        # Ocultar uma função é permitido quando o nome é usado como variável.
        self.analisar_corpo("fun f() -> void {} fun g(int f) -> int { f = 2; return f; }")

    def test_operadores_aritmeticos_e_relacionais(self):
        for operador in ("+", "-", "*", "/", "<", "<=", ">", ">="):
            tipo = "int" if operador in ("+", "-", "*", "/") else "bool"
            outro = "bool" if tipo == "int" else "int"
            with self.subTest(operador=operador):
                self.analisar_corpo(f"{tipo} x; x = 6 {operador} 2;")
                self.rejeitar(f"{outro} x; x = 6 {operador} 2;", "atribuição")
                for esquerdo, direito in (("true", "2"), ("2", "false"), ("true", "false")):
                    self.rejeitar(f"print({esquerdo} {operador} {direito});", "esperado int, recebido bool")
        self.analisar_corpo("int x; x = -2; print(-x);")
        self.rejeitar("print(-true);", "esperado int, recebido bool")

    def test_operadores_logicos_e_igualdade(self):
        for operador in ("&&", "||"):
            with self.subTest(operador=operador):
                self.analisar_corpo(f"bool x; x = true {operador} false;")
                self.rejeitar(f"int x; x = true {operador} false;", "atribuição")
                for esquerdo, direito in (("1", "true"), ("false", "0"), ("1", "0")):
                    self.rejeitar(f"print({esquerdo} {operador} {direito});", "esperado bool, recebido int")
        for operador in ("==", "!="):
            with self.subTest(operador=operador):
                self.analisar_corpo(f"bool x; x = 1 {operador} 2; x = true {operador} false;")
                self.rejeitar(f"int x; x = 1 {operador} 2;", "atribuição")
                self.rejeitar(f"print(1 {operador} true);", "mesmo tipo")
                self.rejeitar(f"print(false {operador} 0);", "mesmo tipo")
        self.analisar_corpo("bool x; x = !false; print(!x);")
        self.rejeitar("print(!1);", "esperado bool, recebido int")
        self.rejeitar("print(false && ausente);", "não declarado")
        self.rejeitar("print(true || ausente);", "não declarado")

    def test_atribuicoes_condicoes_e_entrada_saida(self):
        self.analisar_corpo("int x; bool b; read(x, b); x = 1; b = true; if (b) { print(x, b); } while (b) { b = false; }")
        self.rejeitar("int x; x = true;", "esperado int, recebido bool")
        self.rejeitar("bool b; b = 1;", "esperado bool, recebido int")
        for comando in ("if", "while"):
            self.rejeitar(f"{comando} (1) {{}}", f"condição de {comando}")
        self.rejeitar("int x; read(x, ausente);", "não declarado")
        self.rejeitar("print(1, ausente);", "não declarado")

    def test_assinaturas_quantidade_e_ordem(self):
        prefixo = "fun f(int n, bool b) -> bool { return b; } "
        self.analisar_corpo(prefixo + "f(1, true); print(f(2, false));")
        for argumentos in ("", "1", "1, true, false"):
            self.rejeitar(prefixo + f"f({argumentos});", "esperados 2 argumentos")
        self.rejeitar(prefixo + "f(true, 1);", "argumento 1")
        self.rejeitar(prefixo + "f(1, 2);", "argumento 2")
        self.rejeitar(prefixo + "f(1, ausente);", "não declarado")

    def test_recursao_chamadas_antecipadas_e_aninhadas(self):
        self.analisar_corpo("""
            fun fat(int n) -> int {
                if (n <= 1) { return 1; }
                return n * fat(n - 1);
            }
            fun primeira(int n) -> bool { return segunda(n); }
            fun segunda(int n) -> bool {
                if (n == 0) { return true; }
                return primeira(n - 1);
            }
            print(fat(fat(2)), primeira(4));
        """)

    def test_void_em_expressoes_e_retorno_descartado(self):
        prefixo = "fun v() -> void {} fun i() -> int { return 1; } fun b() -> bool { return true; } "
        self.analisar_corpo(prefixo + "v(); i(); b(); print(i(), b());")
        casos = [
            "int x; " + prefixo + "x = v();",
            prefixo + "print(v());",
            prefixo + "print(v() == v());",
            prefixo + "if (v()) {}",
            prefixo + "while (v()) {}",
            prefixo + "print(!v());",
            prefixo + "print(1 + v());",
            prefixo + "fun f(int n) -> void {} f(v());",
            prefixo + "fun f() -> int { return v(); }",
        ]
        for corpo in casos:
            with self.subTest(corpo=corpo):
                self.rejeitar(corpo, "void.*não produz valor")

    def test_retornos_e_caminhos_parciais(self):
        self.analisar_corpo("fun f() -> int { if (false) { return 1; } }")
        self.analisar_corpo("fun f() -> bool { while (false) { return true; } }")
        self.analisar_corpo("fun f() -> bool { if (true) {} else { return false; } }")
        for tipo in ("int", "bool"):
            self.rejeitar(f"fun f() -> {tipo} {{}}", "pelo menos um return")
        for corpo in ("return 1;", "if (true) { return 1; }", "while (true) { return 1; }"):
            self.rejeitar(corpo, "return fora de função")
        self.rejeitar("fun f() -> void { return 1; }", "não permite return")
        self.rejeitar("fun f() -> void { if (true) { return 1; } }", "não permite return")
        self.rejeitar("fun f() -> int { return false; }", "return.*esperado int, recebido bool")
        self.rejeitar("fun f() -> bool { return 1; }", "return.*esperado bool, recebido int")

    def test_verifica_todos_os_comandos_apos_retorno(self):
        corpos = [
            "fun f() -> int { return 1; return false; }",
            "fun f() -> int { if (true) { return 1; } else { return false; } }",
            "fun f() -> int { return 1; if (true) { return false; } }",
            "fun f() -> int { return 1; while (false) { return false; } }",
        ]
        for corpo in corpos:
            with self.subTest(corpo=corpo):
                self.rejeitar(corpo, "esperado int, recebido bool")
        self.rejeitar("fun f() -> int { return 1; print(ausente); }", "não declarado")

    def test_estado_independente_e_ast_preservada(self):
        programa = self.arvore("program P { int x; fun f(int p) -> int { return p; } }")
        original = deepcopy(programa)
        primeira = analisar(programa)
        segunda = analisar(programa)
        self.assertEqual(programa, original)
        self.assertEqual(primeira, segunda)
        primeira["global"]["f"]["parametros"].append("bool")
        primeira["locais"]["f"]["p"]["tipo"] = "bool"
        self.assertEqual(segunda["global"]["f"]["parametros"], ["int"])
        self.assertEqual(segunda["locais"]["f"]["p"]["tipo"], "int")
        self.rejeitar("int x; bool x;", "já declarado")
        self.assertEqual(self.analisar_corpo(""), {"global": {}, "locais": {}})
        self.rejeitar("print(x);", "não declarado")

    def test_diagnostico_com_linha_sem_impressao(self):
        texto = (CASOS / "invalidos/tipo_incompativel.coda").read_text(encoding="utf-8")
        programa = self.arvore(texto)
        saida, erros = io.StringIO(), io.StringIO()
        with redirect_stdout(saida), redirect_stderr(erros):
            with self.assertRaisesRegex(ValueError, "Erro semântico na linha 3: atribuição a 'x'"):
                analisar(programa)
        self.assertEqual(saida.getvalue(), "")
        self.assertEqual(erros.getvalue(), "")

    def test_regressao_dos_programas_validos_anteriores(self):
        for nome in ("lexer_basico.coda", "parser_completo.coda"):
            with self.subTest(nome=nome):
                analisar(self.arvore((CASOS / "validos" / nome).read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
