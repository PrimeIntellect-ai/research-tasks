# test_final_state.py
import os
import pytest

def compute_expected_tv():
    """
    Recompute the expected Total Variation distance using pure Python (stdlib only)
    to avoid relying on opaque constants or external libraries like numpy/h5py.
    """
    N = 50

    def simulate(D, dt, steps):
        P = [[0.0] * N for _ in range(N)]
        P[25][25] = 1.0  # Initial condition at N//2

        for _ in range(steps):
            P_new = [[P[i][j] for j in range(N)] for i in range(N)]
            for i in range(1, N - 1):
                for j in range(1, N - 1):
                    lap = P[i-1][j] + P[i+1][j] + P[i][j-1] + P[i][j+1] - 4.0 * P[i][j]
                    P_new[i][j] += D * dt * lap
            P = P_new
        return P

    # Simulate expected out.h5 (D=0.1, dt=2.5, steps=4)
    P_out = simulate(0.1, 2.5, 4)

    # Simulate ref.h5 (D=0.12, dt=1.0, steps=10)
    P_ref = simulate(0.12, 1.0, 10)

    tv_dist = 0.0
    for i in range(N):
        for j in range(N):
            tv_dist += abs(P_out[i][j] - P_ref[i][j])
    tv_dist *= 0.5

    return tv_dist

def test_simulate_markov_c_fixed():
    """Verify that the C code was fixed to use the correct dt value."""
    c_file = "/home/user/simulate_markov.c"
    assert os.path.exists(c_file), f"Missing source file: {c_file}"

    with open(c_file, "r") as f:
        content = f.read()

    assert "2.5" in content, "The C code does not appear to contain the correct max stable dt value (2.5)."

def test_compiled_executable_exists():
    """Verify that the C code was recompiled."""
    exe_file = "/home/user/simulate_markov"
    assert os.path.exists(exe_file), f"Missing compiled executable: {exe_file}"
    assert os.access(exe_file, os.X_OK), f"File is not executable: {exe_file}"

def test_out_h5_exists():
    """Verify that the simulation was run and produced out.h5."""
    out_file = "/home/user/out.h5"
    assert os.path.exists(out_file), f"Missing output file: {out_file}"

def test_tv_distance_result():
    """Verify that the calculated TV distance matches the expected value."""
    result_file = "/home/user/tv_distance.txt"
    assert os.path.exists(result_file), f"Missing result file: {result_file}"

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content, f"Result file {result_file} is empty."

    try:
        student_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse a float from {result_file}. Found: '{content}'")

    expected_val = compute_expected_tv()
    expected_str = f"{expected_val:.4f}"

    assert f"{student_val:.4f}" == expected_str, (
        f"Incorrect TV distance. Expected {expected_str}, but got {student_val:.4f}"
    )