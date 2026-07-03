# test_final_state.py

import os
import json
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/generate_audit.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_audit_report_exists():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Report {report_path} does not exist."

def test_audit_report_content():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Report {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "certificate_valid" in report, "Key 'certificate_valid' missing from JSON."
    assert report["certificate_valid"] is True, "certificate_valid should be true."

    assert "server_cert_subject" in report, "Key 'server_cert_subject' missing from JSON."
    expected_subject = "CN = secure.internal.corp"
    actual_subject = report["server_cert_subject"].strip()
    if actual_subject.startswith("subject="):
        actual_subject = actual_subject[len("subject="):].strip()
    assert actual_subject == expected_subject, f"Expected subject '{expected_subject}', got '{report['server_cert_subject']}'"

    assert "threat_ips" in report, "Key 'threat_ips' missing from JSON."
    expected_ips = ["192.168.1.100", "192.168.1.50"]
    actual_ips = report["threat_ips"]
    assert isinstance(actual_ips, list), "threat_ips should be a list."
    assert sorted(actual_ips) == sorted(expected_ips), f"Expected threat_ips {expected_ips}, got {actual_ips}"

    # Check if sorted in ascending order as requested
    assert actual_ips == sorted(actual_ips), "threat_ips are not sorted in ascending order."