# test_final_state.py
import os
import math
import csv

def test_eigen_installed():
    eigen_dir = "/home/user/eigen/Eigen"
    assert os.path.isdir(eigen_dir), f"Eigen directory {eigen_dir} does not exist. Did you download and extract it correctly?"

    # Check for a common Eigen header
    dense_header = os.path.join(eigen_dir, "Dense")
    assert os.path.isfile(dense_header), f"Eigen/Dense header not found at {dense_header}. Is the directory structure correct?"

def test_executable_compiled():
    exe_path = "/home/user/prep_data"
    assert os.path.isfile(exe_path), f"Executable {exe_path} not found. Did you compile the C++ code?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def kl_divergence(p, q):
    return sum(p[i] * math.log(p[i] / q[i]) for i in range(len(p)) if p[i] > 0 and q[i] > 0)

def js_divergence(p, q):
    m = [0.5 * (p[i] + q[i]) for i in range(len(p))]
    return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)

def det3x3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
            m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
            m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

def inv3x3(m):
    d = det3x3(m)
    inv = [[0]*3 for _ in range(3)]
    inv[0][0] = (m[1][1] * m[2][2] - m[1][2] * m[2][1]) / d
    inv[0][1] = (m[0][2] * m[2][1] - m[0][1] * m[2][2]) / d
    inv[0][2] = (m[0][1] * m[1][2] - m[0][2] * m[1][1]) / d
    inv[1][0] = (m[1][2] * m[2][0] - m[1][0] * m[2][2]) / d
    inv[1][1] = (m[0][0] * m[2][2] - m[0][2] * m[2][0]) / d
    inv[1][2] = (m[0][2] * m[1][0] - m[0][0] * m[1][2]) / d
    inv[2][0] = (m[1][0] * m[2][1] - m[1][1] * m[2][0]) / d
    inv[2][1] = (m[0][1] * m[2][0] - m[0][0] * m[2][1]) / d
    inv[2][2] = (m[0][0] * m[1][1] - m[0][1] * m[1][0]) / d
    return inv

def test_training_features_output():
    csv_path = "/home/user/training_features.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} not found. Did you run the executable?"

    # Compute expected matrix
    spectra = [
        [0.2, 0.5, 0.3],
        [0.1, 0.6, 0.3],
        [0.4, 0.4, 0.2]
    ]
    n = 3
    A = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            weight = math.exp(-js_divergence(spectra[i], spectra[j]))
            A[i][j] = weight
            A[j][i] = weight

    D = [[0.0]*n for _ in range(n)]
    for i in range(n):
        D[i][i] = sum(A[i])

    L = [[D[i][j] - A[i][j] for j in range(n)] for i in range(n)]

    # Add regularization
    for i in range(n):
        L[i][i] += 1e-5

    expected_L_inv = inv3x3(L)

    # Read actual output
    actual_L_inv = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                actual_L_inv.append([float(x) for x in row])

    assert len(actual_L_inv) == n, f"Expected {n} rows in CSV, got {len(actual_L_inv)}"
    for i in range(n):
        assert len(actual_L_inv[i]) == n, f"Expected {n} columns in row {i}, got {len(actual_L_inv[i])}"
        for j in range(n):
            expected_val = expected_L_inv[i][j]
            actual_val = actual_L_inv[i][j]
            # Use a relative tolerance for floating point comparison
            assert math.isclose(actual_val, expected_val, rel_tol=1e-2, abs_tol=1e-2), \
                f"Matrix mismatch at ({i}, {j}): expected approx {expected_val}, got {actual_val}. Did you add 1e-5 * I to L?"