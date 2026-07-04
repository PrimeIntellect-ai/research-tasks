# test_final_state.py

import os
import pytest

def test_policy_scanner_cpp_exists():
    assert os.path.isfile("/home/user/policy_scanner.cpp"), "The source file /home/user/policy_scanner.cpp does not exist."

def test_policy_scanner_executable_exists():
    executable_path = "/home/user/policy_scanner"
    assert os.path.isfile(executable_path), f"The executable {executable_path} does not exist. Did you compile the code?"
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_scan_results_content():
    results_path = "/home/user/scan_results.txt"
    assert os.path.isfile(results_path), f"The results file {results_path} does not exist. Did you run the program?"

    with open(results_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "VULN: SQLi found on line 2",
        "VULN: XSS found on line 7",
        "ALERT: Brute force detected from 192.168.1.10"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in scan_results.txt, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in scan_results.txt is incorrect.\nExpected: '{expected}'\nActual: '{actual}'"