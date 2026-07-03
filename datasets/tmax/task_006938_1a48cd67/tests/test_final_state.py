# test_final_state.py
import os
import json
import pytest

def test_audit_report_exists():
    assert os.path.isfile("/home/user/audit_report.json"), "The file /home/user/audit_report.json does not exist."

def test_audit_report_structure():
    with open("/home/user/audit_report.json", "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/audit_report.json is not valid JSON.")

    assert "scanned_files" in report, "The report is missing the 'scanned_files' key."
    assert "vulnerabilities" in report, "The report is missing the 'vulnerabilities' key."

    assert report["scanned_files"] == 3, f"Expected 3 scanned_files, but got {report['scanned_files']}."

    vulns = report["vulnerabilities"]
    assert isinstance(vulns, list), "The 'vulnerabilities' key must be a list."

    for v in vulns:
        assert "file" in v, f"Vulnerability entry missing 'file' key: {v}"
        assert "type" in v, f"Vulnerability entry missing 'type' key: {v}"
        assert "line_number" in v, f"Vulnerability entry missing 'line_number' key: {v}"

def test_audit_report_content():
    with open("/home/user/audit_report.json", "r") as f:
        report = json.load(f)

    vulns = report["vulnerabilities"]

    # Check sorting
    sorted_vulns = sorted(vulns, key=lambda x: (x["file"], x["line_number"]))
    assert vulns == sorted_vulns, "The vulnerabilities list is not sorted alphabetically by file name, then by line_number in ascending order."

    # Expected vulnerabilities based on the provided truth
    expected = [
        {"file": "/home/user/scripts/backup_service.py", "type": "credential_leakage", "line_number": 8},
        {"file": "/home/user/scripts/user_mgmt.py", "type": "command_injection", "line_number": 5},
        {"file": "/home/user/scripts/user_mgmt.py", "type": "credential_leakage", "line_number": 9},
        {"file": "/home/user/scripts/user_mgmt.py", "type": "command_injection", "line_number": 9}
    ]

    # Sort expected to match the required order
    expected_sorted = sorted(expected, key=lambda x: (x["file"], x["line_number"]))

    # Check lengths
    assert len(vulns) == len(expected_sorted), f"Expected {len(expected_sorted)} vulnerabilities, but found {len(vulns)}."

    for exp in expected_sorted:
        assert exp in vulns, f"Expected vulnerability not found in report: {exp}"