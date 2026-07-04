# test_final_state.py

import os
import pytest

def test_c_source_exists():
    src_path = "/home/user/src/policy_checker.c"
    assert os.path.isfile(src_path), f"Source file {src_path} is missing."

def test_binary_exists():
    bin_path = "/home/user/policy_checker"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Compiled binary {bin_path} is not executable."

def test_final_report_content():
    report_path = "/home/user/final_report.log"
    assert os.path.isfile(report_path), f"Final report {report_path} is missing."

    expected_lines = [
        "BUNDLE: /home/user/bundles/dev",
        "CERT: PASS",
        "INTEGRITY: PASS",
        "CSP: FAIL",
        "BUNDLE: /home/user/bundles/staging",
        "CERT: FAIL",
        "INTEGRITY: PASS",
        "CSP: PASS",
        "BUNDLE: /home/user/bundles/prod",
        "CERT: PASS",
        "INTEGRITY: FAIL",
        "CSP: PASS",
        "BUNDLE: /home/user/bundles/dr",
        "CERT: PASS",
        "INTEGRITY: PASS",
        "CSP: PASS"
    ]

    with open(report_path, 'r') as f:
        actual_lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in the report, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}: expected '{expected}', got '{actual}'."