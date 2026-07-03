# test_final_state.py
import os
import pytest

def test_c_source_exists():
    source_path = "/home/user/process_etl.c"
    assert os.path.isfile(source_path), f"C source file {source_path} does not exist."

def test_executable_exists():
    executable_path = "/home/user/process_etl"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist. Did you compile your C program?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_clean_data_output():
    output_path = "/home/user/clean_data.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did you run your C program?"

    expected_lines = [
        "101,alice,45.5,2",
        "102,bob,45.5,3",
        "103,charlie,50.0,4",
        "104,dave,50.0,3"
    ]

    with open(output_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} rows in {output_path}, but found {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Row {i+1} in {output_path} does not match expected output.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )