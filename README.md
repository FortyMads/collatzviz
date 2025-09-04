# Collatz Predictive Graphs

A small Python project to explore and visualize the Collatz conjecture with “predictive” graphs:
- Sequence trajectories for one or many starting values
- Stopping time and total stopping time across ranges
- Peak values across ranges
- Directed transition graph (n -> f(n)) within a range
- Trend lines that suggest how stopping time grows with n (e.g., vs log n)

## Features
- Clean Python API (`collatzviz.*`)
- CLI to generate plots to PNG files
- Minimal tests

## Install
Create a virtual environment (recommended), then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Start
Generate and save the trajectory plot for 27:

```bash
python -m collatzviz sequence --start 27 --outdir out
```

Stopping time and peak value summaries for a range:

```bash
python -m collatzviz range-stats --start 1 --end 5000 --outdir out
```

Directed transition graph within a range (keep ranges modest for readability):

```bash
python -m collatzviz graph --start 1 --end 200 --outdir out
```

Open images in the `out/` folder.

## What “predictive” means here
We can’t predict Collatz convergence, but we can:
- Compare stopping times across ranges
- Fit simple trend lines vs log(n) to visualize growth tendencies
- Highlight peaks and path shapes for insight

## Tests
Run a small test suite:

```bash
pytest -q
```

## Notes
- For very large ranges, computations and plots can be slow or memory-heavy. Start small.
- The transition graph becomes dense quickly; limit `end - start` to a few hundred.
