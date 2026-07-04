# test_final_state.py

import os
import json
import pytest

def test_rust_project_exists():
    """Verify that the Rust project directory and Cargo.toml exist."""
    project_dir = "/home/user/org_query"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")

    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found at {cargo_toml}. Did you create a Rust project?"

def test_reports_output_exists():
    """Verify that the reports_output.json file was generated."""
    output_file = "/home/user/reports_output.json"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. Did the program run successfully?"

def test_reports_output_content():
    """Verify the content of the reports_output.json file matches the expected schema and data."""
    output_file = "/home/user/reports_output.json"
    assert os.path.isfile(output_file), "Cannot test output content, file is missing."

    with open(output_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output must be a list (array) of objects."

    expected_data = [
        {"depth": 0, "emp_id": 2, "emp_name": "Bob"},
        {"depth": 1, "emp_id": 4, "emp_name": "David"},
        {"depth": 1, "emp_id": 5, "emp_name": "Eve"},
        {"depth": 2, "emp_id": 7, "emp_name": "Grace"},
        {"depth": 2, "emp_id": 8, "emp_name": "Heidi"},
        {"depth": 2, "emp_id": 9, "emp_name": "Ivan"}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."

        # Check keys
        assert set(actual.keys()) == {"emp_id", "emp_name", "depth"}, f"Item at index {i} has incorrect keys: {list(actual.keys())}"

        # Check values
        assert actual["emp_id"] == expected["emp_id"], f"Item at index {i} has incorrect emp_id: expected {expected['emp_id']}, got {actual['emp_id']}"
        assert actual["emp_name"] == expected["emp_name"], f"Item at index {i} has incorrect emp_name: expected '{expected['emp_name']}', got '{actual['emp_name']}'"
        assert actual["depth"] == expected["depth"], f"Item at index {i} has incorrect depth: expected {expected['depth']}, got {actual['depth']}"

    # Verify sorting explicitly
    emp_ids = [item["emp_id"] for item in data]
    assert emp_ids == sorted(emp_ids), "The JSON array is not sorted by emp_id in ascending order."