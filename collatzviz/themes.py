from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import matplotlib.pyplot as plt
import seaborn as sns


@dataclass
class ColorTheme:
    name: str
    background: str
    odd: str
    even: str
    line: str
    accent: str
    grid: str
    text: str
    secondary: str
    heatmap_low: str
    heatmap_high: str


THEMES: Dict[str, ColorTheme] = {
    "default": ColorTheme(
        name="default",
        background="#FFFFFF",
        odd="#6C5CE7",
        even="#00B894",
        line="#0984E3",
        accent="#E17055",
        grid="#B2BEC3",
        text="#2D3436",
        secondary="#FD79A8",
        heatmap_low="#74B9FF",
        heatmap_high="#D63031",
    ),
    "dark": ColorTheme(
        name="dark",
        background="#1E1E1E",
        odd="#A29BFE",
        even="#55EFC4",
        line="#74B9FF",
        accent="#FAB1A0",
        grid="#636E72",
        text="#DFE6E9",
        secondary="#FD79A8",
        heatmap_low="#0984E3",
        heatmap_high="#FF7675",
    ),
    "vibrant": ColorTheme(
        name="vibrant",
        background="#FAFAFA",
        odd="#9B59B6",
        even="#1ABC9C",
        line="#3498DB",
        accent="#E74C3C",
        grid="#95A5A6",
        text="#34495E",
        secondary="#F39C12",
        heatmap_low="#3498DB",
        heatmap_high="#E74C3C",
    ),
    "pastel": ColorTheme(
        name="pastel",
        background="#FDF6E3",
        odd="#DCD6F7",
        even="#B9FBC0",
        line="#A0C4FF",
        accent="#FFB5A7",
        grid="#D3D3D3",
        text="#4A4A4A",
        secondary="#FFDAC1",
        heatmap_low="#A0C4FF",
        heatmap_high="#FFB5A7",
    ),
    "ocean": ColorTheme(
        name="ocean",
        background="#0F2027",
        odd="#00C9A7",
        even="#92FE9D",
        line="#4CA1AF",
        accent="#C4E0E5",
        grid="#203A43",
        text="#FFFFFF",
        secondary="#2C5364",
        heatmap_low="#00C9A7",
        heatmap_high="#FFFFFF",
    ),
    "sunset": ColorTheme(
        name="sunset",
        background="#2C1E4A",
        odd="#FF6B6B",
        even="#FFE66D",
        line="#4ECDC4",
        accent="#1A535C",
        grid="#4A3B6B",
        text="#FFE66D",
        secondary="#FF6B6B",
        heatmap_low="#4ECDC4",
        heatmap_high="#FF6B6B",
    ),
    "forest": ColorTheme(
        name="forest",
        background="#1B4332",
        odd="#52B788",
        even="#D8F3DC",
        line="#95D5B2",
        accent="#B7E4C7",
        grid="#2D6A4F",
        text="#D8F3DC",
        secondary="#40916C",
        heatmap_low="#52B788",
        heatmap_high="#D8F3DC",
    ),
}


def get_theme(name: str = "default") -> ColorTheme:
    if name not in THEMES:
        raise ValueError(f"Unknown theme '{name}'. Available themes: {list(THEMES.keys())}")
    return THEMES[name]


def list_themes() -> list[str]:
    return list(THEMES.keys())


def apply_theme(theme: ColorTheme) -> None:
    """Apply a color theme to matplotlib and seaborn styling."""
    sns.set_style("whitegrid" if theme.background == "#FFFFFF" else "darkgrid")
    
    plt.rcParams['figure.facecolor'] = theme.background
    plt.rcParams['axes.facecolor'] = theme.background
    plt.rcParams['axes.edgecolor'] = theme.text
    plt.rcParams['axes.labelcolor'] = theme.text
    plt.rcParams['xtick.color'] = theme.text
    plt.rcParams['ytick.color'] = theme.text
    plt.rcParams['text.color'] = theme.text
    plt.rcParams['axes.titlecolor'] = theme.text
    plt.rcParams['grid.color'] = theme.grid
    plt.rcParams['grid.alpha'] = 0.3
