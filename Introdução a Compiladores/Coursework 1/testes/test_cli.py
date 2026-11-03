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
                    resultado = self.executar("--verificar", arquivo)
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

    def test_modo_de_verificacao_explicito(self):
        resultado = self.executar(RAIZ / "testes/validos/semantica_escopos.coda")
        self.assertEqual(resultado.returncode, 2)
        self.assertEqual(resultado.stdout, "")
        self.assertIn("--verificar", resultado.stderr)


if __name__ == "__main__":
    unittest.main()
