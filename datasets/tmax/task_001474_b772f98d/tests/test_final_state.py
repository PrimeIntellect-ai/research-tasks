# test_final_state.py
import os
import json
import csv
import math
import pytest

def get_mean(X):
    n = len(X)
    cols = len(X[0])
    return [sum(X[i][j] for i in range(n)) / n for j in range(cols)]

def get_cov(X_centered):
    n = len(X_centered)
    cols = len(X_centered[0])
    cov = [[0.0] * cols for _ in range(cols)]
    for i in range(cols):
        for j in range(cols):
            cov[i][j] = sum(X_centered[k][i] * X_centered[k][j] for k in range(n)) / n
    return cov

def cholesky(A):
    L = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                L[i][j] = math.sqrt(max(0.0, A[i][i] - s))
            else:
                L[i][j] = (A[i][j] - s) / L[j][j]
    return L

def forward_sub(L, b):
    y = [0.0] * 3
    for i in range(3):
        s = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - s) / L[i][i]
    return y

def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def matmul(A, B):
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    C = [[0.0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
    return C

def matvec(A, v):
    m = len(A)
    n = len(A[0])
    return [sum(A[i][j] * v[j] for j in range(n)) for i in range(m)]

def solve_3x3(A, b):
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(3):
        pivot = M[i][i]
        for j in range(i, 4):
            M[i][j] /= pivot
        for k in range(3):
            if k != i:
                factor = M[k][i]
                for j in range(i, 4):
                    M[k][j] -= factor * M[i][j]
    return [M[i][3] for i in range(3)]

def get_mse(W, beta, y):
    n = len(W)
    y_pred = matvec(W, beta)
    return sum((y[i] - y_pred[i]) ** 2 for i in range(n)) / n

def compute_expected_results():
    X = []
    y = []
    data_path = '/home/user/ml_prep/data.csv'
    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            X.append([float(row[0]), float(row[1]), float(row[2])])
            y.append(float(row[3]))

    mu = get_mean(X)
    X_centered = [[X[i][j] - mu[j] for j in range(3)] for i in range(len(X))]
    Sigma = get_cov(X_centered)
    L = cholesky(Sigma)

    W = [forward_sub(L, row) for row in X_centered]

    Wt = transpose(W)
    WtW = matmul(Wt, W)
    Wty = matvec(Wt, y)

    beta = solve_3x3(WtW, Wty)
    mse = get_mse(W, beta, y)

    return {
        "mean": mu,
        "cholesky_lower": L,
        "regression_coeffs": beta,
        "mse": mse
    }

@pytest.fixture(scope="module")
def expected_results():
    return compute_expected_results()

@pytest.fixture(scope="module")
def actual_results():
    results_path = '/home/user/ml_prep/results.json'
    assert os.path.isfile(results_path), f"The results file {results_path} does not exist."
    with open(results_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {results_path} does not contain valid JSON.")

def test_results_keys(actual_results):
    expected_keys = {"mean", "cholesky_lower", "regression_coeffs", "mse"}
    actual_keys = set(actual_results.keys())
    missing = expected_keys - actual_keys
    extra = actual_keys - expected_keys
    assert not missing, f"Missing keys in results.json: {missing}"
    assert not extra, f"Extra keys in results.json: {extra}"

def test_mean_vector(actual_results, expected_results):
    actual = actual_results["mean"]
    expected = expected_results["mean"]
    assert len(actual) == 3, "Mean vector must have exactly 3 elements."
    for i in range(3):
        assert math.isclose(actual[i], expected[i], rel_tol=1e-3, abs_tol=1e-4), \
            f"Mean mismatch at index {i}: expected {expected[i]:.5f}, got {actual[i]:.5f}"

def test_cholesky_lower(actual_results, expected_results):
    actual = actual_results["cholesky_lower"]
    expected = expected_results["cholesky_lower"]
    assert len(actual) == 3, "Cholesky matrix must have exactly 3 rows."
    for i in range(3):
        assert len(actual[i]) == 3, f"Cholesky matrix row {i} must have exactly 3 elements."
        for j in range(3):
            assert math.isclose(actual[i][j], expected[i][j], rel_tol=1e-3, abs_tol=1e-4), \
                f"Cholesky matrix mismatch at ({i}, {j}): expected {expected[i][j]:.5f}, got {actual[i][j]:.5f}"

def test_regression_coeffs(actual_results, expected_results):
    actual = actual_results["regression_coeffs"]
    expected = expected_results["regression_coeffs"]
    assert len(actual) == 3, "Regression coefficients must have exactly 3 elements."
    for i in range(3):
        assert math.isclose(actual[i], expected[i], rel_tol=1e-3, abs_tol=1e-4), \
            f"Regression coefficient mismatch at index {i}: expected {expected[i]:.5f}, got {actual[i]:.5f}"

def test_mse(actual_results, expected_results):
    actual = actual_results["mse"]
    expected = expected_results["mse"]
    assert isinstance(actual, (int, float)), "MSE must be a number."
    assert math.isclose(actual, expected, rel_tol=1e-3, abs_tol=1e-4), \
        f"MSE mismatch: expected {expected:.5f}, got {actual:.5f}"