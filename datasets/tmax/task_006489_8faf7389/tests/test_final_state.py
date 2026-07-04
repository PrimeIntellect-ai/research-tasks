# test_final_state.py

import os
import json

def test_audit_script_exists():
    """Test that the audit.py script was created."""
    script_path = "/home/user/audit.py"
    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_audit_report_exists():
    """Test that the audit_report.json file was generated."""
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"The report file {report_path} is missing. Did you run the script?"
    assert os.path.isfile(report_path), f"The path {report_path} is not a file."

def test_audit_report_content():
    """Test that the audit_report.json contains the correct aggregated data."""
    report_path = "/home/user/audit_report.json"

    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"The file {report_path} does not contain valid JSON."
    except Exception as e:
        assert False, f"Could not read {report_path}: {e}"

    expected_data = {
        "Alice": 2,
        "Bob": 1
    }

    assert data == expected_data, f"The report content is incorrect. Expected {expected_data}, but got {data}."