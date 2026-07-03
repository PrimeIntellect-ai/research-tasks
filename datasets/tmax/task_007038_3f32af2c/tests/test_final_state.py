# test_final_state.py

import os
import subprocess
import pytest

SOLUTION_FILE = "/home/user/solution.txt"
EXPECTED_COMMIT_FILE = "/tmp/expected_commit"
EXPECTED_TOKEN_FILE = "/tmp/expected_token"
REPO_DIR = "/home/user/repo"

def test_solution_file_exists():
    """Verify that the solution file has been created."""
    assert os.path.isfile(SOLUTION_FILE), f"Solution file {SOLUTION_FILE} does not exist."

def test_solution_content():
    """Verify that the solution file contains the correct commit hash and token."""
    assert os.path.isfile(EXPECTED_COMMIT_FILE), f"Expected commit file {EXPECTED_COMMIT_FILE} missing."
    assert os.path.isfile(EXPECTED_TOKEN_FILE), f"Expected token file {EXPECTED_TOKEN_FILE} missing."

    with open(EXPECTED_COMMIT_FILE, "r") as f:
        expected_commit = f.read().strip()

    with open(EXPECTED_TOKEN_FILE, "r") as f:
        expected_token = f.read().strip()

    with open(SOLUTION_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) >= 2, f"Solution file must contain at least two lines, found {len(lines)}."

    actual_commit = lines[0]
    actual_token = lines[1]

    assert actual_commit == expected_commit, f"Commit hash mismatch. Expected {expected_commit}, got {actual_commit}."
    assert actual_token == expected_token, f"Token mismatch. Expected {expected_token}, got {actual_token}."

def test_git_head_not_altered():
    """Verify that the HEAD of the repository has not been permanently altered (e.g. left in detached HEAD)."""
    try:
        # The setup creates 6 commits on the master branch. We expect HEAD to be pointing to the branch, not detached.
        # Check if we are on a branch (usually master or main)
        result = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Git HEAD is in a detached state. You should reset to the original branch (e.g., git bisect reset)."

        # Check that the latest commit message is "Add comment"
        log_result = subprocess.run(
            ["git", "log", "-1", "--format=%s"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        assert log_result.stdout.strip() == "Add comment", "The current HEAD does not match the original latest commit. Did you forget to reset the repository state?"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to check git repository state: {e.stderr}")