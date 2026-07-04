# test_final_state.py

import os
import pytest

def test_processor_c_exists():
    assert os.path.isfile("/home/user/processor.c"), "/home/user/processor.c does not exist."

def test_merged_csv_exists():
    assert os.path.isfile("/home/user/merged.csv"), "/home/user/merged.csv does not exist. Did you run your C program?"

def test_merged_csv_content():
    expected_lines = [
        "1,30.0,IDLE",
        "2,31.0,IDLE",
        "3,32.0,IDLE",
        "4,33.0,IDLE",
        "5,34.0,IDLE",
        "6,33.0,ACTIVE",
        "7,32.0,ACTIVE",
        "8,31.0,ACTIVE",
        "9,30.0,ACTIVE",
        "10,29.0,ACTIVE",
        "11,28.0,ACTIVE",
        "12,28.5,ERROR",
        "13,29.0,ERROR",
        "14,29.5,ERROR",
        "15,30.0,ERROR"
    ]

    with open("/home/user/merged.csv", "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in merged.csv, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines), start=1):
        assert actual == expected, f"Line {i} mismatch: expected '{expected}', got '{actual}'."