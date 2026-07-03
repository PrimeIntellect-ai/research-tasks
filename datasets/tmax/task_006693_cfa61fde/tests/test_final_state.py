# test_final_state.py
import os

def test_bad_commit_found():
    actual_file = "/home/user/bad_commit.txt"
    expected_file = "/tmp/expected_bad_commit.txt"

    assert os.path.exists(actual_file), f"File {actual_file} does not exist. Did you save the commit hash?"
    assert os.path.exists(expected_file), f"File {expected_file} does not exist (setup error)."

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash, "The bad_commit.txt file is empty."
    assert expected_hash, "The expected_bad_commit.txt file is empty (setup error)."

    assert actual_hash == expected_hash, f"Incorrect bad commit. Expected {expected_hash}, got {actual_hash}."