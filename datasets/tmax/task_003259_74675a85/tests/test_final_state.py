# test_final_state.py

import os
import json
import pytest

ANOMALIES_FILE = "/home/user/anomalies.json"

def test_anomalies_file_exists():
    assert os.path.isfile(ANOMALIES_FILE), f"The file {ANOMALIES_FILE} does not exist."

def test_anomalies_json_format():
    with open(ANOMALIES_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {ANOMALIES_FILE} is not valid JSON.")

    # Validate schema structure
    assert isinstance(data, dict), "The root of the JSON must be an object."
    assert "anomalies" in data, "The JSON object must contain the 'anomalies' key."
    assert isinstance(data["anomalies"], list), "The 'anomalies' property must be an array."

    for item in data["anomalies"]:
        assert isinstance(item, dict), "Each item in 'anomalies' must be an object."
        for req_key in ["child_backup_id", "parent_backup_id", "chain_root_id"]:
            assert req_key in item, f"Missing required key '{req_key}' in anomaly item."
            assert isinstance(item[req_key], str), f"The value for '{req_key}' must be a string."

def test_anomalies_content():
    with open(ANOMALIES_FILE, 'r') as f:
        data = json.load(f)

    expected_anomalies = [
        {"child_backup_id": "B3", "parent_backup_id": "B2", "chain_root_id": "B1"},
        {"child_backup_id": "D2", "parent_backup_id": "D1", "chain_root_id": "D1"}
    ]

    actual_anomalies = data.get("anomalies", [])

    assert len(actual_anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies, but found {len(actual_anomalies)}."

    # Sort both lists by child_backup_id to compare order-independently
    sorted_actual = sorted(actual_anomalies, key=lambda x: x.get("child_backup_id", ""))
    sorted_expected = sorted(expected_anomalies, key=lambda x: x["child_backup_id"])

    assert sorted_actual == sorted_expected, "The anomalies reported do not match the expected anomalies."