# test_final_state.py

import os
import pytest

def read_file_stripped(path):
    with open(path, "r") as f:
        return f.read().strip()

def test_userid_solution():
    solution_path = "/home/user/solution_userid.txt"
    expected_path = "/home/user/expected_userid.txt"

    assert os.path.isfile(solution_path), f"Solution file {solution_path} is missing."
    assert os.path.isfile(expected_path), f"Expected truth file {expected_path} is missing."

    solution_val = read_file_stripped(solution_path)
    expected_val = read_file_stripped(expected_path)

    assert solution_val == expected_val, f"User ID in {solution_path} is incorrect. Expected '{expected_val}', got '{solution_val}'."

def test_commit_solution():
    solution_path = "/home/user/solution_commit.txt"
    expected_path = "/home/user/expected_commit.txt"

    assert os.path.isfile(solution_path), f"Solution file {solution_path} is missing."
    assert os.path.isfile(expected_path), f"Expected truth file {expected_path} is missing."

    solution_val = read_file_stripped(solution_path)
    expected_val = read_file_stripped(expected_path)

    assert solution_val == expected_val, f"Commit hash in {solution_path} is incorrect. Expected '{expected_val}', got '{solution_val}'."

def test_minimized_payload_solution():
    solution_path = "/home/user/solution_minimized_payload.txt"
    expected_path = "/home/user/expected_payload.txt"

    assert os.path.isfile(solution_path), f"Solution file {solution_path} is missing."
    assert os.path.isfile(expected_path), f"Expected truth file {expected_path} is missing."

    solution_val = read_file_stripped(solution_path)
    expected_val = read_file_stripped(expected_path)

    assert solution_val == expected_val, f"Minimized payload in {solution_path} is incorrect. Expected '{expected_val}', got '{solution_val}'."