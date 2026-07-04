# test_final_state.py

import os
import pytest

def test_bad_commit_file_exists():
    path = "/home/user/bad_commit.txt"
    assert os.path.isfile(path), f"Expected file {path} to exist."

def test_bad_commit_hash_correct():
    actual_path = "/home/user/bad_commit.txt"
    expected_path = "/home/user/.secret_bad_commit"

    assert os.path.isfile(actual_path), f"Cannot verify hash because {actual_path} is missing."
    assert os.path.isfile(expected_path), f"Truth file {expected_path} is missing."

    with open(actual_path, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_path, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Incorrect commit hash in {actual_path}. Expected {expected_hash}, got {actual_hash}."