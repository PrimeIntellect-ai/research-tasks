# test_final_state.py

import os
import pytest

def test_analyze_c_exists():
    """Test that the C program file was created."""
    c_file_path = "/home/user/analyze.c"
    assert os.path.isfile(c_file_path), f"Missing C program file: {c_file_path}"

def test_results_txt_matches_expected():
    """Test that results.txt exists and contains the correct computed values."""
    data_path = "/home/user/data.csv"
    results_path = "/home/user/results.txt"

    assert os.path.isfile(data_path), f"Missing data file: {data_path}"
    assert os.path.isfile(results_path), f"Missing results file: {results_path}"

    # Read and parse data
    X = []
    Y = []
    with open(data_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                X.append(float(parts[0]))
                Y.append(float(parts[1]))

    n = len(X)
    assert n > 1, "Not enough data points to compute covariance."

    # Compute means
    mean_x = sum(X) / n
    mean_y = sum(Y) / n

    # Compute unbiased covariance
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(X, Y)) / (n - 1)

    # Compute posterior mean
    prior_mean = 5.0
    prior_var = 2.0
    data_var = 3.0

    post_mean = (prior_mean / prior_var + n * mean_x / data_var) / (1 / prior_var + n / data_var)

    expected_output = f"Covariance: {cov:.4f}\nPosterior Mean: {post_mean:.4f}\n"

    with open(results_path, 'r') as f:
        actual_output = f.read()

    # Standardize line endings and whitespace for comparison
    expected_lines = [line.strip() for line in expected_output.strip().split('\n')]
    actual_lines = [line.strip() for line in actual_output.strip().split('\n')]

    assert actual_lines == expected_lines, (
        f"Results do not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )