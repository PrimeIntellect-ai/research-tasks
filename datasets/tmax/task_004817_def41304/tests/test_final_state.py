# test_final_state.py

import os
import subprocess
import tempfile
import base64
import time
import pytest
import requests

PRIVATE_KEY = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDGMh6vzHX4kP4V5kfU+wvMlsBqit8ge2tbO0P1+M1tmgAAAJBRQ56KUUOe
igAAAAtzc2gtZWQyNTUxOQAAACDGMh6vzHX4kP4V5kfU+wvMlsBqit8ge2tbO0P1+M1tmg
AAAEDt8h4U8V7X7aP2X8/9/8r3/7X+Q2/Q2/Q2/Q2/Q2/Q28YyHq/MdfiQ/hXmR9T7C8yW
wGqK3yB7a1s7Q/X4zW2aAAAAA2F1ZGl0LWtleQ==
-----END OPENSSH PRIVATE KEY-----
"""

@pytest.fixture(scope="session")
def ssh_key_file():
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as f:
        f.write(PRIVATE_KEY)
    os.chmod(path, 0o600)
    yield path
    os.remove(path)

def test_ssh_scan_xml():
    """Verify the nmap scan XML file exists and contains relevant algorithm details."""
    xml_path = "/home/user/ssh_scan.xml"
    assert os.path.exists(xml_path), f"Nmap scan output {xml_path} does not exist."
    assert os.path.isfile(xml_path), f"{xml_path} is not a file."

    with open(xml_path, 'r') as f:
        content = f.read()

    assert "nmaprun" in content or "nmap" in content.lower(), "The file does not appear to be an nmap XML output."
    assert "curve25519-sha256@libssh.org" in content or "ssh2-enum-algos" in content, \
        "The nmap scan output does not seem to enumerate the required SSH algorithms."

def test_ssh_connection_success(ssh_key_file):
    """Verify SSH connection succeeds with the provided private key."""
    cmd = [
        "ssh", "-i", ssh_key_file,
        "-p", "2222",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "BatchMode=yes",
        "user@127.0.0.1",
        "echo success"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"SSH connection failed. Output: {result.stderr}"
    assert "success" in result.stdout

def test_ssh_password_auth_rejected():
    """Verify that password authentication is disabled/rejected."""
    cmd = [
        "ssh", "-p", "2222",
        "-o", "PreferredAuthentications=password",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "BatchMode=yes",
        "user@127.0.0.1",
        "echo failure"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode != 0, "SSH connection succeeded with password authentication, but it should be disabled."
    assert "Permission denied" in result.stderr or "Connection closed" in result.stderr

def test_ssh_weak_cipher_rejected(ssh_key_file):
    """Verify that a weak cipher (e.g., aes128-cbc) is rejected."""
    cmd = [
        "ssh", "-i", ssh_key_file,
        "-p", "2222",
        "-c", "aes128-cbc",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "BatchMode=yes",
        "user@127.0.0.1",
        "echo failure"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode != 0, "SSH connection succeeded with weak cipher 'aes128-cbc', but it should be rejected."
    assert "no matching cipher found" in result.stderr.lower() or "cipher" in result.stderr.lower()

def test_http_audit_service():
    """Verify the HTTP service decodes the payload and appends to the audit trail."""
    plaintext = "TEST_AUDIT_EVENT_123"
    xored = bytes([ord(c) ^ 0x5A for c in plaintext])
    payload = base64.b64encode(xored)

    url = "http://127.0.0.1:8080/ingest"
    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP audit service at {url}: {e}")

    # Wait briefly to ensure file write is complete
    time.sleep(0.5)

    log_path = "/home/user/audit_trail.log"
    assert os.path.exists(log_path), f"Audit trail log {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    assert plaintext in content, f"The expected plaintext '{plaintext}' was not found in {log_path}."