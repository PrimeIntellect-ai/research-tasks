# test_final_state.py

import os
import json
import pytest

def test_output_jsonl_exists_and_correct():
    output_path = "/home/user/config_tracker/output.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. Did the Rust program run successfully?"

    with open(output_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 valid entries in output.jsonl, but found {len(lines)}."

    try:
        entry1 = json.loads(lines[0])
        entry2 = json.loads(lines[1])
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse lines in output.jsonl as JSON: {e}")

    # Validate first entry (srv-3)
    assert entry1.get("server_id") == "srv-3", f"Expected first entry server_id to be 'srv-3', got '{entry1.get('server_id')}'"
    assert entry1.get("timestamp") == "2023-10-31T08:13:20Z", f"Expected first entry timestamp to be '2023-10-31T08:13:20Z', got '{entry1.get('timestamp')}'"
    assert entry1.get("description") == "Mise à jour du réseau", "Incorrect description for the first entry"

    # Check config_payload (can be a string or parsed JSON depending on how it was written, but spec says it's a JSON string representing the new config)
    # The spec says: config_payload (string): A JSON string representing the new configuration.
    payload1 = entry1.get("config_payload")
    assert isinstance(payload1, str), "config_payload must be a string"
    assert json.loads(payload1) == {"port": 8080}, "Incorrect config_payload content for the first entry"

    # Validate second entry (srv-6)
    assert entry2.get("server_id") == "srv-6", f"Expected second entry server_id to be 'srv-6', got '{entry2.get('server_id')}'"
    assert entry2.get("timestamp") == "2023-11-01T14:46:40Z", f"Expected second entry timestamp to be '2023-11-01T14:46:40Z', got '{entry2.get('timestamp')}'"
    assert entry2.get("description") == "Add new cache node", "Incorrect description for the second entry"

    payload2 = entry2.get("config_payload")
    assert isinstance(payload2, str), "config_payload must be a string"
    assert json.loads(payload2) == {"cache": "redis"}, "Incorrect config_payload content for the second entry"