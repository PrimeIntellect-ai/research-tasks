# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_sha():
    expected_sha_path = "/tmp/expected_bad_commit.sha"
    actual_sha_path = "/home/user/bad_commit.sha"

    assert os.path.exists(expected_sha_path), f"Expected SHA file missing: {expected_sha_path}"
    assert os.path.exists(actual_sha_path), f"Student SHA file missing: {actual_sha_path}"

    with open(expected_sha_path, "r") as f:
        expected_sha = f.read().strip()

    with open(actual_sha_path, "r") as f:
        actual_sha = f.read().strip()

    assert len(actual_sha) == 40, "The commit hash in /home/user/bad_commit.sha must be exactly 40 characters long"
    assert actual_sha == expected_sha, f"Incorrect bad commit. Expected {expected_sha}, got {actual_sha}"

def test_executable_exists_and_runnable():
    calc_path = "/home/user/metric-calc/calc"
    assert os.path.exists(calc_path), f"Executable missing: {calc_path}"
    assert os.access(calc_path, os.X_OK), f"File is not executable: {calc_path}"

    result = subprocess.run([calc_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {calc_path} failed with return code {result.returncode}"
    assert "Health: 80.000000" in result.stdout, f"Executable output did not match expected 'Health: 80.000000'. Got: {result.stdout}"

def test_go_test_passes():
    app_dir = "/home/user/metric-calc"
    assert os.path.isdir(app_dir), f"Directory missing: {app_dir}"

    result = subprocess.run(["go", "test"], cwd=app_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"'go test' failed in {app_dir}. Output: {result.stdout}\n{result.stderr}"