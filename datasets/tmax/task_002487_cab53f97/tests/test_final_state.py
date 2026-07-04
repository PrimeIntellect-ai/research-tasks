# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_tls_certificate():
    """Test that the TLS certificate and private key are generated correctly."""
    cert_file = "/home/user/certs/new_cert.pem"
    key_file = "/home/user/certs/new_key.pem"

    assert os.path.isfile(cert_file), f"Certificate file {cert_file} does not exist."
    assert os.path.isfile(key_file), f"Private key file {key_file} does not exist."

    # Check if CN is localhost
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_file, "-noout", "-subject"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to read certificate with openssl."
    assert "CN = localhost" in result.stdout or "CN=localhost" in result.stdout, "Certificate Common Name (CN) is not localhost."

    # Check if private key is valid RSA
    result_key = subprocess.run(
        ["openssl", "rsa", "-in", key_file, "-check", "-noout"],
        capture_output=True, text=True
    )
    assert result_key.returncode == 0, "Private key is not a valid RSA key."

def test_key_permissions():
    """Test that the private key permissions are set to 400."""
    key_file = "/home/user/certs/new_key.pem"
    assert os.path.isfile(key_file), f"Private key file {key_file} does not exist."

    st = os.stat(key_file)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Permissions of {key_file} are {oct(permissions)}, expected 0o400."

def test_log_redaction():
    """Test that the log file is properly redacted."""
    clean_log_file = "/home/user/logs/app_clean.log"
    assert os.path.isfile(clean_log_file), f"Redacted log file {clean_log_file} does not exist."

    with open(clean_log_file, "r") as f:
        content = f.read()

    assert "v1_secret_9982_abcd" not in content, "Original API key still found in the redacted log."
    assert content.count("API_KEY=REDACTED") == 2, "Expected exactly 2 instances of API_KEY=REDACTED in the log."
    assert "2023-10-01 10:00:01 INFO Server started" in content, "Original non-sensitive log lines are missing."

def test_exploit_payload():
    """Test that the exploit payload file exists with correct content and permissions."""
    payload_file = "/home/user/uploads/test_payload.txt"
    assert os.path.isfile(payload_file), f"Payload file {payload_file} does not exist."

    with open(payload_file, "r") as f:
        content = f.read()

    assert content.strip() == "../../etc/passwd", "Payload file content is incorrect."

    st = os.stat(payload_file)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o600, f"Permissions of {payload_file} are {oct(permissions)}, expected 0o600."