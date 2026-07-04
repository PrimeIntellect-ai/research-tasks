# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import pytest

def b64url_decode(s):
    """Helper to decode base64url strings."""
    # Add padding if necessary
    pad = '=' * (4 - (len(s) % 4))
    return base64.urlsafe_b64decode(s + pad)

def test_pin_file():
    """Verify that the discovered PIN is correctly saved."""
    pin_file = "/home/user/pin.txt"
    assert os.path.exists(pin_file), f"File {pin_file} does not exist."

    with open(pin_file, "r") as f:
        pin = f.read().strip()

    assert pin == "6194", f"Expected PIN '6194', but found '{pin}'."

def test_forged_token():
    """Verify that the forged JWT is correctly generated and signed."""
    token_file = "/home/user/forged_token.txt"
    assert os.path.exists(token_file), f"File {token_file} does not exist."

    with open(token_file, "r") as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) == 3, "The forged token does not appear to be a valid JWT (must have 3 parts separated by dots)."

    header_b64, payload_b64, signature_b64 = parts

    # Verify signature
    secret = "6194"
    message = f"{header_b64}.{payload_b64}".encode('utf-8')
    expected_sig = hmac.new(secret.encode('utf-8'), message, hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode('utf-8').rstrip('=')

    assert hmac.compare_digest(signature_b64, expected_sig_b64), "JWT signature verification failed. The token was not signed correctly with the PIN."

    # Verify payload
    try:
        payload_bytes = b64url_decode(payload_b64)
        payload_data = json.loads(payload_bytes.decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Failed to decode or parse JWT payload: {e}")

    assert payload_data.get("user") == "attacker", f"Expected 'user' claim to be 'attacker', got '{payload_data.get('user')}'."
    assert payload_data.get("role") == "system_admin", f"Expected 'role' claim to be 'system_admin', got '{payload_data.get('role')}'."