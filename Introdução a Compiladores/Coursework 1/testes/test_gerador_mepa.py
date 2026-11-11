"""Compila Coda e executa o resultado no interpretador MEPA recebido."""

from copy import deepcopy
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from gerador_mepa import gerar
from lexer import CodaLexer
from parser import CodaParser
from semantico import analisar


RAIZ = Path(__file__).resolve().parents[1]


class TestGeradorMepa(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = CodaParser()

    def compilar(self, texto):
        arvore = self.parser.parse(texto, CodaLexer())
        return gerar(arvore, analisar(arvore))

    def executar(self, codigo, entrada="", debug=False):
        with tempfile.TemporaryDirectory() as diretorio:
            arquivo = Path(diretorio) / "programa.mepa"
            arquivo.write_text("\n".join(codigo) + "\n", encoding="utf-8")
            comando = [sys.executable, "-B", str(RAIZ / "mepa/mepa_pt.py"),
                       "--progfile", str(arquivo), "--silent", "--limit", "200000"]
            if debug:
                comando.extend(["--debug", "--stacksize", "32"])
            resultado = subprocess.run(
                comando, input=entrada, capture_output=True, encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                cwd=RAIZ, timeout=15, check=False,
            )
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        # A versão recebida captura SystemExit: status 0, sozinho, não prova sucesso.
        self.assertRegex(resultado.stderr, r"\d+ instruções executadas", resultado.stderr)
        return resultado

    def conferir(self, corpo, esperado, entrada=""):
        codigo = self.compilar(f"program P {{ {corpo} }}")
        resultado = self.executar(codigo, entrada)
        self.assertEqual(resultado.stdout, "".join(f"{valor}\n" for valor in esperado))

    def test_programa_vazio(self):
        codigo = self.compilar("program P {}")
        self.assertEqual(codigo, ["INPP", "PARA", "FIM"])
        self.assertEqual(self.executar(codigo).stdout, "")

    def test_soma_e_laco_sem_iteracoes(self):
        texto = (RAIZ / "testes/validos/soma.coda").read_text(encoding="utf-8")
        for fonte, esperado in ((texto, "6\n"), (texto.replace("n = 3;", "n = 0;"), "0\n")):
            with self.subTest(esperado=esperado):
                self.assertEqual(self.executar(self.compilar(fonte)).stdout, esperado)

    def test_aritmetica_precedencia_e_divisao_da_maquina(self):
        self.conferir("""
            print(2 + 3 * 4, (2 + 3) * 4, 10 - 3 - 2, 8 / 2 * 3);
            print(-2, --2, -(-(-3)), 7 / 3, -7 / 3, 7 / -3, -7 / -3);
        """, [14, 20, 5, 12, -2, 2, -3, 2, -3, -3, 2])

    def test_comparacoes_e_booleanos(self):
        self.conferir("""
            print(true, false, !true, !false, !!!false);
            print(1 < 2, 2 < 1, 2 <= 2, 3 <= 2);
            print(2 > 1, 1 > 2, 2 >= 2, 1 >= 2);
            print(2 == 2, 1 == 2, 1 != 2, 2 != 2);
            print(true == true, true == false, false != true, false != false);
            print(1 < 2 == true, (2 >= 1) == (1 <= 2));
        """, [1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0,
               1, 0, 1, 0, 1, 0, 1, 0, 1, 1])

    def test_operadores_logicos_nativos(self):
        self.conferir("""
            print(false && false, false && true, true && false, true && true);
            print(false || false, false || true, true || false, true || true);
            print(true || false && false, !true && false, !(true || false));
        """, [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0])
        # CONJ/DISJ recebem ambos os valores; não são desvios de curto-circuito.
        for texto, instrucao in (("false && (1 / 0 == 0)", "CONJ"),
                                  ("true || (1 / 0 == 0)", "DISJ")):
            codigo = self.compilar(f"program P {{ print({texto}); }}")
            self.assertIn(instrucao, codigo)
            self.assertLess(codigo.index("DIVI"), codigo.index(instrucao))
            self.assertFalse(any(linha.startswith("DSV") for linha in codigo))

    def test_globais_atribuicoes_e_booleanos_lidos(self):
        corpo = """
            int x;
            bool a;
            bool b;
            read(x, a, b);
            print(x, a, b, !a, !b, a && b, a || b);
            x = x + 2;
            a = x > 0;
            b = a;
            print(x, a, b);
        """
        self.conferir(corpo, [7, 0, 1, 1, 0, 0, 1, 9, 1, 1], "7 0 1\n")
        self.conferir(corpo, [-7, 1, 0, 0, 1, 0, 1, -5, 0, 0], "-7\n1\n0\n")

    def test_condicionais_blocos_vazios_e_lacos_aninhados(self):
        self.conferir("""
            int i;
            int j;
            int total;
            total = 0;
            if (false) { total = 100; }
            if (true) {} else { total = 100; }
            if (false) {} else {}
            while (false) {}
            i = 0;
            while (i < 3) {
                j = 0;
                while (j < 2) {
                    if (i == 1) {
                        if (j == 0) { total = total + 10; }
                        else { total = total + 20; }
                    } else { total = total + 1; }
                    j = j + 1;
                }
                i = i + 1;
            }
            print(total, i, j);
        """, [34, 3, 2])

    def test_equilibrio_da_pilha_na_maquina_real(self):
        texto = """program P {
            int i;
            int total;
            i = 0;
            total = 0;
            while (i < 100) {
                if (i < 50) { total = total + i; }
                else { total = total - 1; }
                i = i + 1;
            }
            print(total);
        }"""
        resultado = self.executar(self.compilar(texto), debug=True)
        self.assertEqual(resultado.stdout, "1175\n")
        # O trace oficial antes de PARA deve mostrar a pilha totalmente liberada.
        self.assertRegex(resultado.stderr, r"s=\s*-1:\s+PARA")
        topos = [int(valor) for valor in re.findall(r"i=\s*\d+, s=\s*(-?\d+):", resultado.stderr)]
        self.assertLessEqual(max(topos), 3)  # Duas globais e até dois operandos.

    def test_tabelas_reutilizadas_e_geracao_repetivel(self):
        arvore = self.parser.parse("program P { int x; bool b; x = 2; b = true; if (b) { print(x); } }", CodaLexer())
        original = deepcopy(arvore)
        tabelas = analisar(arvore)
        simbolo = tabelas["global"]["x"]
        codigo = gerar(arvore, tabelas)
        self.assertIs(tabelas["global"]["x"], simbolo)
        self.assertEqual(simbolo["endereco"], 0)
        self.assertEqual(tabelas["global"]["b"]["endereco"], 1)
        self.assertEqual(arvore, original)
        self.assertEqual(gerar(arvore, tabelas), codigo)
        self.assertEqual(self.executar(codigo).stdout, "2\n")

    def test_funcoes_nao_executam_sem_chamada(self):
        self.conferir("fun f() -> void { print(999); }", [])
        self.conferir("fun f() -> int { print(999); return 1; } print(2);", [2])

    def test_fatorial_e_recursao_recebida(self):
        for caminho in ("testes/validos/fatorial.coda", "testes/coda/ok_08_recursao_fatorial.coda"):
            with self.subTest(caminho=caminho):
                codigo = self.compilar((RAIZ / caminho).read_text(encoding="utf-8"))
                resultado = self.executar(codigo, debug=True)
                self.assertEqual(resultado.stdout, "120\n")
                self.assertRegex(resultado.stderr, r"s=\s*-1:\s+PARA")

    def test_passagem_por_valor_e_descarte_sem_acumulo(self):
        codigo = self.compilar((RAIZ / "testes/validos/parametro_por_valor.coda").read_text(encoding="utf-8"))
        resultado = self.executar(codigo, debug=True)
        self.assertEqual(resultado.stdout, "7\n100\n")
        self.assertRegex(resultado.stderr, r"s=\s*-1:\s+PARA")
        topos = [int(valor) for valor in re.findall(r"i=\s*\d+, s=\s*(-?\d+):", resultado.stderr)]
        self.assertEqual(max(topos), 8)  # Global, retorno, argumento, controle e expressão.

    def test_void_booleano_e_chamadas_sem_argumentos(self):
        self.conferir("""
            int contador;
            fun marcar() -> void { contador = contador + 1; }
            fun verdade() -> bool { return true; }
            fun numero() -> int { return 7; }
            contador = 0;
            marcar(); verdade(); numero(); marcar();
            print(contador, verdade(), numero());
        """, [2, 1, 7])

    def test_ordem_de_argumentos_e_operandos_preservados(self):
        self.conferir("""
            fun identidade(int x) -> int { return x; }
            fun combinar(int a, int b, int c) -> int { return 100 * a + 10 * b + c; }
            print(combinar(1, 2, 3));
            print(10 + combinar(identidade(1), identidade(2), identidade(3)) * identidade(2));
            print(identidade(8) - identidade(3));
        """, [123, 256, 5])

    def test_efeitos_em_globais_e_ordem_de_avaliacao(self):
        self.conferir("""
            int contador;
            fun proximo() -> int { contador = contador + 1; return contador; }
            fun par(int a, int b) -> int { return a * 10 + b; }
            fun marcar() -> bool { contador = contador + 1; return true; }
            contador = 0;
            print(par(proximo(), proximo()));
            print(proximo() - proximo());
            print(false && marcar(), true || marcar(), contador);
        """, [12, -1, 0, 1, 6])

    def test_recursao_com_locais_preservadas(self):
        self.conferir("""
            fun soma(int n) -> int {
                int guardado;
                int subtotal;
                guardado = n;
                if (n == 0) { return 0; }
                subtotal = soma(n - 1);
                return guardado + subtotal;
            }
            print(soma(5), soma(3));
        """, [15, 6])

    def test_recursao_mutua_e_restauracao_entre_funcoes(self):
        self.conferir("""
            fun par(int n) -> bool {
                if (n == 0) { return true; }
                return impar(n - 1);
            }
            fun impar(int n) -> bool {
                if (n == 0) { return false; }
                return par(n - 1);
            }
            fun externa(int x) -> int {
                int local;
                local = 20;
                if (par(x)) { return x + local; }
                return local - x;
            }
            print(par(6), impar(6), par(5), impar(5), externa(4), externa(5));
        """, [1, 0, 0, 1, 24, 15])

    def test_sombreamento_e_leitura_de_parametros_e_locais(self):
        self.conferir("""
            int x;
            fun ler(int x) -> int {
                int y;
                bool b;
                read(x, y, b);
                if (b) { return x + y; }
                return x - y;
            }
            fun outra() -> int { int x; x = 3; return x; }
            x = 100;
            print(ler(x), x, outra(), x);
        """, [9, 100, 3, 100], "7 2 1\n")

    def test_retorno_antecipado_em_laco_e_bloco(self):
        self.conferir("""
            fun buscar(int limite) -> int {
                int i;
                i = 0;
                while (i < limite) {
                    if (i == 2) { return i; }
                    i = i + 1;
                }
                return -1;
                print(999);
            }
            print(buscar(5), buscar(1), buscar(3));
        """, [2, -1, 2])

    def test_retorno_em_condicao_literal_verdadeira(self):
        self.conferir("""
            fun positivo(int n) -> int { if (true) { return n; } }
            print(positivo(7));
        """, [7])

    def test_descarte_de_todos_os_tipos_em_laco(self):
        texto = """program P {
            int i;
            fun v(int x) -> void { int local; local = x; }
            fun b(bool x) -> bool { return !x; }
            fun n(int x) -> int { int local; local = x + 1; return local; }
            i = 0;
            while (i < 100) { v(i); b(true); n(i); i = i + 1; }
            print(i);
        }"""
        resultado = self.executar(self.compilar(texto), debug=True)
        self.assertEqual(resultado.stdout, "100\n")
        self.assertRegex(resultado.stderr, r"s=\s*-1:\s+PARA")
        topos = [int(valor) for valor in re.findall(r"i=\s*\d+, s=\s*(-?\d+):", resultado.stderr)]
        self.assertEqual(max(topos), 9)

    def test_enderecos_rotulos_e_reutilizacao_com_funcoes(self):
        arvore = self.parser.parse("""program P {
            int x;
            fun f(int a, bool b) -> int { int x; x = a; if (b) { return x; } return 0; }
            print(f(7, true));
        }""", CodaLexer())
        original = deepcopy(arvore)
        tabelas = analisar(arvore)
        local = tabelas["locais"]["f"]
        simbolo = tabelas["global"]["f"]
        codigo = gerar(arvore, tabelas)
        self.assertIs(local, tabelas["locais"]["f"])
        self.assertIs(simbolo, tabelas["global"]["f"])
        self.assertEqual([local[nome]["endereco"] for nome in ("a", "b", "x")], [-6, -5, 0])
        self.assertEqual(simbolo["endereco_retorno"], -7)
        self.assertEqual(tabelas["global"]["x"]["endereco"], 0)
        self.assertEqual(arvore, original)
        self.assertEqual(gerar(arvore, tabelas), codigo)
        rotulos = [linha.split(":")[0] for linha in codigo if ":" in linha]
        self.assertEqual(len(rotulos), len(set(rotulos)))
        self.assertEqual(self.executar(codigo).stdout, "7\n")

    def test_casos_recebidos_compativeis_sem_funcoes(self):
        casos = [
            ("ok_03_condicional.coda", "", "9\n"),
            ("ok_05_entrada_saida.coda", "4 1\n", "4\n1\n5\n"),
            ("ok_36_unarios_encadeados.coda", "", "-3\n1\n5\n"),
        ]
        for nome, entrada, esperado in casos:
            with self.subTest(nome=nome):
                texto = (RAIZ / "testes/coda" / nome).read_text(encoding="utf-8")
                self.assertEqual(self.executar(self.compilar(texto), entrada).stdout, esperado)

    def test_fluxo_cli_arquivo_mepa_e_execucao(self):
        with tempfile.TemporaryDirectory() as diretorio:
            destino = Path(diretorio) / "soma.mepa"
            for fonte, esperado in (("soma.coda", "6\n"), ("fatorial.coda", "120\n"),
                                    ("semantica_escopos.coda", "3\n"), ("parser_completo.coda", "28\n")):
                with self.subTest(fonte=fonte):
                    compilacao = subprocess.run(
                        [sys.executable, "-B", str(RAIZ / "main.py"),
                         str(RAIZ / "testes/validos" / fonte), "-o", str(destino)],
                        cwd=RAIZ, capture_output=True, text=True, timeout=15, check=False,
                    )
                    self.assertEqual(compilacao.returncode, 0, compilacao.stderr)
                    self.assertEqual(compilacao.stdout, "")
                    self.assertEqual(compilacao.stderr, "")
                    codigo = destino.read_text(encoding="utf-8").splitlines()
                    self.assertEqual(self.executar(codigo).stdout, esperado)


if __name__ == "__main__":
    unittest.main()
