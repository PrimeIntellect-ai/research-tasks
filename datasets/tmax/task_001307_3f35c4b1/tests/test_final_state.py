# test_final_state.py
import os

def test_bad_commit_file_exists():
    """Verify that the user created the bad_commit.txt file."""
    assert os.path.isfile("/home/user/bad_commit.txt"), "Error: /home/user/bad_commit.txt does not exist."

def test_bad_commit_hash_is_correct():
    """Verify that the bad_commit.txt contains the correct commit hash."""
    golden_file = "/tmp/.golden_bad_commit"
    user_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(golden_file), f"Setup error: {golden_file} is missing."
    assert os.path.isfile(user_file), f"Error: {user_file} is missing."

    with open(golden_file, "r") as f:
        expected_commit = f.read().strip()

    with open(user_file, "r") as f:
        actual_commit = f.read().strip()

    assert actual_commit == expected_commit, (
        f"Incorrect commit hash found. "
        f"Expected '{expected_commit}' but got '{actual_commit}'."
    )