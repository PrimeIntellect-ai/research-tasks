# test_final_state.py

import os
import re
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_endpoint.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_exists():
    report_path = "/home/user/investigation_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

def test_report_contents():
    report_path = "/home/user/investigation_report.txt"
    if not os.path.isfile(report_path):
        pytest.fail(f"Report file {report_path} does not exist.")

    with open(report_path, 'r') as f:
        content = f.read()

    # Check CERT_STATUS
    cert_match = re.search(r'^CERT_STATUS:\s*(VALID|INVALID)', content, re.MULTILINE)
    assert cert_match is not None, "CERT_STATUS line is missing or malformed."
    assert cert_match.group(1) == "INVALID", f"Expected CERT_STATUS to be INVALID, but got {cert_match.group(1)}"

    # Check X_INCIDENT_TOKEN
    token_match = re.search(r'^X_INCIDENT_TOKEN:\s*(\S+)', content, re.MULTILINE)
    assert token_match is not None, "X_INCIDENT_TOKEN line is missing or malformed."
    assert token_match.group(1) == "EXFIL_9938_ALPHA", f"Expected X_INCIDENT_TOKEN to be EXFIL_9938_ALPHA, but got {token_match.group(1)}"

    # Check FILE_INTEGRITY
    integrity_match = re.search(r'^FILE_INTEGRITY:\s*(OK|COMPROMISED)', content, re.MULTILINE)
    assert integrity_match is not None, "FILE_INTEGRITY line is missing or malformed."
    assert integrity_match.group(1) == "COMPROMISED", f"Expected FILE_INTEGRITY to be COMPROMISED, but got {integrity_match.group(1)}"