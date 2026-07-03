# test_final_state.py

import os
import csv
import pytest

def test_merged_csv_exists():
    merged_path = "/home/user/merged.csv"
    assert os.path.isfile(merged_path), f"Output file {merged_path} does not exist. Did you run the script?"

def test_merged_csv_content():
    merged_path = "/home/user/merged.csv"

    expected_rows = [
        ["user_id", "name", "age", "score1", "score2", "total_score"],
        ["1", "Alice", "25", "10", "20", "30"],
        ["2", "Bob", "30", "15", "15", "30"],
        ["3", "Charlie", "22", "0", "0", "0"],
        ["4", "Diana", "28", "30", "40", "70"]
    ]

    with open(merged_path, "r") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, f"Content of {merged_path} does not match the expected output. Make sure you performed a left join, filled NAs with 0, calculated total_score, and converted numerical columns to integers."

def test_no_floats_in_merged_csv():
    merged_path = "/home/user/merged.csv"
    with open(merged_path, "r") as f:
        content = f.read()

    assert ".0" not in content, f"Found '.0' in {merged_path}. Ensure that pandas integer columns are strictly cast to integers, not floats."