# test_final_state.py

import os
import pytest

def test_cleaned_csv_exists():
    """Check that the cleaned.csv file has been generated."""
    file_path = "/home/user/pipeline/cleaned.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

def test_cleaned_csv_content():
    """Verify the content of cleaned.csv matches the expected output."""
    file_path = "/home/user/pipeline/cleaned.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

    expected_content = [
        "F1,F2,Target",
        "1.0,2.5,0.0",
        "2.0,8.1,1.0",
        "3.0,3.2,0.0",
        "4.0,9.5,1.0",
        "5.0,1.2,0.0"
    ]

    with open(file_path, "r") as f:
        actual_content = [line.strip() for line in f.read().strip().split("\n")]

    assert actual_content == expected_content, (
        f"The content of {file_path} does not match the expected output. "
        f"Expected:\n{expected_content}\nActual:\n{actual_content}"
    )