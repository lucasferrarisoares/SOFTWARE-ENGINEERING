import argparse
from pathlib import Path


def read_log(path):
    rows = []
    with path.open(encoding="utf-8-sig") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                values = tuple(int(value) for value in line.strip().split(";"))
            except ValueError as error:
                raise ValueError(
                    f"{path}:{line_number}: expected three nonnegative integers."
                ) from error
            if len(values) != 3 or any(value < 0 for value in values):
                raise ValueError(
                    f"{path}:{line_number}: expected three nonnegative integers."
                )
            rows.append(values)
    if not rows:
        raise ValueError(f"{path}: the log is empty.")
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
                      linewidth=1.3, label=f"Server {server}")
        axis.set_title(algorithm)
        axis.set_xlabel("Log event (dispatch or completion)")
        axis.set_ylabel("Pending requests")
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
                        label=f"Server {server}")
        axis.bar_label(bars, padding=3)
    axis.set_xticks(range(3), list(logs))
    axis.set_title("Peak pending requests per server")
    axis.set_ylabel("Maximum observed count")
    axis.set_ylim(0, max(1, max_count) * 1.25)
    axis.yaxis.set_major_locator(MaxNLocator(integer=True))
    axis.grid(axis="y", alpha=0.2)
    axis.set_axisbelow(True)
    axis.legend()
    figure.suptitle(
        f"{title}\nEvent positions are not elapsed time; use the same input for all runs.",
        fontsize=14,
    )
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output, dpi=160)
    finally:
        plt.close(figure)


def main():
    parser = argparse.ArgumentParser(
        description="Compare three load balancing logs generated from the same input."
    )
    parser.add_argument("--rand", type=Path, default=Path("log_rand.txt"))
    parser.add_argument("--rr", type=Path, default=Path("log_rr.txt"))
    parser.add_argument("--lc", type=Path, default=Path("log_lc.txt"))
    parser.add_argument("--output", type=Path, default=Path("comparacao_algoritmos.png"))
    parser.add_argument("--title", default="Load balancing comparison")
    args = parser.parse_args()

    try:
        logs = {
            "Rand": read_log(args.rand),
            "RR": read_log(args.rr),
            "LC": read_log(args.lc),
        }
        create_chart(logs, args.output, args.title)
    except ModuleNotFoundError as error:
        parser.exit(1, f"Missing dependency: {error.name}. "
                    "Run: python -m pip install -r requirements.txt\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Chart saved to {args.output}")


if __name__ == "__main__":
    main()
