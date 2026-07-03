# test_final_state.py
import os
import json
import pytest

def test_audit_report_exists():
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"Audit report not found at {report_path}"
    assert os.path.isfile(report_path), f"Path {report_path} is not a file"

def test_audit_report_content():
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {report_path} as JSON: {e}")

    expected_keys = [
        "jwt_alg_none_vulnerable",
        "cookie_secure_flag_missing",
        "cookie_httponly_flag_missing",
        "ssh_root_login_permitted",
        "ssh_password_auth_permitted"
    ]

    for key in expected_keys:
        assert key in data, f"Missing expected key '{key}' in audit report"
        assert data[key] is True, f"Expected key '{key}' to be true, but got {data[key]}"