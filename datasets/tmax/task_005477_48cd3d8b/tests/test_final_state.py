# test_final_state.py

import os
import pytest

def test_files_exist():
    """Verify that all required files have been created."""
    required_files = [
        "/home/user/deploy.h",
        "/home/user/deploy.c",
        "/home/user/test_deploy.c",
        "/home/user/run_tests",
        "/home/user/test_results.log"
    ]
    for file_path in required_files:
        assert os.path.isfile(file_path), f"Required file {file_path} is missing."

def test_executable_is_executable():
    """Verify that run_tests is an executable."""
    assert os.access("/home/user/run_tests", os.X_OK), "/home/user/run_tests is not executable."

def test_test_results_content():
    """Verify the contents of test_results.log match the expected output exactly."""
    expected_content = (
        "Test 1: 200\n"
        "Test 2: 200\n"
        "Test 3: 429\n"
        "Test 4: 400\n"
        "Test 5: 200\n"
        "Test 6: 429"
    )

    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Contents of {log_path} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )