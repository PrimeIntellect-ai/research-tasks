# test_final_state.py

import os
import subprocess
import hashlib
import pytest

def test_script_exists():
    """Verify that the user script exists."""
    script_path = "/home/user/recover_evidence.py"
    assert os.path.exists(script_path), f"Required script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a regular file."

def test_report_exists():
    """Verify that the generated report exists."""
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist. Did you run your script?"
    assert os.path.isfile(report_path), f"{report_path} is not a regular file."

def test_report_content():
    """Verify the contents of the generated report against the expected derived truth."""
    report_path = "/home/user/report.txt"
    rogue_cert_path = "/home/user/evidence/certs/rogue.crt"

    # Derive the expected hash directly from the rogue certificate
    assert os.path.exists(rogue_cert_path), f"Rogue certificate {rogue_cert_path} is missing from the environment."
    try:
        der_data = subprocess.check_output(
            ["openssl", "x509", "-in", rogue_cert_path, "-outform", "DER"],
            stderr=subprocess.DEVNULL
        )
        expected_hash = hashlib.sha256(der_data).hexdigest()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to process rogue certificate for test verification: {e}")

    expected_domain = "exfil.evil.net"
    expected_payload = '{"user": "admin", "action": "payment", "cc": "[REDACTED]", "cvv": "123", "secondary_cc": "[REDACTED]"}'

    expected_lines = [
        f"Rogue Domain: {expected_domain}",
        f"Rogue Cert Hash: {expected_hash}",
        f"Redacted Payload: {expected_payload}"
    ]
    expected_content = "\n".join(expected_lines)

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, (
        f"Report content at {report_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Got:\n{content}"
    )