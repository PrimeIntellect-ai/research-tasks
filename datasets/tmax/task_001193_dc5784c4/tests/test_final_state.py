# test_final_state.py

import os
import pytest

def test_output_csv_contents():
    output_path = '/home/user/output.csv'
    assert os.path.isfile(output_path), f"{output_path} is missing. Did you run the pipeline script?"

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "user_id,name,item_id",
        "1,Alice,101",
        "2,Bob,",
        "3,Charlie,105",
        "4,David,109"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_path}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {output_path} is incorrect. Expected '{expected}', got '{actual}'."

def test_corrupt_artifacts_txt_contents():
    txt_path = '/home/user/corrupt_artifacts.txt'
    assert os.path.isfile(txt_path), f"{txt_path} is missing."

    with open(txt_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_files = {"run_A.csv", "run_C.csv"}
    actual_files = set(lines)

    assert actual_files == expected_files, f"Expected {txt_path} to contain exactly {expected_files}, but got {actual_files}."
    assert len(lines) == 2, f"Expected exactly 2 lines in {txt_path}, but found {len(lines)} lines."