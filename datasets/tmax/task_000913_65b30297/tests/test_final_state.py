# test_final_state.py
import os
import json
import hashlib
import datetime
import requests
import pytest

URL = "http://127.0.0.1:8443/upload"
SAFE_UPLOADS_DIR = "/home/user/safe_uploads"
LOG_FILE = "/home/user/firewall_access.log"
XOR_KEY = b"NETSEC2024"
SALT = "S@lt123"

def get_valid_auth_token():
    date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    return hashlib.md5((date_str + SALT).encode()).hexdigest()

def xor_encrypt_decrypt(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def read_logs():
    if not os.path.exists(LOG_FILE):
        return []
    logs = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return logs

def test_valid_upload():
    filename = "test_valid_report.txt"
    plaintext = b"This is a secret report."
    ciphertext = xor_encrypt_decrypt(plaintext, XOR_KEY)

    headers = {
        "X-Custom-Auth": get_valid_auth_token(),
        "X-File-Name": filename
    }

    try:
        response = requests.post(URL, headers=headers, data=ciphertext, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid upload, got {response.status_code}"

    saved_file_path = os.path.join(SAFE_UPLOADS_DIR, filename)
    assert os.path.exists(saved_file_path), f"File was not saved to {saved_file_path}"

    with open(saved_file_path, 'rb') as f:
        saved_content = f.read()

    assert saved_content == plaintext, "Saved file content does not match the decrypted payload."

    logs = read_logs()
    matching_logs = [l for l in logs if l.get("filename") == filename and l.get("status") == "ACCEPTED"]
    assert len(matching_logs) > 0, "Expected an ACCEPTED log entry for the valid upload."

def test_invalid_auth():
    filename = "test_invalid_auth.txt"
    plaintext = b"Data"
    ciphertext = xor_encrypt_decrypt(plaintext, XOR_KEY)

    headers = {
        "X-Custom-Auth": "invalid_token123",
        "X-File-Name": filename
    }

    try:
        response = requests.post(URL, headers=headers, data=ciphertext, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code in (401, 403), f"Expected HTTP 401 or 403 for invalid auth, got {response.status_code}"

    logs = read_logs()
    matching_logs = [l for l in logs if l.get("filename") == filename and l.get("status") == "REJECTED"]
    assert len(matching_logs) > 0, "Expected a REJECTED log entry for invalid auth."

def test_path_traversal():
    filename = "../test_traversal.txt"
    plaintext = b"Data"
    ciphertext = xor_encrypt_decrypt(plaintext, XOR_KEY)

    headers = {
        "X-Custom-Auth": get_valid_auth_token(),
        "X-File-Name": filename
    }

    try:
        response = requests.post(URL, headers=headers, data=ciphertext, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert response.status_code in (400, 403), f"Expected HTTP 400 or 403 for path traversal, got {response.status_code}"

    logs = read_logs()
    matching_logs = [l for l in logs if l.get("filename") == filename and l.get("status") == "REJECTED"]
    assert len(matching_logs) > 0, "Expected a REJECTED log entry for path traversal."