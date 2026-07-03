# test_final_state.py

import os
import pytest

def solve_expected():
    m = [
        [4.0, 12.0, -16.0],
        [12.0, 37.0, -43.0],
        [-16.0, -43.0, 98.0],
    ]
    y = [1.0, 5.0, -6.0]
    t = 0.0
    t_end = 0.5
    h = 0.001
    tol = 1e-5

    def mat_vec_mul(mat, v):
        out = [0.0] * 3
        for i in range(3):
            out[i] = mat[i][0]*v[0] + mat[i][1]*v[1] + mat[i][2]*v[2]
        return out

    while t < t_end:
        if t + h > t_end:
            h = t_end - t

        my = mat_vec_mul(m, y)
        k1 = [-my[0], -my[1], -my[2]]

        y_euler = [y[0] + h*k1[0], y[1] + h*k1[1], y[2] + h*k1[2]]

        my_euler = mat_vec_mul(m, y_euler)
        k2 = [-my_euler[0], -my_euler[1], -my_euler[2]]

        y_heun = [
            y[0] + h * 0.5 * (k1[0] + k2[0]),
            y[1] + h * 0.5 * (k1[1] + k2[1]),
            y[2] + h * 0.5 * (k1[2] + k2[2]),
        ]

        err = 0.0
        for i in range(3):
            err += (y_heun[i] - y_euler[i])**2
        err = err**0.5 + 1e-12

        h_new = h * (tol / err)**0.5

        if err <= tol:
            t += h
            y = y_heun

        h = max(1e-6, min(h_new, 0.1))

    return y

def test_result_txt_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"{result_path} is missing"

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content, f"{result_path} is empty"

    parts = content.split()
    assert len(parts) == 3, f"{result_path} does not contain exactly 3 space-separated values"

    try:
        y_actual = [float(p) for p in parts]
    except ValueError:
        pytest.fail(f"{result_path} contains non-numeric values")

    y_expected = solve_expected()

    for i in range(3):
        assert abs(y_actual[i] - y_expected[i]) < 1e-4, \
            f"Value at index {i} ({y_actual[i]}) differs from expected ({y_expected[i]:.5f})"

def test_main_rs_bug_fixed():
    main_rs_path = "/home/user/ode_sim/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} is missing"

    with open(main_rs_path, "r") as f:
        content = f.read()

    # Check that the bug is removed
    assert "let h_new = h * (err / tol).powf(0.5);" not in content, \
        "main.rs still contains the inverted error adaptation bug"

    # Check that a valid fix is present
    assert "tol / err" in content or "tol/err" in content or "err.powi(-1)" in content or "err.powf(-1.0)" in content, \
        "main.rs does not contain the expected fix for the step-size adaptation"