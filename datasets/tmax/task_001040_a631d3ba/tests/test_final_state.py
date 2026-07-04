# test_final_state.py

import os
import pytest

def test_process_data_c_exists():
    assert os.path.isfile("/home/user/process_data.c"), "/home/user/process_data.c is missing."

def test_run_experiments_sh_exists():
    assert os.path.isfile("/home/user/run_experiments.sh"), "/home/user/run_experiments.sh is missing."

def test_results_log_exists_and_correct():
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. Did you run the script?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "File: exp1.csv | Valid: 3, Missing: 1, Outliers: 1, Final Mean: 4.84",
        "File: exp2.csv | Valid: 2, Missing: 2, Outliers: 0, Final Mean: 4.76"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {log_path} is incorrect.\nExpected: {expected}\nActual: {actual}"