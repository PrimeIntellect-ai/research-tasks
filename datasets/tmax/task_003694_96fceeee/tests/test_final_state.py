# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    source_path = "/home/user/track_config.c"
    assert os.path.exists(source_path), f"Source file {source_path} is missing."
    assert os.path.isfile(source_path), f"{source_path} is not a file."
    with open(source_path, "r") as f:
        content = f.read()
    assert len(content.strip()) > 0, f"{source_path} is empty."
    assert "#include" in content, f"{source_path} does not look like a C program."

def test_executable_exists():
    exec_path = "/home/user/track_config"
    assert os.path.exists(exec_path), f"Executable {exec_path} is missing."
    assert os.path.isfile(exec_path), f"{exec_path} is not a file."
    assert os.access(exec_path, os.X_OK), f"{exec_path} is not executable."

def test_csv_output_correct():
    csv_path = "/home/user/latest_configs.csv"
    assert os.path.exists(csv_path), f"Output CSV {csv_path} is missing."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    expected_csv = """server,key,value
srv-01,DB_HOST,primary-db-v2
srv-01,WORKER_THREADS,16
srv-02,DB_HOST,replica-db
srv-02,WORKER_THREADS,8
srv-03,CACHE_SIZE,1024
srv-03,WORKER_THREADS,8"""

    with open(csv_path, "r") as f:
        actual_csv = f.read().strip()

    # Compare line by line to give better error messages
    expected_lines = expected_csv.splitlines()
    actual_lines = actual_csv.splitlines()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in CSV, got {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual.strip() == expected.strip(), f"Mismatch at row {i+1}: expected '{expected.strip()}', got '{actual.strip()}'."