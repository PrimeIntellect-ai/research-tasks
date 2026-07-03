# test_final_state.py

import os
import json
import pytest

PIPELINE_PATH = "/home/user/audit_pipeline.py"
REPORT_PATH = "/home/user/compliance_report.json"

def test_audit_pipeline_exists():
    """Test that the audit pipeline script was created."""
    assert os.path.exists(PIPELINE_PATH), f"Audit pipeline script missing at {PIPELINE_PATH}"
    assert os.path.isfile(PIPELINE_PATH), f"Expected a file at {PIPELINE_PATH}"

def test_compliance_report_exists():
    """Test that the compliance report JSON file was created."""
    assert os.path.exists(REPORT_PATH), f"Compliance report missing at {REPORT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"Expected a file at {REPORT_PATH}"

def test_compliance_report_content():
    """Test that the compliance report contains the correct validated JSON data."""
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON from {REPORT_PATH}: {e}")

    assert isinstance(data, list), "The JSON root must be a list."
    assert len(data) == 1, f"Expected exactly 1 cycle in the report, found {len(data)}."

    cycle = data[0]

    # Check cycle_id
    assert "cycle_id" in cycle, "Missing 'cycle_id' in the report object."
    assert cycle["cycle_id"] == 101, f"Expected cycle_id to be 101, got {cycle['cycle_id']}"

    # Check total_volume
    assert "total_volume" in cycle, "Missing 'total_volume' in the report object."
    assert isinstance(cycle["total_volume"], float) or isinstance(cycle["total_volume"], int), "total_volume must be a number."
    assert cycle["total_volume"] == 225.0, f"Expected total_volume to be 225.0, got {cycle['total_volume']}"

    # Check accounts
    assert "accounts" in cycle, "Missing 'accounts' in the report object."
    accounts = cycle["accounts"]
    assert isinstance(accounts, list), "'accounts' must be a list."
    assert len(accounts) == 3, f"Expected 3 accounts in the cycle, found {len(accounts)}."

    expected_accounts = ["ACC_X1", "ACC_X2", "ACC_X3"]
    assert accounts == expected_accounts, f"Expected accounts to be exactly {expected_accounts} (sorted), got {accounts}"