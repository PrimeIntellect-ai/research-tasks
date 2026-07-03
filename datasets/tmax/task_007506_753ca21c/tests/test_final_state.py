# test_final_state.py

import os
import math
import pytest

def pearson_corr(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_sq = sum(v**2 for v in x)
    sum_y_sq = sum(v**2 for v in y)
    sum_xy = sum(x[i]*y[i] for i in range(n))

    num = n * sum_xy - sum_x * sum_y
    den = math.sqrt((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))
    if den == 0:
        return 0.0
    return num / den

def read_even_epochs(filepath):
    loss_values = []
    with open(filepath, 'r') as f:
        next(f) # skip header
        for line in f:
            if not line.strip():
                continue
            epoch, loss = line.strip().split(',')
            if int(epoch) % 2 == 0:
                loss_values.append(float(loss))
    return loss_values

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_best_candidates_output():
    output_path = "/home/user/best_candidates.txt"
    assert os.path.isfile(output_path), f"{output_path} does not exist."

    # Compute expected results
    baseline_path = "/home/user/experiments/baseline.csv"
    assert os.path.isfile(baseline_path), "baseline.csv missing."

    base_loss = read_even_epochs(baseline_path)

    correlations = []
    for i in range(1, 6):
        cand_file = f"cand_{i}.csv"
        cand_path = os.path.join("/home/user/experiments", cand_file)
        if os.path.isfile(cand_path):
            cand_loss = read_even_epochs(cand_path)
            corr = pearson_corr(base_loss, cand_loss)
            correlations.append((cand_file, corr))

    # Sort descending by correlation
    correlations.sort(key=lambda x: x[1], reverse=True)
    top_2 = correlations[:2]

    expected_lines = [f"{c[0]} {c[1]:.4f}" for c in top_2]

    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 2, f"Expected exactly 2 lines in {output_path}, found {len(actual_lines)}."

    for i in range(2):
        assert actual_lines[i] == expected_lines[i], (
            f"Line {i+1} mismatch in {output_path}. "
            f"Expected '{expected_lines[i]}', got '{actual_lines[i]}'."
        )