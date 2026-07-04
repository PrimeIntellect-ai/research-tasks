# test_final_state.py

import os
import pytest

def test_parser_c_exists():
    assert os.path.isfile("/home/user/parser.c"), "The C source file /home/user/parser.c is missing."

def test_parser_executable_exists():
    assert os.path.isfile("/home/user/parser"), "The compiled executable /home/user/parser is missing."
    assert os.access("/home/user/parser", os.X_OK), "The file /home/user/parser is not executable."

def test_db_import_csv_content():
    csv_path = "/home/user/db_import.csv"
    assert os.path.isfile(csv_path), f"The output file {csv_path} is missing."

    expected_lines = [
        "cfg_id,avg_delta",
        "10,3.50",
        "30,8.00",
        "45,0.00"
    ]

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The content of {csv_path} does not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )