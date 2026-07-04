# test_final_state.py

import os
import json
import pytest

REPORT_FILE = "/home/user/policy_report.json"
SCRIPT_FILE = "/home/user/policy_check.py"

def test_script_exists():
    assert os.path.isfile(SCRIPT_FILE), f"The script {SCRIPT_FILE} does not exist. Did you create it?"

def test_report_file_exists():
    assert os.path.isfile(REPORT_FILE), f"The report file {REPORT_FILE} does not exist. Did you run your script?"

def test_report_file_content():
    try:
        with open(REPORT_FILE, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {REPORT_FILE} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {REPORT_FILE}: {e}")

    expected_keys = {"vulnerable_dependency_found", "intrusion_detected", "certificate_valid"}
    assert set(data.keys()) == expected_keys, f"JSON keys mismatch. Expected {expected_keys}, got {set(data.keys())}"

    assert data["vulnerable_dependency_found"] is True, "Expected 'vulnerable_dependency_found' to be True based on the requirements.txt"
    assert data["intrusion_detected"] is True, "Expected 'intrusion_detected' to be True based on the traffic.log"
    assert data["certificate_valid"] is True, "Expected 'certificate_valid' to be True based on the valid certificate chain"