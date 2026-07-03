# test_final_state.py
import os
import json
import sqlite3
import pytest

SCRIPT_PATH = "/home/user/audit.py"
DB_PATH = "/home/user/financial_logs.db"
OUTPUT_PATH = "/home/user/suspicious_accounts.json"

def test_audit_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Python script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Expected a file at {SCRIPT_PATH}"

def test_output_json_exists():
    assert os.path.exists(OUTPUT_PATH), f"Output JSON file missing at {OUTPUT_PATH}"
    assert os.path.isfile(OUTPUT_PATH), f"Expected a file at {OUTPUT_PATH}"

def test_output_json_contents():
    # Read the output JSON
    try:
        with open(OUTPUT_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File at {OUTPUT_PATH} is not valid JSON.")

    assert isinstance(data, list), "Expected the JSON output to be a list of objects."

    # Expected truth data based on the setup
    expected = [
        {"account_id": "B", "reason": "negative_balance", "trigger_tx_id": "tx_b2"},
        {"account_id": "C", "reason": "rapid_transactions", "trigger_tx_id": "tx_c4"},
        {"account_id": "D", "reason": "negative_balance", "trigger_tx_id": "tx_d2"}
    ]

    assert len(data) == len(expected), f"Expected {len(expected)} records, but found {len(data)}."

    # Check that every expected record is in the output data
    for item in expected:
        assert item in data, f"Missing expected record in output: {item}"

    # Check that no extra records are present
    for item in data:
        assert item in expected, f"Unexpected record found in output: {item}"