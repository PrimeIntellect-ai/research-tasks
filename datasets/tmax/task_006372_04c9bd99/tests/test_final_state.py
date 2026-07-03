# test_final_state.py

import os
import json
import math
import pytest

def invert_matrix(M):
    n = len(M)
    # Augment with identity
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(M)]
    for i in range(n):
        # Find pivot
        pivot_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[pivot_row] = A[pivot_row], A[i]

        pivot = A[i][i]
        if abs(pivot) < 1e-12:
            raise ValueError("Matrix is singular")

        for j in range(2 * n):
            A[i][j] /= pivot

        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(2 * n):
                    A[k][j] -= factor * A[i][j]
    return [row[n:] for row in A]

def transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(A[0]))) for j in range(len(B[0]))] for i in range(len(A))]

def test_results_json_exists_and_correct():
    csv_path = "/home/user/data/sensors.csv"
    assert os.path.isfile(csv_path), f"Input file {csv_path} is missing."

    vibration_raw = []
    temperature = []
    pressure = []
    risk = []

    with open(csv_path, 'r') as f:
        header = f.readline()
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(',')
            vibration_raw.append(parts[1])
            temperature.append(float(parts[2]))
            pressure.append(float(parts[3]))
            risk.append(float(parts[4]))

    # Impute vibration
    valid_vibes = [int(v) for v in vibration_raw if v != "NaN"]
    mean_vibe = sum(valid_vibes) / len(valid_vibes)
    # Round half away from zero
    imputed_vibe = math.floor(mean_vibe + 0.5)

    vibration = [imputed_vibe if v == "NaN" else int(v) for v in vibration_raw]

    # Construct X and y
    X = [[1.0, v, t, p] for v, t, p in zip(vibration, temperature, pressure)]
    y = [[r] for r in risk]

    # OLS: w = (X^T X)^-1 X^T y
    X_T = transpose(X)
    X_T_X = matmul(X_T, X)
    inv_X_T_X = invert_matrix(X_T_X)
    X_T_y = matmul(X_T, y)
    w_mat = matmul(inv_X_T_X, X_T_y)
    weights = [w[0] for w in w_mat]

    # Predictions
    y_hat = [sum(X[i][j] * weights[j] for j in range(4)) for i in range(len(X))]
    mean_y_hat = sum(y_hat) / len(y_hat)

    # Standard deviation and standard error
    var_y_hat = sum((yi - mean_y_hat)**2 for yi in y_hat) / (len(y_hat) - 1)
    std_y_hat = math.sqrt(var_y_hat)
    se = std_y_hat / math.sqrt(len(y_hat))

    # CI
    ci_lower = mean_y_hat - 1.96 * se
    ci_upper = mean_y_hat + 1.96 * se

    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    assert "weights" in results, "'weights' key missing in results.json"
    assert "mean_prediction" in results, "'mean_prediction' key missing in results.json"
    assert "ci_lower" in results, "'ci_lower' key missing in results.json"
    assert "ci_upper" in results, "'ci_upper' key missing in results.json"

    res_weights = results["weights"]
    assert len(res_weights) == 4, "Weights array should have exactly 4 elements."

    for i in range(4):
        assert math.isclose(res_weights[i], weights[i], abs_tol=1e-4), \
            f"Weight {i} mismatch. Expected {weights[i]}, got {res_weights[i]}"

    assert math.isclose(results["mean_prediction"], mean_y_hat, abs_tol=1e-4), \
        f"Mean prediction mismatch. Expected {mean_y_hat}, got {results['mean_prediction']}"

    assert math.isclose(results["ci_lower"], ci_lower, abs_tol=1e-4), \
        f"CI lower bound mismatch. Expected {ci_lower}, got {results['ci_lower']}"

    assert math.isclose(results["ci_upper"], ci_upper, abs_tol=1e-4), \
        f"CI upper bound mismatch. Expected {ci_upper}, got {results['ci_upper']}"