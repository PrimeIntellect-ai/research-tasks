# test_final_state.py

import os
import pytest

def test_filtered_csv_content():
    file_path = "/home/user/data/filtered.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The ETL step was not completed correctly."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "id,val1,val2,label",
        "1,0.8,0.2,1",
        "3,0.9,0.3,1",
        "4,0.1,0.9,1"
    ]

    assert lines == expected_lines, f"Content of {file_path} does not match the expected filtered data. It should contain the header and rows where label is exactly 1."

def test_best_model_log_content():
    file_path = "/home/user/best_model.log"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The reporting step was not completed correctly."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "Best Param: 0.5, Score: 0.70, CI: [0.55, 0.85]"

    # We allow minor formatting differences if the logic holds, but the instruction says "containing exactly one line in this format"
    # So we'll check exact match or very close match.
    assert content == expected_content, f"Content of {file_path} is incorrect. Expected exactly '{expected_content}', but got '{content}'."