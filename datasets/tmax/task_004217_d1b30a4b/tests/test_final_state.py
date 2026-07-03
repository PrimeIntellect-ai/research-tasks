# test_final_state.py

import os
import subprocess
import pytest

def test_certificate_and_key():
    cert_path = "/home/user/new_cert.pem"
    key_path = "/home/user/new_key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Private key file {key_path} does not exist."

    result = subprocess.run(
        ['openssl', 'x509', '-in', cert_path, '-noout', '-subject'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to read certificate with openssl. Error: {result.stderr}"

    subject = result.stdout.strip()
    assert "CN = test.local" in subject or "CN=test.local" in subject, \
        f"Certificate subject does not contain 'CN = test.local'. Actual subject: {subject}"

def test_deploy_log_redacted():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run the deploy script?"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "NewSecurePass2024!" not in content, \
        "The plaintext password 'NewSecurePass2024!' was found in the deploy.log file. It should be redacted."

    assert "***REDACTED***" in content, \
        "The string '***REDACTED***' was not found in deploy.log. The password should be replaced with this exact string."

def test_auth_result_success():
    result_path = "/home/user/auth_result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist. Did you run the auth_test.py script?"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert "AUTH_FLOW_SUCCESS" in content, \
        f"Expected 'AUTH_FLOW_SUCCESS' in {result_path}, but found: {content}"