# test_final_state.py

import os
import json
import pytest

def test_audit_report_exists():
    """Test that the audit report JSON file was generated."""
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"The expected output file {report_path} does not exist."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

def test_audit_report_content():
    """Test that the audit report contains the correct IOCs and malicious IPs."""
    report_path = "/home/user/audit_report.json"

    try:
        with open(report_path, "r") as f:
            report_data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {report_path} does not contain valid JSON.")

    # Check top-level keys
    assert "extracted_iocs" in report_data, "The JSON is missing the 'extracted_iocs' key."
    assert "malicious_ips" in report_data, "The JSON is missing the 'malicious_ips' key."

    # Verify extracted IOCs
    iocs = report_data["extracted_iocs"]
    assert "user_agent" in iocs, "The 'extracted_iocs' object is missing the 'user_agent' key."
    assert "cookie" in iocs, "The 'extracted_iocs' object is missing the 'cookie' key."

    expected_user_agent = "X-Compliance-Bot/v2.4.1-alpha"
    expected_cookie = "auth_token_v2=xyz_9988776655_abc"

    assert iocs["user_agent"] == expected_user_agent, f"Expected user_agent '{expected_user_agent}', but got '{iocs['user_agent']}'."
    assert iocs["cookie"] == expected_cookie, f"Expected cookie '{expected_cookie}', but got '{iocs['cookie']}'."

    # Verify malicious IPs
    malicious_ips = report_data["malicious_ips"]
    assert isinstance(malicious_ips, list), "The 'malicious_ips' value must be a list."

    expected_ips = ["10.0.5.55", "172.16.0.4"]

    # Check if IPs are correct and sorted
    assert malicious_ips == expected_ips, f"Expected malicious_ips to be {expected_ips}, but got {malicious_ips}."