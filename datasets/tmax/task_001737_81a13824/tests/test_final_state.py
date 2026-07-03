# test_final_state.py

import os
import json
import pytest

def test_culprit_device_extracted():
    path = "/home/user/culprit_device.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you extract the device ID?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "DEV-8932", f"Expected culprit device ID 'DEV-8932', but found '{content}'"

def test_output_json_exists_and_valid():
    path = "/home/user/output.json"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the fixed script to generate the output?"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert isinstance(data, list), "Output JSON should be a list of records."
    assert len(data) == 3, f"Expected 3 records in output.json, but found {len(data)}."

def test_output_json_contains_correct_standard_time():
    path = "/home/user/output.json"
    if not os.path.isfile(path):
        pytest.fail(f"File {path} is missing.")

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    dev_8932_record = next((r for r in data if r.get("device_id") == "DEV-8932"), None)
    assert dev_8932_record is not None, "Record for DEV-8932 is missing from output.json"

    expected_timestamp = "2023-11-05T01:30:00-05:00"
    actual_timestamp = dev_8932_record.get("timestamp")

    assert actual_timestamp == expected_timestamp, (
        f"Timestamp for DEV-8932 is incorrect. Expected {expected_timestamp} "
        f"(Standard Time), but got {actual_timestamp}. "
        "Make sure ambiguous times default to Standard Time (is_dst=False)."
    )

def test_output_json_contains_other_records():
    path = "/home/user/output.json"
    if not os.path.isfile(path):
        pytest.fail(f"File {path} is missing.")

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    dev_1111_record = next((r for r in data if r.get("device_id") == "DEV-1111"), None)
    assert dev_1111_record is not None, "Record for DEV-1111 is missing from output.json"
    assert dev_1111_record.get("timestamp") == "2023-11-04T14:00:00-04:00", "Timestamp for DEV-1111 is incorrect."

    dev_2222_record = next((r for r in data if r.get("device_id") == "DEV-2222"), None)
    assert dev_2222_record is not None, "Record for DEV-2222 is missing from output.json"
    assert dev_2222_record.get("timestamp") == "2023-11-06T09:15:00-05:00", "Timestamp for DEV-2222 is incorrect."