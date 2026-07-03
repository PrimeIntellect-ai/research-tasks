# test_final_state.py
import os
import re
import pytest

def test_certificates_generated():
    """Verify that the self-signed certificate and private key were generated."""
    cert_path = "/home/user/vuln_app/certs/server.crt"
    key_path = "/home/user/vuln_app/certs/server.key"

    assert os.path.isfile(cert_path), f"Certificate file is missing: {cert_path}"
    assert os.path.isfile(key_path), f"Private key file is missing: {key_path}"

    with open(cert_path, 'r') as f:
        cert_content = f.read()
    assert "-----BEGIN CERTIFICATE-----" in cert_content, f"File {cert_path} does not appear to be a valid PEM certificate."

    with open(key_path, 'r') as f:
        key_content = f.read()
    assert "-----BEGIN PRIVATE KEY-----" in key_content or "-----BEGIN RSA PRIVATE KEY-----" in key_content, \
        f"File {key_path} does not appear to be a valid PEM private key."

def test_hacked_txt_exists_and_content():
    """Verify that the path traversal exploit successfully created hacked.txt with the correct content."""
    hacked_file = "/home/user/vuln_app/hacked.txt"

    assert os.path.isfile(hacked_file), f"The exploit file was not found at the expected location: {hacked_file}"

    with open(hacked_file, 'r') as f:
        content = f.read().strip()

    assert content == "EXPLOIT_SUCCESS", f"The content of {hacked_file} is incorrect. Expected 'EXPLOIT_SUCCESS', got '{content}'."

def test_timestamp_extracted():
    """Verify that the log was parsed and the timestamp was extracted correctly."""
    timestamp_file = "/home/user/vuln_app/timestamp.txt"

    assert os.path.isfile(timestamp_file), f"The timestamp file is missing: {timestamp_file}"

    with open(timestamp_file, 'r') as f:
        content = f.read().strip()

    # Regex for a timestamp like 14/Nov/2023:15:23:01
    pattern = re.compile(r"^[0-9]{2}/[a-zA-Z]{3}/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}$")
    assert pattern.match(content), f"The extracted timestamp '{content}' does not match the expected format (e.g., DD/Mon/YYYY:HH:MM:SS)."

def test_privesc_user_identified():
    """Verify that the correct user was identified for the privilege escalation vector."""
    privesc_file = "/home/user/vuln_app/privesc_user.txt"

    assert os.path.isfile(privesc_file), f"The privesc user file is missing: {privesc_file}"

    with open(privesc_file, 'r') as f:
        content = f.read().strip()

    assert content == "cicd_runner", f"The identified user is incorrect. Expected 'cicd_runner', got '{content}'."