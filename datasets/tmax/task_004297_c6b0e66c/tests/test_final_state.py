# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import pytest

REPORT_PATH = "/home/user/report.json"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file not found at {REPORT_PATH}. Did the script execute and create the file?"

def test_report_json_structure_and_values():
    assert os.path.isfile(REPORT_PATH), "Report file missing."
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    # Check issuer_cn
    assert "issuer_cn" in data, "Missing 'issuer_cn' key in the report JSON."
    assert data["issuer_cn"] == "DevSecOpsLocal", f"Expected 'issuer_cn' to be 'DevSecOpsLocal', got {data['issuer_cn']}"

    # Check status_code
    assert "status_code" in data, "Missing 'status_code' key in the report JSON."
    assert data["status_code"] == 200, f"Expected 'status_code' to be 200, got {data['status_code']}"

    # Check policy_violations
    assert "policy_violations" in data, "Missing 'policy_violations' key in the report JSON."
    violations = data["policy_violations"]
    assert isinstance(violations, list), "'policy_violations' must be a JSON array (list)."
    expected_violations = {"Strict-Transport-Security", "Content-Security-Policy"}
    assert set(violations) == expected_violations, f"Expected policy violations {expected_violations}, got {set(violations)}"
    assert len(violations) == 2, "Expected exactly 2 policy violations."

def test_jwt_validity_and_payload():
    assert os.path.isfile(REPORT_PATH), "Report file missing."
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Cannot parse JSON to check JWT.")

    assert "jwt_generated" in data, "Missing 'jwt_generated' key in the report JSON."
    token = data["jwt_generated"]

    parts = token.split('.')
    assert len(parts) == 3, "The 'jwt_generated' value is not a valid JWT string (does not have 3 dot-separated parts)."

    header_b64, payload_b64, sig_b64 = parts

    # Verify HMAC SHA256 signature natively
    secret = "devsecops_secret_2024"
    msg = f"{header_b64}.{payload_b64}".encode('utf-8')
    expected_sig = hmac.new(secret.encode('utf-8'), msg, hashlib.sha256).digest()
    expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode('utf-8').rstrip('=')

    assert sig_b64 == expected_sig_b64, "JWT signature verification failed. Ensure it is signed with the correct secret ('devsecops_secret_2024') and algorithm (HS256)."

    # Decode and verify payload
    payload_padded = payload_b64 + '=' * (-len(payload_b64) % 4)
    try:
        payload_bytes = base64.urlsafe_b64decode(payload_padded)
        payload = json.loads(payload_bytes)
    except Exception as e:
        pytest.fail(f"Failed to decode JWT payload: {e}")

    expected_payload = {"sub": "policy_scanner", "role": "auditor"}

    for k, v in expected_payload.items():
        assert payload.get(k) == v, f"JWT payload missing or incorrect for key '{k}'. Expected '{v}', got '{payload.get(k)}'"