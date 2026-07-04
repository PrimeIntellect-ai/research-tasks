# test_final_state.py

import os
import json
import pytest

SCRIPT_PATH = '/home/user/analyze.sh'
REPORT_PATH = '/home/user/report.json'

def test_analyze_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_report_json_exists_and_valid():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file."

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "JSON output should be a list of objects."

def test_report_json_content():
    expected_data = [
        {"id": 1, "parent_id": None, "cost": 100, "depth": 0, "cost_rank": 1},
        {"id": 3, "parent_id": 1, "cost": 700, "depth": 1, "cost_rank": 1},
        {"id": 2, "parent_id": 1, "cost": 500, "depth": 1, "cost_rank": 2},
        {"id": 6, "parent_id": 3, "cost": 800, "depth": 2, "cost_rank": 1},
        {"id": 5, "parent_id": 2, "cost": 300, "depth": 2, "cost_rank": 2},
        {"id": 7, "parent_id": 3, "cost": 200, "depth": 2, "cost_rank": 3},
        {"id": 4, "parent_id": 2, "cost": 150, "depth": 2, "cost_rank": 4},
        {"id": 8, "parent_id": 6, "cost": 900, "depth": 3, "cost_rank": 1}
    ]

    if not os.path.exists(REPORT_PATH):
        pytest.fail(f"Report file {REPORT_PATH} does not exist.")

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} rows, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("id") == expected["id"], f"Row {i}: Expected id {expected['id']}, got {actual.get('id')}"
        assert actual.get("parent_id") == expected["parent_id"], f"Row {i}: Expected parent_id {expected['parent_id']}, got {actual.get('parent_id')}"
        assert actual.get("cost") == expected["cost"], f"Row {i}: Expected cost {expected['cost']}, got {actual.get('cost')}"
        assert actual.get("depth") == expected["depth"], f"Row {i}: Expected depth {expected['depth']}, got {actual.get('depth')}"
        assert actual.get("cost_rank") == expected["cost_rank"], f"Row {i}: Expected cost_rank {expected['cost_rank']}, got {actual.get('cost_rank')}"