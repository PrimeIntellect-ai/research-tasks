# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_txt():
    bad_commit_path = "/home/user/bad_commit.txt"
    expected_commit_path = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(bad_commit_path), f"File {bad_commit_path} is missing."
    assert os.path.isfile(expected_commit_path), f"File {expected_commit_path} is missing."

    with open(bad_commit_path, "r") as f:
        actual_commit = f.read().strip()

    with open(expected_commit_path, "r") as f:
        expected_commit = f.read().strip()

    assert actual_commit == expected_commit, f"Expected bad commit hash '{expected_commit}', but got '{actual_commit}'."

def test_fixed_output_txt():
    output_path = "/home/user/fixed_output.txt"
    assert os.path.isfile(output_path), f"File {output_path} is missing."

    with open(output_path, "r") as f:
        output_content = f.read().strip()

    assert output_content == "1036", f"Expected fixed_output.txt to contain '1036', but got '{output_content}'."

def test_pytest_installed():
    result = subprocess.run(["pytest", "--version"], capture_output=True, text=True)
    assert result.returncode == 0, "pytest is not installed or not available in the environment."

def test_seq_py_fixed():
    repo_dir = "/home/user/seq_repo"
    result = subprocess.run(["python3", "seq.py"], cwd=repo_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"seq.py failed to run. Stderr: {result.stderr}"
    assert result.stdout.strip() == "1036", f"seq.py did not print the correct output. Expected '1036', got '{result.stdout.strip()}'."

def test_tests_pass():
    repo_dir = "/home/user/seq_repo"
    result = subprocess.run(["pytest", "test_seq.py"], cwd=repo_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"pytest tests failed. Output: {result.stdout}\n{result.stderr}"