# test_final_state.py

import os
import json

def test_compliance_report_exists_and_correct():
    report_path = "/home/user/compliance_report.json"

    assert os.path.isfile(report_path), f"Compliance report not found at {report_path}."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {report_path} is not valid JSON."

    # Check root keys
    expected_keys = {"cookie_security", "missing_security_headers", "redacted_users"}
    assert set(report.keys()) == expected_keys, f"Report keys do not match. Expected {expected_keys}, got {set(report.keys())}."

    # Check cookie_security
    cookie_sec = report["cookie_security"]
    assert cookie_sec.get("has_httponly") is True, "Expected 'has_httponly' to be True."
    assert cookie_sec.get("has_secure") is False, "Expected 'has_secure' to be False."

    # Check missing_security_headers
    missing_headers = report["missing_security_headers"]
    expected_missing_headers = ["Content-Security-Policy", "Strict-Transport-Security"]
    assert isinstance(missing_headers, list), "'missing_security_headers' should be a list."
    assert sorted(missing_headers) == expected_missing_headers, f"Expected missing headers {expected_missing_headers}, got {missing_headers}."

    # Check redacted_users
    redacted_users = report["redacted_users"]
    assert isinstance(redacted_users, list), "'redacted_users' should be a list."
    assert len(redacted_users) == 2, f"Expected 2 redacted users, got {len(redacted_users)}."

    expected_users = [
        {"name": "Alice Smith", "ssn": "***-**-****", "role": "Manager"},
        {"name": "Bob Jones", "ssn": "***-**-****", "role": "Developer"}
    ]

    # Sort both lists by name to ensure order doesn't cause a failure
    redacted_users_sorted = sorted(redacted_users, key=lambda x: x.get("name", ""))
    expected_users_sorted = sorted(expected_users, key=lambda x: x.get("name", ""))

    assert redacted_users_sorted == expected_users_sorted, f"Redacted users do not match expected output. Got {redacted_users}."