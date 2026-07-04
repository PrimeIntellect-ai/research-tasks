# test_final_state.py

import requests
import hashlib
import urllib3

# Suppress insecure request warnings since we expect a self-signed cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://127.0.0.1:8443/analyze"
EXPECTED_COOKIE_VAL = "4fc8197dc364f3a093ed037d7a7ff20993f4e24eb2edaa0dd2da24255cf08b00"
VALID_ELF = b"\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00" + b"A" * 64
INVALID_ELF = b"DEADBEEF" + b"B" * 64

def test_missing_auth():
    """Test Request 1: Missing authentication with valid ELF."""
    try:
        response = requests.post(URL, data=VALID_ELF, verify=False, timeout=5)
        assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server at {URL}: {e}"

def test_valid_auth_invalid_elf():
    """Test Request 2: Valid auth, Invalid ELF."""
    cookies = {"session": EXPECTED_COOKIE_VAL}
    try:
        response = requests.post(URL, cookies=cookies, data=INVALID_ELF, verify=False, timeout=5)
        assert response.status_code == 400, f"Expected HTTP 400 for invalid ELF, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server at {URL}: {e}"

def test_valid_auth_valid_elf():
    """Test Request 3: Valid auth, Valid ELF."""
    cookies = {"session": EXPECTED_COOKIE_VAL}
    try:
        response = requests.post(URL, cookies=cookies, data=VALID_ELF, verify=False, timeout=5)
        assert response.status_code == 200, f"Expected HTTP 200 for valid auth and valid ELF, got {response.status_code}. Response: {response.text}"

        expected_hash = hashlib.sha256(VALID_ELF).hexdigest()
        actual_hash = response.text.strip()
        assert actual_hash == expected_hash, f"Expected response body to be SHA-256 hash '{expected_hash}', but got '{actual_hash}'"
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server at {URL}: {e}"