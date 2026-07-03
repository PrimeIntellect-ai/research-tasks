# test_final_state.py
import os
import csv

def test_final_audit_csv_exists():
    assert os.path.isfile("/home/user/final_audit.csv"), "The file /home/user/final_audit.csv does not exist."

def test_final_audit_csv_content():
    expected_rows = [
        ["Request", "SessionID", "Filename", "TraversalAttempt", "CertValid", "HashMatch"],
        ["req1.txt", "abc123xyz", "report.pdf", "0", "true", "true"],
        ["req2.txt", "malicious999", "../../../etc/passwd", "1", "false", "true"],
        ["req3.txt", "legit888", "image.png", "0", "true", "false"]
    ]

    with open("/home/user/final_audit.csv", "r", newline="") as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader if row] # ignore empty lines

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, but got {len(actual_rows)}."

    for i, (expected, actual) in enumerate(zip(expected_rows, actual_rows)):
        assert actual == expected, f"Row {i} in CSV does not match expected. Expected: {expected}, Actual: {actual}"

def test_audit_parser_exists():
    assert os.path.isfile("/home/user/audit_parser.c"), "/home/user/audit_parser.c is missing."
    assert os.path.isfile("/home/user/audit_parser"), "Compiled executable /home/user/audit_parser is missing."
    assert os.access("/home/user/audit_parser", os.X_OK), "/home/user/audit_parser is not executable."

def test_generate_audit_script_exists():
    assert os.path.isfile("/home/user/generate_audit.sh"), "/home/user/generate_audit.sh is missing."