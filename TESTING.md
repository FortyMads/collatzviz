# Testing Guide for collatzviz

This guide explains how to test Python projects like collatzviz.

## Overview

Testing is essential for ensuring your code works correctly. This project uses **pytest**, a popular Python testing framework.

## Project Structure

```
collatzviz/
├── collatzviz/          # Main package
│   ├── __init__.py
│   ├── core.py          # Core logic (math functions)
│   ├── plotting.py      # Visualization functions
│   ├── themes.py        # Color themes
│   ├── interactive.py   # Interactive plots
│   ├── animations.py    # Animation functions
│   ├── advanced.py      # Advanced visualizations
│   └── __main__.py      # CLI entry point
├── tests/               # Test directory
│   ├── test_core.py     # Tests for core functions
│   ├── test_themes.py   # Tests for theme system
│   └── test_advanced.py # Tests for advanced visualizations
├── pyproject.toml       # Project configuration
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

## Setting Up for Testing

### 1. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Install the Project in Editable Mode

This allows you to make changes and test them without reinstalling:

```bash
pip install -e .
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_core.py
```

### Run Specific Test Function

```bash
pytest tests/test_core.py::test_collatz_next_small
```

### Run Tests Matching a Pattern

```bash
pytest -k "sequence"
```

### Stop on First Failure

```bash
pytest -x
```

### Show Print Statements

```bash
pytest -s
```

## Writing Tests

### Basic Test Structure

```python
import pytest
from collatzviz.core import collatz_next

def test_collatz_next_small():
    """Test collatz_next with small inputs."""
    assert collatz_next(1) == 4
    assert collatz_next(2) == 1
    assert collatz_next(3) == 10
```

### Testing for Exceptions

```python
def test_invalid_input():
    """Test that invalid inputs raise ValueError."""
    with pytest.raises(ValueError):
        collatz_next(0)
```

### Testing File Output

```python
from pathlib import Path

def test_plot_creates_file(tmp_path):
    """Test that plotting functions create output files."""
    from collatzviz.plotting import plot_sequence
    
    path = plot_sequence(27, outdir=tmp_path, theme="default")
    assert path.exists()
    assert path.suffix == ".png"
```

The `tmp_path` fixture is provided by pytest and creates a temporary directory that's automatically cleaned up.

### Testing Multiple Cases

```python
@pytest.mark.parametrize("input,expected", [
    (1, 4),
    (2, 1),
    (3, 10),
])
def test_collatz_next_parametrized(input, expected):
    assert collatz_next(input) == expected
```

## Test Categories

### 1. Unit Tests
Test individual functions in isolation:
- Core mathematical functions
- Theme retrieval
- Input validation

Example: `test_core.py`

### 2. Integration Tests
Test that multiple components work together:
- Plotting with different themes
- Full visualization pipelines
- CLI commands

Example: `test_advanced.py`

### 3. Visual Regression Tests (Optional)
For visualization projects, you might want to ensure plots don't change unexpectedly:
- Save reference images
- Compare new outputs with references
- Use tools like `pytest-image-diff`

## Current Test Coverage

### test_core.py
- ✅ `collatz_next()` - basic functionality
- ✅ `collatz_sequence()` - sequence generation
- ✅ `stopping_time()` and `total_stopping_time()` - timing calculations
- ✅ Input validation - error handling

### test_themes.py
- ✅ Theme listing
- ✅ Theme retrieval
- ✅ Theme validation
- ✅ All theme fields present

### test_advanced.py
- ✅ Multi-panel visualizations
- ✅ Heatmap generation
- ✅ 3D trajectory plots
- ✅ Spiral visualizations
- ✅ Radial plots
- ✅ Theme compatibility

## Best Practices

### 1. Test Naming
- Use descriptive names: `test_collatz_next_small()` not `test_1()`
- Group related tests in the same file
- Use clear docstrings

### 2. Test Independence
- Each test should run independently
- Don't rely on test execution order
- Clean up after tests (use fixtures)

### 3. Test Edge Cases
- Test boundary conditions (0, 1, negative numbers)
- Test empty inputs
- Test large inputs (within reason)

### 4. Keep Tests Fast
- Use small test data when possible
- Mock external dependencies
- Avoid slow operations in tests

### 5. Use Fixtures
```python
@pytest.fixture
def sample_sequence():
    return [27, 82, 41, 124, 62, 31, 94, 47, 142, 71, 214, 107, 322, 161, 484, 242, 121, 364, 182, 91, 274, 137, 412, 206, 103, 310, 155, 466, 233, 700, 350, 175, 526, 263, 790, 395, 1186, 593, 1780, 890, 445, 1336, 668, 334, 167, 502, 251, 754, 377, 1132, 566, 283, 850, 425, 1276, 638, 319, 958, 479, 1438, 719, 2158, 1079, 3238, 1619, 4858, 2429, 7288, 3644, 1822, 911, 2734, 1367, 4102, 2051, 6154, 3077, 9232, 4616, 2308, 1154, 577, 1732, 866, 433, 1300, 650, 325, 976, 488, 244, 122, 61, 184, 92, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]

def test_sequence_length(sample_sequence):
    from collatzviz.core import collatz_sequence
    seq = collatz_sequence(27)
    assert len(seq) == len(sample_sequence)
```

## Continuous Integration

For professional projects, add CI to run tests automatically:

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pip install -e .
      - run: pytest
```

## Troubleshooting

### Import Errors
If you get "ModuleNotFoundError", ensure:
1. You've installed the package: `pip install -e .`
2. Your virtual environment is activated
3. You're running pytest from the project root

### Matplotlib Backend Issues
The project uses the "Agg" backend for headless environments. If you see display errors:
```python
import matplotlib
matplotlib.use("Agg")
```

### Slow Tests
Visualization tests can be slow. To speed up:
- Use smaller test data
- Mock the plotting functions
- Mark slow tests: `@pytest.mark.slow`

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Effective Python Testing with Pytest](https://realpython.com/pytest-python-testing/)
