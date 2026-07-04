# test_final_state.py

import os
import math
import pytest

def compute_pearson_correlation(csv_path):
    with open(csv_path, 'r') as f:
        lines = f.read().strip().split('\n')

    header = lines[0].split(',')
    latency_idx = header.index('latency_ms')
    accuracy_idx = header.index('accuracy')

    x = []
    y = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split(',')
        x.append(float(parts[latency_idx]))
        y.append(float(parts[accuracy_idx]))

    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x2 = sum(xi ** 2 for xi in x)
    sum_y2 = sum(yi ** 2 for yi in y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))

    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))

    if denominator == 0:
        return 0.0
    return numerator / denominator

def test_analyze_c_exists():
    """Test that the C source file was created."""
    file_path = "/home/user/analyze.c"
    assert os.path.exists(file_path), f"Missing required file: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"

def test_correlation_result_exists():
    """Test that the output file was created."""
    file_path = "/home/user/correlation_result.txt"
    assert os.path.exists(file_path), f"Missing required file: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"

def test_correlation_result_content():
    """Test that the output file contains the correct correlation coefficient."""
    csv_path = "/home/user/experiments.csv"
    assert os.path.exists(csv_path), f"Missing required file: {csv_path}"

    expected_r = compute_pearson_correlation(csv_path)
    expected_output = f"Correlation: {expected_r:.4f}"

    result_path = "/home/user/correlation_result.txt"
    with open(result_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Incorrect correlation result in {result_path}. "
        f"Expected: '{expected_output}', Got: '{actual_output}'"
    )