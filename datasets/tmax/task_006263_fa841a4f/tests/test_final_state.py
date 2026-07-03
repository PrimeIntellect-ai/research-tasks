# test_final_state.py

import os
import pytest

def test_c_source_exists():
    assert os.path.isfile("/home/user/loc_processor.c"), "The C source file /home/user/loc_processor.c is missing."

def test_makefile_exists():
    assert os.path.isfile("/home/user/Makefile"), "The Makefile /home/user/Makefile is missing."

def test_executable_exists():
    exe_path = "/home/user/loc_processor"
    assert os.path.isfile(exe_path), f"The executable {exe_path} is missing. Did you run 'make all'?"
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_final_stats_tsv_exists_and_content():
    file_path = "/home/user/final_stats.tsv"
    assert os.path.isfile(file_path), f"The file {file_path} is missing. Did you run 'make pipeline'?"

    expected_lines = [
        "1696154400\tfr\tSTR_A\t10\t10.00",
        "1696155300\tfr\tSTR_B\t20\t15.00",
        "1696156200\tde\tSTR_C\t30\t20.00",
        "1696158000\tde\tSTR_D\t15\t21.67"
    ]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch in {file_path}.\nExpected: {expected}\nActual:   {actual}"