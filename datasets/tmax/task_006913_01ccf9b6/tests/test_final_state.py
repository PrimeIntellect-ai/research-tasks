# test_final_state.py

import os
import pytest

def test_audit_exploit_c_exists():
    path = "/home/user/audit_exploit.c"
    assert os.path.isfile(path), f"Expected C source file {path} does not exist."

def test_audit_report_log_content():
    log_path = "/home/user/audit_report.log"
    flag_path = "/home/user/restricted/flag.txt"

    assert os.path.isfile(log_path), f"The audit report {log_path} was not created."
    assert os.path.isfile(flag_path), f"The flag file {flag_path} is missing."

    with open(flag_path, "r") as f:
        flag_content = f.read().strip()

    expected_content = f"[AUDIT_TRAIL] VULNERABILITY_CONFIRMED: {flag_content}"

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    assert log_content == expected_content, (
        f"The content of {log_path} is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Got: '{log_content}'"
    )

def test_vuln_uploader_unmodified():
    path = "/home/user/vuln_uploader"
    assert os.path.isfile(path), f"The original binary {path} was removed or missing."
    assert os.access(path, os.X_OK), f"The original binary {path} is no longer executable."