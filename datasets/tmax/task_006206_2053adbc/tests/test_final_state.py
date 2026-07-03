# test_final_state.py

import os
import math
import pytest

def read_csv(filepath):
    matrix = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                matrix.append([float(x) for x in line.strip().split(',')])
    return matrix

def test_decomposition_results():
    """Test that the C program produced the correct Cholesky decomposition."""
    log_file = '/home/user/decomposition_results.log'
    csv_file = '/home/user/cov_matrix.csv'

    assert os.path.exists(log_file), f"Log file {log_file} missing. Did you run your C program?"
    assert os.path.exists(csv_file), f"Original CSV file {csv_file} missing."

    # Read original matrix
    A = read_csv(csv_file)
    assert len(A) == 5 and all(len(row) == 5 for row in A), "Original matrix must be 5x5."

    # Regularize A (add 1e-4 to diagonal)
    A_reg = [[A[i][j] + (1e-4 if i == j else 0.0) for j in range(5)] for i in range(5)]

    # Parse L matrix from log file
    L = []
    with open(log_file, 'r') as f:
        lines = f.readlines()

    l_start = -1
    for i, line in enumerate(lines):
        if line.startswith('L_Matrix:'):
            l_start = i + 1
            break

    assert l_start != -1, "Could not find 'L_Matrix:' header in the log file."
    assert len(lines) >= l_start + 5, "Log file does not contain 5 rows for the L matrix."

    for i in range(5):
        try:
            row = [float(x.strip()) for x in lines[l_start + i].split(',')]
        except ValueError:
            pytest.fail(f"Could not parse floats from L matrix row {i}: {lines[l_start + i].strip()}")
        assert len(row) == 5, f"Row {i} of L matrix does not have 5 elements."
        L.append(row)

    # Check if L is lower triangular
    for i in range(5):
        for j in range(i + 1, 5):
            assert abs(L[i][j]) < 1e-9, f"L is not lower triangular, L[{i}][{j}] = {L[i][j]} != 0"

    # Reconstruct A_recon = L L^T
    A_recon = [[sum(L[i][k] * L[j][k] for k in range(5)) for j in range(5)] for i in range(5)]

    # Compute Frobenius norm of error
    error_sq = 0.0
    for i in range(5):
        for j in range(5):
            diff = A_recon[i][j] - A_reg[i][j]
            error_sq += diff * diff

    error = math.sqrt(error_sq)
    assert error <= 1e-4, f"Reconstruction error too high: {error} > 1e-4. The decomposition does not match the regularized matrix."

def test_error_frobenius_format():
    """Test that the Frobenius error is present in the log file."""
    log_file = '/home/user/decomposition_results.log'
    assert os.path.exists(log_file), f"Log file {log_file} missing."

    with open(log_file, 'r') as f:
        content = f.read()

    assert "Error_Frobenius:" in content, "Log file missing 'Error_Frobenius:' line."