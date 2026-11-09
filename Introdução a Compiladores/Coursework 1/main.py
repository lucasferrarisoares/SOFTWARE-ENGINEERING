"""Interface de verificação e compilação Coda para MEPA."""

import argparse
from pathlib import Path
import sys

from lexer import CodaLexer
from parser import CodaParser
from semantico import analisar
from gerador_mepa import gerar


def main(argv=None):
    argumentos = argparse.ArgumentParser(description="Compila um programa Coda para MEPA.")
    argumentos.add_argument("arquivo", type=Path, help="arquivo-fonte Coda em UTF-8")
    modo = argumentos.add_mutually_exclusive_group()
    modo.add_argument(
        "--verificar", action="store_true",
        help="executa as análises léxica, sintática e semântica, sem gerar MEPA",
    )
    modo.add_argument("-o", "--saida", type=Path, help="grava o código MEPA em UTF-8 neste arquivo")
    opcoes = argumentos.parse_args(argv)
    try:
        texto = opcoes.arquivo.read_text(encoding="utf-8")
        programa = CodaParser().parse(texto, CodaLexer())
        tabelas = analisar(programa)
        if not opcoes.verificar:
            codigo = "\n".join(gerar(programa, tabelas)) + "\n"
            if opcoes.saida is not None:
                if opcoes.saida.resolve() == opcoes.arquivo.resolve():
                    raise ValueError("Erro de saída: o destino MEPA deve ser diferente do arquivo-fonte")
                opcoes.saida.write_text(codigo, encoding="utf-8")
            else:
                sys.stdout.write(codigo)
    except (OSError, ValueError) as erro:
        print(erro, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
