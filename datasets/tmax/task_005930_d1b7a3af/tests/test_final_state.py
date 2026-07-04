# test_final_state.py

import os
import pytest

AUDIT_DIR = "/home/user/audit_system"
LOGS_DIR = os.path.join(AUDIT_DIR, "logs")
REPORT_FILE = os.path.join(AUDIT_DIR, "report.txt")
C_PROGRAM_FILE = os.path.join(AUDIT_DIR, "verify_integrity.c")
LOG_FILES = ["access.log", "auth.log", "system.log"]

def test_report_content():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} is missing."
    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 3, f"Report file should contain exactly 3 lines, found {len(lines)}."
    assert lines[0] == "system.log", f"Line 1 of report should be 'system.log', found '{lines[0]}'."
    assert lines[1] == "10.0.5.55", f"Line 2 of report should be '10.0.5.55', found '{lines[1]}'."
    assert lines[2] == "REMEDIATED", f"Line 3 of report should be 'REMEDIATED', found '{lines[2]}'."

def test_remediated_permissions():
    assert os.path.isdir(LOGS_DIR), f"Directory {LOGS_DIR} is missing."
    dir_stat = os.stat(LOGS_DIR)
    assert oct(dir_stat.st_mode)[-3:] == '750', f"Permissions for {LOGS_DIR} should be 750, found {oct(dir_stat.st_mode)[-3:]}."

    for log_file in LOG_FILES:
        file_path = os.path.join(LOGS_DIR, log_file)
        assert os.path.isfile(file_path), f"Log file {file_path} is missing."
        file_stat = os.stat(file_path)
        assert oct(file_stat.st_mode)[-3:] == '640', f"Permissions for {file_path} should be 640, found {oct(file_stat.st_mode)[-3:]}."

def test_c_program_exists_and_contains_openssl():
    assert os.path.isfile(C_PROGRAM_FILE), f"C program {C_PROGRAM_FILE} is missing."
    with open(C_PROGRAM_FILE, "r") as f:
        content = f.read()

    assert "openssl" in content.lower() or "evp.h" in content.lower() or "sha.h" in content.lower(), \
        "C program does not appear to include OpenSSL headers (e.g., <openssl/sha.h> or <openssl/evp.h>)."