from .core import (
	collatz_next,
	collatz_sequence,
	stopping_time,
	total_stopping_time,
	collatz_stats_range,
	RangeStats,
)
from .plotting import plot_sequence, plot_range_stats, plot_transition_graph
from .themes import get_theme, list_themes, THEMES
from .interactive import (
	interactive_sequence,
	interactive_range_stats,
	interactive_3d_trajectory,
)
from .animations import animate_sequence, animate_convergence
from .advanced import (
	multi_panel_sequence,
	heatmap_stopping_times,
	heatmap_2d_range,
	plot_3d_trajectory,
	plot_spiral,
	plot_fractal_tree,
	plot_radial,
)
