# test_final_state.py

import os
import subprocess
import pytest

REPO_DIR = "/home/user/data_processor"
BAD_COMMIT_FILE = "/home/user/bad_commit.txt"
EXPECTED_COMMIT_FILE = "/tmp/expected_bad_commit.txt"

def test_bad_commit_file_exists():
    assert os.path.isfile(BAD_COMMIT_FILE), f"The file {BAD_COMMIT_FILE} does not exist."

def test_bad_commit_correct():
    assert os.path.isfile(EXPECTED_COMMIT_FILE), f"Internal error: {EXPECTED_COMMIT_FILE} missing."
    assert os.path.isfile(BAD_COMMIT_FILE), f"{BAD_COMMIT_FILE} is missing."

    with open(EXPECTED_COMMIT_FILE, "r") as f:
        expected_hash = f.read().strip()

    with open(BAD_COMMIT_FILE, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected bad commit {expected_hash}, but got {actual_hash}."

def test_git_not_in_bisect_state():
    bisect_start_file = os.path.join(REPO_DIR, ".git", "BISECT_START")
    assert not os.path.exists(bisect_start_file), (
        "The repository is still in a bisect state. "
        "You must run 'git bisect reset' after finding the commit."
    )