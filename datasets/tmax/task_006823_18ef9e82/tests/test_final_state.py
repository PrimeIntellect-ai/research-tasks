# test_final_state.py

import os
import json
import base64
import pytest

def decode_base64url(data: str) -> bytes:
    """Decode base64url encoded string, adding padding if necessary."""
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def test_recovery_json_exists_and_valid():
    """Test that /home/user/recovery.json exists and is valid JSON."""
    path = "/home/user/recovery.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert isinstance(data, dict), f"JSON in {path} must be an object."
    assert "forged_token" in data, f"'forged_token' key missing in {path}."
    assert "target_user_pin" in data, f"'target_user_pin' key missing in {path}."

def test_target_user_pin():
    """Test that the target_user_pin is correctly cracked."""
    path = "/home/user/recovery.json"
    if not os.path.isfile(path):
        pytest.fail(f"File {path} does not exist.")

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert data.get("target_user_pin") == "7392", "The target_user_pin is incorrect."

def test_forged_token_structure():
    """Test that the forged_token meets the JWT format and bypass requirements."""
    path = "/home/user/recovery.json"
    if not os.path.isfile(path):
        pytest.fail(f"File {path} does not exist.")

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    token = data.get("forged_token", "")
    assert isinstance(token, str), "forged_token must be a string."

    parts = token.split(".")
    assert len(parts) == 3, "forged_token must consist of exactly three dot-separated parts."

    # Check header
    try:
        header_json = decode_base64url(parts[0])
        header = json.loads(header_json)
    except Exception as e:
        pytest.fail(f"Failed to decode or parse JWT header: {e}")

    alg = header.get("alg", "")
    assert str(alg).lower() == "none", "JWT header 'alg' must be 'none' (case-insensitive) to bypass signature verification."

    # Check claims
    try:
        claims_json = decode_base64url(parts[1])
        claims = json.loads(claims_json)
    except Exception as e:
        pytest.fail(f"Failed to decode or parse JWT claims: {e}")

    assert claims.get("user") == "admin", "JWT claims must have 'user' set to 'admin'."
    assert claims.get("role") == "forensics", "JWT claims must have 'role' set to 'forensics'."