# test_final_state.py
import os
import subprocess
import pytest

def test_bad_commit_identified():
    bad_commit_file = "/home/user/bad_commit.txt"
    secret_file = "/home/user/.secret_bad_commit"

    assert os.path.isfile(bad_commit_file), f"{bad_commit_file} does not exist."
    assert os.path.isfile(secret_file), f"{secret_file} does not exist."

    with open(bad_commit_file, "r") as f:
        student_commit = f.read().strip()

    with open(secret_file, "r") as f:
        truth_commit = f.read().strip()

    assert student_commit == truth_commit, f"The commit hash in {bad_commit_file} is incorrect."

def test_recovered_key():
    recovered_key_file = "/home/user/recovered_key.txt"

    assert os.path.isfile(recovered_key_file), f"{recovered_key_file} does not exist."

    with open(recovered_key_file, "r") as f:
        key = f.read().strip()

    assert key == "DEBUG_KEY_7734", f"The recovered key in {recovered_key_file} is incorrect."

def test_make_test_passes():
    repo_dir = "/home/user/repo"
    assert os.path.isdir(repo_dir), f"{repo_dir} does not exist."

    # Run make to ensure the latest changes are compiled
    compile_result = subprocess.run(["make", "all"], cwd=repo_dir, capture_output=True, text=True)
    assert compile_result.returncode == 0, f"'make all' failed:\n{compile_result.stderr}"

    # Run make test
    test_result = subprocess.run(["make", "test"], cwd=repo_dir, capture_output=True, text=True)
    assert test_result.returncode == 0, f"'make test' failed. The bug is not fixed correctly:\n{test_result.stderr}\n{test_result.stdout}"