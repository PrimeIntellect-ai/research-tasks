# test_final_state.py
import os
import pytest

def test_summary_file_exists():
    """Test that the summary.md file has been generated."""
    file_path = "/home/user/summary.md"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_summary_file_content():
    """Test that the summary.md file contains the correctly aggregated report."""
    file_path = "/home/user/summary.md"
    expected_content = """# Log Summary

## Hour: 2023-11-01T08:00:00Z
- auth_fail: 3
- db_timeout: 1
- rate_limit: 2

## Hour: 2023-11-01T09:00:00Z
- db_timeout: 7

## Hour: 2023-11-01T10:00:00Z
- auth_fail: 5
- rate_limit: 4"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of {file_path} does not match the expected Markdown report."