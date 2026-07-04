# test_final_state.py

import os
import pytest

LEAK_COMMIT_FILE = "/home/user/leak_commit.txt"
EXPECTED_BAD_COMMIT_FILE = "/tmp/expected_bad_commit.txt"

def test_leak_commit_file_exists():
    assert os.path.isfile(LEAK_COMMIT_FILE), f"The file {LEAK_COMMIT_FILE} does not exist. Did you save the result?"

def test_correct_commit_identified():
    assert os.path.isfile(EXPECTED_BAD_COMMIT_FILE), f"Internal error: {EXPECTED_BAD_COMMIT_FILE} is missing."

    with open(EXPECTED_BAD_COMMIT_FILE, 'r') as f:
        expected_commit = f.read().strip()

    with open(LEAK_COMMIT_FILE, 'r') as f:
        actual_commit = f.read().strip()

    assert actual_commit == expected_commit, (
        f"Incorrect commit identified. "
        f"Expected '{expected_commit}', but got '{actual_commit}'."
    )