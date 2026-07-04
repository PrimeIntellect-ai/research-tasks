# test_final_state.py

import os
import json
import subprocess
import pytest

def test_etl_go_exists():
    """Test that the Go program exists."""
    assert os.path.exists("/home/user/etl.go"), "/home/user/etl.go does not exist."

def test_summary_json_exists_and_correct():
    """Test that summary.json exists and contains the correct aggregated data for 'completed'."""
    summary_path = "/home/user/summary.json"
    assert os.path.exists(summary_path), f"{summary_path} does not exist."

    with open(summary_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{summary_path} does not contain valid JSON.")

    assert isinstance(data, list), "Output must be a JSON array."

    expected = [
        {"user_id": "u001", "total_spend": 40.0},
        {"user_id": "u003", "total_spend": 45.5}
    ]

    # Check length
    assert len(data) == len(expected), f"Expected {len(expected)} records, found {len(data)}."

    # Check contents and order
    for i, exp in enumerate(expected):
        record = data[i]
        assert "user_id" in record, f"Record {i} missing 'user_id'"
        assert "total_spend" in record, f"Record {i} missing 'total_spend'"
        assert record["user_id"] == exp["user_id"], f"Expected user_id {exp['user_id']} at index {i}, got {record['user_id']}"
        assert float(record["total_spend"]) == exp["total_spend"], f"Expected total_spend {exp['total_spend']} at index {i}, got {record['total_spend']}"

def test_etl_go_execution():
    """Test that the Go program can be executed with a different argument and produces correct results."""
    # Run with 'pending'
    result = subprocess.run(
        ["go", "run", "/home/user/etl.go", "pending"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Go program failed to execute: {result.stderr}"

    summary_path = "/home/user/summary.json"
    assert os.path.exists(summary_path), f"{summary_path} was not created after running the program."

    with open(summary_path, "r") as f:
        data = json.load(f)

    expected = [
        {"user_id": "u002", "total_spend": 100.0}
    ]

    assert len(data) == len(expected), f"Expected {len(expected)} records for 'pending', found {len(data)}."
    assert data[0]["user_id"] == "u002", "Expected user_id 'u002' for 'pending' status."
    assert float(data[0]["total_spend"]) == 100.0, "Expected total_spend 100.0 for 'u002'."