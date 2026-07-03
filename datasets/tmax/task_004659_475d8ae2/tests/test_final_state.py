# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    file_path = "/home/user/evaluate_experiments.c"
    assert os.path.isfile(file_path), f"C source file {file_path} was not created."

def test_report_csv_exists_and_correct():
    file_path = "/home/user/report.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} was not generated."

    expected_content = """exp_id,status
1,Success
2,Invalid
3,Failure
4,Invalid
5,Success
6,Invalid
7,Failure"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    # Normalize line endings and whitespace for robust comparison
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Content of {file_path} does not match the expected output."