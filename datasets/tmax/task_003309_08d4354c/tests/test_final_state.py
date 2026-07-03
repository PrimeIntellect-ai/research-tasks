# test_final_state.py

import os
import json

def test_audit_report_exists():
    """Verify that the audit report file was created at the exact required path."""
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Audit report file not found at {report_path}"

def test_audit_report_valid_json():
    """Verify that the audit report is valid JSON."""
    report_path = "/home/user/audit_report.json"
    with open(report_path, "r") as f:
        try:
            json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Audit report is not valid JSON: {e}"

def test_audit_report_contents():
    """Verify that the audit report contains the correct extracted and decrypted data."""
    report_path = "/home/user/audit_report.json"
    with open(report_path, "r") as f:
        data = json.load(f)

    # Check for required keys
    assert "cert_cn" in data, "The key 'cert_cn' is missing from the JSON output."
    assert "decrypted_cookie" in data, "The key 'decrypted_cookie' is missing from the JSON output."

    # Verify the extracted Common Name
    expected_cn = "legacy.vulnerable.local"
    actual_cn = data.get("cert_cn")
    assert actual_cn == expected_cn, f"Expected cert_cn to be '{expected_cn}', but got '{actual_cn}'."

    # Verify the decrypted cookie payload
    expected_cookie = "user:auditor|role:admin|valid:true"
    actual_cookie = data.get("decrypted_cookie")
    assert actual_cookie == expected_cookie, f"Expected decrypted_cookie to be '{expected_cookie}', but got '{actual_cookie}'."