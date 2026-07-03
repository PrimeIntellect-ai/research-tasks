# test_final_state.py

import os
import json
import math
import pytest

def largest_singular_value(mat):
    n = len(mat)
    m = len(mat[0])

    # Compute A^T * A
    AtA = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            AtA[i][j] = sum(mat[k][i] * mat[k][j] for k in range(n))

    # Power iteration to find the largest eigenvalue of A^T * A
    v = [1.0] * m
    for _ in range(200):
        v_new = [sum(AtA[i][j] * v[j] for j in range(m)) for i in range(m)]
        norm = math.sqrt(sum(x * x for x in v_new))
        if norm == 0:
            break
        v = [x / norm for x in v_new]

    # Rayleigh quotient
    Av = [sum(AtA[i][j] * v[j] for j in range(m)) for i in range(m)]
    lambda_max = sum(v[i] * Av[i] for i in range(m))

    return math.sqrt(lambda_max)

def test_svd_results():
    results_file = "/home/user/svd_results.txt"
    matrices_file = "/home/user/matrices.json"

    assert os.path.isfile(results_file), f"Expected result file {results_file} does not exist."
    assert os.path.isfile(matrices_file), f"Matrices file {matrices_file} is missing."

    with open(matrices_file, "r") as f:
        matrices = json.load(f)

    s_maxes = [largest_singular_value(mat) for mat in matrices]

    mean_val = sum(s_maxes) / len(s_maxes)
    std_val = math.sqrt(sum((x - mean_val) ** 2 for x in s_maxes) / len(s_maxes))

    with open(results_file, "r") as f:
        content = f.read().strip()

    parts = content.split(",")
    assert len(parts) == 2, f"File content '{content}' does not match format 'mean,std'."

    try:
        actual_mean = float(parts[0])
        actual_std = float(parts[1])
    except ValueError:
        pytest.fail(f"Could not parse mean and std as floats from '{content}'.")

    # Check format exactly 4 decimal places
    assert "." in parts[0] and len(parts[0].split(".")[1]) == 4, "Mean is not rounded to exactly 4 decimal places."
    assert "." in parts[1] and len(parts[1].split(".")[1]) == 4, "Std is not rounded to exactly 4 decimal places."

    assert math.isclose(actual_mean, mean_val, abs_tol=0.0002), f"Expected mean approx {mean_val:.4f}, got {actual_mean}"
    assert math.isclose(actual_std, std_val, abs_tol=0.0002), f"Expected std approx {std_val:.4f}, got {actual_std}"

def test_rust_project_exists():
    assert os.path.isdir("/home/user/svd_profile"), "Rust project directory /home/user/svd_profile does not exist."
    assert os.path.isfile("/home/user/svd_profile/Cargo.toml"), "Cargo.toml not found in /home/user/svd_profile."
    assert os.path.isfile("/home/user/svd_profile/src/main.rs"), "src/main.rs not found in /home/user/svd_profile."