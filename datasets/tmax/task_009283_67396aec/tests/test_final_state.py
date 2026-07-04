# test_final_state.py

import os
import json
import stat
import pytest

def test_audit_report():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Audit report missing at {report_path}"

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Audit report at {report_path} is not valid JSON")

    expected_cwes = [78, 798]
    assert "vulnerable_script_cwes" in report_data, "Missing 'vulnerable_script_cwes' in audit report"
    assert report_data["vulnerable_script_cwes"] == expected_cwes, f"Expected CWEs {expected_cwes}, got {report_data['vulnerable_script_cwes']}"

    expected_ip = "198.51.100.55"
    assert "suspicious_ip" in report_data, "Missing 'suspicious_ip' in audit report"
    assert report_data["suspicious_ip"] == expected_ip, f"Expected IP {expected_ip}, got {report_data['suspicious_ip']}"

    expected_suid = "/home/user/bin/backup_creds"
    assert "suid_binary" in report_data, "Missing 'suid_binary' in audit report"
    assert report_data["suid_binary"] == expected_suid, f"Expected SUID binary {expected_suid}, got {report_data['suid_binary']}"

def test_new_secrets_json():
    secrets_path = "/home/user/app/new_secrets.json"
    assert os.path.isfile(secrets_path), f"New secrets file missing at {secrets_path}"

    with open(secrets_path, "r") as f:
        try:
            secrets_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Secrets file at {secrets_path} is not valid JSON")

    assert "db_password" in secrets_data, "Missing 'db_password' key in new secrets file"
    password = secrets_data["db_password"]

    assert isinstance(password, str), "Password is not a string"
    assert len(password) == 16, f"Expected password length 16, got {len(password)}"
    assert password.isalnum(), "Password is not alphanumeric"

def test_new_secrets_permissions():
    secrets_path = "/home/user/app/new_secrets.json"
    assert os.path.isfile(secrets_path), f"New secrets file missing at {secrets_path}"

    st = os.stat(secrets_path)
    permissions = stat.S_IMODE(st.st_mode)

    assert permissions == 0o600, f"Expected permissions 0600, got {oct(permissions)}"