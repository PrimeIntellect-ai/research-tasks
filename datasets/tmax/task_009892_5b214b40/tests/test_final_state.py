# test_final_state.py

import os
import json
import pytest

OUTPUT_FILE = '/home/user/blast_radius_p2.json'

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Expected output file {OUTPUT_FILE} does not exist."

def test_output_file_content():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing."

    with open(OUTPUT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_FILE} is not valid JSON.")

    assert isinstance(data, list), "Output should be a JSON array."
    assert len(data) == 3, f"Expected exactly 3 items in the output array (page size 3), found {len(data)}."

    expected_data = [
        {
            "service_id": "SVC-B",
            "service_name": "Billing",
            "priority": 90,
            "impact_distance": 1,
            "server_location": "us-east-1"
        },
        {
            "service_id": "SVC-E",
            "service_name": "Email",
            "priority": 90,
            "impact_distance": 1,
            "server_location": "eu-central-1"
        },
        {
            "service_id": "SVC-H",
            "service_name": "Helpdesk",
            "priority": 50,
            "impact_distance": 1,
            "server_location": "us-east-1"
        }
    ]

    for i, expected_item in enumerate(expected_data):
        actual_item = data[i]
        assert actual_item == expected_item, f"Mismatch at index {i}. Expected {expected_item}, got {actual_item}."