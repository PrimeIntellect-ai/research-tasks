# test_final_state.py

import os
import numpy as np
import pytest

def f(x):
    return np.exp(-100 * (x - 0.3)**2) + 0.5 * np.sin(20 * x) + 1.0 / (1.0 + 1000 * (x - 0.8)**2)

def test_predictions_mse():
    """Check that predictions.txt exists, has 10000 lines, and MSE < 0.001."""
    pred_path = '/home/user/predictions.txt'
    assert os.path.exists(pred_path), f"{pred_path} does not exist"

    try:
        y_pred = np.loadtxt(pred_path)
    except Exception as e:
        pytest.fail(f"Failed to load {pred_path}: {e}")

    assert len(y_pred) == 10000, f"Expected exactly 10000 predictions, got {len(y_pred)}"

    x_dense = np.linspace(0, 1, 10000)
    y_true = f(x_dense)

    mse = np.mean((y_true - y_pred)**2)
    assert mse < 0.001, f"MSE {mse:.6f} is not < 0.001. The mesh refinement may not be optimal."

def test_bootstrap_ci_format():
    """Check that bootstrap_ci.txt exists and is formatted correctly."""
    ci_path = '/home/user/bootstrap_ci.txt'
    assert os.path.exists(ci_path), f"{ci_path} does not exist"

    with open(ci_path, 'r') as f_ci:
        content = f_ci.read().strip()

    parts = content.split(',')
    assert len(parts) == 2, f"Expected format 'lower,upper', got '{content}'"

    try:
        lower = float(parts[0])
        upper = float(parts[1])
    except ValueError:
        pytest.fail(f"Could not parse '{content}' as comma-separated floats")

    assert lower <= upper, f"Lower bound {lower} is greater than upper bound {upper}"

def test_cpp_source_exists():
    """Check that the C++ source file exists."""
    cpp_path = '/home/user/surrogate.cpp'
    assert os.path.exists(cpp_path), f"{cpp_path} does not exist. A C++ implementation is required."