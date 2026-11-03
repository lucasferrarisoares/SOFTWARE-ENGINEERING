"""Interface de verificação Coda; geração MEPA ainda não disponível."""

import argparse
from pathlib import Path
import sys

from lexer import CodaLexer
from parser import CodaParser
from semantico import analisar


def main(argv=None):
    argumentos = argparse.ArgumentParser(description="Verifica um programa Coda.")
    argumentos.add_argument("arquivo", type=Path, help="arquivo-fonte Coda em UTF-8")
    argumentos.add_argument(
        "--verificar", action="store_true", required=True,
        help="executa as análises léxica, sintática e semântica, sem gerar MEPA",
    )
    opcoes = argumentos.parse_args(argv)
    try:
        texto = opcoes.arquivo.read_text(encoding="utf-8")
        programa = CodaParser().parse(texto, CodaLexer())
        analisar(programa)
    except (OSError, ValueError) as erro:
        print(erro, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
