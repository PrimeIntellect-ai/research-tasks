# test_final_state.py

import os
import pytest

def test_valid_pin_file():
    """Verify that valid_pin.txt contains the correct 4-digit PIN."""
    file_path = "/home/user/valid_pin.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "4829", f"Expected valid_pin.txt to contain '4829', but got '{content}'."

def test_cwe_id_file():
    """Verify that cwe_id.txt contains the correct CWE identifier."""
    file_path = "/home/user/cwe_id.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content.upper() == "CWE-532", f"Expected cwe_id.txt to contain 'CWE-532', but got '{content}'."

def test_redacted_logs_file():
    """Verify that redacted_logs.txt contains the correctly redacted logs."""
    file_path = "/home/user/redacted_logs.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    expected_logs = [
        "[INFO] System started at 08:00",
        "[INFO] User admin logged in",
        "[ERROR] Invalid attempt with PIN: ****",
        "[ERROR] Connection timeout from 192.168.1.50",
        "[ERROR] Invalid attempt with PIN: ****",
        "[ERROR] Invalid attempt with PIN: ****",
        "[INFO] Daily backup completed. PIN: 1234 was used for backup auth? No.",
        "[ERROR] Invalid attempt with PIN: ****"
    ]

    with open(file_path, "r") as f:
        actual_logs = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_logs) == len(expected_logs), "The number of lines in redacted_logs.txt does not match the expected output."

    for i, (actual, expected) in enumerate(zip(actual_logs, expected_logs)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: '{expected}'\nGot: '{actual}'"

def test_redactor_cpp_exists():
    """Verify that the redactor.cpp source file was created."""
    file_path = "/home/user/redactor.cpp"
    assert os.path.isfile(file_path), f"File {file_path} is missing. You must write your C++ program to this location."