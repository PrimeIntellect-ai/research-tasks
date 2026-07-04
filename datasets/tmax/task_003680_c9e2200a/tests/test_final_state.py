# test_final_state.py

import json
import os

def test_top_customers_output():
    json_path = '/home/user/top_customers.json'
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist."

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} does not contain valid JSON."

    assert isinstance(data, list), f"Expected JSON array in {json_path}, got {type(data).__name__}."

    expected_data = [
        {"name": "Charlie", "region": "East", "total_spent": 500.0},
        {"name": "Bob", "region": "South", "total_spent": 250.0},
        {"name": "Diana", "region": "West", "total_spent": 250.0}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in the array, found {len(data)}."

    for i, expected_item in enumerate(expected_data):
        actual_item = data[i]
        assert isinstance(actual_item, dict), f"Item at index {i} must be a JSON object."

        # Check specific fields
        assert actual_item.get("name") == expected_item["name"], \
            f"Expected name '{expected_item['name']}' at index {i}, got '{actual_item.get('name')}'."
        assert actual_item.get("region") == expected_item["region"], \
            f"Expected region '{expected_item['region']}' at index {i}, got '{actual_item.get('region')}'."

        # Handle float comparison safely
        actual_spent = actual_item.get("total_spent")
        assert actual_spent is not None, f"Missing 'total_spent' at index {i}."
        try:
            actual_spent = float(actual_spent)
        except ValueError:
            assert False, f"'total_spent' at index {i} must be a number."

        assert actual_spent == expected_item["total_spent"], \
            f"Expected total_spent {expected_item['total_spent']} at index {i}, got {actual_spent}."