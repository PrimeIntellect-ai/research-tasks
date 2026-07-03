# test_final_state.py

import os
import json
import pytest

def test_compliance_report_exists_and_valid():
    report_path = '/home/user/audit_trail/compliance_report.json'

    # Check if the report file exists
    assert os.path.isfile(report_path), f"The compliance report was not found at {report_path}."

    # Read and parse the JSON report
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file at {report_path} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {report_path}: {e}")

    # Verify the structure and values
    assert "sql_injection_count" in data, "The report is missing the 'sql_injection_count' field."
    assert data["sql_injection_count"] == 2, f"Expected 2 SQL injection occurrences, found {data['sql_injection_count']}."

    assert "xss_count" in data, "The report is missing the 'xss_count' field."
    assert data["xss_count"] == 2, f"Expected 2 XSS occurrences, found {data['xss_count']}."

    assert "critical_sudo_users" in data, "The report is missing the 'critical_sudo_users' field."
    expected_users = ["dev_lead", "ops_manager"]
    actual_users = data["critical_sudo_users"]

    assert isinstance(actual_users, list), "The 'critical_sudo_users' field must be a list."
    assert actual_users == expected_users, f"Expected critical sudo users {expected_users}, found {actual_users}. Make sure the list is sorted alphabetically."