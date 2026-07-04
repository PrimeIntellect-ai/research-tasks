# test_final_state.py

import os
import json
import pytest

def test_result_json_exists():
    """Check that the result.json file was created."""
    assert os.path.isfile("/home/user/result.json"), "/home/user/result.json does not exist. The C++ program may not have run or failed to output."

def test_result_json_content():
    """Check that result.json contains the correct shortest path and aggregations."""
    file_path = "/home/user/result.json"

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{file_path} is not a valid JSON file.")
    except Exception as e:
        pytest.fail(f"Could not read {file_path}: {e}")

    assert "path" in data, "The 'path' key is missing from result.json."
    assert "total_latency" in data, "The 'total_latency' key is missing from result.json."
    assert "total_load" in data, "The 'total_load' key is missing from result.json."

    expected_path = ["Gateway", "Router1", "Database"]
    expected_latency = 25
    expected_load = 85

    assert data["path"] == expected_path, f"Expected path {expected_path}, but got {data['path']}."
    assert data["total_latency"] == expected_latency, f"Expected total_latency {expected_latency}, but got {data['total_latency']}."
    assert data["total_load"] == expected_load, f"Expected total_load {expected_load}, but got {data['total_load']}."