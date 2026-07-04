# test_final_state.py

import os
import json
import math
import random
import pytest

def my_rand(seed):
    seed = (1103515245 * seed + 12345) % 2147483648
    return (seed / 2147483648.0), seed

def generate_true_data():
    width = 20
    height = 20
    steps = 50
    decay = 0.05
    seed = 42

    grid = [[100.0 for _ in range(width)] for _ in range(height)]

    data = []
    for t in range(steps):
        total = 0
        for i in range(height):
            for j in range(width):
                grid[i][j] = grid[i][j] * (1.0 - decay)
                rand_val, seed = my_rand(seed)
                noise = (rand_val - 0.5) * 2.0
                total += grid[i][j] + noise

        # The C code outputs with %.4f
        val = round(total / (width * height), 4)
        data.append((t, val))
    return data

def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xx = sum(xi*xi for xi in x)
    sum_xy = sum(xi*yi for xi, yi in zip(x, y))

    denominator = n * sum_xx - sum_x**2
    if denominator == 0:
        return 0
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    return slope

def compute_expected_results():
    data = generate_true_data()
    x = [d[0] for d in data]
    y = [math.log(d[1]) for d in data]

    k_est = -linear_regression(x, y)

    random.seed(42)
    k_boot = []
    n = len(data)
    for _ in range(1000):
        resample = [random.choice(data) for _ in range(n)]
        rx = [d[0] for d in resample]
        ry = [math.log(d[1]) for d in resample]
        k_boot.append(-linear_regression(rx, ry))

    k_boot.sort()
    # 2.5th and 97.5th percentiles
    # For 1000 elements, indices 25 and 975 are standard simple approximations
    ci_lower = k_boot[25]
    ci_upper = k_boot[975]

    return k_est, ci_lower, ci_upper

def test_data_csv_exists_and_correct():
    """Check if data.csv exists and has the correct output from the fixed C code."""
    file_path = "/home/user/data.csv"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Remove header if present
    if lines and not lines[0][0].isdigit():
        lines = lines[1:]

    assert len(lines) == 50, f"Expected 50 data rows in data.csv, found {len(lines)}"

    expected_data = generate_true_data()
    for i in range(5):
        expected_line = f"{expected_data[i][0]},{expected_data[i][1]:.4f}"
        assert lines[i] == expected_line, f"Mismatch at step {i}: expected '{expected_line}', got '{lines[i]}'"

def test_results_json():
    """Check if results.json exists and contains the correct bootstrap estimates."""
    file_path = "/home/user/results.json"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    for key in ["k_estimate", "ci_lower", "ci_upper"]:
        assert key in results, f"Missing key '{key}' in results.json"

    expected_k, expected_ci_lower, expected_ci_upper = compute_expected_results()

    # Allow a tolerance of 0.001 for floating point and bootstrap index differences
    assert abs(results["k_estimate"] - expected_k) <= 0.001, f"k_estimate {results['k_estimate']} is not within 0.001 of expected {expected_k:.4f}"
    assert abs(results["ci_lower"] - expected_ci_lower) <= 0.005, f"ci_lower {results['ci_lower']} is not within 0.005 of expected {expected_ci_lower:.4f}"
    assert abs(results["ci_upper"] - expected_ci_upper) <= 0.005, f"ci_upper {results['ci_upper']} is not within 0.005 of expected {expected_ci_upper:.4f}"