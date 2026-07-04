# test_final_state.py

import os
import pytest

def test_libcalc_so_exists():
    file_path = "/home/user/libcalc.so"
    assert os.path.isfile(file_path), f"Shared library {file_path} is missing. Did you compile calc.c?"

def test_processor_rs_exists():
    file_path = "/home/user/processor.rs"
    assert os.path.isfile(file_path), f"Rust source file {file_path} is missing."

def test_results_log_exists():
    file_path = "/home/user/results.log"
    assert os.path.isfile(file_path), f"Results log {file_path} is missing. Did you execute your Rust program?"

def test_results_log_content():
    file_path = "/home/user/results.log"
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "1 + 1 = 2.0",
        "10 + 20 = 30.0",
        "100 + 200 = 300.0"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in results.log, but found {len(lines)}. Check your rate limiting and validation logic."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in results.log does not match expected output. Expected '{expected}', got '{actual}'."