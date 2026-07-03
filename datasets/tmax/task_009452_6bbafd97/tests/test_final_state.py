# test_final_state.py

import os
import pytest
import math

def test_executable_exists():
    executable_path = "/home/user/process"
    assert os.path.isfile(executable_path), f"Missing compiled executable: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_stats_txt():
    stats_path = "/home/user/stats.txt"
    assert os.path.isfile(stats_path), f"Missing file: {stats_path}"

    with open(stats_path, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) == 2, f"Expected 2 lines in {stats_path}, got {len(content)}"

    # We allow slight variations in formatting, but numbers should match closely.
    # The prompt asks for exact string matches based on %.4f format.
    expected_f1 = "f1: mean=15.6000, std=2.9394"
    expected_f2 = "f2: mean=25.6000, std=2.9394"

    assert expected_f1 in content[0], f"Line 1 of stats.txt is incorrect. Expected to contain '{expected_f1}', got '{content[0]}'"
    assert expected_f2 in content[1], f"Line 2 of stats.txt is incorrect. Expected to contain '{expected_f2}', got '{content[1]}'"

def test_test_scaled_csv():
    test_scaled_path = "/home/user/test_scaled.csv"
    assert os.path.isfile(test_scaled_path), f"Missing file: {test_scaled_path}"

    with open(test_scaled_path, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) == 3, f"Expected 3 lines (header + 2 rows) in {test_scaled_path}, got {len(content)}"
    assert content[0].strip() == "f1,f2", "Header in test_scaled.csv is incorrect."

    expected_row1 = "-1.2247,-1.2247"
    expected_row2 = "-0.5443,-0.5443"

    assert content[1].strip() == expected_row1, f"Row 1 of test_scaled.csv is incorrect. Expected '{expected_row1}', got '{content[1]}'"
    assert content[2].strip() == expected_row2, f"Row 2 of test_scaled.csv is incorrect. Expected '{expected_row2}', got '{content[2]}'"

def test_train_scaled_csv():
    train_scaled_path = "/home/user/train_scaled.csv"
    assert os.path.isfile(train_scaled_path), f"Missing file: {train_scaled_path}"

    with open(train_scaled_path, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) == 6, f"Expected 6 lines (header + 5 rows) in {train_scaled_path}, got {len(content)}"
    assert content[0].strip() == "f1,f2", "Header in train_scaled.csv is incorrect."

    # Row 3: 16.0 -> (16.0 - 15.6) / 2.939387 = 0.13608 -> 0.1361
    # Row 4: 18.0 -> (18.0 - 15.6) / 2.939387 = 0.81649 -> 0.8165
    # Row 0: 10.0 -> (10.0 - 15.6) / 2.939387 = -1.90515 -> -1.9052

    expected_rows = [
        "0.1361,0.1361",
        "0.8165,0.8165",
        "-1.9052,-1.9052",
        "0.1361,0.1361",
        "0.8165,0.8165"
    ]

    for i in range(5):
        actual = content[i+1].strip()
        expected = expected_rows[i]
        assert actual == expected, f"Row {i+1} of train_scaled.csv is incorrect. Expected '{expected}', got '{actual}'"