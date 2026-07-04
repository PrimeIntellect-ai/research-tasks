# test_final_state.py

import os
import json
import pytest

def test_network_changes_json_exists():
    """Test that the output JSON file exists."""
    file_path = "/home/user/network_changes.json"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_network_changes_json_content():
    """Test that the output JSON file contains the correct filtered and sorted records."""
    file_path = "/home/user/network_changes.json"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {file_path} as JSON: {e}")

    expected_data = [
        {
            "timestamp": 1704067200,
            "key": "system.network.dns",
            "value": "8.8.8.8"
        },
        {
            "timestamp": 1705000000,
            "key": "network.eth0.ip",
            "value": "10.0.0.5"
        },
        {
            "timestamp": 1705500000,
            "key": "network.eth0.mtu",
            "value": "1500"
        }
    ]

    assert isinstance(data, list), f"Expected JSON root to be a list, got {type(data).__name__}."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Expected record {i} to be a dictionary, got {type(actual).__name__}."

        # Check keys
        for key in ["timestamp", "key", "value"]:
            assert key in actual, f"Record {i} is missing required key '{key}'."
            assert actual[key] == expected[key], f"Record {i} '{key}' mismatch: expected {expected[key]}, got {actual[key]}."