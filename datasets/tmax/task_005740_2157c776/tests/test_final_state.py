# test_final_state.py
import os
import math

def solve_linear_system(A, b):
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]

        for j in range(i + 1, n):
            factor = M[j][i] / M[i][i]
            for k in range(i, n + 1):
                M[j][k] -= factor * M[i][k]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n] / M[i][i]
        for j in range(i - 1, -1, -1):
            M[j][n] -= M[j][i] * x[i]

    return x

def test_weights_correctness():
    input_file = "/home/user/protein_features.csv"
    output_file = "/home/user/weights.csv"

    assert os.path.isfile(input_file), f"Input file {input_file} is missing."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    X = []
    y = []
    with open(input_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = [float(p.strip()) for p in line.split(",")]
            X.append(parts[:3])
            y.append(parts[3])

    # Compute A = X^T X
    A = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            A[i][j] = sum(X[k][i] * X[k][j] for k in range(len(X)))

    # Add regularization A_reg = A + 0.05 * I
    for i in range(3):
        A[i][i] += 0.05

    # Compute b = X^T y
    b = [0.0] * 3
    for i in range(3):
        b[i] = sum(X[k][i] * y[k] for k in range(len(X)))

    expected_w = solve_linear_system(A, b)

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content, f"Output file {output_file} is empty."

    lines = content.split('\n')
    assert len(lines) == 1, f"Expected exactly 1 line in {output_file}, found {len(lines)}."

    parts = lines[0].split(',')
    assert len(parts) == 3, f"Expected exactly 3 comma-separated values in {output_file}, found {len(parts)}."

    actual_w = [float(p.strip()) for p in parts]

    for i, (actual, expected) in enumerate(zip(actual_w, expected_w)):
        assert abs(actual - expected) <= 1e-3, f"Weight w{i+1} mismatch: expected {expected:.4f}, got {actual:.4f}"