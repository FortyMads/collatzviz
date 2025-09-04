from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import matplotlib
# Use non-interactive backend for headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .core import RangeStats, collatz_next, collatz_sequence


COLORS = {
    "odd": "#6C5CE7",
    "even": "#00B894",
    "line": "#0984E3",
    "accent": "#E17055",
}


def _ensure_outdir(outdir: str | Path) -> Path:
    p = Path(outdir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def plot_sequence(start: int, outdir: str | Path = "out", show: bool = False) -> Path:
    seq = collatz_sequence(start)
    out = _ensure_outdir(outdir)
    x = np.arange(len(seq))
    y = np.array(seq)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(x, y, color=COLORS["line"], linewidth=2)
    ax.scatter(x, y, c=[COLORS["odd"] if v % 2 else COLORS["even"] for v in y], s=18)
    ax.set_title(f"Collatz trajectory starting at {start}")
    ax.set_xlabel("step")
    ax.set_ylabel("value")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)

    path = out / f"sequence_{start}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    if show:
        plt.show()
    plt.close(fig)
    return path


def plot_range_stats(stats: RangeStats, outdir: str | Path = "out", show: bool = False) -> Dict[str, Path]:
    out = _ensure_outdir(outdir)
    paths: Dict[str, Path] = {}

    # 1) Stopping time vs n with log fit
    n = np.array(sorted(stats.stopping_times.keys()))
    st = np.array([stats.stopping_times[i] for i in n])
    x = np.log(n)
    if len(n) >= 2:
        a, b = np.polyfit(x, st, 1)
        st_fit = a * x + b
    else:
        a = b = 0.0
        st_fit = st.copy()

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.scatter(n, st, s=10, alpha=0.7, label="stopping time", color=COLORS["line"])
    ax.plot(n, st_fit, color=COLORS["accent"], label=f"fit: a*log(n)+b, a={a:.2f}")
    ax.set_title(f"Stopping time vs n ({stats.start}..{stats.end})")
    ax.set_xlabel("n")
    ax.set_ylabel("steps to < n")
    ax.grid(True, alpha=0.3)
    ax.legend()
    path1 = out / f"stopping_time_{stats.start}_{stats.end}.png"
    fig.tight_layout(); fig.savefig(path1, dpi=160); plt.close(fig)
    paths["stopping_time"] = path1

    # 2) Total stopping time vs n
    tst = np.array([stats.total_stopping_times[i] for i in n])
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.scatter(n, tst, s=10, alpha=0.7, label="total stopping time", color=COLORS["line"])
    ax.set_title(f"Total stopping time vs n ({stats.start}..{stats.end})")
    ax.set_xlabel("n")
    ax.set_ylabel("steps to 1")
    ax.grid(True, alpha=0.3)
    ax.legend()
    path2 = out / f"total_stopping_time_{stats.start}_{stats.end}.png"
    fig.tight_layout(); fig.savefig(path2, dpi=160); plt.close(fig)
    paths["total_stopping_time"] = path2

    # 3) Peak values vs n (log y)
    peaks = np.array([stats.peaks[i] for i in n])
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.scatter(n, peaks, s=10, alpha=0.7, label="peak", color=COLORS["line"])
    ax.set_title(f"Peak value vs n ({stats.start}..{stats.end})")
    ax.set_xlabel("n")
    ax.set_ylabel("peak value")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()
    path3 = out / f"peaks_{stats.start}_{stats.end}.png"
    fig.tight_layout(); fig.savefig(path3, dpi=160); plt.close(fig)
    paths["peaks"] = path3

    return paths


def plot_transition_graph(start: int, end: int, outdir: str | Path = "out", show: bool = False) -> Path:
    if end < start:
        start, end = end, start
    out = _ensure_outdir(outdir)

    # Build directed graph of f(n) for nodes in [start, end]
    G = nx.DiGraph()
    for n in range(start, end + 1):
        m = collatz_next(n)
        G.add_edge(n, m)

    pos = nx.kamada_kawai_layout(G)
    fig, ax = plt.subplots(figsize=(9, 6))
    nx.draw_networkx(
        G,
        pos=pos,
        node_size=120,
        node_color="#D6EAF8",
        edge_color="#5DADE2",
        arrowsize=10,
        with_labels=False,
        ax=ax,
    )
    ax.set_title(f"Collatz directed transition graph ({start}..{end})")
    ax.axis("off")

    path = out / f"graph_{start}_{end}.png"
    fig.tight_layout(); fig.savefig(path, dpi=160)
    if show:
        plt.show()
    plt.close(fig)
    return path
