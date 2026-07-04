# test_final_state.py

import os
import math
import csv

def get_expected_error(N):
    """
    Computes the expected L2 error for the 1D Poisson equation solver
    using a standard second-order central finite difference scheme.
    Uses only standard library (Thomas algorithm for tridiagonal system).
    """
    h = 1.0 / N
    n = N - 1
    x_int = [i * h for i in range(1, N)]

    u_exact = [math.sin(2 * math.pi * x) for x in x_int]

    # RHS b_i = 4 * pi^2 * sin(2 * pi * x_i)
    b = [4 * math.pi**2 * math.sin(2 * math.pi * x) for x in x_int]

    # Tridiagonal system: off-diagonal a = c = -1/h^2, main diagonal d = 2/h^2
    a = -1.0 / h**2
    d = 2.0 / h**2
    c = -1.0 / h**2

    # Thomas algorithm
    c_prime = [0.0] * n
    d_prime = [0.0] * n

    c_prime[0] = c / d
    d_prime[0] = b[0] / d

    for i in range(1, n):
        denom = d - a * c_prime[i-1]
        if i < n - 1:
            c_prime[i] = c / denom
        d_prime[i] = (b[i] - a * d_prime[i-1]) / denom

    u_num = [0.0] * n
    u_num[-1] = d_prime[-1]
    for i in range(n-2, -1, -1):
        u_num[i] = d_prime[i] - c_prime[i] * u_num[i+1]

    error_sq = sum((u_num[i] - u_exact[i])**2 for i in range(n))
    error = math.sqrt(h * error_sq)
    return error

def test_convergence_csv():
    csv_path = "/home/user/results/convergence.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist"

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 5, "CSV should contain a header and 4 rows of data"
    assert rows[0] == ["N", "L2_error"], f"CSV header is incorrect, found: {rows[0]}"

    expected_Ns = [16, 32, 64, 128]
    data_dict = {}
    for row in rows[1:]:
        assert len(row) == 2, f"Invalid row format: {row}"
        try:
            n_val = int(row[0].strip())
            err_val = float(row[1].strip())
            data_dict[n_val] = err_val
        except ValueError:
            assert False, f"Could not parse row values as numbers: {row}"

    for N in expected_Ns:
        assert N in data_dict, f"Missing results for N={N} in CSV"
        expected_err = get_expected_error(N)
        actual_err = data_dict[N]

        # Check relative tolerance of 1e-7
        rel_diff = abs(actual_err - expected_err) / expected_err
        assert rel_diff <= 1e-7, (
            f"L2 error for N={N} is incorrect. "
            f"Expected approx {expected_err:.6e}, got {actual_err:.6e}"
        )

def test_other_files_exist():
    # Check if the virtual environment exists
    assert os.path.isdir("/home/user/sim_env"), "Virtual environment directory missing at /home/user/sim_env"

    # Check if solver and template exist
    assert os.path.exists("/home/user/solver.py"), "solver.py is missing"
    assert os.path.exists("/home/user/template.ipynb"), "template.ipynb is missing"
    assert os.path.exists("/home/user/run_study.sh"), "run_study.sh is missing"

    # Check if intermediate outputs exist
    for N in [16, 32, 64, 128]:
        assert os.path.exists(f"/home/user/results/out_{N}.ipynb"), f"out_{N}.ipynb missing"
        assert os.path.exists(f"/home/user/results/error_{N}.txt"), f"error_{N}.txt missing"