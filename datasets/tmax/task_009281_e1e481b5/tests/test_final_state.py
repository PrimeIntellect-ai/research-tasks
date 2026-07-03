# test_final_state.py

import os
import json
import pytest

def test_audit_report_exists_and_valid():
    """Test that the audit report exists, is valid JSON, and contains the correct data."""
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"Audit report missing at {report_path}"
    assert os.path.isfile(report_path), f"{report_path} is not a file"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Audit report is not valid JSON")

    assert "csp_is_strict" in data, "Missing 'csp_is_strict' in audit report"
    assert data["csp_is_strict"] is True, "'csp_is_strict' should be true based on csp.txt"

    assert "escalation_attempts" in data, "Missing 'escalation_attempts' in audit report"
    attempts = data["escalation_attempts"]
    assert isinstance(attempts, list), "'escalation_attempts' should be a list"
    assert len(attempts) == 2, f"Expected exactly 2 escalation attempts, found {len(attempts)}"

    expected_attempts = [
        {"ip": "10.0.0.5", "decoded_url": "https://evil.com/admin/escalate?user=test"},
        {"ip": "10.0.0.9", "decoded_url": "https://attacker.net/su/root"}
    ]

    assert attempts == expected_attempts, f"Escalation attempts do not match expected output. Got {attempts}"