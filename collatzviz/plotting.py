from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Optional

import matplotlib
# Use non-interactive backend for headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .core import RangeStats, collatz_next, collatz_sequence
from .themes import ColorTheme, get_theme, apply_theme


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


def plot_sequence(start: int, outdir: str | Path = "out", show: bool = False, theme: str = "default") -> Path:
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    seq = collatz_sequence(start)
    out = _ensure_outdir(outdir)
    x = np.arange(len(seq))
    y = np.array(seq)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, color=theme_obj.line, linewidth=2.5, alpha=0.8)
    ax.scatter(x, y, c=[theme_obj.odd if v % 2 else theme_obj.even for v in y], s=25, 
                edgecolors=theme_obj.background, linewidth=0.5, zorder=5)
    ax.set_title(f"Collatz trajectory starting at {start}", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("step", fontsize=11)
    ax.set_ylabel("value", fontsize=11)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.2)

    path = out / f"sequence_{start}_{theme}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=200, facecolor=theme_obj.background)
    if show:
        plt.show()
    plt.close(fig)
    return path


def plot_range_stats(stats: RangeStats, outdir: str | Path = "out", show: bool = False, theme: str = "default") -> Dict[str, Path]:
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
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

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(n, st, s=15, alpha=0.6, label="stopping time", color=theme_obj.line, edgecolors=theme_obj.background)
    ax.plot(n, st_fit, color=theme_obj.accent, linewidth=2.5, label=f"fit: a*log(n)+b, a={a:.2f}")
    ax.set_title(f"Stopping time vs n ({stats.start}..{stats.end})", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("n", fontsize=11)
    ax.set_ylabel("steps to < n", fontsize=11)
    ax.grid(True, alpha=0.2)
    ax.legend(framealpha=0.9)
    path1 = out / f"stopping_time_{stats.start}_{stats.end}_{theme}.png"
    fig.tight_layout(); fig.savefig(path1, dpi=200, facecolor=theme_obj.background); plt.close(fig)
    paths["stopping_time"] = path1

    # 2) Total stopping time vs n
    tst = np.array([stats.total_stopping_times[i] for i in n])
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(n, tst, s=15, alpha=0.6, label="total stopping time", color=theme_obj.line, edgecolors=theme_obj.background)
    ax.set_title(f"Total stopping time vs n ({stats.start}..{stats.end})", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("n", fontsize=11)
    ax.set_ylabel("steps to 1", fontsize=11)
    ax.grid(True, alpha=0.2)
    ax.legend(framealpha=0.9)
    path2 = out / f"total_stopping_time_{stats.start}_{stats.end}_{theme}.png"
    fig.tight_layout(); fig.savefig(path2, dpi=200, facecolor=theme_obj.background); plt.close(fig)
    paths["total_stopping_time"] = path2

    # 3) Peak values vs n (log y)
    peaks = np.array([stats.peaks[i] for i in n])
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(n, peaks, s=15, alpha=0.6, label="peak", color=theme_obj.line, edgecolors=theme_obj.background)
    ax.set_title(f"Peak value vs n ({stats.start}..{stats.end})", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("n", fontsize=11)
    ax.set_ylabel("peak value", fontsize=11)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.2)
    ax.legend(framealpha=0.9)
    path3 = out / f"peaks_{stats.start}_{stats.end}_{theme}.png"
    fig.tight_layout(); fig.savefig(path3, dpi=200, facecolor=theme_obj.background); plt.close(fig)
    paths["peaks"] = path3

    return paths


def plot_transition_graph(start: int, end: int, outdir: str | Path = "out", show: bool = False, theme: str = "default") -> Path:
    if end < start:
        start, end = end, start
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    out = _ensure_outdir(outdir)

    # Build directed graph of f(n) for nodes in [start, end]
    G = nx.DiGraph()
    for n in range(start, end + 1):
        m = collatz_next(n)
        G.add_edge(n, m)

    pos = nx.kamada_kawai_layout(G)
    fig, ax = plt.subplots(figsize=(10, 7))
    nx.draw_networkx(
        G,
        pos=pos,
        node_size=150,
        node_color=theme_obj.secondary,
        edge_color=theme_obj.line,
        arrowsize=12,
        with_labels=False,
        ax=ax,
        edgecolors=theme_obj.background,
    )
    ax.set_title(f"Collatz directed transition graph ({start}..{end})", fontsize=14, fontweight='bold', pad=15)
    ax.axis("off")

    path = out / f"graph_{start}_{end}_{theme}.png"
    fig.tight_layout(); fig.savefig(path, dpi=200, facecolor=theme_obj.background)
    if show:
        plt.show()
    plt.close(fig)
    return path
