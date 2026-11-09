"""Contrato do processo de verificação: status, stdout e stderr."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


RAIZ = Path(__file__).resolve().parents[1]


class TestCLI(unittest.TestCase):
    def executar(self, *argumentos):
        return subprocess.run(
            [sys.executable, "-B", str(RAIZ / "main.py"), *map(str, argumentos)],
            capture_output=True, text=True, cwd=RAIZ, check=False,
        )

    def test_programa_valido_sem_saida_mepa(self):
        resultado = self.executar("--verificar", RAIZ / "testes/validos/semantica_escopos.coda")
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertEqual(resultado.stdout, "")
        self.assertEqual(resultado.stderr, "")

    def test_erros_das_tres_fases(self):
        casos = [
            ("program P { print(@); }", "Erro léxico"),
            ("program P { print(); }", "Erro sintático"),
            ("program P { int x; x = true; }", "Erro semântico"),
        ]
        with tempfile.TemporaryDirectory() as diretorio:
            arquivo = Path(diretorio) / "programa.coda"
            for texto, fase in casos:
                with self.subTest(fase=fase):
                    arquivo.write_text(texto, encoding="utf-8")
                    for modo in (("--verificar",), ()):
                        resultado = self.executar(*modo, arquivo)
                        self.assertEqual(resultado.returncode, 1)
                        self.assertEqual(resultado.stdout, "")
                        self.assertIn(fase, resultado.stderr)
                        self.assertIn("linha 1", resultado.stderr)
                        self.assertNotIn("Traceback", resultado.stderr)

    def test_arquivo_ausente(self):
        with tempfile.TemporaryDirectory() as diretorio:
            resultado = self.executar("--verificar", Path(diretorio) / "ausente.coda")
        self.assertEqual(resultado.returncode, 1)
        self.assertEqual(resultado.stdout, "")
        self.assertIn("ausente.coda", resultado.stderr)
        self.assertNotIn("Traceback", resultado.stderr)

    def test_arquivo_com_codificacao_invalida(self):
        with tempfile.TemporaryDirectory() as diretorio:
            arquivo = Path(diretorio) / "invalido.coda"
            arquivo.write_bytes(b"\xff")
            resultado = self.executar("--verificar", arquivo)
        self.assertEqual(resultado.returncode, 1)
        self.assertEqual(resultado.stdout, "")
        self.assertTrue(resultado.stderr)
        self.assertNotIn("Traceback", resultado.stderr)

    def test_funcao_ainda_nao_gera_codigo(self):
        resultado = self.executar(RAIZ / "testes/validos/semantica_escopos.coda")
        self.assertEqual(resultado.returncode, 1)
        self.assertEqual(resultado.stdout, "")
        self.assertIn("Erro de geração", resultado.stderr)
        self.assertIn("etapa 05", resultado.stderr)

    def test_compilacao_em_stdout(self):
        resultado = self.executar(RAIZ / "testes/validos/soma.coda")
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertEqual(resultado.stderr, "")
        self.assertTrue(resultado.stdout.startswith("INPP\n"))
        self.assertTrue(resultado.stdout.endswith("PARA\nFIM\n"))

    def test_erro_preserva_arquivo_de_saida(self):
        with tempfile.TemporaryDirectory() as diretorio:
            destino = Path(diretorio) / "programa.mepa"
            destino.write_text("conteúdo anterior", encoding="utf-8")
            for fonte in ("testes/invalidos/tipo_incompativel.coda", "testes/validos/semantica_escopos.coda"):
                resultado = self.executar(RAIZ / fonte, "-o", destino)
                self.assertEqual(resultado.returncode, 1)
                self.assertEqual(resultado.stdout, "")
                self.assertEqual(destino.read_text(encoding="utf-8"), "conteúdo anterior")

    def test_saida_nao_sobrescreve_fonte(self):
        with tempfile.TemporaryDirectory() as diretorio:
            fonte = Path(diretorio) / "programa.coda"
            fonte.write_text("program P {}", encoding="utf-8")
            resultado = self.executar(fonte, "-o", fonte)
            self.assertEqual(resultado.returncode, 1)
            self.assertIn("Erro de saída", resultado.stderr)
            self.assertEqual(resultado.stdout, "")
            self.assertEqual(fonte.read_text(encoding="utf-8"), "program P {}")

    def test_erro_de_escrita_e_opcoes_incompativeis(self):
        with tempfile.TemporaryDirectory() as diretorio:
            resultado = self.executar(RAIZ / "testes/validos/soma.coda", "-o", diretorio)
            self.assertEqual(resultado.returncode, 1)
            self.assertEqual(resultado.stdout, "")
            self.assertTrue(resultado.stderr)
            self.assertNotIn("Traceback", resultado.stderr)
            resultado = self.executar("--verificar", RAIZ / "testes/validos/soma.coda", "-o", diretorio)
            self.assertEqual(resultado.returncode, 2)


if __name__ == "__main__":
    unittest.main()
