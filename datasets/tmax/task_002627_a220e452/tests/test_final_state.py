# test_final_state.py

import os
import pytest

def test_interpreter_patched():
    path = "/home/user/interpreter.sh"
    assert os.path.isfile(path), f"Interpreter script is missing at {path}"
    with open(path, 'r') as f:
        content = f.read()
    assert "set -f" in content, "The interpreter script was not patched to fix globbing (missing 'set -f')."

def test_test_runner_exists_and_executable():
    path = "/home/user/test_runner.sh"
    assert os.path.isfile(path), f"Test runner script is missing at {path}"
    assert os.access(path, os.X_OK), f"Test runner script at {path} is not executable."

def test_test_data_directory_and_files():
    dir_path = "/home/user/test_data"
    assert os.path.isdir(dir_path), f"Test data directory is missing at {dir_path}"

    expected_files = {
        "test_1.txt": "10 5 +",
        "test_2.txt": "20 4 /",
        "test_3.txt": "3 4 * 2 +",
        "test_4.txt": "15 5 - 2 *",
        "test_5.txt": "100 10 / 5 *",
        "test_6.txt": "50 25 - 5 /",
        "test_7.txt": "7 8 * 10 -"
    }

    for filename, expected_content in expected_files.items():
        file_path = os.path.join(dir_path, filename)
        assert os.path.isfile(file_path), f"Test fixture file missing: {file_path}"
        with open(file_path, 'r') as f:
            content = f.read().strip()
        assert content == expected_content, f"Content of {file_path} is incorrect. Expected '{expected_content}', got '{content}'."

def test_test_report_log():
    path = "/home/user/test_report.log"
    assert os.path.isfile(path), f"Test report log is missing at {path}"

    expected_lines = [
        "Test 1: 15",
        "Test 2: 5",
        "Test 3: 14",
        "Test 4: 20",
        "Test 5: 50",
        "Test 6: 5",
        "Test 7: 46"
    ]

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"Test report log content is incorrect or not properly sorted. Expected: {expected_lines}, Got: {lines}"