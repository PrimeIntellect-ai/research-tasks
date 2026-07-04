# test_final_state.py

import os
import hashlib
import pytest

def test_audit_report_csv_content():
    csv_path = "/home/user/audit_report.csv"
    assert os.path.isfile(csv_path), f"File missing: {csv_path}"

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "alice,d09a3410,pass",
        "bob,1e3f8a00,carl",
        "charlie,8bf8f47d,luke",
        "diana,717c1407,zack",
        "eve,c9842a27,root"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in {csv_path}, found {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Row {i+1} mismatch: expected '{expected}', got '{actual}'"

def test_audit_report_sha256_validity():
    csv_path = "/home/user/audit_report.csv"
    sha_path = "/home/user/audit_report.sha256"

    assert os.path.isfile(csv_path), f"File missing: {csv_path}"
    assert os.path.isfile(sha_path), f"File missing: {sha_path}"

    with open(csv_path, "rb") as f:
        csv_bytes = f.read()

    actual_sha256 = hashlib.sha256(csv_bytes).hexdigest()

    with open(sha_path, "r") as f:
        sha_content = f.read().strip()

    # The standard sha256sum output looks like: "<hash>  audit_report.csv" or similar
    # We just need to check if the computed hash is present in the file
    assert actual_sha256 in sha_content, f"The computed SHA-256 ({actual_sha256}) was not found in {sha_path}"