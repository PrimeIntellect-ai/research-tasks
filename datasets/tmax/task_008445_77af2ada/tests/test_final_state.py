# test_final_state.py

import os
import pytest

def test_cpp_file_exists():
    cpp_file = "/home/user/config_tracker.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} does not exist."

def test_stats_output_exists():
    output_file = "/home/user/stats_output.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. Did you compile and run your C++ program?"

def test_stats_output_content():
    output_file = "/home/user/stats_output.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    expected_lines = [
        "update_01.txt,VALID,2,11.50",
        "update_02.txt,VALID,2,9.50",
        "update_03.txt,INVALID,0,0.00",
        "update_04.txt,VALID,2,7.17",
        "update_05.txt,VALID,1,5.00"
    ]

    with open(output_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_file}, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {output_file} is incorrect.\nExpected: {expected}\nActual: {actual}"