# test_final_state.py
import os
import re
import pytest

def test_redact_logs_script_exists():
    script_path = "/home/user/redact_logs.sh"
    assert os.path.exists(script_path), f"The script {script_path} was not created."

def test_redacted_log_content():
    access_log_path = "/home/user/access.log"
    redacted_log_path = "/home/user/redacted.log"

    assert os.path.exists(redacted_log_path), f"The redacted log {redacted_log_path} is missing."

    with open(access_log_path, "r") as f:
        original_content = f.read()

    # Derive expected content by replacing alphanumeric session IDs
    expected_content = re.sub(r"session_id=[a-zA-Z0-9]+", "session_id=[REDACTED]", original_content)

    with open(redacted_log_path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), "The redacted.log content does not match the expected redaction pattern."

def test_vuln_line():
    vuln_line_path = "/home/user/vuln_line.txt"
    assert os.path.exists(vuln_line_path), f"Missing {vuln_line_path}"

    with open(vuln_line_path, "r") as f:
        content = f.read().strip()

    assert content == "14", f"Expected vulnerable line number to be 14, got '{content}'."

def test_invalid_cert():
    invalid_cert_path = "/home/user/invalid_cert.txt"
    assert os.path.exists(invalid_cert_path), f"Missing {invalid_cert_path}"

    with open(invalid_cert_path, "r") as f:
        content = f.read().strip()

    assert content == "server.crt", f"Expected invalid cert to be 'server.crt', got '{content}'."

def test_payload():
    payload_path = "/home/user/payload.txt"
    assert os.path.exists(payload_path), f"Missing {payload_path}"

    with open(payload_path, "r") as f:
        content = f.read().strip()

    assert content in ["//evil.com", "//evil.com/"], f"Expected payload to be a protocol-relative URL to evil.com, got '{content}'."