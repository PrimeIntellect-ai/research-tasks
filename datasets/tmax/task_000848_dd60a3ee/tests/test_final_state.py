# test_final_state.py

import os
import pytest

def test_bad_commit_hash():
    bad_commit_file = "/home/user/bad_commit.txt"
    expected_commit_file = "/tmp/expected_commit.txt"

    assert os.path.isfile(bad_commit_file), f"{bad_commit_file} does not exist."
    assert os.path.isfile(expected_commit_file), f"{expected_commit_file} does not exist."

    with open(bad_commit_file, "r") as f:
        actual_commit = f.read().strip()

    with open(expected_commit_file, "r") as f:
        expected_commit = f.read().strip()

    assert actual_commit == expected_commit, f"Expected commit hash {expected_commit}, but got {actual_commit}"

def test_crash_function():
    crash_function_file = "/home/user/crash_function.txt"

    assert os.path.isfile(crash_function_file), f"{crash_function_file} does not exist."

    with open(crash_function_file, "r") as f:
        actual_function = f.read().strip()

    assert actual_function == "process", f"Expected crash function 'process', but got '{actual_function}'"

def test_crash_line():
    crash_line_file = "/home/user/crash_line.txt"

    assert os.path.isfile(crash_line_file), f"{crash_line_file} does not exist."

    with open(crash_line_file, "r") as f:
        actual_line = f.read().strip()

    assert actual_line == "8", f"Expected crash line '8', but got '{actual_line}'"