# test_final_state.py

import os
import pytest

def test_audit_report_exists_and_content():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist. The audit report was not generated."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {report_path}, found {len(lines)}."

    # Check CWE ID
    assert lines[0] == "CWE-22", f"Expected 'CWE-22' on line 1, found '{lines[0]}'."

    # Check count
    assert lines[1] == "2", f"Expected count '2' on line 2, found '{lines[1]}'."

    # Check decoded payloads (sorted alphabetically)
    expected_payloads = [
        "../../../../etc/shadow",
        "../../../etc/passwd"
    ]

    actual_payloads = lines[2:]
    assert len(actual_payloads) == len(expected_payloads), f"Expected {len(expected_payloads)} payloads, found {len(actual_payloads)}."

    for i, (expected, actual) in enumerate(zip(expected_payloads, actual_payloads)):
        assert actual == expected, f"Expected payload '{expected}' on line {i+3}, found '{actual}'."