# test_final_state.py

import os
import json
import pytest

SCRIPT_PATH = "/home/user/project/check_abi.sh"
REPORT_PATH = "/home/user/project/report.json"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_report_exists_and_valid():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    assert "status" in data, "'status' key missing in report.json"
    assert "highest_glibc_detected" in data, "'highest_glibc_detected' key missing in report.json"
    assert "missing_exports" in data, "'missing_exports' key missing in report.json"

def test_report_content():
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    assert data.get("status") == "FAIL", f"Expected status 'FAIL', got '{data.get('status')}'"

    missing = data.get("missing_exports", [])
    assert isinstance(missing, list), "'missing_exports' must be a list"
    assert "cleanup" in missing, "'cleanup' should be in 'missing_exports'"
    assert len(missing) == 1, f"Expected exactly 1 missing export ('cleanup'), got {len(missing)}"

    glibc = data.get("highest_glibc_detected")
    assert isinstance(glibc, str) and len(glibc) > 0, "'highest_glibc_detected' should be a non-empty string"