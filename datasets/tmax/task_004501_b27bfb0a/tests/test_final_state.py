# test_final_state.py

import os
import re
import pytest

def compute_expected_variance(N):
    m = (N + 1) // 2
    h = 1.0 / (N + 1)
    sigma = 0.1

    sum_sq = 0.0
    for j in range(1, N + 1):
        t_inv = min(m, j) - (m * j) / (N + 1)
        sum_sq += t_inv ** 2

    v = (sigma ** 2) * (h ** 4) * sum_sq
    return f"{v:.6e}"

def test_files_exist():
    assert os.path.isfile("/home/user/thermal/variance_solver.go"), "variance_solver.go is missing"
    assert os.path.isfile("/home/user/run_meshes.sh"), "run_meshes.sh is missing"
    assert os.path.isfile("/home/user/results.log"), "results.log is missing"
    assert os.path.isfile("/home/user/thermal/go.mod"), "Go module not initialized (go.mod missing)"

def test_script_executable():
    assert os.access("/home/user/run_meshes.sh", os.X_OK), "run_meshes.sh is not executable"

def test_results_log_content():
    with open("/home/user/results.log", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_Ns = [3, 9, 19, 49, 99]
    assert len(lines) == len(expected_Ns), f"Expected {len(expected_Ns)} lines in results.log, found {len(lines)}"

    for i, N in enumerate(expected_Ns):
        expected_var = compute_expected_variance(N)

        # Allow slight rounding differences for float formatting
        if N == 19:
            allowed_vars = ["1.039062e-05", "1.039063e-05"]
            pattern = rf"^N={N},\s*Var=({allowed_vars[0]}|{allowed_vars[1]})$"
            match = re.match(pattern, lines[i])
            assert match, f"Line {i+1} mismatch. Expected N={N}, Var=1.039062e-05 or 1.039063e-05, got: {lines[i]}"
        else:
            expected_line = f"N={N}, Var={expected_var}"
            # Allow optional space after comma
            pattern = rf"^N={N},\s*Var={expected_var}$"
            match = re.match(pattern, lines[i])
            assert match, f"Line {i+1} mismatch. Expected {expected_line}, got: {lines[i]}"