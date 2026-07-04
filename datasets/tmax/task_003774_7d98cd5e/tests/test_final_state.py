# test_final_state.py

import os
import pytest

def test_bad_commit_file_exists():
    path = "/home/user/bad_commit.txt"
    assert os.path.isfile(path), f"File {path} does not exist. The task requires writing the bad commit hash to this file."

def test_bad_commit_hash_correct():
    actual_path = "/home/user/bad_commit.txt"
    expected_path = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(actual_path), f"File {actual_path} is missing."
    assert os.path.isfile(expected_path), f"Truth file {expected_path} is missing."

    with open(actual_path, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_path, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash, f"File {actual_path} is empty."
    assert len(actual_hash) == 40, f"The commit hash in {actual_path} should be exactly 40 characters long, got {len(actual_hash)}."
    assert actual_hash == expected_hash, f"The commit hash found ({actual_hash}) does not match the expected bad commit ({expected_hash})."