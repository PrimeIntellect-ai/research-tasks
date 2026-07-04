# test_final_state.py
import os
import csv
import math

def matmul(A, B):
    return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]

def transpose(A):
    return [list(col) for col in zip(*A)]

def invert_matrix(A):
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    for i in range(n):
        # Partial pivot
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]

        pivot = M[i][i]
        if abs(pivot) < 1e-12:
            raise ValueError("Matrix is singular")

        for j in range(i, 2*n):
            M[i][j] /= pivot

        for k in range(n):
            if k == i:
                continue
            factor = M[k][i]
            for j in range(i, 2*n):
                M[k][j] -= factor * M[i][j]

    return [row[n:] for row in M]

def calculate_expected_ols(csv_path):
    X = []
    y = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append([1.0, float(row['cpu_util']), float(row['mem_util']), float(row['io_wait'])])
            y.append([float(row['response_time'])])

    Xt = transpose(X)
    XtX = matmul(Xt, X)
    Xty = matmul(Xt, y)

    XtX_inv = invert_matrix(XtX)
    beta = matmul(XtX_inv, Xty)
    return [b[0] for b in beta]

def test_files_exist():
    assert os.path.exists("/home/user/perf_model.c"), "/home/user/perf_model.c is missing."
    assert os.path.exists("/home/user/perf_model"), "/home/user/perf_model executable is missing."
    assert os.path.exists("/home/user/perf_analysis.log"), "/home/user/perf_analysis.log is missing."

def test_analysis_log_contents():
    log_path = "/home/user/perf_analysis.log"
    assert os.path.exists(log_path), "Log file missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 2, "Log file must contain at least two lines."

    ols_line = None
    mcmc_line = None
    for line in lines:
        if line.startswith("OLS_COEFS:"):
            ols_line = line
        elif line.startswith("MCMC_MEANS:"):
            mcmc_line = line

    assert ols_line is not None, "Missing OLS_COEFS line in log."
    assert mcmc_line is not None, "Missing MCMC_MEANS line in log."

    try:
        ols_vals = [float(x) for x in ols_line.split()[1:]]
        mcmc_vals = [float(x) for x in mcmc_line.split()[1:]]
    except ValueError:
        assert False, "Could not parse float values from log lines."

    assert len(ols_vals) == 4, "Expected 4 coefficients for OLS."
    assert len(mcmc_vals) == 4, "Expected 4 coefficients for MCMC."

    # Calculate ground truth
    expected_ols = calculate_expected_ols("/home/user/perf_data.csv")

    # Check OLS
    for i, (val, exp) in enumerate(zip(ols_vals, expected_ols)):
        assert abs(val - exp) < 1e-2, f"OLS coefficient {i} ({val}) differs from expected ({exp}) by more than 1e-2."

    # Check MCMC against OLS
    for i, (m_val, o_val) in enumerate(zip(mcmc_vals, ols_vals)):
        assert abs(m_val - o_val) < 0.1, f"MCMC mean {i} ({m_val}) differs from OLS ({o_val}) by more than 0.1."