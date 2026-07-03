# test_final_state.py

import os
import pytest

def test_generate_report_script_exists_and_executable():
    script_path = "/home/user/generate_report.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_audit_report_exists():
    report_path = "/home/user/audit_report.txt"
    assert os.path.exists(report_path), f"The report file {report_path} does not exist."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

def test_audit_report_content():
    report_path = "/home/user/audit_report.txt"
    if not os.path.exists(report_path):
        pytest.fail(f"Report file {report_path} is missing.")

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for correct environment variable injection
    assert "Target IP: 10.0.0.1" in content, "The target IP was not correctly set to 10.0.0.1 in the report."

    # Check for redaction of AWS keys
    assert "Active AWS Credential: REDACTED" in content, "The AWS credential in the tool output was not redacted."
    assert "key REDACTED for backup" in content, "The AWS credential in the firewall rules file was not redacted."
    assert "AKIA" not in content, "Found unredacted AWS credentials (AKIA...) in the report."

    # Check for XSS mitigation
    assert "&lt;script&gt;alert('XSS')&lt;/script&gt;" in content, "The XSS payload was not correctly escaped."
    assert "<" not in content, "Found unescaped '<' character in the report."
    assert ">" not in content, "Found unescaped '>' character in the report."