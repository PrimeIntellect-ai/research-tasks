# test_final_state.py

import os
import json
import subprocess
import pytest

def test_audit_report_content():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {report_path} is not valid JSON.")

    expected_data = {
        "employee_id": "E-7734",
        "name": "Jordan Cole",
        "department_name": "Equities",
        "risk_level": 4,
        "total_trade_volume": 1450000.50,
        "number_of_flagged_trades": 3
    }

    # Check types and values
    assert data.get("employee_id") == expected_data["employee_id"], "Incorrect employee_id"
    assert data.get("name") == expected_data["name"], "Incorrect name"
    assert data.get("department_name") == expected_data["department_name"], "Incorrect department_name"
    assert data.get("risk_level") == expected_data["risk_level"], "Incorrect risk_level"
    assert data.get("total_trade_volume") == expected_data["total_trade_volume"], "Incorrect total_trade_volume"
    assert data.get("number_of_flagged_trades") == expected_data["number_of_flagged_trades"], "Incorrect number_of_flagged_trades"

def test_adversarial_validator():
    validator_script = "/home/user/query_validator.py"
    assert os.path.isfile(validator_script), f"Validator script not found at {validator_script}"

    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_rejected = []

    for filepath in evil_files:
        result = subprocess.run(["python3", validator_script, filepath], capture_output=True, text=True)
        if result.returncode != 1 or "REJECT" not in result.stdout:
            evil_bypassed.append(os.path.basename(filepath))

    for filepath in clean_files:
        result = subprocess.run(["python3", validator_script, filepath], capture_output=True, text=True)
        if result.returncode != 0 or "ACCEPT" not in result.stdout:
            clean_rejected.append(os.path.basename(filepath))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_msgs.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))