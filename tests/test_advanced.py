import pytest
from pathlib import Path

from collatzviz.advanced import (
    multi_panel_sequence,
    heatmap_stopping_times,
    plot_3d_trajectory,
    plot_spiral,
    plot_radial,
)
from collatzviz.core import collatz_stats_range


def test_multi_panel_sequence(tmp_path):
    """Test multi-panel visualization creates output file."""
    path = multi_panel_sequence(27, outdir=tmp_path, theme="default")
    assert path.exists()
    assert path.suffix == ".png"


def test_heatmap_stopping_times(tmp_path):
    """Test heatmap visualization creates output file."""
    path = heatmap_stopping_times(1, 50, outdir=tmp_path, theme="default")
    assert path.exists()
    assert path.suffix == ".png"


def test_plot_3d_trajectory(tmp_path):
    """Test 3D trajectory visualization creates output file."""
    path = plot_3d_trajectory(27, outdir=tmp_path, theme="default")
    assert path.exists()
    assert path.suffix == ".png"


def test_plot_spiral(tmp_path):
    """Test spiral visualization creates output file."""
    path = plot_spiral(27, outdir=tmp_path, theme="default")
    assert path.exists()
    assert path.suffix == ".png"


def test_plot_radial(tmp_path):
    """Test radial visualization creates output file."""
    path = plot_radial(27, outdir=tmp_path, theme="default")
    assert path.exists()
    assert path.suffix == ".png"


def test_all_themes_work_with_advanced(tmp_path):
    """Test that all themes work with advanced visualizations."""
    from collatzviz.themes import list_themes
    
    for theme in list_themes():
        path = plot_spiral(7, outdir=tmp_path, theme=theme)
        assert path.exists()
