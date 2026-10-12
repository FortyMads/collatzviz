from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

from .core import RangeStats, collatz_next, collatz_sequence
from .themes import get_theme, apply_theme


def _ensure_outdir(outdir: str | Path) -> Path:
    p = Path(outdir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def multi_panel_sequence(start: int, outdir: str | Path = "out", theme: str = "default") -> Path:
    """Create a multi-panel figure showing sequence, stopping time, and peak analysis."""
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    seq = collatz_sequence(start)
    out = _ensure_outdir(outdir)
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # Panel 1: Main trajectory
    ax1 = fig.add_subplot(gs[0, :2])
    x = np.arange(len(seq))
    ax1.plot(x, seq, color=theme_obj.line, linewidth=2, alpha=0.8)
    ax1.scatter(x, seq, c=[theme_obj.odd if v % 2 else theme_obj.even for v in seq], 
                s=20, edgecolors=theme_obj.background, linewidth=0.5, zorder=5)
    ax1.set_title(f"Trajectory: {start}", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Step")
    ax1.set_ylabel("Value")
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.2)
    
    # Panel 2: Parity distribution
    ax2 = fig.add_subplot(gs[0, 2])
    odd_count = sum(1 for v in seq if v % 2)
    even_count = len(seq) - odd_count
    ax2.bar(['Odd', 'Even'], [odd_count, even_count], 
            color=[theme_obj.odd, theme_obj.even], edgecolor=theme_obj.background)
    ax2.set_title("Parity Distribution", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Count")
    ax2.grid(True, alpha=0.2, axis='y')
    
    # Panel 3: Value histogram
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.hist(seq, bins=30, color=theme_obj.secondary, edgecolor=theme_obj.background, alpha=0.7)
    ax3.set_title("Value Distribution", fontsize=12, fontweight='bold')
    ax3.set_xlabel("Value")
    ax3.set_ylabel("Frequency")
    ax3.set_xscale('log')
    ax3.grid(True, alpha=0.2, axis='y')
    
    # Panel 4: Step vs Value scatter
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.scatter(x, seq, c=[theme_obj.odd if v % 2 else theme_obj.even for v in seq], 
                s=15, alpha=0.6, edgecolors=theme_obj.background)
    ax4.set_title("Step vs Value", fontsize=12, fontweight='bold')
    ax4.set_xlabel("Step")
    ax4.set_ylabel("Value")
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.2)
    
    # Panel 5: Statistics summary
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.axis('off')
    stats_text = f"""
    Sequence Statistics
    ──────────────────
    Start: {start}
    Length: {len(seq)}
    Max Value: {max(seq)}
    Min Value: {min(seq)}
    Odd Steps: {odd_count}
    Even Steps: {even_count}
    ──────────────────
    """
    ax5.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor=theme_obj.secondary, alpha=0.3))
    
    fig.suptitle(f"Collatz Sequence Analysis: {start}", fontsize=16, fontweight='bold', y=0.98)
    
    path = out / f"multipanel_{start}_{theme}.png"
    fig.savefig(path, dpi=200, facecolor=theme_obj.background, bbox_inches='tight')
    plt.close(fig)
    
    return path


