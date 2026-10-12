import pytest

from collatzviz.themes import get_theme, list_themes, THEMES


def test_list_themes():
    themes = list_themes()
    assert isinstance(themes, list)
    assert len(themes) > 0
    assert "default" in themes
    assert "dark" in themes


def test_get_theme_default():
    theme = get_theme("default")
    assert theme.name == "default"
    assert theme.background == "#FFFFFF"
    assert theme.odd == "#6C5CE7"
    assert theme.even == "#00B894"


def test_get_theme_dark():
    theme = get_theme("dark")
    assert theme.name == "dark"
    assert theme.background == "#1E1E1E"
    assert theme.text == "#DFE6E9"


def test_get_theme_invalid():
    with pytest.raises(ValueError):
        get_theme("nonexistent_theme")


def test_all_themes_have_required_fields():
    for theme_name in list_themes():
        theme = get_theme(theme_name)
        assert hasattr(theme, 'name')
        assert hasattr(theme, 'background')
        assert hasattr(theme, 'odd')
        assert hasattr(theme, 'even')
        assert hasattr(theme, 'line')
        assert hasattr(theme, 'accent')
        assert hasattr(theme, 'grid')
        assert hasattr(theme, 'text')
        assert hasattr(theme, 'secondary')
        assert hasattr(theme, 'heatmap_low')
        assert hasattr(theme, 'heatmap_high')
