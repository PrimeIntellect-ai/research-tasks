# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import pytest

def decode_b64url(s):
    """Helper to decode base64url strings."""
    return base64.urlsafe_b64decode(s + '=' * (-len(s) % 4))

def verify_and_decode_jwt(token, secret):
    """Verify the JWT signature and return header and payload."""
    parts = token.split('.')
    assert len(parts) == 3, f"JWT must have 3 parts, got {len(parts)}"

    header_b64, payload_b64, signature_b64 = parts

    # Verify signature
    msg = f"{header_b64}.{payload_b64}".encode('utf-8')
    expected_sig = hmac.new(secret.encode('utf-8'), msg, hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).rstrip(b'=').decode('utf-8')

    assert signature_b64 == expected_sig_b64, "JWT signature is invalid."

    header = json.loads(decode_b64url(header_b64))
    payload = json.loads(decode_b64url(payload_b64))

    return header, payload

def test_rotated_tokens_file_exists():
    """Ensure the rotated_tokens.json file was created."""
    assert os.path.isfile('/home/user/rotated_tokens.json'), "The file /home/user/rotated_tokens.json is missing."

def test_rotated_tokens_content():
    """Ensure the rotated_tokens.json contains correct users and valid JWTs."""
    with open('/home/user/rotated_tokens.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/rotated_tokens.json is not valid JSON.")

    # Expected users based on the "alg": "none" vulnerability in the log file
    expected_users = {"bob", "diana"}
    actual_users = set(data.keys())

    assert actual_users == expected_users, f"Expected users {expected_users}, but got {actual_users}."

    secret = "SuperSecretKey2023"

    for user in expected_users:
        token = data[user]
        header, payload = verify_and_decode_jwt(token, secret)

        # Check header
        assert header.get("alg") == "HS256", f"Expected alg 'HS256' for user {user}, got {header.get('alg')}"
        assert header.get("typ") == "JWT", f"Expected typ 'JWT' for user {user}, got {header.get('typ')}"

        # Check payload
        assert payload.get("sub") == user, f"Expected sub '{user}' for user {user}, got {payload.get('sub')}"
        assert payload.get("iat") == 1700000000, f"Expected iat 1700000000 for user {user}, got {payload.get('iat')}"
        assert isinstance(payload.get("iat"), int), f"Expected iat to be an integer for user {user}."