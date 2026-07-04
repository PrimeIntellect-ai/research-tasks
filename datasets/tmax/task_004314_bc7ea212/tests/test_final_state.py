# test_final_state.py

import os
import pytest

def test_source_code_exists():
    """Test that the C source code exists."""
    file_path = "/home/user/audit_processor.c"
    assert os.path.exists(file_path), f"The source code file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_executable_exists():
    """Test that the compiled executable exists."""
    file_path = "/home/user/audit_processor"
    assert os.path.exists(file_path), f"The executable {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."
    assert os.access(file_path, os.X_OK), f"The file {file_path} is not executable."

def test_output_csv_exists():
    """Test that the output CSV file exists."""
    file_path = "/home/user/processed_audit.csv"
    assert os.path.exists(file_path), f"The output file {file_path} is missing. Did the program run successfully?"
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_output_csv_content():
    """Test that the output CSV file contains the correct processed records."""
    file_path = "/home/user/processed_audit.csv"
    if not os.path.exists(file_path):
        pytest.fail(f"Cannot verify content because {file_path} is missing.")

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "1696161600,admin,UPDATE,100,NONE",
        "1696161610,dev,READ,100,NONE",
        "1696161615,admin,DELETE,105,NONE",
        "1696161620,admin,UPDATE,110,NONE",
        "1696161625,admin,UPDATE,115,ANOMALY_RATE",
        "1696161630,admin,UPDATE,180,ANOMALY_RATE|ANOMALY_VERSION",
        "1696161635,dev,WRITE,180,NONE",
        "1696161710,admin,READ,185,NONE"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output CSV, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"