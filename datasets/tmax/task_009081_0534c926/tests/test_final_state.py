# test_final_state.py

import os
import pytest

def test_process_c_exists():
    file_path = "/home/user/process.c"
    assert os.path.exists(file_path), f"Source file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_output_csv_exists_and_correct():
    file_path = "/home/user/output.csv"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    expected_lines = [
        "ts,sensor_id,location,val",
        "1700000000,S1,North_Wing,12.5",
        "1700000010,S1,North_Wing,12.5",
        "1700000020,S1,North_Wing,15.0",
        "1700000030,S1,North_Wing,15.0",
        "1700000040,S1,North_Wing,14.5",
        "1700000050,S1,North_Wing,14.5",
        "1700000000,S2,South_Wing,0.0",
        "1700000010,S2,South_Wing,8.0",
        "1700000020,S2,South_Wing,8.5",
        "1700000030,S2,South_Wing,8.5",
        "1700000040,S2,South_Wing,8.5",
        "1700000050,S2,South_Wing,8.5"
    ]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i + 1} in {file_path}.\nExpected: {expected}\nActual: {actual}"