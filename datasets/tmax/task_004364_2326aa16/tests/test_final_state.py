# test_final_state.py
import os
import pytest

def test_output_csv_exists():
    assert os.path.isfile("/home/user/output.csv"), "The file /home/user/output.csv was not created."

def test_output_csv_content():
    expected_rows = [
        "1,0,7,0.75",
        "2,1,8,0.75",
        "3,0,1,0.67",
        "4,1,2,0.67",
        "5,0,1,0.67",
        "6,1,2,0.33",
        "7,0,1,0.75",
        "8,1,2,0.75"
    ]

    with open("/home/user/output.csv", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_rows), f"Expected {len(expected_rows)} lines in output.csv, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_rows)):
        assert actual == expected, f"Mismatch at line {i+1}: expected '{expected}', got '{actual}'."

def test_c_source_exists():
    assert os.path.isfile("/home/user/organizer.c"), "The C source file /home/user/organizer.c was not found."