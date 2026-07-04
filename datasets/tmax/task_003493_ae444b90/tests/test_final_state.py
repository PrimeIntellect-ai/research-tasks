# test_final_state.py

import os
import re

def parse_matrix_file(filepath):
    matrix = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Extract floats using regex or simple split
            parts = line.split(',')
            if len(parts) != 3:
                raise ValueError(f"Line does not have exactly 3 comma-separated values: {line}")
            row = [float(p.strip()) for p in parts]
            matrix.append(row)
    return matrix

def test_c_source_file_exists():
    c_file = '/home/user/clean_covar.c'
    assert os.path.exists(c_file), f"The C source file {c_file} does not exist."
    assert os.path.isfile(c_file), f"The path {c_file} is not a file."

def test_output_file_exists():
    out_file = '/home/user/expected_covar.txt'
    assert os.path.exists(out_file), f"The output file {out_file} does not exist. Did you run your C program?"
    assert os.path.isfile(out_file), f"The path {out_file} is not a file."

def test_covariance_matrix_correctness():
    expected_file = '/home/user/expected_covar.txt'
    truth_file = '/home/user/ground_truth.txt'

    assert os.path.exists(truth_file), f"Ground truth file {truth_file} is missing."

    try:
        user_matrix = parse_matrix_file(expected_file)
    except Exception as e:
        assert False, f"Failed to parse {expected_file}: {e}"

    try:
        truth_matrix = parse_matrix_file(truth_file)
    except Exception as e:
        assert False, f"Failed to parse {truth_file}: {e}"

    assert len(user_matrix) == 3, f"Expected 3 rows in the covariance matrix, but got {len(user_matrix)}"

    tolerance = 0.0002
    for i in range(3):
        assert len(user_matrix[i]) == 3, f"Expected 3 columns in row {i+1}, but got {len(user_matrix[i])}"
        for j in range(3):
            user_val = user_matrix[i][j]
            truth_val = truth_matrix[i][j]
            diff = abs(user_val - truth_val)
            assert diff <= tolerance, (
                f"Value mismatch at row {i+1}, column {j+1}. "
                f"Expected {truth_val:.4f}, but got {user_val:.4f} (difference {diff:.6f} > {tolerance})"
            )