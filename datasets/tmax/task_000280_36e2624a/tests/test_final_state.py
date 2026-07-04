# test_final_state.py

import os
import pytest
import re

def test_summary_csv_content():
    summary_path = "/home/user/summary.csv"
    assert os.path.isfile(summary_path), f"Expected output file {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        content = f.read().strip()

    expected_lines = [
        "filepath,version",
        "/etc/app1/config.json,1.2.4",
        "/opt/app2/settings.json,2.0.1"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Content of {summary_path} does not match expected output.\nExpected: {expected_lines}\nActual: {actual_lines}"

def test_c_source_exists_and_uses_atomic_rename():
    source_path = "/home/user/analyzer.c"
    assert os.path.isfile(source_path), f"C source file {source_path} does not exist."

    with open(source_path, 'r') as f:
        content = f.read()

    # Check for atomic write logic (rename function)
    # The prompt specifies: "atomically rename the temporary file... verifying the C code uses `rename`"
    assert re.search(r'\brename\s*\(', content), "The C code does not appear to use the 'rename' function for atomic writing."

def test_executable_exists():
    executable_path = "/home/user/analyzer"
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} does not exist. Did you compile it?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."