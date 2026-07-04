# test_final_state.py
import os
import json
import pytest

def test_result_json_exists_and_correct():
    result_path = '/home/user/result.json'

    assert os.path.exists(result_path), f"Expected output file not found at {result_path}"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON in {result_path}: {e}")

    assert "source" in data, "JSON missing required key 'source'"
    assert data["source"] == "user1", f"Expected source to be 'user1', got '{data['source']}'"

    assert "transitive_connections" in data, "JSON missing required key 'transitive_connections'"

    expected_connections = ["user2", "user3", "user4", "user7"]
    actual_connections = data["transitive_connections"]

    assert isinstance(actual_connections, list), "'transitive_connections' must be a list"

    # Check if they match regardless of order first, to give a better error message if missing
    assert sorted(actual_connections) == expected_connections, \
        f"Expected transitive_connections to contain {expected_connections}, got {sorted(actual_connections)}"

    # Check if the output list is sorted as requested
    assert actual_connections == expected_connections, \
        f"Expected transitive_connections to be sorted alphabetically: {expected_connections}, got {actual_connections}"