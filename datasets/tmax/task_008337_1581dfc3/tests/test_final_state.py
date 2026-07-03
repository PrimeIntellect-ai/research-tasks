# test_final_state.py

import os
import json

def test_etl_script_exists():
    script_path = "/home/user/etl_script.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_top_employees_json_output():
    json_path = "/home/user/top_employees.json"
    assert os.path.exists(json_path), f"The output file {json_path} does not exist. Did you run your script?"
    assert os.path.isfile(json_path), f"The path {json_path} is not a file."

    with open(json_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {json_path} does not contain valid JSON."

    expected_data = [
        {"name": "Diana Prince", "project_count": 4},
        {"name": "Alice Smith", "project_count": 3},
        {"name": "Frank Miller", "project_count": 3}
    ]

    assert isinstance(actual_data, list), f"The JSON output must be a list of objects, got {type(actual_data).__name__}."
    assert len(actual_data) == 3, f"Expected exactly 3 results, but got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        assert "name" in actual, f"Item at index {i} is missing the 'name' key."
        assert "project_count" in actual, f"Item at index {i} is missing the 'project_count' key."

        # Check types
        assert isinstance(actual["name"], str), f"The 'name' at index {i} should be a string."
        assert isinstance(actual["project_count"], int), f"The 'project_count' at index {i} should be an integer."

        # Check values
        assert actual["name"] == expected["name"], f"Expected name '{expected['name']}' at index {i}, but got '{actual['name']}'."
        assert actual["project_count"] == expected["project_count"], f"Expected project_count {expected['project_count']} for {expected['name']}, but got {actual['project_count']}."

    # Final exact match just to be absolutely sure no extra keys exist
    assert actual_data == expected_data, f"The JSON output does not exactly match the expected list of objects. Expected: {expected_data}, Got: {actual_data}"