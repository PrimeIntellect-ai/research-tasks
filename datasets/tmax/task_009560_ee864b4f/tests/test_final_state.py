# test_final_state.py

import os
import pytest

def test_audit_tool_source_exists():
    file_path = "/home/user/audit_tool.c"
    assert os.path.isfile(file_path), f"Source file {file_path} is missing."

def test_audit_tool_executable_exists():
    file_path = "/home/user/audit_tool"
    assert os.path.isfile(file_path), f"Executable file {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_compliance_report_exists_and_correct():
    file_path = "/home/user/compliance_report.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    expected_lines = [
        "USR_Alice,3",
        "USR_Bob,1",
        "USR_Diana,1",
        "USR_Eve,1"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    # Strip any potential carriage returns or trailing spaces
    content = [line.strip() for line in content if line.strip()]

    # Sometimes students might include a header like "User,RestrictedAccessCount"
    if content and content[0].lower().startswith("user"):
        content = content[1:]

    assert content == expected_lines, f"Contents of {file_path} do not match the expected output.\nExpected: {expected_lines}\nGot: {content}"