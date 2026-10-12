from __future__ import annotations

import argparse
from pathlib import Path

from .core import collatz_stats_range
from .plotting import plot_range_stats, plot_sequence, plot_transition_graph
from .themes import list_themes
from .interactive import interactive_sequence, interactive_range_stats, interactive_3d_trajectory
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


def main() -> None:
	p = argparse.ArgumentParser(
		description="Collatz predictive graphs - Enhanced visualization suite",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Available themes: """ + ", ".join(list_themes()) + """
Examples:
  collatzviz sequence --start 27 --theme dark
  collatzviz range-stats --start 1 --end 100 --theme vibrant
  collatzviz interactive-sequence --start 27
  collatzviz animation --start 27 --theme ocean
  collatzviz multipanel --start 27
  collatzviz heatmap --start 1 --end 100
  collatzviz spiral --start 27 --theme sunset
		"""
	)
	sub = p.add_subparsers(dest="cmd", required=True)

	# Add theme argument to common subparsers
	def add_theme_args(parser):
		parser.add_argument("--theme", type=str, default="default", 
						  help=f"Color theme (default: {', '.join(list_themes())})")
		parser.add_argument("--outdir", type=str, default="out", help="Output directory")

	# Original commands
	p_seq = sub.add_parser("sequence", help="plot a single trajectory")
	p_seq.add_argument("--start", type=int, required=True)
	add_theme_args(p_seq)

	p_range = sub.add_parser("range-stats", help="plot range stats and trend line")
	p_range.add_argument("--start", type=int, required=True)
	p_range.add_argument("--end", type=int, required=True)
	add_theme_args(p_range)

	p_graph = sub.add_parser("graph", help="plot transition digraph for a range")
	p_graph.add_argument("--start", type=int, required=True)
	p_graph.add_argument("--end", type=int, required=True)
	add_theme_args(p_graph)

	# Interactive plots
	p_int_seq = sub.add_parser("interactive-sequence", help="create interactive plotly sequence plot")
	p_int_seq.add_argument("--start", type=int, required=True)
	add_theme_args(p_int_seq)

	p_int_stats = sub.add_parser("interactive-stats", help="create interactive plotly range stats")
	p_int_stats.add_argument("--start", type=int, required=True)
	p_int_stats.add_argument("--end", type=int, required=True)
	add_theme_args(p_int_stats)

	p_int_3d = sub.add_parser("interactive-3d", help="create interactive 3D trajectory")
	p_int_3d.add_argument("--start", type=int, required=True)
	add_theme_args(p_int_3d)

	# Animations
	p_anim = sub.add_parser("animation", help="create animated GIF of sequence")
	p_anim.add_argument("--start", type=int, required=True)
	p_anim.add_argument("--fps", type=int, default=10, help="Frames per second")
	p_anim.add_argument("--interval", type=int, default=200, help="Interval between frames (ms)")
	add_theme_args(p_anim)

	p_anim_conv = sub.add_parser("animation-convergence", help="create animated convergence visualization")
	p_anim_conv.add_argument("--start", type=int, required=True)
	p_anim_conv.add_argument("--fps", type=int, default=10, help="Frames per second")
	p_anim_conv.add_argument("--interval", type=int, default=200, help="Interval between frames (ms)")
	add_theme_args(p_anim_conv)

	# Advanced visualizations
	p_multi = sub.add_parser("multipanel", help="create multi-panel analysis figure")
	p_multi.add_argument("--start", type=int, required=True)
	add_theme_args(p_multi)

	p_heat = sub.add_parser("heatmap", help="create heatmap of stopping times")
	p_heat.add_argument("--start", type=int, required=True)
	p_heat.add_argument("--end", type=int, required=True)
	add_theme_args(p_heat)

	p_heat2d = sub.add_parser("heatmap-2d", help="create 2D multi-metric heatmaps")
	p_heat2d.add_argument("--start", type=int, required=True)
	p_heat2d.add_argument("--end", type=int, required=True)
	add_theme_args(p_heat2d)

	p_3d = sub.add_parser("3d", help="create 3D matplotlib trajectory")
	p_3d.add_argument("--start", type=int, required=True)
	add_theme_args(p_3d)

	p_spiral = sub.add_parser("spiral", help="create spiral visualization")
	p_spiral.add_argument("--start", type=int, required=True)
	add_theme_args(p_spiral)

	p_fractal = sub.add_parser("fractal", help="create fractal tree visualization")
	p_fractal.add_argument("--start", type=int, required=True)
	p_fractal.add_argument("--max-depth", type=int, default=8, help="Maximum recursion depth")
	add_theme_args(p_fractal)

	p_radial = sub.add_parser("radial", help="create radial/circular visualization")
	p_radial.add_argument("--start", type=int, required=True)
	add_theme_args(p_radial)

	args = p.parse_args()

	outdir = Path(args.outdir)
	theme = getattr(args, 'theme', 'default')

	if args.cmd == "sequence":
		path = plot_sequence(args.start, outdir, theme=theme)
		print(path)
	elif args.cmd == "range-stats":
		stats = collatz_stats_range(args.start, args.end)
		paths = plot_range_stats(stats, outdir, theme=theme)
		for k, v in paths.items():
			print(k, v, sep="\t")
	elif args.cmd == "graph":
		path = plot_transition_graph(args.start, args.end, outdir, theme=theme)
		print(path)
	elif args.cmd == "interactive-sequence":
		path = interactive_sequence(args.start, outdir, theme=theme)
		print(f"Interactive HTML: {path}")
	elif args.cmd == "interactive-stats":
		stats = collatz_stats_range(args.start, args.end)
		paths = interactive_range_stats(stats, outdir, theme=theme)
		for k, v in paths.items():
			print(f"Interactive HTML: {v}")
	elif args.cmd == "interactive-3d":
		path = interactive_3d_trajectory(args.start, outdir, theme=theme)
		print(f"Interactive HTML: {path}")
	elif args.cmd == "animation":
		path = animate_sequence(args.start, outdir, theme=theme, 
								fps=args.fps, interval=args.interval)
		print(f"Animation GIF: {path}")
	elif args.cmd == "animation-convergence":
		path = animate_convergence(args.start, outdir, theme=theme,
									fps=args.fps, interval=args.interval)
		print(f"Animation GIF: {path}")
	elif args.cmd == "multipanel":
		path = multi_panel_sequence(args.start, outdir, theme=theme)
		print(path)
	elif args.cmd == "heatmap":
		path = heatmap_stopping_times(args.start, args.end, outdir, theme=theme)
		print(path)
	elif args.cmd == "heatmap-2d":
		path = heatmap_2d_range(args.start, args.end, outdir, theme=theme)
		print(path)
	elif args.cmd == "3d":
		path = plot_3d_trajectory(args.start, outdir, theme=theme)
		print(path)
	elif args.cmd == "spiral":
		path = plot_spiral(args.start, outdir, theme=theme)
		print(path)
	elif args.cmd == "fractal":
		path = plot_fractal_tree(args.start, outdir, theme=theme, max_depth=args.max_depth)
		print(path)
	elif args.cmd == "radial":
		path = plot_radial(args.start, outdir, theme=theme)
		print(path)


if __name__ == "__main__":
	main()
