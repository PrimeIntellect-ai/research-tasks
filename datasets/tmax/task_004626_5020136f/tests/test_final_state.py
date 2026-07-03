# test_final_state.py

import os
import subprocess
import pytest

REPO_PATH = "/home/user/metrics-parser"
BAD_COMMIT_FILE = "/home/user/bad_commit.txt"

def test_bad_commit_recorded():
    """Verify that the correct bad commit SHA is recorded in bad_commit.txt."""
    assert os.path.isfile(BAD_COMMIT_FILE), f"File {BAD_COMMIT_FILE} does not exist."

    with open(BAD_COMMIT_FILE, "r") as f:
        recorded_sha = f.read().strip()

    # Derive the expected bad commit SHA from the git history
    cmd = ["git", "log", "--grep=Refactor parsing loop for performance", "--format=%H"]
    result = subprocess.run(cmd, cwd=REPO_PATH, capture_output=True, text=True, check=True)
    expected_sha = result.stdout.strip()

    assert expected_sha != "", "Could not find the expected bad commit in the git history."
    assert recorded_sha == expected_sha, f"Recorded bad commit SHA '{recorded_sha}' does not match expected SHA '{expected_sha}'."

def test_tests_pass():
    """Verify that the Go test suite passes, indicating the bug was successfully fixed."""
    result = subprocess.run(["go", "test", "./..."], cwd=REPO_PATH, capture_output=True, text=True)
    assert result.returncode == 0, f"Expected tests to pass, but they failed. Output:\n{result.stdout}\n{result.stderr}"

def test_on_main_branch():
    """Verify that the current branch is main."""
    result = subprocess.run(["git", "branch", "--show-current"], cwd=REPO_PATH, capture_output=True, text=True)
    branch = result.stdout.strip()
    assert branch == "main", f"Expected to be on branch 'main', but currently on '{branch}'."

def test_parser_test_unmodified():
    """Verify that parser_test.go was not modified."""
    # Compare current parser_test.go with the one from v1.0.0
    result = subprocess.run(["git", "diff", "v1.0.0", "--", "parser_test.go"], cwd=REPO_PATH, capture_output=True, text=True)
    assert result.stdout.strip() == "", "parser_test.go was modified, which violates the constraints."