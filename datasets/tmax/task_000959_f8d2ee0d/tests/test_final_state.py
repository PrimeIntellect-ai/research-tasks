# test_final_state.py
import os
import json
import pytest

def test_auditor_script_exists():
    filepath = '/home/user/auditor.py'
    assert os.path.isfile(filepath), f"The script {filepath} does not exist."

def test_audit_report_exists():
    filepath = '/home/user/audit_report.json'
    assert os.path.isfile(filepath), f"The report {filepath} does not exist."

def test_audit_report_content():
    filepath = '/home/user/audit_report.json'
    assert os.path.isfile(filepath), f"The report {filepath} does not exist."

    with open(filepath, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {filepath} does not contain valid JSON.")

    expected_keys = {"world_writable", "checksum_match", "cert_expired", "open_redirect_param"}
    assert set(report.keys()) == expected_keys, f"The JSON report keys do not match the expected keys. Found: {list(report.keys())}"

    assert report["world_writable"] is True, "Expected 'world_writable' to be true."
    assert report["checksum_match"] is False, "Expected 'checksum_match' to be false."
    assert report["cert_expired"] is True, "Expected 'cert_expired' to be true."
    assert report["open_redirect_param"] == "return_to_path", "Expected 'open_redirect_param' to be 'return_to_path'."