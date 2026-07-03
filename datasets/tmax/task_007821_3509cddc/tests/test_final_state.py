# test_final_state.py

import os

def test_bad_commit_file_exists():
    """Check if the user created the bad_commit.txt file."""
    assert os.path.isfile("/home/user/bad_commit.txt"), "The file /home/user/bad_commit.txt does not exist."

def test_bad_commit_hash_matches():
    """Check if the commit hash in bad_commit.txt matches the expected bad commit."""
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(expected_file), "The expected bad commit file is missing from /tmp."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert len(actual_hash) == 40, f"The commit hash should be exactly 40 characters, got {len(actual_hash)}."
    assert expected_hash == actual_hash, f"The commit hash in bad_commit.txt is incorrect. Expected {expected_hash}, but got {actual_hash}."