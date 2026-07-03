# test_final_state.py
import os

def test_bad_commit_file_exists():
    assert os.path.exists("/home/user/bad_commit.txt"), "/home/user/bad_commit.txt does not exist."
    assert os.path.isfile("/home/user/bad_commit.txt"), "/home/user/bad_commit.txt is not a file."

def test_bad_commit_hash_is_correct():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.exists(expected_file), f"Truth file {expected_file} is missing."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert len(expected_hash) == 40, "Expected hash is not 40 characters."
    assert actual_hash == expected_hash, f"Incorrect bad commit hash. Expected {expected_hash}, got {actual_hash}."