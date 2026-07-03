# test_final_state.py

import os
import subprocess
import pytest

def get_expected_bad_commit():
    repo_path = "/home/user/math_repo"
    # The bad commit is the one that modified analyze.py to include os.system.
    # Since it was modified exactly once after creation, it's the most recent commit touching analyze.py.
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "log", "--format=%H", "--", "analyze.py"],
            capture_output=True,
            text=True,
            check=True
        )
        commits = result.stdout.strip().split('\n')
        if len(commits) >= 2:
            return commits[0] # The most recent one
    except subprocess.CalledProcessError:
        pass
    return None

def test_bad_commit_txt():
    bad_commit_file = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_file), f"File {bad_commit_file} does not exist."

    with open(bad_commit_file, "r") as f:
        actual_commit = f.read().strip()

    expected_commit = get_expected_bad_commit()
    assert expected_commit is not None, "Could not determine the expected bad commit from git history."

    assert actual_commit == expected_commit, f"Incorrect commit hash in {bad_commit_file}. Expected {expected_commit}, got {actual_commit}."

def test_secret_txt():
    secret_file = "/home/user/secret.txt"
    assert os.path.isfile(secret_file), f"File {secret_file} does not exist."

    with open(secret_file, "r") as f:
        actual_secret = f.read().strip()

    expected_secret = "AKIA12345SECRET98765"
    assert actual_secret == expected_secret, f"Incorrect secret in {secret_file}. Expected {expected_secret}, got {actual_secret}."