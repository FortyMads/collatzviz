from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from .core import collatz_sequence
from .themes import get_theme, apply_theme


def _ensure_outdir(outdir: str | Path) -> Path:
    p = Path(outdir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def animate_sequence(
    start: int,
    outdir: str | Path = "out",
    theme: str = "default",
    fps: int = 10,
    interval: int = 200,
) -> Path:
    """Create an animated GIF of a Collatz sequence unfolding."""
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    seq = collatz_sequence(start)
    out = _ensure_outdir(outdir)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_data = []
    y_data = []
    
    line, = ax.plot([], [], color=theme_obj.line, linewidth=2.5, alpha=0.8)
    scatter = ax.scatter([], [], s=50, zorder=5)
    
    ax.set_xlim(0, len(seq))
    ax.set_ylim(1, max(seq) * 1.1)
    ax.set_yscale('log')
    ax.set_title(f"Collatz Trajectory Animation: {start}", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Step", fontsize=11)
    ax.set_ylabel("Value", fontsize=11)
    ax.grid(True, alpha=0.2)
    
    def init():
        line.set_data([], [])
        scatter.set_offsets(np.empty((0, 2)))
        return line, scatter
    
    def update(frame):
        x_data.append(frame)
        y_data.append(seq[frame])
        
        line.set_data(x_data, y_data)
        
        colors = [theme_obj.odd if v % 2 else theme_obj.even for v in y_data]
        scatter.set_offsets(np.column_stack([x_data, y_data]))
        scatter.set_color(colors)
        scatter.set_edgecolors(theme_obj.background)
        scatter.set_linewidths(0.5)
        
        return line, scatter
    
    ani = animation.FuncAnimation(
        fig, update, frames=len(seq),
        init_func=init, blit=True, interval=interval
    )
    
    path = out / f"animation_sequence_{start}_{theme}.gif"
    ani.save(str(path), writer='pillow', fps=fps)
    plt.close(fig)
    
    return path


def animate_convergence(
    start: int,
    outdir: str | Path = "out",
    theme: str = "default",
    fps: int = 10,
    interval: int = 200,
) -> Path:
    """Create an animated visualization showing convergence to 1."""
    theme_obj = get_theme(theme)
    apply_theme(theme_obj)
    
    seq = collatz_sequence(start)
    out = _ensure_outdir(outdir)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left plot: trajectory
    x_data = []
    y_data = []
    line1, = ax1.plot([], [], color=theme_obj.line, linewidth=2.5, alpha=0.8)
    scatter1 = ax1.scatter([], [], s=50, zorder=5)
    
    ax1.set_xlim(0, len(seq))
    ax1.set_ylim(1, max(seq) * 1.1)
    ax1.set_yscale('log')
    ax1.set_title(f"Trajectory", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Step")
    ax1.set_ylabel("Value")
    ax1.grid(True, alpha=0.2)
    
    # Right plot: convergence meter
    max_val = max(seq)
    bar = ax2.bar([0], [seq[0]], color=[theme_obj.odd if seq[0] % 2 else theme_obj.even], width=0.5)
    ax2.set_xlim(-0.5, 0.5)
    ax2.set_ylim(0, max_val * 1.1)
    ax2.set_yscale('log')
    ax2.set_title("Current Value", fontsize=12, fontweight='bold')
    ax2.set_xticks([])
    ax2.grid(True, alpha=0.2)
    
    text = ax2.text(0, max_val, f"Value: {seq[0]}", ha='center', va='top', fontsize=12, fontweight='bold')
    
    def init():
        line1.set_data([], [])
        scatter1.set_offsets(np.empty((0, 2)))
        return line1, scatter1, bar[0], text
    
    def update(frame):
        x_data.append(frame)
        y_data.append(seq[frame])
        
        line1.set_data(x_data, y_data)
        
        colors = [theme_obj.odd if v % 2 else theme_obj.even for v in y_data]
        scatter1.set_offsets(np.column_stack([x_data, y_data]))
        scatter1.set_color(colors)
        scatter1.set_edgecolors(theme_obj.background)
        scatter1.set_linewidths(0.5)
        
        # Update bar
        bar[0].set_height(seq[frame])
        bar[0].set_color(theme_obj.odd if seq[frame] % 2 else theme_obj.even)
        
        # Update text
        text.set_text(f"Value: {seq[frame]}")
        text.set_position((0, seq[frame] * 1.05))
        
        return line1, scatter1, bar[0], text
    
    ani = animation.FuncAnimation(
        fig, update, frames=len(seq),
        init_func=init, blit=False, interval=interval
    )
    
    path = out / f"animation_convergence_{start}_{theme}.gif"
    ani.save(str(path), writer='pillow', fps=fps)
    plt.close(fig)
    
    return path
