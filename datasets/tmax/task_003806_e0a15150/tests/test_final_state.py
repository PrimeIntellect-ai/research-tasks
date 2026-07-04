# test_final_state.py

import os
import pytest

def test_c_source_exists():
    """Check if the C source file was created."""
    file_path = "/home/user/clean.c"
    assert os.path.exists(file_path), f"Missing C source file: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"

def test_compiled_binary_exists():
    """Check if the compiled binary exists and is executable."""
    file_path = "/home/user/clean"
    assert os.path.exists(file_path), f"Missing compiled binary: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"
    assert os.access(file_path, os.X_OK), f"Compiled binary is not executable: {file_path}"

def test_summary_csv_exists():
    """Check if the output CSV file was created."""
    file_path = "/home/user/summary.csv"
    assert os.path.exists(file_path), f"Missing output CSV file: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"

def test_summary_csv_content():
    """Check if the output CSV matches the expected ground truth exactly."""
    output_path = "/home/user/summary.csv"
    expected_path = "/home/user/.expected_summary.csv"

    assert os.path.exists(output_path), f"Missing output CSV file: {output_path}"
    assert os.path.exists(expected_path), f"Missing expected CSV file: {expected_path}"

    with open(output_path, "r") as f:
        output_lines = [line.strip() for line in f.readlines() if line.strip()]

    with open(expected_path, "r") as f:
        expected_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(output_lines) == len(expected_lines), (
        f"Row count mismatch. Expected {len(expected_lines)} rows, got {len(output_lines)} rows."
    )

    for i, (out_line, exp_line) in enumerate(zip(output_lines, expected_lines)):
        assert out_line == exp_line, (
            f"Mismatch at line {i + 1}:\nExpected: {exp_line}\nGot:      {out_line}"
        )