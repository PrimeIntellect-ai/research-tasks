# test_final_state.py

import os
import math

def test_shared_library_exists():
    so_path = "/home/user/math_utils/libsystemsolver.so"
    assert os.path.exists(so_path), f"Shared library {so_path} is missing. Did you compile the C library correctly?"

def test_c_source_exists():
    c_path = "/home/user/src/compute_boundaries.c"
    assert os.path.exists(c_path), f"Source file {c_path} is missing."

def test_executable_exists():
    bin_path = "/home/user/bin/compute_boundaries"
    assert os.path.exists(bin_path), f"Executable {bin_path} is missing. Did you compile your C program?"
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable."

def det3(m):
    return (m[0][0] * (m[1][1]*m[2][2] - m[1][2]*m[2][1]) -
            m[0][1] * (m[1][0]*m[2][2] - m[1][2]*m[2][0]) +
            m[0][2] * (m[1][0]*m[2][1] - m[1][1]*m[2][0]))

def test_boundaries_output():
    csv_path = "/home/user/data/density_points.csv"
    assert os.path.exists(csv_path), f"CSV file {csv_path} is missing."

    points = []
    with open(csv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(float, line.split(','))
                points.append((x, y))

    assert len(points) == 3, "Expected exactly 3 points in CSV."

    # Setup matrix A and vector B for ax^2 + bx + c = y
    A = [[p[0]**2, p[0], 1.0] for p in points]
    B = [p[1] for p in points]

    detA = det3(A)
    assert detA != 0, "Matrix is singular, cannot solve."

    Ax = [[B[i] if j == 0 else A[i][j] for j in range(3)] for i in range(3)]
    Ay = [[B[i] if j == 1 else A[i][j] for j in range(3)] for i in range(3)]
    Az = [[B[i] if j == 2 else A[i][j] for j in range(3)] for i in range(3)]

    a = det3(Ax) / detA
    b = det3(Ay) / detA
    c = det3(Az) / detA

    # Solve ax^2 + bx + (c - 0.5) = 0
    c_adj = c - 0.5
    discriminant = b**2 - 4*a*c_adj
    assert discriminant >= 0, "No real roots found for y=0.5."

    root1 = (-b - math.sqrt(discriminant)) / (2*a)
    root2 = (-b + math.sqrt(discriminant)) / (2*a)

    r_min = min(root1, root2)
    r_max = max(root1, root2)

    expected_output = f"{r_min:.6f},{r_max:.6f}"

    res_path = "/home/user/results/boundaries.txt"
    assert os.path.exists(res_path), f"Results file {res_path} is missing. Did your program run successfully?"

    with open(res_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Expected output '{expected_output}', but got '{actual_output}' in {res_path}."