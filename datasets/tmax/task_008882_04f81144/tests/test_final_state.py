# test_final_state.py

import os
import json
import pytest

def test_audit_report_exists():
    """Check if the audit report file was created."""
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"File {report_path} does not exist. The script must write the output to this file."

def test_audit_report_content():
    """Check if the audit report contains the correct flag."""
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {report_path} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {report_path}: {e}")

    expected_flag = "FLAG{alg_none_mtls_bypass_success}"

    assert "flag" in data, "The JSON output does not contain the 'flag' key."
    assert data["flag"] == expected_flag, f"The flag in the report is incorrect. Expected {expected_flag}, but got {data['flag']}."

    assert data.get("status") == "vulnerable", "The JSON output does not contain the expected 'status' value."