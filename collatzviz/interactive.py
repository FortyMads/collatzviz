from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from .core import RangeStats, collatz_next, collatz_sequence
from .themes import get_theme


def _ensure_outdir(outdir: str | Path) -> Path:
    p = Path(outdir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def interactive_sequence(start: int, outdir: str | Path = "out", theme: str = "default") -> Path:
    """Create an interactive plotly visualization of a Collatz sequence."""
    theme_obj = get_theme(theme)
    out = _ensure_outdir(outdir)
    
    seq = collatz_sequence(start)
    x = list(range(len(seq)))
    y = seq
    
    colors = [theme_obj.odd if v % 2 else theme_obj.even for v in y]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        line=dict(color=theme_obj.line, width=2),
        marker=dict(color=colors, size=8, line=dict(color=theme_obj.background, width=1)),
        name='Collatz sequence',
        hovertemplate='Step: %{x}<br>Value: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'Collatz Trajectory: {start}',
        xaxis_title='Step',
        yaxis_title='Value',
        template='plotly_dark' if theme_obj.background != '#FFFFFF' else 'plotly',
        height=600,
        hovermode='closest'
    )
    
    fig.update_yaxes(type='log')
    
    path = out / f"interactive_sequence_{start}.html"
    fig.write_html(str(path))
    
    # Also save as PNG
    png_path = out / f"interactive_sequence_{start}.png"
    fig.write_image(str(png_path))
    
    return path


def interactive_range_stats(stats: RangeStats, outdir: str | Path = "out", theme: str = "default") -> Dict[str, Path]:
    """Create interactive plotly visualizations for range statistics."""
    theme_obj = get_theme(theme)
    out = _ensure_outdir(outdir)
    paths: Dict[str, Path] = {}
    
    n = np.array(sorted(stats.stopping_times.keys()))
    st = np.array([stats.stopping_times[i] for i in n])
    tst = np.array([stats.total_stopping_times[i] for i in n])
    peaks = np.array([stats.peaks[i] for i in n])
    
    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Stopping Time vs n', 'Total Stopping Time vs n', 
                       'Peak Values vs n', 'Stopping Time Distribution'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "histogram"}]]
    )
    
    # Stopping time scatter
    fig.add_trace(
        go.Scatter(x=n, y=st, mode='markers', name='Stopping Time',
                  marker=dict(color=theme_obj.line, size=6),
                  hovertemplate='n: %{x}<br>Steps: %{y}<extra></extra>'),
        row=1, col=1
    )
    
    # Add trend line
    x_log = np.log(n)
    if len(n) >= 2:
        a, b = np.polyfit(x_log, st, 1)
        st_fit = a * x_log + b
        fig.add_trace(
            go.Scatter(x=n, y=st_fit, mode='lines', name='Trend',
                      line=dict(color=theme_obj.accent, width=2)),
            row=1, col=1
        )
    
    # Total stopping time scatter
    fig.add_trace(
        go.Scatter(x=n, y=tst, mode='markers', name='Total Stopping Time',
                  marker=dict(color=theme_obj.secondary, size=6),
                  hovertemplate='n: %{x}<br>Steps: %{y}<extra></extra>'),
        row=1, col=2
    )
    
    # Peak values
    fig.add_trace(
        go.Scatter(x=n, y=peaks, mode='markers', name='Peak Values',
                  marker=dict(color=theme_obj.odd, size=6),
                  hovertemplate='n: %{x}<br>Peak: %{y}<extra></extra>'),
        row=2, col=1
    )
    
    # Histogram of stopping times
    fig.add_trace(
        go.Histogram(x=st, name='Distribution', 
                    marker=dict(color=theme_obj.even),
                    hovertemplate='Range: %{x}<br>Count: %{y}<extra></extra>'),
        row=2, col=2
    )
    
    fig.update_layout(
        title=f'Collatz Statistics: {stats.start} to {stats.end}',
        template='plotly_dark' if theme_obj.background != '#FFFFFF' else 'plotly',
        height=800,
        showlegend=True
    )
    
    fig.update_yaxes(type='log', row=2, col=1)
    
    path = out / f"interactive_stats_{stats.start}_{stats.end}.html"
    fig.write_html(str(path))
    
    png_path = out / f"interactive_stats_{stats.start}_{stats.end}.png"
    fig.write_image(str(png_path))
    
    paths["interactive_stats"] = path
    return paths


def interactive_3d_trajectory(start: int, outdir: str | Path = "out", theme: str = "default") -> Path:
    """Create an interactive 3D visualization of Collatz trajectory."""
    theme_obj = get_theme(theme)
    out = _ensure_outdir(outdir)
    
    seq = collatz_sequence(start)
    
    # Create 3D coordinates: (step, value, parity)
    x = list(range(len(seq)))
    y = seq
    z = [1 if v % 2 else 0 for v in seq]  # 1 for odd, 0 for even
    
    colors = [theme_obj.odd if v % 2 else theme_obj.even for v in seq]
    
    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='lines+markers',
        line=dict(color=theme_obj.line, width=4),
        marker=dict(color=colors, size=5),
        name='3D Trajectory',
        hovertemplate='Step: %{x}<br>Value: %{y}<br>Parity: %{z}<extra></extra>'
    )])
    
    fig.update_layout(
        title=f'3D Collatz Trajectory: {start}',
        scene=dict(
            xaxis_title='Step',
            yaxis_title='Value',
            zaxis_title='Parity (0=even, 1=odd)'
        ),
        template='plotly_dark' if theme_obj.background != '#FFFFFF' else 'plotly',
        height=700
    )
    
    path = out / f"interactive_3d_{start}.html"
    fig.write_html(str(path))
    
    png_path = out / f"interactive_3d_{start}.png"
    fig.write_image(str(png_path))
    
    return path
