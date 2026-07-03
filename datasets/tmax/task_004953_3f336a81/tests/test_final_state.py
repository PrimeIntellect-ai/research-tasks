# test_final_state.py
import os
import json
import pytest

def test_script_exists():
    script_path = "/home/user/generate_report.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_report_exists():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"The report file {report_path} was not generated."

def test_report_contents():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), "Report file is missing."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file audit_report.json does not contain valid JSON.")

    expected_keys = {"compromised_ips", "vulnerable_keys", "vulnerable_ssh_dirs"}
    assert set(report_data.keys()) == expected_keys, f"The JSON report keys do not match the expected keys. Found: {list(report_data.keys())}"

    # Verify compromised IPs
    expected_ips = ["10.0.0.5", "10.1.1.1"]
    actual_ips = report_data.get("compromised_ips", [])
    assert isinstance(actual_ips, list), "compromised_ips must be a list."
    assert actual_ips == sorted(actual_ips), "compromised_ips list is not sorted alphabetically."
    assert set(actual_ips) == set(expected_ips), f"compromised_ips do not match expected. Expected {expected_ips}, got {actual_ips}."

    # Verify vulnerable keys
    expected_vuln_keys = [
        "/home/user/home_backup/alice/.ssh/id_rsa",
        "/home/user/home_backup/eve/keys/id_rsa"
    ]
    actual_vuln_keys = report_data.get("vulnerable_keys", [])
    assert isinstance(actual_vuln_keys, list), "vulnerable_keys must be a list."
    assert actual_vuln_keys == sorted(actual_vuln_keys), "vulnerable_keys list is not sorted alphabetically."
    assert set(actual_vuln_keys) == set(expected_vuln_keys), f"vulnerable_keys do not match expected. Expected {expected_vuln_keys}, got {actual_vuln_keys}."

    # Verify vulnerable SSH dirs
    expected_vuln_dirs = [
        "/home/user/home_backup/bob/.ssh"
    ]
    actual_vuln_dirs = report_data.get("vulnerable_ssh_dirs", [])
    assert isinstance(actual_vuln_dirs, list), "vulnerable_ssh_dirs must be a list."
    assert actual_vuln_dirs == sorted(actual_vuln_dirs), "vulnerable_ssh_dirs list is not sorted alphabetically."
    assert set(actual_vuln_dirs) == set(expected_vuln_dirs), f"vulnerable_ssh_dirs do not match expected. Expected {expected_vuln_dirs}, got {actual_vuln_dirs}."