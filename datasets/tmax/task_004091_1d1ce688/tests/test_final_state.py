# test_final_state.py
import os
import pytest

BAD_COMMIT_FILE = "/home/user/bad_commit.txt"
EXPECTED_BAD_COMMIT_FILE = "/home/user/expected_bad_commit.txt"

def test_bad_commit_file_exists():
    assert os.path.isfile(BAD_COMMIT_FILE), f"The file {BAD_COMMIT_FILE} does not exist. Did you save the result?"

def test_bad_commit_hash_correct():
    assert os.path.isfile(EXPECTED_BAD_COMMIT_FILE), f"Setup file {EXPECTED_BAD_COMMIT_FILE} is missing."

    with open(BAD_COMMIT_FILE, "r") as f:
        actual_hash = f.read().strip()

    with open(EXPECTED_BAD_COMMIT_FILE, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The bad commit hash is incorrect. Expected {expected_hash}, but got {actual_hash}."
    assert len(actual_hash) == 40, "The commit hash must be exactly 40 characters long."