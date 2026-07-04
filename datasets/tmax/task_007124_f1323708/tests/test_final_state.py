# test_final_state.py

import os
import subprocess
import difflib
import pytest

def test_valid_users_content():
    valid_users_path = "/home/user/valid_users.txt"
    assert os.path.exists(valid_users_path), f"Missing required file: {valid_users_path}"

    with open(valid_users_path, "r") as f:
        users = [line.strip() for line in f if line.strip()]

    expected_users = ["u1", "u4", "u5"]
    assert users == expected_users, f"Content of {valid_users_path} is incorrect. Expected {expected_users}, got {users}"

def test_all_users_content():
    all_users_path = "/home/user/all_users.txt"
    assert os.path.exists(all_users_path), f"Missing required file: {all_users_path}"

    with open(all_users_path, "r") as f:
        users = [line.strip() for line in f if line.strip()]

    expected_users = ["u0", "u1", "u4", "u5", "u8"]
    assert users == expected_users, f"Content of {all_users_path} is incorrect. Expected {expected_users}, got {users}"

def test_update_patch_content():
    patch_path = "/home/user/update.patch"
    historical_path = "/home/user/historical.txt"
    all_users_path = "/home/user/all_users.txt"

    assert os.path.exists(patch_path), f"Missing required file: {patch_path}"
    assert os.path.exists(historical_path), f"Missing required file: {historical_path}"
    assert os.path.exists(all_users_path), f"Missing required file: {all_users_path}"

    with open(historical_path, "r") as f:
        hist_lines = f.readlines()
    with open(all_users_path, "r") as f:
        all_lines = f.readlines()

    expected_diff = list(difflib.unified_diff(
        hist_lines, all_lines,
        fromfile=historical_path,
        tofile=all_users_path
    ))

    with open(patch_path, "r") as f:
        actual_diff = f.readlines()

    assert len(actual_diff) >= 3, "update.patch does not appear to be a valid unified diff."

    # Strip the timestamp portions of the first two lines for comparison, or just compare from line 3 onwards
    # Unified diffs have the format:
    # --- filename timestamp
    # +++ filename timestamp
    # @@ ... @@

    # Check that the hunks match exactly
    assert actual_diff[2:] == expected_diff[2:], "The hunks in update.patch do not match the expected unified diff between historical.txt and all_users.txt."

def test_pytest_execution():
    test_file_path = "/home/user/test_parser.py"
    assert os.path.exists(test_file_path), f"Missing required file: {test_file_path}"

    # Verify that pytest passes on the provided test file
    result = subprocess.run(
        ["pytest", test_file_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"pytest failed on {test_file_path}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"