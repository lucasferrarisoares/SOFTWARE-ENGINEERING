"""Compare Rand, RR and LC logs produced using the same request input."""

import argparse
from pathlib import Path


class PortugueseHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        super().add_usage(usage, actions, groups, prefix="uso: ")


class PortugueseArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage()
        self.exit(2, "Erro: argumentos inválidos. Confira as opções e seus valores. "
                  "Use --help para consultar a ajuda.\n")


def read_log(path):
    """Read nonnegative A;B;C counts, reporting malformed lines clearly."""
    rows = []
    with path.open(encoding="utf-8-sig") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                values = tuple(int(value) for value in line.strip().split(";"))
            except ValueError as error:
                raise ValueError(
                    f"{path}:{line_number}: informe três números inteiros não negativos."
                ) from error
            if len(values) != 3 or any(value < 0 for value in values):
                raise ValueError(
                    f"{path}:{line_number}: informe três números inteiros não negativos."
                )
            rows.append(values)
    if not rows:
        raise ValueError(f"{path}: o arquivo de log está vazio.")
    return rows


def create_chart(logs, output, title):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    colors = ("#2563eb", "#ea580c", "#16a34a")
    servers = ("A", "B", "C")
    figure, axes = plt.subplots(2, 2, figsize=(14, 9), layout="constrained")
    max_events = max(len(rows) for rows in logs.values())
    max_count = max(max(row) for rows in logs.values() for row in rows)
    peaks = {}

    for axis, (algorithm, rows) in zip(axes.flat, logs.items()):
        events = range(1, len(rows) + 1)
        peaks[algorithm] = []
        for index, (server, color) in enumerate(zip(servers, colors)):
            counts = [row[index] for row in rows]
            peaks[algorithm].append(max(counts))
            axis.step(events, counts, where="post", color=color,
                      linewidth=1.3, label=f"Servidor {server}")
        axis.set_title(algorithm)
        axis.set_xlabel("Evento do log (envio ou conclusão)")
        axis.set_ylabel("Requisições pendentes")
        axis.set_xlim(0, max(2, max_events))
        axis.set_ylim(0, max(1, max_count) * 1.12)
        axis.xaxis.set_major_locator(MaxNLocator(integer=True))
        axis.yaxis.set_major_locator(MaxNLocator(integer=True))
        axis.grid(alpha=0.2)
        axis.legend()

    axis = axes[1, 1]
    width = 0.24
    for index, (server, color) in enumerate(zip(servers, colors)):
        positions = [position + (index - 1) * width for position in range(3)]
        values = [counts[index] for counts in peaks.values()]
        bars = axis.bar(positions, values, width, color=color,
                        label=f"Servidor {server}")
        axis.bar_label(bars, padding=3)
    axis.set_xticks(range(3), list(logs))
    axis.set_title("Pico de requisições pendentes por servidor")
    axis.set_ylabel("Maior contagem observada")
    axis.set_ylim(0, max(1, max_count) * 1.25)
    axis.yaxis.set_major_locator(MaxNLocator(integer=True))
    axis.grid(axis="y", alpha=0.2)
    axis.set_axisbelow(True)
    axis.legend()
    figure.suptitle(
        f"{title}\nO eixo indica a ordem dos eventos; use a mesma entrada nas três execuções.",
        fontsize=14,
    )
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output, dpi=160)
    finally:
        plt.close(figure)


def main():
    parser = PortugueseArgumentParser(
        description="Compara três logs de balanceamento de carga gerados com a mesma entrada.",
        formatter_class=PortugueseHelpFormatter,
        add_help=False,
    )
    options = parser.add_argument_group("Opções")
    options.add_argument("-h", "--help", action="help", help="mostra esta ajuda e encerra")
    options.add_argument("--rand", type=Path, default=Path("log_rand.txt"),
                         metavar="ARQUIVO", help="log Rand (padrão: log_rand.txt)")
    options.add_argument("--rr", type=Path, default=Path("log_rr.txt"),
                         metavar="ARQUIVO", help="log RR (padrão: log_rr.txt)")
    options.add_argument("--lc", type=Path, default=Path("log_lc.txt"),
                         metavar="ARQUIVO", help="log LC (padrão: log_lc.txt)")
    options.add_argument("--output", type=Path, default=Path("comparacao_algoritmos.png"),
                         metavar="ARQUIVO", help="imagem de saída (padrão: comparacao_algoritmos.png)")
    options.add_argument("--title", default="Comparação dos algoritmos de balanceamento de carga",
                         metavar="TÍTULO", help="título do gráfico")
    args = parser.parse_args()

    try:
        logs = {
            "Rand": read_log(args.rand),
            "RR": read_log(args.rr),
            "LC": read_log(args.lc),
        }
        create_chart(logs, args.output, args.title)
    except ModuleNotFoundError as error:
        parser.exit(1, f"Dependência não encontrada: {error.name}. "
                    "Execute: python -m pip install matplotlib\n")
    except OSError as error:
        parser.exit(1, f"Erro ao acessar o arquivo: {error.filename or args.output} "
                    f"(código do sistema: {error.errno}). Confira o caminho e as permissões.\n")
    except ValueError as error:
        parser.exit(1, f"Erro: {error}\n")
    print(f"Gráfico salvo em {args.output}")


if __name__ == "__main__":
    main()
