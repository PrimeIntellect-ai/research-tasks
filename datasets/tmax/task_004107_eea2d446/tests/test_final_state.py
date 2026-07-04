# test_final_state.py

import os
import json
import pytest

JSON_PATH = "/home/user/top_managers.json"

def test_json_file_exists():
    """Check if the output JSON file exists."""
    assert os.path.isfile(JSON_PATH), f"Output JSON file not found at {JSON_PATH}"

def test_json_contents():
    """Check if the JSON file contains the correct results."""
    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON file: {e}")

    assert isinstance(data, list), "JSON output must be a list of objects"
    assert len(data) == 2, f"Expected exactly 2 elements in the output, found {len(data)}"

    # Sort data by dept_name to ensure consistent checking
    data_sorted = sorted(data, key=lambda x: x.get("dept_name", ""))

    expected_engineering = {
        "dept_name": "Engineering",
        "manager_name": "Alice",
        "direct_reports": 2,
        "salary": 120000
    }

    expected_sales = {
        "dept_name": "Sales",
        "manager_name": "Heidi",
        "direct_reports": 1,
        "salary": 90000
    }

    # Verify Engineering
    eng_record = data_sorted[0]
    for key, expected_value in expected_engineering.items():
        assert key in eng_record, f"Missing key '{key}' in Engineering record"
        assert eng_record[key] == expected_value, f"Expected {key}={expected_value} for Engineering, found {eng_record[key]}"

    # Verify Sales
    sales_record = data_sorted[1]
    for key, expected_value in expected_sales.items():
        assert key in sales_record, f"Missing key '{key}' in Sales record"
        assert sales_record[key] == expected_value, f"Expected {key}={expected_value} for Sales, found {sales_record[key]}"