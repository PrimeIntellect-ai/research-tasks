# test_final_state.py
import os
import json
import pytest

OUTPUT_FILE = '/home/user/bom_flattened.json'

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing. Did you run the script and save the output to the correct path?"
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a file."

def test_output_file_content():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing."

    with open(OUTPUT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_FILE} does not contain valid JSON.")

    assert isinstance(data, list), "The output JSON must be an array of objects."

    expected_data = [
        {
            "component_id": 2,
            "component_name": "Sub-Assembly A",
            "total_quantity": 2
        },
        {
            "component_id": 3,
            "component_name": "Sub-Assembly B",
            "total_quantity": 1
        },
        {
            "component_id": 4,
            "component_name": "Part C",
            "total_quantity": 6
        },
        {
            "component_id": 5,
            "component_name": "Part D",
            "total_quantity": 10
        },
        {
            "component_id": 6,
            "component_name": "Standard Screw",
            "total_quantity": 62
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} components in the output, but found {len(data)}."

    for i, expected_item in enumerate(expected_data):
        actual_item = data[i]
        assert isinstance(actual_item, dict), f"Item at index {i} is not a JSON object."

        for key in ["component_id", "component_name", "total_quantity"]:
            assert key in actual_item, f"Missing key '{key}' in item at index {i}."
            assert actual_item[key] == expected_item[key], f"Mismatch for '{key}' at index {i}. Expected {expected_item[key]}, got {actual_item[key]}."