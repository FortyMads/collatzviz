#!/usr/bin/env python3
"""
Quick script to generate example visualizations for collatzviz.
Run this to create a gallery of all visualization types.
"""

from pathlib import Path
from collatzviz import (
    plot_sequence,
    plot_range_stats,
    interactive_sequence,
    multi_panel_sequence,
    heatmap_stopping_times,
    plot_spiral,
    plot_radial,
    plot_3d_trajectory,
    plot_fractal_tree,
)
from collatzviz.core import collatz_stats_range


def main():
    outdir = Path("examples")
    outdir.mkdir(exist_ok=True)
    
    print("Generating example visualizations...")
    print(f"Output directory: {outdir}")
    print()
    
    # Basic sequences with different themes
    print("1. Basic sequence plots with different themes...")
    themes = ["default", "dark", "vibrant", "pastel", "ocean", "sunset", "forest"]
    for theme in themes:
        path = plot_sequence(27, outdir=outdir, theme=theme)
        print(f"   Generated: {path.name}")
    
    # Spiral with sunset theme
    print("\n2. Spiral visualization...")
    path = plot_spiral(27, outdir=outdir, theme="sunset")
    print(f"   Generated: {path.name}")
    
    # Multi-panel with pastel
    print("\n3. Multi-panel analysis...")
    path = multi_panel_sequence(27, outdir=outdir, theme="pastel")
    print(f"   Generated: {path.name}")
    
    # Heatmap with forest
    print("\n4. Heatmap visualization...")
    path = heatmap_stopping_times(1, 50, outdir=outdir, theme="forest")
    print(f"   Generated: {path.name}")
    
    # Radial with vibrant
    print("\n5. Radial visualization...")
    path = plot_radial(27, outdir=outdir, theme="vibrant")
    print(f"   Generated: {path.name}")
    
    # 3D with ocean
    print("\n6. 3D trajectory...")
    path = plot_3d_trajectory(27, outdir=outdir, theme="ocean")
    print(f"   Generated: {path.name}")
    
    # Fractal tree with forest
    print("\n7. Fractal tree...")
    path = plot_fractal_tree(27, outdir=outdir, theme="forest", max_depth=8)
    print(f"   Generated: {path.name}")
    
    # Interactive sequence
    print("\n8. Interactive sequence...")
    path = interactive_sequence(27, outdir=outdir, theme="dark")
    print(f"   Generated: {path.name}")
    
    print("\n✅ All examples generated successfully!")
    print(f"   Total files in {outdir}: {len(list(outdir.glob('*')))}")
    print("\nOpen VISUAL_GALLERY.md for descriptions and usage examples.")


if __name__ == "__main__":
    main()
