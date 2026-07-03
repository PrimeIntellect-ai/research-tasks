# test_final_state.py

import os
import pytest

def test_top3_txt_exists_and_content():
    file_path = "/home/user/top3.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The Go program did not create the output file."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["D", "A", "B"]

    assert len(lines) == 3, f"Expected exactly 3 IDs in {file_path}, but found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Expected line {i+1} to be '{expected}', but got '{lines[i]}'. Check your distance calculations and sorting."

def test_data_csv_untouched():
    file_path = "/home/user/data.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The input data should not be deleted."