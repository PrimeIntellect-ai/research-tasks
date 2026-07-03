# test_final_state.py
import os
import pytest
import math

def test_similarity_csv_exists():
    file_path = "/home/user/ml_prep/similarity.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. Did you run the Rust project?"

def test_similarity_csv_contents():
    file_path = "/home/user/ml_prep/similarity.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 rows in similarity.csv, but found {len(lines)}."

    expected_matrix = [
        [10.0, 6.0, 1.5],
        [6.0, 8.0, 3.0],
        [1.5, 3.0, 4.5]
    ]

    for i, line in enumerate(lines):
        parts = line.split(",")
        assert len(parts) == 3, f"Row {i+1} does not have exactly 3 columns: '{line}'"

        for j, val_str in enumerate(parts):
            try:
                val = float(val_str)
            except ValueError:
                pytest.fail(f"Could not parse value '{val_str}' as a float at row {i+1}, col {j+1}")

            expected_val = expected_matrix[i][j]
            assert math.isclose(val, expected_val, rel_tol=1e-5, abs_tol=1e-5), \
                f"Value mismatch at row {i+1}, col {j+1}. Expected {expected_val}, got {val}"