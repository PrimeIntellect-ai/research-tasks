# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import pytest

REPORT_PATH = "/home/user/audit_report.json"
SCRIPT_PATH = "/home/user/policy_checker.py"
EXPECTED_SECRET = "Sup3rS3cr3t_DevSecOps_K3y_2024!"

def b64_decode(data: str) -> bytes:
    """Helper to decode base64url without padding."""
    padded = data + '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(padded)

def verify_jwt(token: str, secret: str) -> dict:
    """Verify and decode a JWT using only the standard library."""
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("JWT does not have 3 parts separated by dots.")

    header_b64, payload_b64, signature_b64 = parts

    # Verify signature
    msg = f"{header_b64}.{payload_b64}".encode('utf-8')
    expected_sig = base64.urlsafe_b64encode(
        hmac.new(secret.encode('utf-8'), msg, hashlib.sha256).digest()
    ).decode('utf-8').rstrip('=')

    if not hmac.compare_digest(expected_sig, signature_b64):
        raise ValueError("JWT signature verification failed.")

    header = json.loads(b64_decode(header_b64))
    if header.get("alg") != "HS256":
        raise ValueError(f"Expected HS256 algorithm, got {header.get('alg')}")

    payload = json.loads(b64_decode(payload_b64))
    return payload

def test_policy_checker_script_exists():
    """Verify the student created the policy checker script."""
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} was not found."

def test_audit_report_exists():
    """Verify the audit report JSON file was generated."""
    assert os.path.isfile(REPORT_PATH), f"The report {REPORT_PATH} was not generated."

def test_audit_report_contents():
    """Verify the contents of the audit report."""
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

    # Check basic fields
    assert "extracted_secret" in report, "Missing 'extracted_secret' in audit report."
    assert report["extracted_secret"] == EXPECTED_SECRET, "The extracted secret is incorrect."

    assert "cwe_identified" in report, "Missing 'cwe_identified' in audit report."
    assert report["cwe_identified"] == "CWE-798", "The identified CWE is incorrect."

    assert "privilege_escalation_risk_found" in report, "Missing 'privilege_escalation_risk_found' in audit report."
    assert report["privilege_escalation_risk_found"] is True, "The privilege escalation risk should be True based on config.json."

    assert "forged_admin_jwt" in report, "Missing 'forged_admin_jwt' in audit report."

    # Verify the JWT
    token = report["forged_admin_jwt"]
    try:
        payload = verify_jwt(token, EXPECTED_SECRET)
    except Exception as e:
        pytest.fail(f"Failed to verify the forged JWT: {e}")

    assert payload.get("username") == "admin", f"JWT payload username is not 'admin'. Got: {payload.get('username')}"
    assert payload.get("role") == "superuser", f"JWT payload role is not 'superuser'. Got: {payload.get('role')}"