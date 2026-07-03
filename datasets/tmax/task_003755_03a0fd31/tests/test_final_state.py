# test_final_state.py

import os
import pytest

def test_decrypt_c_exists():
    path = "/home/user/decrypt.c"
    assert os.path.exists(path), f"The file {path} is missing."
    assert os.path.isfile(path), f"The path {path} is not a file."

def test_audit_report_exists_and_content():
    report_path = "/home/user/audit_report.txt"
    assert os.path.exists(report_path), f"The report file {report_path} is missing."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

    with open(report_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"The report file {report_path} must contain at least two lines."

    # Check Line 1: The key
    expected_key = "C0mpL1@nc3"
    assert lines[0] == expected_key, f"The first line of the report is incorrect. Expected {expected_key}, but got {lines[0]}"

    # Check Line 2: The SQL injection payload
    payload = lines[1]
    expected_payload_logic = "admin' OR '1'='1' --"
    assert expected_payload_logic in payload, f"The second line does not contain the correct SQL injection payload logic. Got: {payload}"