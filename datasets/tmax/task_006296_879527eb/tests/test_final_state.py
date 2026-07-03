# test_final_state.py

import os
import pytest

def test_bad_commit_file_exists():
    target_file = "/home/user/bad_commit.txt"
    assert os.path.isfile(target_file), f"The file {target_file} was not created."

def test_bad_commit_hash_is_correct():
    target_file = "/home/user/bad_commit.txt"
    truth_file = "/tmp/truth/expected_commit.txt"

    assert os.path.isfile(truth_file), f"Truth file {truth_file} is missing, setup is corrupted."
    assert os.path.isfile(target_file), f"The file {target_file} was not created."

    with open(truth_file, "r") as f:
        expected_hash = f.read().strip()

    with open(target_file, "r") as f:
        actual_hash = f.read().strip()

    assert len(actual_hash) == 40, f"The commit hash in {target_file} must be exactly 40 characters long."
    assert actual_hash == expected_hash, f"Incorrect commit hash. Expected {expected_hash}, got {actual_hash}."