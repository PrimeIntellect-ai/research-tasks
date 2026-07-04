# test_final_state.py
import os
import pytest

def test_bad_commit_file_exists():
    path = "/home/user/bad_commit.txt"
    assert os.path.isfile(path), f"The file {path} does not exist. You must write the first bad commit hash to this file."

def test_bad_commit_hash_correct():
    actual_path = "/home/user/bad_commit.txt"
    expected_path = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(actual_path), f"The file {actual_path} does not exist."
    assert os.path.isfile(expected_path), f"The truth file {expected_path} is missing."

    with open(actual_path, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_path, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, (
        f"The commit hash in {actual_path} is incorrect.\n"
        f"Expected: {expected_hash}\n"
        f"Actual: {actual_hash}"
    )