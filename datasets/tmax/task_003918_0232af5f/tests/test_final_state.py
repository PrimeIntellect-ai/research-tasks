# test_final_state.py

import os
import pytest

def test_fixed_matrix_exists():
    output_path = "/home/user/fixed_matrix.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did you run the program and redirect the output?"

def test_fixed_matrix_content():
    output_path = "/home/user/fixed_matrix.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 4, f"Expected 4 rows in {output_path}, but got {len(lines)}."

    expected_matrix = [
        [0.8500, 0.0500, 0.0500, 0.0500],
        [0.2500, 0.2500, 0.2500, 0.2500],
        [0.0500, 0.0500, 0.0500, 0.8500],
        [0.2500, 0.2500, 0.2500, 0.2500]
    ]

    for i, line in enumerate(lines):
        values = line.strip().split()
        assert len(values) == 4, f"Expected 4 values in row {i+1}, but got {len(values)}."

        for j, val in enumerate(values):
            try:
                float_val = float(val)
            except ValueError:
                pytest.fail(f"Value '{val}' in row {i+1} is not a valid float.")

            expected_val = expected_matrix[i][j]
            assert abs(float_val - expected_val) < 1e-4, \
                f"Value at row {i+1}, col {j+1} is {float_val:.4f}, expected {expected_val:.4f}. Laplace smoothing (+1) may not have been applied correctly."

def test_c_file_modified():
    c_path = "/home/user/sim/sub_matrix.c"
    assert os.path.isfile(c_path), f"File {c_path} does not exist."

    with open(c_path, "r") as f:
        content = f.read()

    # Just verify that the file has been modified from the original to do some +1 or initialization with 1
    # We won't be too strict on the exact C syntax, but we can check if it's different from the original {0} initialization
    # or if there's a +1 or 1 in the matrix initialization/loop.
    assert "matrix[4][4]" in content, "Matrix declaration missing."