# test_final_state.py

import os
import json
import pytest
import re

REPORT_PATH = "/home/user/audit_report.json"
FIXED_APP_PATH = "/home/user/api/fixed_app.py"

def test_audit_report_exists_and_valid_json():
    """Test that the audit_report.json exists and is valid JSON."""
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} is missing."

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    assert isinstance(data, dict), "The JSON root should be a dictionary."

def test_audit_report_cwe_id():
    """Test that the correct CWE ID is identified."""
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    cwe_id = data.get("cwe_id", "").upper()
    valid_cwes = ["CWE-347", "CWE-287", "CWE-327"]
    assert cwe_id in valid_cwes, f"Expected cwe_id to be one of {valid_cwes}, but got '{cwe_id}'."

def test_audit_report_admin_secret():
    """Test that the admin secret was successfully extracted."""
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    secret = data.get("admin_secret")
    expected_secret = "FLAG_SECURE_JWT_DATA_9921"
    assert secret == expected_secret, f"Expected admin_secret to be '{expected_secret}', but got '{secret}'."

def test_audit_report_malicious_ips():
    """Test that the correct malicious IPs were identified."""
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    ips = data.get("malicious_ips")
    assert isinstance(ips, list), "malicious_ips should be a list of strings."

    expected_ips = ["10.0.0.5", "172.16.0.4"]
    assert sorted(ips) == sorted(expected_ips), f"Expected malicious_ips to be {expected_ips}, but got {ips}."

def test_fixed_app_exists_and_patched():
    """Test that the fixed_app.py was created and does not contain the vulnerability."""
    assert os.path.isfile(FIXED_APP_PATH), f"Patched application file {FIXED_APP_PATH} is missing."

    with open(FIXED_APP_PATH, 'r') as f:
        content = f.read()

    # A simple static check to ensure the 'none' algorithm bypass is removed.
    # The original had `if alg == 'none':`
    vulnerable_pattern = re.compile(r"alg\s*==\s*['\"]none['\"]", re.IGNORECASE)
    assert not vulnerable_pattern.search(content), "The fixed_app.py still appears to contain the 'none' algorithm vulnerability."

    # Ensure it at least mentions HS256 explicitly as required
    assert "hs256" in content.lower(), "The fixed_app.py must explicitly enforce the HS256 algorithm."