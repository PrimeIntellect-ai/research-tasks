# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"
SCRIPT_PATH = "/home/user/analyze_backups.py"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script file {SCRIPT_PATH} is missing."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} is missing."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file."

def test_report_contents():
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} does not contain valid JSON.")

    # Check required keys
    required_keys = {"shortest_path", "total_cost", "most_critical_node"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"Report JSON is missing required keys: {missing_keys}"

    # Check types
    assert isinstance(data["shortest_path"], list), "'shortest_path' must be a list."
    assert all(isinstance(x, str) for x in data["shortest_path"]), "All items in 'shortest_path' must be strings."
    assert isinstance(data["total_cost"], int), "'total_cost' must be an integer."
    assert isinstance(data["most_critical_node"], str), "'most_critical_node' must be a string."

    # Check values
    assert data["shortest_path"] == ["ROOT", "C", "TARGET"], "Incorrect shortest path."
    assert data["total_cost"] == 25, "Incorrect total cost."
    assert data["most_critical_node"] == "CRITICAL", "Incorrect most critical node."