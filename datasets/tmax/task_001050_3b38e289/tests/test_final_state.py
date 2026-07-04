# test_final_state.py

import os
import subprocess
import requests
import pytest

URL = "http://127.0.0.1:8080/"
COOKIE_NAME = "AuthToken"
COOKIE_VALUE = "DevSecOps_XYZ99"
AES_KEY_STR = "5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d"

def decrypt_aes_256_cbc(b64_data: str, key_str: str) -> bytes:
    """
    Decrypts base64 encoded AES-256-CBC data using openssl.
    The key_str is used as 32 ASCII bytes, so we convert it to hex for openssl.
    """
    key_hex = key_str.encode('utf-8').hex()
    iv_hex = "00" * 16

    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc",
        "-K", key_hex,
        "-iv", iv_hex,
        "-base64", "-A"
    ]

    res = subprocess.run(cmd, input=b64_data.encode('utf-8'), capture_output=True)
    if res.returncode != 0:
        raise ValueError(f"Decryption failed. OpenSSL error: {res.stderr.decode('utf-8', errors='ignore')}")
    return res.stdout

def test_middleware_source_exists():
    assert os.path.isfile("/home/user/middleware.cpp"), "Source file /home/user/middleware.cpp is missing"

def test_middleware_binary_exists():
    assert os.path.isfile("/home/user/middleware"), "Compiled binary /home/user/middleware is missing"

def test_http_403_on_missing_or_invalid_cookie():
    # Missing cookie
    try:
        resp = requests.post(URL, data="helloworld", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the middleware service: {e}")

    assert resp.status_code == 403, f"Expected 403 Forbidden for missing cookie, got {resp.status_code}"

    # Invalid cookie
    resp = requests.post(URL, data="helloworld", cookies={COOKIE_NAME: "WrongToken"}, timeout=5)
    assert resp.status_code == 403, f"Expected 403 Forbidden for invalid cookie, got {resp.status_code}"

def test_http_200_and_encryption_on_valid_request():
    payload = "The new server for TITAN_PROJECT is deployed."
    expected_redacted = b"The new server for [REDACTED] is deployed."

    resp = requests.post(
        URL, 
        data=payload, 
        cookies={COOKIE_NAME: COOKIE_VALUE}, 
        timeout=5
    )

    assert resp.status_code == 200, f"Expected 200 OK for valid request, got {resp.status_code}"

    b64_response = resp.text.strip()
    assert b64_response, "Response body is empty, expected base64 encoded encrypted data"

    try:
        decrypted_bytes = decrypt_aes_256_cbc(b64_response, AES_KEY_STR)
    except Exception as e:
        pytest.fail(f"Could not decrypt the response: {e}")

    assert decrypted_bytes == expected_redacted, (
        f"Decrypted payload does not match expected redacted text.\n"
        f"Expected: {expected_redacted}\n"
        f"Got: {decrypted_bytes}"
    )

def test_http_200_multiple_redactions():
    payload = "TITAN_PROJECT and TITAN_PROJECT"
    expected_redacted = b"[REDACTED] and [REDACTED]"

    resp = requests.post(
        URL, 
        data=payload, 
        cookies={COOKIE_NAME: COOKIE_VALUE}, 
        timeout=5
    )

    assert resp.status_code == 200, f"Expected 200 OK for valid request, got {resp.status_code}"

    b64_response = resp.text.strip()

    try:
        decrypted_bytes = decrypt_aes_256_cbc(b64_response, AES_KEY_STR)
    except Exception as e:
        pytest.fail(f"Could not decrypt the response: {e}")

    assert decrypted_bytes == expected_redacted, (
        f"Decrypted payload does not match expected redacted text for multiple occurrences.\n"
        f"Expected: {expected_redacted}\n"
        f"Got: {decrypted_bytes}"
    )