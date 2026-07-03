# test_final_state.py

import os
import csv
import math
import pytest

def transpose(A):
    return [list(x) for x in zip(*A)]

def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def norm(v):
    return math.sqrt(sum(x**2 for x in v))

def matmul(A, B):
    B_T = transpose(B)
    return [[dot(row, col) for col in B_T] for row in A]

def qr_decomposition(A):
    m = len(A)
    n = len(A[0])
    R = [[0.0] * n for _ in range(n)]

    V = transpose(A)
    U = []
    for i in range(n):
        u = list(V[i])
        for j in range(i):
            R[j][i] = dot(U[j], V[i])
            u = [u_k - R[j][i] * U[j][k] for k, u_k in enumerate(u)]
        R[i][i] = norm(u)
        U.append([x / R[i][i] for x in u])

    Q = transpose(U)
    return Q, R

def solve_upper_triangular(R, b):
    n = len(R)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= R[i][j] * x[j]
        x[i] /= R[i][i]
    return x

def read_csv(filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        return [[float(val) for val in row] for row in reader if row]

def test_concentrations_and_rss():
    pure_path = '/home/user/pure_components.csv'
    spectra_path = '/home/user/spectra.csv'
    conc_path = '/home/user/concentrations.csv'
    rss_path = '/home/user/rss.txt'

    assert os.path.isfile(pure_path), f"Missing {pure_path}"
    assert os.path.isfile(spectra_path), f"Missing {spectra_path}"
    assert os.path.isfile(conc_path), f"Missing {conc_path}"
    assert os.path.isfile(rss_path), f"Missing {rss_path}"

    A = read_csv(pure_path)
    B = read_csv(spectra_path)

    # Recompute expected values
    Q, R = qr_decomposition(A)
    Q_T = transpose(Q)
    Q_T_B = matmul(Q_T, B)

    # Solve R * X = Q_T * B column by column
    Q_T_B_T = transpose(Q_T_B)
    X_T = [solve_upper_triangular(R, col) for col in Q_T_B_T]
    X_expected = transpose(X_T)

    # Compute expected RSS
    B_pred = matmul(A, X_expected)
    rss_expected = []
    for j in range(len(B[0])):
        col_rss = sum((B[i][j] - B_pred[i][j])**2 for i in range(len(B)))
        rss_expected.append(col_rss)

    # Read user outputs
    X_user = read_csv(conc_path)
    with open(rss_path, 'r') as f:
        rss_user = [float(line.strip()) for line in f if line.strip()]

    # Validate concentrations
    assert len(X_user) == len(X_expected), f"Concentration matrix has {len(X_user)} rows, expected {len(X_expected)}"
    for i in range(len(X_expected)):
        assert len(X_user[i]) == len(X_expected[i]), f"Concentration matrix row {i} has {len(X_user[i])} columns, expected {len(X_expected[i])}"
        for j in range(len(X_expected[i])):
            assert math.isclose(X_user[i][j], X_expected[i][j], abs_tol=1e-5), \
                f"Concentration mismatch at ({i}, {j}): expected {X_expected[i][j]:.6f}, got {X_user[i][j]:.6f}"

    # Validate RSS
    assert len(rss_user) == len(rss_expected), f"RSS list has {len(rss_user)} values, expected {len(rss_expected)}"
    for j in range(len(rss_expected)):
        assert math.isclose(rss_user[j], rss_expected[j], abs_tol=1e-5), \
            f"RSS mismatch at index {j}: expected {rss_expected[j]:.6f}, got {rss_user[j]:.6f}"