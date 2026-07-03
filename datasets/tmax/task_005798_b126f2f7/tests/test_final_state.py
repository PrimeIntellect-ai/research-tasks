# test_final_state.py

import os
import pytest

def test_secret_file_exists_and_correct():
    secret_path = "/home/user/secret.txt"
    expected_secret_path = "/tmp/expected_secret.txt"

    assert os.path.exists(secret_path), f"File {secret_path} does not exist. You must save the recovered secret key to this file."
    assert os.path.exists(expected_secret_path), f"Expected secret file {expected_secret_path} is missing from the environment."

    with open(secret_path, "r") as f:
        actual_secret = f.read().strip()

    with open(expected_secret_path, "r") as f:
        expected_secret = f.read().strip()

    assert actual_secret == expected_secret, f"The secret in {secret_path} is incorrect. Expected '{expected_secret}', got '{actual_secret}'."

def test_bad_commit_file_exists_and_correct():
    bad_commit_path = "/home/user/bad_commit.txt"
    expected_bad_commit_path = "/tmp/expected_bad_commit.txt"

    assert os.path.exists(bad_commit_path), f"File {bad_commit_path} does not exist. You must save the bad commit hash to this file."
    assert os.path.exists(expected_bad_commit_path), f"Expected bad commit file {expected_bad_commit_path} is missing from the environment."

    with open(bad_commit_path, "r") as f:
        actual_commit = f.read().strip()

    with open(expected_bad_commit_path, "r") as f:
        expected_commit = f.read().strip()

    assert len(actual_commit) == 40, f"The commit hash in {bad_commit_path} must be a full 40-character hash, got '{actual_commit}'."
    assert actual_commit == expected_commit, f"The commit hash in {bad_commit_path} is incorrect. Expected '{expected_commit}', got '{actual_commit}'."