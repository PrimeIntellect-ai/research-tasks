# test_final_state.py

import os
import stat
import re
import pytest

SECURE_AUDIT_DIR = "/home/user/secure_audit"
APP_LOGS_DIR = "/home/user/app_logs"
AUDIT_REPORT = "/home/user/audit_report.txt"

def get_permissions(path):
    st = os.stat(path)
    return stat.S_IMODE(st.st_mode)

def test_secure_audit_directory_permissions():
    assert os.path.isdir(SECURE_AUDIT_DIR), f"Directory {SECURE_AUDIT_DIR} does not exist."
    perms = get_permissions(SECURE_AUDIT_DIR)
    assert perms == 0o700, f"Directory {SECURE_AUDIT_DIR} should have 700 permissions, got {oct(perms)}."

def test_redacted_logs_content_and_permissions():
    log_files = ["web_access.log", "api_error.log", "system.log"]
    total_expected_redactions = 0
    token_pattern = re.compile(r"Token:\s+[a-zA-Z0-9]+")

    for filename in log_files:
        orig_path = os.path.join(APP_LOGS_DIR, filename)
        secure_path = os.path.join(SECURE_AUDIT_DIR, filename)

        assert os.path.isfile(secure_path), f"Redacted log file {secure_path} does not exist."

        # Check permissions
        perms = get_permissions(secure_path)
        assert perms == 0o600, f"File {secure_path} should have 600 permissions, got {oct(perms)}."

        # Read original to compute expected content
        with open(orig_path, "r") as f:
            orig_content = f.read()

        # Compute expected redactions
        expected_content, count = token_pattern.subn("Token: [REDACTED]", orig_content)
        total_expected_redactions += count

        # Read actual redacted content
        with open(secure_path, "r") as f:
            actual_content = f.read()

        assert actual_content == expected_content, f"Content of {secure_path} does not match expected redacted content."

def test_audit_report():
    assert os.path.isfile(AUDIT_REPORT), f"Audit report {AUDIT_REPORT} does not exist."

    with open(AUDIT_REPORT, "r") as f:
        content = f.read().strip()

    expected_line = "Total Redactions: 4"
    assert content == expected_line, f"Audit report content is incorrect. Expected '{expected_line}', got '{content}'."