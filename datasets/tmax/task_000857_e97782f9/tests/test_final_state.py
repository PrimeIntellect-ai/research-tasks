# test_final_state.py

import os
import subprocess
import pytest

REPO_DIR = "/home/user/math-solver"
RESOLUTION_FILE = "/home/user/resolution.txt"
BUGGY_COMMIT_FILE = "/home/user/.buggy_commit"
SOLVER_TEST_FILE = os.path.join(REPO_DIR, "solver_test.go")

def test_resolution_file():
    assert os.path.isfile(RESOLUTION_FILE), f"Resolution file {RESOLUTION_FILE} does not exist."

    with open(RESOLUTION_FILE, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {RESOLUTION_FILE}, found {len(lines)}."

    assert os.path.isfile(BUGGY_COMMIT_FILE), f"Hidden buggy commit file {BUGGY_COMMIT_FILE} is missing."
    with open(BUGGY_COMMIT_FILE, "r") as f:
        expected_commit = f.read().strip()

    assert lines[0] == expected_commit, f"Line 1 of {RESOLUTION_FILE} is incorrect. Expected the buggy commit hash."

    expected_root = "2.094551"
    assert lines[1] == expected_root, f"Line 2 of {RESOLUTION_FILE} is incorrect. Expected {expected_root}, got {lines[1]}."

def test_solver_test_minimized():
    assert os.path.isfile(SOLVER_TEST_FILE), f"Test file {SOLVER_TEST_FILE} is missing."

    with open(SOLVER_TEST_FILE, "r") as f:
        content = f.read()

    assert "func TestFindRoot(" in content, "TestFindRoot must be present in solver_test.go."
    assert "func TestAdd(" not in content, "TestAdd should have been removed from solver_test.go."
    assert "func TestAddZero(" not in content, "TestAddZero should have been removed from solver_test.go."

def test_go_tests_pass():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} is missing."

    result = subprocess.run(
        ["go", "test"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"'go test' failed in {REPO_DIR}. Output:\n{result.stdout}\n{result.stderr}"