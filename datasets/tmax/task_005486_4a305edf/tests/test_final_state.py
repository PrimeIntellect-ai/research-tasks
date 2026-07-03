# test_final_state.py

import os
import re
import socket
import pytest

PAYLOAD_FILE = "/home/user/payload.txt"

def test_payload_file_exists():
    """Verify that the payload file exists."""
    assert os.path.isfile(PAYLOAD_FILE), f"Verification failed: {PAYLOAD_FILE} does not exist."

def test_payload_constraints_and_resolution():
    """Verify the payload satisfies all IDS constraints and resolves correctly."""
    with open(PAYLOAD_FILE, "r") as f:
        payload = f.read().strip()

    # 1. Check for exact IP
    assert "192.168.1.100" not in payload, "Verification failed: Payload contains the literal IP '192.168.1.100'."

    # 2. Check for URL encoding
    assert "%" not in payload, "Verification failed: Payload contains '%' (URL encoding blocked)."

    # 3. Check for Hex characters
    assert "x" not in payload.lower(), "Verification failed: Payload contains 'x' or 'X' (Hex blocked)."

    # 4. Verify path includes /login
    assert "/login" in payload, "Verification failed: Payload does not contain the '/login' path."

    # Extract host portion (everything before the first '/')
    host = payload.split('/')[0]

    # 5. Check for alphabetical characters in the host to prevent standard domain names
    assert not re.search(r"[a-zA-Z]", host), f"Verification failed: Host portion '{host}' contains letters."

    # 6. Verify resolution maps to 192.168.1.100
    try:
        resolved_ip = socket.gethostbyname(host)
    except Exception as e:
        pytest.fail(f"Verification failed: Host '{host}' failed to resolve. Error: {e}")

    assert resolved_ip == "192.168.1.100", f"Verification failed: Host '{host}' resolves to '{resolved_ip}' instead of '192.168.1.100'."