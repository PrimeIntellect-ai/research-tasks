# test_final_state.py

import os
import json
import pytest

SCRIPT_PATH = "/home/user/generate_report.sh"
REPORT_PATH = "/home/user/report.json"

def test_script_exists_and_executable():
    """Verify that the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable."

def test_report_exists():
    """Verify that the JSON report file exists."""
    assert os.path.isfile(REPORT_PATH), f"Report missing at {REPORT_PATH}"

def test_report_content():
    """Verify that the JSON report contains the correct data."""
    try:
        with open(REPORT_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "Report JSON must be an array of objects."

    expected_data = [
        {"id": 1, "name": "Core", "type": "System", "total_cost": 310, "cost_rank": 1},
        {"id": 2, "name": "Module A", "type": "Module", "total_cost": 100, "cost_rank": 2},
        {"id": 3, "name": "Module B", "type": "Module", "total_cost": 110, "cost_rank": 1},
        {"id": 4, "name": "Sub A1", "type": "Submodule", "total_cost": 20, "cost_rank": 3},
        {"id": 5, "name": "Sub A2", "type": "Submodule", "total_cost": 30, "cost_rank": 2},
        {"id": 6, "name": "Sub B1", "type": "Submodule", "total_cost": 40, "cost_rank": 1},
        {"id": 7, "name": "Sub B2", "type": "Submodule", "total_cost": 10, "cost_rank": 4}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, but found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        for key in ["id", "name", "type", "total_cost", "cost_rank"]:
            assert key in actual, f"Item at index {i} is missing key '{key}'"
            assert actual[key] == expected[key], f"Mismatch at index {i} for key '{key}': expected {expected[key]}, got {actual[key]}"