def heatmap_stopping_times(start: int, end: int, outdir: str | Path = "out", theme: str = "default") -> Path:
    """Create a heatmap showing stopping times across a range."""
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    from .core import collatz_stats_range
    stats = collatz_stats_range(start, end)
    out = _ensure_outdir(outdir)
    
    n = np.array(sorted(stats.stopping_times.keys()))
    st = np.array([stats.stopping_times[i] for i in n])
    
    # Reshape for heatmap if we have enough data
    size = int(np.ceil(np.sqrt(len(n))))
    padded_len = size * size
    st_padded = np.pad(st, (0, padded_len - len(st)), constant_values=0)
    st_matrix = st_padded.reshape(size, size)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    cmap = sns.color_palette(f"light:{theme_obj.line}", as_cmap=True)
    sns.heatmap(st_matrix, annot=False, cmap=cmap, cbar_kws={'label': 'Stopping Time'}, ax=ax)
    
    ax.set_title(f"Stopping Time Heatmap: {start} to {end}", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Index (res)")
    ax.set_ylabel("Index (res)")
    
    path = out / f"heatmap_stopping_{start}_{end}_{theme}.png"
    fig.savefig(path, dpi=200, facecolor=theme_obj.background, bbox_inches='tight')
    plt.close(fig)
    
    return path


def heatmap_2d_range(start: int, end: int, outdir: str | Path = "out", theme: str = "default") -> Path:
    """Create a 2D heatmap showing metrics across a range."""
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    from .core import collatz_stats_range
    stats = collatz_stats_range(start, end)
    out = _ensure_outdir(outdir)
    
    n = np.array(sorted(stats.stopping_times.keys()))
    st = np.array([stats.stopping_times[i] for i in n])
    tst = np.array([stats.total_stopping_times[i] for i in n])
    peaks = np.array([stats.peaks[i] for i in n])
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Stopping time heatmap
    size = int(np.ceil(np.sqrt(len(n))))
    padded_len = size * size
    st_padded = np.pad(st, (0, padded_len - len(st)), constant_values=0)
    st_matrix = st_padded.reshape(size, size)
    sns.heatmap(st_matrix, cmap='viridis', ax=axes[0], cbar_kws={'label': 'Stopping Time'})
    axes[0].set_title("Stopping Time", fontweight='bold')
    
    # Total stopping time heatmap
    tst_padded = np.pad(tst, (0, padded_len - len(tst)), constant_values=0)
    tst_matrix = tst_padded.reshape(size, size)
    sns.heatmap(tst_matrix, cmap='plasma', ax=axes[1], cbar_kws={'label': 'Total Stopping Time'})
    axes[1].set_title("Total Stopping Time", fontweight='bold')
    
    # Peak values heatmap
    peaks_padded = np.pad(peaks, (0, padded_len - len(peaks)), constant_values=0)
    peaks_matrix = peaks_padded.reshape(size, size)
    sns.heatmap(peaks_matrix, cmap='magma', ax=axes[2], cbar_kws={'label': 'Peak Value'})
    axes[2].set_title("Peak Values", fontweight='bold')
    
    fig.suptitle(f"Range Heatmaps: {start} to {end}", fontsize=16, fontweight='bold')
    
    path = out / f"heatmap_2d_{start}_{end}_{theme}.png"
    fig.savefig(path, dpi=200, facecolor=theme_obj.background, bbox_inches='tight')
    plt.close(fig)
    
    return path


def plot_3d_trajectory(start: int, outdir: str | Path = "out", theme: str = "default") -> Path:
    """Create a 3D matplotlib visualization of Collatz trajectory."""
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    seq = collatz_sequence(start)
    out = _ensure_outdir(outdir)
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    x = np.arange(len(seq))
    y = np.array(seq)
    z = np.array([np.log(v) if v > 0 else 0 for v in seq])  # Log scale for z
    
    colors = [theme_obj.odd if v % 2 else theme_obj.even for v in seq]
    
    ax.plot(x, y, z, color=theme_obj.line, linewidth=2, alpha=0.8)
    ax.scatter(x, y, z, c=colors, s=30, edgecolors=theme_obj.background, linewidth=0.5)
    
    ax.set_xlabel('Step', fontsize=11)
    ax.set_ylabel('Value', fontsize=11)
    ax.set_zlabel('log(Value)', fontsize=11)
    ax.set_title(f'3D Collatz Trajectory: {start}', fontsize=14, fontweight='bold', pad=20)
    
    ax.set_yscale('log')
    
    path = out / f"3d_trajectory_{start}_{theme}.png"
    fig.savefig(path, dpi=200, facecolor=theme_obj.background, bbox_inches='tight')
    plt.close(fig)
    
    return path


def plot_spiral(start: int, outdir: str | Path = "out", theme: str = "default") -> Path:
    """Create a spiral visualization of the Collatz sequence."""
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    seq = collatz_sequence(start)
    out = _ensure_outdir(outdir)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Convert sequence to spiral coordinates
    theta = np.linspace(0, 4 * np.pi, len(seq))
    r = np.array(seq)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    colors = [theme_obj.odd if v % 2 else theme_obj.even for v in seq]
    
    ax.plot(x, y, color=theme_obj.line, linewidth=1.5, alpha=0.6)
    ax.scatter(x, y, c=colors, s=25, edgecolors=theme_obj.background, linewidth=0.5, zorder=5)
    
    ax.set_title(f"Collatz Spiral: {start}", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True, alpha=0.2)
    
    path = out / f"spiral_{start}_{theme}.png"
    fig.savefig(path, dpi=200, facecolor=theme_obj.background, bbox_inches='tight')
    plt.close(fig)
    
    return path


def plot_fractal_tree(start: int, outdir: str | Path = "out", theme: str = "default", max_depth: int = 8) -> Path:
    """Create a fractal tree based on Collatz sequence branching."""
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    seq = collatz_sequence(start)
    out = _ensure_outdir(outdir)
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    def draw_branch(x, y, angle, length, depth):
        if depth == 0 or length < 1:
            return
        
        x_end = x + length * np.cos(angle)
        y_end = y + length * np.sin(angle)
        
        color = theme_obj.odd if depth % 2 else theme_obj.even
        ax.plot([x, x_end], [y, y_end], color=color, linewidth=max(1, depth/2), alpha=0.8)
        
        # Branch based on Collatz-like rule
        if depth > 1:
            new_length = length * 0.7
            draw_branch(x_end, y_end, angle + np.pi/4, new_length, depth - 1)
            draw_branch(x_end, y_end, angle - np.pi/4, new_length, depth - 1)
    
    # Start from bottom center
    draw_branch(0, 0, np.pi/2, max(seq) / 10, min(max_depth, len(seq)))
    
    ax.set_title(f"Collatz Fractal Tree: {start}", fontsize=14, fontweight='bold', pad=15)
    ax.set_aspect('equal')
    ax.axis('off')
    
    path = out / f"fractal_tree_{start}_{theme}.png"
    fig.savefig(path, dpi=200, facecolor=theme_obj.background, bbox_inches='tight')
    plt.close(fig)
    
    return path


def plot_radial(start: int, outdir: str | Path = "out", theme: str = "default") -> Path:
    """Create a radial/circular visualization of the Collatz sequence."""
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    seq = collatz_sequence(start)
    out = _ensure_outdir(outdir)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Radial plot
    angles = np.linspace(0, 2*np.pi, len(seq))
    radii = np.array(seq)
    
    colors = [theme_obj.odd if v % 2 else theme_obj.even for v in seq]
    
    ax = plt.subplot(111, projection='polar')
    ax.plot(angles, radii, color=theme_obj.line, linewidth=2, alpha=0.8)
    ax.scatter(angles, radii, c=colors, s=30, edgecolors=theme_obj.background, linewidth=0.5, zorder=5)
    
    ax.set_title(f"Radial Collatz: {start}", fontsize=14, fontweight='bold', pad=20, va='bottom')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.2)
    
    path = out / f"radial_{start}_{theme}.png"
    fig.savefig(path, dpi=200, facecolor=theme_obj.background, bbox_inches='tight')
    plt.close(fig)
    
    return path
