# test_final_state.py

import os
import re
import math
import pytest

def solve_system(M, B):
    n = len(M)
    # Copy M and B to avoid modifying original
    M = [row[:] for row in M]
    B = B[:]
    for i in range(n):
        for j in range(i + 1, n):
            factor = M[j][i] / M[i][i]
            for k in range(i, n):
                M[j][k] -= factor * M[i][k]
            B[j] -= factor * B[i]
    X = [0] * n
    for i in range(n - 1, -1, -1):
        X[i] = B[i]
        for j in range(i + 1, n):
            X[i] -= M[i][j] * X[j]
        X[i] /= M[i][i]
    return X

def get_expected_results():
    data_path = '/home/user/app/data.csv'
    if not os.path.exists(data_path):
        return None, None

    x_vals = []
    y_vals = []
    with open(data_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                x_vals.append(float(parts[0]))
                y_vals.append(float(parts[1]))

    n_coeffs = 4
    ATA = [[0.0] * n_coeffs for _ in range(n_coeffs)]
    ATB = [0.0] * n_coeffs

    for x, y in zip(x_vals, y_vals):
        px = [1.0, x, x**2, x**3]
        for r in range(n_coeffs):
            ATB[r] += px[r] * y
            for c in range(n_coeffs):
                ATA[r][c] += px[r] * px[c]

    # Add regularization
    for i in range(n_coeffs):
        ATA[i][i] += 1e-4

    coeffs = solve_system(ATA, ATB)

    # Integral from 0 to 10
    integral = (coeffs[0] * 10.0 + 
                coeffs[1] * (10.0**2) / 2.0 + 
                coeffs[2] * (10.0**3) / 3.0 + 
                coeffs[3] * (10.0**4) / 4.0)

    return coeffs, integral

def test_executable_exists():
    assert os.path.isfile('/home/user/app/poly_fit'), "The compiled executable 'poly_fit' is missing. Did you compile the program?"

def test_output_file_exists():
    assert os.path.isfile('/home/user/app/output.txt'), "The 'output.txt' file is missing. Did you run the program and redirect output?"

def test_output_results():
    output_path = '/home/user/app/output.txt'
    assert os.path.isfile(output_path), "output.txt not found"

    with open(output_path, 'r') as f:
        content = f.read()

    c_matches = re.findall(r'c(\d)\s*=\s*([-+]?\d*\.\d+)', content)
    assert len(c_matches) == 4, "Could not find exactly 4 coefficients in output.txt in the expected format (e.g., c0 = 1.2345)"

    parsed_coeffs = [0.0] * 4
    for idx_str, val_str in c_matches:
        idx = int(idx_str)
        if 0 <= idx <= 3:
            parsed_coeffs[idx] = float(val_str)

    int_match = re.search(r'Integral\(0 to 10\):\s*([-+]?\d*\.\d+)', content)
    assert int_match, "Could not find 'Integral(0 to 10): [value]' in output.txt"
    parsed_integral = float(int_match.group(1))

    expected_coeffs, expected_integral = get_expected_results()
    assert expected_coeffs is not None, "Failed to compute expected results because data.csv is missing"

    for i in range(4):
        assert abs(parsed_coeffs[i] - expected_coeffs[i]) < 0.005, f"Coefficient c{i} ({parsed_coeffs[i]}) does not match the expected regularized value ({expected_coeffs[i]:.4f}). Did you add 1e-4 to the diagonal of ATA?"

    assert abs(parsed_integral - expected_integral) < 0.005, f"Integral ({parsed_integral}) does not match the expected value ({expected_integral:.4f}). Check your integrate_poly implementation."