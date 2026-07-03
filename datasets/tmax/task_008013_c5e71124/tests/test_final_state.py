# test_final_state.py

import os
import pytest

def test_bad_commit_hash_file_exists():
    assert os.path.isfile("/home/user/bad_commit_hash.txt"), "The file /home/user/bad_commit_hash.txt does not exist."

def test_bad_commit_hash_correct():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit_hash.txt"

    assert os.path.isfile(expected_file), f"Expected truth file {expected_file} is missing from the environment."
    assert os.path.isfile(actual_file), f"The file {actual_file} is missing."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The commit hash in {actual_file} is incorrect. Expected {expected_hash}, but got {actual_hash}."