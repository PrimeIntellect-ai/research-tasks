# test_final_state.py

import os
import re
import time
import requests
import pytest

def test_makefile_fixed_and_installed():
    auditor_path = "/home/user/bin/auditor.sh"
    worker_path = "/home/user/bin/worker.sh"

    assert os.path.exists(auditor_path), f"File {auditor_path} is missing. Did you run make install?"
    assert os.path.exists(worker_path), f"File {worker_path} is missing. Did you run make install?"

    assert os.access(auditor_path, os.X_OK), f"File {auditor_path} is not executable."
    assert os.access(worker_path, os.X_OK), f"File {worker_path} is not executable."

def test_cwe_identification():
    cwe_path = "/app/cwe.txt"
    assert os.path.exists(cwe_path), f"File {cwe_path} is missing."
    with open(cwe_path, "r") as f:
        content = f.read().strip()
    assert "CWE-532" in content.upper(), f"Expected CWE-532 in {cwe_path}, got {content}"

def test_certificates_exist():
    assert os.path.exists("/app/ca.crt"), "Root CA certificate /app/ca.crt is missing."
    assert os.path.exists("/app/server.crt"), "Server certificate /app/server.crt is missing."
    assert os.path.exists("/app/server.key"), "Server private key /app/server.key is missing."

def test_auditor_script_modifications():
    auditor_path = "/home/user/bin/auditor.sh"
    with open(auditor_path, "r") as f:
        content = f.read()

    # Check that worker.sh is not called with the token as an argument
    assert not re.search(r'worker\.sh\s+"?\$token"?', content), "worker.sh is still being called with the token as a command-line argument."

    # Check that SECRET_TOKEN is exported or passed
    assert "SECRET_TOKEN" in content, "SECRET_TOKEN environment variable is not used in auditor.sh."

def test_https_service_and_redaction():
    token_value = "verification_token_778"
    url = "https://127.0.0.1:8443/"
    headers = {
        "Authorization": f"Bearer {token_value}"
    }

    try:
        response = requests.get(url, headers=headers, verify="/app/ca.crt", timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTPS service or verify certificate: {e}")

    # Wait a moment for the script to write to the log
    time.sleep(1)

    log_path = "/app/audit.log"
    assert os.path.exists(log_path), f"Audit log {log_path} was not created."

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "[REDACTED]" in log_content, "The string [REDACTED] was not found in the audit log."
    assert token_value not in log_content, f"The sensitive token '{token_value}' was leaked in the audit log!"