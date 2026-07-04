# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import pytest

def b64url_decode(s):
    s += '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s.replace('-', '+').replace('_', '/'))

def verify_jwt(token, expected_user):
    parts = token.split('.')
    assert len(parts) == 3, f"JWT must have 3 parts, got {len(parts)}"
    header_b64, payload_b64, sig_b64 = parts

    try:
        header = json.loads(b64url_decode(header_b64))
    except Exception as e:
        pytest.fail(f"Failed to decode JWT header: {e}")

    assert header.get("alg") == "HS256", f"Expected alg HS256, got {header.get('alg')}"
    assert header.get("typ") == "JWT", f"Expected typ JWT, got {header.get('typ')}"

    try:
        payload = json.loads(b64url_decode(payload_b64))
    except Exception as e:
        pytest.fail(f"Failed to decode JWT payload: {e}")

    assert payload.get("user") == expected_user, f"Expected user {expected_user}, got {payload.get('user')}"
    assert payload.get("role") == "admin", f"Expected role admin, got {payload.get('role')}"
    assert payload.get("exp") == 1893456000, f"Expected exp 1893456000, got {payload.get('exp')}"

    msg = f"{header_b64}.{payload_b64}".encode('ascii')
    secret = b"SuperSecretRotationKey2024!"
    expected_sig = hmac.new(secret, msg, hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode('ascii').rstrip('=')

    assert sig_b64 == expected_sig_b64, "JWT signature is invalid or does not match the expected secret"

def test_summary_log():
    summary_path = "/home/user/rotation_summary.txt"
    assert os.path.isfile(summary_path), f"Summary log {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        content = f.read().strip()

    expected_content = "Successfully processed: 2 payloads"
    assert content == expected_content, f"Summary log content mismatch. Expected '{expected_content}', got '{content}'"

def test_output_payload_001():
    payload_path = "/home/user/payloads/output/payload_001.json"
    assert os.path.isfile(payload_path), f"Output payload {payload_path} does not exist."

    with open(payload_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {payload_path} is not valid JSON.")

    assert "id" in data, f"Output {payload_path} missing 'id' key."
    assert "data_b64" in data, f"Output {payload_path} missing 'data_b64' key."
    assert data["id"] == "payload_001", "ID mismatch in payload_001.json"

    try:
        inner_json_str = base64.b64decode(data["data_b64"]).decode('utf-8')
        inner_data = json.loads(inner_json_str)
    except Exception as e:
        pytest.fail(f"Failed to decode and parse inner JSON from data_b64: {e}")

    assert inner_data.get("ssn") == "XXX-XX-XXXX", f"SSN not properly redacted. Got: {inner_data.get('ssn')}"
    assert "old_token" in inner_data, "Missing 'old_token' in inner JSON"

    verify_jwt(inner_data["old_token"], "Alice")

def test_output_payload_002():
    payload_path = "/home/user/payloads/output/payload_002.json"
    assert os.path.isfile(payload_path), f"Output payload {payload_path} does not exist."

    with open(payload_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {payload_path} is not valid JSON.")

    assert "id" in data, f"Output {payload_path} missing 'id' key."
    assert "data_b64" in data, f"Output {payload_path} missing 'data_b64' key."
    assert data["id"] == "payload_002", "ID mismatch in payload_002.json"

    try:
        inner_json_str = base64.b64decode(data["data_b64"]).decode('utf-8')
        inner_data = json.loads(inner_json_str)
    except Exception as e:
        pytest.fail(f"Failed to decode and parse inner JSON from data_b64: {e}")

    assert inner_data.get("ssn") == "XXX-XX-XXXX", f"SSN not properly redacted. Got: {inner_data.get('ssn')}"
    assert "old_token" in inner_data, "Missing 'old_token' in inner JSON"

    verify_jwt(inner_data["old_token"], "Bob")