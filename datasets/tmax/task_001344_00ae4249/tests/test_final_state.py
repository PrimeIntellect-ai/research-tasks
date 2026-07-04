# test_final_state.py

import os
import re
import pytest

def test_c_source_code_exists_and_uses_locking():
    source_path = "/home/user/detect_zipslip.c"
    assert os.path.exists(source_path), f"The C source file {source_path} does not exist."
    assert os.path.isfile(source_path), f"The path {source_path} is not a file."

    with open(source_path, 'r') as f:
        content = f.read()

    # Check for usage of flock or fcntl
    has_flock = "flock" in content
    has_fcntl = "fcntl" in content
    assert has_flock or has_fcntl, f"The C source code in {source_path} must use file locking (flock or fcntl)."

def test_alerts_csv_content():
    alerts_path = "/home/user/alerts.csv"
    assert os.path.exists(alerts_path), f"The output file {alerts_path} does not exist."
    assert os.path.isfile(alerts_path), f"The path {alerts_path} is not a file."

    expected_content = """ID,FILE
REQ002,../../etc/passwd
REQ005,a/b/c/../../../../tmp/hacked
REQ006,/var/log/syslog
"""

    with open(alerts_path, 'r') as f:
        actual_content = f.read()

    # Normalize newlines
    actual_lines = [line.strip() for line in actual_content.strip().split('\n')]
    expected_lines = [line.strip() for line in expected_content.strip().split('\n')]

    assert actual_lines == expected_lines, (
        f"The content of {alerts_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\nActual:\n{actual_content}"
    )

def test_alerts_csv_no_duplicate_headers():
    alerts_path = "/home/user/alerts.csv"
    if os.path.exists(alerts_path):
        with open(alerts_path, 'r') as f:
            content = f.read()

        header_count = content.count("ID,FILE")
        assert header_count == 1, f"The header 'ID,FILE' should appear exactly once in {alerts_path}, found {header_count} times."