# test_final_state.py

import os
import ctypes
import math

def compute_expected_matrix():
    # Emulate 32-bit float Kahan summation
    def kahan_sum(k):
        dt = ctypes.c_float(0.001)
        y = ctypes.c_float(k)
        sum_val = ctypes.c_float(0.0)
        c = ctypes.c_float(0.0)

        for _ in range(100000):
            dy = ctypes.c_float(ctypes.c_float(-0.01).value * y.value * dt.value)
            y = ctypes.c_float(y.value + dy.value)
            y_dt = ctypes.c_float(y.value * dt.value)
            y_val = ctypes.c_float(y_dt.value - c.value)
            t = ctypes.c_float(sum_val.value + y_val.value)
            c = ctypes.c_float((t.value - sum_val.value) - y_val.value)
            sum_val = t

        return sum_val.value

    matrix = [[0.0]*10 for _ in range(10)]
    for i in range(10):
        for j in range(10):
            matrix[i][j] = kahan_sum(i + j + 1)
    return matrix

def compute_largest_singular_value(matrix):
    # The matrix is symmetric and has positive entries, so the largest singular value
    # is the largest eigenvalue, which can be found via power iteration.
    v = [1.0] * 10
    for _ in range(1000):
        v_new = [sum(matrix[i][j] * v[j] for j in range(10)) for i in range(10)]
        norm = math.sqrt(sum(x * x for x in v_new))
        v = [x / norm for x in v_new]

    # Rayleigh quotient
    eigenvalue = sum(v[i] * sum(matrix[i][j] * v[j] for j in range(10)) for i in range(10))
    return eigenvalue

def test_kahan_summation_implemented():
    file_path = "/home/user/data_gen.c"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read()

    # Check that naive summation is removed and Kahan algorithm is present
    assert "sum += y * dt;" not in content, "Naive summation 'sum += y * dt;' is still in data_gen.c"
    assert "c =" in content or "c=" in content, "Kahan summation variable 'c' seems missing."
    assert "t =" in content or "t=" in content, "Kahan summation variable 't' seems missing."

def test_matrix_file_exists():
    assert os.path.exists("/home/user/matrix.txt"), "/home/user/matrix.txt was not created."

def test_result_file_correct():
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"File {result_path} does not exist."

    with open(result_path, 'r') as f:
        result_str = f.read().strip()

    assert result_str, f"File {result_path} is empty."

    try:
        result_val = float(result_str)
    except ValueError:
        assert False, f"Content of {result_path} is not a valid float: '{result_str}'"

    # Check if formatted to 4 decimal places
    assert "." in result_str and len(result_str.split(".")[1]) == 4, f"Result '{result_str}' is not formatted to exactly 4 decimal places."

    expected_matrix = compute_expected_matrix()
    expected_sv = compute_largest_singular_value(expected_matrix)
    expected_sv_rounded = round(expected_sv, 4)

    assert math.isclose(result_val, expected_sv_rounded, abs_tol=0.0002), \
        f"Expected largest singular value approximately {expected_sv_rounded:.4f}, but got {result_val}"