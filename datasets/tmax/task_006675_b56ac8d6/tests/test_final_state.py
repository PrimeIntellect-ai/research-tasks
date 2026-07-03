# test_final_state.py

import os
import re
import pytest

def test_corrupted_lines_file():
    path = "/home/user/corrupted_lines.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["142", "888", "2045", "3333", "4999"]
    assert lines == expected_lines, f"Expected {path} to contain {expected_lines}, but got {lines}"

def test_final_total_file():
    path = "/home/user/final_total.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"

    expected_path = "/tmp/expected_total"
    assert os.path.isfile(expected_path), f"Missing truth file: {expected_path}"

    with open(expected_path, "r") as f:
        expected_total = f.read().strip()

    with open(path, "r") as f:
        actual_total = f.read().strip()

    assert actual_total == expected_total, f"Expected {path} to contain {expected_total}, but got {actual_total}"

def test_log_processor_fixed():
    path = "/home/user/log_processor.py"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        content = f.read()

    # Check that failed_requests.append is no longer present
    # Or more generally, check that the script doesn't append to a list in the except block
    # A simple regex to check for .append inside the script, particularly related to failed_requests
    assert "failed_requests.append" not in content, "The memory leak is still present: 'failed_requests.append' was found in log_processor.py"