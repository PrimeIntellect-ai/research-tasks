# test_final_state.py

import os
import json
import pytest

def test_logs_downloaded():
    server_logs = "/home/user/server/logs.txt"
    workspace_logs = "/home/user/workspace/logs.txt"

    assert os.path.isfile(workspace_logs), f"The file {workspace_logs} does not exist. Did you download it?"

    with open(server_logs, 'r') as f:
        server_content = f.read()
    with open(workspace_logs, 'r') as f:
        workspace_content = f.read()

    assert server_content == workspace_content, f"The content of {workspace_logs} does not match {server_logs}."

def test_summary_json_exists_and_correct():
    summary_path = "/home/user/workspace/summary.json"

    assert os.path.isfile(summary_path), f"The file {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {summary_path} is not valid JSON.")

    expected_keys = {"min", "max", "final_rolling_avg"}
    assert set(data.keys()) == expected_keys, f"The JSON keys in {summary_path} do not match the expected keys. Found: {list(data.keys())}"

    assert data["min"] == 8, f"Expected 'min' to be 8, but got {data['min']}."
    assert data["max"] == 35, f"Expected 'max' to be 35, but got {data['max']}."

    # 35, 8, 14 -> average is 19.0
    assert data["final_rolling_avg"] == 19.0, f"Expected 'final_rolling_avg' to be 19.0, but got {data['final_rolling_avg']}."