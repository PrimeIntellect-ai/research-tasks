# test_final_state.py
import os
import hashlib
import pytest

REPORT_FILE = "/home/user/report.txt"
SCRIPT_FILE = "/home/user/suspicious_service.py"
EXPECTED_SHA256 = "a7f998ccb05ab64d99815a5105a2eab4d516d26732ea952eeeb4918e7e2c9438"

def test_report_file_exists():
    assert os.path.isfile(REPORT_FILE), f"The report file {REPORT_FILE} does not exist."

def test_report_content():
    assert os.path.isfile(REPORT_FILE), f"The report file {REPORT_FILE} does not exist."
    assert os.path.isfile(SCRIPT_FILE), f"The script file {SCRIPT_FILE} does not exist."

    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"The report file {REPORT_FILE} must contain at least two lines."

    # Verify Line 1 (SHA256 of the cookie)
    assert lines[0] == EXPECTED_SHA256, (
        f"Line 1 of {REPORT_FILE} is incorrect. "
        f"Expected {EXPECTED_SHA256}, but got {lines[0]}."
    )

    # Compute MD5 of the script file
    with open(SCRIPT_FILE, "rb") as f:
        file_content = f.read()
    expected_md5 = hashlib.md5(file_content).hexdigest()

    # Verify Line 2 (MD5 of the script file)
    assert lines[1] == expected_md5, (
        f"Line 2 of {REPORT_FILE} is incorrect. "
        f"Expected {expected_md5}, but got {lines[1]}."
    )