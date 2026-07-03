# test_final_state.py

import os
import subprocess
import requests
import pytest

LAB_DIR = "/home/user/forensics_lab"
EVIDENCE_ENC = os.path.join(LAB_DIR, "evidence.enc")
PROXY_URL = "http://127.0.0.1:8000/evidence"

def get_expected_plaintext():
    """Derive the expected plaintext by decrypting the evidence file."""
    assert os.path.isfile(EVIDENCE_ENC), f"Encrypted evidence file missing: {EVIDENCE_ENC}"

    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-k", "f0r3ns1cs!", "-in", EVIDENCE_ENC
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to decrypt evidence file to determine expected truth. Error: {e.stderr}")

def test_pipeline_end_to_end():
    expected_text = get_expected_plaintext()

    headers = {
        "X-Forensics": "true"
    }
    cookies = {
        "Auth-Token": "admin_access"
    }

    try:
        response = requests.get(PROXY_URL, headers=headers, cookies=cookies, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the firewall proxy at {PROXY_URL}. Are the services running?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {PROXY_URL} timed out.")

    assert response.status_code == 200, (
        f"Expected HTTP 200 OK, got {response.status_code}. "
        f"Response body: {response.text[:200]}"
    )

    actual_text = response.text.strip()
    assert actual_text == expected_text, (
        f"Decrypted evidence mismatch. Expected: {expected_text}, Got: {actual_text}"
    )