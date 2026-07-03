# test_final_state.py

import os
import math
import pytest

def compute_expected_cholesky_diagonals():
    # Magnitudes derived from the task description
    M = [0.0, 40.0, 40.0, 0.0]

    # Construct matrix S = M * M^T
    S = [[M[i] * M[j] for j in range(4)] for i in range(4)]

    # Add Tikhonov regularization (lambda = 0.1)
    for i in range(4):
        S[i][i] += 0.1

    # Compute Cholesky decomposition L
    L = [[0.0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(i + 1):
            sum_k = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                L[i][j] = math.sqrt(S[i][i] - sum_k)
            else:
                L[i][j] = (S[i][j] - sum_k) / L[j][j]

    # Return diagonal elements
    return [L[i][i] for i in range(4)]

def test_cholesky_output_exists():
    file_path = "/home/user/cholesky_diag.txt"
    assert os.path.isfile(file_path), f"The expected output file {file_path} does not exist. Make sure your C program writes to this exact path."

def test_cholesky_output_content():
    file_path = "/home/user/cholesky_diag.txt"
    assert os.path.isfile(file_path), f"Cannot check content because {file_path} is missing."

    expected_diags = compute_expected_cholesky_diagonals()
    expected_lines = [f"{val:.4f}" for val in expected_diags]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(actual_lines) == 4, f"Expected exactly 4 lines in {file_path}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i+1} (Sequence {chr(ord('A')+i)}). Expected {expected}, got {actual}."