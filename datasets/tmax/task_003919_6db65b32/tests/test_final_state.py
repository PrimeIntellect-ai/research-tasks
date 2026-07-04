# test_final_state.py

import os
import pytest

def test_clean_data_exists_and_content():
    clean_data_path = "/home/user/clean_data.csv"
    assert os.path.isfile(clean_data_path), f"File not found: {clean_data_path}"

    with open(clean_data_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "ID,X1,X2,X3,Y",
        "1,12,2,24,0",
        "2,14,3,42,100",
        "3,14,1,14,0",
        "4,18,2,36,100",
        "5,10,1,10,0",
        "6,14,4,56,100",
        "7,20,2,40,100",
        "8,15,3,45,100",
        "9,11,1,11,0",
        "10,25,2,50,100"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in clean_data.csv, found {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Row {i} mismatch in clean_data.csv. Expected: {expected}, Got: {actual}"

def test_result_txt_exists_and_content():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File not found: {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_content = "Optimal T: 30\nBest MSE: 0.00"

    assert content == expected_content, f"Content of {result_path} is incorrect.\nExpected:\n{expected_content}\nGot:\n{content}"