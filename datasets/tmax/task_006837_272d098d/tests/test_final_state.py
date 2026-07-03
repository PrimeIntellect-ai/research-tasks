# test_final_state.py

import os
import subprocess
import pytest

def test_audit_report_content():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report missing at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {report_path}, found {len(lines)}"

    assert lines[0] == "CRACKED_PASSWORD: password", f"Line 1 incorrect. Expected 'CRACKED_PASSWORD: password', got '{lines[0]}'"
    assert lines[1] == "REDACTED_COUNT: 2", f"Line 2 incorrect. Expected 'REDACTED_COUNT: 2', got '{lines[1]}'"
    assert lines[2] == "CERT_ACTION: REPLACED", f"Line 3 incorrect. Expected 'CERT_ACTION: REPLACED', got '{lines[2]}'"

def test_app_redacted_log_content():
    redacted_log_path = "/home/user/app_redacted.log"
    assert os.path.isfile(redacted_log_path), f"Redacted log missing at {redacted_log_path}"

    with open(redacted_log_path, "r") as f:
        content = f.read()

    expected_content = """[INFO] Application started
[DEBUG] Connecting to AWS with key AKIA[REDACTED] for bucket access.
[INFO] User logged in.
[DEBUG] Backup completed. Used credentials: AKIA[REDACTED] to store payload.
[ERROR] Failed to connect.
"""
    assert content.strip() == expected_content.strip(), "The contents of app_redacted.log do not match the expected redacted output."

def test_new_certificate_exists_and_valid():
    crt_path = "/home/user/certs/new.crt"
    key_path = "/home/user/certs/new.key"

    assert os.path.isfile(crt_path), f"New certificate missing at {crt_path}"
    assert os.path.isfile(key_path), f"New private key missing at {key_path}"

    # Check the subject of the certificate
    try:
        result = subprocess.run(
            ["openssl", "x509", "-in", crt_path, "-noout", "-subject"],
            capture_output=True,
            text=True,
            check=True
        )
        subject_output = result.stdout.strip()
        assert "CN = secure.local" in subject_output or "CN=secure.local" in subject_output, \
            f"Certificate Common Name is incorrect. Expected 'secure.local', got: {subject_output}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read certificate with openssl: {e.stderr}")