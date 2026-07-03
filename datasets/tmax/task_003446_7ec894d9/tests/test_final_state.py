# test_final_state.py

import os
import subprocess
import tempfile
import hashlib
import base64
import requests
import pytest

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    pytest.fail("cryptography package is not installed. It is required for AES-GCM.")

def test_ssh_access_pubkey_only():
    """Test SSH access on port 2222 using the auditor's key, and verify password auth is disabled."""
    # Test successful public key authentication
    cmd_success = [
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "PasswordAuthentication=no",
        "-o", "BatchMode=yes",
        "-i", "/app/auditor_id_rsa",
        "-p", "2222", "user@127.0.0.1", "echo", "success"
    ]
    res_success = subprocess.run(cmd_success, capture_output=True, text=True)
    assert res_success.returncode == 0, f"SSH public key authentication failed. stderr: {res_success.stderr}"
    assert "success" in res_success.stdout, "SSH command did not execute successfully."

    # Test that password authentication fails
    cmd_fail = [
        "ssh", "-o", "StrictHostKeyChecking=no",
        "-o", "PreferredAuthentications=password",
        "-o", "PubkeyAuthentication=no",
        "-o", "BatchMode=yes",
        "-p", "2222", "user@127.0.0.1", "echo", "success"
    ]
    res_fail = subprocess.run(cmd_fail, capture_output=True, text=True)
    assert res_fail.returncode != 0, "SSH password authentication should be disabled, but connection succeeded."

def test_http_audit_file_403_invalid_permissions():
    """Test that the HTTP service returns 403 for files without 0600 permissions."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"test data")
        temp_path = f.name

    try:
        # Set permissions to 0644
        os.chmod(temp_path, 0o644)

        try:
            resp = requests.post("http://127.0.0.1:8000/audit_file", json={"path": temp_path}, timeout=5)
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to HTTP service: {e}")

        assert resp.status_code == 403, f"Expected HTTP 403 for invalid permissions, got {resp.status_code}. Response: {resp.text}"

        try:
            json_data = resp.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {resp.text}")

        assert json_data.get("error") == "Invalid permissions", f"Expected error message 'Invalid permissions', got: {json_data}"
    finally:
        os.remove(temp_path)

def test_http_audit_file_200_valid_encryption():
    """Test that the HTTP service returns 200 and a correctly encrypted hash for 0600 files."""
    file_content = b"super secret auditor data"
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(file_content)
        temp_path = f.name

    try:
        # Set permissions to 0600 exactly
        os.chmod(temp_path, 0o600)

        # Compute the expected result
        expected_digest = hashlib.sha256(file_content).hexdigest().encode('utf-8')

        aes_key_path = "/app/aes_key.bin"
        assert os.path.exists(aes_key_path), f"AES key file missing at {aes_key_path}"
        with open(aes_key_path, "rb") as key_f:
            aes_key = key_f.read()

        aesgcm = AESGCM(aes_key)
        iv = b'\x00' * 12
        # AESGCM.encrypt automatically appends the 16-byte auth tag
        ciphertext = aesgcm.encrypt(iv, expected_digest, None)
        expected_b64 = base64.b64encode(ciphertext).decode('utf-8')

        try:
            resp = requests.post("http://127.0.0.1:8000/audit_file", json={"path": temp_path}, timeout=5)
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to HTTP service: {e}")

        assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}. Response: {resp.text}"

        try:
            json_data = resp.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {resp.text}")

        assert "encrypted_hash" in json_data, f"Response missing 'encrypted_hash' key: {json_data}"
        assert json_data["encrypted_hash"] == expected_b64, (
            f"Encrypted hash mismatch.\n"
            f"Expected: {expected_b64}\n"
            f"Got:      {json_data['encrypted_hash']}\n"
            f"(Check if SHA-256 is used, AES-GCM IV is all zeros, and tag is appended before base64)"
        )
    finally:
        os.remove(temp_path)