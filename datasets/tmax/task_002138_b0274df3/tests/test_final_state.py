# test_final_state.py
import os
import math
import pytest

def transpose(mat):
    return [list(row) for row in zip(*mat)]

def mat_mul(A, B):
    return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]

def add_mat(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def invert_3x3(m):
    det = (m[0][0] * (m[1][1] * m[2][2] - m[2][1] * m[1][2]) -
           m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
           m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    inv = [
        [(m[1][1] * m[2][2] - m[2][1] * m[1][2]) / det,
         (m[0][2] * m[2][1] - m[0][1] * m[2][2]) / det,
         (m[0][1] * m[1][2] - m[0][2] * m[1][1]) / det],
        [(m[1][2] * m[2][0] - m[1][0] * m[2][2]) / det,
         (m[0][0] * m[2][2] - m[0][2] * m[2][0]) / det,
         (m[1][0] * m[0][2] - m[0][0] * m[1][2]) / det],
        [(m[1][0] * m[2][1] - m[2][0] * m[1][1]) / det,
         (m[2][0] * m[0][1] - m[0][0] * m[2][1]) / det,
         (m[0][0] * m[1][1] - m[1][0] * m[0][1]) / det]
    ]
    return inv

def get_expected_u():
    X = [
        [1.0, 2.0, 2.001],
        [1.0, 3.0, 3.002],
        [1.0, 4.0, 4.001],
        [1.0, 5.0, 5.003],
        [1.0, 6.0, 6.002]
    ]
    y = [[4.1], [6.2], [8.0], [10.1], [11.9]]

    X_T = transpose(X)
    X_T_X = mat_mul(X_T, X)

    lam = 0.05
    lam_I = [
        [lam, 0.0, 0.0],
        [0.0, lam, 0.0],
        [0.0, 0.0, lam]
    ]

    A = add_mat(X_T_X, lam_I)
    A_inv = invert_3x3(A)

    X_T_y = mat_mul(X_T, y)
    theta_mat = mat_mul(A_inv, X_T_y)
    theta = [theta_mat[0][0], theta_mat[1][0], theta_mat[2][0]]

    dt = 0.001
    steps = int(10.0 / dt)
    u = 1.0
    t = 0.0

    for _ in range(steps):
        du = theta[0] * u + theta[1] * math.sin(t) + theta[2] * math.cos(t)
        u += du * dt
        t += dt

    return u

def test_trajectory_png_exists():
    png_path = "/home/user/ode_fitter/trajectory.png"
    assert os.path.exists(png_path), f"File {png_path} does not exist."
    assert os.path.isfile(png_path), f"Path {png_path} is not a file."

    with open(png_path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", f"File {png_path} is not a valid PNG file."

def test_final_u_txt_value():
    txt_path = "/home/user/ode_fitter/final_u.txt"
    assert os.path.exists(txt_path), f"File {txt_path} does not exist."
    assert os.path.isfile(txt_path), f"Path {txt_path} is not a file."

    with open(txt_path, "r") as f:
        content = f.read().strip()

    try:
        actual_u = float(content)
    except ValueError:
        pytest.fail(f"Content of {txt_path} is not a valid float: '{content}'")

    expected_u = get_expected_u()

    assert abs(actual_u - expected_u) <= 0.01, \
        f"Value in {txt_path} ({actual_u}) deviates from expected ({expected_u:.4f}) by more than 0.01."