# test_final_state.py

import os
import pytest

def test_analyze_c_exists():
    assert os.path.isfile("/home/user/analyze.c"), "/home/user/analyze.c does not exist."

def test_analyze_executable_exists():
    assert os.path.isfile("/home/user/analyze"), "Compiled executable /home/user/analyze does not exist."
    assert os.access("/home/user/analyze", os.X_OK), "/home/user/analyze is not executable."

def test_regression_output():
    output_path = "/home/user/regression.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    sequences = [
        "ATGCGTA",
        "GCGCGCGCGC",
        "ATATATATATATAT",
        "GGGCCC",
        "ATGCATGCATGCATGC"
    ]

    # Compute expected values
    x = [(i * 137 % 100000) / 10000.0 for i in range(100000)]
    mean_x = sum(x) / len(x)
    mean_x2 = sum(v**2 for v in x) / len(x)

    areas = []
    lengths = []
    for seq in sequences:
        p = sum(1 for c in seq if c in 'GC') / len(seq)
        A = (p * mean_x2 + (1 - p) * mean_x) * 10
        areas.append(A)
        lengths.append(len(seq))

    n = len(lengths)
    sum_L = sum(lengths)
    sum_A = sum(areas)
    sum_LA = sum(l * a for l, a in zip(lengths, areas))
    sum_L2 = sum(l**2 for l in lengths)

    m = (n * sum_LA - sum_L * sum_A) / (n * sum_L2 - sum_L**2)
    c = (sum_A - m * sum_L) / n

    expected_slope = f"Slope: {m:.4f}"
    expected_intercept = f"Intercept: {c:.4f}"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected 2 lines in {output_path}, found {len(lines)}"

    assert lines[0] == expected_slope, f"Expected '{expected_slope}', got '{lines[0]}'"
    assert lines[1] == expected_intercept, f"Expected '{expected_intercept}', got '{lines[1]}'"