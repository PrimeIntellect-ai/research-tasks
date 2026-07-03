# test_final_state.py

import os
import hashlib
import pytest

HOME_DIR = "/home/user"
REPORT_PATH = os.path.join(HOME_DIR, "rotation_report.txt")
SECRET_PATH = os.path.join(HOME_DIR, "new_secret.txt")

def test_rotation_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}"

def test_rotation_report_content():
    assert os.path.isfile(SECRET_PATH), f"Secret file not found at {SECRET_PATH}"

    with open(SECRET_PATH, 'r') as f:
        new_secret = f.read().strip()

    expected_token = hashlib.sha256(f"admin:{new_secret}".encode()).hexdigest()

    with open(REPORT_PATH, 'r') as f:
        lines = [line.strip() for line in f.read().splitlines()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {REPORT_PATH}, found {len(lines)}"

    cwe_line = lines[0]
    pin_line = lines[1]
    token_line = lines[2]

    assert cwe_line == "CWE-327", f"Line 1 expected to be 'CWE-327', got '{cwe_line}'"
    assert pin_line == "4921", f"Line 2 expected to be '4921', got '{pin_line}'"
    assert token_line == expected_token, f"Line 3 expected to be '{expected_token}', got '{token_line}'"