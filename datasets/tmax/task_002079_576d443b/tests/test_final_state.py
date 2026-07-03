# test_final_state.py

import os
import pytest

def test_fixed_output_correctness():
    data_path = "/home/user/data.csv"
    output_path = "/home/user/fixed_output.csv"

    assert os.path.isfile(output_path), f"Output file missing: {output_path}. Did you run the executable?"

    with open(data_path, "r") as f:
        data_lines = f.readlines()

    assert len(data_lines) == 10000, "Original data should have 10000 rows."

    # Parse data
    data = []
    for line in data_lines:
        if line.strip():
            data.append([float(x) for x in line.strip().split(',')])

    # Calculate means of first 8000 rows (training set)
    sums = [0.0] * 5
    for i in range(8000):
        for j in range(5):
            sums[j] += data[i][j]

    means = [s / 8000.0 for s in sums]

    # Calculate expected output
    expected_output = []
    for i in range(10000):
        row_str = ",".join(f"{data[i][j] - means[j]:.5f}" for j in range(5))
        expected_output.append(row_str)

    # Read actual output
    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == 10000, f"Expected 10000 rows in output, got {len(actual_lines)}"

    # Check lines
    for i in range(10000):
        assert actual_lines[i] == expected_output[i], (
            f"Mismatch at row {i+1}.\n"
            f"Expected: {expected_output[i]}\n"
            f"Got:      {actual_lines[i]}\n"
            "Ensure you are subtracting the mean of the first 8000 rows from ALL rows, "
            "and formatting as %.5f."
        )

def test_executable_exists():
    exe_path = "/home/user/etl_processor"
    assert os.path.isfile(exe_path), f"Missing compiled executable: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable. Did you compile it correctly?"