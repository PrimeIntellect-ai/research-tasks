# test_final_state.py

import os
import pytest

def test_c_source_exists():
    """Verify that the C source file exists."""
    assert os.path.isfile('/home/user/get_org.c'), "The C source file /home/user/get_org.c does not exist."

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    exe_path = '/home/user/get_org'
    assert os.path.isfile(exe_path), f"The executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_report_content():
    """Verify that the output report exists and contains the correct hierarchy."""
    report_path = '/home/user/org_report.txt'
    assert os.path.isfile(report_path), f"The report file {report_path} does not exist."

    expected_lines = [
        "0 - 2: Bob",
        "1 - 4: David",
        "1 - 5: Eve",
        "2 - 6: Frank",
        "2 - 7: Grace",
        "3 - 9: Ivan"
    ]

    with open(report_path, 'r') as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The content of {report_path} is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )