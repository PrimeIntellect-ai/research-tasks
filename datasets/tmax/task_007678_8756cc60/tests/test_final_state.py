# test_final_state.py

import os
import json

def test_violations_json_exists_and_correct():
    output_path = "/home/user/violations.json"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. Did the program run and generate it?"

    try:
        with open(output_path, 'r') as f:
            actual_data = json.load(f)
    except json.JSONDecodeError:
        assert False, f"The file {output_path} does not contain valid JSON."

    expected_data = [
        {
            "emp_id": "E02",
            "name": "Bob",
            "path": ["E02", "G_Dev", "G_Prod", "sys_finance"]
        },
        {
            "emp_id": "E03",
            "name": "Charlie",
            "path": ["E03", "G_Test", "G_Dev", "G_Prod", "sys_finance"]
        },
        {
            "emp_id": "E06",
            "name": "Frank",
            "path": ["E06", "sys_finance"]
        }
    ]

    assert isinstance(actual_data, list), f"Expected the root JSON element to be a list, got {type(actual_data).__name__}."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} violations, but found {len(actual_data)}."

    # Compare sorted by emp_id to be robust against ordering issues, 
    # though the prompt requires them to be sorted alphabetically by emp_id.
    actual_sorted = sorted(actual_data, key=lambda x: x.get("emp_id", ""))
    expected_sorted = sorted(expected_data, key=lambda x: x["emp_id"])

    # First check if it was already sorted
    assert actual_data == actual_sorted, "The output JSON array is not sorted alphabetically by 'emp_id'."

    for i, (actual, expected) in enumerate(zip(actual_sorted, expected_sorted)):
        assert actual.get("emp_id") == expected["emp_id"], f"Mismatch at index {i}: Expected emp_id {expected['emp_id']}, got {actual.get('emp_id')}."
        assert actual.get("name") == expected["name"], f"Mismatch at index {i}: Expected name {expected['name']}, got {actual.get('name')}."
        assert actual.get("path") == expected["path"], f"Mismatch at index {i}: Expected path {expected['path']}, got {actual.get('path')}."