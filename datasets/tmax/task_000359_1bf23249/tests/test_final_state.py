# test_final_state.py

import os
import json
import pytest

def test_audit_report_exists_and_valid():
    report_path = "/home/user/audit_report.json"

    assert os.path.exists(report_path), f"The file {report_path} does not exist."
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

    try:
        with open(report_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {report_path} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {report_path}: {e}")

    assert isinstance(data, dict), f"The JSON in {report_path} should be an object (dictionary)."

    expected_auth_cwe = "CWE-287"
    expected_privesc_cwe = "CWE-269"
    expected_secret_flag = "COMPLIANCE_FLAG_{7h3_4ud17_15_c0mpl373}"

    assert "auth_cwe" in data, "The 'auth_cwe' key is missing from the audit report."
    assert data["auth_cwe"] == expected_auth_cwe, f"Expected auth_cwe to be '{expected_auth_cwe}', got '{data['auth_cwe']}'."

    assert "privesc_cwe" in data, "The 'privesc_cwe' key is missing from the audit report."
    assert data["privesc_cwe"] == expected_privesc_cwe, f"Expected privesc_cwe to be '{expected_privesc_cwe}', got '{data['privesc_cwe']}'."

    assert "secret_flag" in data, "The 'secret_flag' key is missing from the audit report."
    assert data["secret_flag"] == expected_secret_flag, f"Expected secret_flag to be '{expected_secret_flag}', got '{data['secret_flag']}'."