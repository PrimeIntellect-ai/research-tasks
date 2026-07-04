# test_final_state.py

import os
import pytest
import requests
import urllib3

# Suppress insecure request warnings since we expect a self-signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://127.0.0.1:8443/exfil"
AUTH_TOKEN = "OpDagger_2024"
RC4_KEY = b"deadbeefcafebabe"

def rc4_encrypt(key: bytes, data: bytes) -> bytes:
    """Simple RC4 implementation to generate encrypted payloads."""
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    out = bytearray()
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

def test_tls_certificates_exist():
    """Verify that the TLS certificates were generated in the correct location."""
    crt_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"

    assert os.path.exists(crt_path), f"Certificate file missing at {crt_path}"
    assert os.path.exists(key_path), f"Private key file missing at {key_path}"

def test_missing_auth_returns_401():
    """Verify that a request without the X-Auth-Token header returns HTTP 401."""
    try:
        response = requests.post(URL, data=b"dummy", verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to honeypot: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}"

def test_invalid_auth_returns_401():
    """Verify that a request with an incorrect X-Auth-Token header returns HTTP 401."""
    headers = {"X-Auth-Token": "BadToken123"}
    try:
        response = requests.post(URL, headers=headers, data=b"dummy", verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to honeypot: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid auth, got {response.status_code}"

def test_valid_auth_decryption_and_redaction():
    """Verify that a valid request is decrypted, redacted, and acknowledged properly."""
    plaintext = b"User: admin, CC: 1111222233334444, Role: root"
    encrypted_payload = rc4_encrypt(RC4_KEY, plaintext)

    headers = {"X-Auth-Token": AUTH_TOKEN}

    try:
        response = requests.post(URL, headers=headers, data=encrypted_payload, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to honeypot: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid auth, got {response.status_code}"

    expected_redacted_string = "User: admin, CC: [REDACTED_CC], Role: root"
    expected_length = len(expected_redacted_string.encode('utf-8'))
    expected_body = f"ACK: {expected_length}"

    assert response.text == expected_body, f"Expected response body '{expected_body}', got '{response.text}'"

def test_exfil_log_contents():
    """Verify that the decrypted and redacted string is properly logged."""
    log_path = "/home/user/exfil_log.txt"
    assert os.path.exists(log_path), f"Log file missing at {log_path}"

    with open(log_path, "r", encoding="utf-8") as f:
        log_contents = f.read()

    expected_log_entry = "User: admin, CC: [REDACTED_CC], Role: root\n"
    assert expected_log_entry in log_contents, "The expected redacted log entry was not found in the log file."