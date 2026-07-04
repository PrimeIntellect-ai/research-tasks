# test_final_state.py
import os
import subprocess
import requests
import pytest
import hashlib

def test_hash_file():
    hash_file_path = "/home/user/old_hash.txt"
    assert os.path.isfile(hash_file_path), f"Missing hash file: {hash_file_path}"

    with open(hash_file_path, "r") as f:
        actual_hash = f.read().strip()

    expected_text = "RELIANT_DEFENSE_99"
    expected_hash = hashlib.sha256(expected_text.encode("utf-8")).hexdigest()

    assert actual_hash == expected_hash, f"Hash mismatch. Expected {expected_hash}, got {actual_hash}"

def test_http_service():
    url = "http://127.0.0.1:8080/"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP GET request to {url} failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    csp_header = response.headers.get("Content-Security-Policy", "")
    assert "default-src 'none'" in csp_header, f"Missing or incorrect Content-Security-Policy header. Got: {csp_header}"

    assert response.text.strip() == "Secure System", f"Incorrect response body. Got: {response.text}"

def test_ssh_service():
    key_path = "/home/user/admin_key"
    assert os.path.isfile(key_path), f"Missing SSH private key: {key_path}"

    # Ensure correct permissions on the key for SSH to accept it
    os.chmod(key_path, 0o600)

    ssh_command = [
        "ssh",
        "-i", key_path,
        "-p", "2222",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "BatchMode=yes",
        "user@127.0.0.1",
        "echo 'SSH_SUCCESS'"
    ]

    try:
        result = subprocess.run(
            ssh_command,
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("SSH connection timed out.")

    assert result.returncode == 0, f"SSH connection failed. stderr: {result.stderr}"
    assert "SSH_SUCCESS" in result.stdout, f"Expected 'SSH_SUCCESS' in output, got: {result.stdout}"

def test_files_exist():
    required_files = [
        "/home/user/host_key",
        "/home/user/sshd_config",
        "/home/user/httpd.sh"
    ]
    for filepath in required_files:
        assert os.path.isfile(filepath), f"Required file {filepath} is missing."