# test_final_state.py

import os
import pytest

def test_recovery_report_exists():
    """Test that the recovery report was generated."""
    report_path = "/home/user/recovery_report.txt"
    assert os.path.isfile(report_path), f"Expected report file not found at {report_path}"

def test_recovery_report_contents():
    """Test that the recovery report contains the correct information."""
    report_path = "/home/user/recovery_report.txt"
    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Recovered IDs: 1,2,3,5",
        "Precision Loss ID: 2"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == 2, f"Expected exactly 2 lines in the report, got {len(actual_lines)}"

    assert actual_lines[0] == expected_lines[0], f"Expected first line to be '{expected_lines[0]}', but got '{actual_lines[0]}'"
    assert actual_lines[1] == expected_lines[1], f"Expected second line to be '{expected_lines[1]}', but got '{actual_lines[1]}'"

def test_recover_c_exists():
    """Test that the recover.c source file exists."""
    source_path = "/home/user/recover.c"
    assert os.path.isfile(source_path), f"Expected C source file not found at {source_path}"