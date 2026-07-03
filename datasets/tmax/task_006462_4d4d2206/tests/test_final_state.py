# test_final_state.py

import os
import math
import pytest

def test_c_program_exists():
    file_path = "/home/user/analyze_gc.c"
    assert os.path.isfile(file_path), f"The C program {file_path} is missing. You must write the program."

def test_lrt_result_exists_and_correct():
    file_path = "/home/user/lrt_result.txt"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing. Did your program run successfully?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    # Recompute the expected value to be robust
    # Coefficients: c0=1, c1=2, c2=3
    # Z = 3.0 (Simpson's 1/3 rule is exact for quadratics)
    Z = 3.0

    # Read the gc_data.txt to use the actual points in case they were modified
    data_path = "/home/user/gc_data.txt"
    assert os.path.isfile(data_path), f"File {data_path} is missing."

    with open(data_path, "r") as f:
        data_points = [float(line.strip()) for line in f if line.strip()]

    ll_alt = 0.0
    for x in data_points:
        p_alt = (1.0 + 2.0 * x + 3.0 * (x ** 2)) / Z
        ll_alt += math.log(p_alt)

    expected_lrt = 2.0 * ll_alt
    expected_lrt_str = f"{expected_lrt:.5f}"

    assert content == expected_lrt_str, f"Content of {file_path} is incorrect. Expected '{expected_lrt_str}', got '{content}'."