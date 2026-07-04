# test_final_state.py
import os
import re
import subprocess
import pytest

def test_certificate_exists_and_valid():
    cert_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"

    assert os.path.exists(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.exists(key_path), f"Private key file {key_path} does not exist."

    # Check private key validity
    key_check = subprocess.run(
        ["openssl", "rsa", "-in", key_path, "-check", "-noout"],
        capture_output=True, text=True
    )
    assert key_check.returncode == 0, f"Private key is invalid or cannot be read: {key_check.stderr}"

    # Check certificate subject for CN=inspector.local
    cert_check = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout", "-subject"],
        capture_output=True, text=True
    )
    assert cert_check.returncode == 0, f"Certificate is invalid or cannot be read: {cert_check.stderr}"

    subject = cert_check.stdout.strip()
    assert re.search(r'CN\s*=\s*inspector\.local', subject), f"Certificate subject does not contain CN=inspector.local. Subject found: {subject}"

def test_cwe_remediation():
    c_file = "/home/user/inspector/traffic_inspector.c"
    assert os.path.exists(c_file), f"Source file {c_file} does not exist."

    with open(c_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify the exact vulnerable strcpy is removed
    assert "strcpy(buffer, req)" not in content.replace(" ", ""), "The vulnerable strcpy call is still present in the C code."

def test_decrypted_log_contents():
    log_file = "/home/user/inspector/decrypted_log.txt"
    assert os.path.exists(log_file), f"Decrypted log file {log_file} does not exist. Did the utility compile and run successfully?"

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify the injected CSP header
    expected_csp = "Content-Security-Policy: default-src 'self';"
    assert expected_csp in content, "The required Content-Security-Policy header was not found in the decrypted log."

    # Verify the secret payload is still intact
    expected_payload = "<html><body>Secret payload!</body></html>"
    assert expected_payload in content, "The decrypted payload is missing or corrupted in the output log."