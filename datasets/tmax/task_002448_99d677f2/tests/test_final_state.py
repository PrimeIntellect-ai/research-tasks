# test_final_state.py

import os
import pytest

def test_bad_commit_txt_exists():
    assert os.path.isfile("/home/user/bad_commit.txt"), "/home/user/bad_commit.txt does not exist."

def test_bad_commit_txt_content():
    assert os.path.isfile("/home/user/bad_commit.txt"), "/home/user/bad_commit.txt does not exist."
    assert os.path.isfile("/tmp/expected_bad_commit.txt"), "Truth file /tmp/expected_bad_commit.txt does not exist."

    with open("/tmp/expected_bad_commit.txt", "r") as f:
        expected_sha = f.read().strip()

    with open("/home/user/bad_commit.txt", "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) >= 2, "/home/user/bad_commit.txt must contain at least 2 lines."

    actual_sha = lines[0].strip()
    actual_size = lines[1].strip()

    assert actual_sha == expected_sha, f"First line of bad_commit.txt is incorrect. Expected {expected_sha}, got {actual_sha}."
    assert actual_size == "8000", f"Second line of bad_commit.txt is incorrect. Expected 8000, got {actual_size}."