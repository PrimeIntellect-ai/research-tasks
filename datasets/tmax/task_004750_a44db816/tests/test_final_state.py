# test_final_state.py

import os
import json
import pytest

def test_department_influence_json_exists():
    path = "/home/user/department_influence.json"
    assert os.path.isfile(path), f"Output file {path} is missing."

def test_department_influence_json_content():
    path = "/home/user/department_influence.json"
    assert os.path.isfile(path), f"Output file {path} is missing."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert isinstance(data, list), f"JSON data in {path} must be a list (array)."

    expected_data = [
        {"department": "Engineering", "total_in_degree": 9},
        {"department": "HR", "total_in_degree": 0},
        {"department": "Marketing", "total_in_degree": 3},
        {"department": "Sales", "total_in_degree": 2}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} departments, but got {len(data)}."

    for i, expected_item in enumerate(expected_data):
        actual_item = data[i]
        assert "department" in actual_item, f"Missing 'department' key in item {i}."
        assert "total_in_degree" in actual_item, f"Missing 'total_in_degree' key in item {i}."

        assert actual_item["department"] == expected_item["department"], \
            f"Expected department '{expected_item['department']}' at index {i}, but got '{actual_item['department']}'. Ensure the list is sorted alphabetically."
        assert actual_item["total_in_degree"] == expected_item["total_in_degree"], \
            f"Expected total_in_degree {expected_item['total_in_degree']} for department '{expected_item['department']}', but got {actual_item['total_in_degree']}."

def test_json_formatting():
    path = "/home/user/department_influence.json"
    assert os.path.isfile(path), f"Output file {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check for basic 2-space indentation formatting as requested
    assert "[\n  {\n" in content or "[\r\n  {\r\n" in content, "JSON file does not appear to be formatted with 2-space indentation."