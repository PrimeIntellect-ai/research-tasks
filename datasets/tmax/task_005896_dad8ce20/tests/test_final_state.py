# test_final_state.py

import os
import json
import pytest

def test_report_json_exists_and_correct():
    """Check if report.json exists and contains the expected data."""
    report_path = '/home/user/report.json'
    assert os.path.isfile(report_path), f"Output file {report_path} does not exist. Did you run your script?"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    expected_data = [
        {
            "host_id": 101,
            "host_name": "db-node-01",
            "total_success_mb": 4500
        },
        {
            "host_id": 104,
            "host_name": "db-node-04",
            "total_success_mb": 8000
        }
    ]

    assert isinstance(data, list), "The JSON output should be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in the report, but found {len(data)}."

    # Sort both just in case, though the instructions specify sorting by host_id ascending
    data_sorted = sorted(data, key=lambda x: x.get('host_id', 0))
    expected_sorted = sorted(expected_data, key=lambda x: x['host_id'])

    for i, (actual, expected) in enumerate(zip(data_sorted, expected_sorted)):
        assert actual.get('host_id') == expected['host_id'], f"Item {i}: expected host_id {expected['host_id']}, got {actual.get('host_id')}"
        assert actual.get('host_name') == expected['host_name'], f"Item {i}: expected host_name '{expected['host_name']}', got '{actual.get('host_name')}'"
        assert actual.get('total_success_mb') == expected['total_success_mb'], f"Item {i}: expected total_success_mb {expected['total_success_mb']}, got {actual.get('total_success_mb')}"

def test_script_exists():
    """Check if the python script was created."""
    script_path = '/home/user/generate_report.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."