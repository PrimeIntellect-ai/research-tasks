# test_final_state.py

import os
import re
import pytest

def test_dataset_exists():
    """Check that the dataset.csv file exists and has the correct content."""
    dataset_path = "/home/user/dataset.csv"
    assert os.path.isfile(dataset_path), f"File {dataset_path} does not exist."

    with open(dataset_path, "r") as f:
        content = f.read().strip()

    expected_content = "x,y\n1.0,3.2\n2.0,5.1\n3.0,6.8\n4.0,9.1\n5.0,10.9"
    assert content == expected_content, f"Content of {dataset_path} is incorrect."

def test_c_source_exists():
    """Check that the C source file exists."""
    c_source_path = "/home/user/fit_model.c"
    assert os.path.isfile(c_source_path), f"File {c_source_path} does not exist."

def test_solution_txt():
    """Check that solution.txt exists and contains the correct values."""
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"File {solution_path} does not exist."

    with open(solution_path, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 2, f"File {solution_path} must have at least two lines."

    # Compute expected values
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [3.2, 5.1, 6.8, 9.1, 10.9]
    w, b = 0.0, 0.0
    lr = 0.02

    for _ in range(100):
        grad_w = 0.0
        grad_b = 0.0
        for xi, yi in zip(x, y):
            pred = w * xi + b
            grad_w += -2.0/5.0 * xi * (yi - pred)
            grad_b += -2.0/5.0 * (yi - pred)
        w -= lr * grad_w
        b -= lr * grad_b

    log_post = 0.0
    for xi, yi in zip(x, y):
        pred = w * xi + b
        log_post += -0.5 * (yi - pred)**2

    # Parse actual values
    line1 = content[0]
    line2 = content[1]

    match1 = re.search(r'GD w:\s*(-?\d+\.\d+),\s*b:\s*(-?\d+\.\d+)', line1)
    assert match1 is not None, f"Line 1 format is incorrect: {line1}"
    actual_w = float(match1.group(1))
    actual_b = float(match1.group(2))

    match2 = re.search(r'LogPosterior:\s*(-?\d+\.\d+)', line2)
    assert match2 is not None, f"Line 2 format is incorrect: {line2}"
    actual_log_post = float(match2.group(1))

    # Compare with tolerance
    tol = 0.0005
    assert abs(actual_w - w) <= tol, f"Expected w ~ {w:.4f}, but got {actual_w}"
    assert abs(actual_b - b) <= tol, f"Expected b ~ {b:.4f}, but got {actual_b}"
    assert abs(actual_log_post - log_post) <= tol, f"Expected LogPosterior ~ {log_post:.4f}, but got {actual_log_post}"