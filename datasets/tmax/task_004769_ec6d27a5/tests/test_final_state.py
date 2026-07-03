# test_final_state.py

import os
import pytest

def test_calc_energy_binary_exists():
    binary_path = "/home/user/bin/calc_energy"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_regression_results():
    results_path = "/home/user/regression_results.txt"
    assert os.path.isfile(results_path), f"Results file not found at {results_path}"

    signals_path = "/home/user/data/signals.txt"
    targets_path = "/home/user/data/targets.txt"

    assert os.path.isfile(signals_path), "Signals file missing"
    assert os.path.isfile(targets_path), "Targets file missing"

    # Compute expected x (energies)
    x = []
    with open(signals_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            energy = sum(float(val)**2 for val in parts)
            x.append(energy)

    # Compute expected y (targets)
    y = []
    with open(targets_path, 'r') as f:
        for line in f:
            val = line.strip()
            if not val:
                continue
            y.append(float(val))

    assert len(x) == len(y), "Mismatch in number of signals and targets"
    N = len(x)
    assert N > 0, "No data found"

    # Calculate linear regression
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(N))
    sum_x2 = sum(x[i]**2 for i in range(N))

    denominator = (N * sum_x2 - sum_x**2)
    assert denominator != 0, "Denominator for slope is zero"

    m = (N * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y - m * sum_x) / N

    expected_output = f"Slope: {m:.4f}, Intercept: {b:.4f}"

    with open(results_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_output, (
        f"Incorrect regression results.\n"
        f"Expected: '{expected_output}'\n"
        f"Actual:   '{actual_content}'"
    )