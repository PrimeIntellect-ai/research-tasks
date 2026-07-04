# test_final_state.py

import os
import json

def test_security_report_exists():
    report_path = "/home/user/security_report.json"
    assert os.path.exists(report_path), f"The security report was not found at {report_path}."

def test_security_report_content():
    report_path = "/home/user/security_report.json"
    assert os.path.exists(report_path), f"The security report was not found at {report_path}."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "The security report does not contain valid JSON."

    assert isinstance(data, list), "The security report JSON should be a list of history events."

    # Check if the expected response is in the history
    expected_substring = "Status: token_verified_securely"
    found = any(expected_substring in item for item in data if isinstance(item, str))

    assert found, f"The expected string '{expected_substring}' was not found in the security report. This indicates the API or the emulator did not function correctly."