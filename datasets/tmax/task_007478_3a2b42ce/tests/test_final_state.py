# test_final_state.py

import os
import pytest

def test_auditor_cpp_exists():
    file_path = "/home/user/auditor.cpp"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The C++ source code was not created."

def test_audit_job_sh_exists():
    file_path = "/home/user/audit_job.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The execution script was not created."

def test_auditor_binary_exists():
    file_path = "/home/user/auditor"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The C++ program was not compiled."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_report_log_content():
    file_path = "/home/user/report.log"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The report log was not generated."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "GROUP_CHECK: FAIL (eve,mallory)",
        "ROUTE_CHECK: FAIL",
        "QUOTA_CHECK: FAIL (bob,charlie)"
    ]

    assert len(lines) == 3, f"Expected exactly 3 lines in {file_path}, found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} in {file_path} is incorrect. Expected: '{expected}', Got: '{lines[i]}'."