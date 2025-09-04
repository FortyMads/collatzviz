from __future__ import annotations

import argparse
from pathlib import Path

from .core import collatz_stats_range
from .plotting import plot_range_stats, plot_sequence, plot_transition_graph


def main() -> None:
    p = argparse.ArgumentParser(description="Collatz predictive graphs")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_seq = sub.add_parser("sequence", help="plot a single trajectory")
    p_seq.add_argument("--start", type=int, required=True)
    p_seq.add_argument("--outdir", type=str, default="out")

    p_range = sub.add_parser("range-stats", help="plot range stats and trend line")
    p_range.add_argument("--start", type=int, required=True)
    p_range.add_argument("--end", type=int, required=True)
    p_range.add_argument("--outdir", type=str, default="out")

    p_graph = sub.add_parser("graph", help="plot transition digraph for a range")
    p_graph.add_argument("--start", type=int, required=True)
    p_graph.add_argument("--end", type=int, required=True)
    p_graph.add_argument("--outdir", type=str, default="out")

    args = p.parse_args()

    outdir = Path(args.outdir)

    if args.cmd == "sequence":
        path = plot_sequence(args.start, outdir)
        print(path)
    elif args.cmd == "range-stats":
        stats = collatz_stats_range(args.start, args.end)
        paths = plot_range_stats(stats, outdir)
        for k, v in paths.items():
            print(k, v, sep="\t")
    elif args.cmd == "graph":
        path = plot_transition_graph(args.start, args.end, outdir)
        print(path)


if __name__ == "__main__":
    main()
