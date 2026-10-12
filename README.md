# Collatz Predictive Graphs

A comprehensive Python project to explore and visualize the Collatz conjecture through beautiful, interactive, and animated visualizations.

## What is the Collatz Conjecture?

The Collatz conjecture is one of the most famous unsolved problems in mathematics. It's deceptively simple:

- Start with any positive integer n
- If n is even, divide it by 2
- If n is odd, multiply it by 3 and add 1
- Repeat until you reach 1

The conjecture states that no matter what number you start with, you'll always eventually reach 1. Despite decades of study, no one has proven this definitively, and it remains one of mathematics' most intriguing puzzles.

## Why This Project?

While the Collatz conjecture is simple to state, its behavior is complex and chaotic. This project exists to:

1. **Visualize the complexity** - Turn abstract mathematical sequences into beautiful, intuitive visualizations
2. **Explore patterns** - Use different visualization techniques to reveal hidden patterns in the data
3. **Make mathematics accessible** - Create engaging visuals that help people understand this famous problem
4. **Demonstrate visualization techniques** - Showcase various data visualization methods (from basic plots to 3D, animations, and interactive dashboards)
5. **Enable exploration** - Provide tools for others to explore and discover patterns in Collatz sequences

## Features

## Features

### Core Visualizations
- **Sequence trajectories** - Plot Collatz sequences with colored parity markers
- **Range statistics** - Stopping time, total stopping time, and peak values across ranges
- **Transition graphs** - Directed graphs showing n -> f(n) relationships
- **Trend analysis** - Logarithmic fits to visualize growth patterns

### Enhanced Visualizations
- **7 Color themes** - default, dark, vibrant, pastel, ocean, sunset, forest
- **Interactive plots** - Plotly-based HTML visualizations with zooming and hover
- **Animated GIFs** - Watch Collatz sequences unfold in real-time
- **Multi-panel figures** - Comprehensive analysis in single plots
- **Heatmaps** - Visualize stopping times and metrics across ranges
- **3D visualizations** - Three-dimensional trajectory plots
- **Artistic visualizations** - Spirals, fractal trees, and radial plots

### Technical Features
- Clean Python API (`collatzviz.*`)
- Comprehensive CLI with 15+ commands
- Seaborn-powered modern styling
- High-DPI output (200 DPI)
- Theme-aware backgrounds and colors

## Install

Create a virtual environment (recommended), then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Quick Start

### Basic Plots with Themes

Generate a trajectory plot with the dark theme:

```bash
python -m collatzviz sequence --start 27 --theme dark
```

Range statistics with the vibrant theme:

```bash
python -m collatzviz range-stats --start 1 --end 100 --theme vibrant
```

Transition graph with the ocean theme:

```bash
python -m collatzviz graph --start 1 --end 200 --theme ocean
```

### Interactive Visualizations

Create an interactive sequence plot (opens in browser):

```bash
python -m collatzviz interactive-sequence --start 27 --theme dark
```

Interactive range statistics dashboard:

```bash
python -m collatzviz interactive-stats --start 1 --end 100
```

Interactive 3D trajectory:

```bash
python -m collatzviz interactive-3d --start 27 --theme sunset
```

### Animations

Create an animated GIF of a sequence:

```bash
python -m collatzviz animation --start 27 --theme vibrant --fps 15
```

Animated convergence visualization:

```bash
python -m collatzviz animation-convergence --start 27 --theme forest
```

### Advanced Visualizations

Multi-panel comprehensive analysis:

```bash
python -m collatzviz multipanel --start 27 --theme pastel
```

Stopping time heatmap:

```bash
python -m collatzviz heatmap --start 1 --end 100 --theme dark
```

Multi-metric 2D heatmaps:

```bash
python -m collatzviz heatmap-2d --start 1 --end 100 --theme vibrant
```

3D matplotlib trajectory:

```bash
python -m collatzviz 3d --start 27 --theme ocean
```

Spiral visualization:

```bash
python -m collatzviz spiral --start 27 --theme sunset
```

Fractal tree:

```bash
python -m collatzviz fractal --start 27 --theme forest --max-depth 8
```

Radial/circular plot:

```bash
python -m collatzviz radial --start 27 --theme vibrant
```

## Available Themes

- `default` - Clean light theme with purple/green accents
- `dark` - Dark mode with neon colors
- `vibrant` - Bold, saturated colors
- `pastel` - Soft, muted pastel palette
- `ocean` - Deep blue/green ocean theme
- `sunset` - Warm sunset gradient
- `forest` - Natural green forest theme

## Python API

```python
from collatzviz import (
    plot_sequence,
    plot_range_stats,
    interactive_sequence,
    animate_sequence,
    multi_panel_sequence,
    heatmap_stopping_times,
    plot_spiral,
    get_theme,
)
from collatzviz.core import collatz_sequence, collatz_stats_range

# Basic plot with theme
plot_sequence(27, outdir="out", theme="dark")

# Interactive visualization
interactive_sequence(27, outdir="out", theme="vibrant")

# Animation
animate_sequence(27, outdir="out", theme="ocean", fps=15)

# Advanced visualization
multi_panel_sequence(27, outdir="out", theme="pastel")

# Custom theme usage
theme = get_theme("sunset")
heatmap_stopping_times(1, 100, outdir="out", theme="sunset")
```

## What "predictive" means here

We can't predict Collatz convergence, but we can:
- Compare stopping times across ranges
- Fit simple trend lines vs log(n) to visualize growth tendencies
- Highlight peaks and path shapes for insight
- Use interactive exploration to discover patterns
- Visualize convergence through animations

## Tests

Run the test suite:

```bash
pytest -q
```

## Notes

- For very large ranges, computations and plots can be slow or memory-heavy. Start small.
- The transition graph becomes dense quickly; limit `end - start` to a few hundred.
- Interactive plots generate both HTML and PNG files.
- Animations are saved as GIFs and may take time to generate for long sequences.
- All visualizations support the `--theme` parameter for consistent styling.

## Output

All visualizations are saved to the `out/` directory (or custom `--outdir`). Files are named descriptively:
- `sequence_{start}_{theme}.png`
- `interactive_sequence_{start}.html`
- `animation_sequence_{start}_{theme}.gif`
- `multipanel_{start}_{theme}.png`
- etc.
