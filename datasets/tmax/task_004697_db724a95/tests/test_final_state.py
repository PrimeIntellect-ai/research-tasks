# test_final_state.py
import os

def test_bad_commit_hash():
    actual_file = "/home/user/bad_commit.txt"
    expected_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(actual_file), f"The file {actual_file} was not created."
    assert os.path.isfile(expected_file), f"The expected truth file {expected_file} is missing."

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    assert len(expected_hash) > 0, "The expected hash is empty."
    assert actual_hash == expected_hash, f"The bad commit hash is incorrect. Expected: {expected_hash}, Actual: {actual_hash}"