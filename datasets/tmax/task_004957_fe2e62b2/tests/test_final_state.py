# test_final_state.py

import os
import pytest

def test_audit_report_exists():
    assert os.path.isfile("/home/user/audit_report.txt"), "/home/user/audit_report.txt does not exist"

def test_audit_report_content():
    expected_content = """[Decrypted Events]
Unauthorized root login detected from 10.0.0.5
Data exfiltration blocked on interface eth0

[Tampered File]
/home/user/conf/service.ini
"""
    with open("/home/user/audit_report.txt", "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), "The content of /home/user/audit_report.txt does not match the expected report format and content."