# test_final_state.py

import os
import json
import pytest

SCRIPT_PATH = '/home/user/process_routes.py'
RESULTS_PATH = '/home/user/route_results.json'

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script file {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file."

def test_results_file_exists():
    assert os.path.exists(RESULTS_PATH), f"Results file {RESULTS_PATH} does not exist."
    assert os.path.isfile(RESULTS_PATH), f"Path {RESULTS_PATH} is not a file."

def test_results_content():
    with open(RESULTS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} does not contain valid JSON.")

    expected_data = [
        {
            "destination_id": 5,
            "destination_name": "Warehouse_D",
            "total_transit_time": 15
        },
        {
            "destination_id": 4,
            "destination_name": "Warehouse_C",
            "total_transit_time": 17
        },
        {
            "destination_id": 6,
            "destination_name": "Warehouse_E",
            "total_transit_time": 17
        }
    ]

    assert isinstance(data, list), "JSON root should be a list."
    assert len(data) == 3, f"Expected exactly 3 records, got {len(data)}."

    for i, expected_record in enumerate(expected_data):
        actual_record = data[i]
        assert isinstance(actual_record, dict), f"Record at index {i} is not a JSON object."

        # Check keys
        expected_keys = {"destination_id", "destination_name", "total_transit_time"}
        actual_keys = set(actual_record.keys())
        assert actual_keys == expected_keys, f"Record at index {i} has incorrect keys. Expected {expected_keys}, got {actual_keys}."

        # Check values
        assert actual_record["destination_id"] == expected_record["destination_id"], \
            f"Record {i}: expected destination_id {expected_record['destination_id']}, got {actual_record['destination_id']}."
        assert actual_record["destination_name"] == expected_record["destination_name"], \
            f"Record {i}: expected destination_name '{expected_record['destination_name']}', got '{actual_record['destination_name']}'."
        assert actual_record["total_transit_time"] == expected_record["total_transit_time"], \
            f"Record {i}: expected total_transit_time {expected_record['total_transit_time']}, got {actual_record['total_transit_time']}."