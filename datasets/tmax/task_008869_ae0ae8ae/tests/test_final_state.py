# test_final_state.py

import os
import json
import pytest

def test_tracker_go_exists():
    """Verify that the Go script was created at the correct location."""
    script_path = "/home/user/tracker.go"
    assert os.path.isfile(script_path), f"Go script {script_path} is missing. Please ensure you created it."

def test_final_state_json_exists():
    """Verify that the final state JSON file was generated."""
    output_path = "/home/user/final_state.json"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. Please ensure your script generates it."

def test_final_state_json_content():
    """Verify that the final state JSON contains the exact expected values."""
    output_path = "/home/user/final_state.json"

    # Ensure the file exists before trying to read it
    if not os.path.isfile(output_path):
        pytest.fail(f"Cannot verify content because {output_path} does not exist.")

    try:
        with open(output_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {output_path} does not contain valid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read {output_path}: {e}")

    expected = {
        "app_version": "1.1.0",
        "app_debug": True,
        "db_host": "db.internal.corp",
        "db_port": 5433,
        "route_count": 4
    }

    # Verify each expected key and its value
    for key, expected_value in expected.items():
        assert key in data, f"Missing key '{key}' in {output_path}."
        assert data[key] == expected_value, f"Incorrect value for '{key}'. Expected {expected_value}, but got {data[key]}."