# test_final_state.py

import os
import json
import hashlib
import csv
import pytest

def test_cpp_source_exists():
    path = "/home/user/policy_enforcer.cpp"
    assert os.path.isfile(path), f"Expected C++ source file {path} is missing."

def test_audit_report_exists():
    path = "/home/user/audit_report.csv"
    assert os.path.isfile(path), f"Expected report file {path} is missing."

def test_audit_report_content():
    deployments_path = "/home/user/deployments.json"
    dictionary_path = "/home/user/dictionary.txt"
    report_path = "/home/user/audit_report.csv"

    assert os.path.isfile(deployments_path), f"Missing {deployments_path}"
    assert os.path.isfile(dictionary_path), f"Missing {dictionary_path}"
    assert os.path.isfile(report_path), f"Missing {report_path}"

    # Build dictionary hashes
    with open(dictionary_path, "r") as f:
        words = [line.strip() for line in f if line.strip()]

    hash_to_word = {}
    for word in words:
        md5_hash = hashlib.md5(word.encode('utf-8')).hexdigest()
        hash_to_word[md5_hash] = word

    # Process deployments
    with open(deployments_path, "r") as f:
        deployments = json.load(f)

    expected_rows = [["app_name", "password_cracked", "csp_secure"]]
    for dep in deployments:
        app_name = dep.get("app_name", "")
        admin_hash = dep.get("admin_hash", "")
        csp_header = dep.get("csp_header", "")

        password_cracked = hash_to_word.get(admin_hash, "SAFE")

        if "unsafe-inline" in csp_header or "unsafe-eval" in csp_header:
            csp_secure = "FAIL"
        else:
            csp_secure = "PASS"

        expected_rows.append([app_name, password_cracked, csp_secure])

    # Read the actual report
    actual_rows = []
    with open(report_path, "r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."

def test_audit_report_formatting():
    report_path = "/home/user/audit_report.csv"
    assert os.path.isfile(report_path), f"Missing {report_path}"

    with open(report_path, "rb") as f:
        content = f.read()

    # Ensure standard Unix newlines
    assert b"\r\n" not in content, "CSV file contains Windows-style (CRLF) newlines instead of Unix-style (LF)."

    # Ensure no extra spaces around commas
    lines = content.decode('utf-8').split('\n')
    for line in lines:
        if line:
            assert ", " not in line and " ," not in line, f"Extra spaces found around commas in line: '{line}'"