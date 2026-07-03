# test_final_state.py
import os
import json
import pytest

PLANNER_PATH = "/home/user/planner.go"
JSON_PATH = "/home/user/restore_plan.json"

def test_planner_script_exists():
    assert os.path.isfile(PLANNER_PATH), f"Go program {PLANNER_PATH} is missing."

def test_json_output_exists():
    assert os.path.isfile(JSON_PATH), f"Output JSON file {JSON_PATH} is missing."

def test_json_output_content():
    assert os.path.isfile(JSON_PATH), f"Output JSON file {JSON_PATH} is missing."

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert "path" in data, "Key 'path' missing in JSON output."
    assert "total_latency_ms" in data, "Key 'total_latency_ms' missing in JSON output."
    assert "total_backup_gb" in data, "Key 'total_backup_gb' missing in JSON output."

    assert data["path"] == ["Alpha", "Beta", "Delta", "Epsilon"], \
        f"Expected path ['Alpha', 'Beta', 'Delta', 'Epsilon'], but got {data['path']}"

    assert data["total_latency_ms"] == 35, \
        f"Expected total_latency_ms to be 35, but got {data['total_latency_ms']}"

    assert data["total_backup_gb"] == 1000, \
        f"Expected total_backup_gb to be 1000, but got {data['total_backup_gb']}"