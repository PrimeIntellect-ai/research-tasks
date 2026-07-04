# test_final_state.py
import os
import json
import base64

def decode_base64url(s):
    s = s.replace('-', '+').replace('_', '/')
    return base64.b64decode(s + '=' * (-len(s) % 4))

def test_audit_forged_jwt():
    path = "/home/user/audit_forged_jwt.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) == 3, f"Forged JWT in {path} does not have exactly 3 parts (header.payload.signature)."

    header_b64, payload_b64, signature = parts

    try:
        header = json.loads(decode_base64url(header_b64))
    except Exception as e:
        assert False, f"Failed to decode JWT header: {e}"

    try:
        payload = json.loads(decode_base64url(payload_b64))
    except Exception as e:
        assert False, f"Failed to decode JWT payload: {e}"

    assert header.get("alg", "").lower() == "none", f"JWT header 'alg' must be 'none', got: {header.get('alg')}"
    assert payload.get("user") == "admin", f"JWT payload 'user' must be 'admin', got: {payload.get('user')}"
    assert payload.get("role") == "superuser", f"JWT payload 'role' must be 'superuser', got: {payload.get('role')}"
    assert signature == "", f"JWT signature must be empty for 'none' algorithm, got: {signature}"

def test_audit_report():
    path = "/home/user/audit_report.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_output = "CRITICAL: Access granted to superuser. Compliance violation detected!"
    assert content == expected_output, f"Output in {path} does not match expected output.\nExpected: {expected_output}\nGot: {content}"