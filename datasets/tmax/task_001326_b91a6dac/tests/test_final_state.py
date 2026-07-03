# test_final_state.py

import os
import json
import pytest

RESULT_PATH = '/home/user/routing_result.json'

def test_routing_result_exists():
    assert os.path.exists(RESULT_PATH), f"Output file {RESULT_PATH} does not exist."
    assert os.path.isfile(RESULT_PATH), f"{RESULT_PATH} is not a file."

def test_routing_result_contents():
    with open(RESULT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON from {RESULT_PATH}: {e}")

    assert "source" in data, "Missing 'source' key in JSON output."
    assert data["source"] == "API_Gateway", f"Expected source to be 'API_Gateway', got {data['source']}"

    assert "destination" in data, "Missing 'destination' key in JSON output."
    assert data["destination"] == "User_Master", f"Expected destination to be 'User_Master', got {data['destination']}"

    assert "total_latency_ms" in data, "Missing 'total_latency_ms' key in JSON output."
    assert isinstance(data["total_latency_ms"], int), "'total_latency_ms' must be an integer."
    assert data["total_latency_ms"] == 22, f"Expected total_latency_ms to be 22, got {data['total_latency_ms']}"

    assert "path_nodes" in data, "Missing 'path_nodes' key in JSON output."
    assert isinstance(data["path_nodes"], list), "'path_nodes' must be a list."

    expected_path = ["API_Gateway", "Message_Queue", "User_Master"]
    assert data["path_nodes"] == expected_path, f"Expected path_nodes to be {expected_path}, got {data['path_nodes']}"