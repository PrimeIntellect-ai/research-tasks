# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(actual_file), f"File {actual_file} does not exist."
    assert os.path.isfile(expected_file), f"Setup file {expected_file} is missing."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected bad commit hash {expected_hash}, but got {actual_hash}."

def test_processor_fix():
    repo_dir = "/home/user/app_repo"
    assert os.path.isdir(repo_dir), f"Directory {repo_dir} is missing."

    # Run make test
    result = subprocess.run(["make", "test"], cwd=repo_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"make test failed. Output:\n{result.stdout}\n{result.stderr}"

def test_regression_test():
    test_file = "/home/user/app_repo/regression_test.py"
    assert os.path.isfile(test_file), f"Regression test file {test_file} does not exist."

    result = subprocess.run(["python3", test_file], capture_output=True, text=True)
    assert result.returncode == 0, f"Regression test failed. Output:\n{result.stdout}\n{result.stderr}"

def test_recovered_sql():
    sql_file = "/home/user/recovered.sql"
    assert os.path.isfile(sql_file), f"Recovered SQL file {sql_file} does not exist."

    with open(sql_file, "r") as f:
        content = f.read()

    assert "Alice" in content, "Recovered SQL does not contain 'Alice'."
    assert "Bob" in content, "Recovered SQL does not contain 'Bob'."

def test_git_committed():
    repo_dir = "/home/user/app_repo"

    # Check if working directory is clean
    result = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run git status."

    uncommitted_changes = result.stdout.strip()
    assert not uncommitted_changes, f"There are uncommitted changes in the repository:\n{uncommitted_changes}"

    # Check if we are on main or master branch
    branch_result = subprocess.run(["git", "branch", "--show-current"], cwd=repo_dir, capture_output=True, text=True)
    branch = branch_result.stdout.strip()
    assert branch in ["main", "master"], f"Expected to be on 'main' or 'master' branch, but currently on '{branch}'."