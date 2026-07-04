# test_final_state.py
import os
import json
import pytest

def test_recovered_configs_json_exists():
    """Check if the recovered_configs.json file was created."""
    filepath = "/home/user/recovered_configs.json"
    assert os.path.exists(filepath), f"Expected file {filepath} does not exist. Did you run your C++ program?"
    assert os.path.isfile(filepath), f"Expected {filepath} to be a file."

def test_recovered_configs_json_content():
    """Check if the recovered_configs.json contains the correct parsed payloads."""
    filepath = "/home/user/recovered_configs.json"

    assert os.path.exists(filepath), f"File {filepath} is missing."

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse {filepath} as JSON: {e}")

    expected = [
        "server_port=8080\nmax_connections=100",
        "server_port=8081\nmax_connections=200\nenable_cache=true",
        "server_port=8081\nmax_connections=250\nenable_cache=true\nlog_level=debug"
    ]

    assert isinstance(data, list), f"Expected JSON root to be a list, but got {type(data).__name__}"
    assert len(data) == len(expected), f"Expected {len(expected)} records, but got {len(data)}. Ensure truncated records are discarded."

    for i, (actual_record, expected_record) in enumerate(zip(data, expected)):
        assert actual_record == expected_record, f"Record at index {i} does not match expected payload.\nExpected:\n{expected_record}\n\nActual:\n{actual_record}"