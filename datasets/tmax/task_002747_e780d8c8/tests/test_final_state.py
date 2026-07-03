# test_final_state.py
import os
import pytest

def test_compliance_auditor_files_exist():
    c_source = "/home/user/compliance_auditor.c"
    binary = "/home/user/compliance_auditor"

    assert os.path.isfile(c_source), f"C source file {c_source} does not exist."
    assert os.path.isfile(binary), f"Compiled binary {binary} does not exist."
    assert os.access(binary, os.X_OK), f"File {binary} is not executable."

def test_audit_trail_content():
    audit_file = "/home/user/audit_trail.txt"
    assert os.path.isfile(audit_file), f"Audit report {audit_file} does not exist."

    with open(audit_file, "r") as f:
        content = f.read()

    assert "[AUDIT REPORT]" in content, "Missing '[AUDIT REPORT]' header."
    assert "AUTH_TOKEN: Z79_Compliance_Req" in content, "Incorrect or missing AUTH_TOKEN."
    assert "CERT_STATUS: VALID" in content, "Incorrect or missing CERT_STATUS."
    assert "IDS_MATCHES: 2" in content, "Incorrect or missing IDS_MATCHES."