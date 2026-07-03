# test_final_state.py

import os
import pytest

def test_matches_csv_exists_and_correct():
    file_path = "/home/user/matches.csv"
    assert os.path.isfile(file_path), f"Error: {file_path} is missing. Did you run your program?"

    expected_content = "2,102\n5,105\n3,103"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Error: Content of {file_path} does not match expected output.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_c_source_file_exists():
    file_path = "/home/user/match_samples.c"
    assert os.path.isfile(file_path), f"Error: {file_path} is missing. You must save your C code here."

def test_executable_exists():
    file_path = "/home/user/match_samples"
    assert os.path.isfile(file_path), f"Error: {file_path} is missing. Did you compile your code?"
    assert os.access(file_path, os.X_OK), f"Error: {file_path} is not executable."