# test_final_state.py

import os
import json
import pytest

def test_script_exists():
    script_path = "/home/user/process_logs.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} is missing."

def test_output_file_exists():
    output_path = "/home/user/processed_artifacts.json"
    assert os.path.isfile(output_path), f"Expected output file {output_path} is missing."

def test_output_json_content():
    output_path = "/home/user/processed_artifacts.json"

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} is not valid JSON.")

    assert isinstance(data, list), f"The JSON root in {output_path} must be a list."

    expected_data = [
        {"user": "alice", "ts": 100, "hash": 5863486},
        {"user": "bob", "ts": 110, "hash": 5863816},
        {"user": "alice", "ts": 120, "hash": 5864246},
        {"user": "alice", "ts": 160, "hash": 5865766},
        {"user": "bob", "ts": 165, "hash": 5864281},
        {"user": "bob", "ts": 166, "hash": 5867614}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, but found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Record at index {i} is not a JSON object."
        assert set(actual.keys()) == {"user", "ts", "hash"}, f"Record at index {i} has incorrect keys: {list(actual.keys())}"

        assert actual["user"] == expected["user"], f"Record at index {i} has incorrect 'user'. Expected {expected['user']}, got {actual['user']}."
        assert actual["ts"] == expected["ts"], f"Record at index {i} has incorrect 'ts'. Expected {expected['ts']}, got {actual['ts']}."
        assert actual["hash"] == expected["hash"], f"Record at index {i} has incorrect 'hash'. Expected {expected['hash']}, got {actual['hash']}."