# test_final_state.py
import os
import json
import pytest

def test_connection_history_json():
    """Verify that the JSON output file exists and contains the correct data."""
    output_path = "/home/user/connection_history.json"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist. The script must generate this file."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} is not a valid JSON file.")

    expected_data = {
        "state_01.tar.gz": 150,
        "state_03.tar.gz": 200,
        "state_04.tar.gz": 500
    }

    assert data == expected_data, f"The content of {output_path} is incorrect. Expected {expected_data}, but got {data}."