# test_final_state.py

import os
import pytest

def test_c_source_file_exists():
    """Test that the C source code file exists."""
    path = "/home/user/audit_report.c"
    assert os.path.isfile(path), f"The C source file was not found at {path}"

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    path = "/home/user/audit_report"
    assert os.path.isfile(path), f"The compiled executable was not found at {path}"
    assert os.access(path, os.X_OK), f"The file at {path} is not executable"

def test_csv_report_exists():
    """Test that the generated CSV report exists."""
    path = "/home/user/compliance_report.csv"
    assert os.path.isfile(path), f"The compliance report CSV was not found at {path}"

def test_csv_report_contents():
    """Test that the CSV report contains the exact expected output."""
    path = "/home/user/compliance_report.csv"
    assert os.path.isfile(path), f"The compliance report CSV was not found at {path}"

    expected_lines = [
        "Department Head,Employee,System Name,Risk Level,Rank",
        "Alice Smith,Bob Jones,AWS Prod,9,1",
        "Alice Smith,Charlie Brown,Jenkins,9,2",
        "Diana Prince,Evan Wright,Payroll System,10,1",
        "Diana Prince,Diana Prince,Stripe,8,2"
    ]

    with open(path, "r", encoding="utf-8") as f:
        # Read lines, stripping whitespace and ignoring empty lines
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"CSV contents do not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )