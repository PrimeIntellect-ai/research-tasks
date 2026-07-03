# test_final_state.py

import os
import json
import pytest

def test_suspicious_cycle_json_exists():
    """Test that the output JSON file exists."""
    file_path = "/home/user/suspicious_cycle.json"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

def test_suspicious_cycle_json_content():
    """Test that the output JSON file contains the correct sorted account IDs."""
    file_path = "/home/user/suspicious_cycle.json"

    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not a valid JSON file.")

    expected_data = ["ACC_101", "ACC_102", "ACC_103", "ACC_104"]

    assert isinstance(data, list), f"Expected JSON root to be a list, got {type(data).__name__}."
    assert data == expected_data, f"JSON content is incorrect. Expected {expected_data}, got {data}."