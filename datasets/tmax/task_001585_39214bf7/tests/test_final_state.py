# test_final_state.py

import os
import math

def read_matrix(path):
    """Reads a space-separated text file into a 2D list of floats."""
    with open(path, 'r') as f:
        return [[float(x) for x in line.split()] for line in f if line.strip()]

def test_openblas_installed():
    """Test that OpenBLAS headers are installed."""
    # Check common locations for cblas.h
    header_found = False
    for root, dirs, files in os.walk('/usr/include'):
        if 'cblas.h' in files:
            header_found = True
            break
    assert header_found, "cblas.h not found in /usr/include. OpenBLAS development headers may not be installed."

def test_c_source_exists():
    """Test that the C source code exists."""
    assert os.path.isfile('/home/user/validate_pca.c'), "Source file /home/user/validate_pca.c is missing."

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = '/home/user/validate_pca'
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_max_diff_correct():
    """Test that max_diff.txt contains the correctly computed maximum absolute difference."""
    diff_file = '/home/user/max_diff.txt'
    assert os.path.isfile(diff_file), f"Output file {diff_file} is missing."

    # Compute expected value using standard Python
    X = read_matrix('/home/user/X.txt')
    P = read_matrix('/home/user/P.txt')
    Y_ref = read_matrix('/home/user/Y_ref.txt')

    # Matrix multiplication: Y = X @ P
    Y_computed = []
    for i in range(len(X)):
        row = []
        for j in range(len(P[0])):
            val = sum(X[i][k] * P[k][j] for k in range(len(X[0])))
            row.append(val)
        Y_computed.append(row)

    # Compute max absolute difference
    max_diff = 0.0
    for i in range(len(Y_ref)):
        for j in range(len(Y_ref[0])):
            diff = abs(Y_computed[i][j] - Y_ref[i][j])
            if diff > max_diff:
                max_diff = diff

    # Read student's output
    with open(diff_file, 'r') as f:
        content = f.read().strip()

    try:
        student_diff = float(content)
    except ValueError:
        assert False, f"Contents of {diff_file} could not be parsed as a float: '{content}'"

    # Compare values allowing a small tolerance due to floating point arithmetic (e.g. 1e-5)
    assert math.isclose(student_diff, max_diff, abs_tol=1.5e-5), \
        f"Expected max difference around {max_diff:.6f}, but got {student_diff}"