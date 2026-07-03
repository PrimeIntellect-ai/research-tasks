# test_final_state.py
import os
import json
import csv
import math

def transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def mat_mul(A, B):
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def invert_2x2(M):
    a, b = M[0][0], M[0][1]
    c, d = M[1][0], M[1][1]
    det = a*d - b*c
    return [[d/det, -b/det], [-c/det, a/det]]

def solve_ridge(X, Y, lam=0.05):
    XT = transpose(X)
    XTX = mat_mul(XT, X)
    XTX[0][0] += lam
    XTX[1][1] += lam
    inv = invert_2x2(XTX)
    XTY = mat_mul(XT, Y)
    theta = mat_mul(inv, XTY)
    return [theta[0][0], theta[1][0]]

def read_data(filepath):
    X = []
    Y = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append([float(row['x1']), float(row['x2'])])
            Y.append([float(row['y'])])
    return X, Y

def test_results_json_exists_and_valid():
    """Check if results.json exists and contains the required keys."""
    file_path = '/home/user/results.json'
    assert os.path.isfile(file_path), f"Output file missing: {file_path}"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not a valid JSON file."

    expected_keys = {
        "wt_theta1", "wt_theta2", 
        "mut_theta1", "mut_theta2", 
        "mut_dy_dt_at_10", "wt_f_statistic"
    }
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"results.json is missing keys: {missing_keys}"

def test_correct_values():
    """Derive the expected values and assert they match the student's output."""
    wt_X, wt_Y = read_data('/home/user/wt_data.csv')
    mut_X, mut_Y = read_data('/home/user/mut_data.csv')

    # Calculate Ridge Regression for WT and MUT
    wt_theta = solve_ridge(wt_X, wt_Y, lam=0.05)
    mut_theta = solve_ridge(mut_X, mut_Y, lam=0.05)

    # Calculate mut_dy_dt_at_10
    x1_10, x2_10 = mut_X[9]
    y_10_hat = mut_theta[0] * x1_10 + mut_theta[1] * x2_10
    dy_dt = -0.1 * y_10_hat + mut_theta[0] * x1_10 + mut_theta[1] * x2_10

    # Calculate WT F-statistic
    # H1 SSE
    sse_h1 = 0
    for i in range(len(wt_Y)):
        y_hat = wt_theta[0] * wt_X[i][0] + wt_theta[1] * wt_X[i][1]
        sse_h1 += (wt_Y[i][0] - y_hat) ** 2

    # H0 SSE
    sum_x1_sq = sum(x[0]**2 for x in wt_X)
    sum_x1_y = sum(wt_X[i][0] * wt_Y[i][0] for i in range(len(wt_Y)))
    theta0 = sum_x1_y / (sum_x1_sq + 0.05)

    sse_h0 = 0
    for i in range(len(wt_Y)):
        y_hat = theta0 * wt_X[i][0]
        sse_h0 += (wt_Y[i][0] - y_hat) ** 2

    N = len(wt_Y)
    F = ((sse_h0 - sse_h1) / 1) / (sse_h1 / (N - 2))

    expected = {
        "wt_theta1": round(wt_theta[0], 4),
        "wt_theta2": round(wt_theta[1], 4),
        "mut_theta1": round(mut_theta[0], 4),
        "mut_theta2": round(mut_theta[1], 4),
        "mut_dy_dt_at_10": round(dy_dt, 4),
        "wt_f_statistic": round(F, 4)
    }

    with open('/home/user/results.json', 'r') as f:
        data = json.load(f)

    for key, expected_val in expected.items():
        actual_val = data.get(key)
        assert actual_val is not None, f"Missing {key} in results.json"
        assert math.isclose(actual_val, expected_val, abs_tol=1e-3), \
            f"Value for {key} is incorrect. Expected ~{expected_val}, got {actual_val}"