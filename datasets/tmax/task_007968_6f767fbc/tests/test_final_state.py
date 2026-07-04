# test_final_state.py
import os
import pytest

def test_c_source_code_exists():
    path = "/home/user/rolling_stat.c"
    assert os.path.exists(path), f"C source file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

def test_c_executable_exists():
    path = "/home/user/rolling_stat"
    assert os.path.exists(path), f"Compiled executable {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_processed_data_output():
    path = "/home/user/processed_data.csv"
    assert os.path.exists(path), f"Output file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

    expected_lines = [
        "S1,10,10.00",
        "S1,30,15.00",
        "S1,50,20.00",
        "S1,60,30.00",
        "S2,5,25.00",
        "S2,15,15.00",
        "S2,25,15.00"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {path} do not match the expected processed output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )