# test_final_state.py
import os
import pytest

RESULT_FILE = "/home/user/result.txt"
SOLVE_CPP = "/home/user/solve.cpp"

def test_solve_cpp_exists():
    assert os.path.isfile(SOLVE_CPP), f"The C++ source file {SOLVE_CPP} is missing."

def test_result_file_exists():
    assert os.path.isfile(RESULT_FILE), f"The file {RESULT_FILE} was not created."

def test_result_file_content():
    assert os.path.isfile(RESULT_FILE), f"The file {RESULT_FILE} is missing."
    with open(RESULT_FILE, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {RESULT_FILE}, found {len(lines)}."

    path, distance = lines[0], lines[1]

    expected_path = "W001,W002,W005,W006"
    expected_distance = "45"

    assert path == expected_path, f"Expected path '{expected_path}', but got '{path}'."
    assert distance == expected_distance, f"Expected distance '{expected_distance}', but got '{distance}'."