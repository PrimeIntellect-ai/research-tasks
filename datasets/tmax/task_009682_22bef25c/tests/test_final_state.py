# test_final_state.py

import os
import math
import pytest

def test_process_data_executable():
    path = "/home/user/process_data"
    assert os.path.isfile(path), f"Executable missing: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_csv_outputs_exist_and_correct_length():
    train_path = "/home/user/train.csv"
    test_path = "/home/user/test.csv"

    assert os.path.isfile(train_path), f"Missing {train_path}"
    assert os.path.isfile(test_path), f"Missing {test_path}"

    with open(train_path, "r") as f:
        train_lines = f.readlines()
    with open(test_path, "r") as f:
        test_lines = f.readlines()

    assert len(train_lines) == 801, f"Expected 801 lines in train.csv, got {len(train_lines)}"
    assert len(test_lines) == 201, f"Expected 201 lines in test.csv, got {len(test_lines)}"

    assert train_lines[0].strip() == "id,normalized_value", "Incorrect header in train.csv"
    assert test_lines[0].strip() == "id,normalized_value", "Incorrect header in test.csv"

def test_data_leak_fixed():
    # Compute expected mean and stddev for the first 800 rows
    # values: 1.5, 3.0, ..., 1200.0
    values = [i * 1.5 for i in range(1, 801)]
    mean = sum(values) / len(values)
    sq_sum = sum((v - mean) ** 2 for v in values)
    stddev = math.sqrt(sq_sum / len(values))

    # Check first row of test.csv (id=801, value=1201.5)
    expected_norm_801 = (1201.5 - mean) / stddev

    test_path = "/home/user/test.csv"
    with open(test_path, "r") as f:
        test_lines = f.readlines()

    first_test_row = test_lines[1].strip()
    parts = first_test_row.split(",")
    assert len(parts) == 2, f"Malformed row in test.csv: {first_test_row}"
    assert parts[0] == "801", f"Expected first test id to be 801, got {parts[0]}"

    actual_norm = float(parts[1])
    assert math.isclose(actual_norm, expected_norm_801, rel_tol=1e-4), \
        f"Data leak not fixed. Expected normalized value ~{expected_norm_801}, got {actual_norm}"

def test_benchmark_script_and_log():
    script_path = "/home/user/benchmark.sh"
    log_path = "/home/user/benchmark_log.txt"

    assert os.path.isfile(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    assert os.path.isfile(log_path), f"Missing {log_path}"
    with open(log_path, "r") as f:
        log_lines = [line.strip() for line in f if line.strip()]

    assert len(log_lines) == 5, f"Expected exactly 5 lines in benchmark_log.txt, got {len(log_lines)}"
    for i, line in enumerate(log_lines):
        assert line == "Run complete", f"Line {i+1} in log is incorrect: {line}"