# test_final_state.py

import os
import json
import pytest

def test_analyze_script_exists_and_executable():
    script_path = '/home/user/analyze.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_output_json_exists_and_correct():
    output_path = '/home/user/output.json'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected a JSON array in {output_path}, but got {type(data).__name__}."

    expected_data = [
        {
            "department": "Biology",
            "top_partner": "Chemistry",
            "total_external_weight": 7
        },
        {
            "department": "Chemistry",
            "top_partner": "Math",
            "total_external_weight": 4
        },
        {
            "department": "Math",
            "top_partner": "Chemistry",
            "total_external_weight": 4
        },
        {
            "department": "Physics",
            "top_partner": "Chemistry",
            "total_external_weight": 3
        }
    ]

    # Check length
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(data)}."

    # Check sorting by department name
    departments = [item.get("department") for item in data]
    assert departments == sorted(departments), "The JSON array is not sorted alphabetically by department name."

    # Sort both just in case, though we already checked sorting
    sorted_data = sorted(data, key=lambda x: x.get("department", ""))

    for actual, expected in zip(sorted_data, expected_data):
        assert actual.get("department") == expected["department"], f"Expected department {expected['department']}, got {actual.get('department')}."
        assert actual.get("top_partner") == expected["top_partner"], f"Expected top_partner {expected['top_partner']} for {expected['department']}, got {actual.get('top_partner')}."
        assert actual.get("total_external_weight") == expected["total_external_weight"], f"Expected total_external_weight {expected['total_external_weight']} for {expected['department']}, got {actual.get('total_external_weight')}."