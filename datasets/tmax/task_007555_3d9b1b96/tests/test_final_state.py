# test_final_state.py

import os
import pytest

def compute_expected_regression(csv_path: str) -> str:
    """Read the CSV, filter for SENS-42, and compute the expected linear regression."""
    with open(csv_path, 'r') as f:
        lines = f.read().strip().split('\n')

    # Skip header
    data_lines = lines[1:]

    t_raw = []
    temperatures = []

    for line in data_lines:
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) == 3 and parts[1] == 'SENS-42':
            t_raw.append(float(parts[0]))
            temperatures.append(float(parts[2]))

    if not t_raw:
        pytest.fail("No data found for SENS-42 in the CSV.")

    t0 = t_raw[0]
    x = [(t - t0) / 1000.0 for t in t_raw]
    y = temperatures

    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(xi ** 2 for xi in x)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))

    # m = (n * sum(x*y) - sum(x) * sum(y)) / (n * sum(x^2) - sum(x)^2)
    denominator = (n * sum_x2 - sum_x ** 2)
    if denominator == 0:
        pytest.fail("Cannot compute linear regression: denominator is zero.")

    m = (n * sum_xy - sum_x * sum_y) / denominator

    # c = (sum(y) - m * sum(x)) / n
    c = (sum_y - m * sum_x) / n

    return f"Slope: {m:.4f}, Intercept: {c:.4f}"

def test_rust_file_exists():
    """Test that the Rust source file was created."""
    file_path = "/home/user/trend_fitter.rs"
    assert os.path.exists(file_path), f"Rust source file {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_regression_results():
    """Test that the regression results file exists and contains the correct output."""
    results_path = "/home/user/regression_results.txt"
    csv_path = "/home/user/raw_sensor_data.csv"

    assert os.path.exists(results_path), f"Results file {results_path} is missing."
    assert os.path.isfile(results_path), f"Path {results_path} is not a file."

    expected_output = compute_expected_regression(csv_path)

    with open(results_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_output, (
        f"Content of {results_path} is incorrect.\n"
        f"Expected: '{expected_output}'\n"
        f"Got: '{content}'"
    )