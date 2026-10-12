# Visual Gallery

This document showcases the different visualizations available in collatzviz.

## Generated Examples

The following visualizations can be generated in the `examples/` directory using the provided `generate_examples.py` script.

### 1. Basic Sequence Plots (3 Color Themes)

**Dark Theme** - `sequence_27_dark.png`
- Modern dark mode with neon colors
- Purple (odd) and cyan (even) data points
- Professional dark background

**Vibrant Theme** - `sequence_27_vibrant.png`
- Bold, saturated colors
- Purple (odd) and teal (even) data points
- High contrast, eye-catching

**Ocean Theme** - `sequence_27_ocean.png`
- Deep blue/green ocean gradient
- Teal (odd) and light green (even) data points
- Calming, nature-inspired palette

### 2. Spiral Visualization

**Sunset Theme** - `spiral_27_sunset.png`
- Collatz sequence plotted in a spiral pattern
- Warm sunset gradient background
- Shows the sequence in a unique circular form
- Colors indicate odd/even parity

### 3. Multi-Panel Analysis

**Pastel Theme** - `multipanel_27_pastel.png`
- Comprehensive 5-panel analysis including:
  - Main trajectory plot
  - Parity distribution bar chart
  - Value histogram
  - Step vs Value scatter plot
  - Statistics summary text
- Soft, muted pastel colors
- All information in one view

### 4. Heatmap Visualization

**Forest Theme** - `heatmap_stopping_1_50_forest.png`
- Stopping times across range 1-50
- Heatmap visualization showing patterns
- Green forest theme
- Reveals clusters and patterns in stopping times

### 5. Radial Visualization

**Vibrant Theme** - `radial_27_vibrant.png`
- Collatz sequence in polar coordinates
- Circular/radial plot representation
- Shows sequence from center outward
- Logarithmic scale for values

### 6. Interactive Visualization

**Dark Theme** - `interactive_sequence_27.html` and `.png`
- Interactive Plotly visualization
- Can be opened in a web browser
- Features:
  - Zoom and pan
  - Hover tooltips showing step and value
  - Legend toggling
  - Export options
- Static PNG version also generated

## How to View

### Static Images (PNG)
Simply open the PNG files in any image viewer or web browser:
- Windows: Double-click or right-click → Open with
- Mac: Preview app
- Linux: Image viewer or web browser

### Interactive HTML
Open the HTML file in a web browser:
- Chrome, Firefox, Safari, or Edge
- Double-click the file or drag it into your browser
- Interact with zoom, pan, and hover features

## How to Generate More

### Basic Plots with Different Themes
```bash
# Try all 7 themes
python -m collatzviz sequence --start 27 --theme default
python -m collatzviz sequence --start 27 --theme dark
python -m collatzviz sequence --start 27 --theme vibrant
python -m collatzviz sequence --start 27 --theme pastel
python -m collatzviz sequence --start 27 --theme ocean
python -m collatzviz sequence --start 27 --theme sunset
python -m collatzviz sequence --start 27 --theme forest
```

### Different Starting Values
```bash
# Famous Collatz numbers
python -m collatzviz sequence --start 7 --theme dark
python -m collatzviz sequence --start 19 --theme vibrant
python -m collatzviz sequence --start 27 --theme ocean
python -m collatzviz sequence --start 97 --theme sunset
```

### Advanced Visualizations
```bash
# Multi-panel analysis
python -m collatzviz multipanel --start 27 --theme pastel

# Heatmaps
python -m collatzviz heatmap --start 1 --end 100 --theme forest

# Spiral
python -m collatzviz spiral --start 27 --theme sunset

# Radial
python -m collatzviz radial --start 27 --theme vibrant

# 3D
python -m collatzviz 3d --start 27 --theme ocean

# Fractal tree
python -m collatzviz fractal --start 27 --theme forest --max-depth 8
```

### Interactive Plots
```bash
# Interactive sequence
python -m collatzviz interactive-sequence --start 27 --theme dark

# Interactive range stats
python -m collatzviz interactive-stats --start 1 --end 100

# Interactive 3D
python -m collatzviz interactive-3d --start 27 --theme sunset
```

### Animations
```bash
# Animated sequence
python -m collatzviz animation --start 27 --theme vibrant --fps 15

# Animated convergence
python -m collatzviz animation-convergence --start 27 --theme forest
```

## Visualization Types Summary

| Type | Command | Description | Output |
|------|---------|-------------|--------|
| Basic Sequence | `sequence` | Line plot with colored markers | PNG |
| Range Stats | `range-stats` | Multiple statistics plots | Multiple PNGs |
| Transition Graph | `graph` | Directed graph visualization | PNG |
| Interactive Sequence | `interactive-sequence` | Zoomable, hoverable plot | HTML + PNG |
| Interactive Stats | `interactive-stats` | Multi-panel dashboard | HTML + PNG |
| Interactive 3D | `interactive-3d` | 3D trajectory exploration | HTML + PNG |
| Animation | `animation` | Animated GIF sequence | GIF |
| Animation Convergence | `animation-convergence` | Dual-panel animation | GIF |
| Multi-Panel | `multipanel` | 5-panel comprehensive analysis | PNG |
| Heatmap | `heatmap` | Stopping time heatmap | PNG |
| Heatmap 2D | `heatmap-2d` | Multi-metric heatmaps | PNG |
| 3D Trajectory | `3d` | Matplotlib 3D plot | PNG |
| Spiral | `spiral` | Spiral visualization | PNG |
| Fractal Tree | `fractal` | Fractal tree art | PNG |
| Radial | `radial` | Circular/radial plot | PNG |

## Theme Reference

All visualizations support the `--theme` parameter:

- **default** - Clean light theme with purple/green accents
- **dark** - Dark mode with neon colors
- **vibrant** - Bold, saturated colors
- **pastel** - Soft, muted pastel palette
- **ocean** - Deep blue/green ocean theme
- **sunset** - Warm sunset gradient
- **forest** - Natural green forest theme

## Tips for Best Results

1. **For presentations**: Use `vibrant` or `dark` themes for high contrast
2. **For reports**: Use `default` or `pastel` for professional appearance
3. **For artistic**: Use `ocean`, `sunset`, or `forest` for unique aesthetics
4. **For exploration**: Use interactive plots to zoom and explore
5. **For analysis**: Use multi-panel or heatmap for comprehensive views
6. **For sharing**: Export interactive HTML for web sharing
7. **For demonstrations**: Use animations to show sequence evolution
